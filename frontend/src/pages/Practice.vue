<template>
	<div class="practice-page">
		<header class="practice-header">
			<div class="practice-header-inner">
				<Breadcrumbs class="practice-breadcrumbs" :items="breadcrumbs" />

				<router-link :to="{ name: 'PromptLibrary' }" class="practice-link">
					<Zap class="size-4" />
					{{ __('Prompts') }}
				</router-link>
			</div>
		</header>

		<main v-if="access.loading" class="practice-shell skeleton-wrapper">
			<section class="practice-hero skeleton-hero"></section>
			<section class="practice-panel skeleton-panel"></section>
		</main>

		<main v-else class="practice-shell">
			<section class="practice-hero">
				<div class="practice-hero-copy">
					<div class="practice-eyebrow light">
						<Sparkles class="size-4" />
						{{ __('Simulaciones IA') }}
					</div>

					<h1>
						{{ __('Entrena con IA antes del momento real') }}
					</h1>

					<p>
						{{ __('Practica entrevistas, ventas, inglés o casos de marketing con una simulación guiada por IA. Describe tu situación, sube contexto opcional y entra a practicar.') }}
					</p>

					<div class="practice-hero-actions">
						<button
							class="practice-btn-light"
							:disabled="access.loading || !access.data?.can_start"
							@click="focusForm"
						>
							<Video class="size-4" />
							{{ __('Crear simulación') }}
						</button>

						<router-link
							v-if="access.data && !access.data?.can_start"
							:to="{ name: 'Plus' }"
							class="practice-btn-ghost"
						>
							<Crown class="size-4" />
							{{ __('Desbloquear Plus') }}
						</router-link>
					</div>

					<div class="practice-hero-points">
						<span>
							<CheckCircle2 class="size-4" />
							{{ __('Presión real') }}
						</span>
						<span>
							<CheckCircle2 class="size-4" />
							{{ __('CV opcional') }}
						</span>
						<span>
							<CheckCircle2 class="size-4" />
							{{ __('Feedback con IA') }}
						</span>
					</div>
				</div>

				<aside class="practice-access-card">
					<div class="practice-access-top">
						<div class="practice-access-icon" :class="{ active: access.data?.is_plus }">
							<Crown class="size-5" />
						</div>

						<div>
							<span>{{ __('Tu acceso') }}</span>
							<h2>
								{{ access.data?.is_plus ? __('Plus activo') : __('Plan actual') }}
							</h2>
						</div>
					</div>

					<p v-if="access.data?.is_plus">
						{{ __('Tienes simulaciones ilimitadas incluidas en StudyBadge Plus.') }}
					</p>

					<p v-else-if="access.data?.free_trial_used">
						{{ __('Ya usaste tu práctica gratis. Actualiza a Plus para seguir practicando sin límites.') }}
					</p>

					<p v-else>
						{{ __('Tienes 1 práctica gratis disponible. Luego será exclusivo para Plus.') }}
					</p>

					<div class="practice-meter">
						<span :class="{ active: !access.data?.free_trial_used || access.data?.is_plus }"></span>
						<span :class="{ active: access.data?.is_plus }"></span>
						<span :class="{ active: access.data?.is_plus }"></span>
					</div>

					<router-link
						v-if="!access.data?.is_plus"
						:to="{ name: 'Plus' }"
						class="practice-access-link"
					>
						{{ __('Ver StudyBadge Plus') }}
						<ArrowRight class="size-4" />
					</router-link>
				</aside>
			</section>

			<section ref="formSection" class="practice-panel">
				<div class="practice-panel-head">
					<div>
						<div class="practice-eyebrow">
							<SlidersHorizontal class="size-4" />
							{{ __('Configura tu práctica') }}
						</div>

						<h2>{{ __('Crea tu simulación en 1 minuto') }}</h2>

						<p>
							{{ __('Elige el tipo de práctica y describe tu situación. El idioma, nivel y detalles extra quedan como opciones avanzadas.') }}
						</p>
					</div>

					<div class="practice-pill" :class="{ locked: !access.data?.can_start }">
						{{ access.data?.can_start ? __('Disponible') : __('Plus') }}
					</div>
				</div>

				<div class="practice-form">
					<div class="practice-field full">
						<span>{{ __('1. ¿Qué quieres practicar?') }}</span>

						<div class="practice-type-grid">
							<button
								v-for="option in practiceOptions"
								:key="option.value"
								type="button"
								class="practice-type-card"
								:class="{ active: draft.practice_type === option.value }"
								@click="selectPracticeType(option.value)"
							>
								<div class="practice-type-icon">
									<component :is="option.icon" class="size-5" />
								</div>

								<div>
									<strong>{{ option.label }}</strong>
									<small>{{ option.description }}</small>
								</div>
							</button>
						</div>
					</div>

					<label class="practice-field full">
						<span>{{ __('2. Cuéntale a la IA tu situación') }}</span>

						<textarea
							v-model="draft.goal"
							rows="6"
							:placeholder="selectedPracticeOption.placeholder"
						/>
					</label>

					<div class="practice-examples full">
						<span>{{ __('Ejemplos rápidos') }}</span>

						<div>
							<button
								v-for="example in selectedPracticeOption.examples"
								:key="example"
								type="button"
								@click="applyExample(example)"
							>
								{{ example }}
							</button>
						</div>
					</div>

					<div class="practice-upload full">
						<FileUploader
							ref="fileUploader"
							class="practice-uploader"
							:fileTypes="['.pdf', '.doc', '.docx', '.txt']"
							:uploadArgs="{ private: true }"
							:validateFile="validateFile"
							@success="handleFileUploaded"
						/>

						<div class="practice-upload-info">
							<div class="practice-upload-icon">
								<Upload class="size-5" />
							</div>

							<div>
								<strong>{{ __('CV o contexto opcional') }}</strong>
								<span>
									{{ cvName || __('PDF, Word o texto. Ayuda a que la simulación sea más personalizada.') }}
								</span>
							</div>
						</div>

						<button class="practice-btn-outline" type="button" @click="openUploader">
							<Upload class="size-4" />
							{{ cvName ? __('Cambiar archivo') : __('Subir contexto') }}
						</button>
					</div>

					<div class="practice-advanced full">
						<button class="practice-advanced-toggle" type="button" @click="showAdvanced = !showAdvanced">
							<span>
								<SlidersHorizontal class="size-4" />
								{{ __('Opciones avanzadas') }}
							</span>
							<component :is="showAdvanced ? ChevronUp : ChevronDown" class="size-4" />
						</button>

						<div v-if="showAdvanced" class="practice-advanced-grid">
							<label class="practice-field">
								<span>{{ __('Idioma') }}</span>

								<select v-model="draft.language">
									<option value="es">{{ __('Español') }}</option>
									<option value="en">{{ __('Inglés') }}</option>
								</select>
							</label>

							<label class="practice-field">
								<span>{{ __('Nivel') }}</span>

								<select v-model="draft.level">
									<option value="basico">{{ __('Básico') }}</option>
									<option value="intermedio">{{ __('Intermedio') }}</option>
									<option value="avanzado">{{ __('Avanzado') }}</option>
								</select>
							</label>

							<FormControl
								v-model="draft.role_title"
								class="practice-control"
								:label="__('Rol, puesto o caso específico')"
								:placeholder="__('Ej: SDR SaaS, marketing assistant, cliente molesto')"
							/>
						</div>
					</div>
				</div>

				<div class="practice-submit">
					<p v-if="access.data && !access.data?.can_start" class="practice-warning">
						<Crown class="size-4" />
						{{ __('Tu prueba gratis ya fue usada. Plus desbloquea prácticas ilimitadas.') }}
					</p>

					<button
						class="practice-btn-primary"
						:disabled="!access.data?.can_start || creating"
						@click="createPractice"
					>
						<Video class="size-4" />
						{{ creating ? __('Creando...') : __('Entrar a la sala') }}
					</button>
				</div>
			</section>
		</main>
	</div>
</template>

<script setup>
import { computed, markRaw, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
	Breadcrumbs,
	FileUploader,
	FormControl,
	call,
	createResource,
	toast,
	usePageMeta,
} from 'frappe-ui'
import {
	ArrowRight,
	Briefcase,
	CheckCircle2,
	ChevronDown,
	ChevronUp,
	Crown,
	Languages,
	Megaphone,
	MessageCircle,
	ShoppingBag,
	SlidersHorizontal,
	Sparkles,
	Upload,
	Video,
	Zap,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const router = useRouter()

const formSection = ref(null)
const fileUploader = ref(null)
const creating = ref(false)
const cvName = ref('')
const showAdvanced = ref(false)

const draft = ref({
	practice_type: 'sales',
	language: 'es',
	level: 'intermedio',
	role_title: '',
	company_context: '',
	goal: '',
	cv_file: '',
})

const access = createResource({
	url: 'studybadge_ai.ai_practice.get_practice_access',
	auto: true,
})

const practiceOptions = [
	{
		value: 'interview',
		label: __('Entrevista laboral'),
		description: __('Practica respuestas como en una entrevista real.'),
		placeholder: __('Ej: Quiero practicar una entrevista para asistente de marketing en una empresa de tecnología. Quiero mejorar mis respuestas, sonar más seguro y responder con el método STAR.'),
		examples: [
			__('Entrevista para asistente de marketing'),
			__('Práctica con preguntas difíciles'),
			__('Prepararme para mi primera entrevista'),
		],
		icon: markRaw(Briefcase),
	},
	{
		value: 'sales',
		label: __('Práctica de ventas'),
		description: __('Simula clientes, objeciones y cierre de venta.'),
		placeholder: __('Ej: Vendo cursos de IA para emprendedores en StudyBadge. Quiero practicar con un cliente que dice “está caro”, duda del valor y necesita entender por qué le conviene pagar Plus.'),
		examples: [
			__('Vender StudyBadge Plus'),
			__('Cliente dice que está caro'),
			__('Cerrar una venta por WhatsApp'),
		],
		icon: markRaw(ShoppingBag),
	},
	{
		value: 'english',
		label: __('Inglés conversacional'),
		description: __('Mejora fluidez, respuestas y confianza al hablar.'),
		placeholder: __('Ej: Quiero practicar una conversación en inglés para presentarme, hablar de mis estudios, explicar mi negocio y responder preguntas simples sin quedarme en blanco.'),
		examples: [
			__('Presentarme en inglés'),
			__('Conversación para viaje'),
			__('Entrevista básica en inglés'),
		],
		icon: markRaw(Languages),
	},
	{
		value: 'marketing',
		label: __('Caso de marketing'),
		description: __('Resuelve escenarios de campañas, contenido o estrategia.'),
		placeholder: __('Ej: Quiero practicar un caso de marketing para lanzar una campaña de StudyBadge en TikTok e Instagram con poco presupuesto, buscando usuarios gratis y conversiones a Plus.'),
		examples: [
			__('Campaña para TikTok'),
			__('Mejorar conversión de una landing'),
			__('Lanzar un producto digital'),
		],
		icon: markRaw(Megaphone),
	},
	{
		value: 'custom',
		label: __('Personalizada'),
		description: __('Crea una práctica libre con tus propias reglas.'),
		placeholder: __('Ej: Quiero una simulación donde la IA actúe como un inversionista exigente. Yo presentaré mi idea y la IA debe hacerme preguntas difíciles y darme feedback al final.'),
		examples: [
			__('Simular pitch con inversionista'),
			__('Practicar una negociación'),
			__('Roleplay personalizado'),
		],
		icon: markRaw(MessageCircle),
	},
]

const selectedPracticeOption = computed(() => {
	return practiceOptions.find((option) => option.value === draft.value.practice_type) || practiceOptions[0]
})

const breadcrumbs = computed(() => [
	{
		label: __('Simulaciones IA'),
		route: { name: 'Practice' },
	},
])

usePageMeta(() => ({
	title: __('Simulaciones IA'),
	icon: brand.favicon,
}))

function focusForm() {
	formSection.value?.scrollIntoView({
		behavior: 'smooth',
		block: 'start',
	})
}

function selectPracticeType(value) {
	draft.value.practice_type = value
}

function applyExample(example) {
	draft.value.goal = example
}

function validateFile(file) {
	const ext = file.name.split('.').pop().toLowerCase()

	if (!['pdf', 'doc', 'docx', 'txt'].includes(ext)) {
		return __('Sube PDF, Word o texto.')
	}

	if (file.size > 15 * 1024 * 1024) {
		return __('El archivo supera 15 MB.')
	}
}

function openUploader() {
	const input = fileUploader.value?.$el?.querySelector('input[type="file"]')
	input?.click()
}

function handleFileUploaded(file) {
	draft.value.cv_file = file.file_url
	cvName.value = file.file_name || file.file_url
	toast.success(__('Contexto agregado.'))
}

async function createPractice() {
	if (!draft.value.goal?.trim() && !draft.value.cv_file) {
		toast.error(__('Describe qué quieres practicar o sube un archivo de contexto.'))
		return
	}

	creating.value = true

	try {
		const payload = {
			...draft.value,
			role_title: draft.value.role_title || selectedPracticeOption.value.label,
			company_context: draft.value.company_context || draft.value.goal,
		}

		const session = await call('studybadge_ai.ai_practice.create_practice_session', {
			data: JSON.stringify(payload),
		})

		router.push({
			name: 'PracticeRoom',
			params: { sessionId: session.name },
		})
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo crear la práctica.'))
		access.reload()
	} finally {
		creating.value = false
	}
}
</script>

<style scoped>
.practice-page {
	--practice-primary: #0a2251;
	--practice-primary-hover: #12356f;
	--practice-primary-soft: #eaf1fb;
	--practice-primary-soft-2: #f4f8fd;
	--practice-gold: #f5b301;
	--practice-gold-soft: #fff7db;
	--practice-green: #16a34a;
	--practice-green-soft: #ecfdf3;
	--practice-bg: #f5f8fc;
	--practice-card: #ffffff;
	--practice-text: #0f172a;
	--practice-muted: #475569;
	--practice-soft: #64748b;
	--practice-border: #d7e2f0;
	--practice-border-strong: #b9cbe3;
	--practice-shadow-sm: 0 8px 22px rgba(10, 34, 81, 0.08);
	--practice-shadow-md: 0 18px 45px rgba(10, 34, 81, 0.13);
	--practice-shadow-lg: 0 28px 70px rgba(10, 34, 81, 0.18);

	min-height: 100vh;
	background: var(--practice-bg);
	color: var(--practice-text);
	padding-bottom: 3.5rem;
}

:global(:root[data-theme='dark']) .practice-page {
	--practice-bg: #07111f;
	--practice-card: #101a2b;
	--practice-text: #f8fafc;
	--practice-muted: #cbd5e1;
	--practice-soft: #94a3b8;
	--practice-border: rgba(255, 255, 255, 0.1);
	--practice-border-strong: rgba(255, 255, 255, 0.18);
	--practice-primary-soft: rgba(255, 255, 255, 0.06);
	--practice-primary-soft-2: rgba(255, 255, 255, 0.04);
	--practice-shadow-sm: 0 8px 22px rgba(0, 0, 0, 0.22);
	--practice-shadow-md: 0 18px 45px rgba(0, 0, 0, 0.28);
	--practice-shadow-lg: 0 28px 70px rgba(0, 0, 0, 0.34);
}

.practice-header {
	position: sticky;
	top: 0;
	z-index: 20;
	border-bottom: 1px solid var(--practice-border);
	background: rgba(255, 255, 255, 0.94);
	backdrop-filter: blur(16px);
}

:global(:root[data-theme='dark']) .practice-header {
	background: rgba(7, 17, 31, 0.92);
}

.practice-header-inner {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	width: min(1120px, calc(100% - 32px));
	min-height: 72px;
	margin: 0 auto;
}

.practice-breadcrumbs {
	min-width: 0;
}

.practice-shell {
	display: grid;
	gap: 1.25rem;
	width: min(1120px, calc(100% - 32px));
	margin: 0 auto;
	padding-top: 1.5rem;
}

.practice-hero {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 340px;
	gap: 1rem;
	align-items: stretch;
	overflow: hidden;
	border-radius: 30px;
	background:
		radial-gradient(circle at top right, rgba(245, 179, 1, 0.22), transparent 32%),
		linear-gradient(135deg, #0a2251 0%, #102f66 100%);
	color: #ffffff;
	box-shadow: var(--practice-shadow-lg);
}

.practice-hero-copy {
	display: flex;
	flex-direction: column;
	justify-content: center;
	padding: clamp(1.35rem, 4vw, 2.35rem);
}

.practice-eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	margin-bottom: 0.8rem;
	color: var(--practice-primary);
	font-size: 0.74rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.practice-eyebrow.light {
	border: 1px solid rgba(255, 255, 255, 0.18);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.1);
	padding: 0.45rem 0.75rem;
	color: rgba(255, 255, 255, 0.88);
}

.practice-hero h1 {
	margin: 0;
	max-width: 720px;
	color: #ffffff;
	font-size: clamp(2.15rem, 5vw, 4rem);
	font-weight: 950;
	letter-spacing: -0.06em;
	line-height: 1.02;
}

.practice-hero p {
	margin: 1rem 0 0;
	max-width: 650px;
	color: rgba(255, 255, 255, 0.78);
	font-size: 1rem;
	line-height: 1.75;
}

.practice-hero-actions,
.practice-hero-points {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
}

.practice-hero-actions {
	margin-top: 1.5rem;
}

.practice-hero-points {
	margin-top: 1.15rem;
}

.practice-hero-points span {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.08);
	padding: 0.45rem 0.7rem;
	color: rgba(255, 255, 255, 0.84);
	font-size: 0.82rem;
	font-weight: 850;
}

.practice-access-card {
	display: flex;
	flex-direction: column;
	justify-content: center;
	margin: 1rem;
	border: 1px solid rgba(255, 255, 255, 0.18);
	border-radius: 26px;
	background: #ffffff;
	color: var(--practice-text);
	padding: 1.2rem;
	box-shadow: 0 24px 50px rgba(0, 0, 0, 0.22);
}

.practice-access-top {
	display: flex;
	align-items: center;
	gap: 0.85rem;
}

.practice-access-icon,
.practice-upload-icon,
.practice-type-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 46px;
	height: 46px;
	border-radius: 16px;
	background: var(--practice-primary);
	color: #ffffff;
	flex: 0 0 auto;
}

.practice-access-icon {
	background: var(--practice-primary-soft);
	color: var(--practice-primary);
}

.practice-access-icon.active {
	background: var(--practice-gold);
	color: #3b2a00;
}

.practice-access-top span {
	display: block;
	color: var(--practice-muted);
	font-size: 0.75rem;
	font-weight: 900;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.practice-access-top h2 {
	margin: 0.15rem 0 0;
	color: var(--practice-primary);
	font-size: 1.2rem;
	font-weight: 950;
	letter-spacing: -0.035em;
}

.practice-access-card p {
	margin: 1rem 0 0;
	color: var(--practice-muted);
	font-size: 0.92rem;
	line-height: 1.65;
}

.practice-meter {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 0.4rem;
	margin-top: 1.15rem;
}

.practice-meter span {
	height: 8px;
	border-radius: 999px;
	background: var(--practice-primary-soft);
}

.practice-meter span.active {
	background: var(--practice-primary);
}

.practice-access-link {
	display: inline-flex;
	align-items: center;
	gap: 0.4rem;
	margin-top: 1rem;
	color: var(--practice-primary);
	font-size: 0.9rem;
	font-weight: 900;
	text-decoration: none;
}

.practice-access-link:hover {
	color: var(--practice-primary-hover);
}

.practice-panel {
	border: 1px solid var(--practice-border);
	border-radius: 30px;
	background: var(--practice-card);
	padding: 1.5rem;
	box-shadow: var(--practice-shadow-md);
	scroll-margin-top: 90px;
}

.practice-panel-head {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
	border-bottom: 1px solid var(--practice-border);
	padding-bottom: 1.25rem;
}

.practice-panel-head h2 {
	margin: 0;
	color: var(--practice-text);
	font-size: clamp(1.45rem, 3vw, 2rem);
	font-weight: 950;
	letter-spacing: -0.045em;
	line-height: 1.08;
}

.practice-panel-head p {
	margin: 0.55rem 0 0;
	max-width: 720px;
	color: var(--practice-muted);
	font-size: 0.95rem;
	line-height: 1.65;
}

.practice-pill {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border-radius: 999px;
	background: var(--practice-green-soft);
	color: var(--practice-green);
	padding: 0.45rem 0.75rem;
	font-size: 0.75rem;
	font-weight: 950;
	white-space: nowrap;
}

.practice-pill.locked {
	background: var(--practice-gold-soft);
	color: #8a5b00;
}

.practice-form {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 1rem;
	padding-top: 1.25rem;
}

.practice-field,
.practice-control {
	min-width: 0;
}

.practice-field {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	color: var(--practice-text);
	font-size: 0.86rem;
	font-weight: 850;
}

.practice-field.full,
.practice-upload.full,
.practice-advanced.full,
.practice-examples.full {
	grid-column: 1 / -1;
}

.practice-field select,
.practice-field textarea {
	width: 100%;
	border: 1px solid var(--practice-border);
	border-radius: 18px;
	background: var(--practice-card);
	padding: 0.9rem 1rem;
	color: var(--practice-text);
	font-size: 0.94rem;
	outline: none;
	transition: 0.18s ease;
}

.practice-field select:focus,
.practice-field textarea:focus,
.practice-page :deep(input:focus) {
	border-color: var(--practice-primary);
	box-shadow: 0 0 0 4px rgba(10, 34, 81, 0.1);
}

.practice-field textarea {
	min-height: 150px;
	resize: vertical;
	line-height: 1.6;
}

.practice-page :deep(label) {
	color: var(--practice-text);
	font-size: 0.86rem;
	font-weight: 850;
}

.practice-page :deep(input) {
	border: 1px solid var(--practice-border);
	border-radius: 16px;
	background: var(--practice-card);
	color: var(--practice-text);
	padding: 0.82rem 0.9rem;
	font-size: 0.92rem;
	outline: none;
	transition: 0.18s ease;
}

.practice-page :deep(input::placeholder),
.practice-field textarea::placeholder {
	color: var(--practice-soft);
}

.practice-type-grid {
	display: grid;
	grid-template-columns: repeat(5, minmax(0, 1fr));
	gap: 0.75rem;
}

.practice-type-card {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	min-height: 112px;
	border: 1px solid var(--practice-border);
	border-radius: 20px;
	background: var(--practice-primary-soft-2);
	padding: 0.9rem;
	text-align: left;
	cursor: pointer;
	transition: 0.18s ease;
}

.practice-type-card:hover {
	transform: translateY(-2px);
	border-color: var(--practice-primary);
	background: var(--practice-primary-soft);
}

.practice-type-card.active {
	border-color: var(--practice-primary);
	background: var(--practice-primary);
	color: #ffffff;
	box-shadow: var(--practice-shadow-md);
}

.practice-type-card.active .practice-type-icon {
	background: #ffffff;
	color: var(--practice-primary);
}

.practice-type-icon {
	width: 40px;
	height: 40px;
	border-radius: 14px;
}

.practice-type-card strong {
	display: block;
	color: var(--practice-text);
	font-size: 0.88rem;
	font-weight: 950;
	line-height: 1.2;
}

.practice-type-card small {
	display: block;
	margin-top: 0.3rem;
	color: var(--practice-muted);
	font-size: 0.76rem;
	line-height: 1.35;
}

.practice-type-card.active strong,
.practice-type-card.active small {
	color: #ffffff;
}

.practice-examples {
	display: flex;
	align-items: center;
	gap: 0.7rem;
	flex-wrap: wrap;
	margin-top: -0.25rem;
}

.practice-examples > span {
	color: var(--practice-muted);
	font-size: 0.82rem;
	font-weight: 850;
}

.practice-examples > div {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
}

.practice-examples button {
	border: 1px solid var(--practice-border);
	border-radius: 999px;
	background: var(--practice-card);
	color: var(--practice-primary);
	padding: 0.5rem 0.7rem;
	font-size: 0.8rem;
	font-weight: 850;
	cursor: pointer;
	transition: 0.18s ease;
}

.practice-examples button:hover {
	border-color: var(--practice-primary);
	background: var(--practice-primary-soft);
}

.practice-upload {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	border: 1px dashed var(--practice-border-strong);
	border-radius: 22px;
	background: var(--practice-primary-soft-2);
	padding: 1rem;
}

.practice-uploader {
	display: none;
}

.practice-upload-info {
	display: flex;
	align-items: center;
	gap: 0.9rem;
	min-width: 0;
}

.practice-upload-info strong {
	display: block;
	color: var(--practice-text);
	font-size: 0.92rem;
	font-weight: 950;
}

.practice-upload-info span {
	display: block;
	margin-top: 0.2rem;
	color: var(--practice-muted);
	font-size: 0.84rem;
	line-height: 1.45;
	word-break: break-word;
}

.practice-advanced {
	border: 1px solid var(--practice-border);
	border-radius: 20px;
	overflow: hidden;
}

.practice-advanced-toggle {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	width: 100%;
	border: 0;
	background: var(--practice-primary-soft-2);
	color: var(--practice-text);
	padding: 0.9rem 1rem;
	font-weight: 950;
	cursor: pointer;
}

.practice-advanced-toggle span {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
}

.practice-advanced-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 1rem;
	padding: 1rem;
}

.practice-submit {
	display: flex;
	align-items: center;
	justify-content: flex-end;
	gap: 1rem;
	border-top: 1px solid var(--practice-border);
	margin-top: 1.25rem;
	padding-top: 1.25rem;
}

.practice-warning {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	margin: 0;
	color: #8a5b00;
	font-size: 0.86rem;
	font-weight: 850;
	line-height: 1.45;
}

.practice-link,
.practice-btn-primary,
.practice-btn-light,
.practice-btn-ghost,
.practice-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	border-radius: 999px;
	font-size: 0.9rem;
	font-weight: 950;
	text-decoration: none;
	transition: 0.18s ease;
	white-space: nowrap;
}

.practice-link {
	border: 1px solid var(--practice-border);
	background: var(--practice-card);
	color: var(--practice-primary);
	padding: 0.65rem 0.9rem;
}

.practice-link:hover {
	border-color: var(--practice-primary);
	background: var(--practice-primary-soft);
}

.practice-btn-primary {
	border: 1px solid var(--practice-primary);
	background: var(--practice-primary);
	color: #ffffff;
	padding: 0.85rem 1.15rem;
	box-shadow: 0 12px 24px rgba(10, 34, 81, 0.18);
	cursor: pointer;
}

.practice-btn-primary:hover:not(:disabled) {
	transform: translateY(-1px);
	background: var(--practice-primary-hover);
}

.practice-btn-primary:disabled,
.practice-btn-light:disabled {
	cursor: not-allowed;
	opacity: 0.55;
}

.practice-btn-light {
	border: 1px solid #ffffff;
	background: #ffffff;
	color: var(--practice-primary);
	padding: 0.85rem 1.15rem;
	box-shadow: 0 14px 28px rgba(0, 0, 0, 0.18);
	cursor: pointer;
}

.practice-btn-light:hover:not(:disabled) {
	transform: translateY(-1px);
	background: #f8fbff;
}

.practice-btn-ghost {
	border: 1px solid rgba(255, 255, 255, 0.28);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
	padding: 0.85rem 1.15rem;
}

.practice-btn-ghost:hover {
	transform: translateY(-1px);
	background: rgba(255, 255, 255, 0.14);
}

.practice-btn-outline {
	border: 1px solid var(--practice-border-strong);
	background: var(--practice-card);
	color: var(--practice-primary);
	padding: 0.78rem 1rem;
	cursor: pointer;
}

.practice-btn-outline:hover {
	transform: translateY(-1px);
	border-color: var(--practice-primary);
	background: var(--practice-primary-soft);
}

:global(:root[data-theme='dark']) .practice-access-card {
	background: var(--practice-card);
	box-shadow: var(--practice-shadow-lg);
}

:global(:root[data-theme='dark']) .practice-access-top h2,
:global(:root[data-theme='dark']) .practice-access-link,
:global(:root[data-theme='dark']) .practice-link,
:global(:root[data-theme='dark']) .practice-btn-outline,
:global(:root[data-theme='dark']) .practice-examples button {
	color: #ffffff;
}

:global(:root[data-theme='dark']) .practice-field select,
:global(:root[data-theme='dark']) .practice-field textarea,
:global(:root[data-theme='dark']) .practice-page :deep(input) {
	background: #0b1220;
}

@media (max-width: 1100px) {
	.practice-hero {
		grid-template-columns: 1fr;
	}

	.practice-access-card {
		max-width: 560px;
	}

	.practice-type-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.practice-advanced-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 720px) {
	.practice-header-inner,
	.practice-shell {
		width: min(100% - 24px, 1120px);
	}

	.practice-header-inner {
		min-height: 66px;
	}

	.practice-shell {
		padding-top: 1rem;
		gap: 1rem;
	}

	.practice-hero,
	.practice-panel,
	.practice-access-card,
	.practice-upload,
	.practice-type-card,
	.practice-advanced {
		border-radius: 22px;
	}

	.practice-hero-copy {
		padding: 1.25rem;
	}

	.practice-hero h1 {
		font-size: clamp(2rem, 11vw, 2.75rem);
	}

	.practice-hero p {
		font-size: 0.95rem;
	}

	.practice-hero-actions {
		flex-direction: column;
	}

	.practice-btn-light,
	.practice-btn-ghost,
	.practice-btn-primary,
	.practice-btn-outline {
		width: 100%;
	}

	.practice-access-card {
		margin: 0 1.25rem 1.25rem;
	}

	.practice-panel {
		padding: 1rem;
		scroll-margin-top: 76px;
	}

	.practice-panel-head {
		flex-direction: column;
	}

	.practice-pill {
		width: fit-content;
	}

	.practice-form,
	.practice-advanced-grid {
		grid-template-columns: 1fr;
		gap: 0.85rem;
	}

	.practice-type-grid {
		grid-template-columns: 1fr;
	}

	.practice-type-card {
		min-height: auto;
	}

	.practice-examples {
		align-items: flex-start;
		flex-direction: column;
	}

	.practice-upload {
		align-items: stretch;
		flex-direction: column;
	}

	.practice-upload-info {
		align-items: flex-start;
	}

	.practice-submit {
		align-items: stretch;
		flex-direction: column;
	}

	.practice-warning {
		align-items: flex-start;
	}

	.practice-link {
		padding: 0.6rem 0.75rem;
		font-size: 0.82rem;
	}
}

.skeleton-wrapper {
	animation: pulse 1.5s infinite;
}

.skeleton-hero {
	height: 360px;
	border: 1px solid var(--practice-border);
	border-radius: 30px;
	background: var(--practice-card);
	box-shadow: var(--practice-shadow-lg);
}

.skeleton-panel {
	height: 560px;
	border: 1px solid var(--practice-border);
	border-radius: 30px;
	background: var(--practice-card);
	box-shadow: var(--practice-shadow-md);
}

@keyframes pulse {
	0% {
		opacity: 0.6;
	}
	50% {
		opacity: 0.3;
	}
	100% {
		opacity: 0.6;
	}
}
</style>

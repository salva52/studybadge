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

		<main class="practice-shell">
			<section class="practice-hero">
				<div class="practice-hero-copy">
					<div class="practice-eyebrow light">
						<Sparkles class="size-4" />
						{{ __('Simulaciones IA') }}
					</div>

					<h1>
						{{ __('Practica entrevistas, ventas e inglés con IA') }}
					</h1>

					<p>
						{{ __('Crea una simulación personalizada, sube tu CV o contexto y entrena como si estuvieras frente a un entrevistador, cliente o conversación real.') }}
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
						{{ __('Tienes 1 práctica gratis. Después, esta herramienta será exclusiva para usuarios Plus.') }}
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

			<section class="practice-benefits">
				<div class="practice-benefit">
					<div class="practice-benefit-icon">
						<Bot class="size-5" />
					</div>

					<div>
						<strong>{{ __('IA como entrevistador') }}</strong>
						<span>{{ __('Responde preguntas, recibe escenarios y practica presión real.') }}</span>
					</div>
				</div>

				<div class="practice-benefit">
					<div class="practice-benefit-icon gold">
						<FileText class="size-5" />
					</div>

					<div>
						<strong>{{ __('CV y contexto') }}</strong>
						<span>{{ __('Sube un archivo para que la simulación sea más personalizada.') }}</span>
					</div>
				</div>

				<div class="practice-benefit">
					<div class="practice-benefit-icon green">
						<ShieldCheck class="size-5" />
					</div>

					<div>
						<strong>{{ __('Entrena antes de fallar') }}</strong>
						<span>{{ __('Practica entrevistas, ventas, inglés o casos antes del momento real.') }}</span>
					</div>
				</div>
			</section>

			<section ref="formSection" class="practice-panel">
				<div class="practice-panel-head">
					<div>
						<div class="practice-eyebrow">
							<SlidersHorizontal class="size-4" />
							{{ __('Configura tu práctica') }}
						</div>

						<h2>{{ __('Personaliza la simulación') }}</h2>

						<p>
							{{ __('Elige el tipo de práctica, idioma, nivel y contexto. Mientras más específico seas, mejor será la simulación.') }}
						</p>
					</div>

					<div class="practice-pill" :class="{ locked: !access.data?.can_start }">
						{{ access.data?.can_start ? __('Disponible') : __('Plus') }}
					</div>
				</div>

				<div class="practice-form">
					<div class="practice-field full">
						<span>{{ __('Tipo de práctica') }}</span>

						<div class="practice-type-grid">
							<button
								v-for="option in practiceOptions"
								:key="option.value"
								type="button"
								class="practice-type-card"
								:class="{ active: draft.practice_type === option.value }"
								@click="draft.practice_type = option.value"
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
						:label="__('Entrevista, rol o caso')"
						:placeholder="__('Ej: SDR SaaS, marketing assistant, cliente molesto')"
					/>

					<FormControl
						v-model="draft.company_context"
						class="practice-control full"
						:label="__('Contexto')"
						:placeholder="__('Empresa, industria, producto, situación o cliente')"
					/>

					<label class="practice-field full">
						<span>{{ __('Objetivo') }}</span>

						<textarea
							v-model="draft.goal"
							rows="4"
							:placeholder="__('Ej: practicar respuestas STAR, vender una consultoría, mejorar fluidez en inglés')"
						/>
					</label>

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
									{{ cvName || __('PDF, Word o texto. Se usará para personalizar la simulación.') }}
								</span>
							</div>
						</div>

						<button class="practice-btn-outline" type="button" @click="openUploader">
							<Upload class="size-4" />
							{{ cvName ? __('Cambiar archivo') : __('Subir CV') }}
						</button>
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
	Bot,
	Briefcase,
	CheckCircle2,
	Crown,
	FileText,
	Languages,
	Megaphone,
	MessageCircle,
	ShieldCheck,
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

const draft = ref({
	practice_type: 'interview',
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
		icon: markRaw(Briefcase),
	},
	{
		value: 'sales',
		label: __('Práctica de ventas'),
		description: __('Simula clientes, objeciones y cierre de venta.'),
		icon: markRaw(ShoppingBag),
	},
	{
		value: 'english',
		label: __('Inglés conversacional'),
		description: __('Mejora fluidez, respuestas y confianza al hablar.'),
		icon: markRaw(Languages),
	},
	{
		value: 'marketing',
		label: __('Caso de marketing'),
		description: __('Resuelve escenarios de campañas, contenido o estrategia.'),
		icon: markRaw(Megaphone),
	},
	{
		value: 'custom',
		label: __('Personalizada'),
		description: __('Crea una práctica libre con tus propias reglas.'),
		icon: markRaw(MessageCircle),
	},
]

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
	toast.success(__('CV agregado.'))
}

async function createPractice() {
	creating.value = true

	try {
		const session = await call('studybadge_ai.ai_practice.create_practice_session', {
			data: JSON.stringify(draft.value),
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
	width: min(1180px, calc(100% - 32px));
	min-height: 72px;
	margin: 0 auto;
}

.practice-breadcrumbs {
	min-width: 0;
}

.practice-shell {
	display: grid;
	gap: 1.25rem;
	width: min(1180px, calc(100% - 32px));
	margin: 0 auto;
	padding-top: 1.5rem;
}

.practice-hero {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 360px;
	gap: 1.5rem;
	align-items: stretch;
	overflow: hidden;
	border-radius: 30px;
	background: var(--practice-primary);
	color: #ffffff;
	box-shadow: var(--practice-shadow-lg);
}

.practice-hero-copy {
	display: flex;
	flex-direction: column;
	justify-content: center;
	padding: clamp(1.35rem, 4vw, 2.5rem);
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
	max-width: 780px;
	color: #ffffff;
	font-size: clamp(2.1rem, 5.5vw, 4.3rem);
	font-weight: 950;
	letter-spacing: -0.06em;
	line-height: 1.02;
}

.practice-hero p {
	margin: 1rem 0 0;
	max-width: 680px;
	color: rgba(255, 255, 255, 0.78);
	font-size: 1rem;
	line-height: 1.75;
}

.practice-hero-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
	margin-top: 1.5rem;
}

.practice-access-card {
	margin: 1rem;
	border: 1px solid rgba(255, 255, 255, 0.18);
	border-radius: 26px;
	background: #ffffff;
	color: var(--practice-text);
	padding: 1.25rem;
	box-shadow: 0 24px 50px rgba(0, 0, 0, 0.22);
}

.practice-access-top {
	display: flex;
	align-items: center;
	gap: 0.85rem;
}

.practice-access-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 48px;
	height: 48px;
	border-radius: 16px;
	background: var(--practice-primary-soft);
	color: var(--practice-primary);
	flex: 0 0 auto;
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
	font-size: 1.25rem;
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
	margin-top: 1.25rem;
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
	margin-top: 1.1rem;
	color: var(--practice-primary);
	font-size: 0.9rem;
	font-weight: 900;
	text-decoration: none;
}

.practice-access-link:hover {
	color: var(--practice-primary-hover);
}

.practice-benefits {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 1rem;
}

.practice-benefit {
	display: flex;
	align-items: center;
	gap: 0.9rem;
	border: 1px solid var(--practice-border);
	border-radius: 22px;
	background: var(--practice-card);
	padding: 1rem;
	box-shadow: var(--practice-shadow-sm);
}

.practice-benefit-icon,
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

.practice-benefit-icon.gold {
	background: var(--practice-gold);
	color: #3b2a00;
}

.practice-benefit-icon.green {
	background: var(--practice-green);
	color: #ffffff;
}

.practice-benefit strong {
	display: block;
	color: var(--practice-text);
	font-size: 0.92rem;
	font-weight: 950;
	line-height: 1.25;
}

.practice-benefit span {
	display: block;
	margin-top: 0.18rem;
	color: var(--practice-muted);
	font-size: 0.8rem;
	line-height: 1.45;
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
	grid-template-columns: repeat(3, minmax(0, 1fr));
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
.practice-control.full,
.practice-upload.full {
	grid-column: 1 / -1;
}

.practice-field select,
.practice-field textarea {
	width: 100%;
	border: 1px solid var(--practice-border);
	border-radius: 16px;
	background: var(--practice-card);
	padding: 0.82rem 0.9rem;
	color: var(--practice-text);
	font-size: 0.92rem;
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
	min-height: 118px;
	resize: vertical;
	line-height: 1.55;
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
	gap: 0.8rem;
}

.practice-type-card {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	gap: 0.75rem;
	min-height: 152px;
	border: 1px solid var(--practice-border);
	border-radius: 22px;
	background: var(--practice-primary-soft-2);
	padding: 1rem;
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

.practice-type-card strong {
	display: block;
	color: var(--practice-text);
	font-size: 0.92rem;
	font-weight: 950;
	line-height: 1.2;
}

.practice-type-card small {
	display: block;
	margin-top: 0.35rem;
	color: var(--practice-muted);
	font-size: 0.78rem;
	line-height: 1.4;
}

.practice-type-card.active strong,
.practice-type-card.active small {
	color: #ffffff;
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
:global(:root[data-theme='dark']) .practice-btn-outline {
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

	.practice-benefits {
		grid-template-columns: 1fr;
	}

	.practice-type-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.practice-form {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 720px) {
	.practice-header-inner,
	.practice-shell {
		width: min(100% - 24px, 1180px);
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
	.practice-benefit,
	.practice-access-card,
	.practice-upload,
	.practice-type-card {
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

	.practice-benefit {
		align-items: flex-start;
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

	.practice-form {
		grid-template-columns: 1fr;
		gap: 0.85rem;
	}

	.practice-type-grid {
		grid-template-columns: 1fr;
	}

	.practice-type-card {
		min-height: auto;
		flex-direction: row;
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
</style>
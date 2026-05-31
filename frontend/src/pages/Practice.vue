<template>
	<div class="practice-page min-h-screen pb-14">
		<header class="practice-header sticky top-0 z-10 flex items-center justify-between border-b px-4 py-3 shadow-sm">
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<router-link :to="{ name: 'PromptLibrary' }" class="practice-link">
				<Zap class="size-4" /> {{ __('Prompts') }}
			</router-link>
		</header>

		<main class="mx-auto grid max-w-6xl gap-6 px-5 py-8 lg:grid-cols-[1fr_360px]">
			<section class="practice-hero">
				<div class="practice-kicker"><Sparkles class="size-4" /> {{ __('Simulaciones y práctica') }}</div>
				<h1>{{ __('Practica como si estuvieras en una entrevista real') }}</h1>
				<p>
					{{ __('Sube tu CV, elige contexto, idioma y nivel. La IA actúa como entrevistador, cliente o compañero de conversación.') }}
				</p>
				<div class="practice-hero-actions">
					<button class="practice-primary" :disabled="access.loading || !access.data?.can_start" @click="focusForm">
						<Video class="size-4" /> {{ __('Crear simulación') }}
					</button>
					<router-link v-if="!access.data?.can_start" :to="{ name: 'Plus' }" class="practice-secondary">
						<Crown class="size-4" /> {{ __('Desbloquear Plus') }}
					</router-link>
				</div>
			</section>

			<aside class="practice-access">
				<Crown class="size-6 text-amber-500" />
				<h2>{{ access.data?.is_plus ? __('Plus activo') : __('Tu acceso') }}</h2>
				<p v-if="access.data?.is_plus">{{ __('Tienes simulaciones ilimitadas incluidas en StudyBadge Plus.') }}</p>
				<p v-else-if="access.data?.free_trial_used">{{ __('Ya usaste tu práctica gratis. Actualiza a Plus para seguir practicando.') }}</p>
				<p v-else>{{ __('Tienes 1 práctica gratis. Después, esta herramienta será exclusiva para usuarios Plus.') }}</p>
				<div class="practice-meter">
					<span :class="{ active: !access.data?.free_trial_used || access.data?.is_plus }"></span>
					<span :class="{ active: access.data?.is_plus }"></span>
					<span :class="{ active: access.data?.is_plus }"></span>
				</div>
			</aside>

			<section ref="formSection" class="practice-panel lg:col-span-2">
				<div class="practice-panel-head">
					<div>
						<div class="practice-kicker">{{ __('Configura tu práctica') }}</div>
						<h2>{{ __('Personaliza la simulación') }}</h2>
					</div>
					<div class="practice-pill" :class="{ locked: !access.data?.can_start }">
						{{ access.data?.can_start ? __('Disponible') : __('Plus') }}
					</div>
				</div>

				<div class="practice-grid">
					<label class="practice-field">
						<span>{{ __('Tipo de práctica') }}</span>
						<select v-model="draft.practice_type">
							<option value="interview">{{ __('Entrevista laboral') }}</option>
							<option value="sales">{{ __('Práctica de ventas') }}</option>
							<option value="english">{{ __('Conversación en inglés') }}</option>
							<option value="marketing">{{ __('Caso de marketing') }}</option>
							<option value="custom">{{ __('Personalizada') }}</option>
						</select>
					</label>
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
					<FormControl v-model="draft.role_title" :label="__('Entrevista, rol o caso')" :placeholder="__('Ej: SDR SaaS, entrevista para marketing, cliente molesto')" />
					<FormControl class="lg:col-span-2" v-model="draft.company_context" :label="__('Contexto')" :placeholder="__('Empresa, industria, producto, situación o cliente')" />
					<label class="practice-field lg:col-span-2">
						<span>{{ __('Objetivo') }}</span>
						<textarea v-model="draft.goal" rows="4" :placeholder="__('Ej: practicar respuestas STAR, vender una consultoría, mejorar fluidez en inglés')" />
					</label>
					<div class="practice-upload lg:col-span-2">
						<FileUploader
							ref="fileUploader"
							class="hidden"
							:fileTypes="['.pdf', '.doc', '.docx', '.txt']"
							:uploadArgs="{ private: true }"
							:validateFile="validateFile"
							@success="handleFileUploaded"
						/>
						<div>
							<div class="font-semibold">{{ __('CV o contexto opcional') }}</div>
							<div class="text-sm text-slate-500">{{ cvName || __('PDF, Word o texto. Se usará para personalizar la simulación.') }}</div>
						</div>
						<button class="practice-secondary" type="button" @click="openUploader">
							<Upload class="size-4" /> {{ cvName ? __('Cambiar archivo') : __('Subir CV') }}
						</button>
					</div>
				</div>

				<div class="practice-submit">
					<p v-if="!access.data?.can_start" class="text-sm text-amber-700">
						{{ __('Tu prueba gratis ya fue usada. Plus desbloquea prácticas ilimitadas.') }}
					</p>
					<button class="practice-primary" :disabled="!access.data?.can_start || creating" @click="createPractice">
						<Video class="size-4" /> {{ creating ? __('Creando...') : __('Entrar a la sala') }}
					</button>
				</div>
			</section>
		</main>
	</div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Breadcrumbs, FileUploader, FormControl, call, createResource, toast, usePageMeta } from 'frappe-ui'
import { Crown, Sparkles, Upload, Video, Zap } from 'lucide-vue-next'
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

const breadcrumbs = computed(() => [
	{ label: __('Simulaciones IA'), route: { name: 'Practice' } },
])

usePageMeta(() => ({ title: __('Simulaciones IA'), icon: brand.favicon }))

function focusForm() {
	formSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function validateFile(file) {
	const ext = file.name.split('.').pop().toLowerCase()
	if (!['pdf', 'doc', 'docx', 'txt'].includes(ext)) return __('Sube PDF, Word o texto.')
	if (file.size > 15 * 1024 * 1024) return __('El archivo supera 15 MB.')
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
		router.push({ name: 'PracticeRoom', params: { sessionId: session.name } })
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo crear la práctica.'))
		access.reload()
	} finally {
		creating.value = false
	}
}
</script>

<style scoped>
.practice-page { background: #f6f8fc; color: #0f172a; }
.practice-header { background: rgba(255, 255, 255, 0.92); border-color: #e5e7eb; backdrop-filter: blur(12px); }
.practice-link, .practice-secondary, .practice-primary { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; border-radius: 8px; font-weight: 700; transition: 0.2s ease; }
.practice-link { color: #1d4ed8; font-size: 0.875rem; }
.practice-hero { min-height: 320px; border-radius: 8px; padding: clamp(2rem, 5vw, 4rem); color: white; background: linear-gradient(135deg, rgba(6, 27, 73, 0.96), rgba(29, 78, 216, 0.88)), url('/learning.svg'); background-size: cover; background-position: center; display: flex; flex-direction: column; justify-content: center; }
.practice-hero h1 { max-width: 760px; font-size: clamp(2.25rem, 6vw, 4.5rem); line-height: 1; font-weight: 900; letter-spacing: 0; }
.practice-hero p { margin-top: 1rem; max-width: 680px; color: rgba(219, 234, 254, 0.9); font-size: 1.1rem; line-height: 1.7; }
.practice-kicker { display: flex; align-items: center; gap: 0.5rem; color: #2563eb; font-size: 0.78rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0; }
.practice-hero .practice-kicker { color: #fbbf24; }
.practice-hero-actions { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 2rem; }
.practice-primary { min-height: 42px; padding: 0.65rem 1rem; background: #0d6efd; color: white; border: 1px solid #0d6efd; }
.practice-primary:hover:not(:disabled) { background: #0b5ed7; }
.practice-primary:disabled { cursor: not-allowed; opacity: 0.55; }
.practice-secondary { min-height: 42px; padding: 0.65rem 1rem; background: white; color: #0f172a; border: 1px solid #dbe3ef; }
.practice-secondary:hover { background: #f8fafc; }
.practice-access, .practice-panel { border: 1px solid #e2e8f0; border-radius: 8px; background: white; box-shadow: 0 18px 45px rgba(15, 23, 42, 0.06); }
.practice-access { padding: 1.5rem; align-self: stretch; }
.practice-access h2, .practice-panel h2 { margin-top: 0.5rem; font-size: 1.35rem; font-weight: 900; }
.practice-access p { margin-top: 0.75rem; color: #64748b; line-height: 1.6; }
.practice-meter { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.35rem; margin-top: 1.25rem; }
.practice-meter span { height: 8px; border-radius: 999px; background: #e2e8f0; }
.practice-meter span.active { background: #0d6efd; }
.practice-panel { padding: 1.25rem; }
.practice-panel-head { display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-bottom: 1px solid #edf2f7; padding-bottom: 1rem; }
.practice-pill { border-radius: 999px; background: #dcfce7; color: #166534; padding: 0.35rem 0.7rem; font-size: 0.75rem; font-weight: 900; }
.practice-pill.locked { background: #fef3c7; color: #92400e; }
.practice-grid { display: grid; grid-template-columns: repeat(1, minmax(0, 1fr)); gap: 1rem; padding-top: 1.25rem; }
@media (min-width: 1024px) { .practice-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.practice-field { display: flex; flex-direction: column; gap: 0.45rem; font-size: 0.875rem; font-weight: 700; color: #334155; }
.practice-field select, .practice-field textarea { width: 100%; border: 1px solid #dbe3ef; border-radius: 8px; background: white; padding: 0.65rem 0.75rem; color: #0f172a; outline: none; }
.practice-field textarea { resize: vertical; line-height: 1.55; }
.practice-upload { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 1rem; background: #f8fafc; }
.practice-submit { display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-end; gap: 1rem; border-top: 1px solid #edf2f7; margin-top: 1.25rem; padding-top: 1rem; }
:root[data-theme="dark"] .practice-page { background: #0f172a; color: #e5e7eb; }
:root[data-theme="dark"] .practice-header, :root[data-theme="dark"] .practice-access, :root[data-theme="dark"] .practice-panel { background: #111827; border-color: rgba(255,255,255,0.08); }
:root[data-theme="dark"] .practice-field select, :root[data-theme="dark"] .practice-field textarea, :root[data-theme="dark"] .practice-upload { background: #0b1220; border-color: rgba(255,255,255,0.12); color: #e5e7eb; }
</style>

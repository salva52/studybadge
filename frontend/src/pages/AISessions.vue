<template>
	<div class="ai-page" @paste="handlePaste">
		<header class="ai-topbar">
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<div class="ai-topbar-actions">
				<span class="ai-plan-pill" :class="{ plus: access?.is_plus }">
					<Crown v-if="access?.is_plus" class="size-4" />
					<Sparkles v-else class="size-4" />
					{{ access?.is_plus ? __('Plus ilimitado') : __('Plan Free') }}
				</span>
				<router-link v-if="!access?.is_plus" :to="{ name: 'Plus' }" class="ai-btn ai-btn-gold">
					<Crown class="size-4" /> {{ __('Desbloquear Plus') }}
				</router-link>
			</div>
		</header>

		<main class="ai-shell">
			<section class="ai-create-panel">
				<div>
					<div class="ai-kicker"><Brain class="size-4" /> {{ __('Sesiones IA') }}</div>
					<h1>{{ __('Estudia con documentos, chats y practica guiada') }}</h1>
					<p>{{ __('Crea un espacio por curso, trabajo o proyecto. La IA mantiene el contexto academico de tus archivos y conversaciones.') }}</p>
				</div>
				<div class="ai-model-switch" role="group" :aria-label="__('Modelo')">
					<button :class="{ active: draft.model_tier === 'light' }" @click="draft.model_tier = 'light'">
						<Zap class="size-4" />
						<span>Study Model Light</span>
					</button>
					<button :class="{ active: draft.model_tier === 'pro', locked: !access?.pro_available }" @click="selectProModel">
						<Crown class="size-4" />
						<span>Study Model Pro</span>
					</button>
				</div>
				<div class="ai-create-grid">
					<FormControl v-model="draft.title" :label="__('Nombre de la sesion')" :placeholder="__('Ej. Trabajo final de finanzas')" />
					<FormControl v-model="draft.academic_context" :label="__('Curso o contexto')" :placeholder="__('Ej. Universidad, ciclo, profesor')" />
					<div>
						<label class="ai-label">{{ __('Nivel') }}</label>
						<select v-model="draft.student_level" class="ai-input">
							<option value="colegio">{{ __('Colegio') }}</option>
							<option value="preuniversitario">{{ __('Preuniversitario') }}</option>
							<option value="universitario">{{ __('Universitario') }}</option>
							<option value="profesional">{{ __('Profesional') }}</option>
						</select>
					</div>
					<FormControl v-model="draft.goal" :label="__('Objetivo')" :placeholder="__('Ej. entender lecturas, resolver problemas, preparar exposicion')" />
					<label class="ai-field ai-create-wide">
						<span>{{ __('Notas iniciales') }}</span>
						<textarea v-model="draft.manual_text" rows="3" :placeholder="__('Pega indicaciones, rubrica, temas o preguntas iniciales.')" />
					</label>
				</div>
				<div class="ai-create-footer">
					<div class="ai-limit-line">
						<span>{{ accessText }}</span>
					</div>
					<button class="ai-btn ai-btn-primary" :disabled="creating || !canCreate" @click="createSession">
						<Plus class="size-4" /> {{ creating ? __('Creando...') : __('Crear sesion') }}
					</button>
				</div>
			</section>

			<section class="ai-workspace">
				<aside class="ai-sidebar">
					<div class="ai-section-head">
						<div>
							<h2>{{ __('Mis sesiones') }}</h2>
							<p>{{ sessions.length }} {{ __('guardadas') }}</p>
						</div>
						<button class="ai-icon-btn" :title="__('Actualizar')" @click="loadAll">
							<RefreshCw class="size-4" />
						</button>
					</div>
					<div class="ai-session-list">
						<button
							v-for="session in sessions"
							:key="session.name"
							class="ai-session-item"
							:class="{ active: activeSession?.name === session.name }"
							@click="openSession(session.name)"
						>
							<span class="ai-session-icon"><MessagesSquare class="size-4" /></span>
							<span class="ai-session-copy">
								<strong>{{ session.title || session.name }}</strong>
								<small>{{ session.model_label || modelLabel(session.model_tier) }} · {{ formatDate(session.modified) }}</small>
							</span>
						</button>
						<div v-if="!sessions.length" class="ai-empty-mini">
							<FolderOpen class="size-5" />
							<span>{{ __('Aun no tienes sesiones IA.') }}</span>
						</div>
					</div>
				</aside>

				<section class="ai-main-panel">
					<div v-if="!activeSession" class="ai-empty-state">
						<Sparkles class="size-10" />
						<h2>{{ __('Crea o abre una sesion') }}</h2>
						<p>{{ __('Tus documentos, preguntas, quizzes e infografias apareceran aqui.') }}</p>
					</div>
					<template v-else>
						<div class="ai-session-header">
							<div>
								<div class="ai-kicker">{{ activeSession.model_label || modelLabel(activeSession.model_tier) }}</div>
								<h2>{{ activeSession.title }}</h2>
								<p>{{ activeSession.goal || activeSession.academic_context || __('Workspace academico') }}</p>
							</div>
							<FileUploader
								ref="fileUploader"
								class="hidden"
								:fileTypes="['.pdf', '.doc', '.docx', 'image/*', '.txt', '.md']"
								:uploadArgs="{ private: true }"
								:validateFile="validateFile"
								@success="handleFileUploaded"
							/>
							<button class="ai-btn ai-btn-primary" @click="openUploader">
								<Upload class="size-4" /> {{ __('Subir documentos') }}
							</button>
						</div>

						<div class="ai-doc-grid">
							<article class="ai-doc-panel">
								<div class="ai-section-head">
									<div>
										<h3>{{ __('Documentos') }}</h3>
										<p>{{ materialCountText }}</p>
									</div>
									<span class="ai-soft-pill">Ctrl+V {{ __('imagenes') }}</span>
								</div>
								<div class="ai-materials">
									<div v-for="material in activeSession.materials || []" :key="material.idx" class="ai-material">
										<FileText class="size-4" />
										<div>
											<strong>{{ material.file_name }}</strong>
											<small>{{ material.file_type }} · {{ material.analysis_status || __('Pendiente') }}</small>
										</div>
									</div>
									<div v-if="!activeSession.materials?.length" class="ai-empty-mini">
										<Upload class="size-5" />
										<span>{{ __('Sube PDFs, trabajos, lecturas o imagenes para dar contexto a la IA.') }}</span>
									</div>
								</div>
							</article>

							<article class="ai-tools-panel">
								<div class="ai-section-head">
									<div>
										<h3>{{ __('Herramientas academicas') }}</h3>
										<p>{{ __('Resumenes, quizzes, lectura y matematica') }}</p>
									</div>
								</div>
								<div class="ai-tool-grid">
									<button v-for="tool in tools" :key="tool.id" class="ai-tool-card" :class="{ locked: tool.pro && !access?.is_plus }" @click="runTool(tool)">
										<component :is="tool.icon" class="size-5" />
										<strong>{{ tool.label }}</strong>
										<span>{{ tool.description }}</span>
										<small v-if="tool.pro && !access?.is_plus">{{ __('Plus') }}</small>
									</button>
								</div>
							</article>
						</div>

						<article class="ai-output" v-if="toolResult || toolLoading">
							<div class="ai-section-head">
								<div>
									<h3>{{ selectedToolLabel }}</h3>
									<p>{{ __('Resultado generado para esta sesion') }}</p>
								</div>
								<div class="ai-loader" v-if="toolLoading"></div>
							</div>
							<img v-if="toolImage" :src="toolImage" class="ai-infographic" :alt="__('Infografia')" />
							<div v-if="toolResult" class="ai-markdown" v-html="renderMarkdown(toolResult)" />
						</article>
					</template>
				</section>

				<aside class="ai-chat-panel" :class="{ disabled: !activeSession }">
					<div class="ai-section-head">
						<div>
							<h2>{{ __('Chat academico') }}</h2>
							<p>{{ currentThread?.title || __('Chat principal') }}</p>
						</div>
						<span class="ai-soft-pill">{{ remainingText }}</span>
					</div>
					<div ref="chatBox" class="ai-chat-box">
						<div v-if="!chatMessages.length" class="ai-empty-mini chat-empty">
							<MessageCircle class="size-5" />
							<span>{{ __('Pregunta sobre tus documentos, pide ejemplos o resuelve ejercicios paso a paso.') }}</span>
						</div>
						<div v-for="message in chatMessages" :key="message.created_at || message.content" class="ai-message" :class="message.role === 'user' ? 'user' : 'assistant'">
							<div v-html="renderMarkdown(message.content)" />
						</div>
					</div>
					<div v-if="pastedFiles.length" class="ai-pasted-files">
						<span v-for="file in pastedFiles" :key="file.file_url">{{ file.file_name || file.file_url }}</span>
					</div>
					<div class="ai-chat-actions">
						<button class="ai-chip" @click="prefill('summary')">{{ __('Hazme un resumen') }}</button>
						<button class="ai-chip" @click="prefill('math')">{{ __('Guiame en matematica') }}</button>
						<button class="ai-chip" @click="prefill('reader')">{{ __('Pregunta de lectura') }}</button>
					</div>
					<div class="ai-chat-input">
						<textarea v-model="chatInput" :disabled="!activeSession || chatLoading" rows="3" :placeholder="__('Pregunta sobre esta sesion')" @keydown.enter.exact.prevent="sendChat" />
						<button class="ai-btn ai-btn-primary" :disabled="!activeSession || chatLoading || (!chatInput.trim() && !pastedFiles.length)" @click="sendChat">
							<SendHorizontal class="size-4" /> {{ chatLoading ? __('Pensando...') : __('Enviar') }}
						</button>
					</div>
				</aside>
			</section>
		</main>
	</div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Breadcrumbs, FileUploader, FormControl, call, toast, usePageMeta } from 'frappe-ui'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import {
	BookOpenCheck,
	Brain,
	Crown,
	FileQuestion,
	FileText,
	FolderOpen,
	Image as ImageIcon,
	Layers,
	ListTree,
	MessageCircle,
	MessagesSquare,
	Plus,
	RefreshCw,
	SendHorizontal,
	Sigma,
	Sparkles,
	Upload,
	Zap,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const route = useRoute()
const router = useRouter()
const { brand } = sessionStore()
const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true })

const access = ref(null)
const sessions = ref([])
const activeSession = ref(null)
const currentThread = ref(null)
const chatMessages = ref([])
const chatInput = ref('')
const pastedFiles = ref([])
const fileUploader = ref(null)
const chatBox = ref(null)
const creating = ref(false)
const loadingSession = ref(false)
const chatLoading = ref(false)
const toolLoading = ref(false)
const toolResult = ref('')
const toolImage = ref('')
const selectedToolLabel = ref('')

const draft = ref({
	title: '',
	goal: '',
	academic_context: '',
	student_level: 'universitario',
	manual_text: '',
	model_tier: 'light',
})

const tools = [
	{ id: 'summary', label: __('Resumen'), description: __('Ideas clave y prioridades'), icon: BookOpenCheck },
	{ id: 'organize', label: __('Ordenar info'), description: __('Temas, tareas y pendientes'), icon: ListTree },
	{ id: 'quiz', label: __('Cuestionario'), description: __('Preguntas con explicacion'), icon: FileQuestion },
	{ id: 'flashcards', label: __('Flashcards'), description: __('Tarjetas y checklist'), icon: Layers },
	{ id: 'reader_question', label: __('Lectura guiada'), description: __('Pregunta corta por avance'), icon: MessageCircle },
	{ id: 'math', label: __('Matematica paso a paso'), description: __('Resuelve y practica'), icon: Sigma },
	{ id: 'infographic', label: __('Infografia'), description: __('Mapa visual de estudio'), icon: ImageIcon, pro: true },
]

const breadcrumbs = computed(() => [
	{ label: __('Sesiones IA'), route: { name: 'AISessions' } },
])
const canCreate = computed(() => access.value?.can_create_session !== false)
const accessText = computed(() => {
	if (!access.value) return ''
	if (access.value.is_plus) return __('Sesiones, chats y herramientas ilimitadas con Plus.')
	return `${access.value.active_sessions || 0}/${access.value.free_session_limit || 3} ${__('sesiones activas')} · ${access.value.messages_remaining ?? 0} ${__('mensajes hoy')}`
})
const remainingText = computed(() => {
	if (!access.value) return ''
	if (access.value.is_plus) return __('Ilimitado')
	return `${access.value.messages_remaining ?? 0}/${access.value.daily_message_limit || 25}`
})
const materialCountText = computed(() => {
	const count = activeSession.value?.materials?.length || 0
	const max = access.value?.max_files_per_session || 15
	return `${count}/${max} ${__('archivos')}`
})

usePageMeta(() => ({ title: __('Sesiones IA'), icon: brand.favicon }))

onMounted(loadAll)
watch(() => route.fullPath, loadRouteSession)

async function api(method, params = {}) {
	try {
		return await call(`studybadge_ai.ai_sessions.${method}`, params)
	} catch (error) {
		toast.error(error.messages?.[0] || error.message || __('No se pudo completar la accion.'))
		throw error
	}
}

async function loadAll() {
	access.value = await api('get_ai_session_access')
	sessions.value = await api('list_ai_sessions')
	await loadRouteSession()
}

async function loadRouteSession() {
	const name = route.params.sessionId
	if (!name) {
		activeSession.value = null
		currentThread.value = null
		chatMessages.value = []
		return
	}
	loadingSession.value = true
	try {
		activeSession.value = await api('get_ai_session', { name })
		currentThread.value = findThread(route.params.threadId) || activeSession.value.threads?.[0] || null
		chatMessages.value = currentThread.value?.messages || []
		await nextTick(scrollChat)
	} finally {
		loadingSession.value = false
	}
}

function findThread(name) {
	return (activeSession.value?.threads || []).find((thread) => thread.name === name)
}

function modelLabel(tier) {
	return tier === 'pro' ? 'Study Model Pro' : 'Study Model Light'
}

function selectProModel() {
	if (!access.value?.pro_available) {
		toast.warning(__('Study Model Pro esta disponible con StudyBadge Plus.'))
		return
	}
	draft.value.model_tier = 'pro'
}

async function createSession() {
	if (!canCreate.value) {
		toast.warning(__('Tu plan Free alcanzo el limite de sesiones activas.'))
		return
	}
	creating.value = true
	try {
		const session = await api('create_ai_session', { data: draft.value })
		toast.success(__('Sesion creada.'))
		draft.value = { title: '', goal: '', academic_context: '', student_level: 'universitario', manual_text: '', model_tier: 'light' }
		await loadAll()
		router.push({ name: 'AISessionRoom', params: { sessionId: session.name } })
	} finally {
		creating.value = false
	}
}

function openSession(name) {
	router.push({ name: 'AISessionRoom', params: { sessionId: name } })
}

function validateFile(file) {
	const ext = file.name.split('.').pop().toLowerCase()
	if (!['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'webp', 'txt', 'md'].includes(ext)) return __('Usa PDF, imagenes, Word o texto.')
	if (file.size > 25 * 1024 * 1024) return __('El archivo supera 25 MB.')
}

function openUploader() {
	const input = fileUploader.value?.$el?.querySelector('input[type="file"]')
	input?.click()
}

async function handleFileUploaded(file) {
	if (!activeSession.value) {
		toast.warning(__('Abre o crea una sesion primero.'))
		return
	}
	activeSession.value = await api('upload_ai_session_material', {
		session: activeSession.value.name,
		file_url: file.file_url,
	})
	pastedFiles.value.push(file)
	toast.success(__('Archivo agregado a la sesion.'))
}

async function handlePaste(event) {
	if (!activeSession.value) return
	const imageFiles = [...(event.clipboardData?.files || [])].filter((file) => file.type.startsWith('image/'))
	if (!imageFiles.length) return
	event.preventDefault()
	for (const file of imageFiles.slice(0, 3)) {
		await uploadPastedImage(file)
	}
}

async function uploadPastedImage(file) {
	const data = new FormData()
	data.append('file', file, file.name || `captura-${Date.now()}.png`)
	data.append('is_private', '1')
	const response = await fetch('/api/method/upload_file', {
		method: 'POST',
		headers: { 'X-Frappe-CSRF-Token': window.csrf_token || '' },
		body: data,
	})
	const payload = await response.json()
	if (!response.ok || payload.exc) {
		toast.error(__('No se pudo pegar la imagen.'))
		return
	}
	await handleFileUploaded(payload.message)
}

async function sendChat() {
	if (!activeSession.value) return
	const text = chatInput.value.trim()
	if (!text && !pastedFiles.value.length) return
	chatLoading.value = true
	try {
		const optimistic = { role: 'user', content: text || __('Archivo adjunto'), created_at: String(Date.now()) }
		chatMessages.value = [...chatMessages.value, optimistic]
		chatInput.value = ''
		await nextTick(scrollChat)
		const result = await api('chat_ai_session', {
			session: activeSession.value.name,
			thread: currentThread.value?.name,
			message: text,
			files: pastedFiles.value.map((file) => file.file_url),
		})
		currentThread.value = result.thread
		chatMessages.value = result.thread.messages || []
		access.value = result.access || access.value
		pastedFiles.value = []
		await nextTick(scrollChat)
	} finally {
		chatLoading.value = false
	}
}

function prefill(mode) {
	const prompts = {
		summary: __('Hazme un resumen claro de esta sesion y dime que debo estudiar primero.'),
		math: __('Resuelve este problema paso a paso y luego dame uno mas facil para practicar:'),
		reader: __('Hazme una pregunta corta sobre la parte que estoy leyendo.'),
	}
	chatInput.value = prompts[mode] || ''
}

async function runTool(tool) {
	if (tool.pro && !access.value?.is_plus) {
		toast.warning(__('Esta herramienta esta disponible con StudyBadge Plus.'))
		return
	}
	if (!activeSession.value) return
	toolLoading.value = true
	toolResult.value = ''
	toolImage.value = ''
	selectedToolLabel.value = tool.label
	try {
		const result = await api('generate_ai_tool', {
			session: activeSession.value.name,
			tool: tool.id,
			payload: {
				topic: activeSession.value.goal || activeSession.value.title,
				position: activeSession.value.reader_progress || {},
			},
		})
		access.value = result.access || access.value
		if (result.result?.image_base64) {
			toolImage.value = `data:${result.result.mime_type};base64,${result.result.image_base64}`
			toolResult.value = result.result.text || ''
		} else {
			toolResult.value = result.result || ''
		}
	} finally {
		toolLoading.value = false
	}
}

function renderMarkdown(text) {
	if (!text) return ''
	return DOMPurify.sanitize(markdown.render(String(text)))
}

function scrollChat() {
	if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}

function formatDate(value) {
	if (!value) return ''
	return new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric' }).format(new Date(value))
}
</script>

<style scoped>
.ai-page { min-height: 100vh; background: #f5f7fb; color: #101827; }
.ai-topbar { position: sticky; top: 0; z-index: 20; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-bottom: 1px solid #e5e7eb; background: rgba(255, 255, 255, 0.94); padding: 0.75rem 1rem; backdrop-filter: blur(12px); }
.ai-topbar-actions { display: flex; align-items: center; gap: 0.75rem; }
.ai-shell { display: flex; flex-direction: column; gap: 1rem; width: min(1540px, 100%); margin: 0 auto; padding: 1.25rem; }
.ai-create-panel, .ai-sidebar, .ai-main-panel, .ai-chat-panel, .ai-output { border: 1px solid #dfe5ef; border-radius: 8px; background: #fff; box-shadow: 0 16px 38px rgba(15, 23, 42, 0.05); }
.ai-create-panel { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(260px, 0.6fr); gap: 1rem; padding: clamp(1rem, 3vw, 1.5rem); }
.ai-kicker { display: inline-flex; align-items: center; gap: 0.45rem; color: #2563eb; font-size: 0.78rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0; }
.ai-create-panel h1 { margin-top: 0.5rem; max-width: 720px; font-size: clamp(1.8rem, 4vw, 3.4rem); line-height: 1.02; font-weight: 900; letter-spacing: 0; }
.ai-create-panel p, .ai-section-head p, .ai-session-header p { margin-top: 0.4rem; color: #64748b; line-height: 1.55; }
.ai-model-switch { display: grid; grid-template-columns: 1fr; gap: 0.55rem; align-self: start; }
.ai-model-switch button { display: flex; align-items: center; gap: 0.6rem; min-height: 46px; border: 1px solid #dbe3ef; border-radius: 8px; background: #f8fafc; padding: 0.75rem; color: #334155; font-weight: 900; text-align: left; }
.ai-model-switch button.active { border-color: #2563eb; background: #eff6ff; color: #1d4ed8; }
.ai-model-switch button.locked { color: #92400e; background: #fffbeb; border-color: #fde68a; }
.ai-create-grid { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.85rem; }
.ai-create-wide { grid-column: span 4; }
.ai-field { display: flex; flex-direction: column; gap: 0.4rem; font-size: 0.85rem; font-weight: 800; color: #334155; }
.ai-field textarea, .ai-input { width: 100%; border: 1px solid #dbe3ef; border-radius: 8px; background: white; padding: 0.65rem 0.75rem; color: #0f172a; outline: none; }
.ai-label { display: block; margin-bottom: 0.4rem; font-size: 0.85rem; font-weight: 800; color: #334155; }
.ai-create-footer { grid-column: 1 / -1; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-top: 1px solid #edf2f7; padding-top: 1rem; }
.ai-limit-line { color: #64748b; font-size: 0.875rem; font-weight: 700; }
.ai-workspace { display: grid; grid-template-columns: 290px minmax(0, 1fr) 380px; gap: 1rem; align-items: start; }
.ai-sidebar, .ai-main-panel, .ai-chat-panel { min-height: 620px; padding: 1rem; }
.ai-chat-panel { position: sticky; top: 4.75rem; display: flex; flex-direction: column; max-height: calc(100vh - 6rem); }
.ai-chat-panel.disabled { opacity: 0.72; }
.ai-section-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; margin-bottom: 0.9rem; }
.ai-section-head h2, .ai-section-head h3, .ai-session-header h2 { margin: 0; color: #0f172a; font-size: 1rem; font-weight: 900; }
.ai-session-list, .ai-materials { display: flex; flex-direction: column; gap: 0.55rem; }
.ai-session-item { display: flex; align-items: flex-start; gap: 0.75rem; width: 100%; border: 1px solid transparent; border-radius: 8px; background: #f8fafc; padding: 0.75rem; text-align: left; transition: 0.18s ease; }
.ai-session-item:hover, .ai-session-item.active { border-color: #bfdbfe; background: #eff6ff; }
.ai-session-icon { display: grid; width: 32px; height: 32px; flex-shrink: 0; place-items: center; border-radius: 8px; background: #dbeafe; color: #2563eb; }
.ai-session-copy { min-width: 0; display: flex; flex-direction: column; gap: 0.2rem; }
.ai-session-copy strong { overflow: hidden; color: #0f172a; text-overflow: ellipsis; white-space: nowrap; font-size: 0.9rem; }
.ai-session-copy small, .ai-material small { color: #64748b; font-size: 0.75rem; }
.ai-session-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; border-bottom: 1px solid #edf2f7; padding-bottom: 1rem; }
.ai-doc-grid { display: grid; grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr); gap: 1rem; margin-top: 1rem; }
.ai-doc-panel, .ai-tools-panel { border: 1px solid #edf2f7; border-radius: 8px; padding: 1rem; background: #fbfdff; }
.ai-material { display: flex; align-items: flex-start; gap: 0.65rem; border: 1px solid #e2e8f0; border-radius: 8px; background: #fff; padding: 0.7rem; }
.ai-material svg { flex-shrink: 0; color: #2563eb; margin-top: 0.15rem; }
.ai-material strong { display: block; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.85rem; }
.ai-tool-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.65rem; }
.ai-tool-card { position: relative; display: flex; min-height: 122px; flex-direction: column; gap: 0.4rem; border: 1px solid #dbe3ef; border-radius: 8px; background: #fff; padding: 0.85rem; text-align: left; transition: 0.18s ease; }
.ai-tool-card:hover { border-color: #93c5fd; transform: translateY(-1px); }
.ai-tool-card svg { color: #2563eb; }
.ai-tool-card strong { color: #0f172a; font-size: 0.92rem; }
.ai-tool-card span { color: #64748b; font-size: 0.78rem; line-height: 1.35; }
.ai-tool-card small { position: absolute; top: 0.6rem; right: 0.6rem; border-radius: 999px; background: #fef3c7; color: #92400e; padding: 0.15rem 0.45rem; font-size: 0.68rem; font-weight: 900; }
.ai-tool-card.locked { background: #fffbeb; border-color: #fde68a; }
.ai-chat-box { flex: 1; min-height: 300px; overflow-y: auto; border: 1px solid #edf2f7; border-radius: 8px; background: #f8fafc; padding: 0.8rem; }
.ai-message { max-width: 92%; border-radius: 8px; padding: 0.7rem 0.8rem; font-size: 0.9rem; line-height: 1.55; }
.ai-message + .ai-message { margin-top: 0.6rem; }
.ai-message.user { margin-left: auto; background: #2563eb; color: white; }
.ai-message.assistant { background: white; border: 1px solid #e2e8f0; color: #0f172a; }
.ai-chat-actions { display: flex; gap: 0.45rem; overflow-x: auto; padding: 0.75rem 0 0.5rem; }
.ai-chip { flex-shrink: 0; border: 1px solid #dbe3ef; border-radius: 999px; background: white; color: #475569; padding: 0.42rem 0.65rem; font-size: 0.76rem; font-weight: 800; }
.ai-chat-input { display: grid; gap: 0.55rem; }
.ai-chat-input textarea { width: 100%; resize: vertical; border: 1px solid #dbe3ef; border-radius: 8px; padding: 0.75rem; outline: none; }
.ai-pasted-files { display: flex; flex-wrap: wrap; gap: 0.35rem; padding-top: 0.6rem; }
.ai-pasted-files span, .ai-soft-pill, .ai-plan-pill { display: inline-flex; align-items: center; gap: 0.35rem; border-radius: 999px; font-size: 0.75rem; font-weight: 900; }
.ai-pasted-files span { background: #ecfdf5; color: #047857; padding: 0.25rem 0.5rem; }
.ai-soft-pill { background: #eef2ff; color: #4f46e5; padding: 0.3rem 0.55rem; white-space: nowrap; }
.ai-plan-pill { background: #eff6ff; color: #1d4ed8; padding: 0.5rem 0.75rem; }
.ai-plan-pill.plus { background: #fef3c7; color: #92400e; }
.ai-btn, .ai-icon-btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; border-radius: 8px; font-weight: 900; transition: 0.18s ease; }
.ai-btn { min-height: 40px; padding: 0.6rem 0.85rem; border: 1px solid #dbe3ef; background: white; color: #0f172a; }
.ai-btn-primary { border-color: #2563eb; background: #2563eb; color: white; }
.ai-btn-primary:disabled { cursor: not-allowed; opacity: 0.55; }
.ai-btn-gold { border-color: #f59e0b; background: #f59e0b; color: #78350f; }
.ai-icon-btn { width: 34px; height: 34px; border: 1px solid #dbe3ef; background: white; color: #475569; }
.ai-empty-state, .ai-empty-mini { display: flex; align-items: center; justify-content: center; color: #64748b; text-align: center; }
.ai-empty-state { min-height: 540px; flex-direction: column; gap: 0.6rem; }
.ai-empty-state h2 { color: #0f172a; font-size: 1.3rem; font-weight: 900; }
.ai-empty-mini { min-height: 120px; flex-direction: column; gap: 0.5rem; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 1rem; font-size: 0.86rem; }
.chat-empty { min-height: 100%; }
.ai-output { margin-top: 1rem; padding: 1rem; }
.ai-markdown { color: #0f172a; line-height: 1.7; }
.ai-markdown :deep(h1), .ai-markdown :deep(h2), .ai-markdown :deep(h3) { margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 900; }
.ai-markdown :deep(ul), .ai-markdown :deep(ol) { padding-left: 1.25rem; }
.ai-infographic { width: 100%; border: 1px solid #dbe3ef; border-radius: 8px; background: white; }
.ai-loader { width: 24px; height: 24px; border: 3px solid #dbeafe; border-top-color: #2563eb; border-radius: 999px; animation: ai-spin 0.8s linear infinite; }
@keyframes ai-spin { to { transform: rotate(360deg); } }

:root[data-theme="dark"] .ai-page { background: #0f172a; color: #e5e7eb; }
:root[data-theme="dark"] .ai-topbar,
:root[data-theme="dark"] .ai-create-panel,
:root[data-theme="dark"] .ai-sidebar,
:root[data-theme="dark"] .ai-main-panel,
:root[data-theme="dark"] .ai-chat-panel,
:root[data-theme="dark"] .ai-output,
:root[data-theme="dark"] .ai-doc-panel,
:root[data-theme="dark"] .ai-tools-panel,
:root[data-theme="dark"] .ai-tool-card,
:root[data-theme="dark"] .ai-message.assistant { background: #111827; border-color: rgba(255,255,255,0.09); color: #e5e7eb; }
:root[data-theme="dark"] .ai-session-item,
:root[data-theme="dark"] .ai-chat-box,
:root[data-theme="dark"] .ai-material { background: #0b1220; border-color: rgba(255,255,255,0.08); }
:root[data-theme="dark"] .ai-section-head h2,
:root[data-theme="dark"] .ai-section-head h3,
:root[data-theme="dark"] .ai-session-header h2,
:root[data-theme="dark"] .ai-tool-card strong,
:root[data-theme="dark"] .ai-session-copy strong,
:root[data-theme="dark"] .ai-empty-state h2 { color: #f8fafc; }

@media (max-width: 1180px) {
	.ai-workspace { grid-template-columns: 260px minmax(0, 1fr); }
	.ai-chat-panel { position: static; grid-column: 1 / -1; max-height: none; }
}
@media (max-width: 860px) {
	.ai-topbar { align-items: flex-start; flex-direction: column; }
	.ai-topbar-actions { width: 100%; justify-content: space-between; }
	.ai-shell { padding: 0.85rem; }
	.ai-create-panel, .ai-workspace, .ai-doc-grid, .ai-create-grid { grid-template-columns: 1fr; }
	.ai-create-wide { grid-column: auto; }
	.ai-sidebar, .ai-main-panel, .ai-chat-panel { min-height: auto; }
	.ai-session-header, .ai-create-footer { align-items: stretch; flex-direction: column; }
	.ai-tool-grid { grid-template-columns: 1fr; }
	.ai-btn { width: 100%; }
}
</style>

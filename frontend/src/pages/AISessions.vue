<template>
	<div class="chat-page" @paste="handlePaste">
		<FileUploader
			ref="fileUploader"
			class="hidden"
			:fileTypes="['.pdf', '.doc', '.docx', 'image/*', '.txt', '.md']"
			:uploadArgs="{ private: true }"
			:validateFile="validateFile"
			@success="handleFileUploaded"
		/>

		<aside class="session-rail" :class="{ open: showSessions }">
			<div class="rail-head">
				<div>
					<div class="rail-brand"><Sparkles class="size-4" /> {{ __('Sesiones IA') }}</div>
					<p>{{ access?.is_plus ? __('Plus ilimitado') : accessText }}</p>
				</div>
				<button class="icon-btn mobile-only" @click="showSessions = false"><X class="size-4" /></button>
			</div>
			<button class="primary-btn full" :disabled="!canCreate" @click="startNewSession">
				<Plus class="size-4" /> {{ __('Nueva sesion') }}
			</button>
			<label class="search-box">
				<Search class="size-4" />
				<input v-model="sessionSearch" :placeholder="__('Buscar sesiones')" />
			</label>
			<div class="session-list">
				<button
					v-for="session in filteredSessions"
					:key="session.name"
					class="session-item"
					:class="{ active: activeSession?.name === session.name }"
					@click="openSession(session.name)"
				>
					<MessagesSquare class="size-4" />
					<span>
						<strong>{{ session.title || session.name }}</strong>
						<small>{{ session.model_label || modelLabel(session.model_tier) }} · {{ formatDate(session.modified) }}</small>
					</span>
				</button>
				<div v-if="!filteredSessions.length" class="soft-empty">
					<MessagesSquare class="size-5" />
					{{ __('Tus chats de estudio apareceran aqui.') }}
				</div>
			</div>
		</aside>

		<main class="chat-main">
			<header class="chat-header">
				<div class="header-left">
					<button class="icon-btn mobile-only" @click="showSessions = true">
						<Menu class="size-5" />
					</button>
					<div class="session-title">
						<span>{{ activeSession ? activeSession.title : __('Nuevo chat de estudio') }}</span>
						<small>{{ activeSession ? (activeSession.academic_context || activeSession.goal || __('Con tus fuentes y herramientas')) : __('Crea una sesion y empieza a conversar') }}</small>
					</div>
				</div>
				<div class="header-actions">
					<div class="model-switch">
						<button :class="{ active: selectedModel === 'light' }" @click="selectModel('light')">
							<Zap class="size-4" /> <span>Study Model Light</span>
						</button>
						<button :class="{ active: selectedModel === 'pro', locked: !access?.pro_available }" @click="selectModel('pro')">
							<Crown class="size-4" /> <span>Study Model Pro</span>
						</button>
					</div>
					<button class="icon-btn mobile-only" @click="showTools = true">
						<PanelRight class="size-5" />
					</button>
				</div>
			</header>

			<section v-if="!activeSession" class="new-chat">
				<div class="new-chat-inner">
					<div class="new-badge"><Bot class="size-5" /> {{ __('Study chat') }}</div>
					<h1>{{ __('Que vas a estudiar hoy?') }}</h1>
					<p>{{ __('Crea una sesion, sube tus lecturas o trabajos, y conversa con la IA usando esos documentos como contexto.') }}</p>
					<div class="new-form">
						<input v-model="draft.title" :placeholder="__('Nombre de la sesion, ej. Parcial de calculo')" />
						<div class="new-form-row">
							<select v-model="draft.student_level">
								<option value="colegio">{{ __('Colegio') }}</option>
								<option value="preuniversitario">{{ __('Preuniversitario') }}</option>
								<option value="universitario">{{ __('Universitario') }}</option>
								<option value="profesional">{{ __('Profesional') }}</option>
							</select>
							<input v-model="draft.academic_context" :placeholder="__('Curso o contexto')" />
						</div>
						<textarea v-model="initialPrompt" rows="4" :placeholder="__('Pregunta inicial o instrucciones. Ej: ayudame a estudiar estos PDFs para mi examen.')" />
						<div v-if="pendingFiles.length" class="pending-row">
							<span v-for="file in pendingFiles" :key="file.file_url">{{ file.file_name || file.file_url }}</span>
						</div>
						<div class="new-actions">
							<button class="secondary-btn" @click="openUploader">
								<Upload class="size-4" /> {{ __('Subir fuentes') }}
							</button>
							<button class="primary-btn" :disabled="creating || !canCreate" @click="createSession">
								<SendHorizontal class="size-4" /> {{ creating ? __('Creando...') : __('Crear y chatear') }}
							</button>
						</div>
					</div>
				</div>
			</section>

			<section v-else class="chat-thread" ref="chatBox">
				<div v-if="!chatMessages.length" class="welcome-block">
					<div class="new-badge"><Bot class="size-5" /> {{ activeSession.model_label || modelLabel(activeSession.model_tier) }}</div>
					<h2>{{ __('Listo. Este chat ya conoce tu sesion.') }}</h2>
					<p>{{ __('Sube documentos o pregunta directamente. Las herramientas del panel derecho tambien responderan dentro de este chat.') }}</p>
					<div class="suggestions">
						<button v-for="item in starterPrompts" :key="item" @click="chatInput = item">{{ item }}</button>
					</div>
				</div>
				<div v-for="message in chatMessages" :key="message.created_at || message.content" class="message-row" :class="message.role === 'user' ? 'user' : 'assistant'">
					<div class="avatar">{{ message.role === 'user' ? 'Tu' : 'AI' }}</div>
					<div class="message-bubble">
						<div v-if="message.model_label" class="message-model">{{ message.model_label }}</div>
						<div v-if="message.content" v-html="renderMarkdown(message.content)" />
						<img v-if="message.image_base64" class="chat-image" :src="`data:${message.mime_type || 'image/png'};base64,${message.image_base64}`" :alt="__('Infografia')" />
					</div>
				</div>
				<div v-if="chatLoading || toolLoading" class="message-row assistant">
					<div class="avatar">AI</div>
					<div class="message-bubble typing"><span></span><span></span><span></span></div>
				</div>
			</section>

			<footer v-if="activeSession" class="composer-wrap">
				<div v-if="pendingFiles.length" class="pending-row">
					<span v-for="file in pendingFiles" :key="file.file_url">{{ file.file_name || file.file_url }}</span>
				</div>
				<div class="composer">
					<button class="icon-btn" :title="__('Subir fuentes')" @click="openUploader">
						<Paperclip class="size-5" />
					</button>
					<textarea
						v-model="chatInput"
						rows="1"
						:placeholder="__('Pregunta sobre tus documentos o proyecto')"
						@keydown.enter.exact.prevent="sendChat"
					/>
					<button class="send-btn" :disabled="chatLoading || (!chatInput.trim() && !pendingFiles.length)" @click="sendChat">
						<SendHorizontal class="size-5" />
					</button>
				</div>
				<div class="composer-meta">
					<span>{{ remainingText }}</span>
					<span>{{ materialCountText }}</span>
					<span>Ctrl+V {{ __('para imagenes') }}</span>
				</div>
			</footer>
		</main>

		<aside class="source-panel" :class="{ open: showTools }">
			<div class="panel-head">
				<div>
					<h2>{{ __('Fuentes') }}</h2>
					<p>{{ materialCountText }}</p>
				</div>
				<button class="icon-btn mobile-only" @click="showTools = false"><X class="size-4" /></button>
			</div>
			<button class="secondary-btn full" :disabled="!activeSession" @click="openUploader">
				<Upload class="size-4" /> {{ __('Agregar documentos') }}
			</button>
			<div class="sources-list">
				<div v-for="material in activeSession?.materials || []" :key="material.idx" class="source-item">
					<FileText class="size-4" />
					<span>
						<strong>{{ material.file_name }}</strong>
						<small>{{ material.file_type }} · {{ material.analysis_status || __('Pendiente') }}</small>
					</span>
				</div>
				<div v-if="!activeSession?.materials?.length" class="soft-empty">
					<Upload class="size-5" />
					{{ activeSession ? __('Sube PDFs, trabajos, lecturas o imagenes.') : __('Crea una sesion para agregar fuentes.') }}
				</div>
			</div>

			<div class="tools-head">
				<h2>{{ __('Herramientas academicas') }}</h2>
				<p>{{ __('Responden dentro del chat') }}</p>
			</div>
			<div class="tool-list">
				<button v-for="tool in tools" :key="tool.id" class="tool-card" :class="{ locked: tool.pro && !access?.is_plus }" :disabled="!activeSession || toolLoading" @click="runTool(tool)">
					<component :is="tool.icon" class="size-5" />
					<span>
						<strong>{{ tool.label }}</strong>
						<small>{{ tool.description }}</small>
					</span>
					<Crown v-if="tool.pro && !access?.is_plus" class="size-4 lock-icon" />
				</button>
			</div>
		</aside>

		<div v-if="showSessions || showTools" class="mobile-backdrop" @click="showSessions = false; showTools = false"></div>
	</div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { FileUploader, call, toast, usePageMeta } from 'frappe-ui'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import {
	BookOpenCheck,
	Bot,
	Crown,
	FileQuestion,
	FileText,
	Image as ImageIcon,
	Layers,
	ListTree,
	Menu,
	MessageCircle,
	MessagesSquare,
	Paperclip,
	PanelRight,
	Plus,
	Search,
	SendHorizontal,
	Sigma,
	Sparkles,
	Upload,
	X,
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
const initialPrompt = ref('')
const pendingFiles = ref([])
const fileUploader = ref(null)
const chatBox = ref(null)
const creating = ref(false)
const chatLoading = ref(false)
const toolLoading = ref(false)
const showSessions = ref(false)
const showTools = ref(false)
const sessionSearch = ref('')

const draft = ref({
	title: '',
	goal: '',
	academic_context: '',
	student_level: 'universitario',
	manual_text: '',
	model_tier: 'light',
})

const tools = [
	{ id: 'summary', label: __('Resumen'), description: __('Ideas clave y prioridades'), icon: BookOpenCheck, prompt: __('Resume mis fuentes y dime que estudiar primero.') },
	{ id: 'organize', label: __('Ordenar info'), description: __('Temas, tareas y pendientes'), icon: ListTree, prompt: __('Ordena esta sesion en temas, tareas y pendientes claros.') },
	{ id: 'quiz', label: __('Cuestionario'), description: __('Preguntas con explicacion'), icon: FileQuestion, prompt: __('Crea un cuestionario con respuestas explicadas sobre mis fuentes.') },
	{ id: 'flashcards', label: __('Flashcards'), description: __('Tarjetas y checklist'), icon: Layers, prompt: __('Crea flashcards y una checklist de dominio para esta sesion.') },
	{ id: 'reader_question', label: __('Lectura guiada'), description: __('Pregunta corta por avance'), icon: MessageCircle, prompt: __('Hazme una pregunta corta de comprension sobre lo que estoy leyendo.') },
	{ id: 'math', label: __('Matematica paso a paso'), description: __('Resuelve y practica'), icon: Sigma, prompt: __('Ayudame con matematica: resuelve paso a paso y luego dame un ejercicio mas facil.') },
	{ id: 'infographic', label: __('Infografia'), description: __('Mapa visual de estudio'), icon: ImageIcon, pro: true, prompt: __('Genera una infografia academica sobre esta sesion.') },
]

const starterPrompts = [
	__('Hazme un resumen de mis documentos.'),
	__('Que temas deberia estudiar primero?'),
	__('Crea preguntas para practicar.'),
	__('Explicame lo mas dificil con ejemplos simples.'),
]

const filteredSessions = computed(() => {
	const query = sessionSearch.value.trim().toLowerCase()
	if (!query) return sessions.value
	return sessions.value.filter((session) =>
		[session.title, session.goal, session.academic_context]
			.filter(Boolean)
			.join(' ')
			.toLowerCase()
			.includes(query)
	)
})
const selectedModel = computed(() => activeSession.value?.model_tier || draft.value.model_tier || 'light')
const canCreate = computed(() => access.value?.can_create_session !== false)
const accessText = computed(() => {
	if (!access.value) return ''
	if (access.value.is_plus) return __('Plus ilimitado')
	return `${access.value.active_sessions || 0}/${access.value.free_session_limit || 3} ${__('sesiones')} · ${access.value.messages_remaining ?? 0} ${__('mensajes')}`
})
const remainingText = computed(() => {
	if (!access.value) return ''
	if (access.value.is_plus) return __('Mensajes ilimitados')
	return `${access.value.messages_remaining ?? 0}/${access.value.daily_message_limit || 25} ${__('mensajes hoy')}`
})
const materialCountText = computed(() => {
	const count = activeSession.value?.materials?.length || 0
	const max = access.value?.max_files_per_session || 15
	return `${count}/${max} ${__('fuentes')}`
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
	activeSession.value = await api('get_ai_session', { name })
	currentThread.value = findThread(route.params.threadId) || activeSession.value.threads?.[0] || null
	chatMessages.value = currentThread.value?.messages || []
	await nextTick(scrollChat)
}

function findThread(name) {
	return (activeSession.value?.threads || []).find((thread) => thread.name === name)
}

function modelLabel(tier) {
	return tier === 'pro' ? 'Study Model Pro' : 'Study Model Light'
}

function startNewSession() {
	activeSession.value = null
	currentThread.value = null
	chatMessages.value = []
	chatInput.value = ''
	router.push({ name: 'AISessions' })
}

async function selectModel(model) {
	if (model === 'pro' && !access.value?.pro_available) {
		toast.warning(__('Study Model Pro esta disponible con StudyBadge Plus.'))
		return
	}
	if (!activeSession.value) {
		draft.value.model_tier = model
		return
	}
	activeSession.value = await api('set_ai_session_model', {
		session: activeSession.value.name,
		model_tier: model,
	})
	currentThread.value = activeSession.value.threads?.[0] || currentThread.value
	toast.success(modelLabel(model))
}

async function createSession() {
	if (!canCreate.value) {
		toast.warning(__('Tu plan Free alcanzo el limite de sesiones activas.'))
		return
	}
	const seed = initialPrompt.value.trim()
	creating.value = true
	try {
		const session = await api('create_ai_session', {
			data: {
				...draft.value,
				title: draft.value.title || seed.slice(0, 54) || __('Sesion de estudio'),
				goal: draft.value.goal || seed || __('estudiar con IA'),
				manual_text: draft.value.manual_text || seed,
			},
		})
		activeSession.value = session
		currentThread.value = session.threads?.[0] || null
		chatMessages.value = currentThread.value?.messages || []
		await attachPendingFiles()
		await router.push({ name: 'AISessionRoom', params: { sessionId: session.name } })
		sessions.value = await api('list_ai_sessions')
		if (seed) {
			chatInput.value = seed
			initialPrompt.value = ''
			await sendChat()
		}
		draft.value = { title: '', goal: '', academic_context: '', student_level: 'universitario', manual_text: '', model_tier: 'light' }
	} finally {
		creating.value = false
	}
}

function openSession(name) {
	showSessions.value = false
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
		pendingFiles.value.push(file)
		toast.success(__('Fuente lista. Se agregara al crear la sesion.'))
		return
	}
	activeSession.value = await api('upload_ai_session_material', {
		session: activeSession.value.name,
		file_url: file.file_url,
	})
	pendingFiles.value.push(file)
	toast.success(__('Fuente agregada al chat.'))
}

async function attachPendingFiles() {
	if (!activeSession.value || !pendingFiles.value.length) return
	const files = [...pendingFiles.value]
	pendingFiles.value = []
	for (const file of files) {
		activeSession.value = await api('upload_ai_session_material', {
			session: activeSession.value.name,
			file_url: file.file_url,
		})
	}
}

async function handlePaste(event) {
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
	if (!text && !pendingFiles.value.length) return
	chatLoading.value = true
	try {
		const files = pendingFiles.value.map((file) => file.file_url)
		const optimistic = { role: 'user', content: text || __('Analiza las fuentes adjuntas.'), created_at: String(Date.now()) }
		chatMessages.value = [...chatMessages.value, optimistic]
		chatInput.value = ''
		pendingFiles.value = []
		await nextTick(scrollChat)
		const result = await api('chat_ai_session', {
			session: activeSession.value.name,
			thread: currentThread.value?.name,
			message: text || __('Analiza las fuentes adjuntas.'),
			files,
			model_tier: activeSession.value.model_tier,
		})
		currentThread.value = result.thread
		chatMessages.value = result.thread.messages || []
		access.value = result.access || access.value
		await nextTick(scrollChat)
	} finally {
		chatLoading.value = false
	}
}

async function runTool(tool) {
	if (tool.pro && !access.value?.is_plus) {
		toast.warning(__('Esta herramienta esta disponible con StudyBadge Plus.'))
		return
	}
	if (!activeSession.value) return
	toolLoading.value = true
	showTools.value = false
	try {
		chatMessages.value = [
			...chatMessages.value,
			{ role: 'user', content: tool.prompt, created_at: String(Date.now()) },
		]
		await nextTick(scrollChat)
		const result = await api('generate_ai_tool', {
			session: activeSession.value.name,
			thread: currentThread.value?.name,
			tool: tool.id,
			payload: {
				prompt: tool.prompt,
				topic: activeSession.value.goal || activeSession.value.title,
				position: activeSession.value.reader_progress || {},
			},
		})
		if (result.thread) {
			currentThread.value = result.thread
			chatMessages.value = result.thread.messages || []
		}
		access.value = result.access || access.value
		await nextTick(scrollChat)
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
.chat-page { display: grid; grid-template-columns: 280px minmax(0, 1fr) 330px; min-height: 100vh; background: #f7f8fb; color: #101827; }
.session-rail, .source-panel { background: #fff; border-color: #e5e7eb; border-style: solid; min-height: 100vh; padding: 1rem; }
.session-rail { border-width: 0 1px 0 0; }
.source-panel { border-width: 0 0 0 1px; }
.rail-head, .panel-head, .chat-header, .header-left, .header-actions, .new-actions { display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; }
.rail-brand, .new-badge { display: inline-flex; align-items: center; gap: 0.45rem; font-weight: 900; color: #2563eb; }
.rail-head p, .panel-head p, .tools-head p, .session-title small, .source-item small, .session-item small, .composer-meta, .new-chat p, .welcome-block p { color: #64748b; font-size: 0.78rem; }
.primary-btn, .secondary-btn, .icon-btn, .send-btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; border-radius: 8px; font-weight: 900; transition: 0.18s ease; }
.primary-btn { min-height: 40px; border: 1px solid #2563eb; background: #2563eb; color: #fff; padding: 0.6rem 0.85rem; }
.secondary-btn { min-height: 40px; border: 1px solid #dbe3ef; background: #fff; color: #0f172a; padding: 0.6rem 0.85rem; }
.primary-btn:disabled, .secondary-btn:disabled, .send-btn:disabled, .tool-card:disabled { cursor: not-allowed; opacity: 0.55; }
.full { width: 100%; margin-top: 0.85rem; }
.icon-btn { width: 38px; height: 38px; border: 1px solid #dbe3ef; background: #fff; color: #334155; }
.search-box { display: flex; align-items: center; gap: 0.5rem; margin: 0.85rem 0; border: 1px solid #dbe3ef; border-radius: 8px; background: #f8fafc; padding: 0.55rem 0.7rem; color: #64748b; }
.search-box input { min-width: 0; flex: 1; border: 0; outline: 0; background: transparent; color: #0f172a; font-size: 0.88rem; }
.session-list, .sources-list, .tool-list { display: flex; flex-direction: column; gap: 0.55rem; }
.session-item, .source-item, .tool-card { display: flex; align-items: flex-start; gap: 0.7rem; border: 1px solid transparent; border-radius: 8px; padding: 0.75rem; text-align: left; }
.session-item { width: 100%; background: transparent; color: #334155; }
.session-item:hover, .session-item.active { background: #eff6ff; border-color: #bfdbfe; color: #1d4ed8; }
.session-item span, .source-item span, .tool-card span { min-width: 0; display: flex; flex-direction: column; gap: 0.15rem; }
.session-item strong, .source-item strong, .tool-card strong { color: #0f172a; font-size: 0.9rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.chat-main { display: grid; grid-template-rows: auto 1fr auto; min-width: 0; height: 100vh; }
.chat-header { position: sticky; top: 0; z-index: 5; min-height: 68px; border-bottom: 1px solid #e5e7eb; background: rgba(255,255,255,0.92); padding: 0.75rem 1rem; backdrop-filter: blur(12px); }
.session-title { display: flex; min-width: 0; flex-direction: column; }
.session-title span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #0f172a; font-size: 1rem; font-weight: 900; }
.model-switch { display: inline-flex; gap: 0.35rem; border: 1px solid #dbe3ef; border-radius: 999px; background: #f8fafc; padding: 0.25rem; }
.model-switch button { display: inline-flex; align-items: center; gap: 0.35rem; border: 0; border-radius: 999px; background: transparent; color: #64748b; padding: 0.45rem 0.7rem; font-size: 0.78rem; font-weight: 900; }
.model-switch button.active { background: #2563eb; color: white; }
.model-switch button.locked { color: #92400e; }
.new-chat, .chat-thread { min-height: 0; overflow-y: auto; }
.new-chat { display: grid; place-items: center; padding: 2rem; }
.new-chat-inner { width: min(760px, 100%); text-align: center; }
.new-chat h1 { margin-top: 0.8rem; color: #0f172a; font-size: clamp(2rem, 6vw, 4rem); line-height: 1; font-weight: 950; letter-spacing: 0; }
.new-chat p { margin: 1rem auto 0; max-width: 620px; font-size: 1rem; line-height: 1.7; }
.new-form { margin-top: 1.5rem; border: 1px solid #dbe3ef; border-radius: 8px; background: #fff; padding: 1rem; box-shadow: 0 20px 50px rgba(15,23,42,0.07); text-align: left; }
.new-form input, .new-form select, .new-form textarea { width: 100%; border: 1px solid #dbe3ef; border-radius: 8px; background: #fff; color: #0f172a; outline: 0; padding: 0.75rem; }
.new-form textarea { margin-top: 0.7rem; resize: vertical; }
.new-form-row { display: grid; grid-template-columns: 190px 1fr; gap: 0.7rem; margin-top: 0.7rem; }
.chat-thread { padding: 1.5rem max(1rem, calc((100% - 860px) / 2)); }
.welcome-block { display: grid; place-items: center; min-height: 55vh; text-align: center; }
.welcome-block h2 { margin-top: 0.75rem; color: #0f172a; font-size: 1.6rem; font-weight: 950; }
.suggestions { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.55rem; margin-top: 1rem; }
.suggestions button { border: 1px solid #dbe3ef; border-radius: 999px; background: #fff; color: #334155; padding: 0.55rem 0.8rem; font-weight: 800; }
.message-row { display: grid; grid-template-columns: 42px minmax(0, 1fr); gap: 0.75rem; margin: 1rem 0; }
.message-row.user .message-bubble { background: #2563eb; color: #fff; margin-left: auto; }
.avatar { display: grid; width: 36px; height: 36px; place-items: center; border-radius: 999px; background: #e0e7ff; color: #3730a3; font-size: 0.72rem; font-weight: 950; }
.message-bubble { max-width: 780px; border: 1px solid #e5e7eb; border-radius: 8px; background: #fff; padding: 0.9rem 1rem; color: #111827; line-height: 1.7; box-shadow: 0 8px 28px rgba(15,23,42,0.04); }
.message-bubble :deep(ul), .message-bubble :deep(ol) { padding-left: 1.25rem; }
.message-model { margin-bottom: 0.35rem; color: #2563eb; font-size: 0.72rem; font-weight: 900; }
.chat-image { display: block; width: min(100%, 620px); margin-top: 0.75rem; border: 1px solid #dbe3ef; border-radius: 8px; background: white; }
.typing span { display: inline-block; width: 7px; height: 7px; margin-right: 0.3rem; border-radius: 999px; background: #94a3b8; animation: pulse 1s infinite ease-in-out; }
.typing span:nth-child(2) { animation-delay: 0.12s; }
.typing span:nth-child(3) { animation-delay: 0.24s; }
@keyframes pulse { 0%, 80%, 100% { opacity: 0.3; transform: translateY(0); } 40% { opacity: 1; transform: translateY(-3px); } }
.composer-wrap { border-top: 1px solid #e5e7eb; background: rgba(247,248,251,0.96); padding: 0.75rem max(1rem, calc((100% - 860px) / 2)); }
.composer { display: flex; align-items: flex-end; gap: 0.55rem; border: 1px solid #dbe3ef; border-radius: 8px; background: #fff; padding: 0.55rem; box-shadow: 0 16px 40px rgba(15,23,42,0.07); }
.composer textarea { min-height: 42px; max-height: 180px; flex: 1; resize: vertical; border: 0; outline: 0; padding: 0.55rem; line-height: 1.5; }
.send-btn { width: 42px; height: 42px; border: 0; background: #2563eb; color: #fff; }
.composer-meta { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.8rem; padding-top: 0.45rem; font-weight: 700; }
.pending-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.55rem; }
.pending-row span { border-radius: 999px; background: #ecfdf5; color: #047857; padding: 0.25rem 0.55rem; font-size: 0.76rem; font-weight: 900; }
.panel-head h2, .tools-head h2 { color: #0f172a; font-size: 1rem; font-weight: 950; }
.source-item { background: #f8fafc; border-color: #edf2f7; }
.source-item svg, .tool-card svg { flex-shrink: 0; color: #2563eb; margin-top: 0.1rem; }
.tools-head { margin: 1.25rem 0 0.7rem; }
.tool-card { position: relative; width: 100%; background: #fff; border-color: #dbe3ef; }
.tool-card:hover:not(:disabled) { border-color: #93c5fd; background: #eff6ff; }
.tool-card.locked { background: #fffbeb; border-color: #fde68a; }
.tool-card small { color: #64748b; }
.lock-icon { margin-left: auto; color: #f59e0b !important; }
.soft-empty { display: grid; min-height: 110px; place-items: center; border: 1px dashed #cbd5e1; border-radius: 8px; color: #64748b; padding: 1rem; text-align: center; font-size: 0.86rem; }
.mobile-only { display: none; }
.mobile-backdrop { display: none; }
:root[data-theme="dark"] .chat-page { background: #0f172a; color: #e5e7eb; }
:root[data-theme="dark"] .session-rail,
:root[data-theme="dark"] .source-panel,
:root[data-theme="dark"] .chat-header,
:root[data-theme="dark"] .new-form,
:root[data-theme="dark"] .message-bubble,
:root[data-theme="dark"] .composer,
:root[data-theme="dark"] .tool-card,
:root[data-theme="dark"] .source-item { background: #111827; border-color: rgba(255,255,255,0.09); color: #e5e7eb; }
:root[data-theme="dark"] .session-title span,
:root[data-theme="dark"] .new-chat h1,
:root[data-theme="dark"] .welcome-block h2,
:root[data-theme="dark"] .panel-head h2,
:root[data-theme="dark"] .tools-head h2,
:root[data-theme="dark"] .session-item strong,
:root[data-theme="dark"] .source-item strong,
:root[data-theme="dark"] .tool-card strong { color: #f8fafc; }
:root[data-theme="dark"] .search-box,
:root[data-theme="dark"] .model-switch { background: #0b1220; border-color: rgba(255,255,255,0.1); }
:root[data-theme="dark"] .new-form input,
:root[data-theme="dark"] .new-form select,
:root[data-theme="dark"] .new-form textarea { background: #0b1220; border-color: rgba(255,255,255,0.1); color: #e5e7eb; }
@media (max-width: 1180px) {
	.chat-page { grid-template-columns: 250px minmax(0, 1fr); }
	.source-panel { position: fixed; top: 0; right: 0; z-index: 40; width: min(360px, 88vw); transform: translateX(100%); transition: transform 0.2s ease; box-shadow: -20px 0 50px rgba(15,23,42,0.18); }
	.source-panel.open { transform: translateX(0); }
	.mobile-only { display: inline-flex; }
	.mobile-backdrop { display: block; position: fixed; inset: 0; z-index: 30; background: rgba(15,23,42,0.38); }
}
@media (max-width: 760px) {
	.chat-page { display: block; }
	.session-rail { position: fixed; top: 0; left: 0; z-index: 40; width: min(330px, 88vw); transform: translateX(-100%); transition: transform 0.2s ease; box-shadow: 20px 0 50px rgba(15,23,42,0.18); }
	.session-rail.open { transform: translateX(0); }
	.chat-main { height: 100vh; }
	.chat-header { min-height: 62px; padding: 0.55rem; }
	.header-actions { gap: 0.4rem; }
	.model-switch button { padding: 0.42rem 0.55rem; }
	.model-switch span { display: none; }
	.new-chat { padding: 1rem; }
	.new-chat h1 { font-size: 2.1rem; }
	.new-form-row { grid-template-columns: 1fr; }
	.chat-thread { padding: 1rem; }
	.message-row { grid-template-columns: 32px minmax(0, 1fr); gap: 0.5rem; }
	.avatar { width: 30px; height: 30px; font-size: 0.62rem; }
	.message-bubble { max-width: 100%; padding: 0.8rem; }
	.composer-wrap { padding: 0.6rem; }
	.composer-meta { justify-content: flex-start; font-size: 0.7rem; }
}
</style>

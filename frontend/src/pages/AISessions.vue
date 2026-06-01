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
					<h1>{{ __('¿Qué vas a estudiar hoy?') }}</h1>
					<p>{{ __('Crea una sesion, sube tus lecturas o trabajos, y conversa con la IA usando esos documentos como contexto.') }}</p>
						<div class="new-form">
						<div class="form-group main-group">
							<label>{{ __('¿Qué vas a estudiar?') }}</label>
							<input v-model="draft.title" class="title-input" :placeholder="__('Ej: Parcial de Cálculo, Tesis, Lectura de Filosofía...')" />
						</div>

						<button class="toggle-advanced-btn" @click="showAdvanced = !showAdvanced">
							<Settings class="size-4" /> 
							{{ showAdvanced ? __('Ocultar detalles') : __('Añadir más detalles (opcional)') }}
						</button>
						
						<div v-show="showAdvanced" class="advanced-options">
							<div class="new-form-row">
								<div class="form-group">
									<label>{{ __('Tu Nivel Académico') }}</label>
									<select v-model="draft.student_level">
										<option value="colegio">{{ __('Colegio') }}</option>
										<option value="preuniversitario">{{ __('Preuniversitario') }}</option>
										<option value="universitario">{{ __('Universitario') }}</option>
										<option value="profesional">{{ __('Profesional') }}</option>
									</select>
								</div>
								<div class="form-group">
									<label>{{ __('Materia o Contexto') }}</label>
									<input v-model="draft.academic_context" :placeholder="__('Ej: Ingeniería de Sistemas')" />
								</div>
							</div>
							
							<div class="form-group mt-3">
								<label>{{ __('Instrucciones para la IA') }}</label>
								<textarea v-model="initialPrompt" rows="2" :placeholder="__('Ej: Resúmeme los conceptos clave con ejemplos...')" />
							</div>
						</div>
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
					<h2>{{ __('Listo. Este chat ya conoce tu sesión.') }}</h2>
					<p>{{ __('Sube documentos o pregunta directamente. Las herramientas del panel derecho también responderán dentro de este chat.') }}</p>
					<div class="suggestions">
						<button v-for="item in starterPrompts" :key="item" @click="chatInput = item">{{ item }}</button>
					</div>
				</div>
				<div v-for="message in chatMessages" :key="message.created_at || message.content" class="message-row" :class="message.role === 'user' ? 'user' : 'assistant'">
					<div class="avatar">
						<User v-if="message.role === 'user'" class="size-4" />
						<Bot v-else class="size-5" />
					</div>
					<div class="message-bubble">
						<div v-if="message.model_label" class="message-model">{{ message.model_label }}</div>
						<div v-if="message.content" v-html="renderMarkdown(message.content)" />
						<img v-if="message.image_base64" class="chat-image" :src="`data:${message.mime_type || 'image/png'};base64,${message.image_base64}`" :alt="__('Infografia')" />
					</div>
				</div>
				<div v-if="chatLoading || toolLoading" class="message-row assistant">
					<div class="avatar"><Bot class="size-5" /></div>
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
					<button class="icon-btn" :class="{ 'active-search': useSearch }" :title="__('Activar búsqueda en Google')" @click="useSearch = !useSearch">
						<Globe class="size-5" />
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
					<span class="mobile-only">{{ __('Ctrl+V para imagenes') }}</span>
					<a v-if="access && !access.is_plus && access.messages_remaining <= 0" href="https://academy.studybadge.com/lms/plus" target="_blank" class="upgrade-link">
						{{ __('👑 Mejora a Plus') }}
					</a>
				</div>
			</footer>
		</main>

		<aside class="source-panel" :class="{ open: showTools }">
			<div class="panel-head">
				<div>
					<h2>{{ __('Panel de Sesión') }}</h2>
				</div>
				<button class="icon-btn mobile-only" @click="showTools = false"><X class="size-4" /></button>
			</div>

			<div v-if="activeSession" class="tools-head mt-0">
				<h2>{{ __('Chats') }}</h2>
				<p>{{ __('Historial de esta sesión') }}</p>
			</div>
			<button v-if="activeSession" class="secondary-btn full" @click="startNewThread">
				<Plus class="size-4" /> {{ __('Nuevo chat') }}
			</button>
			<div v-if="activeSession" class="sources-list scrollable-list">
				<button v-for="thread in activeSession?.threads || []" :key="thread.name" class="session-item" :class="{ active: currentThread?.name === thread.name }" @click="switchThread(thread)">
					<MessageCircle class="size-4 mt-1" />
					<span>
						<strong>{{ thread.title || __('Chat') }}</strong>
						<small>{{ formatDate(thread.modified) }}</small>
					</span>
				</button>
			</div>

			<div class="tools-head mt-0">
				<h2>{{ __('Fuentes') }}</h2>
				<p>{{ materialCountText }}</p>
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

		<QuizModal v-model:show="showQuiz" :loading="modalLoading" :data="modalData" />
		<FlashcardsModal v-model:show="showFlashcards" :loading="modalLoading" :data="modalData" />
		<GuidedReadingModal v-model:show="showGuidedReading" :loading="modalLoading" :data="modalData" :materials="activeSession?.materials || []" :history="readerHistory" @request-question="requestGuidedQuestion" @verify-answer="verifyGuidedAnswer" />
		<MathModal v-model:show="showMath" :loading="modalLoading" :data="modalData" />
	</div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { FileUploader, call, toast, usePageMeta } from 'frappe-ui'
import MarkdownIt from 'markdown-it'
import mk from 'markdown-it-katex'
import 'katex/dist/katex.min.css'
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
	Settings,
	Sigma,
	Upload,
	User,
	Wrench,
	X,
	Zap,
	Globe,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import QuizModal from '@/components/QuizModal.vue'
import FlashcardsModal from '@/components/FlashcardsModal.vue'
import GuidedReadingModal from '@/components/GuidedReadingModal.vue'
import MathModal from '@/components/MathModal.vue'

const route = useRoute()
const router = useRouter()
const { brand } = sessionStore()
const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true }).use(mk)

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

const showAdvanced = ref(false)

const readerHistory = ref([])
const showSessions = ref(false)
const showTools = ref(false)
const sessionSearch = ref('')
const useSearch = ref(false)

const showQuiz = ref(false)
const showFlashcards = ref(false)
const showGuidedReading = ref(false)
const showMath = ref(false)
const modalData = ref(null)
const modalLoading = ref(false)

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
		if (seed) {
			chatInput.value = seed
			initialPrompt.value = ''
			await sendChat()
		}
		await router.push({ name: 'AISessionRoom', params: { sessionId: session.name } })
		sessions.value = await api('list_ai_sessions')
		draft.value = { title: '', goal: '', academic_context: '', student_level: 'universitario', manual_text: '', model_tier: 'light' }
	} finally {
		creating.value = false
	}
}

function openSession(name) {
	showSessions.value = false
	router.push({ name: 'AISessionRoom', params: { sessionId: name } })
}

function startNewThread() {
	currentThread.value = null
	chatMessages.value = []
	chatInput.value = ''
	showTools.value = false
	toast.success(__('Escribe un mensaje para iniciar el nuevo chat.'))
}

function switchThread(thread) {
	currentThread.value = thread
	chatMessages.value = thread.messages || []
	showTools.value = false
	nextTick(scrollChat)
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
			use_search: useSearch.value ? 1 : 0,
		})
		
		if (result.trigger_modal) {
			const toolId = result.trigger_modal
			if (toolId === 'quiz') showQuiz.value = true
			if (toolId === 'flashcards') showFlashcards.value = true
			if (toolId === 'reader_question') showGuidedReading.value = true
			if (toolId === 'math') showMath.value = true
			
			modalLoading.value = true
			modalData.value = null
			chatMessages.value = chatMessages.value.filter(m => m !== optimistic)
			
			try {
				const toolResult = await api('generate_ai_tool', {
					session: activeSession.value.name,
					thread: currentThread.value?.name,
					tool: toolId,
					payload: { prompt: text || '' },
				})
				modalData.value = toolResult.result
				access.value = toolResult.access || access.value
			} catch (e) {
				toast.error(__('No se pudo generar el contenido. Intenta de nuevo.'))
			} finally {
				modalLoading.value = false
			}
			return
		}

		const isNewThread = !currentThread.value
		currentThread.value = result.thread
		chatMessages.value = result.thread.messages || []
		if (isNewThread) {
			activeSession.value.threads = [result.thread, ...(activeSession.value.threads || [])]
		}
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
	
	if (['quiz', 'flashcards', 'reader_question', 'math'].includes(tool.id)) {
		showTools.value = false
		if (tool.id === 'quiz') showQuiz.value = true
		if (tool.id === 'flashcards') showFlashcards.value = true
		if (tool.id === 'reader_question') {
			showGuidedReading.value = true
			return
		}
		if (tool.id === 'math') showMath.value = true
		
		modalLoading.value = true
		modalData.value = null
		try {
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
			modalData.value = result.result
			access.value = result.access || access.value
		} catch (err) {
			toast.error(__('Ocurrió un error al cargar la herramienta.'))
		} finally {
			modalLoading.value = false
		}
		return
	}

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

async function requestGuidedQuestion(material) {
	if (!activeSession.value) return
	if (!material) return // Must select a material first
	
	modalLoading.value = true
	try {
		const result = await api('generate_ai_tool', {
			session: activeSession.value.name,
			thread: currentThread.value?.name,
			tool: 'reader_question',
			payload: { 
				topic: activeSession.value.goal, 
				material_selected: material.file_name,
				instruction: 'Genera la primera pregunta sobre la Parte 1 del documento seleccionado.' 
			},
		})
		modalData.value = result.result
		access.value = result.access || access.value
	} catch (e) {
		toast.error(__('No se pudo generar la pregunta.'))
	} finally {
		modalLoading.value = false
	}
}

async function verifyGuidedAnswer(answer) {
	if (!activeSession.value) return
	modalLoading.value = true
	const currentQuestion = modalData.value?.question
	try {
		const payloadPrompt = currentQuestion 
			? `Mi respuesta a tu pregunta ("${currentQuestion}") es: "${answer}". Evalúa mi respuesta brevemente.` 
			: `Evalúa esta respuesta: "${answer}"`
			
		const result = await api('generate_ai_tool', {
			session: activeSession.value.name,
			thread: currentThread.value?.name,
			tool: 'reader_question',
			payload: { prompt: payloadPrompt, topic: activeSession.value.goal },
		})
		
		const resultData = result.result
		if (resultData.evaluation && currentQuestion) {
			readerHistory.value.push({
				question: currentQuestion,
				answer: answer,
				evaluation: resultData.evaluation
			})
		}
		
		modalData.value = resultData
		access.value = result.access || access.value
	} catch (e) {
		toast.error(__('No se pudo verificar la respuesta.'))
	} finally {
		modalLoading.value = false
	}
}

function renderMarkdown(text) {
	if (!text) return ''
	return DOMPurify.sanitize(markdown.render(String(text)), {
		ADD_TAGS: ['math', 'semantics', 'mrow', 'mi', 'mo', 'mn', 'msup', 'mspace', 'mtd', 'mtr', 'mtable', 'annotation', 'mfrac', 'msqrt', 'mroot', 'mstyle', 'merror', 'mpadded', 'mphantom', 'mfenced', 'menclose', 'msub', 'msubsup', 'munderover', 'mover', 'munder'],
		ADD_ATTR: ['display', 'xmlns', 'encoding', 'aria-hidden', 'class', 'style', 'href', 'target'],
	})
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
.chat-page { display: grid; grid-template-columns: 280px minmax(0, 1fr) 330px; height: 100vh; overflow: hidden; background: #f7f8fb; color: #101827; }
.session-rail, .source-panel { background: #fff; border-color: #e5e7eb; border-style: solid; height: 100vh; overflow-y: auto; padding: 1rem; position: relative; z-index: 10; }
.session-rail { border-width: 0 1px 0 0; }
.source-panel { border-width: 0 0 0 1px; }
.rail-head, .panel-head, .chat-header, .header-left, .header-actions, .new-actions { display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; }
.rail-brand { display: inline-flex; align-items: center; gap: 0.45rem; font-weight: 900; color: #2563eb; }
.new-badge { display: inline-flex; align-items: center; gap: 0.45rem; font-weight: 800; font-size: 0.95rem; color: #2563eb; background: #eff6ff; padding: 0.4rem 0.85rem; border-radius: 999px; margin-bottom: 0.5rem; }
.rail-head p, .panel-head p, .tools-head p, .session-title small, .source-item small, .session-item small, .composer-meta, .new-chat p, .welcome-block p { color: #64748b; font-size: 0.78rem; }
.primary-btn, .secondary-btn, .icon-btn, .send-btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; border-radius: 8px; font-weight: 900; transition: 0.18s ease; }
.primary-btn { min-height: 40px; border: 1px solid #2563eb; background: #2563eb; color: #fff; padding: 0.6rem 0.85rem; }
.secondary-btn { min-height: 40px; border: 1px solid #dbe3ef; background: #fff; color: #0f172a; padding: 0.6rem 0.85rem; }
.primary-btn:disabled, .secondary-btn:disabled, .send-btn:disabled, .tool-card:disabled { cursor: not-allowed; opacity: 0.55; }
.full { width: 100%; margin-top: 0.85rem; }
.icon-btn { width: 38px; height: 38px; border: 1px solid #dbe3ef; background: #fff; color: #334155; }
.icon-btn.active-search { background: #eff6ff; color: #2563eb; border-color: #bfdbfe; }
.search-box { display: flex; align-items: center; gap: 0.5rem; margin: 0.85rem 0; border: 1px solid #dbe3ef; border-radius: 8px; background: #f8fafc; padding: 0.55rem 0.7rem; color: #64748b; }
.search-box input { min-width: 0; flex: 1; border: 0; outline: 0; background: transparent; color: #0f172a; font-size: 0.88rem; }
.session-list, .sources-list, .tool-list { display: flex; flex-direction: column; gap: 0.65rem; }
.scrollable-list { margin-top: 0.5rem; margin-bottom: 1rem; max-height: 250px; overflow-y: auto; padding-right: 0.25rem; }
.session-item, .source-item, .tool-card { display: flex; align-items: flex-start; gap: 0.75rem; border: 1px solid transparent; border-radius: 12px; padding: 0.85rem; text-align: left; transition: all 0.2s ease; }
.session-item { width: 100%; background: transparent; color: #334155; }
.session-item:hover, .session-item.active { background: #eff6ff; border-color: #bfdbfe; color: #1d4ed8; }
.session-item span, .source-item span, .tool-card span { min-width: 0; display: flex; flex-direction: column; gap: 0.15rem; }
.session-item strong, .source-item strong, .tool-card strong { color: #0f172a; font-size: 0.9rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.chat-main { display: grid; grid-template-rows: auto 1fr auto; min-width: 0; height: 100vh; }
.chat-header { position: sticky; top: 0; z-index: 5; min-height: 68px; border-bottom: 1px solid #e5e7eb; background: rgba(255,255,255,0.92); padding: 0.75rem 1rem; backdrop-filter: blur(12px); }
.header-left { flex: 1; min-width: 0; justify-content: flex-start; }
.header-actions { flex-shrink: 0; }
.session-title { display: flex; min-width: 0; flex-direction: column; }
.session-title span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #0f172a; font-size: 1rem; font-weight: 900; }
.model-switch { display: inline-flex; gap: 0.35rem; border: 1px solid #dbe3ef; border-radius: 999px; background: #f8fafc; padding: 0.25rem; }
.model-switch button { display: inline-flex; align-items: center; gap: 0.35rem; border: 0; border-radius: 999px; background: transparent; color: #64748b; padding: 0.45rem 0.7rem; font-size: 0.78rem; font-weight: 900; white-space: nowrap; }
.model-switch button.active { background: #2563eb; color: white; }
.model-switch button.locked { color: #92400e; }
.new-chat, .chat-thread { min-height: 0; overflow-y: auto; overflow-x: hidden; }
.new-chat { display: grid; place-items: center; padding: 2rem; }
.new-chat-inner { width: min(760px, 100%); text-align: center; }
.new-chat h1 { margin-top: 0.8rem; color: #0f172a; font-size: clamp(2rem, 6vw, 4rem); line-height: 1; font-weight: 950; letter-spacing: 0; }
.new-chat p { margin: 1rem auto 0; max-width: 620px; font-size: 1rem; line-height: 1.7; }
.new-form { margin-top: 2rem; border: 1px solid #e2e8f0; border-radius: 16px; background: #fff; padding: 1.5rem; box-shadow: 0 10px 30px rgba(15,23,42,0.04); text-align: left; }
.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-group label { font-size: 0.85rem; font-weight: 700; color: #475569; }
.new-form input, .new-form select, .new-form textarea { width: 100%; border: 1px solid #cbd5e1; border-radius: 10px; background: #f8fafc; color: #0f172a; outline: 0; padding: 0.85rem 1rem; font-size: 0.95rem; transition: all 0.2s; }
.new-form input:focus, .new-form select:focus, .new-form textarea:focus { border-color: #3b82f6; background: #fff; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
.title-input { font-size: 1.1rem !important; font-weight: 700; padding: 1rem !important; }
.new-form textarea { resize: vertical; }
.new-form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.5rem; }
.toggle-advanced-btn { display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; font-weight: 700; color: #64748b; background: transparent; border: 0; padding: 0.5rem 0; margin-top: 0.75rem; cursor: pointer; transition: color 0.2s; }
.toggle-advanced-btn:hover { color: #2563eb; }
.advanced-options { margin-top: 0.5rem; padding-top: 1rem; border-top: 1px dashed #e2e8f0; animation: fadeInDown 0.3s ease; }
.mt-3 { margin-top: 0.75rem; }
.mt-0 { margin-top: 0 !important; }
.mt-1 { margin-top: 0.25rem !important; }

@keyframes fadeInDown {
	from { opacity: 0; transform: translateY(-5px); }
	to { opacity: 1; transform: translateY(0); }
}

.chat-thread { padding: 1.5rem max(1rem, calc((100% - 860px) / 2)); padding-bottom: 2rem; }
.welcome-block { display: grid; place-items: center; min-height: 55vh; text-align: center; }
.welcome-block h2 { margin-top: 0.75rem; color: #0f172a; font-size: clamp(1.2rem, 3.5vw, 1.8rem); font-weight: 950; text-wrap: balance; max-width: 800px; line-height: 1.35; }
.suggestions { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.85rem; margin-top: 1.8rem; width: 100%; max-width: 720px; }
.suggestions button { display: flex; align-items: center; justify-content: center; border: 1px solid #dbe3ef; border-radius: 12px; background: #fff; color: #334155; padding: 0.85rem 1.2rem; font-weight: 800; font-size: 0.95rem; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(15,23,42,0.02); }
.suggestions button:hover { background: #eff6ff; border-color: #bfdbfe; color: #1d4ed8; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(37,99,235,0.08); }

/* Chat Messages Modernization */
.message-row { 
	display: flex; 
	gap: 0.85rem; 
	margin: 1.5rem 0; 
	animation: messageSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
	opacity: 0;
	transform: translateY(15px);
}
.message-row.user {
	flex-direction: row-reverse;
}

.avatar { 
	flex-shrink: 0; 
	display: grid; 
	width: 38px; 
	height: 38px; 
	place-items: center; 
	border-radius: 12px; 
	transition: all 0.2s ease;
}
.message-row.user .avatar {
	background: #eff6ff; 
	color: #2563eb; 
}
.message-row.assistant .avatar {
	background: #fff; 
	border: 1px solid #e2e8f0; 
	color: #334155;
	box-shadow: 0 2px 8px rgba(15,23,42,0.04);
}

.message-bubble { 
	max-width: calc(100% - 3.5rem); 
	width: fit-content;
	min-width: 0;
	border-radius: 18px; 
	padding: 1rem 1.25rem; 
	color: #1f2937; 
	line-height: 1.75; 
	font-size: 0.95rem; 
	box-shadow: 0 4px 24px rgba(15,23,42,0.04); 
	border: 1px solid rgba(255,255,255,0.4);
	word-wrap: break-word;
	overflow-wrap: break-word;
}
.message-row.user .message-bubble { 
	background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
	color: #fff; 
	border-bottom-right-radius: 4px;
	box-shadow: 0 8px 24px rgba(37,99,235,0.2);
	border: none;
}
.message-row.assistant .message-bubble {
	background: rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(12px);
	border-bottom-left-radius: 4px;
	border: 1px solid #f1f5f9;
}

@keyframes messageSlideIn {
	0% { opacity: 0; transform: translateY(15px) scale(0.98); }
	100% { opacity: 1; transform: translateY(0) scale(1); }
}
.message-bubble :deep(p) { margin-bottom: 0.85rem; }
.message-bubble :deep(p:last-child) { margin-bottom: 0; }
.message-bubble :deep(ul) { list-style-type: disc; padding-left: 1.5rem; margin-bottom: 0.85rem; }
.message-bubble :deep(ol) { list-style-type: decimal; padding-left: 1.5rem; margin-bottom: 0.85rem; }
.message-bubble :deep(li) { margin-bottom: 0.35rem; }
.message-bubble :deep(li > p) { margin-bottom: 0.35rem; }
.message-bubble :deep(h1), .message-bubble :deep(h2), .message-bubble :deep(h3), .message-bubble :deep(h4) { margin-top: 1.5rem; margin-bottom: 0.75rem; font-weight: 800; color: #0f172a; line-height: 1.3; }
.message-bubble :deep(h1) { font-size: 1.4rem; }
.message-bubble :deep(h2) { font-size: 1.25rem; }
.message-bubble :deep(h3) { font-size: 1.1rem; }
.message-bubble :deep(h4) { font-size: 1rem; }
.message-bubble :deep(strong) { font-weight: 700; color: inherit; opacity: 0.95; }
.message-bubble :deep(em) { font-style: italic; }
.message-bubble :deep(hr) { margin: 1.5rem 0; border: 0; border-top: 1px solid #e5e7eb; }
.message-bubble :deep(blockquote) { border-left: 4px solid #e2e8f0; padding-left: 1rem; color: #475569; font-style: italic; margin-bottom: 0.85rem; }
.message-bubble :deep(.katex-display) { overflow-x: auto; overflow-y: hidden; padding: 0.5rem 0; margin: 1em 0; }
.message-bubble :deep(.katex) { font-size: 1.05em; }
.message-model { margin-bottom: 0.5rem; color: #2563eb; font-size: 0.72rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.05em; }
.chat-image { display: block; width: min(100%, 620px); margin-top: 0.75rem; border: 1px solid #dbe3ef; border-radius: 8px; background: white; }
.typing span { display: inline-block; width: 7px; height: 7px; margin-right: 0.3rem; border-radius: 999px; background: #94a3b8; animation: pulse 1s infinite ease-in-out; }
.typing span:nth-child(2) { animation-delay: 0.12s; }
.typing span:nth-child(3) { animation-delay: 0.24s; }
@keyframes pulse { 0%, 80%, 100% { opacity: 0.3; transform: translateY(0); } 40% { opacity: 1; transform: translateY(-3px); } }
.composer-wrap { border-top: 1px solid #e5e7eb; background: rgba(247,248,251,0.96); padding: 0.75rem max(1rem, calc((100% - 860px) / 2)); }
.composer { display: flex; align-items: flex-end; gap: 0.55rem; border: 1px solid #dbe3ef; border-radius: 8px; background: #fff; padding: 0.55rem; box-shadow: 0 16px 40px rgba(15,23,42,0.07); }
.composer textarea { min-height: 42px; max-height: 180px; flex: 1; resize: vertical; border: 0; outline: 0; padding: 0.55rem; line-height: 1.5; }
.send-btn { width: 42px; height: 42px; border: 0; background: #2563eb; color: #fff; }
.composer-meta { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.8rem; padding-top: 0.45rem; font-weight: 700; }
.upgrade-link { color: #d97706; font-weight: 800; text-decoration: none; display: inline-flex; align-items: center; gap: 0.25rem; background: #fef3c7; padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem; }
.upgrade-link:hover { background: #fde68a; color: #b45309; }
.pending-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.55rem; }
.pending-row span { border-radius: 999px; background: #ecfdf5; color: #047857; padding: 0.25rem 0.55rem; font-size: 0.76rem; font-weight: 900; }
.panel-head h2, .tools-head h2 { color: #0f172a; font-size: 1rem; font-weight: 950; }
.session-item svg { flex-shrink: 0; margin-top: 0.1rem; }
.source-item { background: #f8fafc; border-color: #edf2f7; box-shadow: 0 2px 10px rgba(15,23,42,0.02); }
.source-item svg, .tool-card svg { flex-shrink: 0; color: #2563eb; margin-top: 0.1rem; }
.tools-head { margin: 1.5rem 0 0.8rem; }
.tool-card { position: relative; width: 100%; background: #fff; border-color: #dbe3ef; box-shadow: 0 2px 10px rgba(15,23,42,0.03); }
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
:root[data-theme="dark"] .new-form textarea { background: #1e293b; border-color: rgba(255,255,255,0.1); color: #e5e7eb; }
:root[data-theme="dark"] .form-group label { color: #94a3b8; }
@media (max-width: 1180px) {
	.chat-page { grid-template-columns: 250px minmax(0, 1fr); }
	.session-rail { position: fixed; top: 0; left: 0; z-index: 40; width: min(300px, 85vw); transform: translateX(-100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); padding-bottom: 6rem; height: 100dvh; }
	.session-rail.open { transform: translateX(0); box-shadow: 20px 0 60px rgba(15,23,42,0.15); }
	.source-panel { position: fixed; top: 0; right: 0; z-index: 40; width: min(360px, 88vw); transform: translateX(100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: none; padding-bottom: 6rem; height: 100dvh; }
	.source-panel.open { transform: translateX(0); box-shadow: -20px 0 60px rgba(15,23,42,0.15); }
	.mobile-only { display: inline-flex; }
	.mobile-backdrop { display: block; position: fixed; inset: 0; z-index: 30; background: rgba(15,23,42,0.4); backdrop-filter: blur(2px); opacity: 0; pointer-events: none; transition: opacity 0.3s ease; }
	.session-rail.open ~ .mobile-backdrop, .source-panel.open ~ .mobile-backdrop { opacity: 1; pointer-events: auto; }
}
@media (max-width: 760px) {
	.chat-page { display: block; }
	.session-rail { position: fixed; top: 0; left: 0; z-index: 40; width: min(340px, 88vw); transform: translateX(-100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: none; padding-bottom: 6rem; height: 100dvh; }
	.session-rail.open { transform: translateX(0); box-shadow: 20px 0 60px rgba(15,23,42,0.15); }
	.chat-main { height: 100dvh; display: flex; flex-direction: column; }
	.chat-header { min-height: 60px; padding: 0.5rem; }
	.header-actions { gap: 0.4rem; }
	.model-switch button { padding: 0.42rem 0.55rem; }
	.model-switch span { display: none; }
	.new-chat { padding: 1.5rem 1rem 8rem 1rem; }
	.new-chat h1 { font-size: 2rem; }
	.new-form { padding: 1rem; }
	.new-form-row { grid-template-columns: 1fr; gap: 0.75rem; }
	.chat-thread { padding: 1rem 0.75rem; padding-bottom: 5rem; flex: 1; overflow-y: auto; }
	.message-row { gap: 0.5rem; margin: 1.25rem 0; }
	.avatar { width: 32px; height: 32px; border-radius: 10px; }
	.avatar svg { width: 16px; height: 16px; }
	.message-bubble { max-width: 92%; padding: 0.85rem 1rem; border-radius: 16px; font-size: 0.92rem; }
	.message-row.user .message-bubble { border-bottom-right-radius: 4px; }
	.message-row.assistant .message-bubble { border-bottom-left-radius: 4px; }
	
	.composer-wrap { position: fixed; bottom: 65px; left: 0; width: 100%; z-index: 20; padding: 0.6rem; background: rgba(247,248,251,0.92); backdrop-filter: blur(12px); border-top: 1px solid rgba(229,231,235,0.7); padding-bottom: calc(0.6rem + env(safe-area-inset-bottom)); }
	.composer { border-radius: 14px; padding: 0.4rem; box-shadow: 0 10px 25px rgba(15,23,42,0.05); }
	.composer textarea { font-size: 16px; padding: 0.45rem; }
	.composer-meta { justify-content: flex-start; font-size: 0.7rem; }
}
</style>

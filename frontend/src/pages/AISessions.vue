<template>
	<div class="chat-page" :class="{ 'right-collapsed': rightPanelCollapsed }" @paste="handlePaste">
		<FileUploader
			ref="fileUploader"
			class="hidden"
			:fileTypes="['.pdf', '.doc', '.docx', 'image/*', '.txt', '.md']"
			:uploadArgs="{ private: true }"
			:validateFile="validateFile"
			@success="handleFileUploaded"
		/>

		<!-- Skeleton Loader de Página -->
		<div v-if="isPageLoading" class="chat-skeleton-wrapper">
			<aside class="session-rail open">
				<div class="rail-head skeleton-head"></div>
				<div class="skeleton-btn"></div>
				<div class="skeleton-search"></div>
				<div class="session-list">
					<div v-for="i in 5" :key="i" class="skeleton-session-item">
						<div class="skeleton-icon"></div>
						<div class="skeleton-text-group">
							<div class="skeleton-line title"></div>
							<div class="skeleton-line subtitle"></div>
						</div>
					</div>
				</div>
			</aside>
			<main class="chat-main skeleton-main">
				<header class="chat-header">
					<div class="skeleton-header-title"></div>
					<div class="skeleton-header-actions"></div>
				</header>
				<section class="chat-thread">
					<div v-for="i in 3" :key="i" class="message-row-wrapper">
						<div class="message-row" :class="i % 2 === 0 ? 'user' : 'assistant'">
							<div class="avatar skeleton-avatar"></div>
							<div class="message-bubble skeleton-bubble" :style="{ width: i % 2 === 0 ? '40%' : '70%' }"></div>
						</div>
					</div>
				</section>
				<footer class="composer-wrap">
					<div class="composer skeleton-composer"></div>
				</footer>
			</main>
		</div>

		<template v-else>
			<aside class="session-rail" :class="{ open: showSessions }">
			<div class="rail-head">
				<div>
					<div class="rail-brand"><Sparkles class="size-4" /> {{ __('TutorIA Study') }}</div>
					<p>{{ access?.is_plus ? __('Plus: sesiones avanzadas') : accessText }}</p>
				</div>
				<button class="icon-btn mobile-only" @click="showSessions = false"><X class="size-4" /></button>
			</div>
			<button class="primary-btn full" :disabled="!canCreate" @click="startNewSession">
				<Plus class="size-4" /> {{ __('Nueva sesión') }}
			</button>
			<label class="search-box">
				<Search class="size-4" />
				<input v-model="sessionSearch" :placeholder="__('Buscar por curso, tema o examen…')" />
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
						<div class="session-badges mt-1" style="display: flex; gap: 0.25rem;">
							<span v-if="session.materials?.length || session.has_materials || session.status === 'Draft'" class="badge-mini doc-badge" style="font-size: 0.65rem; background: #e0f2fe; color: #0284c7; padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: bold;">{{ __('Con documentos') }}</span>
							<span v-if="session.status === 'Completed'" class="badge-mini status-badge" style="font-size: 0.65rem; background: #dcfce7; color: #166534; padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: bold;">{{ __('Listo') }}</span>
						</div>
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
					<button class="icon-btn hide-on-mobile" :class="{ 'active': rightPanelCollapsed }" @click="rightPanelCollapsed = !rightPanelCollapsed" :title="__('Alternar panel derecho')">
						<PanelRight class="size-5" />
					</button>
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
				<div v-for="(message, index) in chatMessages" :key="message.created_at || message.content" class="message-row-wrapper">
					<div class="message-row" :class="message.role === 'user' ? 'user' : 'assistant'">
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
					<div v-if="message.role !== 'user' && index === chatMessages.length - 1 && !chatLoading && !toolLoading" class="follow-up-actions">
						<button @click="sendFollowUp('Explícalo más simple')">{{ __('Explícalo fácil') }}</button>
						<button @click="sendFollowUp('Dame un ejemplo')">{{ __('Dame un ejemplo') }}</button>
						<button @click="sendFollowUp('Hazme practicar')">{{ __('Hazme practicar') }}</button>
						<button @click="sendFollowUp('Qué podría venir en examen?')">{{ __('Preguntas de examen') }}</button>
						<button @click="sendFollowUp('Hazme un resumen en 5 puntos')">{{ __('Resumen en 5 puntos') }}</button>
					</div>
				</div>
				<div v-if="chatLoading || toolLoading" class="message-row assistant">
					<div class="avatar"><Bot class="size-5" /></div>
					<div class="message-bubble typing"><span></span><span></span><span></span></div>
				</div>
			</section>

			<footer v-if="activeSession" class="composer-wrap" :class="{ 'panel-open': showSessions || showTools }">
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
					<div class="relative mode-dropdown-wrapper">
						<button class="icon-btn" :class="{ 'active-mode': showModesDropdown || chatMode !== 'chat' }" :title="__('Modos de IA')" @click="showModesDropdown = !showModesDropdown">
							<Plus class="size-5" />
						</button>
						<div v-if="showModesDropdown" class="modes-dropdown-menu">
							<div class="modes-header">{{ __('Modo de IA') }}</div>
							<button v-for="m in chatModesList" :key="m.value" class="mode-dropdown-item" :class="{ active: chatMode === m.value }" @click="chatMode = m.value; showModesDropdown = false">
								{{ m.label }}
							</button>
						</div>
					</div>
					<textarea
						ref="chatTextarea"
						v-model="chatInput"
						rows="1"
						:placeholder="__('Pregunta sobre tu lectura, pide ejemplos o escribe \'hazme practicar\'…')"
						@input="autoResizeTextarea"
						@keydown.enter.exact.prevent="sendChat"
						@keydown.shift.enter.stop
					/>
					<button class="send-btn" :disabled="chatLoading || (!chatInput.trim() && !pendingFiles.length)" @click="sendChat">
						<SendHorizontal class="size-5" />
					</button>
				</div>
			</footer>
		</main>

		<aside class="source-panel" :class="{ open: showTools }">
			<div class="panel-head">
				<div>
					<h2>{{ __('Panel de estudio') }}</h2>
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
				<h2>{{ __('Fuentes de estudio') }}</h2>
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
						<small>{{ material.file_type }} · {{ material.analysis_status === 'Completed' ? __('Listo') : (material.analysis_status === 'Error' ? __('Error al leer') : __('Analizando…')) }}</small>
					</span>
				</div>
				<div v-if="!activeSession?.materials?.length" class="soft-empty">
					<Upload class="size-5" />
					{{ activeSession ? __('Sube PDFs, trabajos, lecturas o imagenes.') : __('Crea una sesion para agregar fuentes.') }}
				</div>
			</div>

			<div class="tools-head">
				<h2>{{ __('Herramientas académicas') }}</h2>
				<p>{{ __('Responden dentro del chat') }}</p>
			</div>
			
			<div class="tool-group-title mt-2 mb-1" style="font-size:0.8rem; font-weight:800; color:#64748b; text-transform:uppercase;">{{ __('Estudiar') }}</div>
			<div class="tool-list mb-3">
				<button v-for="tool in tools.filter(t => t.group === 'study')" :key="tool.id" class="tool-card" :class="{ locked: tool.pro && !access?.is_plus }" :disabled="!activeSession || toolLoading" @click="runTool(tool)">
					<component :is="tool.icon" class="size-5" />
					<span>
						<strong>{{ tool.label }}</strong>
						<small>{{ tool.description }}</small>
					</span>
					<Crown v-if="tool.pro && !access?.is_plus" class="size-4 lock-icon" />
				</button>
			</div>

			<div class="tool-group-title mt-2 mb-1" style="font-size:0.8rem; font-weight:800; color:#64748b; text-transform:uppercase;">{{ __('Practicar') }}</div>
			<div class="tool-list mb-3">
				<button v-for="tool in tools.filter(t => t.group === 'practice')" :key="tool.id" class="tool-card" :class="{ locked: tool.pro && !access?.is_plus }" :disabled="!activeSession || toolLoading" @click="runTool(tool)">
					<component :is="tool.icon" class="size-5" />
					<span>
						<strong>{{ tool.label }}</strong>
						<small>{{ tool.description }}</small>
					</span>
					<Crown v-if="tool.pro && !access?.is_plus" class="size-4 lock-icon" />
				</button>
			</div>

			<div class="tool-group-title mt-2 mb-1" style="font-size:0.8rem; font-weight:800; color:#64748b; text-transform:uppercase;">{{ __('Crear') }}</div>
			<div class="tool-list mb-3">
				<button v-for="tool in tools.filter(t => t.group === 'create')" :key="tool.id" class="tool-card" :class="{ locked: tool.pro && !access?.is_plus }" :disabled="!activeSession || toolLoading" @click="runTool(tool)">
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
		</template>

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
const isPageLoading = ref(true)

const showAdvanced = ref(false)

const readerHistory = ref([])
const showSessions = ref(false)
const showTools = ref(false)
const rightPanelCollapsed = ref(false)
const sessionSearch = ref('')
const useSearch = ref(false)

const chatMode = ref('chat')
const showModesDropdown = ref(false)
const chatTextarea = ref(null)

function autoResizeTextarea() {
	const el = chatTextarea.value
	if (!el) return
	const lineHeight = 24
	const maxLines = 5
	const maxHeight = lineHeight * maxLines
	el.style.height = 'auto'
	const nextHeight = Math.min(el.scrollHeight, maxHeight)
	el.style.height = `${nextHeight}px`
	el.style.overflowY = el.scrollHeight > maxHeight ? 'auto' : 'hidden'
}

function resetTextareaHeight() {
	const el = chatTextarea.value
	if (!el) return
	el.style.height = '42px'
	el.style.overflowY = 'hidden'
}

const chatModesList = [
	{ label: __('Libre'), value: 'chat' },
	{ label: __('Simple'), value: 'simple' },
	{ label: __('Paso a paso'), value: 'step' },
	{ label: __('Examen'), value: 'exam' },
	{ label: __('Resumen'), value: 'summary' },
]

function sendFollowUp(text) {
	chatInput.value = text
	sendChat()
}

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
	{ id: 'summary', group: 'study', label: __('Resumen'), description: __('Ideas clave y prioridades'), icon: BookOpenCheck, prompt: __('Resume mis fuentes y dime que estudiar primero.') },
	{ id: 'key_ideas', group: 'study', label: __('Ideas clave'), description: __('Conceptos importantes'), icon: BookOpenCheck, prompt: __('Extrae las ideas clave de estas fuentes.') },
	{ id: 'flashcards', group: 'study', label: __('Flashcards'), description: __('Tarjetas de estudio'), icon: Layers, prompt: __('Crea flashcards para esta sesion.') },
	{ id: 'reader_question', group: 'study', label: __('Lectura guiada'), description: __('Pregunta corta por avance'), icon: MessageCircle, prompt: __('Hazme una pregunta corta de comprension sobre lo que estoy leyendo.') },
	
	{ id: 'quiz', group: 'practice', label: __('Cuestionario'), description: __('Preguntas con explicacion'), icon: FileQuestion, prompt: __('Crea un cuestionario con respuestas explicadas sobre mis fuentes.') },
	{ id: 'math', group: 'practice', label: __('Matemática paso a paso'), description: __('Resuelve y practica'), icon: Sigma, prompt: __('Ayudame con matematica: resuelve paso a paso y luego dame un ejercicio mas facil.') },
	{ id: 'mock_exam', group: 'practice', label: __('Simulacro'), description: __('Simulacro de examen'), icon: FileQuestion, prompt: __('Genera un simulacro de examen completo.') },
	
	{ id: 'infographic', group: 'create', label: __('Infografía'), description: __('Mapa visual de estudio'), icon: ImageIcon, pro: true, prompt: __('Genera una infografia academica sobre esta sesion.') },
	{ id: 'organize', group: 'create', label: __('Ordenar info'), description: __('Temas, tareas y pendientes'), icon: ListTree, prompt: __('Ordena esta sesion en temas, tareas y pendientes claros.') },
]

const starterPrompts = computed(() => {
	if (activeSession.value?.materials?.length > 0) {
		return [
			__('Hazme un resumen de estos documentos.'),
			__('¿Qué temas debería estudiar primero según las fuentes?'),
			__('Crea un quiz basado en este material.'),
			__('Explícame los conceptos más difíciles con ejemplos simples.'),
		]
	}
	return [
		__('Hazme un resumen de un tema.'),
		__('Crea preguntas para practicar.'),
		__('Explícame lo más difícil con ejemplos simples.'),
	]
})

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
	return `${count} de ${max} archivos`
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
	isPageLoading.value = true
	try {
		access.value = await api('get_ai_session_access')
		sessions.value = await api('list_ai_sessions')
		await loadRouteSession()
	} finally {
		isPageLoading.value = false
	}
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
	
	const files = pendingFiles.value.map((file) => file.file_url)
	const optimistic = { role: 'user', content: text || __('Analiza las fuentes adjuntas.'), created_at: String(Date.now()) }
	const assistantOptimistic = { role: 'assistant', content: '', created_at: String(Date.now() + 1), model_label: modelLabel(activeSession.value.model_tier), is_streaming: true }
	chatMessages.value = [...chatMessages.value, optimistic]
	chatInput.value = ''
	pendingFiles.value = []
	await nextTick()
	resetTextareaHeight()
	scrollChat()

	const streamEvent = `ai_stream_${activeSession.value.name}`
	let streamingContent = ''
	let isStreamingStarted = false
	const streamHandler = (data) => {
		if (data && data.chunk) {
			if (!isStreamingStarted) {
				isStreamingStarted = true
				chatLoading.value = false
				chatMessages.value = [...chatMessages.value, assistantOptimistic]
			}
			streamingContent += data.chunk
			const lastMsg = chatMessages.value[chatMessages.value.length - 1]
			if (lastMsg && lastMsg.is_streaming) {
				lastMsg.content = streamingContent
				scrollChat()
			}
		}
	}
	
	if (window.frappe && window.frappe.realtime) {
		window.frappe.realtime.on(streamEvent, streamHandler)
	}

	try {
		let result
		try {
			result = await api('chat_ai_session', {
				session: activeSession.value.name,
				thread: currentThread.value?.name,
				message: text || __('Analiza las fuentes adjuntas.'),
				files,
				model_tier: activeSession.value.model_tier,
				use_search: useSearch.value ? 1 : 0,
				mode: chatMode.value,
			})
		} finally {
			if (window.frappe && window.frappe.realtime) {
				window.frappe.realtime.off(streamEvent, streamHandler)
			}
		}
		
		if (result.thread) {
			const isNewThread = !currentThread.value
			currentThread.value = result.thread
			
			let messages = result.thread?.messages || []
			if (messages.length > 0) {
				const lastMsg = messages[messages.length - 1]
				if (lastMsg.role === 'assistant' || lastMsg.role === 'model') {
					const contentStr = (lastMsg.content || '').trim()
					if (contentStr.startsWith('{') || contentStr.startsWith('[')) {
						lastMsg.content = __('Listo. Preparé la acción solicitada.')
					}
				}
			}
			chatMessages.value = messages

			if (isNewThread) {
				activeSession.value.threads = [result.thread, ...(activeSession.value.threads || [])]
			}
		} else {
			// Backend didn't return a thread (meaning a tool was triggered immediately)
			chatMessages.value = chatMessages.value.map(msg => {
				if (msg === assistantOptimistic) {
					return { role: 'assistant', content: __('Listo. Preparé la acción solicitada.'), created_at: msg.created_at }
				}
				return msg
			})
		}
		access.value = result.access || access.value
		await nextTick(scrollChat)

		const actionTool = (result.action && result.action.type === 'open_tool') ? result.action.tool : result.trigger_modal;

		if (actionTool) {
			if (actionTool === 'quiz') showQuiz.value = true
			if (actionTool === 'flashcards') showFlashcards.value = true
			if (actionTool === 'guided_reading' || actionTool === 'reader_question') showGuidedReading.value = true
			if (actionTool === 'math') showMath.value = true
			
			modalLoading.value = true
			modalData.value = null
			
			try {
				const toolResult = await api('generate_ai_tool', {
					session: activeSession.value.name,
					thread: currentThread.value?.name,
					tool: actionTool,
					payload: { prompt: text || '' },
				})
				modalData.value = toolResult.result
				access.value = toolResult.access || access.value
			} catch (e) {
				toast.error(__('No se pudo generar el contenido. Intenta de nuevo.'))
			} finally {
				modalLoading.value = false
			}
		}
	} catch (e) {
		chatMessages.value = chatMessages.value.filter(m => m !== optimistic && m !== assistantOptimistic)
		toast.error(__('No pude responder en este momento. Intenta de nuevo en unos segundos.'))
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
/* ═══════════════════════════════════════════════
   STUDYBADGE AI SESSIONS — PREMIUM CHAT UI
   Color principal: #0A2251
   Solo diseño. Mantiene la lógica original.
   ═══════════════════════════════════════════════ */

.chat-page {
	--sb-primary: #0a2251;
	--sb-primary-2: #12356e;
	--sb-gold: #f5b301;
	--sb-bg: #f5f8fc;
	--sb-bg-soft: #eef4fb;
	--sb-card: rgba(255, 255, 255, 0.88);
	--sb-card-solid: #ffffff;
	--sb-border: rgba(148, 163, 184, 0.22);
	--sb-border-strong: rgba(10, 34, 81, 0.16);
	--sb-text: #0f172a;
	--sb-muted: #64748b;
	--sb-soft-text: #94a3b8;
	--sb-shadow: 0 18px 46px rgba(15, 23, 42, 0.07);
	--sb-shadow-strong: 0 28px 80px rgba(10, 34, 81, 0.14);

	display: grid;
	grid-template-columns: 292px minmax(0, 1fr) 350px;
	height: 100dvh;
	overflow: hidden;
	background:
		radial-gradient(circle at top left, rgba(10, 34, 81, 0.08), transparent 31rem),
		radial-gradient(circle at bottom right, rgba(245, 179, 1, 0.11), transparent 26rem),
		linear-gradient(180deg, #f5f8fc 0%, #eef4fb 42%, #f8fafc 100%);
	color: var(--sb-text);
}

/* ═══════════════════════════════════════════════
   SIDE PANELS
   ═══════════════════════════════════════════════ */

.session-rail,
.source-panel {
	position: relative;
	z-index: 10;
	height: 100dvh;
	overflow-y: auto;
	border-color: var(--sb-border);
	border-style: solid;
	background: rgba(255, 255, 255, 0.82);
	padding: 1rem;
	backdrop-filter: blur(18px);
	scrollbar-width: thin;
	scrollbar-color: rgba(10, 34, 81, 0.22) transparent;
}

.session-rail::-webkit-scrollbar,
.source-panel::-webkit-scrollbar,
.chat-thread::-webkit-scrollbar {
	width: 8px;
}

.session-rail::-webkit-scrollbar-thumb,
.source-panel::-webkit-scrollbar-thumb,
.chat-thread::-webkit-scrollbar-thumb {
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.18);
}

.session-rail {
	border-width: 0 1px 0 0;
	box-shadow: 12px 0 40px rgba(15, 23, 42, 0.035);
}

.source-panel {
	border-width: 0 0 0 1px;
	padding: 1.05rem;
	box-shadow: -12px 0 40px rgba(15, 23, 42, 0.035);
}

.rail-head,
.panel-head,
.chat-header,
.header-left,
.header-actions,
.new-actions {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.75rem;
}

.rail-head,
.panel-head {
	margin-bottom: 0.9rem;
}

.rail-brand {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	width: fit-content;
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.08);
	padding: 0.42rem 0.7rem;
	color: var(--sb-primary);
	font-size: 0.76rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.rail-head p,
.panel-head p,
.tools-head p,
.session-title small,
.source-item small,
.session-item small,
.composer-meta,
.new-chat p,
.welcome-block p {
	margin: 0.4rem 0 0;
	color: var(--sb-muted);
	font-size: 0.78rem;
	line-height: 1.5;
}

.panel-head h2,
.tools-head h2 {
	margin: 0;
	color: var(--sb-primary);
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.tools-head {
	margin-top: 1.35rem;
	margin-bottom: 0.75rem;
	padding-top: 1.15rem;
	border-top: 1px solid rgba(226, 232, 240, 0.82);
}

.tools-head.mt-0 {
	padding-top: 0;
	border-top: 0;
}

/* ═══════════════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════════════ */

.primary-btn,
.secondary-btn,
.icon-btn,
.send-btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	border: 0;
	border-radius: 999px;
	font-weight: 900;
	text-decoration: none;
	cursor: pointer;
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease,
		color 0.18s ease,
		opacity 0.18s ease;
}

.primary-btn {
	min-height: 42px;
	border: 1px solid rgba(10, 34, 81, 0.95);
	background: linear-gradient(135deg, var(--sb-primary), var(--sb-primary-2));
	color: #ffffff;
	padding: 0.7rem 1rem;
	box-shadow: 0 14px 28px rgba(10, 34, 81, 0.18);
}

.primary-btn:hover:not(:disabled) {
	transform: translateY(-1px);
	box-shadow: 0 18px 34px rgba(10, 34, 81, 0.24);
}

.secondary-btn {
	min-height: 42px;
	border: 1px solid rgba(10, 34, 81, 0.13);
	background: rgba(255, 255, 255, 0.88);
	color: var(--sb-primary);
	padding: 0.7rem 1rem;
	box-shadow: 0 10px 22px rgba(15, 23, 42, 0.04);
}

.secondary-btn:hover:not(:disabled) {
	transform: translateY(-1px);
	border-color: rgba(10, 34, 81, 0.22);
	background: #ffffff;
	box-shadow: 0 16px 32px rgba(15, 23, 42, 0.08);
}

.primary-btn:disabled,
.secondary-btn:disabled,
.send-btn:disabled,
.tool-card:disabled {
	cursor: not-allowed;
	opacity: 0.55;
	transform: none;
	box-shadow: none;
}

.full {
	width: 100%;
	margin-top: 0.85rem;
}

.icon-btn {
	width: 40px;
	height: 40px;
	flex: 0 0 auto;
	border: 1px solid rgba(10, 34, 81, 0.12);
	background: rgba(255, 255, 255, 0.9);
	color: #334155;
	box-shadow: 0 10px 22px rgba(15, 23, 42, 0.04);
}

.icon-btn:hover {
	transform: translateY(-1px);
	border-color: rgba(10, 34, 81, 0.22);
	color: var(--sb-primary);
	box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
}

.icon-btn.active-search,
.icon-btn.active-mode,
.icon-btn.active {
	border-color: rgba(10, 34, 81, 0.2);
	background: rgba(10, 34, 81, 0.08);
	color: var(--sb-primary);
}

.send-btn {
	width: 46px;
	height: 46px;
	flex: 0 0 auto;
	background: var(--sb-primary);
	color: #ffffff;
	box-shadow: 0 16px 34px rgba(10, 34, 81, 0.25);
}

.send-btn:hover:not(:disabled) {
	transform: translateY(-1px) scale(1.02);
	background: var(--sb-primary-2);
}

/* ═══════════════════════════════════════════════
   SEARCH / LISTS
   ═══════════════════════════════════════════════ */

.search-box {
	display: flex;
	align-items: center;
	gap: 0.55rem;
	margin: 0.9rem 0;
	border: 1px solid rgba(10, 34, 81, 0.12);
	border-radius: 18px;
	background: rgba(248, 250, 252, 0.92);
	padding: 0.68rem 0.8rem;
	color: var(--sb-muted);
	transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}

.search-box:focus-within {
	border-color: rgba(10, 34, 81, 0.32);
	background: #ffffff;
	box-shadow: 0 0 0 4px rgba(10, 34, 81, 0.08);
}

.search-box input {
	min-width: 0;
	flex: 1;
	border: 0;
	outline: 0;
	background: transparent;
	color: var(--sb-text);
	font-size: 0.88rem;
}

.search-box input::placeholder {
	color: #94a3b8;
}

.session-list,
.sources-list,
.tool-list {
	display: flex;
	flex-direction: column;
	gap: 0.62rem;
}

.scrollable-list {
	margin-top: 0.5rem;
	margin-bottom: 1rem;
	max-height: 250px;
	overflow-y: auto;
	padding-right: 0.25rem;
	scrollbar-width: thin;
}

.session-item,
.source-item,
.tool-card {
	position: relative;
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	width: 100%;
	border: 1px solid transparent;
	border-radius: 18px;
	padding: 0.85rem;
	text-align: left;
	transition:
		transform 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease,
		box-shadow 0.18s ease,
		color 0.18s ease;
}

.session-item {
	background: transparent;
	color: #334155;
	cursor: pointer;
}

.session-item svg {
	flex: 0 0 auto;
	margin-top: 0.15rem;
	color: var(--sb-muted);
	transition: color 0.18s ease;
}

.session-item:hover {
	transform: translateY(-1px);
	background: rgba(10, 34, 81, 0.055);
	border-color: rgba(10, 34, 81, 0.11);
	box-shadow: 0 10px 24px rgba(15, 23, 42, 0.045);
}

.session-item.active {
	background: linear-gradient(135deg, rgba(10, 34, 81, 0.1), rgba(10, 34, 81, 0.045));
	border-color: rgba(10, 34, 81, 0.18);
	color: var(--sb-primary);
	box-shadow: 0 14px 30px rgba(10, 34, 81, 0.08);
}

.session-item.active::before {
	content: '';
	position: absolute;
	top: 0.75rem;
	bottom: 0.75rem;
	left: 0;
	width: 4px;
	border-radius: 999px;
	background: var(--sb-primary);
}

.session-item:hover svg,
.session-item.active svg {
	color: var(--sb-primary);
}

.session-item span,
.source-item span,
.tool-card span {
	min-width: 0;
	display: flex;
	flex-direction: column;
	gap: 0.15rem;
}

.session-item strong,
.source-item strong,
.tool-card strong {
	overflow: hidden;
	color: var(--sb-text);
	font-size: 0.88rem;
	font-weight: 950;
	line-height: 1.25;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.source-item {
	border-color: rgba(226, 232, 240, 0.9);
	background: rgba(248, 250, 252, 0.92);
}

.source-item svg {
	flex: 0 0 auto;
	margin-top: 0.12rem;
	color: var(--sb-primary);
}

.tool-card {
	border-color: rgba(226, 232, 240, 0.92);
	background: rgba(255, 255, 255, 0.9);
	cursor: pointer;
}

.tool-card::after {
	content: '';
	position: absolute;
	inset: auto 0.85rem 0.65rem 0.85rem;
	height: 3px;
	border-radius: 999px;
	background: linear-gradient(90deg, var(--sb-primary), var(--sb-gold));
	opacity: 0;
	transform: scaleX(0.55);
	transform-origin: left;
	transition: 0.18s ease;
}

.tool-card:hover:not(:disabled) {
	transform: translateY(-2px);
	border-color: rgba(10, 34, 81, 0.16);
	background: #ffffff;
	box-shadow: 0 16px 34px rgba(10, 34, 81, 0.09);
}

.tool-card:hover:not(:disabled)::after {
	opacity: 1;
	transform: scaleX(1);
}

.tool-card svg {
	flex: 0 0 auto;
	margin-top: 0.12rem;
	color: var(--sb-primary);
}

.tool-card strong {
	font-size: 0.87rem;
}

.tool-card small {
	color: var(--sb-muted);
	font-size: 0.74rem;
	line-height: 1.35;
}

.tool-card.locked {
	background: rgba(245, 179, 1, 0.09);
	border-color: rgba(245, 179, 1, 0.2);
}

.lock-icon {
	margin-left: auto;
	color: #b77900 !important;
}

/* ═══════════════════════════════════════════════
   MAIN CHAT AREA
   ═══════════════════════════════════════════════ */

.chat-main {
	display: flex;
	flex-direction: column;
	min-width: 0;
	width: 100%;
	max-width: 100%;
	height: 100dvh;
	overflow: hidden;
}

.chat-header {
	position: sticky;
	top: 0;
	z-index: 5;
	min-height: 72px;
	border-bottom: 1px solid rgba(226, 232, 240, 0.78);
	background: rgba(255, 255, 255, 0.78);
	padding: 0.78rem 1rem;
	backdrop-filter: blur(18px);
}

.header-left {
	flex: 1;
	min-width: 0;
	justify-content: flex-start;
}

.header-actions {
	flex-shrink: 0;
}

.session-title {
	display: flex;
	min-width: 0;
	flex-direction: column;
}

.session-title span {
	overflow: hidden;
	color: var(--sb-text);
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.025em;
	line-height: 1.25;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.model-switch {
	display: inline-flex;
	gap: 0.35rem;
	border: 1px solid rgba(10, 34, 81, 0.12);
	border-radius: 999px;
	background: rgba(248, 250, 252, 0.9);
	padding: 0.25rem;
	box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
}

.model-switch button {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	border: 0;
	border-radius: 999px;
	background: transparent;
	color: var(--sb-muted);
	padding: 0.48rem 0.72rem;
	font-size: 0.78rem;
	font-weight: 950;
	white-space: nowrap;
	cursor: pointer;
	transition: 0.18s ease;
}

.model-switch button:hover {
	color: var(--sb-primary);
}

.model-switch button.active {
	background: var(--sb-primary);
	color: #ffffff;
	box-shadow: 0 10px 22px rgba(10, 34, 81, 0.18);
}

.model-switch button.locked {
	color: #9a6a00;
}

/* ═══════════════════════════════════════════════
   NEW CHAT SCREEN
   ═══════════════════════════════════════════════ */

.new-chat,
.chat-thread {
	min-height: 0;
	overflow-y: auto;
	overflow-x: hidden;
}

.new-chat {
	display: grid;
	place-items: center;
	padding: 2rem;
}

.new-chat-inner {
	position: relative;
	width: min(760px, 100%);
	text-align: center;
}

.new-chat-inner::before {
	content: '';
	position: absolute;
	top: -4rem;
	left: 50%;
	width: min(520px, 85vw);
	height: min(520px, 85vw);
	border-radius: 999px;
	background: radial-gradient(circle, rgba(10, 34, 81, 0.1), transparent 68%);
	transform: translateX(-50%);
	pointer-events: none;
	z-index: -1;
}

.new-badge {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	margin-bottom: 0.65rem;
	border: 1px solid rgba(10, 34, 81, 0.12);
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.07);
	padding: 0.45rem 0.85rem;
	color: var(--sb-primary);
	font-size: 0.82rem;
	font-weight: 950;
	letter-spacing: 0.03em;
}

.new-chat h1 {
	margin: 0.75rem 0 0;
	color: var(--sb-primary);
	font-size: clamp(2.2rem, 6vw, 4.6rem);
	font-weight: 950;
	letter-spacing: -0.065em;
	line-height: 0.98;
	text-wrap: balance;
}

.new-chat p {
	margin: 1rem auto 0;
	max-width: 640px;
	font-size: 1rem;
	line-height: 1.75;
}

.new-form {
	position: relative;
	margin-top: 2rem;
	overflow: hidden;
	border: 1px solid rgba(10, 34, 81, 0.12);
	border-radius: 28px;
	background: rgba(255, 255, 255, 0.9);
	padding: 1.35rem;
	text-align: left;
	box-shadow: var(--sb-shadow-strong);
	backdrop-filter: blur(18px);
}

.new-form::before {
	content: '';
	position: absolute;
	inset: 0;
	background:
		radial-gradient(circle at top right, rgba(245, 179, 1, 0.14), transparent 14rem),
		radial-gradient(circle at bottom left, rgba(10, 34, 81, 0.07), transparent 13rem);
	pointer-events: none;
}

.new-form > * {
	position: relative;
	z-index: 1;
}

.form-group {
	display: flex;
	flex-direction: column;
	gap: 0.42rem;
}

.form-group label {
	color: #334155;
	font-size: 0.82rem;
	font-weight: 950;
}

.new-form input,
.new-form select,
.new-form textarea {
	width: 100%;
	border: 1px solid rgba(203, 213, 225, 0.92);
	border-radius: 18px;
	background: rgba(248, 250, 252, 0.92);
	color: var(--sb-text);
	outline: 0;
	padding: 0.82rem 0.95rem;
	font-size: 0.95rem;
	transition:
		border-color 0.18s ease,
		background 0.18s ease,
		box-shadow 0.18s ease;
}

.new-form input:focus,
.new-form select:focus,
.new-form textarea:focus {
	border-color: rgba(10, 34, 81, 0.42);
	background: #ffffff;
	box-shadow: 0 0 0 4px rgba(10, 34, 81, 0.09);
}

.title-input {
	border-radius: 20px !important;
	padding: 1rem !important;
	font-size: 1.08rem !important;
	font-weight: 850;
}

.new-form textarea {
	resize: vertical;
	line-height: 1.55;
}

.new-form-row {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 1rem;
	margin-top: 0.5rem;
}

.toggle-advanced-btn {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	margin-top: 0.85rem;
	border: 0;
	background: transparent;
	color: var(--sb-muted);
	padding: 0.5rem 0;
	font-size: 0.85rem;
	font-weight: 900;
	cursor: pointer;
	transition: color 0.18s ease;
}

.toggle-advanced-btn:hover {
	color: var(--sb-primary);
}

.advanced-options {
	margin-top: 0.65rem;
	padding-top: 1rem;
	border-top: 1px dashed rgba(148, 163, 184, 0.42);
	animation: fadeInDown 0.25s ease;
}

.mt-3 {
	margin-top: 0.75rem;
}

.mt-0 {
	margin-top: 0 !important;
}

.mt-1 {
	margin-top: 0.25rem !important;
}

@keyframes fadeInDown {
	from {
		opacity: 0;
		transform: translateY(-5px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

.new-actions {
	margin-top: 1rem;
}

/* ═══════════════════════════════════════════════
   CHAT THREAD
   ═══════════════════════════════════════════════ */

.chat-thread {
	flex: 1;
	min-width: 0;
	width: 100%;
	max-width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: clamp(44px, 7vh, 76px) 24px 32px;
}

.welcome-block {
	display: grid;
	width: min(820px, 100%);
	min-height: 56vh;
	place-items: center;
	align-content: center;
	text-align: center;
}

.welcome-block h2 {
	margin: 0.75rem auto 0;
	max-width: 760px;
	color: var(--sb-primary);
	font-size: clamp(1.35rem, 3.5vw, 2.1rem);
	font-weight: 950;
	letter-spacing: -0.045em;
	line-height: 1.16;
	text-wrap: balance;
}

.suggestions {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
	gap: 0.85rem;
	width: 100%;
	max-width: 760px;
	margin-top: 1.8rem;
}

.suggestions button {
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 54px;
	border: 1px solid rgba(10, 34, 81, 0.12);
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.9);
	color: #334155;
	padding: 0.85rem 1rem;
	font-size: 0.9rem;
	font-weight: 850;
	text-align: center;
	cursor: pointer;
	box-shadow: 0 12px 28px rgba(15, 23, 42, 0.045);
	transition: 0.18s ease;
}

.suggestions button:hover {
	transform: translateY(-2px);
	border-color: rgba(10, 34, 81, 0.22);
	background: #ffffff;
	color: var(--sb-primary);
	box-shadow: 0 18px 34px rgba(10, 34, 81, 0.1);
}

/* ═══════════════════════════════════════════════
   MESSAGES
   ═══════════════════════════════════════════════ */

.message-row-wrapper {
	display: flex;
	flex-direction: column;
	gap: 8px;
	width: 100%;
	max-width: 1040px;
}

.message-row {
	display: flex;
	width: 100%;
	min-width: 0;
	gap: 10px;
	margin: 1.05rem 0;
	opacity: 0;
	transform: translateY(14px);
	animation: messageSlideIn 0.34s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.message-row.user {
	flex-direction: row-reverse;
	justify-content: flex-start;
}

.message-row.assistant {
	justify-content: flex-start;
}

.avatar {
	display: grid;
	width: 40px;
	height: 40px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 16px;
	transition: 0.18s ease;
}

.message-row.user .avatar {
	background: rgba(10, 34, 81, 0.08);
	color: var(--sb-primary);
}

.message-row.assistant .avatar {
	border: 1px solid rgba(10, 34, 81, 0.12);
	background: #ffffff;
	color: var(--sb-primary);
	box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}

.message-bubble {
	box-sizing: border-box;
	min-width: 0;
	max-width: min(820px, calc(100% - 56px));
	border-radius: 24px;
	padding: 1rem 1.15rem;
	color: #1f2937;
	font-size: 0.95rem;
	line-height: 1.75;
	overflow-wrap: anywhere;
	word-break: break-word;
}

.message-bubble > div {
	min-width: 0;
	max-width: 100%;
	overflow-wrap: anywhere;
	word-break: break-word;
}

.message-row.user .message-bubble {
	border-bottom-right-radius: 8px;
	background: linear-gradient(135deg, var(--sb-primary), var(--sb-primary-2));
	color: #ffffff;
	box-shadow: 0 16px 34px rgba(10, 34, 81, 0.18);
}

.message-row.assistant .message-bubble {
	border: 1px solid rgba(226, 232, 240, 0.9);
	border-bottom-left-radius: 8px;
	background: rgba(255, 255, 255, 0.94);
	box-shadow: 0 14px 34px rgba(15, 23, 42, 0.055);
}

@keyframes messageSlideIn {
	0% {
		opacity: 0;
		transform: translateY(14px) scale(0.985);
	}
	100% {
		opacity: 1;
		transform: translateY(0) scale(1);
	}
}

.message-model {
	display: inline-flex;
	align-items: center;
	width: fit-content;
	margin-bottom: 0.55rem;
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.07);
	padding: 0.25rem 0.55rem;
	color: var(--sb-primary);
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.message-row.user .message-model {
	background: rgba(255, 255, 255, 0.16);
	color: rgba(255, 255, 255, 0.86);
}

.message-bubble :deep(p) {
	margin: 0 0 0.85rem;
}

.message-bubble :deep(p:last-child) {
	margin-bottom: 0;
}

.message-bubble :deep(ul),
.message-bubble :deep(ol) {
	margin: 0.75rem 0 0.9rem 1.2rem;
	padding: 0;
}

.message-bubble :deep(li) {
	margin: 0.35rem 0;
}

.message-bubble :deep(li > p) {
	margin: 0;
}

.message-bubble :deep(h1),
.message-bubble :deep(h2),
.message-bubble :deep(h3),
.message-bubble :deep(h4) {
	margin: 1rem 0 0.55rem;
	color: var(--sb-primary);
	font-weight: 950;
	letter-spacing: -0.035em;
	line-height: 1.2;
}

.message-row.user .message-bubble :deep(h1),
.message-row.user .message-bubble :deep(h2),
.message-row.user .message-bubble :deep(h3),
.message-row.user .message-bubble :deep(h4) {
	color: #ffffff;
}

.message-bubble :deep(h1) {
	font-size: 1.45rem;
}

.message-bubble :deep(h2) {
	font-size: 1.25rem;
}

.message-bubble :deep(h3) {
	font-size: 1.08rem;
}

.message-bubble :deep(h4) {
	font-size: 0.98rem;
}

.message-bubble :deep(strong) {
	font-weight: 950;
}

.message-bubble :deep(hr) {
	margin: 1rem 0;
	border: 0;
	border-top: 1px solid rgba(226, 232, 240, 0.9);
}

.message-bubble :deep(blockquote) {
	margin: 0.85rem 0;
	border-left: 4px solid rgba(10, 34, 81, 0.2);
	border-radius: 0 14px 14px 0;
	background: rgba(10, 34, 81, 0.045);
	padding: 0.7rem 0.85rem;
	color: #475569;
}

.message-bubble pre,
.message-bubble code,
.message-bubble :deep(pre),
.message-bubble :deep(code) {
	max-width: 100%;
	overflow-x: auto;
	white-space: pre-wrap;
}

.message-bubble :deep(code) {
	border-radius: 8px;
	background: rgba(10, 34, 81, 0.07);
	padding: 0.14rem 0.35rem;
	color: var(--sb-primary);
	font-size: 0.9em;
}

.message-row.user .message-bubble :deep(code) {
	background: rgba(255, 255, 255, 0.14);
	color: #ffffff;
}

.message-bubble :deep(pre) {
	border-radius: 18px;
	background: #08172c;
	padding: 1rem;
	color: #e5edf8;
}

.message-bubble table,
.message-bubble :deep(table) {
	display: block;
	max-width: 100%;
	overflow-x: auto;
	border-collapse: collapse;
}

.message-bubble :deep(th),
.message-bubble :deep(td) {
	border: 1px solid rgba(226, 232, 240, 0.9);
	padding: 0.55rem 0.7rem;
}

.message-bubble img,
.chat-image {
	display: block;
	max-width: 100%;
	height: auto;
	margin-top: 0.8rem;
	border-radius: 18px;
	box-shadow: 0 14px 30px rgba(15, 23, 42, 0.1);
}

.message-bubble :deep(.katex-display),
.katex-display {
	max-width: 100%;
	overflow-x: auto;
	overflow-y: hidden;
	margin: 0.75rem 0;
	padding: 0.2rem 0;
}

.typing {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	min-width: 78px;
}

.typing span {
	width: 8px;
	height: 8px;
	border-radius: 999px;
	background: var(--sb-primary);
	opacity: 0.25;
	animation: typingPulse 1s infinite ease-in-out;
}

.typing span:nth-child(2) {
	animation-delay: 0.16s;
}

.typing span:nth-child(3) {
	animation-delay: 0.32s;
}

@keyframes typingPulse {
	0%,
	80%,
	100% {
		opacity: 0.25;
		transform: translateY(0);
	}
	40% {
		opacity: 0.95;
		transform: translateY(-4px);
	}
}

.follow-up-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
	max-width: 100%;
	margin: 0.1rem 0 0.8rem 50px;
	overflow: hidden;
}

.follow-up-actions button {
	max-width: 100%;
	border: 1px solid rgba(10, 34, 81, 0.11);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.9);
	color: var(--sb-muted);
	padding: 0.45rem 0.75rem;
	font-size: 0.76rem;
	font-weight: 850;
	white-space: normal;
	overflow-wrap: anywhere;
	cursor: pointer;
	transition: 0.18s ease;
	box-shadow: 0 8px 18px rgba(15, 23, 42, 0.035);
}

.follow-up-actions button:hover {
	transform: translateY(-1px);
	border-color: rgba(10, 34, 81, 0.2);
	background: #ffffff;
	color: var(--sb-primary);
}

/* ═══════════════════════════════════════════════
   COMPOSER
   ═══════════════════════════════════════════════ */

.composer-wrap {
	position: sticky;
	bottom: 0;
	z-index: 6;
	width: 100%;
	padding: 0.8rem 1rem 1rem;
	background:
		linear-gradient(180deg, rgba(245, 248, 252, 0), rgba(245, 248, 252, 0.92) 28%, rgba(245, 248, 252, 0.98));
	backdrop-filter: blur(14px);
}

.composer {
	display: flex;
	align-items: flex-end;
	gap: 0.55rem;
	width: min(980px, 100%);
	margin: 0 auto;
	border: 1px solid rgba(10, 34, 81, 0.13);
	border-radius: 26px;
	background: rgba(255, 255, 255, 0.94);
	padding: 0.55rem;
	box-shadow: 0 20px 54px rgba(10, 34, 81, 0.12);
}

.composer textarea {
	min-height: 44px;
	max-height: 150px;
	flex: 1;
	resize: none;
	border: 0;
	outline: 0;
	background: transparent;
	color: var(--sb-text);
	padding: 0.62rem 0.45rem;
	font-size: 0.95rem;
	line-height: 1.55;
	scrollbar-width: thin;
}

.composer textarea::placeholder {
	color: #94a3b8;
}

.composer textarea::-webkit-scrollbar {
	width: 6px;
}

.composer textarea::-webkit-scrollbar-thumb {
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.2);
}

.composer-meta {
	margin: 0.35rem auto 0;
	width: min(980px, 100%);
	text-align: center;
}

.pending-row {
	display: flex;
	flex-wrap: wrap;
	gap: 0.45rem;
	width: min(980px, 100%);
	margin: 0 auto 0.55rem;
}

.pending-row span {
	display: inline-flex;
	align-items: center;
	max-width: 100%;
	border: 1px solid rgba(10, 34, 81, 0.12);
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.06);
	padding: 0.35rem 0.65rem;
	color: var(--sb-primary);
	font-size: 0.75rem;
	font-weight: 850;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

/* ═══════════════════════════════════════════════
   DROPDOWN
   ═══════════════════════════════════════════════ */

.mode-dropdown-wrapper {
	position: relative;
}

.modes-dropdown-menu {
	position: absolute;
	bottom: calc(100% + 10px);
	left: 0;
	z-index: 60;
	width: 210px;
	max-width: calc(100vw - 24px);
	border: 1px solid rgba(10, 34, 81, 0.13);
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.98);
	padding: 0.42rem;
	box-shadow: 0 24px 56px rgba(15, 23, 42, 0.16);
	backdrop-filter: blur(18px);
}

.modes-header {
	padding: 0.55rem 0.75rem 0.4rem;
	color: var(--sb-muted);
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.mode-dropdown-item,
.modes-dropdown-menu button {
	width: 100%;
	border: 0;
	border-radius: 13px;
	background: transparent;
	padding: 0.7rem 0.75rem;
	color: var(--sb-text);
	font-size: 0.84rem;
	font-weight: 850;
	text-align: left;
	cursor: pointer;
	transition: 0.18s ease;
}

.mode-dropdown-item:hover,
.mode-dropdown-item.active,
.modes-dropdown-menu button:hover,
.modes-dropdown-menu button.active {
	background: rgba(10, 34, 81, 0.07);
	color: var(--sb-primary);
}

/* ═══════════════════════════════════════════════
   EMPTY STATES
   ═══════════════════════════════════════════════ */

.soft-empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	min-height: 110px;
	border: 1px dashed rgba(148, 163, 184, 0.45);
	border-radius: 20px;
	background: rgba(248, 250, 252, 0.78);
	padding: 1rem;
	color: var(--sb-muted);
	font-size: 0.84rem;
	font-weight: 750;
	line-height: 1.45;
	text-align: center;
}

.soft-empty svg {
	color: var(--sb-primary);
	opacity: 0.78;
}

.mobile-only {
	display: none;
}

.mobile-backdrop {
	display: none;
}

.hidden {
	display: none;
}

/* ═══════════════════════════════════════════════
   RIGHT PANEL COLLAPSED
   ═══════════════════════════════════════════════ */

@media (min-width: 1181px) {
	.chat-page.right-collapsed {
		grid-template-columns: 292px minmax(0, 1fr);
	}

	.chat-page.right-collapsed .source-panel {
		display: none;
	}
}

/* ═══════════════════════════════════════════════
   DARK MODE
   ═══════════════════════════════════════════════ */

:global(:root[data-theme='dark']) .chat-page,
:global(.dark) .chat-page {
	--sb-bg: #07111f;
	--sb-bg-soft: #0b1728;
	--sb-card: rgba(15, 23, 42, 0.72);
	--sb-card-solid: #0f172a;
	--sb-border: rgba(148, 163, 184, 0.16);
	--sb-border-strong: rgba(245, 179, 1, 0.18);
	--sb-text: #f8fafc;
	--sb-muted: #94a3b8;
	--sb-soft-text: #64748b;

	background:
		radial-gradient(circle at top left, rgba(245, 179, 1, 0.08), transparent 30rem),
		radial-gradient(circle at bottom right, rgba(10, 34, 81, 0.55), transparent 30rem),
		linear-gradient(180deg, #07111f 0%, #081827 48%, #07111f 100%);
	color: #e5edf8;
}

:global(:root[data-theme='dark']) .session-rail,
:global(:root[data-theme='dark']) .source-panel,
:global(.dark) .session-rail,
:global(.dark) .source-panel {
	border-color: rgba(148, 163, 184, 0.16);
	background: rgba(2, 6, 23, 0.52);
	box-shadow: none;
}

:global(:root[data-theme='dark']) .chat-header,
:global(.dark) .chat-header {
	border-color: rgba(148, 163, 184, 0.15);
	background: rgba(2, 6, 23, 0.64);
}

:global(:root[data-theme='dark']) .new-form,
:global(:root[data-theme='dark']) .composer,
:global(:root[data-theme='dark']) .message-row.assistant .message-bubble,
:global(:root[data-theme='dark']) .suggestions button,
:global(:root[data-theme='dark']) .tool-card,
:global(:root[data-theme='dark']) .source-item,
:global(:root[data-theme='dark']) .modes-dropdown-menu,
:global(.dark) .new-form,
:global(.dark) .composer,
:global(.dark) .message-row.assistant .message-bubble,
:global(.dark) .suggestions button,
:global(.dark) .tool-card,
:global(.dark) .source-item,
:global(.dark) .modes-dropdown-menu {
	border-color: rgba(148, 163, 184, 0.16);
	background: rgba(15, 23, 42, 0.76);
	box-shadow: 0 18px 44px rgba(0, 0, 0, 0.22);
}

:global(:root[data-theme='dark']) .message-row.assistant .avatar,
:global(:root[data-theme='dark']) .icon-btn,
:global(:root[data-theme='dark']) .secondary-btn,
:global(.dark) .message-row.assistant .avatar,
:global(.dark) .icon-btn,
:global(.dark) .secondary-btn {
	border-color: rgba(148, 163, 184, 0.18);
	background: rgba(15, 23, 42, 0.74);
	color: #e5edf8;
}

:global(:root[data-theme='dark']) .new-chat h1,
:global(:root[data-theme='dark']) .welcome-block h2,
:global(:root[data-theme='dark']) .panel-head h2,
:global(:root[data-theme='dark']) .tools-head h2,
:global(:root[data-theme='dark']) .session-title span,
:global(:root[data-theme='dark']) .session-item strong,
:global(:root[data-theme='dark']) .source-item strong,
:global(:root[data-theme='dark']) .tool-card strong,
:global(:root[data-theme='dark']) .message-bubble :deep(h1),
:global(:root[data-theme='dark']) .message-bubble :deep(h2),
:global(:root[data-theme='dark']) .message-bubble :deep(h3),
:global(:root[data-theme='dark']) .message-bubble :deep(h4),
:global(.dark) .new-chat h1,
:global(.dark) .welcome-block h2,
:global(.dark) .panel-head h2,
:global(.dark) .tools-head h2,
:global(.dark) .session-title span,
:global(.dark) .session-item strong,
:global(.dark) .source-item strong,
:global(.dark) .tool-card strong,
:global(.dark) .message-bubble :deep(h1),
:global(.dark) .message-bubble :deep(h2),
:global(.dark) .message-bubble :deep(h3),
:global(.dark) .message-bubble :deep(h4) {
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .rail-brand,
:global(:root[data-theme='dark']) .new-badge,
:global(:root[data-theme='dark']) .message-model,
:global(:root[data-theme='dark']) .pending-row span,
:global(.dark) .rail-brand,
:global(.dark) .new-badge,
:global(.dark) .message-model,
:global(.dark) .pending-row span {
	border-color: rgba(245, 179, 1, 0.2);
	background: rgba(245, 179, 1, 0.12);
	color: #f8c84e;
}

:global(:root[data-theme='dark']) .search-box,
:global(:root[data-theme='dark']) .model-switch,
:global(:root[data-theme='dark']) .new-form input,
:global(:root[data-theme='dark']) .new-form select,
:global(:root[data-theme='dark']) .new-form textarea,
:global(:root[data-theme='dark']) .soft-empty,
:global(.dark) .search-box,
:global(.dark) .model-switch,
:global(.dark) .new-form input,
:global(.dark) .new-form select,
:global(.dark) .new-form textarea,
:global(.dark) .soft-empty {
	border-color: rgba(148, 163, 184, 0.18);
	background: rgba(2, 6, 23, 0.38);
	color: #e5edf8;
}

:global(:root[data-theme='dark']) .form-group label,
:global(.dark) .form-group label {
	color: #cbd5e1;
}

:global(:root[data-theme='dark']) .composer-wrap,
:global(.dark) .composer-wrap {
	background:
		linear-gradient(180deg, rgba(7, 17, 31, 0), rgba(7, 17, 31, 0.9) 28%, rgba(7, 17, 31, 0.98));
}

:global(:root[data-theme='dark']) .session-item,
:global(.dark) .session-item {
	color: #cbd5e1;
}

:global(:root[data-theme='dark']) .session-item:hover,
:global(:root[data-theme='dark']) .session-item.active,
:global(.dark) .session-item:hover,
:global(.dark) .session-item.active {
	background: rgba(245, 179, 1, 0.1);
	border-color: rgba(245, 179, 1, 0.18);
	color: #f8c84e;
}

:global(:root[data-theme='dark']) .session-item.active::before,
:global(.dark) .session-item.active::before {
	background: var(--sb-gold);
}

:global(:root[data-theme='dark']) .message-bubble,
:global(.dark) .message-bubble {
	color: #e5edf8;
}

:global(:root[data-theme='dark']) .message-bubble :deep(code),
:global(.dark) .message-bubble :deep(code) {
	background: rgba(245, 179, 1, 0.12);
	color: #f8c84e;
}

/* ═══════════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════════ */

@media (max-width: 1180px) {
	.chat-page {
		grid-template-columns: minmax(0, 1fr);
		display: block;
	}

	.session-rail {
		position: fixed;
		top: 0;
		left: 0;
		z-index: 80;
		width: min(350px, 88vw);
		height: 100dvh;
		transform: translateX(-100%);
		transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
		box-shadow: none;
		padding-bottom: 6rem;
	}

	.session-rail.open {
		transform: translateX(0);
		box-shadow: 20px 0 70px rgba(15, 23, 42, 0.22);
	}

	.source-panel {
		position: fixed;
		top: 0;
		right: 0;
		z-index: 80;
		width: min(380px, 88vw);
		height: 100dvh;
		transform: translateX(100%);
		transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
		box-shadow: none;
		padding-bottom: 6rem;
	}

	.source-panel.open {
		transform: translateX(0);
		box-shadow: -20px 0 70px rgba(15, 23, 42, 0.22);
	}

	.mobile-only {
		display: inline-flex;
	}

	.hide-on-mobile {
		display: none !important;
	}

	.mobile-backdrop {
		position: fixed;
		inset: 0;
		z-index: 70;
		display: block;
		background: rgba(15, 23, 42, 0.42);
		backdrop-filter: blur(4px);
		opacity: 0;
		pointer-events: none;
		transition: opacity 0.25s ease;
	}

	.session-rail.open ~ .mobile-backdrop,
	.source-panel.open ~ .mobile-backdrop {
		opacity: 1;
		pointer-events: auto;
	}

	.chat-main {
		height: 100dvh;
	}
}

@media (max-width: 760px) {
	.chat-page {
		background:
			radial-gradient(circle at top left, rgba(10, 34, 81, 0.08), transparent 22rem),
			linear-gradient(180deg, #f5f8fc 0%, #f8fafc 100%);
	}

	.chat-header {
		min-height: 62px;
		padding: 0.55rem 0.65rem;
	}

	.header-actions {
		gap: 0.42rem;
	}

	.session-title span {
		font-size: 0.92rem;
	}

	.session-title small {
		max-width: 50vw;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.model-switch button {
		padding: 0.44rem 0.55rem;
	}

	.model-switch span {
		display: none;
	}

	.new-chat {
		padding: 1.5rem 1rem 8rem;
		align-items: start;
	}

	.new-chat-inner {
		padding-top: 1.4rem;
	}

	.new-chat h1 {
		font-size: clamp(2rem, 12vw, 2.65rem);
		letter-spacing: -0.06em;
	}

	.new-chat p {
		font-size: 0.9rem;
		line-height: 1.6;
	}

	.new-form {
		border-radius: 24px;
		padding: 1rem;
	}

	.new-form-row {
		grid-template-columns: 1fr;
		gap: 0.75rem;
	}

	.new-actions {
		display: grid;
		grid-template-columns: 1fr;
	}

	.new-actions .primary-btn,
	.new-actions .secondary-btn {
		width: 100%;
	}

	.chat-thread {
		flex: 1;
		padding: 1rem 1rem 150px;
	}

	.welcome-block {
		min-height: 52vh;
	}

	.welcome-block h2 {
		font-size: 1.5rem;
	}

	.suggestions {
		grid-template-columns: 1fr;
		gap: 0.65rem;
	}

	.suggestions button {
		min-height: 48px;
		border-radius: 16px;
		padding: 0.75rem 0.85rem;
		font-size: 0.84rem;
	}

	.message-row {
		gap: 0.5rem;
		margin: 1rem 0;
	}

	.avatar {
		width: 34px;
		height: 34px;
		border-radius: 13px;
	}

	.avatar svg {
		width: 16px;
		height: 16px;
	}

	.message-bubble {
		max-width: calc(100% - 42px);
		border-radius: 19px;
		padding: 0.82rem 0.92rem;
		font-size: 0.9rem;
		line-height: 1.65;
	}

	.message-row.user .message-bubble {
		border-bottom-right-radius: 6px;
	}

	.message-row.assistant .message-bubble {
		border-bottom-left-radius: 6px;
	}

	.follow-up-actions {
		margin-left: 42px;
		padding: 0;
		gap: 0.42rem;
	}

	.follow-up-actions button {
		padding: 0.42rem 0.65rem;
		font-size: 0.76rem;
	}

	.composer-wrap {
		position: fixed;
		right: 0;
		bottom: 0;
		left: 0;
		z-index: 50;
		padding: 0.55rem 0.75rem 0.7rem;
		background: rgba(245, 248, 252, 0.94);
		border-top: 1px solid rgba(226, 232, 240, 0.82);
		backdrop-filter: blur(16px);
	}

	.composer-wrap.panel-open {
		opacity: 0;
		pointer-events: none;
	}

	.composer {
		gap: 0.42rem;
		border-radius: 22px;
		padding: 0.45rem;
		box-shadow: 0 14px 36px rgba(15, 23, 42, 0.12);
	}

	.composer .icon-btn {
		width: 38px;
		height: 38px;
		border-radius: 14px;
	}

	.composer .send-btn {
		width: 42px;
		height: 42px;
		border-radius: 16px;
	}

	.composer textarea {
		min-height: 40px;
		max-height: 116px;
		padding: 0.52rem 0.35rem;
		font-size: 16px;
		line-height: 22px;
	}

	.pending-row {
		margin-bottom: 0.45rem;
	}

	.composer-meta {
		display: none !important;
	}

	.source-panel,
	.session-rail {
		width: min(350px, 90vw);
		padding: 0.9rem;
	}

	.tool-card,
	.session-item,
	.source-item {
		border-radius: 16px;
		padding: 0.78rem;
	}
}

@media (max-width: 430px) {
	.chat-header {
		gap: 0.45rem;
	}

	.header-left {
		gap: 0.45rem;
	}

	.icon-btn {
		width: 38px;
		height: 38px;
	}

	.model-switch {
		padding: 0.2rem;
	}

	.model-switch button {
		padding: 0.42rem 0.48rem;
	}

	.new-chat {
		padding-inline: 0.75rem;
	}

	.new-form {
		border-radius: 22px;
	}

	.message-bubble {
		font-size: 0.88rem;
		padding: 0.78rem 0.86rem;
	}

	.message-bubble :deep(h1) {
		font-size: 1.22rem;
	}

	.message-bubble :deep(h2) {
		font-size: 1.1rem;
	}

	.message-bubble :deep(h3) {
		font-size: 1rem;
	}

	.follow-up-actions {
		margin-left: 0;
	}

	.composer-wrap {
		padding-inline: 0.55rem;
	}

	.composer {
		border-radius: 20px;
	}

	.composer .icon-btn {
		width: 36px;
		height: 36px;
	}

	.composer .send-btn {
		width: 40px;
		height: 40px;
	}
}

/* ═══════════════════════════════════════════════
   REDUCED MOTION
   ═══════════════════════════════════════════════ */

@media (prefers-reduced-motion: reduce) {
	*,
	*::before,
	*::after {
		animation-duration: 0.001ms !important;
		animation-iteration-count: 1 !important;
		scroll-behavior: auto !important;
		transition-duration: 0.001ms !important;
	}
}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   QUITAR DEGRADADOS â€” STUDYBADGE CLEAN STYLE
   Pega esto al final del <style scoped>
   â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */

.chat-page {
	background: #f5f8fc !important;
}

.primary-btn {
	background: #0a2251 !important;
}

.primary-btn:hover:not(:disabled) {
	background: #12356e !important;
}

.send-btn {
	background: #0a2251 !important;
}

.send-btn:hover:not(:disabled) {
	background: #12356e !important;
}

.message-row.user .message-bubble {
	background: #0a2251 !important;
}

.tool-card::after {
	background: #0a2251 !important;
}

.new-form::before,
.new-chat-inner::before {
	display: none !important;
}

.composer-wrap {
	background: #f5f8fc !important;
}

.composer-wrap::before,
.composer-wrap::after {
	display: none !important;
}

/* MOBILE SIN DEGRADADO */
@media (max-width: 760px) {
	.chat-page {
		background: #f5f8fc !important;
	}

	.composer-wrap {
		background: #f5f8fc !important;
	}
}

/* DARK MODE SIN DEGRADADO */
:global(:root[data-theme='dark']) .chat-page,
:global(.dark) .chat-page {
	background: #07111f !important;
}

:global(:root[data-theme='dark']) .composer-wrap,
:global(.dark) .composer-wrap {
	background: #07111f !important;
}

/* ==========================================
   Skeleton Loaders
   ========================================== */
.chat-skeleton-wrapper {
	display: flex;
	height: 100vh;
	width: 100%;
	background: var(--bg-color);
}

.skeleton-head { height: 40px; margin-bottom: 1rem; border-radius: 8px; background: var(--border-color); animation: pulse 1.5s infinite; }
.skeleton-btn { height: 40px; margin-bottom: 1rem; border-radius: 8px; background: var(--border-color); animation: pulse 1.5s infinite; }
.skeleton-search { height: 40px; margin-bottom: 1.5rem; border-radius: 8px; background: var(--border-color); animation: pulse 1.5s infinite; }
.skeleton-session-item { display: flex; gap: 10px; margin-bottom: 1rem; padding: 0.5rem; border-radius: 8px; }
.skeleton-icon { width: 24px; height: 24px; border-radius: 4px; background: var(--border-color); animation: pulse 1.5s infinite; }
.skeleton-text-group { flex: 1; }
.skeleton-line { height: 12px; border-radius: 4px; background: var(--border-color); animation: pulse 1.5s infinite; margin-bottom: 6px; }
.skeleton-line.title { width: 80%; }
.skeleton-line.subtitle { width: 50%; height: 10px; }

.skeleton-main { padding: 0; background: var(--bg-color); }
.skeleton-header-title { width: 150px; height: 24px; border-radius: 6px; background: var(--border-color); animation: pulse 1.5s infinite; margin: 16px; }
.skeleton-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--border-color); animation: pulse 1.5s infinite; }
.skeleton-bubble { height: 60px; border-radius: 12px; background: var(--border-color); animation: pulse 1.5s infinite; margin-top: 4px; }
.skeleton-composer { width: 100%; height: 50px; border-radius: 12px; background: var(--border-color); animation: pulse 1.5s infinite; margin: 16px auto; max-width: 800px; }

@keyframes pulse {
	0% { opacity: 0.6; }
	50% { opacity: 0.3; }
	100% { opacity: 0.6; }
}
</style>

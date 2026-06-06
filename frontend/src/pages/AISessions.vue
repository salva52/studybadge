<template>
	<div class="chat-page" :class="{ 'right-collapsed': rightPanelCollapsed || !activeSession }" @paste="handlePaste">
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
					class="session-item session-card"
					:class="{ active: activeSession?.name === session.name }"
					@click="openSession(session.name)"
				>
					<span>
						<strong class="session-title-text">{{ session.title || session.name }}</strong>
						<small>{{ session.model_label || modelLabel(session.model_tier) }} · {{ formatDate(session.modified) }}</small>
						<div class="session-badges mt-1">
							<span v-if="session.materials?.length || session.has_materials || session.status === 'Draft'" class="badge-mini doc-badge">{{ __('Con documentos') }}</span>
							<span v-if="session.status === 'Completed'" class="badge-mini status-badge">{{ __('Listo') }}</span>
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
							<Zap class="size-4" /> <span>Light</span>
						</button>
						<button :class="{ active: selectedModel === 'pro', locked: !access?.pro_available }" @click="selectModel('pro')">
							<Crown class="size-4" /> <span>Pro</span>
						</button>
					</div>
					<button v-if="activeSession" class="icon-btn hide-on-mobile" :title="__('Agendar examen o tarea')" @click="scheduleActiveSession('exam')">
						<CalendarDays class="size-5" />
					</button>
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

			<footer v-if="activeSession" class="composer-wrap">
				<div class="composer-container">
					<!-- Bandeja de archivos pendientes (Estilo 'Chips' modernos) -->
					<div v-if="pendingFiles.length" class="pending-files-tray">
						<div v-for="file in pendingFiles" :key="file.file_url" class="pending-chip">
							<Paperclip class="size-3.5" />
							<span class="pending-chip-text">{{ file.file_name || file.file_url }}</span>
						</div>
					</div>

					<!-- Caja principal del input -->
					<div class="composer">
						<!-- Herramientas (Izquierda) -->
						<div class="composer-tools">
							<button class="composer-btn-ghost" :title="__('Subir fuentes')" @click="openUploader">
								<Paperclip class="size-5" />
							</button>
							<button class="composer-btn-ghost" :class="{ 'is-active': useSearch }" :title="__('Activar búsqueda web')" @click="useSearch = !useSearch">
								<Globe class="size-5" />
							</button>
							<div class="relative mode-dropdown-wrapper">
								<button class="composer-btn-ghost" :class="{ 'is-active': showModesDropdown || chatMode !== 'chat' }" :title="__('Modos de IA')" @click="showModesDropdown = !showModesDropdown">
									<Plus class="size-5" />
								</button>
								<div v-if="showModesDropdown" class="modes-dropdown-menu">
									<div class="modes-header">{{ __('Modo de IA') }}</div>
									<button v-for="m in chatModesList" :key="m.value" class="mode-dropdown-item" :class="{ active: chatMode === m.value }" @click="chatMode = m.value; showModesDropdown = false">
										{{ m.label }}
									</button>
								</div>
							</div>
						</div>

						<!-- Área de texto fluida -->
						<textarea
							ref="chatTextarea"
							v-model="chatInput"
							rows="1"
							:placeholder="__('Escríbeme…')"
							@input="autoResizeTextarea"
							@keydown.enter.exact.prevent="sendChat"
							@keydown.shift.enter.stop
						/>

						<!-- Botón de enviar interactivo (Derecha) -->
						<div class="composer-send-wrapper">
							<button 
								class="composer-send" 
								:class="{ 'can-send': chatInput.trim() || pendingFiles.length }" 
								:disabled="chatLoading || (!chatInput.trim() && !pendingFiles.length)" 
								@click="sendChat"
							>
								<SendHorizontal class="size-5" />
							</button>
						</div>
					</div>
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

			<div v-if="activeSession" class="calendar-actions">
				<button class="secondary-btn full" @click="scheduleActiveSession('exam')">
					<CalendarDays class="size-4" /> {{ __('Agendar examen') }}
				</button>
				<button class="secondary-btn full" @click="scheduleActiveSession('reminder')">
					<BellRing class="size-4" /> {{ __('Crear recordatorio') }}
				</button>
			</div>

			<div class="tools-head mt-0">
				<h2>{{ __('Chats') }}</h2>
				<p>{{ __('Historial de esta sesión') }}</p>
			</div>
			<button class="secondary-btn full" @click="startNewThread">
				<Plus class="size-4" /> {{ __('Nuevo chat') }}
			</button>
			<div class="sources-list scrollable-list">
				<div v-if="pinnedThreads.length > 0" class="thread-group-title">{{ __('Chats fijados') }}</div>
				<button v-for="thread in pinnedThreads" :key="thread.name" class="session-item group relative" :class="{ active: currentThread?.name === thread.name }" @click="switchThread(thread)">
					<MessageCircle class="size-4 mt-1" />
					<span>
						<strong>{{ thread.title || __('Chat') }}</strong>
						<small>{{ formatDate(thread.modified) }}</small>
					</span>
					<div class="thread-actions" @click.stop>
						<button class="thread-action-btn" title="Desfijar chat" @click.stop="togglePinThread(thread)">
							<PinOff class="size-3.5" />
						</button>
						<button class="thread-action-btn delete-btn" title="Eliminar chat" @click.stop="deleteThread(thread)">
							<Trash2 class="size-3.5" />
						</button>
					</div>
				</button>
				
				<div v-if="pinnedThreads.length > 0 && recentThreads.length > 0" class="thread-group-title mt-3">{{ __('Recientes') }}</div>
				<button v-for="thread in recentThreads" :key="thread.name" class="session-item group relative" :class="{ active: currentThread?.name === thread.name }" @click="switchThread(thread)">
					<MessageCircle class="size-4 mt-1" />
					<span>
						<strong>{{ thread.title || __('Chat') }}</strong>
						<small>{{ formatDate(thread.modified) }}</small>
					</span>
					<div class="thread-actions" @click.stop>
						<button class="thread-action-btn" title="Fijar chat" @click.stop="togglePinThread(thread)">
							<Pin class="size-3.5" />
						</button>
						<button class="thread-action-btn delete-btn" title="Eliminar chat" @click.stop="deleteThread(thread)">
							<Trash2 class="size-3.5" />
						</button>
					</div>
				</button>
			</div>

			<div class="tools-head mt-0">
				<h2>{{ __('Fuentes de estudio') }}</h2>
				<p>{{ materialCountText }}</p>
			</div>
			
			<TranscriptionCard v-if="activeSession" :session-name="activeSession.name" @transcription-completed="onTranscriptionCompleted" />
			<TranscriptionHistory v-if="activeSession" :session-name="activeSession.name" :refresh-trigger="refreshTranscriptionHistoryTrigger" @deleted="refreshSession" @completed="refreshSession" />

			<div class="flex gap-2">
				<button class="secondary-btn full flex-1" @click="openUploader">
					<Upload class="size-4" /> {{ __('Archivo') }}
				</button>
				<button class="secondary-btn full flex-1" @click="showTextModal = true">
					<Type class="size-4" /> {{ __('Texto') }}
				</button>
			</div>
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
					{{ __('Sube PDFs, trabajos, lecturas o imagenes.') }}
				</div>
			</div>

			<div class="tools-head">
				<h2>{{ __('Herramientas académicas') }}</h2>
				<p>{{ __('Responden dentro del chat') }}</p>
			</div>
			
			<div class="tool-group-title mt-2 mb-1">{{ __('Estudiar') }}</div>
			<div class="tool-list mb-3">
				<button v-for="tool in tools.filter(t => t.group === 'study')" :key="tool.id" class="tool-card" :class="{ locked: tool.pro && !access?.is_plus }" :disabled="toolLoading" @click="runTool(tool)">
					<component :is="tool.icon" class="size-5" />
					<span>
						<strong>{{ tool.label }}</strong>
						<small>{{ tool.description }}</small>
					</span>
					<Crown v-if="tool.pro && !access?.is_plus" class="size-4 lock-icon" />
				</button>
			</div>

			<div class="tool-group-title mt-2 mb-1">{{ __('Practicar') }}</div>
			<div class="tool-list mb-3">
				<button v-for="tool in tools.filter(t => t.group === 'practice')" :key="tool.id" class="tool-card" :class="{ locked: tool.pro && !access?.is_plus }" :disabled="toolLoading" @click="runTool(tool)">
					<component :is="tool.icon" class="size-5" />
					<span>
						<strong>{{ tool.label }}</strong>
						<small>{{ tool.description }}</small>
					</span>
					<Crown v-if="tool.pro && !access?.is_plus" class="size-4 lock-icon" />
				</button>
			</div>

			<div class="tool-group-title mt-2 mb-1">{{ __('Crear') }}</div>
			<div class="tool-list mb-3">
				<button v-for="tool in tools.filter(t => t.group === 'create')" :key="tool.id" class="tool-card" :class="{ locked: tool.pro && !access?.is_plus }" :disabled="toolLoading" @click="runTool(tool)">
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
		
		<div v-if="showTextModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-[1000]" @click="showTextModal = false">
			<div class="bg-white rounded-xl p-5 w-[90%] max-w-lg shadow-2xl flex flex-col" @click.stop>
				<div class="flex justify-between items-center mb-4 border-b pb-3">
					<h3 class="text-[1.05rem] font-bold text-ink-gray-9 m-0">{{ __('Agregar texto como fuente') }}</h3>
					<button class="icon-btn" @click="showTextModal = false"><X class="size-4" /></button>
				</div>
				<div class="flex flex-col gap-4 overflow-y-auto max-h-[60vh] p-1">
					<label class="flex flex-col gap-1.5">
						<span class="text-[0.8rem] font-bold text-ink-gray-5 uppercase tracking-wider">{{ __('Título (opcional)') }}</span>
						<input v-model="textTitle" class="border border-ink-gray-3 rounded-lg px-3 py-2.5 text-[0.9rem] focus:outline-none focus:ring-2 focus:ring-ink-blue-3" :placeholder="__('Ej: Apuntes de clase')" />
					</label>
					<label class="flex flex-col gap-1.5">
						<span class="text-[0.8rem] font-bold text-ink-gray-5 uppercase tracking-wider">{{ __('Contenido del texto') }}</span>
						<textarea v-model="textContent" rows="8" class="border border-ink-gray-3 rounded-lg px-3 py-2.5 text-[0.9rem] resize-y focus:outline-none focus:ring-2 focus:ring-ink-blue-3" :placeholder="__('Pega aquí el texto que quieres que la IA lea...')" />
					</label>
				</div>
				<div class="flex justify-end gap-3 mt-5 pt-3 border-t">
					<button class="secondary-btn" @click="showTextModal = false">{{ __('Cancelar') }}</button>
					<button class="primary-btn" :disabled="!textContent.trim() || isTextUploading" @click="uploadManualText">
						<Loader2 v-if="isTextUploading" class="size-4 animate-spin" />
						{{ isTextUploading ? __('Guardando...') : __('Agregar texto') }}
					</button>
				</div>
			</div>
		</div>
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
	BellRing,
	CalendarDays,
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
	Pin,
	PinOff,
	Trash2,
	Plus,
	Search,
	SendHorizontal,
	Settings,
	Sigma,
	Sparkles,
	Upload,
	User,
	Wrench,
	X,
	Zap,
	Globe,
	Type,
	Loader2,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import QuizModal from '@/components/QuizModal.vue'
import FlashcardsModal from '@/components/FlashcardsModal.vue'
import GuidedReadingModal from '@/components/GuidedReadingModal.vue'
import MathModal from '@/components/MathModal.vue'
import TranscriptionCard from '@/components/TranscriptionCard.vue'
import TranscriptionHistory from '@/components/TranscriptionHistory.vue'

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

const refreshTranscriptionHistoryTrigger = ref(0)

function onTranscriptionCompleted(res) {
	refreshTranscriptionHistoryTrigger.value++
	refreshSession()
}

async function refreshSession() {
	if (activeSession.value) {
		activeSession.value = await api('get_ai_session', { name: activeSession.value.name })
	}
}

const showAdvanced = ref(false)

const showTextModal = ref(false)
const textTitle = ref('')
const textContent = ref('')
const isTextUploading = ref(false)

async function uploadManualText() {
	if (!textContent.value.trim() || !activeSession.value) return
	isTextUploading.value = true
	try {
		const res = await api('upload_ai_session_text', {
			session: activeSession.value.name,
			title: textTitle.value,
			text: textContent.value
		})
		activeSession.value = res
		showTextModal.value = false
		textTitle.value = ''
		textContent.value = ''
		toast.success(__('Texto agregado a tus fuentes.'))
	} catch (e) {
		console.error(e)
	} finally {
		isTextUploading.value = false
	}
}

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

const pinnedThreads = computed(() => {
	return (activeSession.value?.threads || []).filter((t) => t.is_pinned)
})

const recentThreads = computed(() => {
	return (activeSession.value?.threads || []).filter((t) => !t.is_pinned)
})

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

const togglePinThread = async (thread) => {
	try {
		const newIsPinned = thread.is_pinned ? 0 : 1
		thread.is_pinned = newIsPinned
		const res = await api('pin_ai_thread', {
			session: activeSession.value.name,
			thread: thread.name,
			is_pinned: newIsPinned
		})
		activeSession.value = res
	} catch (error) {
		console.error(error)
		thread.is_pinned = thread.is_pinned ? 0 : 1
	}
}

const deleteThread = async (thread) => {
	if (!confirm(__('¿Seguro que deseas eliminar este chat?'))) return

	try {
		const isCurrent = currentThread.value?.name === thread.name
		const res = await api('delete_ai_thread', {
			session: activeSession.value.name,
			thread: thread.name
		})
		activeSession.value = res
		
		if (isCurrent) {
			currentThread.value = activeSession.value.threads?.[0] || null
			if (currentThread.value) {
				router.push(`/lms/ai-sessions/${activeSession.value.name}/${currentThread.value.name}`)
			} else {
				router.push(`/lms/ai-sessions/${activeSession.value.name}`)
			}
		}
	} catch (error) {
		console.error(error)
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

function scheduleActiveSession(type = 'exam') {
	if (!activeSession.value) return
	showTools.value = false
	router.push({
		name: 'StudyCalendar',
		query: {
			session: activeSession.value.name,
			type,
		},
	})
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
/*
	StudyBadge AI Sessions — clean readable UI
	Solo diseño: sin degradados, menos ruido visual y mejor orden móvil.
*/

.chat-page {
	--sb-primary: #0a2251;
	--sb-primary-hover: #12356e;
	--sb-bg: #f7f8fa;
	--sb-panel: #ffffff;
	--sb-panel-soft: #f3f4f6;
	--sb-panel-muted: #f8fafc;
	--sb-border: #e5e7eb;
	--sb-border-strong: #d1d5db;
	--sb-text: #111827;
	--sb-muted: #6b7280;
	--sb-soft: #9ca3af;
	--sb-success-bg: #ecfdf3;
	--sb-success: #15803d;
	--sb-info-bg: #eef6ff;
	--sb-info: #0b5cad;
	--sb-danger: #dc2626;
	--sb-shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.05);
	--sb-shadow-md: 0 8px 24px rgba(15, 23, 42, 0.08);
	--sb-radius-sm: 10px;
	--sb-radius-md: 14px;
	--sb-radius-lg: 20px;
	--sb-radius-xl: 26px;

	display: grid;
	grid-template-columns: 292px minmax(0, 1fr) 340px;
	height: 100dvh;
	min-height: 0;
	overflow: hidden;
	background: var(--sb-bg);
	color: var(--sb-text);
	font-size: 14px;
}

.hidden {
	display: none !important;
}

.relative {
	position: relative;
}

.mt-0 {
	margin-top: 0 !important;
}

.mt-1 {
	margin-top: 0.25rem !important;
}

.mt-2 {
	margin-top: 0.5rem !important;
}

.mt-3 {
	margin-top: 0.75rem !important;
}

.mb-1 {
	margin-bottom: 0.25rem !important;
}

.mb-3 {
	margin-bottom: 0.75rem !important;
}

.session-rail,
.source-panel,
.chat-thread,
.scrollable-list,
.composer textarea {
	scrollbar-width: thin;
	scrollbar-color: #d1d5db transparent;
}

.session-rail::-webkit-scrollbar,
.source-panel::-webkit-scrollbar,
.chat-thread::-webkit-scrollbar,
.scrollable-list::-webkit-scrollbar,
.composer textarea::-webkit-scrollbar {
	width: 8px;
}

.session-rail::-webkit-scrollbar-thumb,
.source-panel::-webkit-scrollbar-thumb,
.chat-thread::-webkit-scrollbar-thumb,
.scrollable-list::-webkit-scrollbar-thumb,
.composer textarea::-webkit-scrollbar-thumb {
	border-radius: 999px;
	background: #d1d5db;
}

/* Layout lateral */
.session-rail,
.source-panel {
	position: relative;
	z-index: 10;
	height: 100dvh;
	min-height: 0;
	overflow-y: auto;
	background: var(--sb-panel);
	padding: 18px;
}

.session-rail {
	border-right: 1px solid var(--sb-border);
}

.source-panel {
	border-left: 1px solid var(--sb-border);
}

.rail-head,
.panel-head,
.chat-header,
.header-left,
.header-actions,
.new-actions {
	display: flex;
	align-items: center;
	gap: 0.75rem;
}

.rail-head,
.panel-head,
.chat-header,
.new-actions {
	justify-content: space-between;
}

.rail-head,
.panel-head {
	margin-bottom: 1rem;
}

.rail-head > div,
.panel-head > div,
.session-title {
	min-width: 0;
}

.rail-brand,
.new-badge,
.message-model {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	width: fit-content;
	border: 1px solid var(--sb-border);
	border-radius: 999px;
	background: var(--sb-panel-muted);
	color: var(--sb-primary);
	font-size: 0.75rem;
	font-weight: 750;
	line-height: 1;
}

.rail-brand {
	padding: 0.45rem 0.65rem;
}

.rail-head p,
.panel-head p,
.tools-head p,
.session-title small,
.source-item small,
.session-item small,
.composer-meta,
.new-chat p,
.welcome-block p,
.tool-card small {
	margin: 0.32rem 0 0;
	color: var(--sb-muted);
	font-size: 0.78rem;
	line-height: 1.45;
}

.panel-head h2,
.tools-head h2 {
	margin: 0;
	color: var(--sb-text);
	font-size: 0.98rem;
	font-weight: 760;
	letter-spacing: -0.02em;
}

.tools-head {
	margin: 1.35rem 0 0.65rem;
	padding-top: 1.1rem;
	border-top: 1px solid var(--sb-border);
}

.tools-head.mt-0 {
	padding-top: 0;
	border-top: 0;
}

.tool-group-title,
.thread-group-title {
	padding: 0 0.35rem;
	color: var(--sb-muted);
	font-size: 0.72rem;
	font-weight: 760;
	letter-spacing: 0.06em;
	line-height: 1.3;
	text-transform: uppercase;
}

/* Botones */
.primary-btn,
.secondary-btn,
.icon-btn,
.send-btn,
.session-item,
.tool-card,
.suggestions button,
.mode-dropdown-item,
.modes-dropdown-menu button,
.thread-action-btn,
.toggle-advanced-btn {
	font: inherit;
	-webkit-tap-highlight-color: transparent;
	transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
}

.primary-btn,
.secondary-btn,
.icon-btn,
.send-btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	border-radius: 999px;
	font-weight: 760;
	text-decoration: none;
	cursor: pointer;
}

.primary-btn {
	min-height: 42px;
	border: 1px solid var(--sb-primary);
	background: var(--sb-primary);
	color: #ffffff;
	padding: 0.72rem 1rem;
	box-shadow: var(--sb-shadow-sm);
}

.primary-btn:hover:not(:disabled) {
	background: var(--sb-primary-hover);
	border-color: var(--sb-primary-hover);
}

.secondary-btn {
	min-height: 42px;
	border: 1px solid var(--sb-border);
	background: var(--sb-panel);
	color: var(--sb-text);
	padding: 0.72rem 1rem;
	box-shadow: var(--sb-shadow-sm);
}

.secondary-btn:hover:not(:disabled) {
	border-color: var(--sb-border-strong);
	background: var(--sb-panel-soft);
}

.primary-btn:disabled,
.secondary-btn:disabled,
.send-btn:disabled,
.tool-card:disabled {
	cursor: not-allowed;
	opacity: 0.55;
}

.full {
	width: 100%;
	margin-top: 0.75rem;
}

.icon-btn {
	width: 38px;
	height: 38px;
	flex: 0 0 auto;
	border: 1px solid var(--sb-border);
	background: var(--sb-panel);
	color: var(--sb-muted);
	box-shadow: none;
}

.icon-btn:hover,
.icon-btn.active,
.icon-btn.active-search,
.icon-btn.active-mode {
	border-color: var(--sb-border-strong);
	background: var(--sb-panel-soft);
	color: var(--sb-primary);
}

.send-btn {
	width: 42px;
	height: 42px;
	flex: 0 0 auto;
	border: 1px solid var(--sb-primary);
	background: var(--sb-primary);
	color: #ffffff;
}

.send-btn:hover:not(:disabled) {
	background: var(--sb-primary-hover);
	border-color: var(--sb-primary-hover);
}

/* Buscador y listas */
.search-box {
	display: flex;
	align-items: center;
	gap: 0.55rem;
	margin: 0.85rem 0 1rem;
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-md);
	background: var(--sb-panel-muted);
	padding: 0.68rem 0.78rem;
	color: var(--sb-muted);
}

.search-box:focus-within {
	border-color: var(--sb-primary);
	background: var(--sb-panel);
	box-shadow: 0 0 0 3px rgba(10, 34, 81, 0.09);
}

.search-box input {
	min-width: 0;
	flex: 1;
	border: 0;
	outline: 0;
	background: transparent;
	color: var(--sb-text);
	font-size: 0.9rem;
}

.search-box input::placeholder,
.new-form input::placeholder,
.new-form textarea::placeholder,
.composer textarea::placeholder {
	color: var(--sb-soft);
}

.session-list,
.sources-list,
.tool-list {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

.scrollable-list {
	max-height: 260px;
	overflow-y: auto;
	padding-right: 0.2rem;
}

.session-item,
.source-item,
.tool-card {
	position: relative;
	display: flex;
	align-items: flex-start;
	gap: 0.72rem;
	width: 100%;
	border: 1px solid transparent;
	border-radius: var(--sb-radius-md);
	background: transparent;
	padding: 0.78rem;
	color: var(--sb-text);
	text-align: left;
}

.session-item {
	cursor: pointer;
}

.session-card {
	border-color: var(--sb-border);
	background: var(--sb-panel);
	box-shadow: none;
}

.session-item:hover,
.tool-card:hover:not(:disabled),
.source-item:hover {
	border-color: var(--sb-border-strong);
	background: var(--sb-panel-soft);
}

.session-item.active,
.session-card.active {
	border-color: rgba(10, 34, 81, 0.35);
	background: #eef2f7;
	color: var(--sb-primary);
}

.session-item.active::before {
	content: '';
	position: absolute;
	top: 10px;
	bottom: 10px;
	left: 0;
	width: 3px;
	border-radius: 999px;
	background: var(--sb-primary);
}

.session-item svg,
.source-item svg,
.tool-card svg {
	flex: 0 0 auto;
	margin-top: 0.12rem;
	color: var(--sb-muted);
}

.session-item.active svg,
.session-item:hover svg,
.source-item svg,
.tool-card svg {
	color: var(--sb-primary);
}

.session-item span,
.source-item span,
.tool-card span {
	min-width: 0;
	display: flex;
	flex: 1;
	flex-direction: column;
	gap: 0.12rem;
}

.session-item strong,
.source-item strong,
.tool-card strong {
	overflow: hidden;
	color: var(--sb-text);
	font-size: 0.88rem;
	font-weight: 760;
	line-height: 1.25;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.session-title-text {
	font-size: 0.95rem !important;
	letter-spacing: -0.01em;
}

.session-badges {
	display: flex;
	flex-wrap: wrap;
	gap: 0.32rem;
	margin-top: 0.38rem !important;
}

.badge-mini {
	display: inline-flex;
	align-items: center;
	width: fit-content;
	border-radius: 999px;
	padding: 0.2rem 0.46rem;
	font-size: 0.68rem;
	font-weight: 760;
	line-height: 1;
}

.doc-badge {
	background: var(--sb-info-bg);
	color: var(--sb-info);
}

.status-badge {
	background: var(--sb-success-bg);
	color: var(--sb-success);
}

.source-item {
	border-color: var(--sb-border);
	background: var(--sb-panel-muted);
}

.tool-card {
	border-color: var(--sb-border);
	background: var(--sb-panel);
	cursor: pointer;
}

.tool-card small {
	font-size: 0.74rem;
}

.tool-card.locked {
	background: #fffbeb;
	border-color: #fde68a;
}

.lock-icon {
	margin-left: auto;
	color: #b45309 !important;
}

/* Chat principal */
.chat-main {
	display: flex;
	flex-direction: column;
	min-width: 0;
	height: 100dvh;
	overflow: hidden;
	background: var(--sb-bg);
}

.chat-header {
	position: sticky;
	top: 0;
	z-index: 5;
	min-height: 64px;
	border-bottom: 1px solid var(--sb-border);
	background: rgba(247, 248, 250, 0.94);
	padding: 0.75rem 1rem;
	backdrop-filter: blur(14px);
}

.header-left {
	flex: 1;
	min-width: 0;
	justify-content: flex-start;
}

.header-actions {
	flex-shrink: 0;
	justify-content: flex-end;
}

.session-title {
	display: flex;
	flex-direction: column;
}

.session-title span {
	overflow: hidden;
	color: var(--sb-text);
	font-size: 0.98rem;
	font-weight: 760;
	letter-spacing: -0.02em;
	line-height: 1.2;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.model-switch {
	display: inline-flex;
	gap: 0.25rem;
	border: 1px solid var(--sb-border);
	border-radius: 999px;
	background: var(--sb-panel);
	padding: 0.22rem;
}

.model-switch button {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	border: 0;
	border-radius: 999px;
	background: transparent;
	color: var(--sb-muted);
	padding: 0.45rem 0.7rem;
	font-size: 0.78rem;
	font-weight: 760;
	white-space: nowrap;
	cursor: pointer;
}

.model-switch button:hover {
	color: var(--sb-primary);
}

.model-switch button.active {
	background: var(--sb-primary);
	color: #ffffff;
}

.model-switch button.locked:not(.active) {
	color: #a16207;
}

/* Pantalla inicial */
.new-chat,
.chat-thread {
	min-height: 0;
	overflow-y: auto;
	overflow-x: hidden;
}

.new-chat {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 2rem;
}

.new-chat-inner {
	width: min(760px, 100%);
	text-align: center;
}

.new-badge {
	margin-bottom: 0.9rem;
	padding: 0.45rem 0.75rem;
}

.new-chat h1 {
	margin: 0;
	color: var(--sb-text);
	font-size: clamp(2rem, 4.8vw, 3.4rem);
	font-weight: 820;
	letter-spacing: -0.055em;
	line-height: 1.02;
	text-wrap: balance;
}

.new-chat p {
	max-width: 600px;
	margin: 0.9rem auto 0;
	font-size: 0.98rem;
	line-height: 1.65;
}

.new-form {
	width: 100%;
	margin-top: 1.65rem;
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-xl);
	background: var(--sb-panel);
	padding: 1.1rem;
	text-align: left;
	box-shadow: var(--sb-shadow-md);
}

.form-group {
	display: flex;
	flex-direction: column;
	gap: 0.42rem;
}

.form-group label {
	color: var(--sb-text);
	font-size: 0.82rem;
	font-weight: 760;
}

.new-form input,
.new-form select,
.new-form textarea {
	width: 100%;
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-md);
	background: var(--sb-panel-muted);
	color: var(--sb-text);
	outline: 0;
	padding: 0.82rem 0.92rem;
	font-size: 0.95rem;
}

.new-form input:focus,
.new-form select:focus,
.new-form textarea:focus {
	border-color: var(--sb-primary);
	background: var(--sb-panel);
	box-shadow: 0 0 0 3px rgba(10, 34, 81, 0.09);
}

.title-input {
	min-height: 54px;
	border-radius: 18px !important;
	font-size: 1.02rem !important;
	font-weight: 650;
}

.new-form textarea {
	resize: vertical;
	line-height: 1.55;
}

.new-form-row {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 0.8rem;
	margin-top: 0.7rem;
}

.toggle-advanced-btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.45rem;
	margin-top: 0.8rem;
	border: 1px solid var(--sb-border);
	border-radius: 999px;
	background: var(--sb-panel);
	color: var(--sb-muted);
	padding: 0.58rem 0.85rem;
	font-size: 0.84rem;
	font-weight: 720;
	cursor: pointer;
}

.toggle-advanced-btn:hover {
	border-color: var(--sb-border-strong);
	background: var(--sb-panel-soft);
	color: var(--sb-primary);
}

.advanced-options {
	margin-top: 0.8rem;
	padding-top: 0.9rem;
	border-top: 1px solid var(--sb-border);
}

.new-actions {
	margin-top: 1rem;
}

/* Conversación */
.chat-thread {
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: clamp(36px, 6vh, 64px) 24px 32px;
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
	max-width: 680px;
	margin: 0.75rem auto 0;
	color: var(--sb-text);
	font-size: clamp(1.35rem, 3.2vw, 2rem);
	font-weight: 800;
	letter-spacing: -0.045em;
	line-height: 1.15;
	text-wrap: balance;
}

.suggestions {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
	gap: 0.7rem;
	width: 100%;
	max-width: 760px;
	margin-top: 1.4rem;
}

.suggestions button {
	min-height: 50px;
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-md);
	background: var(--sb-panel);
	color: var(--sb-text);
	padding: 0.85rem 0.95rem;
	font-size: 0.88rem;
	font-weight: 650;
	text-align: left;
	cursor: pointer;
	box-shadow: none;
}

.suggestions button:hover {
	border-color: var(--sb-border-strong);
	background: var(--sb-panel-soft);
	color: var(--sb-primary);
}

.message-row-wrapper {
	display: flex;
	flex-direction: column;
	gap: 0.45rem;
	width: 100%;
	max-width: 980px;
}

.message-row {
	display: flex;
	width: 100%;
	min-width: 0;
	gap: 0.65rem;
	margin: 0.85rem 0;
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
	width: 34px;
	height: 34px;
	flex: 0 0 auto;
	place-items: center;
	border: 1px solid var(--sb-border);
	border-radius: 999px;
	background: var(--sb-panel);
	color: var(--sb-muted);
}

.message-row.user .avatar {
	background: var(--sb-primary);
	border-color: var(--sb-primary);
	color: #ffffff;
}

.message-row.assistant .avatar {
	color: var(--sb-primary);
}

.message-bubble {
	box-sizing: border-box;
	min-width: 0;
	max-width: min(780px, calc(100% - 48px));
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-lg);
	background: var(--sb-panel);
	padding: 0.88rem 1rem;
	color: var(--sb-text);
	font-size: 0.95rem;
	line-height: 1.72;
	overflow-wrap: anywhere;
	word-break: break-word;
}

.message-row.user .message-bubble {
	border-color: var(--sb-primary);
	border-bottom-right-radius: 7px;
	background: var(--sb-primary);
	color: #ffffff;
}

.message-row.assistant .message-bubble {
	border-bottom-left-radius: 7px;
}

.message-bubble > div {
	min-width: 0;
	max-width: 100%;
	overflow-wrap: anywhere;
	word-break: break-word;
}

.message-model {
	margin-bottom: 0.5rem;
	padding: 0.25rem 0.5rem;
	font-size: 0.67rem;
	letter-spacing: 0.05em;
	text-transform: uppercase;
}

.message-row.user .message-model {
	border-color: rgba(255, 255, 255, 0.22);
	background: rgba(255, 255, 255, 0.12);
	color: rgba(255, 255, 255, 0.9);
}

.message-bubble :deep(p) {
	margin: 0 0 0.85rem;
}

.message-bubble :deep(p:last-child) {
	margin-bottom: 0;
}

.message-bubble :deep(ul),
.message-bubble :deep(ol) {
	margin: 0.7rem 0 0.85rem 1.2rem;
	padding: 0;
}

.message-bubble :deep(li) {
	margin: 0.32rem 0;
}

.message-bubble :deep(li > p) {
	margin: 0;
}

.message-bubble :deep(h1),
.message-bubble :deep(h2),
.message-bubble :deep(h3),
.message-bubble :deep(h4) {
	margin: 1rem 0 0.5rem;
	color: var(--sb-text);
	font-weight: 780;
	letter-spacing: -0.03em;
	line-height: 1.22;
}

.message-row.user .message-bubble :deep(h1),
.message-row.user .message-bubble :deep(h2),
.message-row.user .message-bubble :deep(h3),
.message-row.user .message-bubble :deep(h4) {
	color: #ffffff;
}

.message-bubble :deep(h1) {
	font-size: 1.4rem;
}

.message-bubble :deep(h2) {
	font-size: 1.2rem;
}

.message-bubble :deep(h3) {
	font-size: 1.06rem;
}

.message-bubble :deep(h4) {
	font-size: 0.98rem;
}

.message-bubble :deep(strong) {
	font-weight: 780;
}

.message-bubble :deep(hr) {
	margin: 1rem 0;
	border: 0;
	border-top: 1px solid var(--sb-border);
}

.message-bubble :deep(blockquote) {
	margin: 0.85rem 0;
	border-left: 3px solid rgba(10, 34, 81, 0.24);
	border-radius: 0 var(--sb-radius-sm) var(--sb-radius-sm) 0;
	background: var(--sb-panel-muted);
	padding: 0.7rem 0.85rem;
	color: #4b5563;
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
	border: 1px solid var(--sb-border);
	border-radius: 8px;
	background: var(--sb-panel-muted);
	padding: 0.14rem 0.35rem;
	color: var(--sb-primary);
	font-size: 0.9em;
}

.message-row.user .message-bubble :deep(code) {
	border-color: rgba(255, 255, 255, 0.18);
	background: rgba(255, 255, 255, 0.14);
	color: #ffffff;
}

.message-bubble :deep(pre) {
	border-radius: var(--sb-radius-md);
	background: #0f172a;
	padding: 0.9rem;
	color: #f8fafc;
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
	border: 1px solid var(--sb-border);
	padding: 0.52rem 0.65rem;
}

.message-bubble img,
.chat-image {
	display: block;
	max-width: 100%;
	height: auto;
	margin-top: 0.8rem;
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-md);
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
	min-width: 70px;
}

.typing span {
	width: 7px;
	height: 7px;
	border-radius: 999px;
	background: var(--sb-primary);
	opacity: 0.3;
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
		opacity: 0.3;
		transform: translateY(0);
	}
	40% {
		opacity: 1;
		transform: translateY(-3px);
	}
}

.follow-up-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.45rem;
	max-width: 100%;
	margin: 0 0 0.7rem 44px;
}

.follow-up-actions button {
	border: 1px solid var(--sb-border);
	border-radius: 999px;
	background: var(--sb-panel);
	color: var(--sb-muted);
	padding: 0.42rem 0.68rem;
	font-size: 0.76rem;
	font-weight: 650;
	white-space: normal;
	overflow-wrap: anywhere;
	cursor: pointer;
}

.follow-up-actions button:hover {
	border-color: var(--sb-border-strong);
	background: var(--sb-panel-soft);
	color: var(--sb-primary);
}

/* =========================================
   COMPOSER (Área de escritura moderna)
   ========================================= */
.composer-wrap {
	position: sticky;
	bottom: 0;
	z-index: 6;
	width: 100%;
	/* Fondo difuminado moderno en lugar de un borde estricto */
	background: linear-gradient(180deg, transparent 0%, var(--sb-bg) 20%);
	padding: 0 1rem 1.5rem;
}

.composer-container {
	position: relative;
	width: min(860px, 100%);
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	gap: 0.6rem;
}

.composer {
	display: flex;
	align-items: flex-end;
	gap: 0.2rem;
	background: var(--sb-panel);
	border: 1px solid var(--sb-border-strong);
	border-radius: 26px; /* Forma de píldora/cápsula redonda */
	padding: 0.35rem 0.5rem;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
	transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.composer:focus-within {
	border-color: var(--sb-primary);
	box-shadow: 0 4px 24px rgba(10, 34, 81, 0.08);
}

/* Herramientas (Botones Izquierda) */
.composer-tools {
	display: flex;
	align-items: center;
	gap: 0.15rem;
	padding-bottom: 0.18rem; /* Ancla los botones abajo cuando el textarea crece */
}

.composer-btn-ghost {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 38px;
	height: 38px;
	border-radius: 50%;
	border: none;
	background: transparent;
	color: var(--sb-muted);
	cursor: pointer;
	transition: all 0.2s ease;
}

.composer-btn-ghost:hover {
	background: var(--sb-panel-soft);
	color: var(--sb-text);
}

.composer-btn-ghost.is-active {
	color: var(--sb-primary);
	background: var(--sb-info-bg);
}

/* Textarea fluido */
.composer textarea {
	flex: 1;
	min-height: 42px;
	max-height: 200px;
	padding: 0.65rem 0.4rem;
	border: none;
	background: transparent;
	color: var(--sb-text);
	font-size: 0.98rem;
	line-height: 1.5;
	resize: none;
	outline: none;
}

.composer textarea::placeholder {
	color: var(--sb-soft);
}

/* Botón de Enviar dinámico (Derecha) */
.composer-send-wrapper {
	padding-bottom: 0.18rem;
}

.composer-send {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 40px;
	height: 40px;
	border-radius: 50%;
	border: none;
	background: var(--sb-panel-soft);
	color: var(--sb-muted);
	cursor: pointer;
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Estado activo: cuando hay texto o archivos */
.composer-send.can-send {
	background: var(--sb-primary);
	color: white;
	box-shadow: 0 4px 12px rgba(10, 34, 81, 0.2);
}

.composer-send.can-send:hover:not(:disabled) {
	transform: scale(1.05);
	background: var(--sb-primary-hover);
}

/* Archivos pendientes (Chips) */
.pending-files-tray {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
	padding: 0 0.5rem;
}

.pending-chip {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	background: var(--sb-panel);
	border: 1px solid var(--sb-border);
	border-radius: 12px;
	padding: 0.4rem 0.7rem;
	font-size: 0.82rem;
	font-weight: 650;
	color: var(--sb-text);
	box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

.pending-chip svg {
	color: var(--sb-primary);
}

.pending-chip-text {
	max-width: 180px;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

/* Dropdown */
.mode-dropdown-wrapper {
	position: relative;
}

.modes-dropdown-menu {
	position: absolute;
	bottom: calc(100% + 8px);
	left: 0;
	z-index: 60;
	width: 210px;
	max-width: calc(100vw - 24px);
	border: 1px solid var(--sb-border);
	border-radius: var(--sb-radius-md);
	background: var(--sb-panel);
	padding: 0.35rem;
	box-shadow: var(--sb-shadow-md);
}

.modes-header {
	padding: 0.52rem 0.7rem 0.35rem;
	color: var(--sb-muted);
	font-size: 0.68rem;
	font-weight: 760;
	letter-spacing: 0.07em;
	text-transform: uppercase;
}

.mode-dropdown-item,
.modes-dropdown-menu button {
	width: 100%;
	border: 0;
	border-radius: 10px;
	background: transparent;
	padding: 0.68rem 0.7rem;
	color: var(--sb-text);
	font-size: 0.84rem;
	font-weight: 650;
	text-align: left;
	cursor: pointer;
}

.mode-dropdown-item:hover,
.mode-dropdown-item.active,
.modes-dropdown-menu button:hover,
.modes-dropdown-menu button.active {
	background: var(--sb-panel-soft);
	color: var(--sb-primary);
}

/* Estados vacíos */
.soft-empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	min-height: 104px;
	border: 1px dashed var(--sb-border-strong);
	border-radius: var(--sb-radius-md);
	background: var(--sb-panel-muted);
	padding: 1rem;
	color: var(--sb-muted);
	font-size: 0.84rem;
	font-weight: 650;
	line-height: 1.45;
	text-align: center;
}

.soft-empty svg {
	color: var(--sb-primary);
}

/* Acciones de chats */
.thread-actions {
	position: absolute;
	right: 0.45rem;
	top: 50%;
	display: flex;
	gap: 0.25rem;
	opacity: 0;
	transform: translateY(-50%);
}

.session-item:hover .thread-actions,
.session-item:focus-within .thread-actions {
	opacity: 1;
}

.thread-action-btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border: 1px solid var(--sb-border);
	border-radius: 9px;
	background: var(--sb-panel);
	color: var(--sb-muted);
	padding: 0.35rem;
	cursor: pointer;
}

.thread-action-btn:hover {
	border-color: var(--sb-border-strong);
	background: var(--sb-panel-soft);
	color: var(--sb-text);
}

.thread-action-btn.delete-btn:hover {
	border-color: #fecaca;
	background: #fef2f2;
	color: var(--sb-danger);
}

.calendar-actions {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 0.55rem;
	margin-bottom: 1rem;
}

.mobile-only,
.mobile-backdrop {
	display: none;
}

/* Panel derecho oculto */
@media (min-width: 1181px) {
	.chat-page.right-collapsed {
		grid-template-columns: 292px minmax(0, 1fr);
	}

	.chat-page.right-collapsed .source-panel {
		display: none;
	}
}

/* Skeleton */
.chat-skeleton-wrapper {
	grid-column: 1 / -1;
	display: grid;
	grid-template-columns: 292px minmax(0, 1fr);
	height: 100dvh;
	width: 100%;
	background: var(--sb-bg);
}

.skeleton-head,
.skeleton-btn,
.skeleton-search,
.skeleton-icon,
.skeleton-line,
.skeleton-header-title,
.skeleton-header-actions,
.skeleton-avatar,
.skeleton-bubble,
.skeleton-composer {
	border-radius: var(--sb-radius-sm);
	background: #e5e7eb;
	animation: pulse 1.35s infinite ease-in-out;
}

.skeleton-head {
	height: 40px;
	margin-bottom: 1rem;
}

.skeleton-btn,
.skeleton-search {
	height: 40px;
	margin-bottom: 1rem;
}

.skeleton-session-item {
	display: flex;
	gap: 10px;
	margin-bottom: 0.85rem;
	padding: 0.5rem;
	border-radius: var(--sb-radius-sm);
}

.skeleton-icon {
	width: 24px;
	height: 24px;
}

.skeleton-text-group {
	flex: 1;
}

.skeleton-line {
	height: 12px;
	margin-bottom: 6px;
}

.skeleton-line.title {
	width: 80%;
}

.skeleton-line.subtitle {
	width: 50%;
	height: 10px;
}

.skeleton-main {
	padding: 0;
	background: var(--sb-bg);
}

.skeleton-header-title {
	width: 150px;
	height: 24px;
}

.skeleton-header-actions {
	width: 110px;
	height: 32px;
}

.skeleton-avatar {
	width: 34px;
	height: 34px;
	border-radius: 999px;
}

.skeleton-bubble {
	height: 60px;
	margin-top: 4px;
}

.skeleton-composer {
	width: 100%;
	max-width: 920px;
	height: 52px;
	margin: 0 auto;
	border-radius: 24px;
}

@keyframes pulse {
	0%, 100% {
		opacity: 0.62;
	}
	50% {
		opacity: 0.34;
	}
}

/* Móvil y tablet */
@media (max-width: 1180px) {
	.chat-page {
		display: block;
		grid-template-columns: minmax(0, 1fr);
	}

	.session-rail,
	.source-panel {
		position: fixed;
		top: 0;
		z-index: 80;
		width: min(380px, 90vw);
		height: 100dvh;
		padding-bottom: calc(5rem + env(safe-area-inset-bottom, 0px));
		box-shadow: var(--sb-shadow-md);
		transition: transform 0.24s ease;
	}

	.session-rail {
		left: 0;
		transform: translateX(-100%);
	}

	.session-rail.open {
		transform: translateX(0);
	}

	.source-panel {
		right: 0;
		transform: translateX(100%);
	}

	.source-panel.open {
		transform: translateX(0);
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
		background: rgba(17, 24, 39, 0.42);
	}

	.chat-main {
		height: 100dvh;
	}

	.chat-skeleton-wrapper {
		grid-template-columns: minmax(0, 1fr);
	}

	.chat-skeleton-wrapper .session-rail {
		display: none;
	}
}

@media (max-width: 760px) {
	.chat-page {
		font-size: 14px;
	}

	.chat-header {
		min-height: 60px;
		padding: 0.55rem 0.65rem;
	}

	.header-left {
		gap: 0.5rem;
	}

	.header-actions {
		gap: 0.4rem;
	}

	.session-title span {
		max-width: 42vw;
		font-size: 0.92rem;
	}

	.session-title small {
		max-width: 42vw;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.model-switch button {
		padding: 0.42rem 0.54rem;
	}

	.model-switch span {
		display: none;
	}

	.new-chat {
		align-items: flex-start;
		padding: 1.35rem 0.85rem 7.5rem;
	}

	.new-chat-inner {
		padding-top: 1rem;
	}

	.new-chat h1 {
		font-size: clamp(2rem, 11vw, 2.7rem);
		letter-spacing: -0.06em;
	}

	.new-chat p {
		font-size: 0.92rem;
		line-height: 1.55;
	}

	.new-form {
		margin-top: 1.25rem;
		border-radius: 22px;
		padding: 0.9rem;
	}

	.title-input {
		min-height: 52px;
		font-size: 16px !important;
	}

	.new-form input,
	.new-form select,
	.new-form textarea {
		font-size: 16px;
		padding: 0.78rem 0.86rem;
	}

	.new-form-row {
		grid-template-columns: 1fr;
		gap: 0.7rem;
	}

	.toggle-advanced-btn {
		width: 100%;
		min-height: 42px;
	}

	.new-actions {
		display: grid;
		grid-template-columns: 1fr;
		gap: 0.55rem;
	}

	.new-actions .primary-btn {
		order: -1;
	}

	.new-actions .primary-btn,
	.new-actions .secondary-btn {
		width: 100%;
	}

	.chat-thread {
		padding: 1rem 0.85rem 145px;
	}

	.welcome-block {
		min-height: 50vh;
	}

	.welcome-block h2 {
		font-size: 1.45rem;
	}

	.suggestions {
		grid-template-columns: 1fr;
		gap: 0.55rem;
	}

	.suggestions button {
		min-height: 48px;
		border-radius: var(--sb-radius-md);
		padding: 0.72rem 0.8rem;
		font-size: 0.84rem;
	}

	.message-row {
		gap: 0.5rem;
		margin: 0.75rem 0;
	}

	.avatar {
		width: 30px;
		height: 30px;
	}

	.avatar svg {
		width: 15px;
		height: 15px;
	}

	.message-bubble {
		max-width: calc(100% - 38px);
		border-radius: 17px;
		padding: 0.78rem 0.86rem;
		font-size: 0.9rem;
		line-height: 1.62;
	}

	.message-row.user .message-bubble {
		border-bottom-right-radius: 6px;
	}

	.message-row.assistant .message-bubble {
		border-bottom-left-radius: 6px;
	}

	.follow-up-actions {
		margin-left: 38px;
		gap: 0.38rem;
	}

	.follow-up-actions button {
		padding: 0.4rem 0.62rem;
		font-size: 0.74rem;
	}

	.composer-wrap {
		position: fixed;
		right: 0;
		bottom: 0;
		left: 0;
		z-index: 5;
		padding: 0.55rem 0.65rem calc(65px + env(safe-area-inset-bottom, 0px));
	}

	.composer {
		gap: 0.35rem;
		border-radius: 21px;
		padding: 0.38rem;
	}

	.composer .icon-btn {
		width: 36px;
		height: 36px;
	}

	.composer .send-btn {
		width: 40px;
		height: 40px;
	}

	.composer textarea {
		min-height: 39px;
		max-height: 116px;
		padding: 0.52rem 0.3rem;
		font-size: 16px;
		line-height: 22px;
	}

	.pending-row {
		margin-bottom: 0.42rem;
	}

	.composer-meta {
		display: none !important;
	}

	.session-rail,
	.source-panel {
		width: min(360px, 92vw);
		padding: 0.85rem;
	}

	.session-list,
	.sources-list,
	.tool-list {
		gap: 0.45rem;
	}

	.tool-card,
	.session-item,
	.source-item {
		border-radius: var(--sb-radius-md);
		padding: 0.72rem;
	}

	.tool-list {
		display: grid;
		grid-template-columns: 1fr;
	}

	.calendar-actions {
		grid-template-columns: 1fr 1fr;
	}
}

@media (max-width: 430px) {
	.chat-header {
		gap: 0.4rem;
	}

	.icon-btn {
		width: 36px;
		height: 36px;
	}

	.model-switch {
		padding: 0.18rem;
	}

	.model-switch button {
		padding: 0.38rem 0.44rem;
	}

	.new-chat {
		padding-inline: 0.7rem;
	}

	.message-bubble {
		font-size: 0.88rem;
		padding: 0.74rem 0.82rem;
	}

	.follow-up-actions {
		margin-left: 0;
	}

	.calendar-actions {
		grid-template-columns: 1fr;
	}

	.thread-actions {
		opacity: 1;
	}
}

@media (max-width: 760px) {
	.composer-wrap {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		z-index: 5;
		padding: 0.5rem 0.6rem calc(65px + env(safe-area-inset-bottom, 0px));
		background: rgba(247, 248, 250, 0.88);
		backdrop-filter: blur(14px);
		-webkit-backdrop-filter: blur(14px);
		border-top: 1px solid var(--sb-border);
	}

	.composer {
		border-radius: 24px;
		padding: 0.35rem;
	}

	.composer-btn-ghost {
		width: 36px;
		height: 36px;
	}

	.composer textarea {
		min-height: 40px;
		padding: 0.55rem 0.2rem;
		font-size: 16px;
	}

	.composer-send {
		width: 36px;
		height: 36px;
	}

	.pending-chip {
		padding: 0.3rem 0.6rem;
		font-size: 0.75rem;
	}
}

/* Dark mode limpio */
:global(:root[data-theme='dark']) .chat-page,
:global(.dark) .chat-page {
	--sb-bg: #0b0f17;
	--sb-panel: #111827;
	--sb-panel-soft: #1f2937;
	--sb-panel-muted: #151d2b;
	--sb-border: #253044;
	--sb-border-strong: #334155;
	--sb-text: #f8fafc;
	--sb-muted: #a1aab8;
	--sb-soft: #697386;
	--sb-info-bg: #0b2744;
	--sb-info: #93c5fd;
	--sb-success-bg: #092b19;
	--sb-success: #86efac;
	--sb-shadow-sm: 0 1px 2px rgba(0,0,0,0.2);
	--sb-shadow-md: 0 8px 30px rgba(0, 0, 0, 0.4);
	background: linear-gradient(135deg, var(--sb-bg) 0%, #131b2c 100%);
	color: var(--sb-text);
}

:global(:root[data-theme='dark']) .chat-header,
:global(.dark) .chat-header {
	background: rgba(11, 15, 23, 0.75);
	backdrop-filter: blur(16px);
	-webkit-backdrop-filter: blur(16px);
	border-top: 1px solid rgba(255, 255, 255, 0.05);
}

/* Soporte Dark Mode para el nuevo diseño */
:global(:root[data-theme='dark']) .composer,
:global(.dark) .composer {
	background: var(--sb-panel);
	border-color: rgba(255,255,255,0.08);
}

:global(:root[data-theme='dark']) .composer-wrap,
:global(.dark) .composer-wrap {
	background: linear-gradient(180deg, transparent 0%, var(--sb-bg) 35%);
}

@media (max-width: 760px) {
	:global(:root[data-theme='dark']) .composer-wrap,
	:global(.dark) .composer-wrap {
		background: rgba(11, 15, 23, 0.85);
		border-top-color: rgba(255,255,255,0.05);
	}
}

:global(:root[data-theme='dark']) .message-row.user .message-bubble,
:global(.dark) .message-row.user .message-bubble,
:global(:root[data-theme='dark']) .message-row.user .avatar,
:global(.dark) .message-row.user .avatar,
:global(:root[data-theme='dark']) .primary-btn,
:global(.dark) .primary-btn,
:global(:root[data-theme='dark']) .send-btn,
:global(.dark) .send-btn,
:global(:root[data-theme='dark']) .model-switch button.active,
:global(.dark) .model-switch button.active {
	background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
	border-color: transparent;
	box-shadow: 0 4px 14px rgba(59, 130, 246, 0.25);
	transition: all 0.2s ease-out;
}

:global(:root[data-theme='dark']) .primary-btn:hover:not(:disabled),
:global(.dark) .primary-btn:hover:not(:disabled),
:global(:root[data-theme='dark']) .send-btn:hover:not(:disabled),
:global(.dark) .send-btn:hover:not(:disabled) {
	transform: translateY(-1px);
	box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
	background: linear-gradient(135deg, #2563eb 0%, #60a5fa 100%);
}

:global(:root[data-theme='dark']) .message-bubble :deep(blockquote),
:global(.dark) .message-bubble :deep(blockquote) {
	color: #cbd5e1;
}

:global(:root[data-theme='dark']) .message-bubble :deep(pre),
:global(.dark) .message-bubble :deep(pre) {
	background: #020617;
}

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
</style>

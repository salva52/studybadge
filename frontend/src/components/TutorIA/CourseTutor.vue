<template>
	<!-- Floating Toggle Button -->
	<button v-if="!isOpen" @click="isOpen = true" class="tutor-floating-btn shadow-xl hover:scale-105 transition-transform group">
		<Bot class="w-7 h-7 text-white" />
		<span class="absolute right-full mr-3 bg-gray-800 text-white text-xs px-2.5 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 whitespace-nowrap transition-opacity shadow-lg">
			TutorIA del Curso
		</span>
	</button>

	<!-- Floating Window -->
	<Transition name="tutor-window">
		<div v-show="isOpen" class="tutor-floating-window shadow-2xl" :style="{ width: windowWidth + 'px', height: windowHeight + 'px', right: windowX + 'px', bottom: windowY + 'px' }" ref="tutorWindow">
			
			<!-- Resize Handles (Bordes) -->
			<div class="absolute top-0 left-0 w-full h-2 cursor-ns-resize z-[100]" @mousedown="startResize($event, 'top')"></div>
			<div class="absolute top-0 left-0 w-2 h-full cursor-ew-resize z-[100]" @mousedown="startResize($event, 'left')"></div>
			<div class="absolute top-0 left-0 w-4 h-4 cursor-nwse-resize z-[101]" @mousedown="startResize($event, 'both')"></div>

			<!-- Header (Draggable) -->
			<div class="tutor-header" @mousedown="startDrag">
				<div class="flex items-center gap-2.5 min-w-0 flex-1">
					<div class="bg-white/20 p-1.5 rounded-lg text-white shrink-0">
						<Bot class="w-5 h-5" />
					</div>
					<div class="min-w-0 pr-2">
						<div class="text-sm font-bold text-white truncate">TutorIA</div>
						<div class="text-[10px] text-blue-100 truncate opacity-90">{{ courseTitle }}</div>
					</div>
				</div>
				<div class="flex items-center gap-1.5 shrink-0">
					<button @click.stop="toggleExpand" class="tutor-header-btn" title="Agrandar">
						<Maximize2 v-if="!isExpanded" class="w-3.5 h-3.5" />
						<Minimize2 v-else class="w-3.5 h-3.5" />
					</button>
					<button @click.stop="isOpen = false" class="tutor-header-btn" title="Cerrar">
						<X class="w-4 h-4" />
					</button>
				</div>
			</div>

			<!-- Messages -->
			<div class="flex-1 overflow-y-auto p-4 flex flex-col gap-4 bg-gray-50 dark:bg-gray-900" ref="messagesContainer">
				<div class="tutor-msg-ai shadow-sm">
					👋 Soy el tutor de <strong>{{ courseTitle }}</strong>.<br>
					¿Tienes alguna duda sobre la lección actual?
				</div>

				<div v-for="(msg, i) in messages" :key="i" :class="msg.role === 'user' ? 'tutor-msg-user' : 'tutor-msg-ai'">
					<div v-if="msg.role === 'model'" class="flex items-center gap-1.5 mb-1.5 text-indigo-600 dark:text-indigo-400 font-bold text-xs">
						<Sparkles class="w-3.5 h-3.5" />
						TutorIA
					</div>
					
					<!-- Images in message -->
					<div v-if="msg.images_base64 && msg.images_base64.length" class="flex flex-wrap gap-2 mb-2">
						<img v-for="(img, idx) in msg.images_base64" :key="idx" :src="`data:image/jpeg;base64,${img}`" class="rounded-lg max-h-32 object-contain border border-gray-200 dark:border-gray-700 shadow-sm" />
					</div>

					<div v-html="formatMessage(msg.content)" class="prose prose-sm max-w-none text-current"></div>
				</div>

				<div v-if="isLoading" class="tutor-typing self-start mt-1 p-3 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm">
					<span></span><span></span><span></span>
				</div>
			</div>

			<!-- Footer Input -->
			<div class="tutor-footer p-3 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 z-10">
				<!-- Attached Images Preview -->
				<div v-if="attachedImages.length" class="flex flex-wrap gap-2 mb-2 p-2 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
					<div v-for="(img, idx) in attachedImages" :key="idx" class="relative group">
						<img :src="img" class="h-14 w-14 object-cover rounded-lg shadow-sm border border-gray-200 dark:border-gray-600" />
						<button @click="removeImage(idx)" class="absolute -top-2 -right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-all shadow-md">
							<X class="w-3 h-3" />
						</button>
					</div>
				</div>

				<div class="flex gap-2 items-end relative">
					<div class="flex-1 relative bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-100 dark:focus-within:ring-indigo-900/30 transition-all">
						<textarea 
							ref="chatInput"
							v-model="inputMessage" 
							placeholder="Pregunta algo (Shift+Enter para saltar línea)..." 
							@keydown="handleKeydown"
							@paste="handlePaste"
							@dragover.prevent
							@drop="handleDrop"
							:disabled="isLoading"
							rows="1"
							class="w-full bg-transparent border-none outline-none resize-none pl-3 pr-10 py-3 text-sm max-h-[140px] scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600"
							@input="autoResize"
						></textarea>
						
						<!-- Upload Button -->
						<div class="absolute right-1.5 bottom-1.5">
							<input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" multiple class="hidden" />
							<button @click="$refs.fileInput.click()" class="p-1.5 text-gray-400 hover:text-indigo-500 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors" title="Adjuntar imagen">
								<Image class="w-5 h-5" />
							</button>
						</div>
					</div>
					
					<button class="tutor-send-btn flex-shrink-0" @click="sendMessage" :disabled="(!inputMessage.trim() && !attachedImages.length) || isLoading">
						<Send class="w-4 h-4 ml-0.5" />
					</button>
				</div>
				
				<div class="flex justify-between items-center mt-2 px-1">
					<div class="text-[10px] text-gray-400 font-medium">Ctrl+V para pegar imágenes</div>
					<div class="text-[10px] text-amber-600 font-semibold" v-if="unlimited">Plus: Ilimitado</div>
					<div class="text-[10px] text-gray-400 font-medium" v-else-if="remaining !== null">Restantes: {{ remaining }}</div>
				</div>
			</div>
		</div>
	</Transition>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { Bot, X, Maximize2, Minimize2, Send, Image, Sparkles } from 'lucide-vue-next'
import { call, toast } from 'frappe-ui'
import MarkdownIt from 'markdown-it'
import mk from 'markdown-it-katex'
import 'katex/dist/katex.min.css'
import DOMPurify from 'dompurify'

const props = defineProps({
	courseName: { type: String, required: true },
	courseTitle: { type: String, required: true },
	lessonTitle: { type: String, default: '' },
	lessonContent: { type: String, default: '' }
})

// Markdown setup
const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true }).use(mk)
const formatMessage = (text) => {
	if (!text) return ''
	return DOMPurify.sanitize(markdown.render(String(text)), {
		ADD_TAGS: ['math', 'mrow', 'mi', 'mo', 'mn', 'ms', 'mspace', 'mtext', 'menclose', 'merror', 'mfrac', 'mpadded', 'mphantom', 'mroot', 'mrow', 'msqrt', 'mstyle', 'mmultiscripts', 'mover', 'mprescripts', 'msub', 'msubsup', 'msup', 'munder', 'munderover', 'none', 'semantics', 'annotation', 'annotation-xml'],
		ADD_ATTR: ['mathvariant', 'mathcolor', 'mathsize', 'mathbackground', 'dir', 'display', 'class', 'style', 'aria-hidden']
	})
}

// Window state
const isOpen = ref(false)
const windowX = ref(24)
const windowY = ref(24)
const windowWidth = ref(380)
const windowHeight = ref(520)
const isExpanded = ref(false)
const savedDimensions = ref({ w: 380, h: 520, x: 24, y: 24 })

// Drag logic
const isDragging = ref(false)
let dragStartX = 0
let dragStartY = 0
let startX = 0
let startY = 0

const startDrag = (e) => {
	// Don't drag if clicking buttons
	if (e.target.closest('button')) return
	isDragging.value = true
	dragStartX = e.clientX
	dragStartY = e.clientY
	startX = windowX.value
	startY = windowY.value
	document.addEventListener('mousemove', onDrag)
	document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e) => {
	if (!isDragging.value) return
	const dx = e.clientX - dragStartX
	const dy = e.clientY - dragStartY
	windowX.value = Math.max(0, startX - dx)
	windowY.value = Math.max(0, startY - dy)
}

const stopDrag = () => {
	isDragging.value = false
	document.removeEventListener('mousemove', onDrag)
	document.removeEventListener('mouseup', stopDrag)
}

// Resize logic
const isResizing = ref(false)
let startW = 0
let startH = 0
let resizeMode = 'both'

const startResize = (e, mode = 'both') => {
	isResizing.value = true
	resizeMode = mode
	dragStartX = e.clientX
	dragStartY = e.clientY
	startW = windowWidth.value
	startH = windowHeight.value
	document.addEventListener('mousemove', onResize)
	document.addEventListener('mouseup', stopResize)
}

const onResize = (e) => {
	if (!isResizing.value) return
	const dx = e.clientX - dragStartX
	const dy = e.clientY - dragStartY
	
	if (resizeMode === 'both' || resizeMode === 'left') {
		windowWidth.value = Math.max(300, startW - dx)
	}
	if (resizeMode === 'both' || resizeMode === 'top') {
		windowHeight.value = Math.max(400, startH - dy)
	}
}

const stopResize = () => {
	isResizing.value = false
	document.removeEventListener('mousemove', onResize)
	document.removeEventListener('mouseup', stopResize)
}

const toggleExpand = () => {
	if (isExpanded.value) {
		windowWidth.value = savedDimensions.value.w
		windowHeight.value = savedDimensions.value.h
		windowX.value = savedDimensions.value.x
		windowY.value = savedDimensions.value.y
		isExpanded.value = false
	} else {
		savedDimensions.value = { w: windowWidth.value, h: windowHeight.value, x: windowX.value, y: windowY.value }
		windowWidth.value = Math.min(800, window.innerWidth - 48)
		windowHeight.value = window.innerHeight - 48
		windowX.value = 24
		windowY.value = 24
		isExpanded.value = true
	}
}

// Chat state
const inputMessage = ref('')
const isLoading = ref(false)
const messages = ref([])
const messagesContainer = ref(null)
const chatInput = ref(null)
const remaining = ref(null)
const unlimited = ref(false)

// Images state
const attachedImages = ref([])

onMounted(() => {
	call('lms.lms.subscriptions.get_plus_status')
		.then((res) => {
			unlimited.value = !!res.active
		})
		.catch(() => {})
})

watch(() => props.lessonTitle, () => {
	messages.value = []
})

const scrollToBottom = () => {
	if (messagesContainer.value) {
		messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
	}
}

const autoResize = () => {
	const el = chatInput.value
	if (el) {
		el.style.height = 'auto'
		el.style.height = Math.min(el.scrollHeight, 140) + 'px'
	}
}

const handleKeydown = (e) => {
	if (e.key === 'Enter' && !e.shiftKey) {
		e.preventDefault()
		sendMessage()
	}
}

// Image handling
const processImageFile = (file) => {
	if (!file.type.startsWith('image/')) {
		toast.error('Solo se permiten imágenes')
		return
	}
	const reader = new FileReader()
	reader.onload = (e) => {
		attachedImages.value.push(e.target.result)
	}
	reader.readAsDataURL(file)
}

const handlePaste = (e) => {
	const items = e.clipboardData?.items
	if (!items) return
	for (let item of items) {
		if (item.type.indexOf('image') === 0) {
			const file = item.getAsFile()
			if (file) processImageFile(file)
		}
	}
}

const handleDrop = (e) => {
	const items = e.dataTransfer?.items
	if (!items) return
	for (let item of items) {
		if (item.type.indexOf('image') === 0) {
			const file = item.getAsFile()
			if (file) processImageFile(file)
		}
	}
}

const handleFileUpload = (e) => {
	const files = e.target.files
	if (!files) return
	for (let file of files) {
		processImageFile(file)
	}
	e.target.value = ''
}

const removeImage = (idx) => {
	attachedImages.value.splice(idx, 1)
}

const sendMessage = async () => {
	if ((!inputMessage.value.trim() && !attachedImages.value.length) || isLoading.value) return

	const msgText = inputMessage.value
	const msgImages = [...attachedImages.value]
	
	inputMessage.value = ''
	attachedImages.value = []
	
	if (chatInput.value) {
		chatInput.value.style.height = 'auto'
	}
	
	const base64Images = msgImages.map(img => img.split(',')[1])
	
	messages.value.push({ role: 'user', content: msgText, images_base64: base64Images })
	isLoading.value = true
	
	await nextTick()
	scrollToBottom()

	const imagesPayload = JSON.stringify(base64Images)

	const historyForApi = messages.value.slice(-6).map(m => ({
		role: m.role === 'model' ? 'assistant' : m.role,
		content: m.content
	}))

	call('studybadge_ai.ai_tutor.chat_with_course_tutor', {
		message: msgText,
		course_name: props.courseName,
		lesson_name: props.lessonTitle,
		lesson_content: props.lessonContent,
		images_base64: imagesPayload,
		history: JSON.stringify(historyForApi)
	}).then((res) => {
		messages.value.push({ role: 'model', content: res.reply })
		unlimited.value = !!res.unlimited
		if (res.remaining !== undefined) {
			remaining.value = res.remaining
		}
	}).catch((err) => {
		toast.error(err.messages?.[0] || 'Error de conexión con el tutor.')
		messages.value.push({ role: 'model', content: 'Lo siento, hubo un problema al procesar tu solicitud.' })
	}).finally(() => {
		isLoading.value = false
		nextTick(scrollToBottom)
	})
}
</script>

<style scoped>
.tutor-floating-btn {
	position: fixed;
	bottom: 24px;
	right: 24px;
	width: 64px;
	height: 64px;
	border-radius: 50%;
	background: linear-gradient(135deg, #4f46e5, #3b82f6);
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	z-index: 90;
	border: none;
}

.tutor-floating-window {
	position: fixed;
	background: white;
	border-radius: 20px;
	display: flex;
	flex-direction: column;
	z-index: 95;
	border: 1px solid rgba(229, 231, 235, 0.8);
}
:root.dark .tutor-floating-window {
	background: #1f2937;
	border-color: rgba(75, 85, 99, 0.5);
}

.tutor-header {
	background: linear-gradient(to right, #312e81, #4f46e5);
	padding: 14px 18px;
	display: flex;
	justify-content: space-between;
	align-items: center;
	cursor: grab;
	user-select: none;
	border-radius: 20px 20px 0 0;
}
.tutor-header:active {
	cursor: grabbing;
}

.tutor-header-btn {
	background: rgba(255, 255, 255, 0.15);
	border: none;
	color: white;
	width: 30px;
	height: 30px;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	transition: background 0.2s;
}
.tutor-header-btn:hover {
	background: rgba(255, 255, 255, 0.3);
}

.tutor-msg-user {
	align-self: flex-end;
	background: white;
	border: 1px solid #e5e7eb;
	color: #1f2937;
	border-radius: 20px 20px 4px 20px;
	padding: 10px 14px;
	max-width: 85%;
	font-size: 13px;
	box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
:root.dark .tutor-msg-user {
	background: #374151;
	border-color: #4b5563;
	color: #f9fafb;
}

.tutor-msg-ai {
	align-self: flex-start;
	background: white;
	border: 1px solid #e0e7ff;
	border-radius: 20px 20px 20px 4px;
	padding: 12px 14px;
	max-width: 90%;
	font-size: 13px;
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
}
:root.dark .tutor-msg-ai {
	background: #1f2937;
	border-color: rgba(99, 102, 241, 0.2);
	color: #f9fafb;
}

.tutor-send-btn {
	width: 44px;
	height: 44px;
	border-radius: 14px;
	background: linear-gradient(135deg, #4f46e5, #3b82f6);
	color: white;
	border: none;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.2s;
	box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
}
.tutor-send-btn:hover:not(:disabled) {
	transform: translateY(-1px);
	box-shadow: 0 6px 14px rgba(59, 130, 246, 0.4);
}
.tutor-send-btn:disabled {
	opacity: 0.5;
	background: #9ca3af;
	cursor: not-allowed;
	box-shadow: none;
}



.tutor-window-enter-active,
.tutor-window-leave-active {
	transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.tutor-window-enter-from,
.tutor-window-leave-to {
	opacity: 0;
	transform: scale(0.9) translateY(40px) translateX(20px);
}

.tutor-typing span {
	width: 6px;
	height: 6px;
	background: #6366f1;
	border-radius: 50%;
	display: inline-block;
	margin: 0 2px;
	animation: tutor-bounce 1.4s infinite;
}
.tutor-typing span:nth-child(2) { animation-delay: 0.2s; }
.tutor-typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes tutor-bounce {
	0%, 80%, 100% { transform: translateY(0); }
	40% { transform: translateY(-6px); }
}

/* Custom scrollbar for text area */
.scrollbar-thin::-webkit-scrollbar {
	width: 6px;
}
.scrollbar-thin::-webkit-scrollbar-track {
	background: transparent;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
	background-color: #cbd5e1;
	border-radius: 10px;
}
:root.dark .scrollbar-thin::-webkit-scrollbar-thumb {
	background-color: #475569;
}
</style>

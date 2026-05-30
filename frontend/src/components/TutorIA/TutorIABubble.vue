<template>
	<!-- Floating Bubble -->
	<div class="tutoria-bubble" @click="toggleChat" v-if="!isOpen">
		<Bot class="w-8 h-8 text-white" />
	</div>

	<!-- Chat Panel -->
	<Transition name="tutoria-slide">
		<div v-if="isOpen" class="tutoria-panel">
			<!-- Header -->
			<div class="tutoria-header">
				<div class="flex items-center gap-3 flex-1">
					<div class="bg-white/20 p-2 rounded-full">
						<Bot class="w-6 h-6 text-white" />
					</div>
					<div>
						<h3 class="font-bold text-white leading-tight m-0">TutorIA</h3>
						<span class="text-xs text-blue-100">Tu asistente inteligente</span>
					</div>
				</div>
				<div class="flex items-center gap-2">
					<button @click="clearHistory" class="text-white/80 hover:text-white transition-colors bg-transparent border-none cursor-pointer flex items-center justify-center p-1" title="Limpiar chat">
						<Trash2 class="w-4 h-4" />
					</button>
					<button @click="toggleChat" class="text-white/80 hover:text-white transition-colors bg-transparent border-none cursor-pointer flex items-center justify-center p-1" title="Cerrar">
						<X class="w-5 h-5" />
					</button>
				</div>
			</div>

			<!-- Messages -->
			<div class="tutoria-messages" ref="messagesContainer">
				<div class="tutoria-welcome">
					<div class="font-bold text-base mb-1 text-blue-900">¡Hola! 👋 Soy TutorIA</div>
					<div class="text-sm text-blue-800 mb-2">Tu asistente de aprendizaje en StudyBadge. Puedo ayudarte a:</div>
					<ul class="text-xs list-disc pl-4 space-y-1 text-blue-800 mb-2">
						<li>Elegir qué curso estudiar</li>
						<li>Resolver dudas paso a paso</li>
						<li>Explicarte temas difíciles con ejemplos</li>
						<li>Revisar imágenes o capturas relacionadas con tus clases</li>
					</ul>
					<div class="text-sm font-medium mt-2 text-blue-900">¿Qué quieres aprender hoy?</div>
				</div>

				<div v-for="(msg, i) in messages" :key="i" 
					:class="msg.role === 'user' ? 'tutoria-msg-user' : 'tutoria-msg-ai'">
					<div v-if="msg.role === 'model'" class="flex items-center gap-1.5 mb-1.5 text-blue-600 dark:text-blue-400 font-semibold text-xs">
						<Sparkles class="w-3.5 h-3.5" />
						TutorIA
					</div>
					<div v-if="msg.images_base64 && msg.images_base64.length > 0" class="flex flex-wrap gap-2 mb-2">
						<img v-for="(img, idx) in msg.images_base64" :key="idx" :src="'data:image/jpeg;base64,' + img" class="h-24 w-auto object-contain rounded-lg border border-gray-200 bg-white" />
					</div>
					<div v-html="formatMessage(msg.content)" class="prose prose-sm max-w-none text-current"></div>
				</div>

				<div v-if="isLoading" class="tutoria-typing self-start mt-2 p-3 bg-blue-50 rounded-2xl rounded-tl-sm border border-blue-100">
					<span></span><span></span><span></span>
				</div>
			</div>

			<!-- Footer -->
			<div class="tutoria-footer bg-white dark:bg-gray-800">
				<label class="tutoria-screen-toggle" style="display: none;">
					<input type="checkbox" v-model="readScreen" />
					<MonitorSmartphone class="w-3.5 h-3.5" />
					Leer texto de mi pantalla
				</label>

				<div v-if="selectedImages.length > 0" class="flex flex-wrap gap-2 mb-3 ml-2">
					<div v-for="(img, idx) in selectedImages" :key="idx" class="relative inline-block">
						<img :src="img.preview" class="h-16 w-16 object-cover rounded-lg border border-gray-200" />
						<button @click="removeImage(idx)" class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-0.5 cursor-pointer border-none flex items-center justify-center shadow-sm">
							<X class="w-3 h-3" />
						</button>
					</div>
				</div>

				<div class="tutoria-input-row">
					<input type="file" ref="fileInput" accept="image/png, image/jpeg, image/webp" multiple class="hidden" @change="handleImageUpload" />
					<button @click="$refs.fileInput.click()" class="text-gray-400 hover:text-blue-500 bg-transparent border-none cursor-pointer p-2 flex-shrink-0" title="Adjuntar imagen">
						<Image class="w-5 h-5" />
					</button>
					<textarea 
						v-model="inputMessage" 
						placeholder="Pregúntale a TutorIA..." 
						@keydown.enter.prevent="sendMessage"
						@paste="handlePaste"
						:disabled="isLoading"
						rows="1"
					></textarea>
					<button class="tutoria-send-btn" @click="sendMessage" :disabled="(!inputMessage.trim() && selectedImages.length === 0) || isLoading">
						<SendHorizontal class="w-5 h-5" />
					</button>
				</div>
					<div class="text-center text-[10px] text-amber-600 mt-2" v-if="unlimited">
						Plus: mensajes ilimitados
					</div>
					<div class="text-center text-[10px] text-gray-400 mt-2" v-else-if="remaining !== null">
						Mensajes restantes hoy: {{ remaining }}
					</div>
			</div>
		</div>
	</Transition>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Bot, X, SendHorizontal, MonitorSmartphone, Sparkles, Trash2, Image } from 'lucide-vue-next'
import { call, toast } from 'frappe-ui'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const isOpen = ref(false)
const inputMessage = ref('')
const isLoading = ref(false)
const readScreen = ref(true)
const messages = ref([])
const messagesContainer = ref(null)
const remaining = ref(null)
const unlimited = ref(false)

const selectedImages = ref([])
const totalImagesSent = ref(0)
const fileInput = ref(null)

onMounted(() => {
	checkConfig()
})

watch(messages, () => {
	scrollToBottom()
}, { deep: true })

const checkConfig = () => {
		call('studybadge_ai.ai_tutor.get_tutor_config')
			.then(res => {
				remaining.value = res.remaining
				unlimited.value = !!res.unlimited
				if (res.history) {
				try {
					const parsed = JSON.parse(res.history)
					if (Array.isArray(parsed) && parsed.length > 0) {
						messages.value = parsed
						
						let count = 0
						parsed.forEach(m => {
							if (m.images_base64 && Array.isArray(m.images_base64)) {
								count += m.images_base64.length
							}
						})
						totalImagesSent.value = count
						
						nextTick(scrollToBottom)
					}
				} catch (e) {
					console.error('Error parsing history from DB')
				}
			}
		})
}

const toggleChat = async () => {
	isOpen.value = !isOpen.value
	if (isOpen.value) {
		await nextTick()
		scrollToBottom()
	}
}

const formatMessage = (text) => {
	if (!text) return ''
	const html = marked(text)
	return DOMPurify.sanitize(html)
}

const getScreenText = () => {
	if (!readScreen.value) return ''
	try {
		const proseElement = document.querySelector('.ProseMirror') || document.querySelector('.prose')
		let text = proseElement ? proseElement.innerText : document.body.innerText
		return text.substring(0, 3000)
	} catch {
		return ''
	}
}

const scrollToBottom = () => {
	if (messagesContainer.value) {
		messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
	}
}

const addImageFile = (file) => {
	if (!file.type.startsWith('image/')) {
		toast.error('Solo puedes subir imágenes (PNG, JPG, WEBP)')
		return
	}
	
	if (selectedImages.value.length >= 5) {
		toast.error('Solo puedes adjuntar hasta 5 imágenes por mensaje.')
		return
	}
	
	if (totalImagesSent.value + selectedImages.value.length >= 10) {
		toast.error('Has alcanzado el límite de 10 imágenes por conversación.')
		return
	}
	
	const reader = new FileReader()
	reader.onload = (e) => {
		selectedImages.value.push({
			preview: e.target.result,
			base64: e.target.result.split(',')[1]
		})
	}
	reader.readAsDataURL(file)
}

const handleImageUpload = (event) => {
	const files = event.target.files
	if (!files) return
	
	Array.from(files).forEach(file => addImageFile(file))
	if (fileInput.value) fileInput.value.value = ''
}

const handlePaste = (event) => {
	const items = event.clipboardData?.items
	if (!items) return
	
	for (let i = 0; i < items.length; i++) {
		if (items[i].type.indexOf('image') !== -1) {
			const blob = items[i].getAsFile()
			addImageFile(blob)
		}
	}
}

const removeImage = (index) => {
	selectedImages.value.splice(index, 1)
}

const clearHistory = () => {
	if (!confirm('¿Estás seguro de que quieres borrar el historial de este chat?')) return
	
	call('studybadge_ai.ai_tutor.clear_tutor_history').then(() => {
		messages.value = []
		totalImagesSent.value = 0
		toast.success('Chat borrado')
	}).catch(() => {
		toast.error('Error al borrar chat')
	})
}

const sendMessage = async () => {
	if ((!inputMessage.value.trim() && selectedImages.value.length === 0) || isLoading.value) return

	const msgText = inputMessage.value
	const imgsBase64 = selectedImages.value.map(img => img.base64)
	
	inputMessage.value = ''
	selectedImages.value = []
	if (fileInput.value) fileInput.value.value = ''
	
	messages.value.push({ role: 'user', content: msgText, images_base64: imgsBase64 })
	totalImagesSent.value += imgsBase64.length
	isLoading.value = true
	
	await nextTick()
	scrollToBottom()

	const screenText = getScreenText()
	
	// Prepare history for API (last 10 messages before this new one)
	const historyForApi = messages.value.slice(0, -1).slice(-10).map(m => ({
		role: m.role === 'model' ? 'assistant' : m.role,
		content: m.content,
		images_base64: m.images_base64
	}))

	call('studybadge_ai.ai_tutor.chat_with_tutor', {
		message: msgText,
		screen_text: screenText,
		images_base64: JSON.stringify(imgsBase64),
		history: JSON.stringify(historyForApi)
		}).then((res) => {
			messages.value.push({ role: 'model', content: res.reply })
			unlimited.value = !!res.unlimited
			if (res.remaining !== undefined) {
				remaining.value = res.remaining
			}
	}).catch((err) => {
		toast.error(err.messages?.[0] || 'Ocurrió un error al contactar al tutor.')
		messages.value.push({ role: 'model', content: 'Lo siento, hubo un problema al procesar tu solicitud. Por favor intenta de nuevo.' })
	}).finally(() => {
		isLoading.value = false
		nextTick(scrollToBottom)
	})
}
</script>

<style scoped>
.tutoria-bubble {
	position: fixed;
	bottom: 24px;
	right: 24px;
	width: 64px;
	height: 64px;
	border-radius: 50%;
	background: linear-gradient(135deg, var(--sb-dark), var(--sb-primary));
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	box-shadow: 0 4px 20px rgba(0, 123, 255, 0.4);
	z-index: 9999;
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tutoria-bubble:hover {
	transform: scale(1.05) translateY(-4px);
	box-shadow: 0 8px 25px rgba(0, 123, 255, 0.5);
}

.tutoria-bubble::before {
	content: '';
	position: absolute;
	width: 100%;
	height: 100%;
	border-radius: 50%;
	border: 2px solid var(--sb-primary);
	animation: tutoria-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.tutoria-panel {
	position: fixed;
	bottom: 100px;
	right: 24px;
	width: 380px;
	height: 580px;
	max-height: calc(100vh - 120px);
	background: white;
	border-radius: 24px;
	box-shadow: 0 12px 48px rgba(6, 27, 73, 0.15);
	display: flex;
	flex-direction: column;
	overflow: hidden;
	z-index: 9998;
	border: 1px solid rgba(0, 123, 255, 0.1);
}

.tutoria-header {
	background: linear-gradient(135deg, var(--sb-dark), #0A2352);
	padding: 16px 20px;
	display: flex;
	align-items: center;
	justify-content: space-between;
}

.tutoria-messages {
	flex: 1;
	overflow-y: auto;
	padding: 20px;
	display: flex;
	flex-direction: column;
	gap: 16px;
	background: #f9fafb;
}

.tutoria-welcome {
	background: linear-gradient(135deg, #eff6ff, #dbeafe);
	color: #1e3a8a;
	padding: 16px;
	border-radius: 16px;
	font-size: 14px;
	line-height: 1.5;
	border: 1px solid #bfdbfe;
}

.tutoria-msg-user {
	align-self: flex-end;
	background: white;
	border: 1px solid #e5e7eb;
	color: #1f2937;
	border-radius: 20px 20px 4px 20px;
	padding: 12px 16px;
	max-width: 85%;
	font-size: 14px;
	line-height: 1.5;
	box-shadow: 0 2px 4px rgba(0,0,0,0.02);
	animation: tutoria-fade-in 0.3s ease-out;
}

.tutoria-msg-ai {
	align-self: flex-start;
	background: white;
	border: 1px solid #e0e7ff;
	border-radius: 20px 20px 20px 4px;
	padding: 14px 16px;
	max-width: 90%;
	font-size: 14px;
	line-height: 1.5;
	box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
	animation: tutoria-fade-in 0.3s ease-out;
}

.tutoria-footer {
	padding: 16px;
	border-top: 1px solid #f3f4f6;
}

.tutoria-screen-toggle {
	display: flex;
	align-items: center;
	gap: 8px;
	font-size: 12px;
	color: #6b7280;
	margin-bottom: 12px;
	cursor: pointer;
	user-select: none;
	font-weight: 500;
}

.tutoria-input-row {
	display: flex;
	gap: 10px;
	align-items: flex-end;
}

.tutoria-input-row textarea {
	flex: 1;
	resize: none;
	background: #f3f4f6;
	border: 1px solid transparent;
	border-radius: 16px;
	padding: 12px 16px;
	font-size: 14px;
	font-family: inherit;
	outline: none;
	min-height: 44px;
	max-height: 120px;
	transition: all 0.2s;
}

.tutoria-input-row textarea:focus {
	background: white;
	border-color: var(--sb-primary);
	box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.1);
}

.tutoria-send-btn {
	width: 44px;
	height: 44px;
	border-radius: 16px;
	background: linear-gradient(135deg, var(--sb-primary), var(--sb-medium));
	color: white;
	border: none;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.2s;
	flex-shrink: 0;
}

.tutoria-send-btn:hover:not(:disabled) {
	transform: scale(1.05);
	box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.tutoria-send-btn:disabled {
	opacity: 0.5;
	cursor: not-allowed;
	background: #9ca3af;
}

.tutoria-typing span {
	width: 6px;
	height: 6px;
	background: var(--sb-primary);
	border-radius: 50%;
	display: inline-block;
	margin: 0 2px;
	animation: tutoria-bounce 1.4s infinite;
}
.tutoria-typing span:nth-child(2) { animation-delay: 0.2s; }
.tutoria-typing span:nth-child(3) { animation-delay: 0.4s; }

/* Transitions */
.tutoria-slide-enter-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.tutoria-slide-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 1, 1); }
.tutoria-slide-enter-from, .tutoria-slide-leave-to {
	opacity: 0;
	transform: translateY(20px) scale(0.95) !important;
}

@media (max-width: 640px) {
	.tutoria-panel {
		width: calc(100vw - 32px);
		height: calc(100vh - 120px);
		bottom: 100px;
		right: 16px;
	}
	.tutoria-bubble {
		bottom: 84px;
		right: 16px;
		width: 56px;
		height: 56px;
	}
}
</style>

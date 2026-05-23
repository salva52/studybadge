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
				<button @click="toggleChat" class="text-white/80 hover:text-white transition-colors bg-transparent border-none cursor-pointer">
					<X class="w-5 h-5" />
				</button>
			</div>

			<!-- Messages -->
			<div class="tutoria-messages" ref="messagesContainer">
				<div class="tutoria-welcome">
					¡Hola! 👋 Soy TutorIA, tu asistente inteligente. ¿No sabes qué aprender? ¿Tienes alguna duda? ¡Estoy aquí para ayudarte!
				</div>

				<div v-for="(msg, i) in messages" :key="i" 
					:class="msg.role === 'user' ? 'tutoria-msg-user' : 'tutoria-msg-ai'">
					<div v-if="msg.role === 'model'" class="flex items-center gap-1.5 mb-1.5 text-blue-600 dark:text-blue-400 font-semibold text-xs">
						<Sparkles class="w-3.5 h-3.5" />
						TutorIA
					</div>
					<div v-html="formatMessage(msg.content)" class="prose prose-sm max-w-none text-current"></div>
				</div>

				<div v-if="isLoading" class="tutoria-typing self-start mt-2 p-3 bg-blue-50 rounded-2xl rounded-tl-sm border border-blue-100">
					<span></span><span></span><span></span>
				</div>
			</div>

			<!-- Footer -->
			<div class="tutoria-footer bg-white dark:bg-gray-800">
				<label class="tutoria-screen-toggle">
					<input type="checkbox" v-model="readScreen" />
					<MonitorSmartphone class="w-3.5 h-3.5" />
					Leer texto de mi pantalla
				</label>

				<div class="tutoria-input-row">
					<textarea 
						v-model="inputMessage" 
						placeholder="Pregúntale a TutorIA..." 
						@keydown.enter.prevent="sendMessage"
						:disabled="isLoading"
						rows="1"
					></textarea>
					<button class="tutoria-send-btn" @click="sendMessage" :disabled="!inputMessage.trim() || isLoading">
						<SendHorizontal class="w-5 h-5" />
					</button>
				</div>
				<div class="text-center text-[10px] text-gray-400 mt-2" v-if="remaining !== null">
					Mensajes restantes hoy: {{ remaining }}
				</div>
			</div>
		</div>
	</Transition>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Bot, X, SendHorizontal, MonitorSmartphone, Sparkles } from 'lucide-vue-next'
import { call, toast } from 'frappe-ui'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const isOpen = ref(false)
const inputMessage = ref('')
const isLoading = ref(false)
const readScreen = ref(false)
const messages = ref([])
const messagesContainer = ref(null)
const remaining = ref(null)

onMounted(() => {
	loadHistory()
	checkConfig()
})

watch(messages, () => {
	saveHistory()
	scrollToBottom()
}, { deep: true })

const checkConfig = () => {
	call('studybadge_ai.ai_tutor.get_tutor_config')
		.then(res => {
			remaining.value = res.remaining
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

const saveHistory = () => {
	if (messages.value.length > 0) {
		localStorage.setItem('tutoria_chat_history', JSON.stringify(messages.value.slice(-50)))
	}
}

const loadHistory = () => {
	const saved = localStorage.getItem('tutoria_chat_history')
	if (saved) {
		try {
			messages.value = JSON.parse(saved)
		} catch (e) {
			console.error('Error parsing chat history')
		}
	}
}

const sendMessage = async () => {
	if (!inputMessage.value.trim() || isLoading.value) return

	const msgText = inputMessage.value
	inputMessage.value = ''
	
	messages.value.push({ role: 'user', content: msgText })
	isLoading.value = true
	
	await nextTick()
	scrollToBottom()

	const screenText = getScreenText()
	
	// Prepare history for API (last 10 messages)
	const historyForApi = messages.value.slice(-10).map(m => ({
		role: m.role === 'model' ? 'assistant' : m.role,
		content: m.content
	}))

	call('studybadge_ai.ai_tutor.chat_with_tutor', {
		message: msgText,
		screen_text: screenText,
		history: JSON.stringify(historyForApi)
	}).then((res) => {
		messages.value.push({ role: 'model', content: res.reply })
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
		height: calc(100vh - 100px);
		bottom: 80px;
		right: 16px;
	}
	.tutoria-bubble {
		bottom: 16px;
		right: 16px;
		width: 56px;
		height: 56px;
	}
}
</style>

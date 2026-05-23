<template>
	<div class="course-tutor mt-6">
		<button @click="isOpen = !isOpen" class="course-tutor-toggle w-full flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 transition-all hover:border-blue-300">
			<div class="flex items-center gap-3">
				<div class="bg-blue-50 dark:bg-blue-900/30 p-2 rounded-xl text-blue-600 dark:text-blue-400">
					<Bot class="w-5 h-5" />
				</div>
				<span class="font-semibold text-ink-gray-9">TutorIA del Curso</span>
			</div>
			<ChevronDown v-if="!isOpen" class="w-5 h-5 text-gray-400" />
			<ChevronUp v-if="isOpen" class="w-5 h-5 text-gray-400" />
		</button>

		<Transition name="course-tutor-expand">
			<div v-if="isOpen" class="course-tutor-chat mt-3 bg-white dark:bg-gray-800 rounded-2xl shadow-sb-soft border border-gray-100 dark:border-gray-700 overflow-hidden flex flex-col h-[500px]">
				<!-- Header -->
				<div class="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 px-5 py-4 border-b border-blue-100 dark:border-gray-700">
					<div class="text-sm font-semibold text-blue-900 dark:text-blue-100 line-clamp-1">
						{{ courseTitle }}
					</div>
					<div class="text-xs text-blue-600 dark:text-blue-400 mt-0.5">
						Pregunta sobre esta lección
					</div>
				</div>

				<!-- Messages -->
				<div class="flex-1 overflow-y-auto p-4 flex flex-col gap-4 bg-gray-50/50 dark:bg-gray-900/20" ref="messagesContainer">
					<div class="course-tutor-welcome bg-white dark:bg-gray-800 border border-blue-100 dark:border-blue-900/50 p-4 rounded-2xl text-sm text-ink-gray-9 shadow-sm">
						👋 Soy el tutor de <strong>{{ courseTitle }}</strong>.<br>
						¿Tienes alguna duda sobre la lección actual?
					</div>

					<div v-for="(msg, i) in messages" :key="i" 
						:class="msg.role === 'user' ? 'tutoria-msg-user' : 'course-tutor-msg-ai'">
						<div v-if="msg.role === 'model'" class="flex items-center gap-1.5 mb-1.5 text-blue-600 dark:text-blue-400 font-semibold text-xs">
							<Sparkles class="w-3.5 h-3.5" />
							TutorIA
						</div>
						<div v-html="formatMessage(msg.content)" class="prose prose-sm max-w-none text-current"></div>
					</div>

					<div v-if="isLoading" class="tutoria-typing self-start mt-1 p-3 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700">
						<span></span><span></span><span></span>
					</div>
				</div>

				<!-- Footer -->
				<div class="p-4 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700">
					<div class="tutoria-input-row">
						<textarea 
							v-model="inputMessage" 
							placeholder="Pregunta sobre la lección..." 
							@keydown.enter.prevent="sendMessage"
							:disabled="isLoading"
							rows="1"
						></textarea>
						<button class="tutoria-send-btn" @click="sendMessage" :disabled="!inputMessage.trim() || isLoading">
							<SendHorizontal class="w-5 h-5" />
						</button>
					</div>
					<div class="text-center text-[10px] text-gray-400 mt-2" v-if="remaining !== null">
						Mensajes restantes en este curso hoy: {{ remaining }}
					</div>
				</div>
			</div>
		</Transition>
	</div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { Bot, ChevronDown, ChevronUp, SendHorizontal, Sparkles } from 'lucide-vue-next'
import { call, toast } from 'frappe-ui'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
	courseName: { type: String, required: true },
	courseTitle: { type: String, required: true },
	lessonTitle: { type: String, default: '' },
	lessonContent: { type: String, default: '' }
})

const isOpen = ref(true)
const inputMessage = ref('')
const isLoading = ref(false)
const messages = ref([])
const messagesContainer = ref(null)
const remaining = ref(null)

// Reset messages when lesson changes
watch(() => props.lessonTitle, () => {
	messages.value = []
})

const formatMessage = (text) => {
	if (!text) return ''
	const html = marked(text)
	return DOMPurify.sanitize(html)
}

const scrollToBottom = () => {
	if (messagesContainer.value) {
		messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
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

	const historyForApi = messages.value.slice(-6).map(m => ({
		role: m.role === 'model' ? 'assistant' : m.role,
		content: m.content
	}))

	call('studybadge_ai.ai_tutor.chat_with_course_tutor', {
		message: msgText,
		course_name: props.courseName,
		lesson_name: props.lessonTitle,
		lesson_content: props.lessonContent,
		history: JSON.stringify(historyForApi)
	}).then((res) => {
		messages.value.push({ role: 'model', content: res.reply })
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
.course-tutor-expand-enter-active,
.course-tutor-expand-leave-active {
	transition: all 0.3s ease;
	transform-origin: top;
}
.course-tutor-expand-enter-from,
.course-tutor-expand-leave-to {
	opacity: 0;
	transform: scaleY(0.95);
}

.tutoria-msg-user {
	align-self: flex-end;
	background: white;
	border: 1px solid #e5e7eb;
	color: #1f2937;
	border-radius: 20px 20px 4px 20px;
	padding: 10px 14px;
	max-width: 85%;
	font-size: 13px;
	box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.course-tutor-msg-ai {
	align-self: flex-start;
	background: white;
	border: 1px solid #e0e7ff;
	border-radius: 20px 20px 20px 4px;
	padding: 12px 14px;
	max-width: 90%;
	font-size: 13px;
	box-shadow: 0 4px 12px rgba(59, 130, 246, 0.05);
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
	padding: 10px 14px;
	font-size: 13px;
	font-family: inherit;
	outline: none;
	min-height: 40px;
	max-height: 120px;
	transition: all 0.2s;
}

.tutoria-input-row textarea:focus {
	background: white;
	border-color: var(--sb-primary);
	box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.1);
}

.tutoria-send-btn {
	width: 40px;
	height: 40px;
	border-radius: 12px;
	background: linear-gradient(135deg, var(--sb-primary), var(--sb-medium));
	color: white;
	border: none;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-shrink: 0;
}
.tutoria-send-btn:disabled {
	opacity: 0.5;
	background: #9ca3af;
}

.tutoria-typing span {
	width: 5px;
	height: 5px;
	background: var(--sb-primary);
	border-radius: 50%;
	display: inline-block;
	margin: 0 2px;
	animation: tutoria-bounce 1.4s infinite;
}
.tutoria-typing span:nth-child(2) { animation-delay: 0.2s; }
.tutoria-typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes tutoria-bounce {
	0%, 80%, 100% { transform: translateY(0); }
	40% { transform: translateY(-6px); }
}
</style>

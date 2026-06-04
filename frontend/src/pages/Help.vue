<template>
	<div class="help-page min-h-screen pb-16">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b help-header px-4 py-3 sm:px-6 shadow-sm"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
		</header>

		<!-- Hero Section -->
		<div class="help-hero relative overflow-hidden text-center text-white py-16 px-6 sm:py-24">
			<!-- Subtle background decoration -->
			<div class="absolute -top-24 -right-24 w-[500px] h-[500px] bg-blue-500 opacity-20 blur-[80px] rounded-full"></div>
			<div class="absolute top-1/2 -left-24 w-[400px] h-[400px] bg-amber-500 opacity-10 blur-[80px] rounded-full"></div>
			
			<div class="mx-auto max-w-5xl relative z-10">
				<div class="flex flex-col items-center gap-6">
					<div class="rounded-2xl bg-white/10 p-5 ring-1 ring-white/20 backdrop-blur-md shadow-2xl">
						<LifeBuoy class="size-12 sm:size-14 stroke-1.5 text-blue-300 drop-shadow-md" />
					</div>
					<div>
						<h1 class="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight mb-4">
							Centro de <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 via-cyan-200 to-blue-200">Ayuda</span>
						</h1>
						<p class="mt-6 text-xl sm:text-2xl text-blue-100/90 max-w-3xl mx-auto font-medium leading-relaxed">
							{{ __('Estamos aquí para apoyarte. Encuentra respuestas rápidas o contacta con nuestro equipo de soporte.') }}
						</p>
					</div>
				</div>
			</div>
		</div>

		<div class="mx-auto max-w-5xl px-5 py-12 -mt-8 relative z-20">
			<div class="space-y-12">
				
				<!-- Soporte Rápido -->
				<section>
					<h2 class="text-2xl sm:text-3xl font-extrabold help-text-primary mb-6 flex items-center gap-3">
						<Headset class="size-7 text-blue-600" />
						{{ __('¿Cómo podemos ayudarte?') }}
					</h2>
					
					<div class="grid gap-6 md:grid-cols-2">
						<!-- IA Bubble Info -->
						<div class="help-card p-6 sm:p-8 relative overflow-hidden group cursor-pointer" @click="showSupportChat = true">
							<div class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity pointer-events-none">
								<Bot class="size-32 text-blue-600" />
							</div>
							<div class="rounded-2xl bg-blue-50 dark:bg-blue-900/20 w-fit p-3.5 mb-5 ring-1 ring-blue-100 dark:ring-blue-800/50">
								<Bot class="size-7 text-blue-600 dark:text-blue-400 stroke-1.5" />
							</div>
							<h3 class="text-xl sm:text-2xl font-bold help-text-primary mb-3">{{ __('Asistente de IA de Soporte') }}</h3>
							<p class="help-text-muted mb-6 text-sm sm:text-base leading-relaxed flex-grow">
								{{ __('Habla con nuestro asistente de IA con contexto de tus cursos, facturación y problemas técnicos. Exclusivo para soporte.') }}
							</p>
							<div class="mt-auto pt-5 border-t help-border flex flex-col items-start">
								<button class="help-btn-primary w-full sm:w-auto" @click.stop="showSupportChat = true">
									<Bot class="size-4" />
									{{ __('Abrir Chat de Soporte') }}
								</button>
							</div>
						</div>

						<!-- Correo Soporte -->
						<div class="help-card p-6 sm:p-8 relative overflow-hidden group">
							<div class="absolute top-0 right-0 p-4 opacity-[0.03] group-hover:opacity-10 transition-opacity pointer-events-none">
								<Mail class="size-32 text-gray-900 dark:text-white" />
							</div>
							<div class="rounded-2xl bg-gray-100 dark:bg-gray-800 w-fit p-3.5 mb-5 ring-1 ring-gray-200 dark:ring-gray-700">
								<Mail class="size-7 text-gray-700 dark:text-gray-300 stroke-1.5" />
							</div>
							<h3 class="text-xl sm:text-2xl font-bold help-text-primary mb-3">{{ __('Contacto Directo') }}</h3>
							<p class="help-text-muted mb-6 text-sm sm:text-base leading-relaxed flex-grow">
								{{ __('¿Tienes un problema complejo, un error técnico, o una consulta sobre facturación? Nuestro equipo humano está listo para revisar tu caso a detalle.') }}
							</p>
							<div class="mt-auto pt-5 border-t help-border flex flex-col items-start">
								<a
									href="mailto:soporte@studybadge.com"
									class="help-btn-primary w-full sm:w-auto"
								>
									<Mail class="size-4" />
									{{ __('Escribir a soporte@studybadge.com') }}
								</a>
								<p class="text-sm font-medium text-gray-500 dark:text-gray-400 mt-4 flex items-center gap-2">
									<Clock class="size-4" /> {{ __('Respondemos de Lunes a Viernes en menos de 24 horas.') }}
								</p>
							</div>
						</div>
					</div>
				</section>

				<!-- Documentación Básica -->
				<section class="pt-6">
					<h2 class="text-2xl sm:text-3xl font-extrabold help-text-primary mb-8 flex items-center gap-3">
						<BookOpen class="size-7 text-amber-500" />
						{{ __('Preguntas Frecuentes') }}
					</h2>

					<div class="grid gap-5">
						<div class="help-card p-6 sm:p-8">
							<div class="flex flex-col sm:flex-row items-start gap-5">
								<div class="rounded-2xl bg-blue-50 dark:bg-blue-900/20 p-3.5 shrink-0 ring-1 ring-blue-100 dark:ring-blue-800/50">
									<GraduationCap class="size-6 text-blue-600 dark:text-blue-400 stroke-2" />
								</div>
								<div>
									<h3 class="font-extrabold help-text-primary text-xl mb-3">{{ __('¿Cómo empiezo un curso?') }}</h3>
									<p class="text-base help-text-muted leading-relaxed">
										Para empezar un curso, dirígete a la pestaña <strong>Cursos</strong> en el menú lateral. Haz clic en el curso que te interese y luego en el botón <strong>"Inscribirse"</strong> o <strong>"Empezar Curso"</strong>. Todo tu progreso se guardará automáticamente en tu perfil.
									</p>
								</div>
							</div>
						</div>

						<div class="help-card p-6 sm:p-8">
							<div class="flex flex-col sm:flex-row items-start gap-5">
								<div class="rounded-2xl bg-amber-50 dark:bg-amber-900/20 p-3.5 shrink-0 ring-1 ring-amber-100 dark:ring-amber-800/50">
									<Award class="size-6 text-amber-600 dark:text-amber-400 stroke-2" />
								</div>
								<div>
									<h3 class="font-extrabold help-text-primary text-xl mb-3">{{ __('¿Cómo obtengo mis certificaciones?') }}</h3>
									<p class="text-base help-text-muted leading-relaxed">
										Una vez que completes al 100% todas las lecciones y evaluaciones de un curso, se generará tu certificado automáticamente si cumples con los requisitos. Puedes descargarlo e integrarlo a LinkedIn desde la sección <strong>Certificaciones</strong> o desde tu perfil público.
									</p>
								</div>
							</div>
						</div>

						<div class="help-card p-6 sm:p-8">
							<div class="flex flex-col sm:flex-row items-start gap-5">
								<div class="rounded-2xl bg-green-50 dark:bg-green-900/20 p-3.5 shrink-0 ring-1 ring-green-100 dark:ring-green-800/50">
									<User class="size-6 text-green-600 dark:text-green-400 stroke-2" />
								</div>
								<div>
									<h3 class="font-extrabold help-text-primary text-xl mb-3">{{ __('¿Por qué debo completar mi perfil?') }}</h3>
									<p class="text-base help-text-muted leading-relaxed">
										Completar tu perfil con una foto, titular y biografía te permite acceder a una mejor experiencia. Además, un perfil completo es un requisito previo para ciertas actividades dentro de la plataforma y te ayuda a destacar ante reclutadores en los Rankings.
									</p>
								</div>
							</div>
						</div>
					</div>
				</section>
				
			</div>
		</div>

		<!-- Dialog Support Chat -->
		<Dialog
			v-model="showSupportChat"
			:options="{
				title: __('Asistente de Soporte IA'),
				size: '3xl',
			}"
		>
			<template #body-content>
				<div class="flex flex-col h-[600px] bg-gray-50 dark:bg-gray-900 rounded-xl overflow-hidden border help-border -m-4">
					<!-- Chat Messages -->
					<div class="flex-1 overflow-y-auto p-5 space-y-5" ref="chatContainer">
						<div v-if="chatHistory.length === 0" class="text-center text-gray-500 mt-16">
							<div class="size-20 mx-auto mb-4 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
								<Bot class="size-10 text-blue-600 dark:text-blue-400" />
							</div>
							<h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2">{{ __('¡Hola! Soy el bot de soporte') }}</h3>
							<p class="max-w-md mx-auto text-sm text-gray-500 dark:text-gray-400">
								{{ __('¿Tienes dudas sobre tu facturación, certificados o cómo usar la plataforma? Escríbeme y estaré encantado de ayudarte. También puedes subir capturas de pantalla.') }}
							</p>
						</div>
						
						<div
							v-for="(msg, index) in chatHistory"
							:key="index"
							class="flex w-full"
							:class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
						>
							<div
								class="max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-3.5 shadow-sm"
								:class="
									msg.role === 'user'
										? 'bg-blue-600 text-white rounded-br-none'
										: 'bg-white dark:bg-gray-800 border help-border text-gray-800 dark:text-gray-200 rounded-bl-none'
								"
							>
								<!-- If image -->
								<div v-if="msg.images_base64 && msg.images_base64.length" class="mb-3 flex flex-wrap gap-2">
									<img
										v-for="(img, idx) in msg.images_base64"
										:key="idx"
										:src="'data:image/jpeg;base64,' + img"
										class="rounded-xl max-h-48 object-cover cursor-pointer border shadow-sm"
									/>
								</div>
								
								<div class="prose prose-sm dark:prose-invert max-w-none" v-html="renderMarkdown(msg.content)"></div>
							</div>
						</div>
						
						<div v-if="isTyping" class="flex justify-start w-full">
							<div class="bg-white dark:bg-gray-800 border help-border rounded-2xl rounded-bl-none px-5 py-3.5 flex items-center gap-3 shadow-sm">
								<Loader2 class="size-5 animate-spin text-blue-500" />
								<span class="text-sm font-medium text-gray-500">{{ __('Analizando tu consulta...') }}</span>
							</div>
						</div>
					</div>

					<!-- Chat Input -->
					<div class="bg-white dark:bg-gray-800 p-4 border-t help-border">
						<div v-if="previewImage" class="relative inline-block mb-3 ml-2">
							<img :src="previewImage" class="h-20 rounded-xl border object-cover shadow-sm" />
							<button @click="clearImage" class="absolute -top-2 -right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1 shadow-md transition-colors">
								<X class="size-3.5" />
							</button>
						</div>
						
						<div class="flex items-center gap-2">
							<button 
								class="p-2.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-xl transition-colors shrink-0"
								@click="triggerImageUpload"
								title="Adjuntar imagen"
							>
								<ImagePlus class="size-5" />
							</button>
							<input
								type="file"
								ref="fileInput"
								accept="image/*"
								class="hidden"
								@change="handleImageSelect"
							/>
							
							<input
								v-model="currentMessage"
								type="text"
								class="flex-1 bg-gray-100 dark:bg-gray-900 border border-transparent focus:border-blue-300 dark:focus:border-blue-700 rounded-xl px-4 py-3 focus:ring-4 focus:ring-blue-500/10 focus:outline-none text-sm transition-all text-gray-800 dark:text-gray-100"
								:placeholder="__('Escribe tu mensaje aquí...')"
								@keyup.enter="sendMessage"
								:disabled="isTyping"
							/>
							
							<button
								class="p-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 hover:shadow-lg hover:-translate-y-0.5 transition-all shrink-0 shadow-md"
								:class="{'opacity-50 cursor-not-allowed transform-none shadow-none hover:shadow-none': (!currentMessage.trim() && !previewImageBase64) || isTyping}"
								@click="sendMessage"
								:disabled="(!currentMessage.trim() && !previewImageBase64) || isTyping"
							>
								<Send class="size-5" />
							</button>
						</div>
					</div>
				</div>
			</template>
		</Dialog>

	</div>
</template>

<script setup>
import { computed, ref, nextTick } from 'vue'
import { Breadcrumbs, usePageMeta, Dialog, call } from 'frappe-ui'
import { marked } from 'marked'
import {
	LifeBuoy,
	Headset,
	Bot,
	Mail,
	Info,
	ExternalLink,
	BookOpen,
	GraduationCap,
	Award,
	User,
	Clock,
	Send,
	ImagePlus,
	X,
	Loader2
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()

const showSupportChat = ref(false)
const currentMessage = ref('')
const chatHistory = ref([])
const isTyping = ref(false)
const chatContainer = ref(null)
const fileInput = ref(null)
const previewImage = ref(null)
const previewImageBase64 = ref(null)

const renderMarkdown = (content) => {
	if (!content) return ''
	return marked(content)
}

const triggerImageUpload = () => {
	fileInput.value?.click()
}

const handleImageSelect = (event) => {
	const file = event.target.files[0]
	if (file) {
		const reader = new FileReader()
		reader.onload = (e) => {
			previewImage.value = e.target.result
			previewImageBase64.value = e.target.result.split(',')[1]
		}
		reader.readAsDataURL(file)
	}
}

const clearImage = () => {
	previewImage.value = null
	previewImageBase64.value = null
	if (fileInput.value) fileInput.value.value = ''
}

const scrollToBottom = async () => {
	await nextTick()
	if (chatContainer.value) {
		chatContainer.value.scrollTop = chatContainer.value.scrollHeight
	}
}

const sendMessage = async () => {
	const msgText = currentMessage.value.trim()
	const imgBase64 = previewImageBase64.value
	
	if (!msgText && !imgBase64) return
	if (isTyping.value) return

	// Add user message to UI
	const newMsg = {
		role: 'user',
		content: msgText,
	}
	if (imgBase64) {
		newMsg.images_base64 = [imgBase64]
	}
	
	chatHistory.value.push(newMsg)
	
	currentMessage.value = ''
	clearImage()
	isTyping.value = true
	await scrollToBottom()
	
	try {
		const response = await call('studybadge_ai.ai_support.chat_with_support', {
			message: msgText,
			images_base64: imgBase64 ? JSON.stringify([imgBase64]) : '[]',
			history: JSON.stringify(chatHistory.value.slice(0, -1)) // send previous history
		})
		
		if (response.reply) {
			chatHistory.value.push({
				role: 'assistant',
				content: response.reply
			})
		}
	} catch (error) {
		chatHistory.value.push({
			role: 'assistant',
			content: 'Hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.'
		})
	} finally {
		isTyping.value = false
		await scrollToBottom()
	}
}

const breadcrumbs = computed(() => [
	{
		label: __('Centro de Ayuda'),
		route: { name: 'Help' },
	},
])

usePageMeta(() => {
	return {
		title: __('Centro de Ayuda'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
/* ═══════════════════════════════════════
   TOKENS & THEME
   ═══════════════════════════════════════ */

.help-page {
	background: var(--sb-bg);
}

.help-header {
	background: var(--sb-white);
	border-color: rgba(6, 27, 73, 0.05);
}

:root[data-theme="dark"] .help-header {
	border-color: rgba(255, 255, 255, 0.05);
}

.help-border {
	border-color: rgba(6, 27, 73, 0.06);
}

:root[data-theme="dark"] .help-border {
	border-color: rgba(255, 255, 255, 0.06);
}

.help-text-primary { color: #111827; }
.help-text-muted { color: #4b5563; }
:root[data-theme="dark"] .help-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .help-text-muted { color: #9ca3af; }

/* ═══════════════════════════════════════
   HERO
   ═══════════════════════════════════════ */

.help-hero {
	background: linear-gradient(135deg, #061B49 0%, #0b2f73 50%, #0a2259 100%);
	box-shadow: inset 0 -1px 0 rgba(0,0,0,0.2);
}

/* ═══════════════════════════════════════
   CARDS
   ═══════════════════════════════════════ */

.help-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.06);
	border-radius: 24px;
	box-shadow: 0 4px 6px -1px rgba(6, 27, 73, 0.02), 0 2px 4px -2px rgba(6, 27, 73, 0.02);
	transition: all 0.25s ease;
	display: flex;
	flex-direction: column;
}

.help-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 12px 24px -4px rgba(6, 27, 73, 0.06), 0 8px 12px -6px rgba(6, 27, 73, 0.04);
	border-color: rgba(13, 110, 253, 0.2);
}

:root[data-theme="dark"] .help-card {
	border-color: rgba(255, 255, 255, 0.08);
	box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}

:root[data-theme="dark"] .help-card:hover {
	border-color: rgba(13, 110, 253, 0.4);
	box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.4), 0 8px 12px -6px rgba(0, 0, 0, 0.2);
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */

.help-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 12px 24px;
	border-radius: 14px;
	font-size: 15px;
	font-weight: 700;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 4px 12px rgba(13, 110, 253, 0.25);
	text-decoration: none;
}

.help-btn-primary:hover {
	transform: translateY(-1px);
	box-shadow: 0 6px 16px rgba(13, 110, 253, 0.35);
	color: #fff;
}

.help-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 12px 24px;
	border-radius: 14px;
	font-size: 15px;
	font-weight: 700;
	color: #374151;
	background: var(--sb-white);
	border: 2px solid rgba(0, 0, 0, 0.08);
	cursor: pointer;
	transition: all 0.15s ease;
	text-decoration: none;
}

.help-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.15);
}

:root[data-theme="dark"] .help-btn-outline {
	color: #e5e7eb;
	border-color: rgba(255, 255, 255, 0.12);
}

:root[data-theme="dark"] .help-btn-outline:hover {
	background: rgba(255, 255, 255, 0.05);
	border-color: rgba(255, 255, 255, 0.2);
}
</style>

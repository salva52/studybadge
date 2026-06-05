<template>
	<div class="help-page">
		<header class="help-header">
			<Breadcrumbs class="h-7 min-w-0" :items="breadcrumbs" />

			<a href="mailto:soporte@studybadge.com" class="help-header-mail">
				<Mail class="size-4" />
				<span>soporte@studybadge.com</span>
			</a>
		</header>

		<section class="help-hero">
			<div class="help-hero-inner">
				<div class="hero-icon">
					<LifeBuoy class="size-10 sm:size-12" />
				</div>

				<div class="hero-eyebrow">
					<Sparkles class="size-4" />
					{{ __('Soporte StudyBadge') }}
				</div>

				<h1>
					{{ __('Centro de Ayuda') }}
				</h1>

				<p>
					{{
						__(
							'Encuentra respuestas rápidas, resuelve problemas técnicos y contacta con nuestro equipo cuando necesites ayuda.'
						)
					}}
				</p>

				<div class="hero-actions">
					<button class="help-btn-light" @click="showSupportChat = true">
						<Bot class="size-4" />
						{{ __('Hablar con soporte IA') }}
					</button>

					<a href="mailto:soporte@studybadge.com" class="help-btn-ghost">
						<Mail class="size-4" />
						{{ __('Contactar soporte') }}
					</a>
				</div>
			</div>
		</section>

		<main class="help-main">
			<section class="help-section">
				<div class="section-head">
					<div>
						<div class="section-kicker">
							<Headset class="size-4" />
							{{ __('Soporte rápido') }}
						</div>
						<h2>{{ __('¿Cómo podemos ayudarte?') }}</h2>
						<p>
							{{
								__(
									'Elige la opción que mejor se adapte a tu consulta. Puedes hablar con la IA de soporte o escribirnos directamente.'
								)
							}}
						</p>
					</div>
				</div>

				<div class="support-grid">
					<article class="support-card support-card-primary" @click="showSupportChat = true">
						<div class="card-top">
							<div class="card-icon card-icon-blue">
								<Bot class="size-7" />
							</div>

							<div class="card-badge">
								{{ __('Rápido') }}
							</div>
						</div>

						<h3>{{ __('Asistente de IA de Soporte') }}</h3>

						<p>
							{{
								__(
									'Haz preguntas sobre cursos, certificados, facturación, errores técnicos o funcionamiento de la plataforma.'
								)
							}}
						</p>

						<div class="card-action">
							<button class="help-btn-primary" @click.stop="showSupportChat = true">
								<Bot class="size-4" />
								{{ __('Abrir chat') }}
							</button>
						</div>
					</article>

					<article class="support-card">
						<div class="card-top">
							<div class="card-icon card-icon-gold">
								<Mail class="size-7" />
							</div>

							<div class="card-badge card-badge-soft">
								{{ __('Humano') }}
							</div>
						</div>

						<h3>{{ __('Contacto directo') }}</h3>

						<p>
							{{
								__(
									'Para problemas complejos, pagos, errores con tu cuenta o consultas que necesitan revisión manual.'
								)
							}}
						</p>

						<div class="card-action">
							<a href="mailto:soporte@studybadge.com" class="help-btn-primary">
								<Mail class="size-4" />
								{{ __('Escribir a soporte') }}
							</a>

							<div class="response-note">
								<Clock class="size-4" />
								<span>{{ __('Respondemos de lunes a viernes en menos de 24 horas.') }}</span>
							</div>
						</div>
					</article>
				</div>
			</section>

			<section class="help-section">
				<div class="section-head">
					<div>
						<div class="section-kicker section-kicker-gold">
							<BookOpen class="size-4" />
							{{ __('Guía básica') }}
						</div>
						<h2>{{ __('Preguntas frecuentes') }}</h2>
						<p>
							{{
								__(
									'Estas son las dudas más comunes al usar StudyBadge por primera vez.'
								)
							}}
						</p>
					</div>
				</div>

				<div class="faq-grid">
					<article class="faq-card">
						<div class="faq-icon faq-icon-blue">
							<GraduationCap class="size-6" />
						</div>

						<div>
							<h3>{{ __('¿Cómo empiezo un curso?') }}</h3>
							<p>
								Para empezar un curso, dirígete a la pestaña
								<strong>Cursos</strong>, elige el curso que te interese y haz clic en
								<strong>Inscribirse</strong> o <strong>Empezar curso</strong>. Tu
								progreso se guardará automáticamente.
							</p>
						</div>
					</article>

					<article class="faq-card">
						<div class="faq-icon faq-icon-gold">
							<Award class="size-6" />
						</div>

						<div>
							<h3>{{ __('¿Cómo obtengo mis certificaciones?') }}</h3>
							<p>
								Cuando completes el 100% de las lecciones y evaluaciones de un curso,
								se generará tu certificado si cumples los requisitos. Podrás verlo en
								<strong> Certificaciones</strong> o desde tu perfil.
							</p>
						</div>
					</article>

					<article class="faq-card">
						<div class="faq-icon faq-icon-green">
							<User class="size-6" />
						</div>

						<div>
							<h3>{{ __('¿Por qué debo completar mi perfil?') }}</h3>
							<p>
								Un perfil completo mejora tu experiencia, permite mostrar mejor tus
								logros y puede ser necesario para participar en rankings, actividades o
								funciones avanzadas de StudyBadge.
							</p>
						</div>
					</article>

					<article class="faq-card">
						<div class="faq-icon faq-icon-purple">
							<CreditCard class="size-6" />
						</div>

						<div>
							<h3>{{ __('¿Qué hago si tengo un problema de pago?') }}</h3>
							<p>
								Si tienes problemas con una compra, suscripción, acceso Plus o
								facturación, escríbenos a
								<strong> soporte@studybadge.com</strong> con una captura y el correo de
								tu cuenta.
							</p>
						</div>
					</article>
				</div>
			</section>

			<section class="help-bottom-card">
				<div class="bottom-icon">
					<ShieldCheck class="size-6" />
				</div>

				<div>
					<h2>{{ __('Consejo para recibir ayuda más rápido') }}</h2>
					<p>
						{{
							__(
								'Cuando reportes un problema, incluye tu correo de cuenta, el nombre del curso, una captura de pantalla y una breve explicación de lo que ocurrió.'
							)
						}}
					</p>
				</div>

				<button class="help-btn-primary bottom-btn" @click="showSupportChat = true">
					<MessageCircle class="size-4" />
					{{ __('Reportar problema') }}
				</button>
			</section>
		</main>

		<Dialog
			v-model="showSupportChat"
			:options="{
				title: __('Asistente de Soporte IA'),
				size: '3xl',
			}"
		>
			<template #body-content>
				<div class="support-chat-shell">
					<div class="support-chat-head">
						<div class="support-chat-avatar">
							<Bot class="size-6" />
						</div>

						<div>
							<h3>{{ __('Soporte IA de StudyBadge') }}</h3>
							<p>{{ __('Puedes escribir tu duda o adjuntar una captura de pantalla.') }}</p>
						</div>
					</div>

					<div ref="chatContainer" class="support-chat-messages">
						<div v-if="chatHistory.length === 0" class="support-empty">
							<div class="support-empty-icon">
								<Bot class="size-10" />
							</div>

							<h3>{{ __('¡Hola! Soy el bot de soporte') }}</h3>

							<p>
								{{
									__(
										'Cuéntame qué pasó. Puedo ayudarte con cursos, certificados, pagos, errores técnicos o dudas generales de la plataforma.'
									)
								}}
							</p>

							<div class="support-suggestions">
								<button @click="currentMessage = __('No puedo acceder a mi curso')">
									{{ __('No puedo acceder a mi curso') }}
								</button>
								<button @click="currentMessage = __('Tengo un problema con mi certificado')">
									{{ __('Problema con certificado') }}
								</button>
								<button @click="currentMessage = __('Tengo una duda sobre mi pago')">
									{{ __('Duda sobre pago') }}
								</button>
							</div>
						</div>

						<div
							v-for="(msg, index) in chatHistory"
							:key="index"
							class="support-message-row"
							:class="msg.role === 'user' ? 'is-user' : 'is-assistant'"
						>
							<div class="support-message-avatar">
								<User v-if="msg.role === 'user'" class="size-4" />
								<Bot v-else class="size-4" />
							</div>

							<div class="support-message-bubble">
								<div
									v-if="msg.images_base64 && msg.images_base64.length"
									class="support-message-images"
								>
									<img
										v-for="(img, idx) in msg.images_base64"
										:key="idx"
										:src="'data:image/jpeg;base64,' + img"
										class="support-message-image"
									/>
								</div>

								<div
									class="support-markdown"
									v-html="renderMarkdown(msg.content)"
								></div>
							</div>
						</div>

						<div v-if="isTyping" class="support-message-row is-assistant">
							<div class="support-message-avatar">
								<Bot class="size-4" />
							</div>

							<div class="support-message-bubble support-typing">
								<Loader2 class="size-5 animate-spin" />
								<span>{{ __('Analizando tu consulta...') }}</span>
							</div>
						</div>
					</div>

					<div class="support-chat-input-area">
						<div v-if="previewImage" class="image-preview">
							<img :src="previewImage" />

							<button @click="clearImage" title="Quitar imagen">
								<X class="size-3.5" />
							</button>
						</div>

						<div class="support-input-row">
							<button
								class="attach-btn"
								@click="triggerImageUpload"
								title="Adjuntar imagen"
								:disabled="isTyping"
							>
								<ImagePlus class="size-5" />
							</button>

							<input
								ref="fileInput"
								type="file"
								accept="image/*"
								class="hidden"
								@change="handleImageSelect"
							/>

							<input
								v-model="currentMessage"
								type="text"
								class="support-input"
								:placeholder="__('Escribe tu mensaje aquí...')"
								@keyup.enter="sendMessage"
								:disabled="isTyping"
							/>

							<button
								class="send-support-btn"
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
import { computed, ref, nextTick, onMounted } from 'vue'
import { Breadcrumbs, usePageMeta, Dialog, call } from 'frappe-ui'
import { marked } from 'marked'
import {
	LifeBuoy,
	Headset,
	Bot,
	Mail,
	BookOpen,
	GraduationCap,
	Award,
	User,
	Clock,
	Send,
	ImagePlus,
	X,
	Loader2,
	Sparkles,
	ShieldCheck,
	MessageCircle,
	CreditCard,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()

onMounted(async () => {
	try {
		const siteKey = await call('studybadge_ai.keys.get_public_site_key')
		if (siteKey) {
			window.RECAPTCHA_SITE_KEY = siteKey
			const script = document.createElement('script')
			script.src = "https://www.google.com/recaptcha/api.js?render=" + siteKey
			document.head.appendChild(script)
		}
	} catch (e) {
		console.error('Failed to load recaptcha', e)
	}
})

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
		let captchaToken = null
		if (window.grecaptcha && window.RECAPTCHA_SITE_KEY) {
			captchaToken = await window.grecaptcha.execute(window.RECAPTCHA_SITE_KEY, {action: 'support_chat'})
		}
		const response = await call('studybadge_ai.ai_support.chat_with_support', {
			message: msgText,
			images_base64: imgBase64 ? JSON.stringify([imgBase64]) : '[]',
			history: JSON.stringify(chatHistory.value.slice(0, -1)),
			captcha_token: captchaToken
		})

		if (response.reply) {
			chatHistory.value.push({
				role: 'assistant',
				content: response.reply,
			})
		}
	} catch (error) {
		chatHistory.value.push({
			role: 'assistant',
			content:
				'Hubo un error al procesar tu solicitud. Por favor, intenta de nuevo o escribe a soporte@studybadge.com.',
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
.help-page {
	min-height: 100vh;
	background: #f5f8fc;
	color: #0f172a;
	padding-bottom: 4rem;
}

.help-header {
	position: sticky;
	top: 0;
	z-index: 20;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	border-bottom: 1px solid rgba(10, 34, 81, 0.08);
	background: rgba(255, 255, 255, 0.92);
	padding: 0.8rem 1rem;
	backdrop-filter: blur(14px);
	box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.help-header-mail {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.45rem;
	border: 1px solid rgba(10, 34, 81, 0.1);
	border-radius: 999px;
	background: #ffffff;
	padding: 0.55rem 0.8rem;
	color: #0a2251;
	font-size: 0.82rem;
	font-weight: 900;
	text-decoration: none;
	white-space: nowrap;
	box-shadow: 0 10px 22px rgba(15, 23, 42, 0.045);
	transition: 0.18s ease;
}

.help-header-mail:hover {
	transform: translateY(-1px);
	border-color: rgba(10, 34, 81, 0.2);
	box-shadow: 0 14px 28px rgba(15, 23, 42, 0.075);
}

.help-hero {
	position: relative;
	overflow: hidden;
	background: #0a2251;
	color: #ffffff;
	padding: 4.5rem 1.25rem 5.5rem;
	text-align: center;
}

.help-hero::before {
	content: '';
	position: absolute;
	inset: 1rem;
	border: 1px solid rgba(255, 255, 255, 0.08);
	border-radius: 32px;
	pointer-events: none;
}

.help-hero-inner {
	position: relative;
	z-index: 1;
	width: min(920px, 100%);
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.hero-icon {
	display: grid;
	width: 82px;
	height: 82px;
	place-items: center;
	border-radius: 28px;
	background: rgba(255, 255, 255, 0.1);
	color: #ffffff;
	border: 1px solid rgba(255, 255, 255, 0.16);
	box-shadow: 0 20px 46px rgba(0, 0, 0, 0.18);
}

.hero-eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	margin-top: 1.25rem;
	border-radius: 999px;
	border: 1px solid rgba(255, 255, 255, 0.16);
	background: rgba(255, 255, 255, 0.08);
	padding: 0.45rem 0.75rem;
	color: rgba(255, 255, 255, 0.88);
	font-size: 0.76rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.help-hero h1 {
	margin: 1rem 0 0;
	max-width: 760px;
	color: #ffffff;
	font-size: clamp(2.35rem, 7vw, 5.25rem);
	font-weight: 950;
	letter-spacing: -0.065em;
	line-height: 0.98;
}

.help-hero p {
	margin: 1.1rem auto 0;
	max-width: 720px;
	color: rgba(255, 255, 255, 0.78);
	font-size: clamp(0.98rem, 2vw, 1.18rem);
	line-height: 1.75;
}

.hero-actions {
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	gap: 0.75rem;
	margin-top: 1.7rem;
}

.help-btn-light,
.help-btn-ghost,
.help-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	min-height: 44px;
	border-radius: 999px;
	padding: 0.78rem 1.1rem;
	font-size: 0.9rem;
	font-weight: 950;
	text-decoration: none;
	cursor: pointer;
	transition:
		transform 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease,
		box-shadow 0.18s ease,
		opacity 0.18s ease;
}

.help-btn-light {
	border: 1px solid #ffffff;
	background: #ffffff;
	color: #0a2251;
	box-shadow: 0 16px 32px rgba(0, 0, 0, 0.18);
}

.help-btn-light:hover {
	transform: translateY(-1px);
	background: #f8fbff;
}

.help-btn-ghost {
	border: 1px solid rgba(255, 255, 255, 0.24);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
}

.help-btn-ghost:hover {
	transform: translateY(-1px);
	background: rgba(255, 255, 255, 0.14);
}

.help-btn-primary {
	border: 1px solid #0a2251;
	background: #0a2251;
	color: #ffffff;
	box-shadow: 0 14px 28px rgba(10, 34, 81, 0.18);
}

.help-btn-primary:hover {
	transform: translateY(-1px);
	background: #12356e;
	border-color: #12356e;
	color: #ffffff;
	box-shadow: 0 18px 34px rgba(10, 34, 81, 0.22);
}

.help-main {
	position: relative;
	z-index: 2;
	width: min(1100px, calc(100% - 2rem));
	margin: -2.2rem auto 0;
	display: flex;
	flex-direction: column;
	gap: 2rem;
}

.help-section,
.help-bottom-card {
	border: 1px solid rgba(10, 34, 81, 0.08);
	border-radius: 28px;
	background: rgba(255, 255, 255, 0.94);
	padding: 1.4rem;
	box-shadow: 0 20px 50px rgba(15, 23, 42, 0.07);
	backdrop-filter: blur(14px);
}

.section-head {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
	margin-bottom: 1.2rem;
}

.section-kicker {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	width: fit-content;
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.08);
	padding: 0.38rem 0.68rem;
	color: #0a2251;
	font-size: 0.72rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.section-kicker-gold {
	background: rgba(245, 179, 1, 0.16);
	color: #8a6100;
}

.section-head h2 {
	margin: 0.75rem 0 0;
	color: #0a2251;
	font-size: clamp(1.5rem, 3vw, 2.1rem);
	font-weight: 950;
	letter-spacing: -0.045em;
	line-height: 1.1;
}

.section-head p {
	margin: 0.45rem 0 0;
	max-width: 720px;
	color: #64748b;
	font-size: 0.94rem;
	line-height: 1.7;
}

.support-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 1rem;
}

.support-card {
	position: relative;
	display: flex;
	min-height: 310px;
	flex-direction: column;
	overflow: hidden;
	border: 1px solid rgba(226, 232, 240, 0.95);
	border-radius: 24px;
	background: #ffffff;
	padding: 1.25rem;
	box-shadow: 0 12px 30px rgba(15, 23, 42, 0.045);
	cursor: default;
	transition:
		transform 0.18s ease,
		border-color 0.18s ease,
		box-shadow 0.18s ease;
}

.support-card-primary {
	cursor: pointer;
}

.support-card:hover {
	transform: translateY(-2px);
	border-color: rgba(10, 34, 81, 0.18);
	box-shadow: 0 22px 48px rgba(10, 34, 81, 0.095);
}

.card-top {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
}

.card-icon,
.faq-icon,
.bottom-icon {
	display: grid;
	place-items: center;
	flex: 0 0 auto;
}

.card-icon {
	width: 56px;
	height: 56px;
	border-radius: 20px;
}

.card-icon-blue {
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.card-icon-gold {
	background: rgba(245, 179, 1, 0.16);
	color: #8a6100;
}

.card-badge {
	display: inline-flex;
	align-items: center;
	border-radius: 999px;
	background: #0a2251;
	padding: 0.3rem 0.6rem;
	color: #ffffff;
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.card-badge-soft {
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.support-card h3 {
	margin: 1.2rem 0 0;
	color: #0f172a;
	font-size: 1.28rem;
	font-weight: 950;
	letter-spacing: -0.035em;
	line-height: 1.16;
}

.support-card p {
	margin: 0.7rem 0 0;
	color: #64748b;
	font-size: 0.94rem;
	line-height: 1.65;
}

.card-action {
	margin-top: auto;
	padding-top: 1.2rem;
	border-top: 1px solid rgba(226, 232, 240, 0.9);
}

.response-note {
	display: flex;
	align-items: center;
	gap: 0.45rem;
	margin-top: 0.8rem;
	color: #64748b;
	font-size: 0.82rem;
	font-weight: 750;
	line-height: 1.45;
}

.faq-grid {
	display: grid;
	gap: 0.85rem;
}

.faq-card {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr);
	gap: 1rem;
	align-items: flex-start;
	border: 1px solid rgba(226, 232, 240, 0.94);
	border-radius: 22px;
	background: #ffffff;
	padding: 1.1rem;
	box-shadow: 0 10px 26px rgba(15, 23, 42, 0.04);
	transition:
		transform 0.18s ease,
		border-color 0.18s ease,
		box-shadow 0.18s ease;
}

.faq-card:hover {
	transform: translateY(-1px);
	border-color: rgba(10, 34, 81, 0.15);
	box-shadow: 0 18px 38px rgba(15, 23, 42, 0.07);
}

.faq-icon {
	width: 48px;
	height: 48px;
	border-radius: 18px;
}

.faq-icon-blue {
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.faq-icon-gold {
	background: rgba(245, 179, 1, 0.16);
	color: #8a6100;
}

.faq-icon-green {
	background: rgba(34, 197, 94, 0.12);
	color: #15803d;
}

.faq-icon-purple {
	background: rgba(99, 102, 241, 0.12);
	color: #4338ca;
}

.faq-card h3 {
	margin: 0;
	color: #0f172a;
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.025em;
	line-height: 1.25;
}

.faq-card p {
	margin: 0.42rem 0 0;
	color: #64748b;
	font-size: 0.92rem;
	line-height: 1.68;
}

.faq-card strong {
	color: #0a2251;
	font-weight: 950;
}

.help-bottom-card {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr) auto;
	align-items: center;
	gap: 1rem;
}

.bottom-icon {
	width: 54px;
	height: 54px;
	border-radius: 20px;
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.help-bottom-card h2 {
	margin: 0;
	color: #0a2251;
	font-size: 1.08rem;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.help-bottom-card p {
	margin: 0.35rem 0 0;
	color: #64748b;
	font-size: 0.9rem;
	line-height: 1.6;
}

.bottom-btn {
	white-space: nowrap;
}

/* CHAT MODAL */

.support-chat-shell {
	display: flex;
	height: min(680px, calc(100dvh - 8rem));
	flex-direction: column;
	overflow: hidden;
	border: 1px solid rgba(10, 34, 81, 0.1);
	border-radius: 22px;
	background: #f5f8fc;
	margin: -1rem;
}

.support-chat-head {
	display: flex;
	align-items: center;
	gap: 0.8rem;
	border-bottom: 1px solid rgba(10, 34, 81, 0.08);
	background: #ffffff;
	padding: 1rem;
}

.support-chat-avatar {
	display: grid;
	width: 48px;
	height: 48px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 18px;
	background: #0a2251;
	color: #ffffff;
}

.support-chat-head h3 {
	margin: 0;
	color: #0a2251;
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.025em;
}

.support-chat-head p {
	margin: 0.25rem 0 0;
	color: #64748b;
	font-size: 0.82rem;
	line-height: 1.45;
}

.support-chat-messages {
	flex: 1;
	overflow-y: auto;
	padding: 1rem;
	scrollbar-width: thin;
	scrollbar-color: rgba(10, 34, 81, 0.24) transparent;
}

.support-chat-messages::-webkit-scrollbar {
	width: 8px;
}

.support-chat-messages::-webkit-scrollbar-thumb {
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.22);
}

.support-empty {
	display: flex;
	min-height: 100%;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 2rem 1rem;
	text-align: center;
}

.support-empty-icon {
	display: grid;
	width: 78px;
	height: 78px;
	place-items: center;
	border-radius: 28px;
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.support-empty h3 {
	margin: 1rem 0 0;
	color: #0a2251;
	font-size: 1.25rem;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.support-empty p {
	margin: 0.45rem auto 0;
	max-width: 520px;
	color: #64748b;
	font-size: 0.9rem;
	line-height: 1.65;
}

.support-suggestions {
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	gap: 0.5rem;
	margin-top: 1rem;
}

.support-suggestions button {
	border: 1px solid rgba(10, 34, 81, 0.12);
	border-radius: 999px;
	background: #ffffff;
	padding: 0.55rem 0.8rem;
	color: #0a2251;
	font-size: 0.78rem;
	font-weight: 900;
	cursor: pointer;
	transition: 0.18s ease;
}

.support-suggestions button:hover {
	transform: translateY(-1px);
	border-color: rgba(10, 34, 81, 0.22);
	box-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

.support-message-row {
	display: flex;
	align-items: flex-start;
	gap: 0.6rem;
	width: 100%;
	margin: 0.85rem 0;
}

.support-message-row.is-user {
	flex-direction: row-reverse;
}

.support-message-avatar {
	display: grid;
	width: 34px;
	height: 34px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 13px;
	background: #ffffff;
	color: #0a2251;
	border: 1px solid rgba(10, 34, 81, 0.1);
	box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
}

.support-message-row.is-user .support-message-avatar {
	background: rgba(10, 34, 81, 0.08);
}

.support-message-bubble {
	max-width: min(78%, 680px);
	border: 1px solid rgba(226, 232, 240, 0.92);
	border-radius: 20px;
	border-bottom-left-radius: 7px;
	background: #ffffff;
	padding: 0.85rem 1rem;
	color: #334155;
	font-size: 0.9rem;
	line-height: 1.65;
	box-shadow: 0 12px 26px rgba(15, 23, 42, 0.045);
	overflow-wrap: anywhere;
}

.support-message-row.is-user .support-message-bubble {
	border-color: #0a2251;
	border-bottom-right-radius: 7px;
	border-bottom-left-radius: 20px;
	background: #0a2251;
	color: #ffffff;
	box-shadow: 0 14px 30px rgba(10, 34, 81, 0.16);
}

.support-message-images {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
	margin-bottom: 0.7rem;
}

.support-message-image {
	max-height: 190px;
	max-width: 100%;
	border-radius: 16px;
	object-fit: cover;
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-shadow: 0 10px 22px rgba(15, 23, 42, 0.1);
}

.support-markdown :deep(p) {
	margin: 0 0 0.65rem;
}

.support-markdown :deep(p:last-child) {
	margin-bottom: 0;
}

.support-markdown :deep(ul),
.support-markdown :deep(ol) {
	margin: 0.55rem 0 0.7rem 1.1rem;
	padding: 0;
}

.support-markdown :deep(strong) {
	font-weight: 950;
}

.support-markdown :deep(code) {
	border-radius: 7px;
	background: rgba(10, 34, 81, 0.08);
	padding: 0.1rem 0.3rem;
	color: #0a2251;
	font-size: 0.9em;
}

.support-message-row.is-user .support-markdown :deep(code) {
	background: rgba(255, 255, 255, 0.14);
	color: #ffffff;
}

.support-typing {
	display: inline-flex;
	align-items: center;
	gap: 0.55rem;
	color: #64748b;
	font-weight: 800;
}

.support-typing svg {
	color: #0a2251;
}

.support-chat-input-area {
	border-top: 1px solid rgba(10, 34, 81, 0.08);
	background: #ffffff;
	padding: 0.9rem;
}

.image-preview {
	position: relative;
	display: inline-block;
	margin-bottom: 0.75rem;
}

.image-preview img {
	height: 82px;
	max-width: 180px;
	border-radius: 16px;
	object-fit: cover;
	border: 1px solid rgba(10, 34, 81, 0.1);
	box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08);
}

.image-preview button {
	position: absolute;
	top: -8px;
	right: -8px;
	display: grid;
	width: 24px;
	height: 24px;
	place-items: center;
	border: 0;
	border-radius: 999px;
	background: #ef4444;
	color: #ffffff;
	cursor: pointer;
	box-shadow: 0 10px 20px rgba(239, 68, 68, 0.24);
}

.support-input-row {
	display: flex;
	align-items: center;
	gap: 0.55rem;
}

.attach-btn,
.send-support-btn {
	display: grid;
	width: 44px;
	height: 44px;
	flex: 0 0 auto;
	place-items: center;
	border: 0;
	border-radius: 16px;
	cursor: pointer;
	transition:
		transform 0.18s ease,
		background 0.18s ease,
		opacity 0.18s ease;
}

.attach-btn {
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.attach-btn:hover:not(:disabled) {
	transform: translateY(-1px);
	background: rgba(10, 34, 81, 0.12);
}

.support-input {
	min-width: 0;
	flex: 1;
	height: 44px;
	border: 1px solid rgba(203, 213, 225, 0.9);
	border-radius: 16px;
	background: #f8fafc;
	padding: 0 0.9rem;
	color: #0f172a;
	font-size: 0.92rem;
	outline: none;
	transition:
		border-color 0.18s ease,
		box-shadow 0.18s ease,
		background 0.18s ease;
}

.support-input:focus {
	border-color: rgba(10, 34, 81, 0.42);
	background: #ffffff;
	box-shadow: 0 0 0 4px rgba(10, 34, 81, 0.08);
}

.send-support-btn {
	background: #0a2251;
	color: #ffffff;
	box-shadow: 0 12px 24px rgba(10, 34, 81, 0.2);
}

.send-support-btn:hover:not(:disabled) {
	transform: translateY(-1px);
	background: #12356e;
}

.attach-btn:disabled,
.send-support-btn:disabled {
	cursor: not-allowed;
	opacity: 0.55;
	transform: none;
	box-shadow: none;
}

/* DARK MODE */

:global(:root[data-theme='dark']) .help-page,
:global(.dark) .help-page {
	background: #07111f;
	color: #e5edf8;
}

:global(:root[data-theme='dark']) .help-header,
:global(.dark) .help-header {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(7, 17, 31, 0.92);
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.24);
}

:global(:root[data-theme='dark']) .help-header-mail,
:global(.dark) .help-header-mail {
	border-color: rgba(255, 255, 255, 0.1);
	background: rgba(15, 23, 42, 0.72);
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .help-section,
:global(:root[data-theme='dark']) .help-bottom-card,
:global(:root[data-theme='dark']) .support-card,
:global(:root[data-theme='dark']) .faq-card,
:global(:root[data-theme='dark']) .support-chat-head,
:global(:root[data-theme='dark']) .support-chat-input-area,
:global(:root[data-theme='dark']) .support-message-bubble,
:global(.dark) .help-section,
:global(.dark) .help-bottom-card,
:global(.dark) .support-card,
:global(.dark) .faq-card,
:global(.dark) .support-chat-head,
:global(.dark) .support-chat-input-area,
:global(.dark) .support-message-bubble {
	border-color: rgba(148, 163, 184, 0.16);
	background: rgba(15, 23, 42, 0.78);
	box-shadow: 0 18px 44px rgba(0, 0, 0, 0.22);
}

:global(:root[data-theme='dark']) .help-section,
:global(:root[data-theme='dark']) .help-bottom-card,
:global(.dark) .help-section,
:global(.dark) .help-bottom-card {
	backdrop-filter: blur(14px);
}

:global(:root[data-theme='dark']) .support-chat-shell,
:global(.dark) .support-chat-shell {
	border-color: rgba(148, 163, 184, 0.16);
	background: #07111f;
}

:global(:root[data-theme='dark']) .section-head h2,
:global(:root[data-theme='dark']) .support-card h3,
:global(:root[data-theme='dark']) .faq-card h3,
:global(:root[data-theme='dark']) .help-bottom-card h2,
:global(:root[data-theme='dark']) .support-chat-head h3,
:global(:root[data-theme='dark']) .support-empty h3,
:global(.dark) .section-head h2,
:global(.dark) .support-card h3,
:global(.dark) .faq-card h3,
:global(.dark) .help-bottom-card h2,
:global(.dark) .support-chat-head h3,
:global(.dark) .support-empty h3 {
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .section-head p,
:global(:root[data-theme='dark']) .support-card p,
:global(:root[data-theme='dark']) .faq-card p,
:global(:root[data-theme='dark']) .help-bottom-card p,
:global(:root[data-theme='dark']) .support-chat-head p,
:global(:root[data-theme='dark']) .support-empty p,
:global(:root[data-theme='dark']) .response-note,
:global(.dark) .section-head p,
:global(.dark) .support-card p,
:global(.dark) .faq-card p,
:global(.dark) .help-bottom-card p,
:global(.dark) .support-chat-head p,
:global(.dark) .support-empty p,
:global(.dark) .response-note {
	color: #94a3b8;
}

:global(:root[data-theme='dark']) .section-kicker,
:global(:root[data-theme='dark']) .card-icon-blue,
:global(:root[data-theme='dark']) .faq-icon-blue,
:global(:root[data-theme='dark']) .bottom-icon,
:global(:root[data-theme='dark']) .support-empty-icon,
:global(:root[data-theme='dark']) .attach-btn,
:global(.dark) .section-kicker,
:global(.dark) .card-icon-blue,
:global(.dark) .faq-icon-blue,
:global(.dark) .bottom-icon,
:global(.dark) .support-empty-icon,
:global(.dark) .attach-btn {
	background: rgba(245, 179, 1, 0.14);
	color: #f8c84e;
}

:global(:root[data-theme='dark']) .section-kicker-gold,
:global(:root[data-theme='dark']) .card-icon-gold,
:global(:root[data-theme='dark']) .faq-icon-gold,
:global(.dark) .section-kicker-gold,
:global(.dark) .card-icon-gold,
:global(.dark) .faq-icon-gold {
	background: rgba(245, 179, 1, 0.14);
	color: #f8c84e;
}

:global(:root[data-theme='dark']) .card-badge-soft,
:global(.dark) .card-badge-soft {
	background: rgba(245, 179, 1, 0.14);
	color: #f8c84e;
}

:global(:root[data-theme='dark']) .faq-card strong,
:global(.dark) .faq-card strong {
	color: #f8c84e;
}

:global(:root[data-theme='dark']) .support-message-row.is-user .support-message-bubble,
:global(.dark) .support-message-row.is-user .support-message-bubble {
	border-color: #0a2251;
	background: #0a2251;
	color: #ffffff;
}

:global(:root[data-theme='dark']) .support-message-avatar,
:global(:root[data-theme='dark']) .support-suggestions button,
:global(.dark) .support-message-avatar,
:global(.dark) .support-suggestions button {
	border-color: rgba(148, 163, 184, 0.16);
	background: rgba(15, 23, 42, 0.78);
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .support-input,
:global(.dark) .support-input {
	border-color: rgba(148, 163, 184, 0.18);
	background: rgba(2, 6, 23, 0.42);
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .support-input:focus,
:global(.dark) .support-input:focus {
	background: rgba(2, 6, 23, 0.58);
}

/* RESPONSIVE */

@media (max-width: 900px) {
	.help-main {
		width: min(100% - 1.5rem, 1100px);
	}

	.support-grid {
		grid-template-columns: 1fr;
	}

	.support-card {
		min-height: auto;
	}

	.help-bottom-card {
		grid-template-columns: 1fr;
		text-align: left;
	}

	.bottom-btn {
		width: 100%;
	}
}

@media (max-width: 640px) {
	.help-header {
		padding: 0.72rem 0.85rem;
	}

	.help-header-mail span {
		display: none;
	}

	.help-header-mail {
		width: 40px;
		height: 40px;
		padding: 0;
	}

	.help-hero {
		padding: 3.2rem 1rem 4.5rem;
	}

	.help-hero::before {
		inset: 0.65rem;
		border-radius: 24px;
	}

	.hero-icon {
		width: 70px;
		height: 70px;
		border-radius: 24px;
	}

	.help-hero h1 {
		font-size: clamp(2.2rem, 12vw, 3.2rem);
	}

	.help-hero p {
		font-size: 0.92rem;
		line-height: 1.65;
	}

	.hero-actions {
		width: 100%;
		flex-direction: column;
	}

	.help-btn-light,
	.help-btn-ghost,
	.help-btn-primary {
		width: 100%;
	}

	.help-main {
		width: calc(100% - 1rem);
		margin-top: -1.7rem;
		gap: 1rem;
	}

	.help-section,
	.help-bottom-card {
		border-radius: 22px;
		padding: 1rem;
	}

	.section-head {
		margin-bottom: 1rem;
	}

	.section-head h2 {
		font-size: 1.35rem;
	}

	.section-head p {
		font-size: 0.86rem;
	}

	.support-card {
		border-radius: 20px;
		padding: 1rem;
	}

	.card-icon {
		width: 50px;
		height: 50px;
		border-radius: 18px;
	}

	.support-card h3 {
		font-size: 1.1rem;
	}

	.support-card p,
	.faq-card p {
		font-size: 0.86rem;
	}

	.faq-card {
		grid-template-columns: 1fr;
		border-radius: 20px;
		padding: 1rem;
	}

	.faq-icon {
		width: 46px;
		height: 46px;
	}

	.support-chat-shell {
		height: min(650px, calc(100dvh - 5rem));
		margin: -0.75rem;
		border-radius: 18px;
	}

	.support-chat-head {
		align-items: flex-start;
		padding: 0.85rem;
	}

	.support-chat-avatar {
		width: 42px;
		height: 42px;
		border-radius: 16px;
	}

	.support-chat-messages {
		padding: 0.75rem;
	}

	.support-empty {
		padding: 1.5rem 0.5rem;
	}

	.support-suggestions {
		flex-direction: column;
		width: 100%;
	}

	.support-suggestions button {
		width: 100%;
	}

	.support-message-avatar {
		width: 30px;
		height: 30px;
		border-radius: 12px;
	}

	.support-message-bubble {
		max-width: calc(100% - 38px);
		border-radius: 18px;
		padding: 0.78rem 0.85rem;
		font-size: 0.86rem;
		line-height: 1.6;
	}

	.support-input-row {
		gap: 0.42rem;
	}

	.attach-btn,
	.send-support-btn {
		width: 40px;
		height: 40px;
		border-radius: 14px;
	}

	.support-input {
		height: 40px;
		border-radius: 14px;
		font-size: 16px;
	}
}
</style>

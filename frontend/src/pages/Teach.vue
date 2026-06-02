<template>
	<div class="teach-page">
		<header class="teach-hero">
			<div class="hero-grid-bg" aria-hidden="true"></div>

			<nav class="topbar">
				<a href="/" class="brand" aria-label="Ir al inicio de StudyBadge">
					<span class="brand-logo">
						<img v-if="brand.favicon" :src="brand.favicon" alt="StudyBadge" />
						<GraduationCap v-else class="size-5" />
					</span>
					<span>StudyBadge</span>
				</a>

				<div class="topbar-actions">
					<a href="/login" class="login-link">
						<LogIn class="size-4" />
						{{ __('Iniciar sesión') }}
					</a>
					<a href="#postula" class="topbar-cta">
						{{ __('Postular') }}
						<ArrowRight class="size-4" />
					</a>
				</div>
			</nav>

			<div class="hero-inner">
				<section class="hero-copy">
					<div class="eyebrow">
						<GraduationCap class="size-4" />
						{{ __('Programa de instructores') }}
					</div>

					<h1>
						{{ __('Enseña en StudyBadge y convierte tu conocimiento en ingresos.') }}
					</h1>

					<p class="lead">
						{{ __('Publica cursos prácticos, recibe acompañamiento, usa herramientas con IA y gana por cada venta aprobada dentro de la plataforma.') }}
					</p>

					<div class="hero-actions">
						<a href="#postula" class="primary-link">
							{{ __('Postular ahora') }}
							<ArrowRight class="size-4" />
						</a>
						<a href="#plus" class="secondary-link">
							{{ __('Ver programa Plus') }}
						</a>
					</div>

					<div class="hero-proof">
						<div class="proof-item">
							<CheckCircle2 class="size-4" />
							<span>{{ __('Sin costo inicial') }}</span>
						</div>
						<div class="proof-item">
							<ShieldCheck class="size-4" />
							<span>{{ __('Revisión de calidad') }}</span>
						</div>
						<div class="proof-item">
							<Wallet class="size-4" />
							<span>{{ __('Retiros desde S/20') }}</span>
						</div>
					</div>
				</section>

				<section class="hero-panel" aria-label="Resumen del programa de instructores">
					<div class="panel-header">
						<div>
							<span>{{ __('Modelo para fundadores') }}</span>
							<strong>{{ __('Gana más por enseñar') }}</strong>
						</div>
						<div class="panel-badge">
							<BadgePercent class="size-5" />
						</div>
					</div>

					<div class="panel-stats">
						<div class="panel-stat">
							<span>{{ __('Ventas propias') }}</span>
							<strong>95%</strong>
							<small>{{ __('Para ti') }}</small>
						</div>
						<div class="panel-stat">
							<span>{{ __('Ventas StudyBadge') }}</span>
							<strong>80%</strong>
							<small>{{ __('Para ti') }}</small>
						</div>
					</div>

					<div class="panel-list">
						<div class="panel-line">
							<Wallet class="size-5" />
							<span>{{ __('Solicita retiros desde S/20 cuando tengas ganancias disponibles.') }}</span>
						</div>
						<div class="panel-line">
							<ShieldCheck class="size-5" />
							<span>{{ __('Tus cursos pasan por revisión antes de publicarse en el catálogo.') }}</span>
						</div>
						<div class="panel-line">
							<BookOpenCheck class="size-5" />
							<span>{{ __('Organiza tus lecciones, recursos y actividades desde tu panel privado.') }}</span>
						</div>
					</div>
				</section>
			</div>
		</header>

		<main class="content">
			<section class="program-grid" aria-label="Beneficios para instructores">
				<article v-for="item in benefits" :key="item.title" class="program-card">
					<div class="icon-box"><component :is="item.icon" class="size-5" /></div>
					<h2>{{ item.title }}</h2>
					<p>{{ item.body }}</p>
				</article>
			</section>

			<section id="plus" class="plus-band">
				<div class="plus-icon"><BadgePercent class="size-6" /></div>
				<div class="plus-copy">
					<p class="section-kicker">{{ __('StudyBadge Plus') }}</p>
					<h2>{{ __('Un programa para hacer tus cursos más atractivos.') }}</h2>
					<p>
						{{ __('Plus permite ofrecer descuentos automáticos a miembros activos. Puedes participar de forma opcional y elegir un descuento sugerido de 10%, 15% o 20%.') }}
					</p>
				</div>
				<div class="plus-metrics" aria-label="Opciones de descuento">
					<span>10%</span>
					<span>15%</span>
					<span>20%</span>
				</div>
			</section>

			<section id="postula" class="form-layout">
				<aside class="form-intro">
					<div class="sticky-card">
						<p class="section-kicker">{{ __('Postulación') }}</p>
						<h2>{{ __('Completa lo esencial y revisaremos tu perfil.') }}</h2>
						<p>
							{{ __('Si tu perfil es aprobado, podrás terminar tu configuración, crear cursos y gestionar ventas desde tu panel de instructor.') }}
						</p>

						<div class="timeline">
							<div v-for="step in steps" :key="step.title" class="timeline-item">
								<span>{{ step.number }}</span>
								<div>
									<strong>{{ step.title }}</strong>
									<p>{{ step.body }}</p>
								</div>
							</div>
						</div>

						<div class="support-card">
							<Headphones class="size-5" />
							<div>
								<strong>{{ __('¿Tienes dudas?') }}</strong>
								<span>{{ __('Si el formulario falla, intenta nuevamente o escríbenos a soporte.') }}</span>
								<a href="mailto:soporte@studybadge.com">soporte@studybadge.com</a>
							</div>
						</div>
					</div>
				</aside>

				<form class="application-card" @submit.prevent="submit">
					<div class="form-card-header">
						<div>
							<p class="section-kicker">{{ __('Formulario') }}</p>
							<h2>{{ __('Postula como instructor') }}</h2>
							<span>{{ __('La información se usará para evaluar tu perfil y ayudarte a publicar mejores cursos.') }}</span>
						</div>
						<div class="form-header-icon">
							<Send class="size-5" />
						</div>
					</div>

					<div class="form-section">
						<div class="form-section-title">
							<UserRound class="size-4" />
							<h3>{{ __('Datos básicos') }}</h3>
						</div>
						<div class="field-grid">
							<FormControl v-model="form.full_name" :label="__('Nombre completo')" required />
							<FormControl v-model="form.display_name" :label="__('Nombre de instructor')" required />
							<FormControl v-model="form.email" :label="__('Email')" type="email" required />
							<FormControl v-model="form.birth_date" :label="__('Fecha de nacimiento')" type="date" required />
							<FormControl v-model="form.country" :label="__('País')" required />
							<FormControl v-model="form.city" :label="__('Ciudad')" required />
						</div>
					</div>

					<div class="form-section">
						<div class="form-section-title">
							<BookOpenCheck class="size-4" />
							<h3>{{ __('Tu experiencia') }}</h3>
						</div>
						<FormControl v-model="form.main_specialty" :label="__('Especialidad principal')" required />
						<FormControl v-model="form.professional_bio" :label="__('Resumen profesional')" type="textarea" :rows="4" required />
						<FormControl v-model="form.topics_to_teach" :label="__('Qué cursos quieres enseñar')" type="textarea" :rows="3" required />
						<FormControl v-model="form.first_course_idea" :label="__('Primera idea de curso')" type="textarea" :rows="3" required />
					</div>

					<div class="option-row">
						<label class="option-card">
							<input v-model="form.wants_to_charge" type="checkbox" />
							<span class="option-check">
								<CheckCircle2 class="size-4" />
							</span>
							<span>
								<strong>{{ __('Quiero vender cursos') }}</strong>
								<small>{{ __('Podrás definir precio al crear cada curso.') }}</small>
							</span>
						</label>

						<label class="option-card plus-option">
							<input v-model="form.accepts_plus_program" type="checkbox" />
							<span class="option-check">
								<BadgePercent class="size-4" />
							</span>
							<span>
								<strong>{{ __('Participar en Plus') }}</strong>
								<small>{{ __('Descuentos automáticos para vender más rápido.') }}</small>
							</span>
						</label>
					</div>

					<div v-if="form.accepts_plus_program" class="plus-choice">
						<label class="field-label">{{ __('Descuento para miembros Plus') }}</label>
						<div class="discount-options">
							<label v-for="discount in ['10', '15', '20']" :key="discount">
								<input v-model="form.plus_discount_percent" type="radio" :value="discount" />
								<span>{{ discount }}%</span>
							</label>
						</div>
					</div>

					<details class="optional-details">
						<summary>
							<span>{{ __('Agregar información opcional') }}</span>
							<ChevronDown class="size-4" />
						</summary>
						<div class="optional-body">
							<div class="field-grid">
								<FormControl v-model="form.whatsapp" label="WhatsApp" />
								<FormControl v-model="form.years_of_experience" :label="__('Años de experiencia')" type="number" />
								<FormControl v-model="form.target_audience" :label="__('Público objetivo')" />
								<FormControl v-model="form.estimated_course_price" :label="__('Precio estimado')" type="number" />
								<FormControl v-model="form.portfolio_url" :label="__('Portafolio')" />
								<FormControl v-model="form.linkedin_url" label="LinkedIn" />
								<FormControl v-model="form.tiktok_url" label="TikTok" />
								<FormControl v-model="form.youtube_url" label="YouTube" />
								<FormControl v-model="form.website_url" :label="__('Web')" />
							</div>
							<FormControl v-model="form.additional_message" :label="__('Mensaje adicional')" type="textarea" :rows="3" />
						</div>
					</details>

					<div class="legal-box">
						<label v-for="item in legal" :key="item.key" class="check-row">
							<input v-model="form[item.key]" type="checkbox" required />
							<span>{{ item.label }}</span>
						</label>
					</div>

					<div v-if="result" class="result-box" :class="`status-${result.status}`">
						<div class="result-icon">
							<CheckCircle2 v-if="result.status !== 'Rejected'" class="size-5" />
							<AlertTriangle v-else class="size-5" />
						</div>
						<div>
							<strong>{{ statusTitle }}</strong>
							<span>{{ resultMessage }}</span>
						</div>
					</div>

					<div class="submit-row">
						<Button variant="solid" size="lg" :loading="loading" type="submit" class="submit-button">
							{{ loading ? __('Enviando postulación') : __('Enviar postulación') }}
						</Button>
						<p>{{ __('Verás una confirmación apenas se procese el envío. No necesitas esperar ningún correo en esta pantalla.') }}</p>
					</div>
				</form>
			</section>
		</main>

		<Teleport to="body">
			<div v-if="modal.open" class="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="teach-modal-title">
				<div class="modal-card" :class="`modal-${modal.type}`">
					<div class="modal-icon">
						<Loader2 v-if="modal.type === 'sending'" class="size-6 modal-spinner" />
						<CheckCircle2 v-else-if="modal.type === 'success'" class="size-6" />
						<AlertTriangle v-else class="size-6" />
					</div>

					<div class="modal-content">
						<h3 id="teach-modal-title">{{ modal.title }}</h3>
						<p>{{ modal.message }}</p>

						<div class="modal-actions">
							<button v-if="modal.type === 'sending'" type="button" class="modal-button muted" @click="closeModal">
								{{ __('Seguir completando') }}
							</button>
							<button v-else-if="modal.type === 'success'" type="button" class="modal-button" @click="closeModal">
								{{ __('Entendido') }}
							</button>
							<template v-else>
								<button type="button" class="modal-button muted" @click="closeModal">
									{{ __('Cerrar') }}
								</button>
								<button type="button" class="modal-button" @click="submit">
									{{ __('Reintentar') }}
								</button>
							</template>
						</div>
					</div>
				</div>
			</div>
		</Teleport>
	</div>
</template>

<script setup>
import { Button, FormControl, call, toast, usePageMeta } from 'frappe-ui'
import { computed, reactive, ref, watch } from 'vue'
import {
	AlertTriangle,
	ArrowRight,
	BadgePercent,
	BookOpenCheck,
	CheckCircle2,
	ChevronDown,
	DollarSign,
	GraduationCap,
	Headphones,
	Loader2,
	LogIn,
	Send,
	ShieldCheck,
	Store,
	UserRound,
	Wallet,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const loading = ref(false)
const result = ref(null)

const modal = reactive({
	open: false,
	type: 'success',
	title: '',
	message: '',
})

const form = reactive({
	full_name: '',
	display_name: '',
	email: '',
	birth_date: '',
	country: '',
	city: '',
	whatsapp: '',
	main_specialty: '',
	years_of_experience: '',
	professional_bio: '',
	topics_to_teach: '',
	first_course_idea: '',
	target_audience: '',
	wants_to_charge: true,
	estimated_course_price: '',
	accepts_plus_program: false,
	plus_discount_percent: '',
	portfolio_url: '',
	linkedin_url: '',
	tiktok_url: '',
	youtube_url: '',
	website_url: '',
	additional_message: '',
	accepts_instructor_terms: false,
	confirms_truthful_information: false,
	confirms_adult: false,
})

const benefits = [
	{
		title: __('Gana por tus cursos'),
		body: __('Recibe hasta 95% por ventas propias y 80% por ventas generadas desde StudyBadge.'),
		icon: DollarSign,
	},
	{
		title: __('Publica sin costo inicial'),
		body: __('Crea cursos, organiza lecciones y envía tu contenido a revisión antes de publicarlo.'),
		icon: Store,
	},
	{
		title: __('Retiros simples'),
		body: __('Configura tu cuenta en el panel privado y solicita retiros desde S/20 cuando tengas ganancias disponibles.'),
		icon: Wallet,
	},
]

const steps = [
	{ number: '1', title: __('Postula'), body: __('Completa el formulario con tus datos y experiencia principal.') },
	{ number: '2', title: __('Revisión'), body: __('Evaluamos tu perfil y verificamos que encaje con la plataforma.') },
	{ number: '3', title: __('Crea'), body: __('Accede al panel y estructura tu primer curso con apoyo de StudyBadge.') },
	{ number: '4', title: __('Publica'), body: __('Tu curso pasa por revisión de calidad antes de salir al catálogo.') },
]

const legal = [
	{ key: 'accepts_instructor_terms', label: __('Acepto los términos del programa de instructores.') },
	{ key: 'confirms_truthful_information', label: __('Declaro que la información enviada es verdadera.') },
	{ key: 'confirms_adult', label: __('Declaro que soy mayor de edad.') },
]

watch(
	() => form.accepts_plus_program,
	(value) => {
		if (value && !form.plus_discount_percent) {
			form.plus_discount_percent = '10'
		}
		if (!value) {
			form.plus_discount_percent = ''
		}
	}
)

const statusTitle = computed(() => {
	if (!result.value) return ''
	if (result.value.status === 'Approved') return __('Tu perfil fue aprobado')
	if (result.value.status === 'Rejected') return __('Resultado de tu postulación')
	return __('Postulación recibida')
})

const resultMessage = computed(() => {
	if (!result.value) return ''
	if (result.value.status === 'Approved') {
		return __('Te enviaremos por correo los siguientes pasos para crear tu primer curso.')
	}
	if (result.value.status === 'Rejected') {
		return __('Gracias por postular. Te avisaremos por correo si necesitamos más información.')
	}
	return __('Recibimos tu postulación. Te avisaremos por correo cuando tengamos una respuesta.')
})

const openModal = (type, title, message) => {
	modal.type = type
	modal.title = title
	modal.message = message
	modal.open = true
}

const closeModal = () => {
	modal.open = false
}

const submit = async () => {
	if (loading.value) return

	loading.value = true
	result.value = null

	openModal(
		'sending',
		__('Postulación enviada'),
		__('Estamos registrando tu información. Puedes cerrar esta ventana; si ocurre un error, te avisaremos para reintentar o escribir a soporte@studybadge.com.')
	)

	try {
		const response = await call('studybadge_ai.instructor_review.submit_application', {
			data: { ...form },
		})

		result.value = response

		openModal(
			'success',
			statusTitle.value || __('Postulación recibida'),
			resultMessage.value || __('Recibimos tu postulación correctamente. Te avisaremos por correo cuando tengamos una respuesta.')
		)

		toast.success(__('Postulación enviada correctamente'))
	} catch (error) {
		const message =
			error?.messages?.[0] ||
			error?.message ||
			__('No pudimos enviar la postulación. Intenta nuevamente o escríbenos a soporte@studybadge.com.')

		openModal(
			'error',
			__('No pudimos completar el envío'),
			message
		)

		toast.error(message)
	} finally {
		loading.value = false
	}
}

usePageMeta(() => ({
	title: __('Enseña en StudyBadge'),
	icon: brand.favicon,
}))
</script>

<style scoped>
.teach-page {
	--sb-blue: #0a2352;
	--sb-blue-2: #0d3779;
	--sb-blue-3: #0f5fbf;
	--sb-gold: #d8a538;
	--sb-gold-soft: #fff3cf;
	--sb-ink: #172033;
	--sb-muted: #667085;
	--sb-soft: #f4f7fb;
	--sb-soft-2: #edf4ff;
	--sb-line: #dbe6f3;
	--sb-white: #ffffff;
	--sb-green: #079455;
	--sb-red: #b42318;
	--sb-shadow: 0 24px 70px rgba(10, 35, 82, 0.14);
	--sb-shadow-soft: 0 14px 36px rgba(10, 35, 82, 0.08);
	min-height: 100vh;
	background:
		radial-gradient(circle at 14% 8%, rgba(216, 165, 56, 0.18), transparent 26%),
		linear-gradient(180deg, #f8fbff 0%, #f4f7fb 48%, #ffffff 100%);
	color: var(--sb-ink);
	overflow-x: hidden;
}

.size-4 {
	width: 1rem;
	height: 1rem;
}

.size-5 {
	width: 1.25rem;
	height: 1.25rem;
}

.size-6 {
	width: 1.5rem;
	height: 1.5rem;
}

.teach-hero {
	position: relative;
	isolation: isolate;
	overflow: hidden;
	background:
		linear-gradient(135deg, rgba(10, 35, 82, 0.98) 0%, rgba(8, 31, 72, 0.98) 48%, rgba(13, 55, 121, 0.96) 100%),
		url('/assets/lms/images/wallpaper.png') center/cover no-repeat;
	color: white;
}

.hero-grid-bg {
	position: absolute;
	inset: 0;
	z-index: -2;
	background:
		radial-gradient(circle at 78% 12%, rgba(216, 165, 56, 0.24), transparent 27%),
		radial-gradient(circle at 16% 74%, rgba(255, 255, 255, 0.11), transparent 32%),
		linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px),
		linear-gradient(180deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
	background-size: auto, auto, 58px 58px, 58px 58px;
	mask-image: linear-gradient(180deg, #000 0%, rgba(0, 0, 0, 0.74) 66%, transparent 100%);
}

.teach-hero::after {
	content: '';
	position: absolute;
	width: 620px;
	height: 620px;
	right: -260px;
	top: -240px;
	border-radius: 999px;
	border: 1px solid rgba(255, 255, 255, 0.15);
	box-shadow: inset 0 0 0 82px rgba(255, 255, 255, 0.035);
	z-index: -1;
}

.topbar {
	position: relative;
	z-index: 1;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 18px;
	max-width: 1180px;
	margin: 0 auto;
	padding: 20px 22px;
}

.brand {
	display: inline-flex;
	align-items: center;
	gap: 12px;
	color: white;
	text-decoration: none;
	font-size: 20px;
	font-weight: 900;
	letter-spacing: -0.03em;
}

.brand:hover {
	color: white;
	text-decoration: none;
}

.brand-logo {
	width: 42px;
	height: 42px;
	display: grid;
	place-items: center;
	border-radius: 14px;
	background: rgba(255, 255, 255, 0.96);
	color: var(--sb-blue);
	box-shadow: 0 14px 34px rgba(0, 0, 0, 0.16);
	overflow: hidden;
}

.brand-logo img {
	width: 30px;
	height: 30px;
	object-fit: contain;
}

.topbar-actions {
	display: flex;
	align-items: center;
	gap: 10px;
}

.login-link,
.topbar-cta,
.primary-link,
.secondary-link {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	border-radius: 999px;
	font-weight: 850;
	text-decoration: none;
	transition: transform 0.2s ease, background 0.2s ease, color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.login-link {
	min-height: 42px;
	padding: 0 16px;
	color: rgba(255, 255, 255, 0.9);
	background: rgba(255, 255, 255, 0.09);
	border: 1px solid rgba(255, 255, 255, 0.16);
	backdrop-filter: blur(14px);
	-webkit-backdrop-filter: blur(14px);
}

.login-link:hover {
	color: white;
	background: rgba(255, 255, 255, 0.15);
	text-decoration: none;
	transform: translateY(-1px);
}

.topbar-cta {
	min-height: 42px;
	padding: 0 16px;
	background: white;
	color: var(--sb-blue);
	box-shadow: 0 14px 32px rgba(0, 0, 0, 0.14);
}

.topbar-cta:hover {
	color: var(--sb-blue);
	text-decoration: none;
	transform: translateY(-1px);
}

.hero-inner {
	position: relative;
	z-index: 1;
	display: grid;
	grid-template-columns: minmax(0, 1.08fr) minmax(340px, 0.72fr);
	gap: 48px;
	align-items: center;
	max-width: 1180px;
	margin: 0 auto;
	padding: 72px 22px 128px;
}

.eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	padding: 8px 12px;
	border-radius: 999px;
	background: rgba(216, 165, 56, 0.15);
	border: 1px solid rgba(216, 165, 56, 0.30);
	color: #ffe7a8;
	font-size: 12px;
	font-weight: 900;
	text-transform: uppercase;
	letter-spacing: 0.06em;
}

.hero-copy h1 {
	max-width: 760px;
	margin: 18px 0 20px;
	font-size: clamp(42px, 6vw, 76px);
	line-height: 0.94;
	font-weight: 950;
	letter-spacing: -0.06em;
	color: white;
}

.lead {
	max-width: 690px;
	margin: 0;
	font-size: clamp(17px, 2vw, 20px);
	line-height: 1.72;
	color: rgba(231, 239, 255, 0.84);
}

.hero-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	margin-top: 34px;
}

.primary-link {
	min-height: 52px;
	padding: 0 22px;
	background: white;
	color: var(--sb-blue);
	box-shadow: 0 18px 36px rgba(0, 0, 0, 0.18);
}

.primary-link:hover {
	color: var(--sb-blue);
	text-decoration: none;
	transform: translateY(-2px);
	box-shadow: 0 22px 44px rgba(0, 0, 0, 0.22);
}

.secondary-link {
	min-height: 52px;
	padding: 0 21px;
	color: white;
	border: 1px solid rgba(255, 255, 255, 0.26);
	background: rgba(255, 255, 255, 0.08);
	backdrop-filter: blur(12px);
	-webkit-backdrop-filter: blur(12px);
}

.secondary-link:hover {
	color: white;
	text-decoration: none;
	background: rgba(255, 255, 255, 0.14);
	transform: translateY(-2px);
}

.hero-proof {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
	margin-top: 26px;
}

.proof-item {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	padding: 9px 12px;
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.09);
	border: 1px solid rgba(255, 255, 255, 0.12);
	color: rgba(255, 255, 255, 0.86);
	font-size: 13px;
	font-weight: 780;
}

.proof-item svg {
	color: #f6d27b;
}

.hero-panel {
	align-self: stretch;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	gap: 18px;
	padding: 24px;
	border-radius: 30px;
	background: rgba(255, 255, 255, 0.12);
	border: 1px solid rgba(255, 255, 255, 0.18);
	box-shadow: 0 26px 70px rgba(0, 0, 0, 0.20);
	backdrop-filter: blur(18px);
	-webkit-backdrop-filter: blur(18px);
	overflow: hidden;
}

.panel-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 16px;
}

.panel-header span {
	display: block;
	color: rgba(255, 255, 255, 0.68);
	font-size: 13px;
	font-weight: 800;
}

.panel-header strong {
	display: block;
	margin-top: 5px;
	color: white;
	font-size: 22px;
	line-height: 1.18;
	font-weight: 920;
	letter-spacing: -0.03em;
}

.panel-badge {
	width: 50px;
	height: 50px;
	display: grid;
	place-items: center;
	border-radius: 18px;
	background: var(--sb-gold);
	color: var(--sb-blue);
	box-shadow: 0 16px 34px rgba(216, 165, 56, 0.26);
	flex-shrink: 0;
}

.panel-stats {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 12px;
}

.panel-stat {
	padding: 18px;
	border-radius: 22px;
	background: rgba(255, 255, 255, 0.13);
	border: 1px solid rgba(255, 255, 255, 0.15);
}

.panel-stat span,
.panel-stat small {
	display: block;
	color: rgba(255, 255, 255, 0.70);
	font-size: 12px;
	font-weight: 850;
}

.panel-stat strong {
	display: block;
	margin: 8px 0 4px;
	color: white;
	font-size: 44px;
	line-height: 1;
	font-weight: 950;
	letter-spacing: -0.06em;
}

.panel-list {
	display: grid;
	gap: 10px;
}

.panel-line {
	display: grid;
	grid-template-columns: 38px minmax(0, 1fr);
	gap: 12px;
	align-items: center;
	padding: 13px;
	border-radius: 18px;
	background: rgba(255, 255, 255, 0.10);
	border: 1px solid rgba(255, 255, 255, 0.12);
	color: rgba(255, 255, 255, 0.84);
	font-size: 13px;
	font-weight: 740;
	line-height: 1.45;
}

.panel-line svg {
	width: 38px;
	height: 38px;
	padding: 9px;
	border-radius: 14px;
	background: rgba(255, 255, 255, 0.12);
	color: #f6d27b;
}

.content {
	max-width: 1180px;
	margin: 0 auto;
	padding: 0 22px 86px;
}

.program-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 18px;
	margin-top: -58px;
	position: relative;
	z-index: 2;
}

.program-card,
.plus-band,
.application-card,
.sticky-card {
	background: rgba(255, 255, 255, 0.94);
	border: 1px solid rgba(219, 230, 243, 0.94);
	border-radius: 26px;
	box-shadow: var(--sb-shadow-soft);
	backdrop-filter: blur(14px);
	-webkit-backdrop-filter: blur(14px);
}

.program-card {
	position: relative;
	padding: 24px;
	overflow: hidden;
	transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}


.program-card:hover {
	transform: translateY(-4px);
	border-color: rgba(10, 35, 82, 0.18);
	box-shadow: 0 22px 52px rgba(10, 35, 82, 0.12);
}

.icon-box,
.plus-icon,
.form-header-icon,
.result-icon {
	width: 46px;
	height: 46px;
	display: grid;
	place-items: center;
	border-radius: 16px;
	background: #eaf1fb;
	color: var(--sb-blue);
}

.program-card h2 {
	margin: 18px 0 9px;
	font-size: 18px;
	line-height: 1.2;
	font-weight: 920;
	color: var(--sb-ink);
	letter-spacing: -0.02em;
}

.program-card p,
.plus-band p,
.form-intro p {
	margin: 0;
	color: var(--sb-muted);
	line-height: 1.65;
}

.plus-band {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr) auto;
	gap: 20px;
	align-items: center;
	margin-top: 24px;
	padding: 26px;
	overflow: hidden;
}

.plus-icon {
	background: var(--sb-gold-soft);
	color: #9a6a15;
}

.section-kicker {
	margin: 0 0 6px !important;
	text-transform: uppercase;
	font-size: 12px;
	font-weight: 950;
	letter-spacing: 0.07em;
	color: var(--sb-blue) !important;
}

.plus-band h2,
.form-intro h2,
.form-card-header h2 {
	margin: 0 0 10px;
	font-size: clamp(24px, 3vw, 30px);
	line-height: 1.12;
	font-weight: 950;
	letter-spacing: -0.04em;
	color: var(--sb-ink);
}

.plus-metrics {
	display: flex;
	align-items: center;
	gap: 8px;
	flex-wrap: wrap;
}

.plus-metrics span {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-width: 58px;
	height: 40px;
	border-radius: 999px;
	background: var(--sb-blue);
	color: white;
	font-weight: 920;
	box-shadow: 0 12px 26px rgba(10, 35, 82, 0.18);
}

.form-layout {
	display: grid;
	grid-template-columns: minmax(280px, 0.76fr) minmax(0, 1.24fr);
	gap: 24px;
	margin-top: 24px;
	align-items: start;
}

.form-intro {
	min-width: 0;
}

.sticky-card {
	position: sticky;
	top: 18px;
	padding: 26px;
}

.timeline {
	display: grid;
	gap: 15px;
	margin-top: 24px;
	position: relative;
}

.timeline::before {
	content: '';
	position: absolute;
	left: 17px;
	top: 12px;
	bottom: 12px;
	width: 2px;
	background: #dfe8f5;
}

.timeline-item {
	position: relative;
	display: grid;
	grid-template-columns: 36px minmax(0, 1fr);
	gap: 13px;
}

.timeline-item > span {
	position: relative;
	z-index: 1;
	width: 36px;
	height: 36px;
	display: grid;
	place-items: center;
	border-radius: 50%;
	background: var(--sb-blue);
	color: white;
	font-weight: 950;
	box-shadow: 0 10px 24px rgba(10, 35, 82, 0.18);
}

.timeline-item strong {
	display: block;
	color: var(--sb-ink);
	font-weight: 920;
}

.timeline-item p {
	font-size: 13px;
	margin-top: 3px;
}

.support-card {
	display: grid;
	grid-template-columns: 42px minmax(0, 1fr);
	gap: 12px;
	align-items: start;
	margin-top: 24px;
	padding: 15px;
	border-radius: 20px;
	background: #f7fbff;
	border: 1px solid #e2ebf7;
}

.support-card svg {
	width: 42px;
	height: 42px;
	padding: 10px;
	border-radius: 15px;
	background: var(--sb-gold-soft);
	color: #9a6a15;
}

.support-card strong {
	display: block;
	color: var(--sb-ink);
	font-weight: 920;
}

.support-card span {
	display: block;
	margin-top: 3px;
	color: var(--sb-muted);
	font-size: 13px;
	line-height: 1.45;
}

.support-card a {
	display: inline-flex;
	width: fit-content;
	margin-top: 8px;
	color: var(--sb-blue);
	font-size: 13px;
	font-weight: 850;
	text-decoration: none;
}

.support-card a:hover {
	color: var(--sb-blue-soft);
	text-decoration: underline;
}

.application-card {
	padding: 28px;
	display: grid;
	gap: 24px;
	box-shadow: var(--sb-shadow);
}

.form-card-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 18px;
	padding-bottom: 22px;
	border-bottom: 1px solid #e7eef8;
}

.form-card-header span {
	display: block;
	color: var(--sb-muted);
	line-height: 1.55;
}

.form-header-icon {
	background: var(--sb-blue);
	color: white;
	flex-shrink: 0;
}

.form-section {
	display: grid;
	gap: 15px;
}

.form-section-title {
	display: flex;
	align-items: center;
	gap: 9px;
	color: var(--sb-blue);
}

.form-section-title h3 {
	margin: 0;
	font-size: 15px;
	font-weight: 950;
	letter-spacing: -0.01em;
}

.field-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 15px;
}

.application-card :deep(label),
.application-card :deep(.text-sm) {
	font-weight: 820;
	color: #344054;
}

.application-card :deep(input),
.application-card :deep(textarea),
.application-card :deep(select) {
	border-radius: 15px !important;
	border-color: #d7e2f0 !important;
	background: #fbfdff !important;
	color: var(--sb-ink) !important;
	box-shadow: none !important;
	transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.application-card :deep(input:focus),
.application-card :deep(textarea:focus),
.application-card :deep(select:focus) {
	border-color: var(--sb-blue) !important;
	box-shadow: 0 0 0 4px rgba(10, 35, 82, 0.10) !important;
	background: white !important;
}

.option-row {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 14px;
}

.option-card {
	position: relative;
	display: grid;
	grid-template-columns: 26px minmax(0, 1fr);
	gap: 12px;
	align-items: start;
	border: 1px solid #dbe6f3;
	border-radius: 20px;
	padding: 16px;
	background: #f8fbff;
	cursor: pointer;
	transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

.option-card:hover {
	transform: translateY(-2px);
	border-color: rgba(10, 35, 82, 0.20);
	box-shadow: 0 14px 30px rgba(10, 35, 82, 0.08);
}

.plus-option {
	background: linear-gradient(180deg, #fffaf0 0%, #f7fbff 100%);
	border-color: #ead9a8;
}

.option-card input {
	position: absolute;
	opacity: 0;
	pointer-events: none;
}

.option-check {
	width: 26px;
	height: 26px;
	display: grid;
	place-items: center;
	border-radius: 999px;
	background: white;
	border: 1px solid #cfdcec;
	color: #98a6ba;
	transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.option-card input:checked + .option-check {
	background: var(--sb-blue);
	border-color: var(--sb-blue);
	color: white;
}

.option-card strong {
	display: block;
	color: var(--sb-ink);
	font-weight: 920;
}

.option-card small {
	display: block;
	margin-top: 4px;
	color: var(--sb-muted);
	line-height: 1.45;
}

.plus-choice {
	border: 1px solid #dbe6f3;
	border-radius: 20px;
	padding: 16px;
	background: #f8fbff;
}

.field-label {
	display: block;
	font-size: 12px;
	font-weight: 900;
	color: #506178;
	margin-bottom: 10px;
	text-transform: uppercase;
	letter-spacing: 0.04em;
}

.discount-options {
	display: flex;
	gap: 10px;
	flex-wrap: wrap;
}

.discount-options label {
	cursor: pointer;
}

.discount-options input {
	position: absolute;
	opacity: 0;
}

.discount-options span {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-width: 68px;
	border: 1px solid #c9d6e6;
	border-radius: 999px;
	padding: 9px 16px;
	color: var(--sb-blue);
	background: white;
	font-weight: 900;
	transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.discount-options input:checked + span {
	background: var(--sb-blue);
	border-color: var(--sb-blue);
	color: white;
	transform: translateY(-1px);
}

.optional-details {
	border: 1px solid #dbe6f3;
	border-radius: 20px;
	background: #fbfdff;
	overflow: hidden;
}

.optional-details summary {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 12px;
	padding: 17px;
	cursor: pointer;
	font-weight: 900;
	color: var(--sb-blue);
	list-style: none;
}

.optional-details summary::-webkit-details-marker {
	display: none;
}

.optional-details summary svg {
	transition: transform 0.2s ease;
}

.optional-details[open] summary svg {
	transform: rotate(180deg);
}

.optional-body {
	display: grid;
	gap: 15px;
	padding: 0 17px 17px;
}

.legal-box {
	display: grid;
	gap: 10px;
	padding: 16px;
	border-radius: 20px;
	background: #f5f8fc;
	border: 1px solid #e1eaf5;
}

.check-row {
	display: flex;
	align-items: flex-start;
	gap: 10px;
	color: #344054;
	font-weight: 720;
	line-height: 1.45;
}

.check-row input {
	margin-top: 3px;
	width: 17px;
	height: 17px;
	accent-color: var(--sb-blue);
	flex-shrink: 0;
}

.result-box {
	display: grid;
	grid-template-columns: 42px minmax(0, 1fr);
	gap: 12px;
	align-items: start;
	border-radius: 20px;
	padding: 15px;
	background: #eff6ff;
	border: 1px solid #bfdbfe;
	color: var(--sb-blue);
}

.result-box strong,
.result-box span {
	display: block;
}

.result-box span {
	margin-top: 3px;
	line-height: 1.45;
}

.status-Rejected {
	background: #fff1f3;
	border-color: #fecdd6;
	color: var(--sb-red);
}

.status-Approved {
	background: #ecfdf3;
	border-color: #abefc6;
	color: var(--sb-green);
}

.submit-row {
	display: flex;
	align-items: center;
	gap: 16px;
	flex-wrap: wrap;
	padding-top: 4px;
}

.submit-row p {
	margin: 0;
	color: var(--sb-muted);
	font-size: 13px;
	line-height: 1.45;
	max-width: 420px;
}

.submit-button {
	min-height: 52px;
	border-radius: 999px !important;
	background: var(--sb-blue) !important;
	border-color: var(--sb-blue) !important;
	color: white !important;
	font-weight: 900 !important;
	padding-left: 24px !important;
	padding-right: 24px !important;
	box-shadow: 0 16px 32px rgba(10, 35, 82, 0.18);
}

.submit-button:hover {
	filter: brightness(1.06);
}

.modal-backdrop {
	position: fixed;
	inset: 0;
	z-index: 9999;
	display: grid;
	place-items: center;
	padding: 22px;
	background: rgba(6, 18, 42, 0.50);
	backdrop-filter: blur(10px);
	-webkit-backdrop-filter: blur(10px);
}

.modal-card {
	width: min(460px, 100%);
	display: grid;
	grid-template-columns: 54px minmax(0, 1fr);
	gap: 16px;
	padding: 22px;
	border-radius: 28px;
	background: white;
	border: 1px solid rgba(219, 230, 243, 0.95);
	box-shadow: 0 34px 90px rgba(6, 18, 42, 0.28);
}

.modal-icon {
	width: 54px;
	height: 54px;
	display: grid;
	place-items: center;
	border-radius: 18px;
	background: #eef4ff;
	color: var(--sb-blue);
}

.modal-success .modal-icon {
	background: #ecfdf3;
	color: var(--sb-green);
}

.modal-error .modal-icon {
	background: #fff1f3;
	color: var(--sb-red);
}

.modal-sending .modal-icon {
	background: var(--sb-gold-soft);
	color: #9a6a15;
}

.modal-spinner {
	animation: spin 1s linear infinite;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

.modal-content h3 {
	margin: 0 0 7px;
	color: var(--sb-ink);
	font-size: 21px;
	line-height: 1.18;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.modal-content p {
	margin: 0;
	color: var(--sb-muted);
	line-height: 1.6;
}

.modal-actions {
	display: flex;
	justify-content: flex-end;
	gap: 10px;
	margin-top: 18px;
	flex-wrap: wrap;
}

.modal-button {
	min-height: 42px;
	border: 0;
	border-radius: 999px;
	padding: 0 16px;
	background: var(--sb-blue);
	color: white;
	font-weight: 900;
	cursor: pointer;
	transition: transform 0.2s ease, filter 0.2s ease;
}

.modal-button:hover {
	transform: translateY(-1px);
	filter: brightness(1.06);
}

.modal-button.muted {
	background: #eef4fb;
	color: var(--sb-blue);
}

@media (max-width: 980px) {
	.hero-inner,
	.program-grid,
	.form-layout {
		grid-template-columns: 1fr;
	}

	.hero-inner {
		padding-bottom: 104px;
	}

	.program-grid {
		margin-top: -46px;
	}

	.sticky-card {
		position: static;
	}

	.plus-band {
		grid-template-columns: auto minmax(0, 1fr);
	}

	.plus-metrics {
		grid-column: 1 / -1;
	}
}

@media (max-width: 720px) {
	.topbar {
		align-items: flex-start;
	}

	.topbar-actions {
		flex-direction: column;
		align-items: stretch;
	}

	.login-link,
	.topbar-cta {
		min-height: 38px;
		padding: 0 12px;
		font-size: 13px;
	}

	.hero-inner {
		padding-top: 44px;
	}

	.hero-copy h1 {
		font-size: clamp(38px, 12vw, 54px);
	}

	.hero-panel,
	.field-grid,
	.option-row {
		grid-template-columns: 1fr;
	}

	.panel-stats {
		grid-template-columns: 1fr 1fr;
	}

	.application-card,
	.sticky-card,
	.plus-band,
	.program-card {
		padding: 20px;
		border-radius: 22px;
	}

	.form-card-header {
		display: grid;
	}

	.form-header-icon {
		display: none;
	}

	.submit-row {
		display: grid;
	}

	.submit-button {
		width: 100%;
	}

	.modal-card {
		grid-template-columns: 1fr;
		text-align: left;
	}

	.modal-actions {
		justify-content: stretch;
	}

	.modal-button {
		flex: 1;
	}
}

@media (max-width: 480px) {
	.brand span:last-child {
		display: none;
	}

	.panel-stats {
		grid-template-columns: 1fr;
	}

	.hero-actions,
	.hero-actions a {
		width: 100%;
	}

	.primary-link,
	.secondary-link {
		width: 100%;
	}

	.plus-band {
		grid-template-columns: 1fr;
	}

	.plus-icon {
		width: 42px;
		height: 42px;
	}
}
</style>

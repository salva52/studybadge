<template>
	<div class="teach-page">
		<header class="hero">
			<nav class="topbar">
				<div class="brand">
					<img v-if="brand.favicon" :src="brand.favicon" alt="StudyBadge" />
					<span>StudyBadge</span>
				</div>
				<a href="/login" class="login-link">{{ __('Iniciar sesion') }}</a>
			</nav>

			<div class="hero-inner">
				<section class="hero-copy">
					<div class="eyebrow">
						<GraduationCap class="size-4" />
						{{ __('Programa de instructores') }}
					</div>
					<h1>{{ __('Ensena en StudyBadge') }}</h1>
					<p class="lead">
						{{ __('Convierte tu experiencia en cursos practicos, llega a mas estudiantes y gana por cada venta aprobada en la plataforma.') }}
					</p>
					<div class="hero-actions">
						<a href="#postula" class="primary-link">{{ __('Postular ahora') }}</a>
						<a href="#plus" class="secondary-link">{{ __('Ver programa Plus') }}</a>
					</div>
				</section>

				<section class="hero-panel">
					<div class="panel-stat">
						<span>{{ __('Ventas propias') }}</span>
						<strong>95%</strong>
					</div>
					<div class="panel-stat">
						<span>{{ __('Ventas StudyBadge') }}</span>
						<strong>80%</strong>
					</div>
					<div class="panel-line">
						<Wallet class="size-5" />
						<span>{{ __('Retiros desde S/20. Maximo 72 horas.') }}</span>
					</div>
					<div class="panel-line">
						<ShieldCheck class="size-5" />
						<span>{{ __('Tus cursos pasan por revision de calidad antes de publicarse.') }}</span>
					</div>
				</section>
			</div>
		</header>

		<main class="content">
			<section class="program-grid">
				<article v-for="item in benefits" :key="item.title" class="program-card">
					<div class="icon-box"><component :is="item.icon" class="size-5" /></div>
					<h2>{{ item.title }}</h2>
					<p>{{ item.body }}</p>
				</article>
			</section>

			<section id="plus" class="plus-band">
				<div class="plus-icon"><BadgePercent class="size-6" /></div>
				<div>
					<p class="section-kicker">{{ __('StudyBadge Plus') }}</p>
					<h2>{{ __('Un programa para vender mas rapido') }}</h2>
					<p>
						{{ __('Plus ayuda a que tus cursos sean mas atractivos para estudiantes con descuentos automaticos para miembros Plus. Tu decides si quieres participar y el descuento sugerido: 10%, 15% o 20%.') }}
					</p>
				</div>
			</section>

			<section id="postula" class="form-layout">
				<aside class="form-intro">
					<p class="section-kicker">{{ __('Postulacion') }}</p>
					<h2>{{ __('Solo necesitamos lo esencial para empezar') }}</h2>
					<p>
						{{ __('Luego, si tu perfil es aprobado, podras completar datos de retiro y gestionar tus cursos desde tu panel privado.') }}
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
				</aside>

				<form class="application-card" @submit.prevent="submit">
					<div class="form-section">
						<div class="form-section-title">
							<UserRound class="size-4" />
							<h3>{{ __('Datos basicos') }}</h3>
						</div>
						<div class="field-grid">
							<FormControl v-model="form.full_name" :label="__('Nombre completo')" required />
							<FormControl v-model="form.display_name" :label="__('Nombre de instructor')" required />
							<FormControl v-model="form.email" :label="__('Email')" type="email" required />
							<FormControl v-model="form.birth_date" :label="__('Fecha de nacimiento')" type="date" required />
							<FormControl v-model="form.country" :label="__('Pais')" required />
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
						<FormControl v-model="form.topics_to_teach" :label="__('Que cursos quieres ensenar')" type="textarea" :rows="3" required />
						<FormControl v-model="form.first_course_idea" :label="__('Primera idea de curso')" type="textarea" :rows="3" required />
					</div>

					<div class="option-row">
						<label class="option-card">
							<input v-model="form.wants_to_charge" type="checkbox" />
							<span>
								<strong>{{ __('Quiero vender cursos') }}</strong>
								<small>{{ __('Podras definir precio al crear cada curso.') }}</small>
							</span>
						</label>
						<label class="option-card plus-option">
							<input v-model="form.accepts_plus_program" type="checkbox" />
							<span>
								<strong>{{ __('Participar en Plus') }}</strong>
								<small>{{ __('Descuentos automaticos para vender mas rapido.') }}</small>
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
							<span>{{ __('Agregar mas informacion opcional') }}</span>
							<ChevronDown class="size-4" />
						</summary>
						<div class="optional-body">
							<div class="field-grid">
								<FormControl v-model="form.whatsapp" label="WhatsApp" />
								<FormControl v-model="form.years_of_experience" :label="__('Anos de experiencia')" type="number" />
								<FormControl v-model="form.target_audience" :label="__('Publico objetivo')" />
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
						<strong>{{ statusTitle }}</strong>
						<span>{{ resultMessage }}</span>
					</div>

					<Button variant="solid" size="lg" :loading="loading" type="submit" class="submit-button">
						{{ __('Enviar postulacion') }}
					</Button>
				</form>
			</section>
		</main>
	</div>
</template>

<script setup>
import { Button, FormControl, call, toast, usePageMeta } from 'frappe-ui'
import { computed, reactive, ref, watch } from 'vue'
import {
	BadgePercent,
	BookOpenCheck,
	ChevronDown,
	DollarSign,
	GraduationCap,
	ShieldCheck,
	Store,
	UserRound,
	Wallet,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const loading = ref(false)
const result = ref(null)

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
		body: __('Crea cursos, organiza lecciones y envia tu contenido a revision antes de publicarlo.'),
		icon: Store,
	},
	{
		title: __('Retiros simples'),
		body: __('Configura tu cuenta en el panel privado y solicita retiros desde S/20.'),
		icon: Wallet,
	},
]

const steps = [
	{ number: '1', title: __('Postula'), body: __('Completa el formulario con lo esencial.') },
	{ number: '2', title: __('Revision'), body: __('Revisamos tu perfil y te avisamos por correo.') },
	{ number: '3', title: __('Crea'), body: __('Accede al panel y arma tu primer curso.') },
	{ number: '4', title: __('Publica'), body: __('El curso pasa por revision de calidad antes de salir al catalogo.') },
]

const legal = [
	{ key: 'accepts_instructor_terms', label: __('Acepto los terminos del programa de instructores.') },
	{ key: 'confirms_truthful_information', label: __('Declaro que la informacion enviada es verdadera.') },
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
	if (result.value.status === 'Rejected') return __('Resultado de tu postulacion')
	return __('Postulacion recibida')
})

const resultMessage = computed(() => {
	if (!result.value) return ''
	if (result.value.status === 'Approved') {
		return __('Te enviamos por correo los siguientes pasos para crear tu primer curso.')
	}
	if (result.value.status === 'Rejected') {
		return __('Gracias por postular. Te avisaremos por correo si necesitamos mas informacion.')
	}
	return __('Recibimos tu postulacion. Te avisaremos por correo cuando tengamos una respuesta.')
})

const submit = async () => {
	loading.value = true
	result.value = null
	try {
		result.value = await call('studybadge_ai.instructor_review.submit_application', {
			data: { ...form },
		})
		toast.success(__('Postulacion enviada correctamente'))
	} catch (error) {
		toast.error(error.messages?.[0] || __('No pudimos enviar la postulacion'))
	} finally {
		loading.value = false
	}
}

usePageMeta(() => ({
	title: __('Ensena en StudyBadge'),
	icon: brand.favicon,
}))
</script>

<style scoped>
.teach-page {
	min-height: 100vh;
	background: #f4f7fb;
	color: #172033;
}
.hero {
	position: relative;
	overflow: hidden;
	background:
		linear-gradient(140deg, rgba(10, 35, 82, 0.96), rgba(11, 69, 134, 0.9)),
		url('/assets/lms/images/wallpaper.png') center/cover no-repeat;
	color: white;
}
.hero::after {
	content: '';
	position: absolute;
	inset: auto -10% -36% 42%;
	height: 360px;
	background: radial-gradient(circle, rgba(255, 255, 255, 0.2), transparent 64%);
	pointer-events: none;
}
.topbar {
	position: relative;
	z-index: 1;
	display: flex;
	align-items: center;
	justify-content: space-between;
	max-width: 1180px;
	margin: 0 auto;
	padding: 18px 22px;
}
.brand {
	display: flex;
	align-items: center;
	gap: 10px;
	font-weight: 850;
	font-size: 20px;
}
.brand img {
	width: 34px;
	height: 34px;
}
.login-link,
.primary-link,
.secondary-link {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border-radius: 8px;
	font-weight: 800;
	text-decoration: none;
}
.login-link {
	color: white;
	border: 1px solid rgba(255, 255, 255, 0.35);
	padding: 9px 14px;
}
.hero-inner {
	position: relative;
	z-index: 1;
	display: grid;
	grid-template-columns: minmax(0, 1.08fr) minmax(300px, 0.72fr);
	gap: 44px;
	max-width: 1180px;
	margin: 0 auto;
	padding: 62px 22px 86px;
}
.eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	padding: 7px 10px;
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.12);
	border: 1px solid rgba(255, 255, 255, 0.18);
	font-size: 12px;
	font-weight: 850;
	text-transform: uppercase;
	letter-spacing: 0;
}
.hero-copy h1 {
	max-width: 680px;
	margin: 18px 0 18px;
	font-size: 58px;
	line-height: 0.98;
	font-weight: 920;
	letter-spacing: 0;
}
.lead {
	max-width: 660px;
	margin: 0;
	font-size: 19px;
	line-height: 1.65;
	color: rgba(255, 255, 255, 0.84);
}
.hero-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	margin-top: 30px;
}
.primary-link {
	background: white;
	color: #0A2352;
	padding: 12px 18px;
}
.secondary-link {
	color: white;
	border: 1px solid rgba(255, 255, 255, 0.3);
	padding: 11px 17px;
}
.hero-panel {
	align-self: end;
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 12px;
	padding: 16px;
	border-radius: 8px;
	background: rgba(255, 255, 255, 0.12);
	border: 1px solid rgba(255, 255, 255, 0.18);
	backdrop-filter: blur(14px);
}
.panel-stat,
.panel-line {
	background: rgba(255, 255, 255, 0.12);
	border: 1px solid rgba(255, 255, 255, 0.14);
	border-radius: 8px;
	padding: 14px;
}
.panel-stat span {
	display: block;
	font-size: 12px;
	color: rgba(255, 255, 255, 0.72);
	font-weight: 800;
}
.panel-stat strong {
	display: block;
	margin-top: 6px;
	font-size: 34px;
	line-height: 1;
}
.panel-line {
	grid-column: 1 / -1;
	display: flex;
	align-items: center;
	gap: 10px;
	color: rgba(255, 255, 255, 0.86);
	font-weight: 750;
}
.content {
	max-width: 1180px;
	margin: 0 auto;
	padding: 34px 22px 76px;
}
.program-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 16px;
	margin-top: -64px;
	position: relative;
	z-index: 2;
}
.program-card,
.plus-band,
.application-card,
.form-intro {
	background: white;
	border: 1px solid #e4e9f2;
	border-radius: 8px;
	box-shadow: 0 12px 34px rgba(10, 35, 82, 0.1);
}
.program-card {
	padding: 22px;
}
.icon-box,
.plus-icon {
	width: 42px;
	height: 42px;
	display: grid;
	place-items: center;
	border-radius: 8px;
	background: #eaf1fb;
	color: #0A2352;
}
.program-card h2 {
	margin: 16px 0 8px;
	font-size: 18px;
	font-weight: 900;
}
.program-card p,
.plus-band p,
.form-intro p {
	margin: 0;
	color: #5d697c;
	line-height: 1.6;
}
.plus-band {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr);
	gap: 18px;
	align-items: start;
	margin-top: 22px;
	padding: 24px;
}
.section-kicker {
	margin: 0 0 5px !important;
	text-transform: uppercase;
	font-size: 12px;
	font-weight: 900;
	color: #0A2352 !important;
}
.plus-band h2,
.form-intro h2 {
	margin: 0 0 10px;
	font-size: 25px;
	font-weight: 920;
	color: #172033;
}
.form-layout {
	display: grid;
	grid-template-columns: minmax(280px, 0.78fr) minmax(0, 1.22fr);
	gap: 22px;
	margin-top: 22px;
	align-items: start;
}
.form-intro {
	position: sticky;
	top: 18px;
	padding: 24px;
}
.timeline {
	display: grid;
	gap: 14px;
	margin-top: 22px;
}
.timeline-item {
	display: grid;
	grid-template-columns: 30px minmax(0, 1fr);
	gap: 12px;
}
.timeline-item > span {
	width: 30px;
	height: 30px;
	display: grid;
	place-items: center;
	border-radius: 50%;
	background: #0A2352;
	color: white;
	font-weight: 900;
}
.timeline-item strong {
	display: block;
	color: #172033;
}
.timeline-item p {
	font-size: 13px;
	margin-top: 3px;
}
.application-card {
	padding: 24px;
	display: grid;
	gap: 22px;
}
.form-section {
	display: grid;
	gap: 14px;
}
.form-section-title {
	display: flex;
	align-items: center;
	gap: 8px;
	color: #0A2352;
}
.form-section-title h3 {
	margin: 0;
	font-size: 15px;
	font-weight: 920;
}
.field-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 14px;
}
.option-row {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 14px;
}
.option-card {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr);
	gap: 12px;
	align-items: start;
	border: 1px solid #d9e2ef;
	border-radius: 8px;
	padding: 14px;
	background: #f8fbff;
	cursor: pointer;
}
.plus-option {
	background: #eef5ff;
	border-color: #c6d8ef;
}
.option-card input,
.check-row input {
	margin-top: 3px;
	width: 16px;
	height: 16px;
	accent-color: #0A2352;
}
.option-card strong {
	display: block;
	color: #172033;
}
.option-card small {
	display: block;
	margin-top: 3px;
	color: #667085;
	line-height: 1.4;
}
.plus-choice {
	border: 1px solid #d9e2ef;
	border-radius: 8px;
	padding: 14px;
	background: #f8fbff;
}
.field-label {
	display: block;
	font-size: 12px;
	font-weight: 800;
	color: #5d697c;
	margin-bottom: 10px;
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
	border: 1px solid #c9d6e6;
	border-radius: 999px;
	padding: 8px 14px;
	color: #0A2352;
	font-weight: 850;
}
.discount-options input:checked + span {
	background: #0A2352;
	border-color: #0A2352;
	color: white;
}
.optional-details {
	border: 1px solid #d9e2ef;
	border-radius: 8px;
	background: #fbfdff;
}
.optional-details summary {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 12px;
	padding: 15px;
	cursor: pointer;
	font-weight: 850;
	color: #0A2352;
	list-style: none;
}
.optional-details summary::-webkit-details-marker {
	display: none;
}
.optional-details[open] summary svg {
	transform: rotate(180deg);
}
.optional-body {
	display: grid;
	gap: 14px;
	padding: 0 15px 15px;
}
.legal-box {
	display: grid;
	gap: 9px;
	padding: 14px;
	border-radius: 8px;
	background: #f5f8fc;
	border: 1px solid #e4e9f2;
}
.check-row {
	display: flex;
	align-items: flex-start;
	gap: 10px;
	color: #344054;
	font-weight: 650;
}
.result-box {
	display: grid;
	gap: 4px;
	border-radius: 8px;
	padding: 14px;
	background: #eff6ff;
	border: 1px solid #bfdbfe;
	color: #0A2352;
}
.status-Rejected {
	background: #fff1f3;
	border-color: #fecdd6;
	color: #b42318;
}
.status-Approved {
	background: #ecfdf3;
	border-color: #abefc6;
	color: #067647;
}
.submit-button {
	justify-self: start;
	background: #0A2352;
}
@media (max-width: 920px) {
	.hero-inner,
	.program-grid,
	.form-layout {
		grid-template-columns: 1fr;
	}
	.program-grid {
		margin-top: -42px;
	}
	.form-intro {
		position: static;
	}
}
@media (max-width: 680px) {
	.hero-inner {
		padding-top: 40px;
	}
	.hero-copy h1 {
		font-size: 40px;
	}
	.hero-panel,
	.field-grid,
	.option-row {
		grid-template-columns: 1fr;
	}
	.application-card,
	.form-intro,
	.plus-band,
	.program-card {
		padding: 18px;
	}
}
</style>

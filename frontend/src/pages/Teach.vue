<template>
	<div class="teach-page">
		<header class="teach-hero">
			<nav class="teach-nav">
				<div class="teach-brand">
					<img v-if="brand.favicon" :src="brand.favicon" alt="StudyBadge" />
					<span>StudyBadge</span>
				</div>
				<a href="/login" class="teach-login">{{ __('Iniciar sesión') }}</a>
			</nav>
			<div class="teach-hero-inner">
				<section class="teach-copy">
					<p class="teach-kicker">{{ __('Programa de instructores') }}</p>
					<h1>{{ __('Enseña en StudyBadge') }}</h1>
					<p class="teach-lead">
						{{ __('Postula como instructor, crea cursos prácticos con apoyo de IA y gana por cada estudiante que aprende contigo.') }}
					</p>
					<div class="teach-benefits">
						<div v-for="benefit in benefits" :key="benefit.label" class="teach-benefit">
							<component :is="benefit.icon" class="size-5" />
							<span>{{ benefit.label }}</span>
						</div>
					</div>
				</section>
				<section class="teach-process">
					<div v-for="step in steps" :key="step.title" class="teach-step">
						<div class="teach-step-number">{{ step.number }}</div>
						<div>
							<h3>{{ step.title }}</h3>
							<p>{{ step.body }}</p>
						</div>
					</div>
				</section>
			</div>
		</header>

		<main class="teach-main">
			<section class="teach-form-shell">
				<div class="teach-form-heading">
					<p>{{ __('Postulación') }}</p>
					<h2>{{ __('Cuéntanos qué quieres enseñar') }}</h2>
				</div>
				<form class="teach-form" @submit.prevent="submit">
					<div class="teach-grid">
						<FormControl v-model="form.full_name" :label="__('Nombre completo')" required />
						<FormControl v-model="form.display_name" :label="__('Nombre para mostrar')" required />
						<FormControl v-model="form.email" :label="__('Email')" type="email" required />
						<FormControl v-model="form.birth_date" :label="__('Fecha de nacimiento')" type="date" required />
						<FormControl v-model="form.country" :label="__('País')" required />
						<FormControl v-model="form.city" :label="__('Ciudad')" required />
						<FormControl v-model="form.whatsapp" :label="__('WhatsApp opcional')" />
						<FormControl v-model="form.main_specialty" :label="__('Especialidad principal')" required />
						<FormControl v-model="form.years_of_experience" :label="__('Años de experiencia')" type="number" />
						<FormControl v-model="form.target_audience" :label="__('Público objetivo')" />
					</div>

					<FormControl v-model="form.professional_bio" :label="__('Biografía profesional')" type="textarea" :rows="5" required />
					<FormControl v-model="form.topics_to_teach" :label="__('Qué cursos quieres enseñar')" type="textarea" :rows="4" required />
					<FormControl v-model="form.first_course_idea" :label="__('Idea de curso')" type="textarea" :rows="4" required />

					<div class="teach-grid">
						<label class="teach-check">
							<input v-model="form.wants_to_charge" type="checkbox" />
							<span>{{ __('Quiero cobrar por mis cursos') }}</span>
						</label>
						<FormControl v-model="form.estimated_course_price" :label="__('Precio estimado')" type="number" />
						<label class="teach-check">
							<input v-model="form.accepts_plus_program" type="checkbox" />
							<span>{{ __('Acepto unirme al programa Plus') }}</span>
						</label>
						<div>
							<label class="teach-label">{{ __('Descuento Plus') }}</label>
							<select v-model="form.plus_discount_percent" class="teach-select">
								<option value="">{{ __('No aplica') }}</option>
								<option value="10">10%</option>
								<option value="15">15%</option>
								<option value="20">20%</option>
							</select>
						</div>
					</div>

					<div class="teach-grid">
						<FormControl v-model="form.portfolio_url" :label="__('Portafolio')" />
						<FormControl v-model="form.linkedin_url" label="LinkedIn" />
						<FormControl v-model="form.tiktok_url" label="TikTok" />
						<FormControl v-model="form.youtube_url" label="YouTube" />
						<FormControl v-model="form.website_url" :label="__('Web')" />
					</div>
					<FormControl v-model="form.additional_message" :label="__('Mensaje adicional')" type="textarea" :rows="4" />

					<div class="teach-legal">
						<label v-for="item in legal" :key="item.key" class="teach-check">
							<input v-model="form[item.key]" type="checkbox" required />
							<span>{{ item.label }}</span>
						</label>
					</div>

					<div v-if="result" class="teach-result" :class="`status-${result.status}`">
						<strong>{{ statusTitle }}</strong>
						<span>{{ result.ai_summary || __('Recibimos tu postulación y te avisaremos por correo.') }}</span>
					</div>

					<Button variant="solid" size="lg" :loading="loading" type="submit">
						{{ __('Enviar postulación') }}
					</Button>
				</form>
			</section>
		</main>
	</div>
</template>

<script setup>
import { Button, FormControl, call, toast, usePageMeta } from 'frappe-ui'
import { computed, reactive, ref } from 'vue'
import { Award, Brain, Clock, DollarSign } from 'lucide-vue-next'
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
	{ label: __('Gana hasta 95% por ventas propias'), icon: DollarSign },
	{ label: __('80% en ventas generadas por StudyBadge'), icon: Award },
	{ label: __('IA integrada a tus cursos'), icon: Brain },
	{ label: __('Retiros desde S/20'), icon: Clock },
]

const steps = [
	{ number: '1', title: __('Postula'), body: __('Completa el formulario con tu experiencia e idea de curso.') },
	{ number: '2', title: __('Evaluación IA'), body: __('Revisamos claridad, experiencia, riesgos y valor para estudiantes.') },
	{ number: '3', title: __('Crea cursos'), body: __('Si eres aprobado, tendrás acceso al panel de instructor.') },
	{ number: '4', title: __('Revisión final'), body: __('Tus cursos pasan por revisión antes de publicarse.') },
]

const legal = [
	{ key: 'accepts_instructor_terms', label: __('Acepto los términos del programa de instructores.') },
	{ key: 'confirms_truthful_information', label: __('Declaro que la información enviada es verdadera.') },
	{ key: 'confirms_adult', label: __('Declaro que soy mayor de edad.') },
]

const statusTitle = computed(() => {
	if (!result.value) return ''
	if (result.value.status === 'Approved') return __('Tu perfil fue aprobado')
	if (result.value.status === 'Rejected') return __('Resultado de la evaluación')
	return __('Postulación recibida')
})

const submit = async () => {
	loading.value = true
	result.value = null
	try {
		result.value = await call('studybadge_ai.instructor_review.submit_application', {
			data: { ...form },
		})
		toast.success(__('Postulación enviada correctamente'))
	} catch (error) {
		toast.error(error.messages?.[0] || __('No pudimos enviar la postulación'))
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
	min-height: 100vh;
	background: #f6f8fb;
	color: #101828;
}
.teach-hero {
	background: #061b49 url('/assets/lms/images/wallpaper.png') center/cover no-repeat;
	color: white;
}
.teach-nav {
	display: flex;
	align-items: center;
	justify-content: space-between;
	max-width: 1180px;
	margin: 0 auto;
	padding: 18px 22px;
}
.teach-brand {
	display: flex;
	align-items: center;
	gap: 10px;
	font-weight: 800;
	font-size: 20px;
}
.teach-brand img {
	width: 34px;
	height: 34px;
}
.teach-login {
	color: white;
	font-weight: 700;
	text-decoration: none;
	border: 1px solid rgba(255, 255, 255, 0.35);
	border-radius: 8px;
	padding: 9px 14px;
}
.teach-hero-inner {
	display: grid;
	grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
	gap: 36px;
	max-width: 1180px;
	margin: 0 auto;
	padding: 56px 22px 72px;
}
.teach-kicker {
	font-size: 13px;
	font-weight: 800;
	text-transform: uppercase;
	letter-spacing: 0;
	color: #f5b301;
}
.teach-copy h1 {
	font-size: 48px;
	line-height: 1;
	font-weight: 900;
	margin: 12px 0 16px;
}
.teach-lead {
	max-width: 680px;
	font-size: 18px;
	line-height: 1.65;
	color: rgba(255, 255, 255, 0.86);
}
.teach-benefits {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 12px;
	margin-top: 28px;
}
.teach-benefit,
.teach-step {
	display: flex;
	align-items: center;
	gap: 12px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 8px;
	padding: 14px;
	font-weight: 700;
}
.teach-process {
	display: grid;
	gap: 12px;
	align-content: start;
}
.teach-step {
	align-items: flex-start;
	backdrop-filter: blur(8px);
}
.teach-step-number {
	width: 30px;
	height: 30px;
	border-radius: 50%;
	display: grid;
	place-items: center;
	background: #f5b301;
	color: #061b49;
	font-weight: 900;
	flex: 0 0 auto;
}
.teach-step h3 {
	font-weight: 800;
	margin: 0 0 4px;
}
.teach-step p {
	margin: 0;
	color: rgba(255, 255, 255, 0.76);
	line-height: 1.5;
}
.teach-main {
	max-width: 980px;
	margin: -36px auto 0;
	padding: 0 22px 72px;
}
.teach-form-shell {
	background: white;
	border: 1px solid #e4e7ec;
	border-radius: 8px;
	box-shadow: 0 18px 44px rgba(16, 24, 40, 0.12);
	padding: 28px;
}
.teach-form-heading p {
	font-size: 12px;
	text-transform: uppercase;
	font-weight: 900;
	color: #0d6efd;
	margin: 0 0 6px;
}
.teach-form-heading h2 {
	font-size: 28px;
	font-weight: 900;
	margin: 0 0 22px;
}
.teach-form {
	display: grid;
	gap: 18px;
}
.teach-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 16px;
}
.teach-label {
	display: block;
	font-size: 12px;
	color: #667085;
	margin-bottom: 6px;
}
.teach-select {
	width: 100%;
	border: 1px solid #d0d5dd;
	border-radius: 8px;
	padding: 9px 10px;
	background: white;
}
.teach-check {
	display: flex;
	align-items: center;
	gap: 10px;
	min-height: 38px;
	font-weight: 650;
	color: #344054;
}
.teach-check input {
	width: 16px;
	height: 16px;
}
.teach-legal {
	display: grid;
	gap: 8px;
	border-top: 1px solid #eaecf0;
	padding-top: 16px;
}
.teach-result {
	display: grid;
	gap: 4px;
	border-radius: 8px;
	padding: 14px;
	background: #eff8ff;
	border: 1px solid #b2ddff;
	color: #1849a9;
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
@media (max-width: 860px) {
	.teach-hero-inner,
	.teach-grid,
	.teach-benefits {
		grid-template-columns: 1fr;
	}
	.teach-copy h1 {
		font-size: 38px;
	}
	.teach-form-shell {
		padding: 20px;
	}
}
</style>

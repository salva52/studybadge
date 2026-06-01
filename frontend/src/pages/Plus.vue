<template>
	<div class="sb-plus-page min-h-screen">
		<header class="sb-plus-header">
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
		</header>

		<!-- Loading -->
		<div v-if="billing.data === undefined" class="sb-loading">
			<div class="sb-loading-card">
				<div class="sb-spinner-wrap">
					<div class="sb-spinner"></div>
					<Crown class="size-6 text-amber-400 sb-spinner-icon" />
				</div>
				<p>{{ __('Cargando tu plan...') }}</p>
			</div>
		</div>

		<div v-else>
			<!-- =========================================================
				PLAN ACTIVO
			========================================================= -->
			<div v-if="billing.data?.active" class="sb-active">
				<section class="sb-active-hero">
					<div class="sb-hero-decoration sb-hero-decoration-one"></div>
					<div class="sb-hero-decoration sb-hero-decoration-two"></div>
					<div class="sb-hero-grid"></div>

					<div class="sb-container sb-active-hero-inner">
						<div class="sb-active-hero-content">
							<div class="sb-crown-badge">
								<Crown class="size-11 text-amber-300" />
							</div>

							<div class="sb-active-copy">
								<div class="sb-status-pill">
									<span class="sb-status-dot"></span>
									{{ __('Plan activo') }}
								</div>

								<h1>
									{{ __('Tu membresía') }}
									<span>StudyBadge Plus</span>
								</h1>

								<p>
									{{ __('Gestiona tu plan, revisa tus beneficios activos y descarga tus comprobantes de pago.') }}
								</p>
							</div>
						</div>
					</div>
				</section>

				<main class="sb-container sb-active-layout">
					<div class="sb-active-main">
						<section class="sb-panel">
							<div class="sb-section-heading">
								<div class="sb-section-icon">
									<Sparkles class="size-5" />
								</div>
								<div>
									<h2>{{ __('Tus beneficios activos') }}</h2>
									<p>{{ __('Todo esto está desbloqueado en tu cuenta.') }}</p>
								</div>
							</div>

							<div class="sb-active-benefits-grid">
								<div
									v-for="benefit in benefits"
									:key="benefit.label"
									class="sb-active-benefit"
								>
									<div class="sb-active-benefit-icon">
										<component :is="benefit.icon" class="size-5" />
									</div>
									<div>
										<h3>{{ benefit.label }}</h3>
										<p>{{ benefit.description }}</p>
									</div>
									<CheckCircle2 class="size-4 text-emerald-500 sb-active-check" />
								</div>
							</div>
						</section>

						<section class="sb-panel">
							<div class="sb-panel-header">
								<div class="sb-section-heading sb-section-heading-tight">
									<div class="sb-section-icon sb-section-icon-muted">
										<Download class="size-5" />
									</div>
									<div>
										<h2>{{ __('Historial de pagos') }}</h2>
										<p>{{ __('Tus comprobantes aparecerán aquí cuando se confirmen los cobros.') }}</p>
									</div>
								</div>

								<button class="sb-ghost-btn" @click="billing.reload()">
									<RefreshCcw class="size-4" :class="{ 'animate-spin': billing.loading }" />
									{{ __('Actualizar') }}
								</button>
							</div>

							<div v-if="receipts.length" class="sb-receipts">
								<div
									v-for="receipt in receipts"
									:key="receipt.name"
									class="sb-receipt-row"
								>
									<div class="sb-receipt-main">
										<h3>{{ receipt.receipt_number || receipt.name }}</h3>
										<div class="sb-receipt-meta">
											<CalendarDays class="size-3.5" />
											<span>{{ formatDate(receipt.paid_at || receipt.date_created) }}</span>
											<span
												class="sb-mini-status"
												:class="receipt.status === 'paid' ? 'sb-mini-status-paid' : 'sb-mini-status-default'"
											>
												{{ receipt.status || __('pendiente') }}
											</span>
										</div>
									</div>

									<div class="sb-receipt-actions">
										<strong>{{ formatMoney(receipt.amount, receipt.currency) }}</strong>
										<button
											class="sb-outline-btn sb-outline-btn-small"
											@click="downloadReceipt(receipt)"
										>
											<Download class="size-3.5" />
											PDF
										</button>
									</div>
								</div>
							</div>

							<div v-else class="sb-empty">
								<div class="sb-empty-icon">
									<Download class="size-8" />
								</div>
								<h3>{{ __('Todavía no hay recibos') }}</h3>
								<p>{{ __('Cuando Mercado Pago confirme un cobro, aparecerá aquí tu comprobante.') }}</p>
							</div>
						</section>
					</div>

					<aside class="sb-active-sidebar">
						<section class="sb-plan-card">
							<div class="sb-plan-card-accent"></div>

							<div class="sb-plan-top">
								<div>
									<h2>StudyBadge Plus</h2>
									<p>{{ formattedPrice }} / {{ __('mes') }}</p>
								</div>

								<Badge theme="green" class="font-bold text-xs">
									<CheckCircle2 class="size-3 mr-1" />
									{{ __('Activo') }}
								</Badge>
							</div>

							<div class="sb-plan-info-list">
								<div class="sb-plan-info">
									<CalendarDays class="size-4" />
									<div>
										<span>{{ __('Próximo cobro') }}</span>
										<strong>{{ formatDate(subscription?.next_payment_date) }}</strong>
									</div>
								</div>

								<div class="sb-plan-info">
									<CreditCard class="size-4" />
									<div>
										<span>{{ __('Método de pago') }}</span>
										<strong>{{ paymentMethodLabel }}</strong>
									</div>
								</div>
							</div>

							<div
								v-if="subscription?.cancel_at_period_end"
								class="sb-cancel-warning"
							>
								<strong>{{ __('Cancelación programada') }}</strong>
								<p>
									{{ __('Tu suscripción se cancelará el {0}.', [formatDate(subscription.cancel_scheduled_for)]) }}
								</p>
							</div>

							<div class="sb-plan-actions">
								<button
									v-if="!subscription?.cancel_at_period_end"
									class="sb-primary-btn"
									@click="showPaymentMethodForm"
								>
									<CreditCard class="size-4" />
									{{ __('Gestionar suscripción') }}
								</button>

								<button
									v-if="!subscription?.cancel_at_period_end"
									class="sb-danger-btn"
									:disabled="cancelResource.loading"
									@click="requestCancellation"
								>
									{{ cancelResource.loading ? __('Cancelando...') : __('Cancelar plan') }}
								</button>

								<button
									v-if="subscription?.cancel_at_period_end"
									class="sb-primary-btn"
									:disabled="reactivateResource.loading"
									@click="reactivateSubscription"
								>
									<RefreshCcw class="size-4" />
									{{ reactivateResource.loading ? __('Reactivando...') : __('Reactivar mi Plus') }}
								</button>
							</div>
						</section>

						<section class="sb-support-card">
							<LifeBuoy class="size-8" />
							<h3>{{ __('¿Necesitas ayuda?') }}</h3>
							<p>{{ __('Nuestro equipo está listo para ayudarte con pagos, certificados o tu cuenta.') }}</p>

							<a
								class="sb-ghost-btn sb-support-link"
								:href="`mailto:${billing.data?.support_email || 'soporte@studybadge.com'}`"
							>
								<Mail class="size-4" />
								{{ __('Contactar soporte') }}
							</a>
						</section>
					</aside>
				</main>

				<Teleport to="body">
					<Transition name="sb-modal">
						<div
							v-if="cardFormVisible"
							class="sb-modal-shell"
							@click.self="hidePaymentMethodForm"
						>
							<div class="sb-modal-overlay"></div>

							<div class="sb-modal-content">
								<div class="sb-modal-header">
									<div>
										<ShieldCheck class="size-5 text-emerald-500" />
										<strong>{{ __('Actualizar método de pago') }}</strong>
									</div>

									<button class="sb-modal-close" @click="hidePaymentMethodForm">
										<XCircle class="size-5" />
									</button>
								</div>

								<div class="sb-modal-body">
									<div v-if="cardFormLoading" class="sb-card-loading">
										{{ __('Estableciendo conexión segura...') }}
									</div>

									<div id="studybadge-mp-card-form"></div>
								</div>
							</div>
						</div>
					</Transition>
				</Teleport>
			</div>

			<!-- =========================================================
				SIN PLAN — LANDING DE CONVERSIÓN
			========================================================= -->
			<div v-else class="sb-sales">
				<section class="sb-sales-hero">
					<div class="sb-hero-decoration sb-hero-decoration-one"></div>
					<div class="sb-hero-decoration sb-hero-decoration-two"></div>
					<div class="sb-hero-grid"></div>

					<div class="sb-container sb-sales-hero-inner">
						<div class="sb-sales-copy">
							<div class="sb-eyebrow">
								<Crown class="size-4" />
								STUDYBADGE PLUS
							</div>

							<h1>{{ __('Estudia mejor, crea más rápido y avanza con IA sin límites.') }}</h1>

							<p>
								{{ __('Desbloquea certificados ilimitados, Tutor IA, prompts premium, simulaciones y herramientas inteligentes para convertir StudyBadge en tu ventaja académica y profesional.') }}
							</p>

							<div class="sb-hero-actions">
								<button
									class="sb-hero-primary"
									:disabled="activating"
									@click="subscription?.init_point ? openExistingCheckout() : activatePlus()"
								>
									<span v-if="activating" class="sb-button-spinner"></span>
									<Crown v-else class="size-5" />
									{{ subscription?.init_point ? __('Continuar pago pendiente') : __('Desbloquear Plus ahora') }}
								</button>

								<button class="sb-hero-secondary" @click="scrollToBenefits">
									{{ __('Ver beneficios') }}
									<ArrowDown class="size-4" />
								</button>
							</div>

							<div class="sb-trust-row">
								<span>
									<Sparkles class="size-4" />
									{{ __('Acceso inmediato') }}
								</span>
								<span>
									<RefreshCcw class="size-4" />
									{{ __('Cancela cuando quieras') }}
								</span>
								<span>
									<ShieldCheck class="size-4" />
									{{ __('Pago seguro') }}
								</span>
							</div>
						</div>

						<div id="pricing-card" class="sb-pricing-wrap">
							<section class="sb-pricing-card">
								<div class="sb-pricing-ribbon">
									<Crown class="size-4" />
									{{ __('Membresía Plus') }}
								</div>

								<div class="sb-pricing-body">
									<div class="sb-price-head">
										<span class="sb-price-label">{{ __('Plan mensual') }}</span>

										<div class="sb-price">
											<span>{{ formattedPrice }}</span>
											<small>/ {{ __('mes') }}</small>
										</div>

										<p>{{ __('Menos de S/1 al día para desbloquear todas las herramientas premium.') }}</p>
									</div>

									<ul class="sb-price-list">
										<li>
											<CheckCircle2 class="size-5" />
											{{ __('Certificados ilimitados') }}
										</li>
										<li>
											<CheckCircle2 class="size-5" />
											{{ __('Tutor IA ilimitado') }}
										</li>
										<li>
											<CheckCircle2 class="size-5" />
											{{ __('Prompts premium listos') }}
										</li>
										<li>
											<CheckCircle2 class="size-5" />
											{{ __('Simulaciones y calendario inteligente') }}
										</li>
									</ul>

									<button
										class="sb-pricing-cta"
										:disabled="activating"
										@click="subscription?.init_point ? openExistingCheckout() : activatePlus()"
									>
										<span v-if="activating" class="sb-button-spinner sb-button-spinner-light"></span>
										<Crown v-else class="size-5" />
										{{ subscription?.init_point ? __('Continuar pago pendiente') : __('Desbloquear StudyBadge Plus') }}
									</button>

									<div class="sb-payment-note">
										<ShieldCheck class="size-4" />
										{{ __('Pago 100% seguro con Mercado Pago') }}
									</div>
								</div>

								<div class="sb-pricing-footer">
									<strong>{{ __('Próximamente plan anual') }}</strong>
									<span>{{ __('Ahorra más pagando por año.') }}</span>
								</div>
							</section>
						</div>
					</div>
				</section>

				<section class="sb-social-proof">
					<div class="sb-container sb-stats-grid">
						<div class="sb-stat">
							<div><Users class="size-5" /></div>
							<strong>+1,000</strong>
							<span>{{ __('estudiantes') }}</span>
						</div>

						<div class="sb-stat">
							<div><FileText class="size-5" /></div>
							<strong>+100</strong>
							<span>{{ __('prompts listos') }}</span>
						</div>

						<div class="sb-stat">
							<div><PlayCircle class="size-5" /></div>
							<strong>+30</strong>
							<span>{{ __('cursos y recursos') }}</span>
						</div>

						<div class="sb-stat">
							<div><ClockIcon class="size-5" /></div>
							<strong>24/7</strong>
							<span>{{ __('disponible') }}</span>
						</div>
					</div>
				</section>

				<section id="benefits-section" class="sb-container sb-section">
					<div class="sb-section-title">
						<span>{{ __('Beneficios premium') }}</span>
						<h2>{{ __('Todo lo que desbloqueas con StudyBadge Plus') }}</h2>
						<p>{{ __('No es solo pagar por funciones. Es ahorrar tiempo, estudiar con más claridad y crear mejores resultados con IA.') }}</p>
					</div>

					<div class="sb-benefits-grid">
						<article
							v-for="benefit in benefits"
							:key="benefit.label"
							class="sb-benefit-card"
						>
							<div class="sb-benefit-icon">
								<component :is="benefit.icon" class="size-7" />
							</div>
							<h3>{{ benefit.label }}</h3>
							<p>{{ benefit.description }}</p>
						</article>
					</div>
				</section>

				<section class="sb-white-section">
					<div class="sb-container sb-results-layout">
						<div class="sb-results-copy">
							<div class="sb-section-title sb-section-title-left">
								<span>{{ __('Resultados desde hoy') }}</span>
								<h2>{{ __('Tu flujo de estudio y creación se vuelve más rápido.') }}</h2>
								<p>{{ __('StudyBadge Plus está pensado para que no empieces desde cero cada vez que tengas una tarea, exposición, proyecto o idea de negocio.') }}</p>
							</div>

							<div class="sb-results-list">
								<div
									v-for="result in results"
									:key="result.title"
									class="sb-result-item"
								>
									<div :class="['sb-result-icon', result.className]">
										<component :is="result.icon" class="size-5" />
									</div>
									<div>
										<h3>{{ result.title }}</h3>
										<p>{{ result.description }}</p>
									</div>
								</div>
							</div>
						</div>

						<div class="sb-ai-preview">
							<div class="sb-ai-window">
								<div class="sb-ai-header">
									<div class="sb-ai-avatar">
										<Bot class="size-6" />
									</div>
									<div>
										<strong>Tutor IA StudyBadge</strong>
										<span>{{ __('En línea') }}</span>
									</div>
								</div>

								<div class="sb-ai-message sb-ai-message-left">
									{{ __('Analicé tu documento. Te preparé un resumen, 5 preguntas tipo examen y una explicación simple de los conceptos más difíciles.') }}
								</div>

								<div class="sb-ai-message sb-ai-message-right">
									{{ __('Perfecto, empecemos con preguntas difíciles.') }}
								</div>

								<div class="sb-ai-suggestions">
									<span>{{ __('Resumen') }}</span>
									<span>{{ __('Quiz') }}</span>
									<span>{{ __('Exposición') }}</span>
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="sb-container sb-section">
					<div class="sb-section-title">
						<span>{{ __('Comparación') }}</span>
						<h2>{{ __('Gratis vs Plus') }}</h2>
						<p>{{ __('Muestra claramente por qué Plus vale la pena desde el primer mes.') }}</p>
					</div>

					<div class="sb-comparison">
						<div class="sb-comparison-head">
							<div>
								<h3>{{ __('Plan Gratis') }}</h3>
								<p>{{ __('Para probar la plataforma') }}</p>
							</div>

							<div class="sb-comparison-plus">
								<span>{{ __('Recomendado') }}</span>
								<h3>StudyBadge Plus</h3>
								<p>{{ __('Para avanzar más rápido') }}</p>
							</div>
						</div>

						<div class="sb-comparison-rows">
							<div
								v-for="row in comparisonRows"
								:key="row.free + row.plus"
								class="sb-comparison-row"
							>
								<div class="sb-free-col">
									<X v-if="row.freeNegative" class="size-4" />
									<span>{{ row.free }}</span>
								</div>

								<div class="sb-plus-col">
									<CheckCircle2 class="size-5" />
									<strong>{{ row.plus }}</strong>
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="sb-white-section">
					<div class="sb-container sb-faq-section">
						<div class="sb-section-title">
							<span>{{ __('Dudas frecuentes') }}</span>
							<h2>{{ __('Preguntas frecuentes') }}</h2>
						</div>

						<div class="sb-faq-grid">
							<article v-for="faq in faqs" :key="faq.q" class="sb-faq-card">
								<h3>{{ faq.q }}</h3>
								<p>{{ faq.a }}</p>
							</article>
						</div>
					</div>
				</section>

				<section class="sb-final-cta">
					<div class="sb-hero-decoration sb-hero-decoration-two"></div>
					<div class="sb-container sb-final-inner">
						<Crown class="size-11 text-amber-300" />
						<h2>{{ __('Empieza hoy con StudyBadge Plus') }}</h2>
						<p>{{ __('Desbloquea herramientas inteligentes para estudiar, crear y avanzar más rápido.') }}</p>

						<button
							class="sb-final-btn"
							:disabled="activating"
							@click="subscription?.init_point ? openExistingCheckout() : activatePlus()"
						>
							<span v-if="activating" class="sb-button-spinner"></span>
							{{ subscription?.init_point ? __('Continuar pago pendiente') : __('Desbloquear Plus por ') + formattedPrice }}
						</button>

						<div class="sb-final-trust">
							<span>{{ __('Acceso inmediato') }}</span>
							<span>{{ __('Cancela cuando quieras') }}</span>
							<span>{{ __('Pago seguro') }}</span>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject, nextTick, onBeforeUnmount, ref } from 'vue'
import { Badge, Breadcrumbs, createResource, toast, usePageMeta } from 'frappe-ui'
import {
	Award,
	Bot,
	Briefcase,
	CalendarDays,
	CheckCircle2,
	Clock as ClockIcon,
	CreditCard,
	Crown,
	Download,
	FileText,
	LifeBuoy,
	Mail,
	PlayCircle,
	RefreshCcw,
	ShieldCheck,
	Sparkles,
	Users,
	Video,
	X,
	XCircle,
	Zap,
	ArrowDown,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const user = inject('$user')

const activating = ref(false)
const cardFormVisible = ref(false)
const cardFormLoading = ref(false)
const cardController = ref(null)
const mercadoPagoLoader = ref(null)

const benefits = [
	{
		icon: Award,
		label: __('Certificados ilimitados'),
		description: __('Obtén certificados por cada curso completado y desbloquea todos los certificados premium.'),
	},
	{
		icon: Bot,
		label: __('Tutor IA ilimitado'),
		description: __('Haz preguntas, resuelve dudas, practica temas y recibe ayuda personalizada sin límites.'),
	},
	{
		icon: FileText,
		label: __('Biblioteca de prompts premium'),
		description: __('Usa prompts listos para marketing, estudio, negocios, productividad e imágenes IA.'),
	},
	{
		icon: Video,
		label: __('Simulaciones con IA'),
		description: __('Practica entrevistas, ventas, inglés, exposiciones y casos reales con retroalimentación.'),
	},
	{
		icon: CalendarDays,
		label: __('Calendario inteligente'),
		description: __('Organiza tus cursos, tareas y objetivos con seguimiento automático.'),
	},
	{
		icon: Zap,
		label: __('Herramientas de estudio IA'),
		description: __('Resume, practica, genera quizzes y convierte temas difíciles en ejercicios simples.'),
	},
]

const results = [
	{
		icon: Zap,
		className: 'sb-result-green',
		title: __('Aprende más rápido'),
		description: __('Convierte clases largas en resúmenes, quizzes y ejemplos simples en minutos.'),
	},
	{
		icon: Briefcase,
		className: 'sb-result-blue',
		title: __('Crea mejores trabajos'),
		description: __('Prepara exposiciones, tareas, presentaciones y entrevistas con ayuda guiada.'),
	},
	{
		icon: ClockIcon,
		className: 'sb-result-amber',
		title: __('Ahorra horas con prompts'),
		description: __('Genera contenido, planes, ideas de negocio y tareas sin empezar desde cero.'),
	},
	{
		icon: Bot,
		className: 'sb-result-purple',
		title: __('Practica con IA sin límites'),
		description: __('Recibe retroalimentación inmediata y mejora tus respuestas paso a paso.'),
	},
]

const comparisonRows = [
	{
		free: __('Acceso limitado a cursos'),
		plus: __('Cursos y recursos premium'),
	},
	{
		free: __('Certificados limitados'),
		plus: __('Certificados ilimitados'),
	},
	{
		free: __('Prompts básicos'),
		plus: __('Prompts premium ilimitados'),
	},
	{
		free: __('Tutor IA limitado'),
		plus: __('Tutor IA ilimitado'),
	},
	{
		free: __('Sin simulaciones premium'),
		plus: __('Simulaciones con IA completas'),
		freeNegative: true,
	},
	{
		free: __('Sin calendario inteligente'),
		plus: __('Calendario y seguimiento total'),
		freeNegative: true,
	},
]

const faqs = [
	{
		q: __('¿Puedo cancelar cuando quiera?'),
		a: __('Sí. No hay contratos largos. Puedes cancelar tu suscripción cuando quieras y mantener el acceso hasta el final del periodo pagado.'),
	},
	{
		q: __('¿Qué incluye StudyBadge Plus?'),
		a: __('Incluye certificados ilimitados, Tutor IA ilimitado, simulaciones, prompts premium, calendario inteligente y herramientas de estudio con IA.'),
	},
	{
		q: __('¿Los certificados son ilimitados?'),
		a: __('Sí. Con Plus puedes generar certificados de los cursos que completes y apruebes, sin pagar extra por cada certificado.'),
	},
	{
		q: __('¿El pago es seguro?'),
		a: __('Sí. El pago se procesa con Mercado Pago, una pasarela segura y conocida en Latinoamérica.'),
	},
	{
		q: __('¿Sirve para estudiar y para negocios?'),
		a: __('Sí. StudyBadge Plus está pensado para estudiantes, emprendedores, freelancers y pequeños negocios que quieren avanzar con IA.'),
	},
	{
		q: __('¿Qué pasa después de pagar?'),
		a: __('Tu cuenta se actualiza y tendrás acceso a las funciones Plus cuando el pago sea confirmado.'),
	},
]

const billing = createResource({
	url: 'lms.lms.subscriptions.get_plus_billing',
	auto: true,
	onSuccess(data) {
		if (data?.active) {
			user?.reload?.()
		}
	},
})

const checkout = createResource({
	url: 'lms.lms.subscriptions.create_plus_checkout',
})

const cancelResource = createResource({
	url: 'lms.lms.subscriptions.request_plus_cancellation',
})

const reactivateResource = createResource({
	url: 'lms.lms.subscriptions.reactivate_plus_subscription',
})

const paymentMethodResource = createResource({
	url: 'lms.lms.subscriptions.update_plus_payment_method',
})

const subscription = computed(() => billing.data?.subscription || null)
const receipts = computed(() => billing.data?.receipts || [])

const formattedPrice = computed(() => {
	const plan = billing.data?.plan
	if (!plan) return 'S/ 29.90'

	const amount = Number(plan.amount || 29.9).toFixed(2)

	if (plan.currency === 'PEN') {
		return `S/ ${amount}`
	}

	return `${plan.currency || 'S/'} ${amount}`
})

const paymentMethodLabel = computed(() => {
	const method = subscription.value?.payment_method

	if (!method?.id && !method?.card_last_four) {
		return __('Mercado Pago')
	}

	if (method.card_last_four) {
		return `${method.card_brand || method.name || __('Tarjeta')} **** ${method.card_last_four}`
	}

	return method.name || method.id || __('Mercado Pago')
})

const breadcrumbs = computed(() => [
	{
		label: __('StudyBadge Plus'),
		route: { name: 'Plus' },
	},
])

function scrollToPricing() {
	document.getElementById('pricing-card')?.scrollIntoView({
		behavior: 'smooth',
		block: 'center',
	})
}

function scrollToBenefits() {
	document.getElementById('benefits-section')?.scrollIntoView({
		behavior: 'smooth',
		block: 'start',
	})
}

function getErrorMessage(err) {
	if (!err) return __('Ocurrió un error.')
	if (typeof err === 'string') return err
	if (err.messages?.length) return err.messages[0]
	if (err.message) return err.message
	return __('Ocurrió un error.')
}

function activatePlus() {
	if (activating.value) return

	activating.value = true

	checkout.submit(
		{},
		{
			onSuccess(url) {
				if (!url) {
					activating.value = false
					toast.error(__('No se recibió el enlace de pago.'))
					return
				}

				window.location.href = url
			},
			onError(err) {
				activating.value = false
				toast.error(getErrorMessage(err))
			},
		}
	)
}

function openExistingCheckout() {
	const url = subscription.value?.init_point

	if (!url) {
		activatePlus()
		return
	}

	window.location.href = url
}

function requestCancellation() {
	const confirmed = window.confirm(
		__('Tu Plus seguirá activo hasta el final del periodo pagado. ¿Quieres cancelar la renovación?')
	)

	if (!confirmed) return

	cancelResource.submit(
		{},
		{
			onSuccess(data) {
				billing.data = data
				toast.success(__('Cancelación programada.'))
			},
			onError(err) {
				toast.error(getErrorMessage(err))
			},
		}
	)
}

function reactivateSubscription() {
	reactivateResource.submit(
		{},
		{
			onSuccess(data) {
				billing.data = data
				toast.success(__('Tu Plus sigue activo.'))
			},
			onError(err) {
				toast.error(getErrorMessage(err))
			},
		}
	)
}

async function showPaymentMethodForm() {
	cardFormVisible.value = true
	await nextTick()
	initMercadoPagoCardForm()
}

function hidePaymentMethodForm() {
	cardFormVisible.value = false
	destroyCardForm()
}

function loadMercadoPago() {
	if (window.MercadoPago) {
		return Promise.resolve(window.MercadoPago)
	}

	if (mercadoPagoLoader.value) {
		return mercadoPagoLoader.value
	}

	mercadoPagoLoader.value = new Promise((resolve, reject) => {
		const script = document.createElement('script')
		script.src = 'https://sdk.mercadopago.com/js/v2'
		script.onload = () => resolve(window.MercadoPago)
		script.onerror = reject
		document.body.appendChild(script)
	})

	return mercadoPagoLoader.value
}

async function initMercadoPagoCardForm() {
	if (!billing.data?.public_key) {
		cardFormLoading.value = false
		toast.error(__('Falta configurar la public key de Mercado Pago.'))
		return
	}

	cardFormLoading.value = true
	destroyCardForm()

	try {
		const MercadoPago = await loadMercadoPago()
		const mp = new MercadoPago(billing.data.public_key, { locale: 'es-PE' })
		const bricksBuilder = mp.bricks()

		cardController.value = await bricksBuilder.create(
			'cardPayment',
			'studybadge-mp-card-form',
			{
				initialization: {
					amount: Number(billing.data?.plan?.amount || 29.9),
				},
				customization: {
					paymentMethods: {
						maxInstallments: 1,
					},
				},
				callbacks: {
					onReady() {
						cardFormLoading.value = false
					},
					onError(error) {
						cardFormLoading.value = false
						toast.error(error?.message || __('Mercado Pago no pudo cargar.'))
					},
					onSubmit(cardFormData) {
						return new Promise((resolve, reject) => {
							const cardToken = cardFormData.token || cardFormData.card_token_id

							if (!cardToken) {
								const error = __('No se pudo generar el token de la tarjeta.')
								toast.error(error)
								reject(error)
								return
							}

							paymentMethodResource.submit(
								{ card_token_id: cardToken },
								{
									onSuccess(data) {
										billing.data = data
										hidePaymentMethodForm()
										toast.success(__('Método de pago actualizado.'))
										resolve()
									},
									onError(err) {
										toast.error(getErrorMessage(err))
										reject(err)
									},
								}
							)
						})
					},
				},
			}
		)
	} catch (error) {
		cardFormLoading.value = false
		toast.error(error?.message || __('No se pudo cargar Mercado Pago.'))
	}
}

function destroyCardForm() {
	if (cardController.value?.unmount) {
		cardController.value.unmount()
	}

	cardController.value = null
}

function downloadReceipt(receipt) {
	if (!receipt?.download_url) {
		toast.error(__('Este recibo todavía no tiene PDF disponible.'))
		return
	}

	window.open(receipt.download_url, '_blank', 'noopener')
}

function formatDate(value) {
	if (!value) return __('Pendiente')

	const date = new Date(value)

	if (Number.isNaN(date.getTime())) {
		return __('Pendiente')
	}

	return new Intl.DateTimeFormat('es-PE', {
		dateStyle: 'medium',
		timeStyle: 'short',
	}).format(date)
}

function formatMoney(amount, currency) {
	const parsedAmount = Number(amount || 0).toFixed(2)

	if (currency === 'PEN' || !currency) {
		return `S/ ${parsedAmount}`
	}

	return `${currency} ${parsedAmount}`
}

onBeforeUnmount(() => {
	destroyCardForm()
})

usePageMeta(() => ({
	title: __('StudyBadge Plus'),
	icon: brand.favicon,
}))
</script>

<style scoped>
.sb-plus-page {
	background: #f5f7fb;
	color: #111827;
	font-family:
		Inter,
		ui-sans-serif,
		system-ui,
		-apple-system,
		BlinkMacSystemFont,
		"Segoe UI",
		sans-serif;
}

.sb-container {
	width: min(1180px, calc(100% - 32px));
	margin-inline: auto;
}

.sb-plus-header {
	position: sticky;
	top: 0;
	z-index: 40;
	display: flex;
	align-items: center;
	justify-content: space-between;
	height: 48px;
	padding: 0 16px;
	background: rgba(255, 255, 255, 0.92);
	border-bottom: 1px solid rgba(8, 32, 78, 0.08);
	backdrop-filter: blur(16px);
}

.sb-loading {
	display: grid;
	place-items: center;
	min-height: calc(100vh - 48px);
	padding: 48px 16px;
}

.sb-loading-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 16px;
	padding: 32px;
	background: #ffffff;
	border: 1px solid rgba(8, 32, 78, 0.08);
	border-radius: 24px;
	box-shadow: 0 20px 60px rgba(8, 32, 78, 0.08);
}

.sb-loading-card p {
	margin: 0;
	color: #6b7280;
	font-size: 14px;
	font-weight: 700;
}

.sb-spinner-wrap {
	position: relative;
	width: 64px;
	height: 64px;
}

.sb-spinner {
	width: 64px;
	height: 64px;
	border: 4px solid #e5e7eb;
	border-top-color: #1473e6;
	border-radius: 999px;
	animation: sb-spin 0.9s linear infinite;
}

.sb-spinner-icon {
	position: absolute;
	inset: 0;
	margin: auto;
}

@keyframes sb-spin {
	to {
		transform: rotate(360deg);
	}
}

/* Shared hero */
.sb-active-hero,
.sb-sales-hero,
.sb-final-cta {
	position: relative;
	overflow: hidden;
	background:
		radial-gradient(circle at 82% 18%, rgba(36, 101, 222, 0.46), transparent 32%),
		linear-gradient(135deg, #061942 0%, #08204e 42%, #0d347a 100%);
	color: white;
}

.sb-hero-grid {
	position: absolute;
	inset: 0;
	opacity: 0.32;
	background-image:
		linear-gradient(rgba(255, 255, 255, 0.045) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px);
	background-size: 56px 56px;
	pointer-events: none;
}

.sb-hero-decoration {
	position: absolute;
	border-radius: 999px;
	filter: blur(64px);
	pointer-events: none;
}

.sb-hero-decoration-one {
	top: -160px;
	left: -120px;
	width: 380px;
	height: 380px;
	background: rgba(20, 115, 230, 0.35);
}

.sb-hero-decoration-two {
	right: -120px;
	bottom: -180px;
	width: 420px;
	height: 420px;
	background: rgba(250, 204, 21, 0.16);
}

.sb-crown-badge {
	display: inline-grid;
	place-items: center;
	width: 88px;
	height: 88px;
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.18);
	box-shadow: 0 24px 70px rgba(0, 0, 0, 0.16);
	backdrop-filter: blur(12px);
}

/* Active state */
.sb-active-hero-inner {
	position: relative;
	z-index: 2;
	padding: 64px 0;
}

.sb-active-hero-content {
	display: flex;
	align-items: center;
	gap: 28px;
}

.sb-status-pill {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	padding: 8px 12px;
	margin-bottom: 16px;
	color: #bbf7d0;
	background: rgba(34, 197, 94, 0.16);
	border: 1px solid rgba(74, 222, 128, 0.22);
	border-radius: 999px;
	font-size: 12px;
	font-weight: 900;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.sb-status-dot {
	position: relative;
	width: 8px;
	height: 8px;
	background: #22c55e;
	border-radius: 999px;
	box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.14);
}

.sb-active-copy h1 {
	margin: 0;
	color: #ffffff;
	font-size: clamp(34px, 5vw, 56px);
	font-weight: 950;
	letter-spacing: -0.055em;
	line-height: 0.98;
}

.sb-active-copy h1 span {
	display: block;
	margin-top: 8px;
	color: #facc15;
}

.sb-active-copy p {
	max-width: 620px;
	margin: 18px 0 0;
	color: rgba(219, 234, 254, 0.84);
	font-size: 18px;
	font-weight: 600;
	line-height: 1.55;
}

.sb-active-layout {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 340px;
	gap: 28px;
	align-items: start;
	padding: 36px 0 64px;
}

.sb-active-main {
	display: grid;
	gap: 24px;
}

.sb-panel,
.sb-plan-card,
.sb-support-card {
	background: #ffffff;
	border: 1px solid rgba(8, 32, 78, 0.08);
	border-radius: 24px;
	box-shadow:
		0 1px 2px rgba(8, 32, 78, 0.04),
		0 16px 50px rgba(8, 32, 78, 0.06);
}

.sb-panel {
	padding: 28px;
}

.sb-section-heading {
	display: flex;
	align-items: flex-start;
	gap: 14px;
	margin-bottom: 24px;
}

.sb-section-heading-tight {
	margin-bottom: 0;
}

.sb-section-icon {
	display: grid;
	place-items: center;
	flex: 0 0 auto;
	width: 42px;
	height: 42px;
	color: #1473e6;
	background: #eff6ff;
	border-radius: 14px;
}

.sb-section-icon-muted {
	color: #64748b;
	background: #f1f5f9;
}

.sb-section-heading h2 {
	margin: 0;
	color: #08204e;
	font-size: 21px;
	font-weight: 900;
	letter-spacing: -0.02em;
}

.sb-section-heading p {
	margin: 4px 0 0;
	color: #64748b;
	font-size: 14px;
	line-height: 1.5;
}

.sb-active-benefits-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 14px;
}

.sb-active-benefit {
	position: relative;
	display: flex;
	align-items: flex-start;
	gap: 12px;
	min-height: 112px;
	padding: 16px;
	background: #f8fbff;
	border: 1px solid #e8f0ff;
	border-radius: 18px;
	transition: 0.2s ease;
}

.sb-active-benefit:hover {
	transform: translateY(-2px);
	border-color: rgba(20, 115, 230, 0.28);
	box-shadow: 0 16px 35px rgba(8, 32, 78, 0.08);
}

.sb-active-benefit-icon {
	display: grid;
	place-items: center;
	width: 40px;
	height: 40px;
	flex: 0 0 auto;
	color: #1473e6;
	background: #eaf3ff;
	border-radius: 14px;
}

.sb-active-benefit h3 {
	margin: 0;
	color: #111827;
	font-size: 14px;
	font-weight: 900;
}

.sb-active-benefit p {
	margin: 5px 0 0;
	color: #64748b;
	font-size: 12.5px;
	line-height: 1.45;
}

.sb-active-check {
	margin-left: auto;
	opacity: 0.8;
}

.sb-panel-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	padding-bottom: 20px;
	margin-bottom: 20px;
	border-bottom: 1px solid #edf1f7;
}

.sb-ghost-btn,
.sb-outline-btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	border: 0;
	border-radius: 12px;
	font-weight: 800;
	cursor: pointer;
	transition: 0.18s ease;
}

.sb-ghost-btn {
	padding: 10px 12px;
	color: #64748b;
	background: transparent;
	font-size: 13px;
}

.sb-ghost-btn:hover {
	color: #08204e;
	background: #f1f5f9;
}

.sb-outline-btn {
	padding: 10px 14px;
	color: #334155;
	background: #ffffff;
	border: 1px solid #e2e8f0;
	font-size: 13px;
}

.sb-outline-btn:hover {
	color: #1473e6;
	border-color: rgba(20, 115, 230, 0.32);
	background: #f8fbff;
}

.sb-outline-btn-small {
	padding: 8px 10px;
	font-size: 12px;
}

.sb-receipts {
	display: grid;
	gap: 10px;
}

.sb-receipt-row {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	padding: 14px 16px;
	background: #f8fafc;
	border: 1px solid #eef2f7;
	border-radius: 16px;
}

.sb-receipt-main {
	min-width: 0;
}

.sb-receipt-main h3 {
	margin: 0;
	color: #111827;
	font-size: 14px;
	font-weight: 900;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.sb-receipt-meta {
	display: flex;
	align-items: center;
	gap: 7px;
	margin-top: 6px;
	color: #64748b;
	font-size: 12px;
}

.sb-mini-status {
	display: inline-flex;
	align-items: center;
	padding: 2px 7px;
	border-radius: 999px;
	font-size: 10px;
	font-weight: 900;
	letter-spacing: 0.04em;
	text-transform: uppercase;
}

.sb-mini-status-paid {
	color: #047857;
	background: #d1fae5;
}

.sb-mini-status-default {
	color: #475569;
	background: #e2e8f0;
}

.sb-receipt-actions {
	display: flex;
	align-items: center;
	gap: 12px;
	flex: 0 0 auto;
}

.sb-receipt-actions strong {
	color: #0f172a;
	font-size: 14px;
}

.sb-empty {
	display: grid;
	place-items: center;
	text-align: center;
	padding: 42px 16px;
}

.sb-empty-icon {
	display: grid;
	place-items: center;
	width: 68px;
	height: 68px;
	color: #94a3b8;
	background: #f1f5f9;
	border-radius: 22px;
}

.sb-empty h3 {
	margin: 16px 0 0;
	color: #111827;
	font-size: 16px;
	font-weight: 900;
}

.sb-empty p {
	max-width: 340px;
	margin: 6px 0 0;
	color: #64748b;
	font-size: 14px;
	line-height: 1.5;
}

.sb-active-sidebar {
	position: sticky;
	top: 72px;
	display: grid;
	gap: 18px;
}

.sb-plan-card {
	position: relative;
	overflow: hidden;
	padding: 24px;
}

.sb-plan-card-accent {
	position: absolute;
	inset: 0 0 auto;
	height: 5px;
	background: linear-gradient(90deg, #1473e6, #22c55e);
}

.sb-plan-top {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 12px;
	margin-bottom: 22px;
}

.sb-plan-top h2 {
	margin: 0;
	color: #08204e;
	font-size: 20px;
	font-weight: 950;
}

.sb-plan-top p {
	margin: 4px 0 0;
	color: #64748b;
	font-size: 14px;
	font-weight: 700;
}

.sb-plan-info-list {
	display: grid;
	gap: 10px;
}

.sb-plan-info {
	display: flex;
	align-items: flex-start;
	gap: 12px;
	padding: 13px 14px;
	color: #64748b;
	background: #f8fafc;
	border-radius: 16px;
}

.sb-plan-info span {
	display: block;
	color: #64748b;
	font-size: 10px;
	font-weight: 900;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.sb-plan-info strong {
	display: block;
	margin-top: 3px;
	color: #111827;
	font-size: 13px;
	line-height: 1.35;
	overflow-wrap: anywhere;
}

.sb-cancel-warning {
	margin-top: 18px;
	padding: 14px;
	background: #fffbeb;
	border: 1px solid #fde68a;
	border-radius: 16px;
}

.sb-cancel-warning strong {
	color: #92400e;
	font-size: 13px;
}

.sb-cancel-warning p {
	margin: 4px 0 0;
	color: #b45309;
	font-size: 12px;
	line-height: 1.45;
}

.sb-plan-actions {
	display: grid;
	gap: 10px;
	margin-top: 20px;
}

.sb-primary-btn,
.sb-danger-btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	width: 100%;
	min-height: 46px;
	border: 0;
	border-radius: 14px;
	font-size: 14px;
	font-weight: 900;
	cursor: pointer;
	transition: 0.18s ease;
}

.sb-primary-btn {
	color: #ffffff;
	background: linear-gradient(135deg, #1473e6, #0b5ed7);
	box-shadow: 0 12px 26px rgba(20, 115, 230, 0.23);
}

.sb-primary-btn:hover {
	transform: translateY(-1px);
	box-shadow: 0 16px 34px rgba(20, 115, 230, 0.3);
}

.sb-danger-btn {
	color: #ef4444;
	background: #fff1f2;
}

.sb-danger-btn:hover {
	background: #ffe4e6;
}

.sb-primary-btn:disabled,
.sb-danger-btn:disabled,
.sb-hero-primary:disabled,
.sb-pricing-cta:disabled,
.sb-final-btn:disabled {
	cursor: not-allowed;
	opacity: 0.72;
	transform: none;
	box-shadow: none;
}

.sb-support-card {
	padding: 24px;
	text-align: center;
	color: #64748b;
	background: linear-gradient(180deg, #ffffff, #f8fbff);
}

.sb-support-card svg {
	margin-inline: auto;
	color: #1473e6;
}

.sb-support-card h3 {
	margin: 12px 0 0;
	color: #08204e;
	font-size: 15px;
	font-weight: 900;
}

.sb-support-card p {
	margin: 6px 0 18px;
	color: #64748b;
	font-size: 13px;
	line-height: 1.5;
}

.sb-support-link {
	text-decoration: none;
}

/* Modal */
.sb-modal-shell {
	position: fixed;
	inset: 0;
	z-index: 70;
	display: grid;
	place-items: center;
	padding: 16px;
}

.sb-modal-overlay {
	position: absolute;
	inset: 0;
	background: rgba(2, 6, 23, 0.68);
	backdrop-filter: blur(8px);
}

.sb-modal-content {
	position: relative;
	z-index: 1;
	width: min(100%, 480px);
	max-height: 90vh;
	overflow: hidden;
	background: #ffffff;
	border-radius: 24px;
	box-shadow: 0 28px 90px rgba(0, 0, 0, 0.36);
}

.sb-modal-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 12px;
	padding: 18px 20px;
	border-bottom: 1px solid #edf1f7;
}

.sb-modal-header > div {
	display: flex;
	align-items: center;
	gap: 10px;
	color: #08204e;
}

.sb-modal-header strong {
	font-size: 15px;
	font-weight: 950;
}

.sb-modal-close {
	display: grid;
	place-items: center;
	width: 36px;
	height: 36px;
	color: #64748b;
	background: transparent;
	border: 0;
	border-radius: 12px;
	cursor: pointer;
}

.sb-modal-close:hover {
	color: #ef4444;
	background: #fff1f2;
}

.sb-modal-body {
	max-height: calc(90vh - 74px);
	overflow-y: auto;
	padding: 22px;
}

.sb-card-loading {
	display: grid;
	place-items: center;
	min-height: 120px;
	color: #64748b;
	font-size: 14px;
	font-weight: 700;
}

.sb-modal-enter-active,
.sb-modal-leave-active {
	transition: opacity 0.2s ease;
}

.sb-modal-enter-from,
.sb-modal-leave-to {
	opacity: 0;
}

.sb-modal-enter-active .sb-modal-content,
.sb-modal-leave-active .sb-modal-content {
	transition: transform 0.2s ease;
}

.sb-modal-enter-from .sb-modal-content,
.sb-modal-leave-to .sb-modal-content {
	transform: translateY(10px) scale(0.97);
}

/* Sales page */
.sb-sales {
	background: #f5f7fb;
}

.sb-sales-hero {
	padding: 72px 0 92px;
}

.sb-sales-hero-inner {
	position: relative;
	z-index: 2;
	display: grid;
	grid-template-columns: minmax(0, 1.08fr) minmax(340px, 0.72fr);
	gap: 56px;
	align-items: center;
}

.sb-sales-copy {
	max-width: 720px;
}

.sb-eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	padding: 8px 12px;
	margin-bottom: 22px;
	color: #facc15;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 999px;
	font-size: 12px;
	font-weight: 950;
	letter-spacing: 0.1em;
}

.sb-sales-copy h1 {
	margin: 0;
	color: #ffffff;
	font-size: clamp(42px, 6vw, 72px);
	font-weight: 950;
	letter-spacing: -0.065em;
	line-height: 0.94;
}

.sb-sales-copy p {
	max-width: 680px;
	margin: 24px 0 0;
	color: rgba(219, 234, 254, 0.9);
	font-size: clamp(17px, 2vw, 21px);
	font-weight: 600;
	line-height: 1.55;
}

.sb-hero-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 14px;
	margin-top: 34px;
}

.sb-hero-primary,
.sb-hero-secondary,
.sb-pricing-cta,
.sb-final-btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 9px;
	min-height: 54px;
	border: 0;
	border-radius: 16px;
	font-size: 15px;
	font-weight: 950;
	cursor: pointer;
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		background 0.18s ease;
}

.sb-hero-primary,
.sb-final-btn {
	padding: 0 24px;
	color: #08204e;
	background: #facc15;
	box-shadow: 0 16px 32px rgba(250, 204, 21, 0.22);
}

.sb-hero-primary:hover,
.sb-final-btn:hover {
	transform: translateY(-2px);
	background: #fde047;
	box-shadow: 0 20px 42px rgba(250, 204, 21, 0.28);
}

.sb-hero-secondary {
	padding: 0 20px;
	color: #ffffff;
	background: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.2);
}

.sb-hero-secondary:hover {
	transform: translateY(-2px);
	background: rgba(255, 255, 255, 0.14);
	border-color: rgba(255, 255, 255, 0.34);
}

.sb-button-spinner {
	width: 18px;
	height: 18px;
	border: 3px solid rgba(8, 32, 78, 0.22);
	border-top-color: #08204e;
	border-radius: 999px;
	animation: sb-spin 0.85s linear infinite;
}

.sb-button-spinner-light {
	border-color: rgba(255, 255, 255, 0.24);
	border-top-color: #ffffff;
}

.sb-trust-row,
.sb-final-trust {
	display: flex;
	flex-wrap: wrap;
	gap: 14px 20px;
	margin-top: 24px;
	color: rgba(219, 234, 254, 0.86);
	font-size: 14px;
	font-weight: 800;
}

.sb-trust-row span,
.sb-final-trust span {
	display: inline-flex;
	align-items: center;
	gap: 7px;
}

.sb-trust-row svg {
	color: #facc15;
}

.sb-pricing-wrap {
	width: 100%;
}

.sb-pricing-card {
	position: relative;
	overflow: hidden;
	background: #ffffff;
	border: 1px solid rgba(255, 255, 255, 0.65);
	border-radius: 32px;
	box-shadow:
		0 34px 90px rgba(2, 8, 23, 0.34),
		0 0 0 1px rgba(255, 255, 255, 0.08) inset;
}

.sb-pricing-ribbon {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 16px;
	color: #78350f;
	background: linear-gradient(135deg, #fde047, #f59e0b);
	font-size: 13px;
	font-weight: 950;
	letter-spacing: 0.11em;
	text-transform: uppercase;
}

.sb-pricing-body {
	padding: 30px;
}

.sb-price-head {
	text-align: center;
}

.sb-price-label {
	display: inline-flex;
	padding: 7px 10px;
	color: #0b5ed7;
	background: #eff6ff;
	border-radius: 999px;
	font-size: 12px;
	font-weight: 900;
	text-transform: uppercase;
	letter-spacing: 0.06em;
}

.sb-price {
	display: flex;
	align-items: flex-end;
	justify-content: center;
	gap: 6px;
	margin-top: 18px;
}

.sb-price span {
	color: #0f172a;
	font-size: 52px;
	font-weight: 950;
	letter-spacing: -0.06em;
	line-height: 1;
}

.sb-price small {
	padding-bottom: 7px;
	color: #64748b;
	font-size: 15px;
	font-weight: 800;
}

.sb-price-head p {
	max-width: 290px;
	margin: 10px auto 0;
	color: #64748b;
	font-size: 14px;
	font-weight: 650;
	line-height: 1.45;
}

.sb-price-list {
	display: grid;
	gap: 12px;
	padding: 18px;
	margin: 26px 0;
	list-style: none;
	background: #f8fbff;
	border: 1px solid #e7f0ff;
	border-radius: 20px;
}

.sb-price-list li {
	display: flex;
	align-items: flex-start;
	gap: 10px;
	color: #334155;
	font-size: 14px;
	font-weight: 850;
}

.sb-price-list svg {
	flex: 0 0 auto;
	color: #1473e6;
}

.sb-pricing-cta {
	width: 100%;
	padding: 0 20px;
	color: #ffffff;
	background: linear-gradient(135deg, #1473e6, #0b5ed7);
	box-shadow: 0 18px 40px rgba(20, 115, 230, 0.25);
}

.sb-pricing-cta:hover {
	transform: translateY(-2px);
	box-shadow: 0 22px 48px rgba(20, 115, 230, 0.33);
}

.sb-payment-note {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 7px;
	margin-top: 14px;
	color: #64748b;
	font-size: 12.5px;
	font-weight: 800;
}

.sb-payment-note svg {
	color: #10b981;
}

.sb-pricing-footer {
	display: grid;
	place-items: center;
	gap: 3px;
	padding: 16px;
	text-align: center;
	background: #f8fafc;
	border-top: 1px solid #edf1f7;
}

.sb-pricing-footer strong {
	color: #08204e;
	font-size: 13px;
	font-weight: 950;
}

.sb-pricing-footer span {
	color: #64748b;
	font-size: 12px;
	font-weight: 700;
}

.sb-social-proof {
	position: relative;
	z-index: 5;
	margin-top: -34px;
}

.sb-stats-grid {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 14px;
	padding: 18px;
	background: #ffffff;
	border: 1px solid rgba(8, 32, 78, 0.08);
	border-radius: 24px;
	box-shadow: 0 20px 60px rgba(8, 32, 78, 0.09);
}

.sb-stat {
	display: flex;
	align-items: center;
	gap: 12px;
	padding: 14px;
	background: #f8fafc;
	border: 1px solid #eef2f7;
	border-radius: 18px;
}

.sb-stat div {
	display: grid;
	place-items: center;
	width: 42px;
	height: 42px;
	color: #1473e6;
	background: #eff6ff;
	border-radius: 14px;
}

.sb-stat strong {
	display: block;
	color: #08204e;
	font-size: 18px;
	font-weight: 950;
	line-height: 1;
}

.sb-stat span {
	display: block;
	margin-top: 3px;
	color: #64748b;
	font-size: 12px;
	font-weight: 800;
}

.sb-section {
	padding: 86px 0;
}

.sb-section-title {
	max-width: 720px;
	margin: 0 auto 42px;
	text-align: center;
}

.sb-section-title-left {
	margin: 0 0 34px;
	text-align: left;
}

.sb-section-title span {
	display: inline-flex;
	margin-bottom: 10px;
	color: #1473e6;
	font-size: 12px;
	font-weight: 950;
	letter-spacing: 0.1em;
	text-transform: uppercase;
}

.sb-section-title h2 {
	margin: 0;
	color: #08204e;
	font-size: clamp(30px, 4vw, 46px);
	font-weight: 950;
	letter-spacing: -0.055em;
	line-height: 1.02;
}

.sb-section-title p {
	margin: 14px 0 0;
	color: #64748b;
	font-size: 17px;
	font-weight: 600;
	line-height: 1.6;
}

.sb-benefits-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 20px;
}

.sb-benefit-card {
	min-height: 260px;
	padding: 26px;
	background: #ffffff;
	border: 1px solid rgba(8, 32, 78, 0.08);
	border-radius: 24px;
	box-shadow:
		0 1px 2px rgba(8, 32, 78, 0.04),
		0 16px 45px rgba(8, 32, 78, 0.045);
	transition: 0.2s ease;
}

.sb-benefit-card:hover {
	transform: translateY(-4px);
	border-color: rgba(20, 115, 230, 0.25);
	box-shadow: 0 24px 65px rgba(8, 32, 78, 0.1);
}

.sb-benefit-icon {
	display: grid;
	place-items: center;
	width: 58px;
	height: 58px;
	margin-bottom: 22px;
	color: #1473e6;
	background: linear-gradient(135deg, #eff6ff, #e0f2fe);
	border-radius: 18px;
}

.sb-benefit-card h3 {
	margin: 0;
	color: #111827;
	font-size: 20px;
	font-weight: 950;
	letter-spacing: -0.02em;
}

.sb-benefit-card p {
	margin: 10px 0 0;
	color: #64748b;
	font-size: 15px;
	line-height: 1.6;
}

.sb-white-section {
	padding: 86px 0;
	background: #ffffff;
	border-top: 1px solid #edf1f7;
	border-bottom: 1px solid #edf1f7;
}

.sb-results-layout {
	display: grid;
	grid-template-columns: minmax(0, 0.94fr) minmax(330px, 0.72fr);
	gap: 70px;
	align-items: center;
}

.sb-results-list {
	display: grid;
	gap: 18px;
}

.sb-result-item {
	display: flex;
	align-items: flex-start;
	gap: 15px;
}

.sb-result-icon {
	display: grid;
	place-items: center;
	flex: 0 0 auto;
	width: 46px;
	height: 46px;
	border-radius: 16px;
}

.sb-result-green {
	color: #059669;
	background: #d1fae5;
}

.sb-result-blue {
	color: #1473e6;
	background: #dbeafe;
}

.sb-result-amber {
	color: #b45309;
	background: #fef3c7;
}

.sb-result-purple {
	color: #7c3aed;
	background: #ede9fe;
}

.sb-result-item h3 {
	margin: 0;
	color: #111827;
	font-size: 18px;
	font-weight: 950;
}

.sb-result-item p {
	margin: 5px 0 0;
	color: #64748b;
	font-size: 15px;
	line-height: 1.55;
}

.sb-ai-preview {
	position: relative;
	padding: 20px;
	background:
		radial-gradient(circle at top right, rgba(20, 115, 230, 0.12), transparent 34%),
		#f8fafc;
	border: 1px solid #e2e8f0;
	border-radius: 34px;
	box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.7);
}

.sb-ai-window {
	position: relative;
	padding: 24px;
	background: #ffffff;
	border: 1px solid #edf1f7;
	border-radius: 26px;
	box-shadow: 0 22px 60px rgba(8, 32, 78, 0.1);
}

.sb-ai-header {
	display: flex;
	align-items: center;
	gap: 12px;
	margin-bottom: 20px;
}

.sb-ai-avatar {
	display: grid;
	place-items: center;
	width: 46px;
	height: 46px;
	color: #ffffff;
	background: linear-gradient(135deg, #1473e6, #0b5ed7);
	border-radius: 999px;
}

.sb-ai-header strong {
	display: block;
	color: #111827;
	font-size: 14px;
	font-weight: 950;
}

.sb-ai-header span {
	display: block;
	margin-top: 2px;
	color: #10b981;
	font-size: 12px;
	font-weight: 900;
}

.sb-ai-message {
	width: fit-content;
	max-width: 92%;
	padding: 14px 16px;
	border-radius: 18px;
	font-size: 14px;
	font-weight: 600;
	line-height: 1.55;
}

.sb-ai-message-left {
	color: #334155;
	background: #f1f5f9;
	border-top-left-radius: 6px;
}

.sb-ai-message-right {
	margin: 14px 0 0 auto;
	color: #ffffff;
	background: #1473e6;
	border-top-right-radius: 6px;
	box-shadow: 0 12px 22px rgba(20, 115, 230, 0.2);
}

.sb-ai-suggestions {
	display: flex;
	flex-wrap: wrap;
	gap: 8px;
	margin-top: 18px;
}

.sb-ai-suggestions span {
	padding: 7px 10px;
	color: #1473e6;
	background: #eff6ff;
	border-radius: 999px;
	font-size: 12px;
	font-weight: 900;
}

.sb-comparison {
	overflow: hidden;
	background: #ffffff;
	border: 1px solid rgba(8, 32, 78, 0.08);
	border-radius: 28px;
	box-shadow: 0 24px 70px rgba(8, 32, 78, 0.08);
}

.sb-comparison-head {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	background: #f8fafc;
}

.sb-comparison-head > div {
	position: relative;
	padding: 26px;
	text-align: center;
}

.sb-comparison-head > div:first-child {
	border-right: 1px solid #e2e8f0;
}

.sb-comparison-head h3 {
	margin: 0;
	color: #64748b;
	font-size: 22px;
	font-weight: 950;
}

.sb-comparison-head p {
	margin: 6px 0 0;
	color: #94a3b8;
	font-size: 13px;
	font-weight: 800;
}

.sb-comparison-head .sb-comparison-plus {
	background: #eff6ff;
}

.sb-comparison-plus span {
	position: absolute;
	top: 0;
	left: 50%;
	transform: translate(-50%, -50%);
	display: inline-flex;
	padding: 6px 12px;
	color: #78350f;
	background: #facc15;
	border-radius: 999px;
	font-size: 10px;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
	box-shadow: 0 8px 20px rgba(250, 204, 21, 0.22);
}

.sb-comparison-plus h3 {
	color: #08204e;
}

.sb-comparison-plus p {
	color: #1473e6;
}

.sb-comparison-rows {
	display: grid;
}

.sb-comparison-row {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	border-top: 1px solid #edf1f7;
}

.sb-free-col,
.sb-plus-col {
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 62px;
	padding: 16px;
	text-align: center;
	font-size: 14px;
}

.sb-free-col {
	gap: 8px;
	color: #64748b;
	border-right: 1px solid #edf1f7;
	background: #ffffff;
}

.sb-free-col svg {
	color: #cbd5e1;
}

.sb-plus-col {
	gap: 9px;
	color: #0f172a;
	background: rgba(239, 246, 255, 0.52);
}

.sb-plus-col svg {
	flex: 0 0 auto;
	color: #1473e6;
}

.sb-plus-col strong {
	font-weight: 950;
}

.sb-faq-section {
	padding-top: 0;
	padding-bottom: 0;
}

.sb-faq-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 16px;
}

.sb-faq-card {
	padding: 22px;
	background: #f8fafc;
	border: 1px solid #edf1f7;
	border-radius: 22px;
}

.sb-faq-card h3 {
	margin: 0;
	color: #111827;
	font-size: 16px;
	font-weight: 950;
}

.sb-faq-card p {
	margin: 8px 0 0;
	color: #64748b;
	font-size: 14px;
	line-height: 1.55;
}

.sb-final-cta {
	padding: 86px 0;
	text-align: center;
}

.sb-final-inner {
	position: relative;
	z-index: 2;
	display: grid;
	place-items: center;
}

.sb-final-inner h2 {
	max-width: 720px;
	margin: 20px auto 0;
	color: #ffffff;
	font-size: clamp(34px, 5vw, 56px);
	font-weight: 950;
	letter-spacing: -0.055em;
	line-height: 1;
}

.sb-final-inner p {
	max-width: 640px;
	margin: 18px auto 0;
	color: rgba(219, 234, 254, 0.88);
	font-size: 18px;
	font-weight: 650;
	line-height: 1.55;
}

.sb-final-btn {
	margin-top: 30px;
	padding: 0 30px;
}

.sb-final-trust {
	justify-content: center;
	color: rgba(219, 234, 254, 0.85);
}

/* Responsive */
@media (max-width: 1024px) {
	.sb-sales-hero-inner,
	.sb-active-layout,
	.sb-results-layout {
		grid-template-columns: 1fr;
	}

	.sb-pricing-wrap {
		max-width: 460px;
		margin-inline: auto;
	}

	.sb-active-sidebar {
		position: static;
	}

	.sb-benefits-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.sb-stats-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 720px) {
	.sb-container {
		width: min(100% - 24px, 1180px);
	}

	.sb-plus-header {
		height: 46px;
		padding: 0 12px;
	}

	.sb-sales-hero {
		padding: 42px 0 62px;
	}

	.sb-sales-hero-inner {
		gap: 34px;
	}

	.sb-sales-copy h1 {
		font-size: 42px;
		letter-spacing: -0.055em;
		line-height: 0.98;
	}

	.sb-sales-copy p {
		font-size: 16px;
	}

	.sb-hero-actions {
		display: grid;
		grid-template-columns: 1fr;
	}

	.sb-hero-primary,
	.sb-hero-secondary,
	.sb-final-btn {
		width: 100%;
	}

	.sb-trust-row {
		gap: 10px;
		font-size: 12.5px;
	}

	.sb-pricing-card {
		border-radius: 26px;
	}

	.sb-pricing-body {
		padding: 22px;
	}

	.sb-price span {
		font-size: 44px;
	}

	.sb-social-proof {
		margin-top: -22px;
	}

	.sb-stats-grid {
		grid-template-columns: 1fr;
		padding: 12px;
	}

	.sb-section,
	.sb-white-section {
		padding: 58px 0;
	}

	.sb-section-title {
		margin-bottom: 28px;
	}

	.sb-benefits-grid,
	.sb-active-benefits-grid,
	.sb-faq-grid {
		grid-template-columns: 1fr;
	}

	.sb-benefit-card {
		min-height: auto;
		padding: 22px;
	}

	.sb-results-layout {
		gap: 32px;
	}

	.sb-comparison-head,
	.sb-comparison-row {
		grid-template-columns: 1fr;
	}

	.sb-comparison-head > div:first-child,
	.sb-free-col {
		border-right: 0;
		border-bottom: 1px solid #edf1f7;
	}

	.sb-comparison-plus span {
		top: 8px;
		transform: translateX(-50%);
	}

	.sb-active-hero-inner {
		padding: 42px 0;
	}

	.sb-active-hero-content {
		flex-direction: column;
		align-items: flex-start;
		gap: 20px;
	}

	.sb-active-copy h1 {
		font-size: 40px;
	}

	.sb-active-copy p {
		font-size: 16px;
	}

	.sb-panel {
		padding: 20px;
	}

	.sb-panel-header {
		align-items: flex-start;
		flex-direction: column;
	}

	.sb-receipt-row {
		align-items: flex-start;
		flex-direction: column;
	}

	.sb-receipt-actions {
		width: 100%;
		justify-content: space-between;
	}
}
</style>
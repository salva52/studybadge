<template>
	<div class="plus-page min-h-screen pb-16">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b px-4 py-3 shadow-sm plus-header"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
		</header>

		<!-- Loading State -->
		<div v-if="billing.data === undefined" class="flex justify-center items-center py-24">
			<div class="flex flex-col items-center gap-4">
				<div class="relative">
					<div class="size-16 rounded-full plus-loading-ring animate-spin"></div>
					<Crown class="size-6 text-amber-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
				</div>
				<span class="text-sm font-medium plus-text-muted animate-pulse">{{ __('Cargando tu plan...') }}</span>
			</div>
		</div>

		<div v-else>

			<!-- ═══════════════════════════════════════════
			     ESTADO 2: PLAN ACTIVO
			     ═══════════════════════════════════════════ -->
			<div v-if="billing.data?.active">

				<!-- Hero Activo -->
				<div class="plus-hero-active relative overflow-hidden">
					<div class="plus-hero-glow-1"></div>
					<div class="plus-hero-glow-2"></div>
					<div class="plus-hero-grid"></div>
					<div class="mx-auto max-w-5xl relative z-10 px-6 py-14 sm:py-20">
						<div class="flex flex-col sm:flex-row items-center sm:items-start gap-8">
							<div class="plus-crown-badge shrink-0">
								<Crown class="size-10 sm:size-12 text-amber-400 drop-shadow-lg" />
							</div>
							<div class="text-center sm:text-left">
								<div class="inline-flex items-center gap-2 rounded-full bg-green-500/20 border border-green-400/30 px-4 py-1.5 text-xs font-bold text-green-300 uppercase tracking-wider mb-4 backdrop-blur-sm">
									<span class="relative flex h-2 w-2">
										<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
										<span class="relative inline-flex rounded-full h-2 w-2 bg-green-400"></span>
									</span>
									{{ __('Plan activo') }}
								</div>
								<h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
									{{ __('Tu membresía') }}
									<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-yellow-200 to-amber-400">Plus</span>
								</h1>
								<p class="mt-4 text-base sm:text-lg text-blue-100/80 max-w-xl font-medium">
									{{ __('Gestiona tu plan, revisa tus beneficios y descarga tus recibos.') }}
								</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Contenido Activo -->
				<div class="mx-auto max-w-5xl px-5 py-10">
					<div class="grid gap-8 lg:grid-cols-3 items-start">

						<!-- Main: Beneficios + Recibos -->
						<div class="lg:col-span-2 space-y-8">

							<!-- Beneficios Activos -->
							<div class="plus-card p-6 sm:p-8">
								<h2 class="text-xl font-bold plus-text-primary mb-6 flex items-center gap-3">
									<div class="plus-icon-badge bg-blue-500/10 text-blue-500">
										<Sparkles class="size-5" />
									</div>
									{{ __('Tus beneficios activos') }}
								</h2>
								<div class="grid gap-3 sm:grid-cols-2">
									<div
										v-for="benefit in benefits"
										:key="benefit.label"
										class="plus-benefit-item group"
									>
										<div class="plus-benefit-icon">
											<component :is="benefit.icon" class="size-5" />
										</div>
										<div class="min-w-0">
											<div class="font-bold text-sm plus-text-primary">{{ benefit.label }}</div>
											<div class="mt-0.5 text-xs plus-text-muted leading-relaxed">{{ benefit.description }}</div>
										</div>
										<CheckCircle2 class="size-4 text-green-500 shrink-0 ml-auto opacity-60" />
									</div>
								</div>
							</div>

							<!-- Historial de Pagos -->
							<div class="plus-card p-6 sm:p-8">
								<div class="flex items-center justify-between gap-4 border-b plus-border pb-5 mb-5">
									<h2 class="text-xl font-bold plus-text-primary flex items-center gap-3">
										<div class="plus-icon-badge bg-gray-500/10 text-gray-500">
											<Download class="size-5" />
										</div>
										{{ __('Historial de pagos') }}
									</h2>
									<button
										class="plus-btn-ghost text-xs"
										@click="billing.reload()"
									>
										<RefreshCcw class="size-3.5" :class="{'animate-spin': billing.loading}" />
										{{ __('Actualizar') }}
									</button>
								</div>

								<!-- Receipts List -->
								<div v-if="receipts.length" class="space-y-3">
									<div
										v-for="receipt in receipts"
										:key="receipt.name"
										class="plus-receipt-row"
									>
										<div class="min-w-0 flex-1">
											<div class="font-bold text-sm plus-text-primary truncate">
												{{ receipt.receipt_number || receipt.name }}
											</div>
											<div class="flex items-center gap-2 mt-1 text-xs plus-text-muted">
												<CalendarDays class="size-3.5 shrink-0" />
												{{ formatDate(receipt.paid_at || receipt.date_created) }}
												<span class="plus-status-pill" :class="receipt.status === 'paid' ? 'plus-status-paid' : 'plus-status-default'">
													{{ receipt.status }}
												</span>
											</div>
										</div>
										<div class="flex items-center gap-4 shrink-0">
											<span class="font-bold text-sm plus-text-primary">{{ formatMoney(receipt.amount, receipt.currency) }}</span>
											<button class="plus-btn-outline text-xs" @click="downloadReceipt(receipt)">
												<Download class="size-3.5" /> PDF
											</button>
										</div>
									</div>
								</div>

								<!-- Empty Receipts -->
								<div v-else class="plus-empty-state py-12">
									<div class="plus-empty-icon">
										<Download class="size-8" />
									</div>
									<h3 class="text-base font-bold plus-text-primary mt-4">{{ __('Todavía no hay recibos') }}</h3>
									<p class="text-sm plus-text-muted mt-1 max-w-xs">{{ __('Cuando Mercado Pago confirme un cobro, aparecerá aquí tu comprobante.') }}</p>
								</div>
							</div>
						</div>

						<!-- Sidebar -->
						<div class="space-y-6">

							<!-- Estado del Plan -->
							<div class="plus-card relative overflow-hidden">
								<div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 via-blue-400 to-cyan-400"></div>
								<div class="p-6">
									<div class="flex justify-between items-start mb-5">
										<div>
											<h3 class="font-bold text-lg plus-text-primary">StudyBadge Plus</h3>
											<div class="text-sm plus-text-muted mt-0.5">{{ formattedPrice }} / {{ __('mes') }}</div>
										</div>
										<Badge theme="green" class="font-bold text-xs">
											<CheckCircle2 class="size-3 mr-1" /> {{ __('Activo') }}
										</Badge>
									</div>

									<div class="space-y-3">
										<div class="plus-info-row">
											<CalendarDays class="size-4 plus-text-muted shrink-0" />
											<div class="min-w-0">
												<div class="text-[10px] plus-text-muted font-bold uppercase tracking-wider">{{ __('Próximo cobro') }}</div>
												<div class="text-sm font-semibold plus-text-primary mt-0.5">{{ formatDate(subscription.next_payment_date) }}</div>
											</div>
										</div>
										<div class="plus-info-row">
											<CreditCard class="size-4 plus-text-muted shrink-0" />
											<div class="min-w-0">
												<div class="text-[10px] plus-text-muted font-bold uppercase tracking-wider">{{ __('Método de pago') }}</div>
												<div class="text-sm font-semibold plus-text-primary mt-0.5 truncate">{{ paymentMethodLabel }}</div>
											</div>
										</div>
									</div>

									<!-- Cancellation Warning -->
									<div v-if="subscription.cancel_at_period_end" class="mt-5 rounded-xl bg-amber-500/10 border border-amber-500/20 p-4 text-sm">
										<span class="font-bold text-amber-600 dark:text-amber-400 block mb-1">{{ __('Cancelación programada') }}</span>
										<span class="text-amber-700 dark:text-amber-300 text-xs">
											{{ __('Tu suscripción se cancelará el {0}.', [formatDate(subscription.cancel_scheduled_for)]) }}
										</span>
									</div>

									<!-- Action Buttons -->
									<div class="mt-6 space-y-2.5">
										<button
											v-if="!subscription.cancel_at_period_end"
											class="plus-btn-primary w-full"
											@click="showPaymentMethodForm"
										>
											<CreditCard class="size-4" /> {{ __('Gestionar suscripción') }}
										</button>
										<button
											v-if="!subscription.cancel_at_period_end"
											class="plus-btn-danger-ghost w-full"
											:disabled="cancelResource.loading"
											@click="requestCancellation"
										>
											{{ __('Cancelar plan') }}
										</button>
										<button
											v-if="subscription.cancel_at_period_end"
											class="plus-btn-primary w-full"
											:disabled="reactivateResource.loading"
											@click="reactivateSubscription"
										>
											<RefreshCcw class="size-4" /> {{ __('Reactivar mi Plus') }}
										</button>
									</div>
								</div>
							</div>

							<!-- Soporte -->
							<div class="plus-card-support p-6 text-center">
								<LifeBuoy class="size-7 mx-auto mb-3 opacity-70" />
								<h3 class="font-bold text-sm plus-text-primary">{{ __('¿Necesitas ayuda?') }}</h3>
								<p class="mt-1.5 text-xs plus-text-muted mb-4 leading-relaxed">{{ __('Nuestro equipo está listo para ayudarte.') }}</p>
								<a
									class="plus-btn-ghost text-xs inline-flex"
									:href="`mailto:${billing.data?.support_email || 'soporte@studybadge.com'}`"
								>
									<Mail class="size-3.5" /> {{ __('Contactar Soporte') }}
								</a>
							</div>
						</div>
					</div>
				</div>

				<!-- Card Form Modal -->
				<Teleport to="body">
					<Transition name="plus-modal">
						<div v-if="cardFormVisible" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="hidePaymentMethodForm">
							<div class="fixed inset-0 bg-black/60 backdrop-blur-sm"></div>
							<div class="plus-modal-content relative z-10 w-full max-w-md max-h-[90vh] flex flex-col">
								<div class="flex justify-between items-center px-6 py-4 border-b plus-border">
									<div class="flex items-center gap-3">
										<ShieldCheck class="size-5 text-green-500" />
										<span class="font-bold plus-text-primary">{{ __('Actualizar método de pago') }}</span>
									</div>
									<button @click="hidePaymentMethodForm" class="plus-text-muted hover:plus-text-primary transition-colors p-1 rounded-lg">
										<XCircle class="size-5" />
									</button>
								</div>
								<div class="p-6 overflow-y-auto">
									<div v-if="cardFormLoading" class="flex justify-center py-10 text-sm plus-text-muted animate-pulse">
										{{ __('Estableciendo conexión segura...') }}
									</div>
									<div id="studybadge-mp-card-form"></div>
								</div>
							</div>
						</div>
					</Transition>
				</Teleport>
			</div>

			<!-- ═══════════════════════════════════════════
			     ESTADO 1: SIN PLAN — PÁGINA DE VENTA
			     ═══════════════════════════════════════════ -->
			<div v-else>

				<!-- Hero de Venta -->
				<div class="plus-hero-sell relative overflow-hidden text-center">
					<div class="plus-hero-glow-1"></div>
					<div class="plus-hero-glow-2"></div>
					<div class="plus-hero-grid"></div>
					<div class="mx-auto max-w-3xl relative z-10 px-6 py-20 sm:py-28">
						<div class="plus-crown-badge mx-auto mb-8">
							<Crown class="size-12 text-amber-400 drop-shadow-lg" />
						</div>
						<h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight mb-6">
							{{ __('Desbloquea') }}
							<br class="sm:hidden" />
							<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-yellow-200 to-amber-400 animate-gradient-x">StudyBadge Plus</span>
						</h1>
						<p class="text-lg sm:text-xl text-blue-100/80 font-medium max-w-2xl mx-auto leading-relaxed">
							{{ __('Impulsa tu carrera con certificados, Tutor IA ilimitado, calendario inteligente y herramientas premium de estudio.') }}
						</p>
					</div>
				</div>

				<!-- Pricing + Beneficios -->
				<div class="mx-auto max-w-5xl px-5 py-12 -mt-10 relative z-20">
					<div class="grid gap-8 lg:grid-cols-3 items-start">

						<!-- Pricing Card (sticky) -->
						<div class="lg:col-span-1 order-first lg:order-last sticky top-24">
							<div class="plus-pricing-card overflow-hidden">
								<div class="bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-500 py-2 text-center">
									<span class="text-xs font-extrabold uppercase tracking-widest text-amber-900">{{ __('Membresía Plus') }}</span>
								</div>
								<div class="p-8 text-center">
									<div class="flex items-end justify-center gap-1 mb-1">
										<span class="text-5xl font-black plus-text-primary tracking-tight">{{ formattedPrice }}</span>
										<span class="pb-2 text-base font-medium plus-text-muted">/ {{ __('mes') }}</span>
									</div>
									<p class="text-sm plus-text-muted mb-8">{{ __('Cancela cuando quieras. Sin compromisos.') }}</p>

									<button
										class="plus-btn-cta w-full text-base"
										:disabled="activating"
										@click="subscription?.init_point ? openExistingCheckout() : activatePlus()"
									>
										<span v-if="activating" class="animate-spin mr-2">⏳</span>
										{{ subscription?.init_point ? __('Continuar pago pendiente') : __('Suscribirme ahora') }}
									</button>

									<div class="mt-6 flex items-center justify-center gap-2 text-xs plus-text-muted">
										<ShieldCheck class="size-4 text-green-500" />
										{{ __('Pago 100% seguro con Mercado Pago') }}
									</div>
								</div>
							</div>
						</div>

						<!-- Beneficios + Confianza -->
						<div class="lg:col-span-2 space-y-10">

							<!-- Beneficios Grid -->
							<div>
								<h2 class="text-2xl font-bold plus-text-primary mb-8 flex items-center gap-3">
									<Sparkles class="size-6 text-amber-500" />
									{{ __('Beneficios exclusivos') }}
								</h2>
								<div class="grid gap-4 sm:grid-cols-2">
									<div
										v-for="benefit in benefits"
										:key="benefit.label"
										class="plus-benefit-card group"
									>
										<div class="plus-benefit-card-icon group-hover:scale-110 transition-transform">
											<component :is="benefit.icon" class="size-6" />
										</div>
										<div>
											<div class="font-bold text-base plus-text-primary">{{ benefit.label }}</div>
											<div class="mt-1 text-sm plus-text-muted leading-relaxed">{{ benefit.description }}</div>
										</div>
									</div>
								</div>
							</div>

							<!-- Confianza -->
							<div class="plus-card p-8">
								<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
									<div v-for="trust in trustPoints" :key="trust.label" class="flex flex-col items-center text-center gap-2">
										<div class="plus-trust-icon">
											<component :is="trust.icon" class="size-6" />
										</div>
										<span class="text-sm font-bold plus-text-primary">{{ trust.label }}</span>
										<span class="text-xs plus-text-muted">{{ trust.sub }}</span>
									</div>
								</div>
							</div>

							<!-- Empty Recibos -->
							<div class="plus-card p-8 text-center">
								<div class="plus-empty-icon mx-auto">
									<Download class="size-8" />
								</div>
								<h3 class="text-lg font-bold plus-text-primary mt-4">{{ __('Aún no tienes recibos') }}</h3>
								<p class="mt-2 text-sm plus-text-muted max-w-sm mx-auto mb-6">
									{{ __('Cuando realices tu primer pago, tus comprobantes aparecerán aquí.') }}
								</p>
								<button class="plus-btn-outline text-sm" @click="billing.reload()" :disabled="billing.loading">
									<RefreshCcw class="size-4" :class="{'animate-spin': billing.loading}" /> {{ __('Actualizar') }}
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject, nextTick, onBeforeUnmount, ref } from 'vue'
import { Badge, Breadcrumbs, Button, createResource, toast, usePageMeta } from 'frappe-ui'
import {
	Award,
	Bot,
	CalendarDays,
	CheckCircle2,
	CreditCard,
	Crown,
	Download,
	LifeBuoy,
	RefreshCcw,
	Sparkles,
	XCircle,
	ShieldCheck,
	Mail,
	Info,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const activating = ref(false)
const cardFormVisible = ref(false)
const cardFormLoading = ref(false)
const cardController = ref(null)
const mercadoPagoLoader = ref(null)
const user = inject('$user')

const benefits = [
	{
		icon: Award,
		label: __('Certificados desbloqueados'),
		description: __('Accede a certificados de cursos inscritos con certificado pagado.'),
	},
	{
		icon: Bot,
		label: __('TutorIA ilimitado'),
		description: __('Mensajes ilimitados en el tutor global y tutor por curso.'),
	},
	{
		icon: Sparkles,
		label: __('IA motivacional'),
		description: __('Beneficio incluido para herramientas inteligentes de estudio.'),
	},
	{
		icon: CalendarDays,
		label: __('Calendario y seguimiento'),
		description: __('Organiza evaluaciones y actividades con funciones Plus.'),
	},
	{
		icon: CheckCircle2,
		label: __('Insignia PRO'),
		description: __('Tu perfil muestra que eres miembro Plus de StudyBadge.'),
	},
	{
		icon: Crown,
		label: __('Cursos propios ilimitados'),
		description: __('Beneficio mostrado para la generacion de cursos propios.'),
	},
]

const trustPoints = [
	{ icon: ShieldCheck, label: __('Pago seguro'), sub: __('Con Mercado Pago') },
	{ icon: RefreshCcw, label: __('Cancela cuando quieras'), sub: __('Sin contratos') },
	{ icon: Sparkles, label: __('Activación inmediata'), sub: __('Disfruta al instante') },
	{ icon: Download, label: __('Recibos en PDF'), sub: __('Comprobantes claros') },
]

const billing = createResource({
	url: 'lms.lms.subscriptions.get_plus_billing',
	auto: true,
	onSuccess(data) {
		if (data.active) {
			user.reload?.()
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

const subscription = computed(() => billing.data?.subscription)
const receipts = computed(() => billing.data?.receipts || [])

const formattedPrice = computed(() => {
	const plan = billing.data?.plan
	if (!plan) return 'S/ 29'
	if (plan.currency === 'PEN') return `S/ ${Number(plan.amount).toFixed(0)}`
	return `${plan.currency} ${Number(plan.amount).toFixed(0)}`
})

const paymentMethodLabel = computed(() => {
	const method = subscription.value?.payment_method
	if (!method?.id && !method?.card_last_four) {
		return __('Mercado Pago')
	}
	if (method.card_last_four) {
		return `${method.card_brand || method.name || __('Tarjeta')} **** ${method.card_last_four}`
	}
	return method.name || method.id
})

function activatePlus() {
	activating.value = true
	checkout.submit(
		{},
		{
			onSuccess(url) {
				window.location.href = url
			},
			onError(err) {
				activating.value = false
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

function openExistingCheckout() {
	window.location.href = subscription.value.init_point
}

function requestCancellation() {
	if (!window.confirm(__('Tu Plus seguira activo hasta el final del periodo.'))) {
		return
	}
	cancelResource.submit(
		{},
		{
			onSuccess(data) {
				billing.data = data
				toast.success(__('Cancelacion programada.'))
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
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
				toast.error(err.messages?.[0] || err)
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
					amount: Number(billing.data?.plan?.amount || 29),
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
							paymentMethodResource.submit(
								{ card_token_id: cardToken },
								{
									onSuccess(data) {
										billing.data = data
										hidePaymentMethodForm()
										toast.success(__('Metodo de pago actualizado.'))
										resolve()
									},
									onError(err) {
										toast.error(err.messages?.[0] || err)
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
	window.open(receipt.download_url, '_blank', 'noopener')
}

function formatDate(value) {
	if (!value) return __('Pendiente')
	return new Intl.DateTimeFormat('es-PE', {
		dateStyle: 'medium',
		timeStyle: 'short',
	}).format(new Date(value))
}

function formatMoney(amount, currency) {
	if (currency === 'PEN' || !currency) {
		return `S/ ${Number(amount || 0).toFixed(2)}`
	}
	return `${currency} ${Number(amount || 0).toFixed(2)}`
}

function formatSubscriptionStatus(status) {
	if (!status) return ''
	if (status === 'authorized' || status === 'active') return __('Activa')
	if (status === 'pending') return __('Pendiente de pago')
	if (status === 'cancelled') return __('Cancelada')
	return status.charAt(0).toUpperCase() + status.slice(1)
}

onBeforeUnmount(() => {
	destroyCardForm()
})

const breadcrumbs = computed(() => [
	{
		label: __('StudyBadge Plus'),
		route: { name: 'Plus' },
	},
])

usePageMeta(() => {
	return {
		title: __('StudyBadge Plus'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
/* ═══════════════════════════════════════
   PLUS PAGE — LIGHT & DARK TOKENS
   ═══════════════════════════════════════ */

.plus-page {
	background: var(--sb-bg);
	font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.plus-header {
	background: var(--sb-white);
	border-color: rgba(6, 27, 73, 0.06);
}

:root[data-theme="dark"] .plus-header {
	border-color: rgba(255, 255, 255, 0.06);
}

/* Text */
.plus-text-primary { color: #111827; }
.plus-text-muted { color: #6b7280; }
:root[data-theme="dark"] .plus-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .plus-text-muted { color: #9ca3af; }

/* Border */
.plus-border { border-color: rgba(0, 0, 0, 0.06); }
:root[data-theme="dark"] .plus-border { border-color: rgba(255, 255, 255, 0.08); }

/* ═══════════════════════════════════════
   HERO SECTIONS
   ═══════════════════════════════════════ */

.plus-hero-active,
.plus-hero-sell {
	background: linear-gradient(145deg, #061B49 0%, #0b2f73 40%, #0a2259 100%);
}

.plus-hero-glow-1 {
	position: absolute;
	top: -120px;
	right: -80px;
	width: 400px;
	height: 400px;
	background: radial-gradient(circle, rgba(59, 130, 246, 0.25), transparent 70%);
	border-radius: 50%;
	filter: blur(60px);
}

.plus-hero-glow-2 {
	position: absolute;
	bottom: -100px;
	left: -60px;
	width: 300px;
	height: 300px;
	background: radial-gradient(circle, rgba(245, 179, 1, 0.12), transparent 70%);
	border-radius: 50%;
	filter: blur(50px);
}

.plus-hero-grid {
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
	background-size: 48px 48px;
}

.plus-crown-badge {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 1.25rem;
	border-radius: 1.25rem;
	background: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.12);
	backdrop-filter: blur(12px);
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

/* ═══════════════════════════════════════
   CARDS
   ═══════════════════════════════════════ */

.plus-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.06);
	border-radius: 20px;
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.04), 0 4px 12px rgba(6, 27, 73, 0.03);
	transition: all 0.2s ease;
}

:root[data-theme="dark"] .plus-card {
	border-color: rgba(255, 255, 255, 0.06);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.15);
}

.plus-card-support {
	background: rgba(59, 130, 246, 0.04);
	border: 1px solid rgba(59, 130, 246, 0.1);
	border-radius: 20px;
}

:root[data-theme="dark"] .plus-card-support {
	background: rgba(59, 130, 246, 0.08);
	border-color: rgba(59, 130, 246, 0.15);
}

/* ═══════════════════════════════════════
   PRICING CARD
   ═══════════════════════════════════════ */

.plus-pricing-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.08);
	border-radius: 24px;
	box-shadow: 0 4px 6px rgba(6, 27, 73, 0.04), 0 20px 48px rgba(6, 27, 73, 0.08);
}

:root[data-theme="dark"] .plus-pricing-card {
	border-color: rgba(255, 255, 255, 0.08);
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2), 0 20px 48px rgba(0, 0, 0, 0.3);
}

/* ═══════════════════════════════════════
   BENEFIT ITEMS (Active state)
   ═══════════════════════════════════════ */

.plus-benefit-item {
	display: flex;
	align-items: center;
	gap: 12px;
	padding: 14px 16px;
	border-radius: 14px;
	background: rgba(59, 130, 246, 0.03);
	border: 1px solid rgba(59, 130, 246, 0.06);
	transition: all 0.2s ease;
}

.plus-benefit-item:hover {
	background: rgba(59, 130, 246, 0.06);
	border-color: rgba(59, 130, 246, 0.12);
}

:root[data-theme="dark"] .plus-benefit-item {
	background: rgba(59, 130, 246, 0.05);
	border-color: rgba(59, 130, 246, 0.1);
}

:root[data-theme="dark"] .plus-benefit-item:hover {
	background: rgba(59, 130, 246, 0.1);
	border-color: rgba(59, 130, 246, 0.18);
}

.plus-benefit-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
	background: rgba(59, 130, 246, 0.08);
	color: #3b82f6;
	flex-shrink: 0;
}

:root[data-theme="dark"] .plus-benefit-icon {
	background: rgba(59, 130, 246, 0.15);
	color: #60a5fa;
}

/* BENEFIT CARDS (Sale state) */
.plus-benefit-card {
	display: flex;
	align-items: flex-start;
	gap: 16px;
	padding: 20px;
	border-radius: 18px;
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.06);
	box-shadow: 0 1px 4px rgba(6, 27, 73, 0.04);
	transition: all 0.25s ease;
}

.plus-benefit-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 24px rgba(6, 27, 73, 0.1);
	border-color: rgba(59, 130, 246, 0.15);
}

:root[data-theme="dark"] .plus-benefit-card {
	border-color: rgba(255, 255, 255, 0.06);
	box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

:root[data-theme="dark"] .plus-benefit-card:hover {
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
	border-color: rgba(59, 130, 246, 0.25);
}

.plus-benefit-card-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 48px;
	height: 48px;
	border-radius: 14px;
	background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.04));
	color: #3b82f6;
	flex-shrink: 0;
	transition: transform 0.2s ease;
}

:root[data-theme="dark"] .plus-benefit-card-icon {
	background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.08));
	color: #60a5fa;
}

/* ═══════════════════════════════════════
   ICON BADGES
   ═══════════════════════════════════════ */

.plus-icon-badge {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
	flex-shrink: 0;
}

/* ═══════════════════════════════════════
   TRUST ICONS
   ═══════════════════════════════════════ */

.plus-trust-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 48px;
	height: 48px;
	border-radius: 14px;
	background: rgba(16, 185, 129, 0.06);
	color: #10b981;
	margin-bottom: 4px;
}

:root[data-theme="dark"] .plus-trust-icon {
	background: rgba(16, 185, 129, 0.1);
	color: #34d399;
}

/* ═══════════════════════════════════════
   INFO ROWS
   ═══════════════════════════════════════ */

.plus-info-row {
	display: flex;
	align-items: flex-start;
	gap: 12px;
	padding: 12px 14px;
	border-radius: 12px;
	background: rgba(0, 0, 0, 0.02);
}

:root[data-theme="dark"] .plus-info-row {
	background: rgba(255, 255, 255, 0.04);
}

/* ═══════════════════════════════════════
   RECEIPT ROWS
   ═══════════════════════════════════════ */

.plus-receipt-row {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	padding: 14px 16px;
	border-radius: 14px;
	background: rgba(0, 0, 0, 0.015);
	border: 1px solid transparent;
	transition: all 0.15s ease;
}

.plus-receipt-row:hover {
	background: rgba(59, 130, 246, 0.03);
	border-color: rgba(59, 130, 246, 0.08);
}

:root[data-theme="dark"] .plus-receipt-row {
	background: rgba(255, 255, 255, 0.03);
}

:root[data-theme="dark"] .plus-receipt-row:hover {
	background: rgba(59, 130, 246, 0.06);
	border-color: rgba(59, 130, 246, 0.12);
}

/* ═══════════════════════════════════════
   STATUS PILLS
   ═══════════════════════════════════════ */

.plus-status-pill {
	display: inline-flex;
	align-items: center;
	padding: 2px 8px;
	border-radius: 20px;
	font-size: 10px;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 0.04em;
}

.plus-status-paid {
	background: rgba(16, 185, 129, 0.1);
	color: #059669;
}

:root[data-theme="dark"] .plus-status-paid {
	background: rgba(16, 185, 129, 0.15);
	color: #34d399;
}

.plus-status-default {
	background: rgba(107, 114, 128, 0.1);
	color: #6b7280;
}

/* ═══════════════════════════════════════
   EMPTY STATE
   ═══════════════════════════════════════ */

.plus-empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	text-align: center;
}

.plus-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 64px;
	height: 64px;
	border-radius: 20px;
	background: rgba(0, 0, 0, 0.03);
	color: #d1d5db;
}

:root[data-theme="dark"] .plus-empty-icon {
	background: rgba(255, 255, 255, 0.05);
	color: #4b5563;
}

/* ═══════════════════════════════════════
   LOADING RING
   ═══════════════════════════════════════ */

.plus-loading-ring {
	border: 3px solid rgba(0, 0, 0, 0.05);
	border-top-color: #3b82f6;
	border-radius: 50%;
}

:root[data-theme="dark"] .plus-loading-ring {
	border-color: rgba(255, 255, 255, 0.08);
	border-top-color: #60a5fa;
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */

.plus-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 12px 20px;
	border-radius: 12px;
	font-size: 14px;
	font-weight: 700;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 2px 8px rgba(13, 110, 253, 0.25);
}

.plus-btn-primary:hover {
	background: linear-gradient(135deg, #0b5ed7, #084298);
	transform: translateY(-1px);
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.35);
}

.plus-btn-primary:disabled {
	opacity: 0.6;
	pointer-events: none;
}

.plus-btn-cta {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 16px 24px;
	border-radius: 14px;
	font-size: 15px;
	font-weight: 800;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	border: none;
	cursor: pointer;
	transition: all 0.25s ease;
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.3);
}

.plus-btn-cta:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 32px rgba(13, 110, 253, 0.4);
}

.plus-btn-cta:disabled {
	opacity: 0.7;
	pointer-events: none;
}

.plus-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 8px 14px;
	border-radius: 10px;
	font-weight: 600;
	color: #374151;
	background: transparent;
	border: 1.5px solid rgba(0, 0, 0, 0.1);
	cursor: pointer;
	transition: all 0.15s ease;
}

.plus-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.18);
}

:root[data-theme="dark"] .plus-btn-outline {
	color: #d1d5db;
	border-color: rgba(255, 255, 255, 0.12);
}

:root[data-theme="dark"] .plus-btn-outline:hover {
	background: rgba(255, 255, 255, 0.06);
	border-color: rgba(255, 255, 255, 0.2);
}

.plus-btn-ghost {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 8px 14px;
	border-radius: 10px;
	font-weight: 600;
	color: #6b7280;
	background: transparent;
	border: none;
	cursor: pointer;
	transition: all 0.15s ease;
}

.plus-btn-ghost:hover {
	background: rgba(0, 0, 0, 0.04);
	color: #374151;
}

:root[data-theme="dark"] .plus-btn-ghost:hover {
	background: rgba(255, 255, 255, 0.06);
	color: #e5e7eb;
}

.plus-btn-danger-ghost {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 10px 16px;
	border-radius: 12px;
	font-size: 13px;
	font-weight: 600;
	color: #9ca3af;
	background: transparent;
	border: none;
	cursor: pointer;
	transition: all 0.15s ease;
}

.plus-btn-danger-ghost:hover {
	color: #ef4444;
	background: rgba(239, 68, 68, 0.06);
}

:root[data-theme="dark"] .plus-btn-danger-ghost:hover {
	background: rgba(239, 68, 68, 0.1);
}

/* ═══════════════════════════════════════
   MODAL
   ═══════════════════════════════════════ */

.plus-modal-content {
	background: var(--sb-white);
	border-radius: 20px;
	box-shadow: 0 24px 64px rgba(0, 0, 0, 0.3);
	overflow: hidden;
}

/* Modal Transition */
.plus-modal-enter-active,
.plus-modal-leave-active {
	transition: all 0.25s ease;
}

.plus-modal-enter-from,
.plus-modal-leave-to {
	opacity: 0;
}

.plus-modal-enter-from .plus-modal-content,
.plus-modal-leave-to .plus-modal-content {
	transform: scale(0.95) translateY(10px);
}

/* ═══════════════════════════════════════
   GRADIENT ANIMATION
   ═══════════════════════════════════════ */

@keyframes gradient-x {
	0%, 100% { background-position: 0% 50%; }
	50% { background-position: 100% 50%; }
}

.animate-gradient-x {
	background-size: 200% auto;
	animation: gradient-x 4s ease infinite;
}
</style>

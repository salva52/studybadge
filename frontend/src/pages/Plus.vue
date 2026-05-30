<template>
	<div class="min-h-screen bg-[#f5f7fb] pb-12 font-sans">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-4 py-3 shadow-sm"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
		</header>

		<div v-if="billing.data === undefined" class="flex justify-center items-center py-20">
			<!-- Loading state -->
			<div class="animate-pulse flex flex-col items-center">
				<div class="h-12 w-12 bg-gray-200 rounded-full mb-4"></div>
				<div class="h-4 w-32 bg-gray-200 rounded"></div>
			</div>
		</div>
		<div v-else>
			<!-- ESTADO 2: CON PLAN ACTIVO -->
			<div v-if="billing.data?.active">
				<!-- Hero Section (Activo) -->
				<div class="bg-[#08204e] text-white py-12 px-5 sm:py-16 sm:px-8 relative overflow-hidden">
					<div class="absolute -top-24 -right-24 size-96 bg-[#0b2f73] opacity-50 blur-3xl rounded-full"></div>
					<div class="mx-auto max-w-5xl relative z-10 flex flex-col sm:flex-row items-center sm:items-start gap-6">
						<div class="rounded-2xl bg-white/10 p-4 ring-1 ring-white/20 backdrop-blur-md shadow-lg shrink-0">
							<Crown class="size-12 text-amber-400" />
						</div>
						<div class="text-center sm:text-left">
							<h1 class="text-3xl sm:text-4xl font-bold tracking-tight">
								{{ __('Tu membresía StudyBadge Plus está activa') }}
							</h1>
							<p class="mt-3 text-lg text-blue-100 max-w-2xl font-medium">
								{{ __('Gestiona tu plan, revisa tus beneficios y descarga tus recibos.') }}
							</p>
						</div>
					</div>
				</div>

				<div class="mx-auto max-w-5xl px-5 py-10">
					<div class="grid gap-8 lg:grid-cols-3 items-start">
						<!-- Main Column -->
						<div class="lg:col-span-2 space-y-8">
							<!-- Beneficios Activos -->
							<div class="rounded-2xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
								<h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
									<Sparkles class="size-6 text-[#0d6efd]" />
									{{ __('Tus beneficios activos') }}
								</h2>
								<div class="grid gap-4 sm:grid-cols-2">
									<div
										v-for="benefit in benefits"
										:key="benefit.label"
										class="flex items-start gap-3 rounded-xl border border-blue-50 bg-blue-50/30 p-4 transition-all hover:bg-blue-50/50"
									>
										<div class="rounded-full bg-blue-100 p-2 shrink-0">
											<component
												:is="benefit.icon"
												class="size-5 text-[#0d6efd]"
											/>
										</div>
										<div>
											<div class="font-bold text-gray-900 text-sm">
												{{ benefit.label }}
											</div>
											<div class="mt-1 text-xs text-gray-600">
												{{ benefit.description }}
											</div>
										</div>
									</div>
								</div>
							</div>

							<!-- Historial de Recibos (Activo) -->
							<div class="rounded-2xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
								<div class="flex items-center justify-between gap-4 border-b border-gray-100 pb-5 mb-5">
									<h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
										<Download class="size-5 text-gray-500" />
										{{ __('Historial de pagos') }}
									</h2>
									<Button
										variant="ghost"
										class="text-sm"
										:loading="billing.loading"
										@click="billing.reload()"
									>
										<RefreshCcw class="size-4 mr-1.5" /> {{ __('Actualizar') }}
									</Button>
								</div>
								
								<div v-if="receipts.length" class="divide-y divide-gray-100">
									<div
										v-for="receipt in receipts"
										:key="receipt.name"
										class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 py-4"
									>
										<div>
											<div class="font-bold text-gray-900">
												{{ formatMoney(receipt.amount, receipt.currency) }} • {{ receipt.receipt_number || receipt.name }}
											</div>
											<div class="mt-1 flex items-center gap-2 text-sm text-gray-500">
												<CalendarDays class="size-4" />
												{{ formatDate(receipt.paid_at || receipt.date_created) }}
												<Badge :theme="receipt.status === 'paid' ? 'green' : 'gray'" class="ml-2">
													{{ receipt.status }}
												</Badge>
											</div>
										</div>
										<Button variant="outline" @click="downloadReceipt(receipt)">
											<Download class="size-4 mr-1.5" /> {{ __('Descargar PDF') }}
										</Button>
									</div>
								</div>
								<div v-else class="flex flex-col items-center justify-center py-10 text-center">
									<div class="rounded-full bg-gray-50 p-4 mb-4">
										<Download class="size-8 text-gray-300" />
									</div>
									<h3 class="text-base font-bold text-gray-900">{{ __('Todavía no hay recibos disponibles') }}</h3>
									<p class="mt-1 text-sm text-gray-500 max-w-sm">{{ __('Cuando Mercado Pago confirme un cobro, aparecerá aquí tu comprobante.') }}</p>
								</div>
							</div>
						</div>

						<!-- Sidebar Column -->
						<div class="space-y-6">
							<!-- Estado del plan -->
							<div class="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm relative overflow-hidden">
								<div class="absolute top-0 left-0 w-full h-1 bg-[#0d6efd]"></div>
								<div class="flex justify-between items-start mb-4">
									<div>
										<h3 class="font-bold text-gray-900 text-lg">{{ __('StudyBadge Plus') }}</h3>
										<div class="text-sm text-gray-500 mt-0.5">{{ formattedPrice }} / {{ __('mes') }}</div>
									</div>
									<Badge theme="green" class="font-bold">
										<CheckCircle2 class="size-3 mr-1" /> {{ __('Activo') }}
									</Badge>
								</div>

								<div class="space-y-4 mt-6">
									<div class="bg-gray-50 rounded-lg p-3">
										<div class="text-xs text-gray-500 font-semibold uppercase mb-1">{{ __('Próximo cobro') }}</div>
										<div class="font-medium text-gray-900">{{ formatDate(subscription.next_payment_date) }}</div>
									</div>
									<div class="bg-gray-50 rounded-lg p-3">
										<div class="text-xs text-gray-500 font-semibold uppercase mb-1">{{ __('Método de pago') }}</div>
										<div class="font-medium text-gray-900 truncate">{{ paymentMethodLabel }}</div>
									</div>
								</div>

								<div
									v-if="subscription.cancel_at_period_end"
									class="mt-4 rounded-lg bg-amber-50 p-3 text-sm text-amber-900 border border-amber-100"
								>
									<span class="font-bold block mb-1">{{ __('Cancelación programada') }}</span>
									{{ __('Tu suscripción se cancelará el {0}.', [formatDate(subscription.cancel_scheduled_for)]) }}
								</div>

								<div class="mt-6 space-y-3">
									<Button
										v-if="!subscription.cancel_at_period_end"
										variant="solid"
										class="w-full justify-center bg-[#0d6efd] hover:bg-[#0b2f73] text-white"
										@click="showPaymentMethodForm"
									>
										{{ __('Gestionar suscripción') }}
									</Button>
									<Button
										v-if="!subscription.cancel_at_period_end"
										variant="ghost"
										class="w-full justify-center text-gray-500 hover:text-red-600 hover:bg-red-50"
										:loading="cancelResource.loading"
										@click="requestCancellation"
									>
										{{ __('Cancelar plan') }}
									</Button>
									<Button
										v-if="subscription.cancel_at_period_end"
										variant="solid"
										theme="blue"
										class="w-full justify-center"
										:loading="reactivateResource.loading"
										@click="reactivateSubscription"
									>
										<RefreshCcw class="size-4 mr-1.5" /> {{ __('Reactivar mi Plus') }}
									</Button>
								</div>
							</div>

							<!-- Soporte -->
							<div class="rounded-2xl border border-blue-100 bg-blue-50 p-6 text-center">
								<LifeBuoy class="size-8 text-[#0d6efd] mx-auto mb-3" />
								<h3 class="font-bold text-gray-900">{{ __('¿Necesitas ayuda?') }}</h3>
								<p class="mt-2 text-xs text-gray-600 mb-4">{{ __('Nuestro equipo de soporte está listo para ayudarte con tu suscripción.') }}</p>
								<a
									class="inline-block text-sm font-bold text-[#0d6efd] hover:text-[#0b2f73]"
									:href="`mailto:${billing.data?.support_email || 'soporte@studybadge.com'}`"
								>
									{{ __('Contactar Soporte') }} &rarr;
								</a>
							</div>
						</div>
					</div>
				</div>

				<!-- Modal para tarjeta (if needed to display within page) -->
				<div v-if="cardFormVisible" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
					<div class="bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
						<div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
							<div class="font-bold text-gray-900">{{ __('Actualizar método de pago') }}</div>
							<button @click="hidePaymentMethodForm" class="text-gray-400 hover:text-gray-600">
								<XCircle class="size-6" />
							</button>
						</div>
						<div class="p-6 overflow-y-auto">
							<div v-if="cardFormLoading" class="flex justify-center py-8 text-sm text-gray-500 animate-pulse">
								{{ __('Estableciendo conexión segura...') }}
							</div>
							<div id="studybadge-mp-card-form"></div>
						</div>
					</div>
				</div>

			</div>
			
			<!-- ESTADO 1: SIN PLAN ACTIVO -->
			<div v-else>
				<!-- Hero Section (Venta) -->
				<div class="bg-[#08204e] text-white py-16 px-5 sm:py-24 sm:px-8 relative overflow-hidden text-center">
					<div class="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-3xl h-full bg-gradient-to-b from-[#0b2f73] to-transparent opacity-50 blur-3xl rounded-full"></div>
					<div class="mx-auto max-w-3xl relative z-10">
						<div class="inline-flex justify-center items-center rounded-2xl bg-white/10 p-4 ring-1 ring-white/20 backdrop-blur-md shadow-lg mb-6">
							<Crown class="size-12 text-amber-400" />
						</div>
						<h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6">
							{{ __('Desbloquea StudyBadge') }} <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-yellow-200">Plus</span>
						</h1>
						<p class="text-lg sm:text-xl text-blue-100 font-medium max-w-2xl mx-auto">
							{{ __('Impulsa tu carrera con certificados, Tutor IA ilimitado, calendario inteligente y herramientas premium de estudio.') }}
						</p>
					</div>
				</div>

				<div class="mx-auto max-w-5xl px-5 py-12 -mt-8 relative z-20">
					<div class="grid gap-8 lg:grid-cols-3 items-start">
						
						<!-- Pricing Card Prominente -->
						<div class="lg:col-span-1 rounded-3xl border border-gray-200 bg-white shadow-xl overflow-hidden order-first lg:order-last sticky top-24">
							<div class="bg-gradient-to-r from-amber-400 to-yellow-500 p-1 text-center text-xs font-bold uppercase tracking-wider text-amber-900">
								{{ __('Membresía Plus') }}
							</div>
							<div class="p-8 text-center">
								<div class="flex items-end justify-center gap-1 mb-2">
									<div class="text-5xl font-black text-gray-900 tracking-tight">
										{{ formattedPrice }}
									</div>
									<div class="pb-2 text-base font-medium text-gray-500">
										/ {{ __('mes') }}
									</div>
								</div>
								<p class="text-sm text-gray-500 mb-8">{{ __('Cancela cuando quieras. Sin compromisos.') }}</p>
								
								<Button
									class="w-full py-6 text-base font-bold shadow-lg shadow-blue-500/30 transition-transform hover:-translate-y-0.5 bg-[#0d6efd] hover:bg-[#0b2f73] text-white rounded-xl"
									size="lg"
									:loading="activating"
									@click="subscription?.init_point ? openExistingCheckout() : activatePlus()"
								>
									{{ subscription?.init_point ? __('Continuar pago pendiente') : __('Suscribirme ahora') }}
								</Button>
								
								<div class="mt-6 flex items-center justify-center gap-2 text-xs text-gray-500">
									<ShieldCheck class="size-4 text-green-500" />
									{{ __('Pago 100% seguro con Mercado Pago') }}
								</div>
							</div>
						</div>

						<!-- Beneficios y Confianza -->
						<div class="lg:col-span-2 space-y-12">
							<div>
								<h2 class="text-2xl font-bold text-gray-900 mb-8 text-center sm:text-left">
									{{ __('Beneficios exclusivos') }}
								</h2>
								<div class="grid gap-4 sm:grid-cols-2">
									<div
										v-for="benefit in benefits"
										:key="benefit.label"
										class="flex items-start gap-4 rounded-2xl border border-gray-100 bg-white p-5 shadow-sm transition-all hover:shadow-md hover:border-blue-100 group"
									>
										<div class="rounded-xl bg-[#f5f7fb] p-3 group-hover:bg-blue-50 transition-colors">
											<component
												:is="benefit.icon"
												class="size-6 text-[#0d6efd]"
											/>
										</div>
										<div>
											<div class="font-bold text-gray-900 text-base">
												{{ benefit.label }}
											</div>
											<div class="mt-1 text-sm text-gray-500 leading-relaxed">
												{{ benefit.description }}
											</div>
										</div>
									</div>
								</div>
							</div>

							<!-- Sección de confianza -->
							<div class="rounded-2xl bg-white border border-gray-100 p-8 shadow-sm">
								<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
									<div class="flex flex-col items-center text-center gap-2">
										<ShieldCheck class="size-8 text-green-500" />
										<span class="text-sm font-bold text-gray-900">{{ __('Pago seguro') }}</span>
										<span class="text-xs text-gray-500">{{ __('Con Mercado Pago') }}</span>
									</div>
									<div class="flex flex-col items-center text-center gap-2">
										<RefreshCcw class="size-8 text-blue-500" />
										<span class="text-sm font-bold text-gray-900">{{ __('Cancela cuando quieras') }}</span>
										<span class="text-xs text-gray-500">{{ __('Sin contratos') }}</span>
									</div>
									<div class="flex flex-col items-center text-center gap-2">
										<Sparkles class="size-8 text-amber-500" />
										<span class="text-sm font-bold text-gray-900">{{ __('Activación inmediata') }}</span>
										<span class="text-xs text-gray-500">{{ __('Disfruta al instante') }}</span>
									</div>
									<div class="flex flex-col items-center text-center gap-2">
										<Download class="size-8 text-gray-500" />
										<span class="text-sm font-bold text-gray-900">{{ __('Recibos en PDF') }}</span>
										<span class="text-xs text-gray-500">{{ __('Comprobantes claros') }}</span>
									</div>
								</div>
							</div>

							<!-- Empty state de recibos (para no usuarios Plus) -->
							<div class="rounded-2xl border border-gray-100 bg-white p-8 text-center shadow-sm">
								<div class="flex justify-center mb-4">
									<div class="rounded-full bg-[#f5f7fb] p-5">
										<Download class="size-8 text-gray-400" />
									</div>
								</div>
								<h3 class="text-lg font-bold text-gray-900">{{ __('Aún no tienes recibos') }}</h3>
								<p class="mt-2 text-sm text-gray-500 max-w-md mx-auto mb-6">
									{{ __('Cuando realices tu primer pago para activar StudyBadge Plus, tus comprobantes aparecerán aquí.') }}
								</p>
								<Button variant="outline" @click="billing.reload()" :loading="billing.loading">
									<RefreshCcw class="size-4 mr-2" /> {{ __('Actualizar') }}
								</Button>
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

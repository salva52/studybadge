<template>
	<div class="min-h-screen bg-surface-gray-2 pb-12">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5 shadow-sm"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<Badge v-if="billing.data?.active" theme="green" class="shadow-sm">
				<Sparkles class="mr-1.5 size-3 inline-block align-text-bottom" />
				{{ __('Plus activo') }}
			</Badge>
		</header>

		<!-- Hero Section -->
		<div class="bg-gradient-to-br from-gray-900 to-gray-800 text-white py-12 px-5 sm:py-16 sm:px-8 border-b border-gray-700 shadow-inner relative overflow-hidden">
			<!-- Subtle background decoration -->
			<div class="absolute -top-24 -right-24 size-96 bg-blue-500 opacity-20 blur-3xl rounded-full"></div>
			<div class="absolute top-1/2 -left-24 size-64 bg-amber-500 opacity-20 blur-3xl rounded-full"></div>
			
			<div class="mx-auto max-w-6xl relative z-10">
				<div class="flex flex-col items-center text-center gap-4">
					<div class="rounded-2xl bg-white/10 p-4 ring-1 ring-white/20 backdrop-blur-md shadow-lg">
						<Crown class="size-10 stroke-1.5 text-amber-400" />
					</div>
					<div>
						<h1 class="text-4xl sm:text-5xl font-bold tracking-tight">
							StudyBadge <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-amber-200">Plus</span>
						</h1>
						<p class="mt-4 text-lg sm:text-xl text-gray-300 max-w-2xl mx-auto font-medium">
							{{ __('Impulsa tu carrera al siguiente nivel con facturación, certificados e Inteligencia Artificial sin límites.') }}
						</p>
					</div>
				</div>
			</div>
		</div>

		<div class="mx-auto max-w-6xl px-5 py-10">
			<div class="grid gap-10 lg:grid-cols-[1fr_380px] items-start">
				
				<!-- Main Content -->
				<section class="space-y-10">
					
					<!-- Beneficios Comerciales -->
					<div>
						<h2 class="text-2xl font-bold text-ink-gray-9 mb-6 flex items-center gap-2">
							<Sparkles class="size-6 text-amber-500" />
							{{ __('Beneficios exclusivos') }}
						</h2>
						<div class="grid gap-4 sm:grid-cols-2">
							<div
								v-for="benefit in benefits"
								:key="benefit.label"
								class="group flex items-start gap-4 rounded-xl border border-gray-200 bg-surface-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-md hover:border-blue-200"
							>
								<div class="rounded-lg bg-blue-50 p-3 group-hover:bg-blue-100 transition-colors">
									<component
										:is="benefit.icon"
										class="size-6 shrink-0 stroke-1.5 text-blue-600"
									/>
								</div>
								<div>
									<div class="font-semibold text-ink-gray-9 text-base">
										{{ benefit.label }}
									</div>
									<div class="mt-1 text-sm leading-relaxed text-ink-gray-6">
										{{ benefit.description }}
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Facturación y Suscripción -->
					<div
						v-if="billing.data?.subscription"
						class="rounded-xl border border-gray-200 bg-surface-white p-6 sm:p-8 shadow-sm transition-all"
					>
						<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-100 pb-5">
							<div>
								<h2 class="text-xl font-bold text-ink-gray-9 flex items-center gap-2">
									<CreditCard class="size-5 text-gray-500" />
									{{ __('Tu Suscripción') }}
								</h2>
								<p class="mt-1 text-sm text-ink-gray-6">
									{{ __('Gestiona tu plan y tus pagos de forma segura.') }}
								</p>
							</div>
							<Badge :theme="billing.data.active ? 'green' : 'gray'" class="w-fit px-3 py-1 text-sm">
								<CheckCircle2 v-if="billing.data.active" class="mr-1 size-4 inline-block align-text-bottom" />
								{{ formatSubscriptionStatus(subscription.status) }}
							</Badge>
						</div>

						<div class="mt-6 grid gap-4 sm:grid-cols-3">
							<div class="rounded-xl bg-gray-50 p-5 border border-gray-100">
								<div class="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
									<CalendarDays class="size-4" />
									{{ __('Próximo cobro') }}
								</div>
								<div class="mt-2 text-lg font-bold text-ink-gray-9">
									{{ formatDate(subscription.next_payment_date) }}
								</div>
							</div>
							<div class="rounded-xl bg-gray-50 p-5 border border-gray-100">
								<div class="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
									<CreditCard class="size-4" />
									{{ __('Método de pago') }}
								</div>
								<div class="mt-2 text-lg font-bold text-ink-gray-9 truncate">
									{{ paymentMethodLabel }}
								</div>
							</div>
							<div class="rounded-xl bg-gray-50 p-5 border border-gray-100">
								<div class="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
									<Award class="size-4" />
									{{ __('Plan') }}
								</div>
								<div class="mt-2 text-lg font-bold text-ink-gray-9">
									{{ formattedPrice }} <span class="text-sm font-medium text-gray-500">/ {{ __('mes') }}</span>
								</div>
							</div>
						</div>

						<div
							v-if="subscription.cancel_at_period_end"
							class="mt-6 flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 p-5 text-sm text-amber-900"
						>
							<XCircle class="mt-0.5 size-5 shrink-0 text-amber-600" />
							<div>
								<div class="font-bold">
									{{ __('Cancelación programada') }}
								</div>
								<div class="mt-1">
									{{
										__('Tu suscripción se cancelará automáticamente, pero mantienes los beneficios Plus hasta el {0}.', [
											formatDate(subscription.cancel_scheduled_for),
										])
									}}
								</div>
							</div>
						</div>

						<div class="mt-8 flex flex-wrap gap-3">
							<Button
								v-if="billing.data.active && !subscription.cancel_at_period_end"
								variant="outline"
								class="hover:bg-gray-50"
								@click="showPaymentMethodForm"
							>
								<template #prefix>
									<CreditCard class="size-4 stroke-1.5" />
								</template>
								{{ __('Actualizar tarjeta') }}
							</Button>
							<Button
								v-if="billing.data.active && !subscription.cancel_at_period_end"
								variant="ghost"
								class="text-red-600 hover:bg-red-50"
								:loading="cancelResource.loading"
								@click="requestCancellation"
							>
								{{ __('Cancelar suscripción') }}
							</Button>
							<Button
								v-if="billing.data.active && subscription.cancel_at_period_end"
								variant="solid"
								theme="blue"
								class="w-full sm:w-auto shadow-sm"
								:loading="reactivateResource.loading"
								@click="reactivateSubscription"
							>
								<template #prefix>
									<RefreshCcw class="size-4 stroke-1.5" />
								</template>
								{{ __('Reactivar mi Plus') }}
							</Button>
						</div>

						<div v-if="cardFormVisible" class="mt-8 overflow-hidden rounded-xl border border-gray-200 shadow-sm">
							<div class="bg-gray-50 px-6 py-4 flex items-center justify-between border-b border-gray-200">
								<div>
									<div class="font-bold text-ink-gray-9 flex items-center gap-2">
										<ShieldCheck class="size-5 text-green-600" />
										{{ __('Actualizar método de pago') }}
									</div>
									<div class="mt-1 text-xs text-ink-gray-6">
										{{ __('Procesado de forma segura por Mercado Pago') }}
									</div>
								</div>
								<Button variant="ghost" class="shrink-0" @click="hidePaymentMethodForm">
									{{ __('Cerrar') }}
								</Button>
							</div>
							<div class="p-6">
								<div
									v-if="cardFormLoading"
									class="flex justify-center py-8 text-sm text-ink-gray-6 animate-pulse"
								>
									{{ __('Estableciendo conexión segura...') }}
								</div>
								<div id="studybadge-mp-card-form"></div>
							</div>
						</div>
					</div>

					<!-- Recibos -->
					<div class="rounded-xl border border-gray-200 bg-surface-white p-6 sm:p-8 shadow-sm">
						<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-100 pb-5">
							<div>
								<h2 class="text-xl font-bold text-ink-gray-9 flex items-center gap-2">
									<Download class="size-5 text-gray-500" />
									{{ __('Historial de Recibos') }}
								</h2>
								<p class="mt-1 text-sm text-ink-gray-6">
									{{ __('Descarga tus comprobantes de pago en PDF.') }}
								</p>
							</div>
							<Button
								variant="outline"
								class="w-fit"
								:loading="billing.loading"
								@click="billing.reload()"
							>
								<template #prefix>
									<RefreshCcw class="size-4 stroke-1.5" />
								</template>
								{{ __('Actualizar') }}
							</Button>
						</div>

						<div v-if="receipts.length" class="mt-6 divide-y divide-gray-100 rounded-lg border border-gray-100 bg-gray-50/50">
							<div
								v-for="receipt in receipts"
								:key="receipt.name"
								class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 hover:bg-gray-50 transition-colors"
							>
								<div>
									<div class="font-bold text-ink-gray-9">
										{{ receipt.receipt_number || receipt.name }}
									</div>
									<div class="mt-1 flex items-center gap-2 text-sm text-ink-gray-6">
										<CalendarDays class="size-3.5" />
										{{ formatDate(receipt.paid_at || receipt.date_created) }}
										<span v-if="receipt.status" class="inline-flex items-center rounded-full bg-gray-200 px-2 py-0.5 text-xs font-medium text-gray-800">
											{{ receipt.status }}
										</span>
									</div>
								</div>
								<div class="flex items-center justify-between sm:justify-end gap-4 w-full sm:w-auto">
									<div class="text-base font-bold text-ink-gray-9">
										{{ formatMoney(receipt.amount, receipt.currency) }}
									</div>
									<Button variant="outline" class="shrink-0 bg-white" @click="downloadReceipt(receipt)">
										<template #prefix>
											<Download class="size-4 stroke-1.5" />
										</template>
										{{ __('PDF') }}
									</Button>
								</div>
							</div>
						</div>
						<div
							v-else
							class="mt-6 flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-gray-50 py-12 text-center"
						>
							<div class="rounded-full bg-gray-100 p-3 mb-3">
								<Download class="size-6 text-gray-400" />
							</div>
							<div class="text-sm font-medium text-ink-gray-9">
								{{ __('Aún no hay recibos') }}
							</div>
							<div class="text-sm text-ink-gray-5 mt-1">
								{{ __('Aquí aparecerán tus comprobantes cuando realices pagos.') }}
							</div>
						</div>
					</div>

					<!-- Soporte / Reembolsos -->
					<div class="rounded-xl border border-blue-100 bg-blue-50/50 p-6 sm:p-8">
						<div class="flex flex-col sm:flex-row items-start sm:items-center gap-5">
							<div class="rounded-full bg-blue-100 p-4 shrink-0">
								<LifeBuoy class="size-8 stroke-1.5 text-blue-600" />
							</div>
							<div>
								<h2 class="text-xl font-bold text-ink-gray-9">
									{{ __('¿Necesitas ayuda? Estamos para ti') }}
								</h2>
								<p class="mt-2 text-sm leading-relaxed text-ink-gray-7 max-w-2xl">
									{{
										__(
											'Ya sea un problema técnico, una consulta sobre tu suscripción o una solicitud de reembolso, nuestro equipo de soporte prioritario resolverá tus dudas rápidamente.'
										)
									}}
								</p>
								<a
									class="mt-4 inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2 text-sm font-bold text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 transition-colors"
									:href="`mailto:${billing.data?.support_email || 'soporte@studybadge.com'}`"
								>
									<Mail class="size-4" />
									{{ __('Contactar Soporte') }}
								</a>
							</div>
						</div>
					</div>
				</section>

				<!-- Aside CTA -->
				<aside class="sticky top-24 h-fit rounded-2xl border border-gray-200 bg-surface-white p-6 sm:p-8 shadow-xl shadow-gray-200/40">
					<!-- Mercado Pago Badge -->
					<div class="mb-6 flex justify-center">
						<div class="flex items-center gap-2 rounded-full bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-700 border border-blue-100">
							<ShieldCheck class="size-4" />
							{{ __('Pagos 100% seguros con Mercado Pago') }}
						</div>
					</div>

					<div class="text-center mb-6">
						<div class="text-sm font-bold uppercase tracking-wider text-amber-500 mb-2">
							{{ __('Membresía Plus') }}
						</div>
						<div class="flex items-end justify-center gap-1">
							<div class="text-5xl font-black text-ink-gray-9 tracking-tight">
								{{ formattedPrice }}
							</div>
							<div class="pb-2 text-base font-medium text-gray-500">
								/ {{ __('mes') }}
							</div>
						</div>
					</div>

					<div
						v-if="subscription?.status"
						class="mb-6 rounded-xl bg-gray-50 p-4 text-center border border-gray-100 shadow-inner"
					>
						<div class="text-xs uppercase tracking-wider text-gray-500 font-semibold mb-1">{{ __('Estado Actual') }}</div>
						<div class="font-bold text-lg text-ink-gray-9 flex items-center justify-center gap-2">
							<span class="relative flex h-3 w-3" v-if="subscription.status === 'authorized'">
								<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
								<span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
							</span>
							{{ formatSubscriptionStatus(subscription.status) }}
						</div>
					</div>

					<Button
						class="w-full py-6 text-lg font-bold shadow-md transition-transform hover:-translate-y-0.5"
						:variant="billing.data?.active ? 'outline' : 'solid'"
						theme="blue"
						size="lg"
						:loading="activating"
						:disabled="billing.data?.active"
						@click="activatePlus"
					>
						<template #prefix>
							<CreditCard class="size-5 mr-1" />
						</template>
						{{
							billing.data?.active
								? __('Tu plan ya está activo')
								: __('Suscribirme ahora')
						}}
					</Button>

					<Button
						v-if="subscription?.init_point && !billing.data?.active"
						class="mt-3 w-full py-5 font-bold"
						variant="outline"
						@click="openExistingCheckout"
					>
						{{ __('Continuar pago pendiente') }}
					</Button>

					<div class="mt-6 flex items-start gap-3 rounded-lg bg-amber-50 p-3 text-xs leading-relaxed text-amber-900 border border-amber-100">
						<Info class="size-4 shrink-0 mt-0.5 text-amber-600" />
						<p>
							{{
								__(
									'Cancela cuando quieras. Sin compromisos a largo plazo. Todos tus pagos son encriptados y procesados mediante la tecnología segura de Mercado Pago.'
								)
							}}
						</p>
					</div>
				</aside>
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
	if (status === 'authorized' || status === 'active') return __('Activa 🌟')
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

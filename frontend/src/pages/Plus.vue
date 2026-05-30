<template>
	<div>
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<Badge v-if="billing.data?.active" theme="green">
				{{ __('Plus activo') }}
			</Badge>
		</header>

		<div class="mx-auto max-w-6xl px-5 py-8">
			<div class="grid gap-8 lg:grid-cols-[1fr_360px]">
				<section class="space-y-6">
					<div class="flex items-center gap-3">
						<div class="rounded-lg bg-surface-amber-2 p-2 text-ink-amber-3">
							<Crown class="size-6 stroke-1.5" />
						</div>
						<div>
							<h1 class="text-3xl font-semibold text-ink-gray-9">
								StudyBadge Plus
							</h1>
							<p class="mt-1 text-base text-ink-gray-7">
								{{ __('Facturacion, certificados e IA sin limites.') }}
							</p>
						</div>
					</div>

					<div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
						<div
							v-for="benefit in benefits"
							:key="benefit.label"
							class="flex items-start gap-3 rounded-md border bg-surface-white p-4"
						>
							<component
								:is="benefit.icon"
								class="mt-0.5 size-5 shrink-0 stroke-1.5 text-ink-blue-3"
							/>
							<div>
								<div class="font-medium text-ink-gray-9">
									{{ benefit.label }}
								</div>
								<div class="mt-1 text-sm leading-5 text-ink-gray-6">
									{{ benefit.description }}
								</div>
							</div>
						</div>
					</div>

					<div
						v-if="billing.data?.subscription"
						class="rounded-md border bg-surface-white p-5"
					>
						<div class="flex flex-wrap items-center justify-between gap-3">
							<div>
								<h2 class="text-lg font-semibold text-ink-gray-9">
									{{ __('Facturacion') }}
								</h2>
								<p class="mt-1 text-sm text-ink-gray-6">
									{{ __('Gestiona tu plan Plus y tus pagos recurrentes.') }}
								</p>
							</div>
							<Badge :theme="billing.data.active ? 'green' : 'gray'">
								{{ subscription.status }}
							</Badge>
						</div>

						<div class="mt-5 grid gap-3 sm:grid-cols-3">
							<div class="rounded-md bg-surface-gray-2 p-4">
								<div class="text-xs font-medium uppercase text-ink-gray-5">
									{{ __('Proximo cobro') }}
								</div>
								<div class="mt-2 text-sm font-semibold text-ink-gray-9">
									{{ formatDate(subscription.next_payment_date) }}
								</div>
							</div>
							<div class="rounded-md bg-surface-gray-2 p-4">
								<div class="text-xs font-medium uppercase text-ink-gray-5">
									{{ __('Metodo de pago') }}
								</div>
								<div class="mt-2 text-sm font-semibold text-ink-gray-9">
									{{ paymentMethodLabel }}
								</div>
							</div>
							<div class="rounded-md bg-surface-gray-2 p-4">
								<div class="text-xs font-medium uppercase text-ink-gray-5">
									{{ __('Plan') }}
								</div>
								<div class="mt-2 text-sm font-semibold text-ink-gray-9">
									{{ formattedPrice }} / {{ __('mes') }}
								</div>
							</div>
						</div>

						<div
							v-if="subscription.cancel_at_period_end"
							class="mt-5 rounded-md border border-outline-amber-2 bg-surface-amber-1 p-4 text-sm text-ink-gray-8"
						>
							<div class="font-medium">
								{{ __('Tu plan se cancelara al final del periodo.') }}
							</div>
							<div class="mt-1">
								{{
									__('Mantienes Plus hasta {0}.', [
										formatDate(subscription.cancel_scheduled_for),
									])
								}}
							</div>
						</div>

						<div class="mt-5 flex flex-wrap gap-3">
							<Button
								v-if="billing.data.active && !subscription.cancel_at_period_end"
								variant="outline"
								@click="showPaymentMethodForm"
							>
								<template #prefix>
									<CreditCard class="size-4 stroke-1.5" />
								</template>
								{{ __('Cambiar metodo de pago') }}
							</Button>
							<Button
								v-if="billing.data.active && !subscription.cancel_at_period_end"
								variant="outline"
								:loading="cancelResource.loading"
								@click="requestCancellation"
							>
								<template #prefix>
									<XCircle class="size-4 stroke-1.5" />
								</template>
								{{ __('Cancelar al final del periodo') }}
							</Button>
							<Button
								v-if="billing.data.active && subscription.cancel_at_period_end"
								variant="solid"
								:loading="reactivateResource.loading"
								@click="reactivateSubscription"
							>
								<template #prefix>
									<RefreshCcw class="size-4 stroke-1.5" />
								</template>
								{{ __('Mantener Plus') }}
							</Button>
						</div>

						<div v-if="cardFormVisible" class="mt-5 rounded-md border p-4">
							<div class="mb-4 flex items-center justify-between gap-3">
								<div>
									<div class="font-medium text-ink-gray-9">
										{{ __('Nuevo metodo de pago') }}
									</div>
									<div class="mt-1 text-sm text-ink-gray-6">
										{{ __('Tus datos de tarjeta los procesa Mercado Pago.') }}
									</div>
								</div>
								<Button variant="ghost" @click="hidePaymentMethodForm">
									{{ __('Cerrar') }}
								</Button>
							</div>
							<div
								v-if="cardFormLoading"
								class="rounded-md bg-surface-gray-2 p-4 text-sm text-ink-gray-6"
							>
								{{ __('Cargando formulario seguro...') }}
							</div>
							<div id="studybadge-mp-card-form"></div>
						</div>
					</div>

					<div class="rounded-md border bg-surface-white p-5">
						<div class="flex items-center justify-between gap-3">
							<div>
								<h2 class="text-lg font-semibold text-ink-gray-9">
									{{ __('Recibos') }}
								</h2>
								<p class="mt-1 text-sm text-ink-gray-6">
									{{ __('Descarga tus recibos StudyBadge Plus en PDF.') }}
								</p>
							</div>
							<Button
								variant="outline"
								:loading="billing.loading"
								@click="billing.reload()"
							>
								<template #prefix>
									<RefreshCcw class="size-4 stroke-1.5" />
								</template>
								{{ __('Actualizar') }}
							</Button>
						</div>

						<div v-if="receipts.length" class="mt-5 divide-y rounded-md border">
							<div
								v-for="receipt in receipts"
								:key="receipt.name"
								class="flex flex-wrap items-center justify-between gap-3 p-4"
							>
								<div>
									<div class="font-medium text-ink-gray-9">
										{{ receipt.receipt_number || receipt.name }}
									</div>
									<div class="mt-1 text-sm text-ink-gray-6">
										{{ formatDate(receipt.paid_at || receipt.date_created) }}
										<span v-if="receipt.status"> - {{ receipt.status }}</span>
									</div>
								</div>
								<div class="flex items-center gap-3">
									<div class="text-sm font-semibold text-ink-gray-9">
										{{ formatMoney(receipt.amount, receipt.currency) }}
									</div>
									<Button variant="outline" @click="downloadReceipt(receipt)">
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
							class="mt-5 rounded-md bg-surface-gray-2 p-4 text-sm text-ink-gray-6"
						>
							{{ __('Aun no hay recibos disponibles para tu suscripcion.') }}
						</div>
					</div>

					<div class="rounded-md border bg-surface-white p-5">
						<div class="flex items-start gap-3">
							<LifeBuoy class="mt-0.5 size-5 shrink-0 stroke-1.5 text-ink-blue-3" />
							<div>
								<h2 class="text-lg font-semibold text-ink-gray-9">
									{{ __('Reembolsos') }}
								</h2>
								<p class="mt-1 text-sm leading-6 text-ink-gray-6">
									{{
										__(
											'Para solicitar un reembolso, contacta a soporte y revisaremos tu caso.'
										)
									}}
								</p>
								<a
									class="mt-3 inline-flex text-sm font-medium text-ink-blue-3 hover:underline"
									:href="`mailto:${billing.data?.support_email || 'soporte@studybadge.com'}`"
								>
									{{ billing.data?.support_email || 'soporte@studybadge.com' }}
								</a>
							</div>
						</div>
					</div>
				</section>

				<aside class="h-fit rounded-md border bg-surface-white p-5 shadow-sm">
					<div class="text-sm font-medium uppercase text-ink-gray-5">
						{{ __('Plan Plus') }}
					</div>
					<div class="mt-3 flex items-end gap-1">
						<div class="text-4xl font-semibold text-ink-gray-9">
							{{ formattedPrice }}
						</div>
						<div class="pb-1 text-sm text-ink-gray-6">
							{{ __('mensual') }}
						</div>
					</div>

					<div
						v-if="subscription?.status"
						class="mt-4 rounded-md bg-surface-gray-2 p-3 text-sm text-ink-gray-7"
					>
						{{ __('Estado') }}:
						<span class="font-medium text-ink-gray-9">
							{{ subscription.status }}
						</span>
					</div>

					<Button
						class="mt-5 w-full"
						variant="solid"
						size="md"
						:loading="activating"
						:disabled="billing.data?.active"
						@click="activatePlus"
					>
						<template #prefix>
							<CreditCard class="size-4 stroke-1.5" />
						</template>
						{{
							billing.data?.active
								? __('Plus activo')
								: __('Activar Plus con Mercado Pago')
						}}
					</Button>

					<Button
						v-if="subscription?.init_point && !billing.data?.active"
						class="mt-3 w-full"
						variant="outline"
						@click="openExistingCheckout"
					>
						{{ __('Continuar pago pendiente') }}
					</Button>

					<p class="mt-4 text-xs leading-5 text-ink-gray-5">
						{{
							__(
								'El cobro recurrente se procesa con Mercado Pago. La gestion queda disponible aqui cuando tu Plus este activo.'
							)
						}}
					</p>
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

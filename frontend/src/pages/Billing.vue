<template>
	<div class="">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs
				class="h-7"
				:items="[{ label: pageTitle, route: { name: 'Billing' } }]"
			/>
		</header>
		<div
			v-if="isCertificateCheckout && access.data?.access && orderSummary.data"
			class="certificate-checkout min-h-[calc(100vh-49px)] pb-12"
		>
			<section class="certificate-band">
				<div class="mx-auto grid max-w-6xl gap-6 px-5 py-8 lg:grid-cols-[1.15fr_0.85fr] lg:py-10">
					<div class="certificate-hero-panel">
						<div class="mb-4 inline-flex items-center gap-2 rounded-md border border-white/20 bg-white/10 px-3 py-1 text-xs font-semibold text-white">
							<BadgeCheck class="size-4" />
							{{ __('Certificacion StudyBadge') }}
						</div>
						<h1 class="max-w-2xl text-3xl font-bold leading-tight text-white sm:text-4xl">
							{{ __('Paga este certificado una vez') }}
						</h1>
						<p class="mt-3 max-w-2xl text-sm leading-6 text-blue-100 sm:text-base">
							{{ __('Completa el pago seguro en soles y agenda tu evaluacion para obtener una credencial verificable de este curso.') }}
						</p>
						<div class="mt-5 grid gap-3 text-sm text-white sm:grid-cols-3">
							<div class="certificate-proof">
								<ShieldCheck class="size-4" />
								{{ __('Pago seguro') }}
							</div>
							<div class="certificate-proof">
								<CreditCard class="size-4" />
								{{ __('Tarjetas, Yape y mas') }}
							</div>
							<div class="certificate-proof">
								<Award class="size-4" />
								{{ __('Certificado premium') }}
							</div>
						</div>
					</div>

					<aside class="certificate-summary">
						<div class="text-xs font-semibold uppercase tracking-wide text-ink-gray-5">
							{{ __('Certificado para') }}
						</div>
						<div class="mt-1 text-lg font-bold text-ink-gray-9">
							{{ orderSummary.data.title }}
						</div>
						<div class="mt-5 flex items-end justify-between border-t pt-5">
							<div>
								<div class="text-xs font-semibold uppercase tracking-wide text-ink-gray-5">
									{{ __('Total') }}
								</div>
								<div class="text-xs text-ink-gray-5">
									{{ __('Pago unico en PEN') }}
								</div>
							</div>
							<div class="text-3xl font-black text-[#0a2351]">
								{{ formatCertificateMoney(orderSummary.data.total_amount) }}
							</div>
						</div>
						<router-link
							:to="{ name: 'Plus', query: { from: 'certificate', course: name } }"
							class="mt-5 flex items-start gap-3 rounded-md border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900 hover:bg-amber-100"
						>
							<Crown class="mt-0.5 size-4 shrink-0" />
							<span>
								<strong>{{ __('Con StudyBadge Plus tienes certificados ilimitados.') }}</strong>
								{{ __(' Ideal si planeas certificarte en varios cursos.') }}
							</span>
						</router-link>
					</aside>
				</div>
			</section>

			<div class="mx-auto grid max-w-6xl gap-6 px-5 py-8 lg:grid-cols-[0.9fr_1.1fr]">
				<section class="certificate-card p-5">
					<div class="mb-5">
						<h2 class="text-lg font-semibold text-ink-gray-9">
							{{ __('Datos de facturacion') }}
						</h2>
						<p class="mt-1 text-sm text-ink-gray-6">
							{{ __('Usaremos estos datos para registrar tu compra del certificado.') }}
						</p>
					</div>
					<div class="space-y-4">
						<FormControl
							label="Nombre completo"
							v-model="billingDetails.billing_name"
							:required="!!fieldMeta.billing_name?.reqd"
						/>
						<FormControl
							:label="__('Address Line 1')"
							v-model="billingDetails.address_line1"
							:required="!!fieldMeta.address_line1?.reqd"
						/>
						<FormControl
							:label="__('Address Line 2')"
							v-model="billingDetails.address_line2"
							:required="!!fieldMeta.address_line2?.reqd"
						/>
						<div class="grid gap-4 sm:grid-cols-2">
							<FormControl
								:label="__('City')"
								v-model="billingDetails.city"
								:required="!!fieldMeta.city?.reqd"
							/>
							<FormControl
								:label="__('State/Province')"
								v-model="billingDetails.state"
								:required="!!fieldMeta.state?.reqd"
							/>
						</div>
						<div class="grid gap-4 sm:grid-cols-2">
							<FormControl
								:label="__('Postal Code')"
								v-model="billingDetails.pincode"
								:required="!!fieldMeta.pincode?.reqd"
							/>
							<FormControl
								:label="__('Phone Number')"
								v-model="billingDetails.phone"
								:required="!!fieldMeta.phone?.reqd"
							/>
						</div>
						<Link
							doctype="Country"
							:value="billingDetails.country"
							@change="(option) => changeCurrency(option)"
							:label="__('Country')"
							:required="!!fieldMeta.country?.reqd"
						/>
						<Link
							doctype="LMS Source"
							:value="billingDetails.source"
							@change="(option) => (billingDetails.source = option)"
							:label="__('Where did you hear about us?')"
							:required="!!fieldMeta.source?.reqd"
						/>
						<FormControl
							label="Autorizo el uso de mis datos para registrar esta compra"
							type="checkbox"
							class="leading-6"
							v-model="billingDetails.member_consent"
						/>
						<div v-if="showConsentWarning" class="text-xs text-ink-red-3">
							{{ __('Please provide your consent to proceed with the payment') }}
						</div>
						<Button
							variant="solid"
							size="md"
							class="certificate-primary w-full"
							:disabled="certificateCheckout.loading || brickLoading"
							@click="prepareCertificateCheckout"
						>
							<template #prefix>
								<CreditCard class="size-4" />
							</template>
							{{ certificateCheckout.data ? __('Reiniciar pago seguro') : __('Continuar al pago seguro') }}
						</Button>
					</div>
				</section>

				<section class="certificate-card min-h-[420px] p-5">
					<div class="mb-5 flex items-start justify-between gap-4">
						<div>
							<h2 class="text-lg font-semibold text-ink-gray-9">
								{{ __('Mercado Pago Checkout') }}
							</h2>
							<p class="mt-1 text-sm text-ink-gray-6">
								{{ __('Elige tarjeta, saldo de Mercado Pago, Yape u otros metodos disponibles para Peru.') }}
							</p>
						</div>
						<div class="rounded-md bg-blue-50 px-3 py-1 text-xs font-semibold text-[#0a2351]">
							{{ __('PEN') }}
						</div>
					</div>
					<div class="mb-4 rounded-md border border-blue-100 bg-blue-50 p-3 text-sm text-[#0a2351]">
						<div class="font-semibold">
							{{ __('Si quieres pagar con Yape') }}
						</div>
						<div class="mt-1 leading-5">
							{{ __('En Medios de pago, elige Mercado Pago Wallet. Ahi apareceran tus medios favoritos, incluido Yape si esta disponible para tu cuenta.') }}
						</div>
					</div>
					<div
						v-if="!certificateCheckout.data"
						class="certificate-empty"
					>
						<ShieldCheck class="size-8 text-[#0a2351]" />
						<div class="mt-3 font-semibold text-ink-gray-9">
							{{ __('Confirma tus datos para cargar la pasarela') }}
						</div>
						<p class="mt-1 max-w-sm text-center text-sm text-ink-gray-6">
							{{ __('Mercado Pago se abrira aqui mismo, sin salir de StudyBadge.') }}
						</p>
					</div>
					<div v-else>
						<div v-if="brickLoading" class="py-8 text-center text-sm text-ink-gray-6">
							{{ __('Cargando pasarela segura...') }}
						</div>
						<div id="studybadge-mp-payment-brick"></div>
						<div
							v-if="certificatePaymentStatus"
							class="mt-4 rounded-md border p-4 text-sm"
							:class="certificatePaymentStatus === 'approved' ? 'border-green-200 bg-green-50 text-green-800' : 'border-amber-200 bg-amber-50 text-amber-800'"
						>
							<div class="font-semibold">
								{{ paymentStatusTitle }}
							</div>
							<div class="mt-1">
								{{ paymentStatusMessage }}
							</div>
							<Button
								v-if="certificatePaymentStatus !== 'approved'"
								variant="outline"
								size="sm"
								class="mt-3"
								:disabled="paymentStatus.loading"
								@click="refreshCertificatePayment"
							>
								<template #prefix>
									<RefreshCcw class="size-4" />
								</template>
								{{ __('Actualizar estado') }}
							</Button>
						</div>
					</div>
				</section>
			</div>
		</div>
		<div
			v-else-if="access.data?.access && orderSummary.data"
			class="pt-5 pb-10 mx-5"
		>
			<div class="flex flex-col lg:flex-row justify-between">
				<div class="flex flex-col lg:order-last mb-10 lg:mt-10 lg:w-1/4">
					<div class="h-fit bg-surface-gray-2 rounded-md p-5 space-y-4">
						<div class="space-y-1">
							<div class="text-ink-gray-5 uppercase text-xs">
								{{ __('Payment for ') }} {{ type }}:
							</div>
							<div class="leading-5 text-ink-gray-9">
								{{ orderSummary.data.title }}
							</div>
						</div>
						<div
							v-if="
								orderSummary.data.gst_applied ||
								orderSummary.data.discount_amount
							"
							class="space-y-1"
						>
							<div class="text-ink-gray-5 uppercase text-xs">
								{{ __('Original Amount') }}:
							</div>
							<div class="text-ink-gray-9">
								{{ orderSummary.data.original_amount_formatted }}
							</div>
						</div>
						<div v-if="orderSummary.data.discount_amount" class="space-y-1">
							<div class="text-ink-gray-5">{{ __('Discount') }}:</div>
							<div>- {{ orderSummary.data.discount_amount_formatted }}</div>
						</div>
						<div v-if="orderSummary.data.gst_applied" class="space-y-1">
							<div class="text-ink-gray-5 uppercase text-xs">
								{{ __('GST Amount') }}:
							</div>
							<div class="text-ink-gray-9">
								{{ orderSummary.data.gst_amount_formatted }}
							</div>
						</div>
						<div class="space-y-1 border-t border-outline-gray-3 pt-4 mt-2">
							<div class="uppercase text-ink-gray-5 text-xs">
								{{ __('Total') }}:
							</div>
							<div class="font-bold text-ink-gray-9">
								{{ orderSummary.data.total_amount_formatted }}
							</div>
						</div>
					</div>

					<div class="bg-surface-gray-2 rounded-md p-4 space-y-2 my-5">
						<span class="text-ink-gray-5 uppercase text-xs">
							{{ __('Enter a Coupon Code') }}:
						</span>
						<div class="flex items-center gap-x-2">
							<FormControl
								v-model="appliedCoupon"
								:disabled="orderSummary.data.discount_amount > 0"
								@input="appliedCoupon = $event.target.value.toUpperCase()"
								@keydown.enter="applyCouponCode"
								placeholder="COUPON2025"
								autocomplete="off"
								class="flex-1 [&_input]:bg-white"
							/>
							<Button
								v-if="!orderSummary.data.discount_amount"
								@click="applyCouponCode"
								variant="outline"
							>
								{{ __('Apply') }}
							</Button>
							<Button
								v-if="orderSummary.data.discount_amount"
								@click="removeCoupon"
								variant="outline"
							>
								<template #icon>
									<X class="size-4 stroke-1.5" />
								</template>
							</Button>
						</div>
					</div>

					<p
						class="bg-surface-amber-2 text-ink-amber-2 text-sm leading-5 p-2 rounded-md"
					>
						{{
							__(
								'Please ensure that the billing name you enter is correct, as it will be used on your invoice.'
							)
						}}
					</p>
				</div>

				<div class="flex-1 lg:me-10">
					<div class="mb-5">
						<div class="text-lg font-semibold text-ink-gray-9">
							{{ __('Address') }}
						</div>
					</div>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
						<div class="space-y-4">
							<FormControl
								:label="__('Billing Name')"
								v-model="billingDetails.billing_name"
								:required="!!fieldMeta.billing_name?.reqd"
							/>
							<FormControl
								:label="__('Address Line 1')"
								v-model="billingDetails.address_line1"
								:required="!!fieldMeta.address_line1?.reqd"
							/>
							<FormControl
								:label="__('Address Line 2')"
								v-model="billingDetails.address_line2"
								:required="!!fieldMeta.address_line2?.reqd"
							/>
							<FormControl
								:label="__('City')"
								v-model="billingDetails.city"
								:required="!!fieldMeta.city?.reqd"
							/>
							<FormControl
								:label="__('State/Province')"
								v-model="billingDetails.state"
								:required="!!fieldMeta.state?.reqd"
							/>
						</div>
						<div class="space-y-4">
							<Link
								doctype="Country"
								:value="billingDetails.country"
								@change="(option) => changeCurrency(option)"
								:label="__('Country')"
								:required="!!fieldMeta.country?.reqd"
							/>
							<FormControl
								:label="__('Postal Code')"
								v-model="billingDetails.pincode"
								:required="!!fieldMeta.pincode?.reqd"
							/>
							<FormControl
								:label="__('Phone Number')"
								v-model="billingDetails.phone"
								:required="!!fieldMeta.phone?.reqd"
							/>
							<Link
								doctype="LMS Source"
								:value="billingDetails.source"
								@change="(option) => (billingDetails.source = option)"
								:label="__('Where did you hear about us?')"
								:required="!!fieldMeta.source?.reqd"
							/>
							<FormControl
								v-if="billingDetails.country == 'India'"
								:label="__('GST Number')"
								v-model="billingDetails.gstin"
								:required="!!fieldMeta.gstin?.reqd"
							/>
							<FormControl
								v-if="billingDetails.country == 'India'"
								:label="__('PAN Number')"
								v-model="billingDetails.pan"
								:required="!!fieldMeta.pan?.reqd"
							/>
						</div>
					</div>
					<div
						class="flex flex-col lg:flex-row items-start lg:items-center justify-between border-t pt-4 mt-8 space-y-4 lg:space-y-0"
					>
						<div>
							<FormControl
								:label="
									__(
										'I consent to my personal information being stored for invoicing'
									)
								"
								type="checkbox"
								class="leading-6"
								v-model="billingDetails.member_consent"
							/>
							<div
								v-if="showConsentWarning"
								class="mt-1 text-xs text-ink-red-3"
							>
								{{
									__('Please provide your consent to proceed with the payment')
								}}
							</div>
						</div>
						<Button
							variant="solid"
							size="md"
							class="ms-auto"
							@click="generatePaymentLink()"
						>
							{{
								isZeroAmount ? __('Enroll for Free') : __('Proceed to Payment')
							}}
						</Button>
					</div>
				</div>
			</div>
		</div>
		<div v-else-if="access.data?.message">
			<NotPermitted
				:text="access.data.message"
				:buttonLabel="
					type == 'course'
						? 'Checkout Course'
						: type == 'certificate'
							? 'Volver al curso'
							: 'Checkout Batch'
				"
				:buttonLink="
					type == 'course' || type == 'certificate'
						? getLmsRoute(`courses/${name}`)
						: getLmsRoute(`batches/${name}`)
				"
			/>
		</div>
		<div v-else-if="!user.data?.name">
			<NotPermitted
				text="Please login to access this page."
				:buttonLink="`/login?redirect-to=${getLmsRoute(
					`billing/${type}/${name}`
				)}`"
			/>
		</div>
	</div>
</template>
<script setup>
import {
	Button,
	createResource,
	FormControl,
	Breadcrumbs,
	usePageMeta,
	toast,
	call,
} from 'frappe-ui'
import {
	reactive,
	inject,
	onMounted,
	computed,
	ref,
	watch,
	nextTick,
	onBeforeUnmount,
} from 'vue'
import { sessionStore } from '../stores/session'
import Link from '@/components/Controls/Link.vue'
import NotPermitted from '@/components/NotPermitted.vue'
import {
	Award,
	BadgeCheck,
	CreditCard,
	Crown,
	RefreshCcw,
	ShieldCheck,
	X,
} from 'lucide-vue-next'
import { useTelemetry } from 'frappe-ui/frappe'
import { getLmsRoute } from '@/utils/basePath'

const user = inject('$user')
const { brand } = sessionStore()
const showConsentWarning = ref(false)
const mercadoPagoLoader = ref(null)
const paymentBrickController = ref(null)
const brickLoading = ref(false)
const certificatePaymentStatus = ref('')
const certificatePaymentMessage = ref('')
const { capture } = useTelemetry()

onMounted(() => {
	if (!isCertificateCheckout.value) {
		const script = document.createElement('script')
		script.src = `https://checkout.razorpay.com/v1/checkout.js`
		document.body.appendChild(script)
	}
	if (user.data?.name) {
		access.submit()
	}
})

const props = defineProps({
	type: {
		type: String,
		required: true,
	},
	name: {
		type: String,
		required: true,
	},
})

const isCertificateCheckout = computed(() => props.type == 'certificate')

const pageTitle = computed(() =>
	isCertificateCheckout.value ? __('Pagar certificado') : __('Billing Details')
)

const access = createResource({
	url: 'lms.lms.api.validate_billing_access',
	params: {
		billing_type: props.type,
		name: props.name,
	},
	onSuccess(data) {
		Object.assign(fieldMeta, data.billing_field_meta || {})
		setBillingDetails(data.address)
		orderSummary.submit()
	},
})

const orderSummary = createResource({
	url: 'lms.lms.utils.get_order_summary',
	makeParams(values) {
		return {
			doctype: props.type == 'batch' ? 'LMS Batch' : 'LMS Course',
			docname: props.name,
			country: billingDetails.country,
			coupon: appliedCoupon.value,
		}
	},
	onError(err) {
		showError(err)
	},
})

const appliedCoupon = ref(null)
const billingDetails = reactive({})
const fieldMeta = reactive({})

const getDefault = (fieldname) => fieldMeta[fieldname]?.default || ''

const setBillingDetails = (data) => {
	billingDetails.billing_name = data?.billing_name || getDefault('billing_name')
	billingDetails.address_line1 =
		data?.address_line1 || getDefault('address_line1')
	billingDetails.address_line2 =
		data?.address_line2 || getDefault('address_line2')
	billingDetails.city = data?.city || getDefault('city')
	billingDetails.state = data?.state || getDefault('state')
	billingDetails.country = data?.country || getDefault('country')
	billingDetails.pincode = data?.pincode || getDefault('pincode')
	billingDetails.phone = data?.phone || getDefault('phone')
	billingDetails.source = data?.source || getDefault('source')
	billingDetails.gstin = data?.gstin || getDefault('gstin')
	billingDetails.pan = data?.pan || getDefault('pan')
}

const paymentLink = createResource({
	url: 'lms.lms.payments.get_payment_link',
	makeParams(values) {
		let data = {
			doctype: props.type == 'batch' ? 'LMS Batch' : 'LMS Course',
			docname: props.name,
			address: billingDetails,
			payment_for_certificate: props.type == 'certificate',
			coupon_code: appliedCoupon.value,
			country: billingDetails.country,
		}
		return data
	},
})

const certificateCheckout = createResource({
	url: 'lms.lms.payments.create_certificate_brick_checkout',
	makeParams() {
		return {
			course: props.name,
			address: billingDetails,
			coupon_code: appliedCoupon.value,
			country: billingDetails.country,
		}
	},
})

const certificatePayment = createResource({
	url: 'lms.lms.payments.process_certificate_brick_payment',
})

const paymentStatus = createResource({
	url: 'lms.lms.payments.get_certificate_payment_status',
})

const paymentStatusTitle = computed(() => {
	if (certificatePaymentStatus.value === 'approved') {
		return __('Pago aprobado')
	}
	if (
		certificatePaymentStatus.value === 'pending' ||
		certificatePaymentStatus.value === 'in_process'
	) {
		return __('Pago en revision')
	}
	return __('No pudimos confirmar el pago')
})

const paymentStatusMessage = computed(() => {
	if (certificatePaymentStatus.value === 'approved') {
		return __('Tu certificado ya esta desbloqueado. Te llevaremos a la pantalla de certificacion.')
	}
	if (
		certificatePaymentStatus.value === 'pending' ||
		certificatePaymentStatus.value === 'in_process'
	) {
		return __('Mercado Pago esta procesando la operacion. Puedes actualizar el estado en unos segundos.')
	}
	return certificatePaymentMessage.value || __('Revisa los datos del metodo de pago e intenta nuevamente.')
})

function formatCertificateMoney(amount) {
	return `S/ ${Number(amount || 0).toFixed(2)}`
}

const generatePaymentLink = () => {
	paymentLink.submit(
		{},
		{
			validate() {
				if (!billingDetails.source && fieldMeta.source?.reqd) {
					return __('Please let us know where you heard about us from.')
				}
				if (!billingDetails.member_consent) {
					showConsentWarning.value = true
					return __('Please provide your consent to proceed with the payment.')
				}
				return validateAddress()
			},
			onSuccess(data) {
				capture('checkout_initiated', { type: props.type })
				window.location.href = data
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const validateBillingDetails = () => {
	if (!billingDetails.source && fieldMeta.source?.reqd) {
		return __('Please let us know where you heard about us from.')
	}
	if (!billingDetails.member_consent) {
		showConsentWarning.value = true
		return __('Please provide your consent to proceed with the payment.')
	}
	return validateAddress()
}

const prepareCertificateCheckout = () => {
	const validationError = validateBillingDetails()
	if (validationError) {
		toast.error(validationError)
		return
	}
	destroyPaymentBrick()
	certificatePaymentStatus.value = ''
	certificatePaymentMessage.value = ''
	certificateCheckout.submit(
		{},
		{
			onSuccess(data) {
				capture('checkout_initiated', { type: 'certificate' })
				if (data.status === 'approved') {
					window.location.href = data.redirect_url
					return
				}
				nextTick(() => initMercadoPagoPaymentBrick())
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
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

async function initMercadoPagoPaymentBrick() {
	if (!certificateCheckout.data?.public_key || !certificateCheckout.data?.preference_id) {
		toast.error(__('Mercado Pago no devolvio los datos del checkout.'))
		return
	}
	brickLoading.value = true
	try {
		const MercadoPago = await loadMercadoPago()
		const mp = new MercadoPago(certificateCheckout.data.public_key, {
			locale: 'es-PE',
		})
		const bricksBuilder = mp.bricks()
		paymentBrickController.value = await bricksBuilder.create(
			'payment',
			'studybadge-mp-payment-brick',
			{
				initialization: {
					amount: Number(certificateCheckout.data.amount),
					preferenceId: certificateCheckout.data.preference_id,
				},
				customization: {
					visual: {
						style: {
							theme: 'default',
							customVariables: {
								baseColor: '#0a2351',
								borderRadiusMedium: '8px',
							},
						},
					},
					paymentMethods: {
						creditCard: 'all',
						debitCard: 'all',
						prepaidCard: 'all',
						mercadoPago: 'all',
						ticket: 'all',
						bankTransfer: 'all',
						maxInstallments: 1,
					},
				},
				callbacks: {
					onReady() {
						brickLoading.value = false
					},
					onError(error) {
						brickLoading.value = false
						toast.error(error?.message || __('Mercado Pago no pudo cargar.'))
					},
					onSubmit({ formData }) {
						return new Promise((resolve, reject) => {
							certificatePayment.submit(
								{
									payment: certificateCheckout.data.payment,
									form_data: formData,
								},
								{
									onSuccess(data) {
										handleCertificatePaymentResult(data)
										resolve()
									},
									onError(err) {
										const message = err.messages?.[0] || err
										certificatePaymentStatus.value = 'rejected'
										certificatePaymentMessage.value = message
										toast.error(message)
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
		brickLoading.value = false
		toast.error(error?.message || __('No se pudo cargar Mercado Pago.'))
	}
}

function handleCertificatePaymentResult(data) {
	certificatePaymentStatus.value = data.status
	certificatePaymentMessage.value = data.status_detail || ''
	if (data.status === 'approved') {
		toast.success(__('Pago aprobado. Certificado desbloqueado.'))
		setTimeout(() => {
			window.location.href = data.redirect_url
		}, 900)
		return
	}
	if (data.status === 'pending' || data.status === 'in_process') {
		toast.success(__('Pago recibido por Mercado Pago. Esperando confirmacion.'))
		return
	}
	toast.error(__('Mercado Pago no aprobo la operacion.'))
}

function refreshCertificatePayment() {
	if (!certificateCheckout.data?.payment) return
	paymentStatus.submit(
		{ payment: certificateCheckout.data.payment },
		{
			onSuccess(data) {
				handleCertificatePaymentResult(data)
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

function destroyPaymentBrick() {
	if (paymentBrickController.value?.unmount) {
		paymentBrickController.value.unmount()
	}
	paymentBrickController.value = null
}

function applyCouponCode() {
	if (!appliedCoupon.value) {
		toast.error(__('Please enter a coupon code'))
		return
	}
	orderSummary.reload()
}

function removeCoupon() {
	appliedCoupon.value = null
	orderSummary.reload()
}

const validateAddress = () => {
	let billingFields = [
		'billing_name',
		'address_line1',
		'address_line2',
		'city',
		'state',
		'pincode',
		'country',
		'phone',
		'gstin',
		'pan',
	]
	let mandatoryFields = billingFields.filter((f) => fieldMeta[f]?.reqd)
	for (let field of mandatoryFields) {
		if (!billingDetails[field])
			return (
				'Please enter a valid ' +
				field
					.replaceAll('_', ' ')
					.toLowerCase()
					.replace(/\b\w/g, (s) => s.toUpperCase())
			)
	}

	if (billingDetails.gstin && !billingDetails.pan)
		return 'Please enter a valid pan number.'

	if (billingDetails.country == 'India' && !billingDetails.state)
		return 'Please enter a valid state with correct spelling and the first letter capitalized.'

	const states = [
		'Andhra Pradesh',
		'Arunachal Pradesh',
		'Assam',
		'Bihar',
		'Chhattisgarh',
		'Delhi',
		'Goa',
		'Gujarat',
		'Haryana',
		'Himachal Pradesh',
		'Jammu and Kashmir',
		'Jharkhand',
		'Karnataka',
		'Kerala',
		'Madhya Pradesh',
		'Maharashtra',
		'Manipur',
		'Meghalaya',
		'Mizoram',
		'Nagaland',
		'Odisha',
		'Punjab',
		'Rajasthan',
		'Sikkim',
		'Tamil Nadu',
		'Telangana',
		'Tripura',
		'Uttar Pradesh',
		'Uttarakhand',
		'West Bengal',
	]
	if (
		billingDetails.country == 'India' &&
		!states.includes(billingDetails.state)
	)
		return 'Please enter a valid state with correct spelling and the first letter capitalized.'
}

const showError = (err) => {
	toast.error(err.messages?.[0] || err)
}

const changeCurrency = (country) => {
	billingDetails.country = country
	orderSummary.reload()
}

const isZeroAmount = computed(() => {
	return orderSummary.data && parseFloat(orderSummary.data.total_amount) <= 0
})

watch(billingDetails, () => {
	if (billingDetails.member_consent) {
		showConsentWarning.value = false
	}
})

onBeforeUnmount(() => {
	destroyPaymentBrick()
})

usePageMeta(() => {
	return {
		title: pageTitle.value,
		icon: brand.favicon,
	}
})
</script>

<style scoped>
.certificate-checkout {
	background: #f6f8fb;
}

.certificate-band {
	background: #0a2351;
}

.certificate-hero-panel,
.certificate-summary,
.certificate-card {
	border-radius: 8px;
}

.certificate-hero-panel {
	border: 1px solid rgba(255, 255, 255, 0.12);
	background: rgba(255, 255, 255, 0.06);
	padding: 28px;
}

.certificate-proof {
	display: flex;
	align-items: center;
	gap: 8px;
	border-radius: 8px;
	background: rgba(255, 255, 255, 0.1);
	padding: 10px 12px;
	font-weight: 600;
}

.certificate-summary,
.certificate-card {
	border: 1px solid rgba(10, 35, 81, 0.08);
	background: white;
	box-shadow: 0 8px 24px rgba(10, 35, 81, 0.08);
}

.certificate-summary {
	padding: 24px;
}

.certificate-empty {
	display: flex;
	min-height: 300px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	border: 1px dashed rgba(10, 35, 81, 0.24);
	border-radius: 8px;
	background: #f8fafc;
	padding: 24px;
}

.certificate-primary {
	background: #0a2351 !important;
}

:root[data-theme='dark'] .certificate-checkout {
	background: #0f172a;
}

:root[data-theme='dark'] .certificate-summary,
:root[data-theme='dark'] .certificate-card {
	border-color: rgba(255, 255, 255, 0.08);
	background: #111827;
	box-shadow: none;
}

:root[data-theme='dark'] .certificate-empty {
	background: rgba(255, 255, 255, 0.03);
}
</style>

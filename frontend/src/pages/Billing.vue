<template>
	<div class="billing-page">
		<header class="billing-topbar">
			<Breadcrumbs
				class="billing-breadcrumbs"
				:items="[{ label: pageTitle, route: { name: 'Billing' } }]"
			/>
			<a class="support-chip" :href="`mailto:${SUPPORT_EMAIL}`">
				<Mail class="size-4" />
				<span>{{ SUPPORT_EMAIL }}</span>
			</a>
		</header>

		<div
			v-if="isCertificateCheckout && access.data?.access && orderSummary.data"
			class="certificate-checkout"
		>
			<section class="certificate-band">
				<div class="certificate-band-grid">
					<div class="certificate-hero-panel">
						<div class="certificate-eyebrow">
							<BadgeCheck class="size-4" />
							{{ __('Certificación StudyBadge') }}
						</div>
						<h1>{{ __('Desbloquea tu certificado verificable') }}</h1>
						<p>
							{{ selectedPaymentCurrency === 'PEN' ? __('Completa el pago seguro en soles, registra tus datos y continúa con tu certificación oficial de este curso.') : __('Completa el pago seguro en dólares con PayPal, registra tus datos y continúa con tu certificación oficial de este curso.') }}
						</p>
						<div class="certificate-proof-grid">
							<div class="certificate-proof">
								<LockKeyhole class="size-4" />
								<span>{{ __('Pago protegido') }}</span>
							</div>
							<div class="certificate-proof">
								<CreditCard class="size-4" />
								<span>{{ selectedPaymentCurrency === 'PEN' ? __('Tarjetas, Yape y más') : __('PayPal y tarjetas') }}</span>
							</div>
							<div class="certificate-proof">
								<Award class="size-4" />
								<span>{{ __('PDF verificable') }}</span>
							</div>
						</div>
					</div>

					<aside class="certificate-summary">
						<div class="summary-top">
							<div class="summary-icon">
								<ReceiptText class="size-5" />
							</div>
							<div>
								<div class="summary-kicker">{{ __('Certificado para') }}</div>
								<h2>{{ orderSummary.data.title }}</h2>
							</div>
						</div>

						<div class="summary-total-card">
							<div>
								<span>{{ __('Total a pagar') }}</span>
								<small>{{ __('Pago único en') }} {{ selectedPaymentCurrency }}</small>
							</div>
							<strong>{{ orderSummary.data.total_amount_formatted }}</strong>
						</div>

						<div class="currency-switch" aria-label="Selector de moneda">
							<button
								v-for="option in paymentCurrencyOptions"
								:key="option.currency"
								class="currency-option"
								:class="{ 'currency-option-active': selectedPaymentCurrency === option.currency }"
								@click="selectPaymentCurrency(option.currency)"
							>
								{{ option.label }}
							</button>
						</div>

						<router-link
							:to="{ name: 'Plus', query: { from: 'certificate', course: name } }"
							class="plus-callout"
						>
							<Crown class="size-5" />
							<span>
								<strong>{{ __('Con StudyBadge Plus tienes certificados ilimitados.') }}</strong>
								{{ __('Ideal si planeas certificarte en varios cursos.') }}
							</span>
						</router-link>
					</aside>
				</div>
			</section>

			<section class="checkout-grid">
				<div class="certificate-card billing-card">
					<div class="card-heading">
						<div class="card-icon">
							<MapPin class="size-5" />
						</div>
						<div>
							<h2>{{ __('Datos de facturación') }}</h2>
							<p>{{ __('Usaremos estos datos para registrar tu compra y emitir el comprobante correspondiente.') }}</p>
						</div>
					</div>

					<div class="form-stack">
						<FormControl
							:label="__('Nombre completo')"
							v-model="billingDetails.billing_name"
							:required="!!fieldMeta.billing_name?.reqd"
						/>
						<FormControl
							:label="__('Dirección principal')"
							v-model="billingDetails.address_line1"
							:required="!!fieldMeta.address_line1?.reqd"
						/>
						<FormControl
							:label="__('Referencia, departamento o piso')"
							v-model="billingDetails.address_line2"
							:required="!!fieldMeta.address_line2?.reqd"
						/>
						<div class="field-pair">
							<FormControl
								:label="__('Ciudad')"
								v-model="billingDetails.city"
								:required="!!fieldMeta.city?.reqd"
							/>
							<FormControl
								:label="__('Provincia o región')"
								v-model="billingDetails.state"
								:required="!!fieldMeta.state?.reqd"
							/>
						</div>
						<div class="field-pair">
							<FormControl
								:label="__('Código postal')"
								v-model="billingDetails.pincode"
								:required="!!fieldMeta.pincode?.reqd"
							/>
							<FormControl
								:label="__('Teléfono')"
								v-model="billingDetails.phone"
								:required="!!fieldMeta.phone?.reqd"
							/>
						</div>
						<Link
							doctype="Country"
							:value="billingDetails.country"
							@change="(option) => changeCurrency(option)"
							:label="__('País')"
							:required="!!fieldMeta.country?.reqd"
						/>
						<Link
							doctype="LMS Source"
							:value="billingDetails.source"
							@change="(option) => (billingDetails.source = option)"
							:label="__('¿Dónde conociste StudyBadge?')"
							:required="!!fieldMeta.source?.reqd"
						/>
						<FormControl
							:label="__('Autorizo el uso de mis datos para registrar esta compra')"
							type="checkbox"
							class="consent-control"
							v-model="billingDetails.member_consent"
						/>
						<div v-if="showConsentWarning" class="consent-warning">
							{{ __('Autoriza el uso de tus datos para continuar con el pago.') }}
						</div>

						<Button
							variant="solid"
							size="md"
							class="certificate-primary"
							:disabled="certificateCheckout.loading || brickLoading || paypalLoading"
							@click="prepareSelectedCheckout"
						>
							<template #prefix>
								<CreditCard class="size-4" />
							</template>
							{{ checkoutButtonLabel }}
						</Button>
					</div>
				</div>

				<div class="certificate-card gateway-card">
					<div class="card-heading gateway-heading">
						<div class="card-icon gateway-icon">
							<ShieldCheck class="size-5" />
						</div>
						<div>
							<h2>{{ selectedPaymentCurrency === 'PEN' ? __('Pago con Mercado Pago') : __('Pago con PayPal') }}</h2>
							<p>
								{{ selectedPaymentCurrency === 'PEN' ? __('Paga en soles con tarjeta, saldo de Mercado Pago, Yape u otros métodos disponibles para Perú.') : __('Paga en dólares con PayPal, tarjeta internacional o los métodos disponibles en tu cuenta.') }}
							</p>
						</div>
						<div class="gateway-currency">{{ selectedPaymentCurrency }}</div>
					</div>

					<div v-if="selectedPaymentCurrency === 'PEN'" class="gateway-tip">
						<CreditCard class="size-4" />
						<div>
							<strong>{{ __('¿Quieres pagar con Yape?') }}</strong>
							<p>{{ __('En medios de pago, elige Mercado Pago Wallet. Allí aparecerán tus métodos favoritos, incluido Yape si está disponible para tu cuenta.') }}</p>
						</div>
					</div>

					<div v-if="!hasCheckoutData" class="certificate-empty">
						<div class="empty-icon">
							<ShieldCheck class="size-8" />
						</div>
						<h3>{{ __('Confirma tus datos para cargar la pasarela') }}</h3>
						<p>
							{{ selectedPaymentCurrency === 'PEN' ? __('Mercado Pago se abrirá aquí mismo, sin salir de StudyBadge.') : __('PayPal se cargará aquí mismo para confirmar el pago en dólares.') }}
						</p>
					</div>
					<div v-else>
						<div v-if="brickLoading || paypalLoading" class="gateway-loading">
							<RefreshCcw class="size-4 animate-spin" />
							{{ __('Cargando pasarela segura...') }}
						</div>
						<div v-show="selectedPaymentCurrency === 'PEN'" id="studybadge-mp-payment-brick"></div>
						<div v-show="selectedPaymentCurrency === 'USD'" id="studybadge-paypal-buttons-certificate"></div>
						<div
							v-if="certificatePaymentStatus"
							class="payment-status"
							:class="certificatePaymentStatus === 'approved' || certificatePaymentStatus === 'COMPLETED' ? 'payment-status-success' : 'payment-status-warning'"
						>
							<div>
								<strong>{{ paymentStatusTitle }}</strong>
								<p>{{ paymentStatusMessage }}</p>
							</div>
							<Button
								v-if="certificatePaymentStatus !== 'approved' && selectedPaymentCurrency === 'PEN'"
								variant="outline"
								size="sm"
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

					<a class="support-box" :href="`mailto:${SUPPORT_EMAIL}`">
						<Mail class="size-4" />
						<span>{{ __('Si tienes problemas con el pago, escríbenos a') }} <strong>{{ SUPPORT_EMAIL }}</strong></span>
					</a>
				</div>
			</section>
		</div>

		<div
			v-else-if="access.data?.access && orderSummary.data"
			class="standard-checkout"
		>
			<div class="standard-layout">
				<aside class="standard-summary">
					<div class="summary-top">
						<div class="summary-icon">
							<ReceiptText class="size-5" />
						</div>
						<div>
							<div class="summary-kicker">{{ __('Pago de') }} {{ type }}</div>
							<h2>{{ orderSummary.data.title }}</h2>
						</div>
					</div>

					<div v-if="orderSummary.data.gst_applied || orderSummary.data.discount_amount" class="price-row">
						<span>{{ __('Importe original') }}</span>
						<strong>{{ orderSummary.data.original_amount_formatted }}</strong>
					</div>
					<div v-if="orderSummary.data.discount_amount" class="price-row discount-row">
						<span>{{ __('Descuento') }}</span>
						<strong>- {{ orderSummary.data.discount_amount_formatted }}</strong>
					</div>
					<div v-if="orderSummary.data.gst_applied" class="price-row">
						<span>{{ __('Impuesto') }}</span>
						<strong>{{ orderSummary.data.gst_amount_formatted }}</strong>
					</div>
					<div class="summary-total-card compact-total">
						<div>
							<span>{{ __('Total') }}</span>
							<small>{{ selectedPaymentCurrency }}</small>
						</div>
						<strong>{{ orderSummary.data.total_amount_formatted }}</strong>
					</div>

					<div class="currency-switch">
						<button
							v-for="option in paymentCurrencyOptions"
							:key="option.currency"
							class="currency-option"
							:class="{ 'currency-option-active': selectedPaymentCurrency === option.currency }"
							@click="selectPaymentCurrency(option.currency)"
						>
							{{ option.label }}
						</button>
					</div>

					<div class="coupon-box">
						<label>{{ __('Código de cupón') }}</label>
						<div class="coupon-actions">
							<FormControl
								v-model="appliedCoupon"
								:disabled="orderSummary.data.discount_amount > 0"
								@input="appliedCoupon = $event.target.value.toUpperCase()"
								@keydown.enter="applyCouponCode"
								placeholder="COUPON2025"
								autocomplete="off"
								class="coupon-input"
							/>
							<Button v-if="!orderSummary.data.discount_amount" @click="applyCouponCode" variant="outline">
								{{ __('Aplicar') }}
							</Button>
							<Button v-if="orderSummary.data.discount_amount" @click="removeCoupon" variant="outline">
								<template #icon>
									<X class="size-4 stroke-1.5" />
								</template>
							</Button>
						</div>
					</div>

					<div class="name-note">
						<HelpCircle class="size-4" />
						<span>{{ __('Verifica que el nombre de facturación sea correcto, porque se usará en tu comprobante.') }}</span>
					</div>
				</aside>

				<section class="standard-form certificate-card">
					<div class="card-heading">
						<div class="card-icon">
							<MapPin class="size-5" />
						</div>
						<div>
							<h2>{{ __('Datos de facturación') }}</h2>
							<p>{{ __('Completa tu información para continuar con el pago de forma segura.') }}</p>
						</div>
					</div>

					<div class="standard-fields">
						<div class="field-column">
							<FormControl
								:label="__('Nombre de facturación')"
								v-model="billingDetails.billing_name"
								:required="!!fieldMeta.billing_name?.reqd"
							/>
							<FormControl
								:label="__('Dirección principal')"
								v-model="billingDetails.address_line1"
								:required="!!fieldMeta.address_line1?.reqd"
							/>
							<FormControl
								:label="__('Referencia, departamento o piso')"
								v-model="billingDetails.address_line2"
								:required="!!fieldMeta.address_line2?.reqd"
							/>
							<FormControl
								:label="__('Ciudad')"
								v-model="billingDetails.city"
								:required="!!fieldMeta.city?.reqd"
							/>
							<FormControl
								:label="__('Provincia o región')"
								v-model="billingDetails.state"
								:required="!!fieldMeta.state?.reqd"
							/>
						</div>
						<div class="field-column">
							<Link
								doctype="Country"
								:value="billingDetails.country"
								@change="(option) => changeCurrency(option)"
								:label="__('País')"
								:required="!!fieldMeta.country?.reqd"
							/>
							<FormControl
								:label="__('Código postal')"
								v-model="billingDetails.pincode"
								:required="!!fieldMeta.pincode?.reqd"
							/>
							<FormControl
								:label="__('Teléfono')"
								v-model="billingDetails.phone"
								:required="!!fieldMeta.phone?.reqd"
							/>
							<Link
								doctype="LMS Source"
								:value="billingDetails.source"
								@change="(option) => (billingDetails.source = option)"
								:label="__('¿Dónde conociste StudyBadge?')"
								:required="!!fieldMeta.source?.reqd"
							/>
							<FormControl
								v-if="billingDetails.country == 'India'"
								:label="__('Número GST')"
								v-model="billingDetails.gstin"
								:required="!!fieldMeta.gstin?.reqd"
							/>
							<FormControl
								v-if="billingDetails.country == 'India'"
								:label="__('Número PAN')"
								v-model="billingDetails.pan"
								:required="!!fieldMeta.pan?.reqd"
							/>
						</div>
					</div>

					<div class="standard-footer">
						<div>
							<FormControl
								:label="__('Autorizo que mi información personal se almacene para facturación')"
								type="checkbox"
								class="consent-control"
								v-model="billingDetails.member_consent"
							/>
							<div v-if="showConsentWarning" class="consent-warning">
								{{ __('Autoriza el uso de tus datos para continuar con el pago.') }}
							</div>
						</div>
						<Button
							variant="solid"
							size="md"
							class="certificate-primary"
							:disabled="paypalLoading || brickLoading"
							@click="prepareSelectedCheckout()"
						>
							{{ checkoutButtonLabel }}
						</Button>
					</div>

					<div v-if="hasCheckoutData" class="paypal-standard-box">
						<div v-if="paypalLoading || brickLoading" class="gateway-loading">
							<RefreshCcw class="size-4 animate-spin" />
							{{ __('Cargando pasarela segura...') }}
						</div>
						<div v-show="selectedPaymentCurrency === 'USD'" id="studybadge-paypal-buttons-standard"></div>
						<div v-show="selectedPaymentCurrency === 'PEN'" id="studybadge-mp-payment-brick-standard"></div>
					</div>

					<a class="support-box standard-support" :href="`mailto:${SUPPORT_EMAIL}`">
						<Mail class="size-4" />
						<span>{{ __('¿Necesitas ayuda? Escríbenos a') }} <strong>{{ SUPPORT_EMAIL }}</strong></span>
					</a>
				</section>
			</div>
		</div>

		<div v-else-if="access.data?.message" class="permission-shell">
			<NotPermitted
				:text="access.data.message"
				:buttonLabel="
					type == 'course'
						? 'Pagar curso'
						: type == 'certificate'
							? 'Volver al curso'
							: 'Pagar batch'
				"
				:buttonLink="
					type == 'course' || type == 'certificate'
						? getLmsRoute(`courses/${name}`)
						: getLmsRoute(`batches/${name}`)
				"
			/>
		</div>
		<div v-else-if="!user.data?.name" class="permission-shell">
			<NotPermitted
				text="Inicia sesión para acceder a esta página."
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
	HelpCircle,
	LockKeyhole,
	Mail,
	MapPin,
	ReceiptText,
	RefreshCcw,
	ShieldCheck,
	X,
} from 'lucide-vue-next'
import { useTelemetry } from 'frappe-ui/frappe'
import { getLmsRoute } from '@/utils/basePath'

const user = inject('$user')
const { brand } = sessionStore()
const SUPPORT_EMAIL = 'soporte@studybadge.com'
const showConsentWarning = ref(false)
const mercadoPagoLoader = ref(null)
const paypalLoader = ref(null)
const paymentBrickController = ref(null)
const paypalButtonsController = ref(null)
const brickLoading = ref(false)
const paypalLoading = ref(false)
const certificatePaymentStatus = ref('')
const certificatePaymentMessage = ref('')
const selectedPaymentCurrency = ref('PEN')
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
	isCertificateCheckout.value ? __('Pagar certificado') : __('Datos de facturación')
)

const access = createResource({
	url: 'lms.lms.api.validate_billing_access',
	params: {
		billing_type: props.type,
		name: props.name,
	},
	onSuccess(data) {
		let meta = data.billing_field_meta || {}
		if (meta.source) {
			meta.source.reqd = 0
		}
		Object.assign(fieldMeta, meta)
		setBillingDetails(data.address)
		selectedPaymentCurrency.value = data.preferred_payment_currency || 'PEN'
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
			currency: selectedPaymentCurrency.value,
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
			currency: selectedPaymentCurrency.value,
		}
		return data
	},
})

const certificateCheckout = createResource({
	url: 'lms.lms.payments.create_mp_brick_checkout',
	makeParams() {
		return {
			doctype: props.type == 'batch' ? 'LMS Batch' : 'LMS Course',
			docname: props.name,
			address: billingDetails,
			payment_for_certificate: props.type == 'certificate',
			coupon_code: appliedCoupon.value,
			country: billingDetails.country,
		}
	},
})

const certificatePayment = createResource({
	url: 'lms.lms.payments.process_mp_brick_payment',
})

const paymentStatus = createResource({
	url: 'lms.lms.payments.get_mp_payment_status',
})

const paypalCheckout = createResource({
	url: 'lms.lms.payments.create_paypal_checkout',
	makeParams() {
		return {
			doctype: props.type == 'batch' ? 'LMS Batch' : 'LMS Course',
			docname: props.name,
			address: billingDetails,
			payment_for_certificate: props.type == 'certificate',
			coupon_code: appliedCoupon.value,
			country: billingDetails.country,
		}
	},
})

const paypalCapture = createResource({
	url: 'lms.lms.payments.capture_paypal_checkout',
})

const paymentCurrencyOptions = [
	{ currency: 'PEN', label: 'S/ PEN' },
	{ currency: 'USD', label: '$ USD' },
]

const checkoutButtonLabel = computed(() => {
	if (selectedPaymentCurrency.value === 'USD') {
		return paypalCheckout.data ? __('Reiniciar PayPal') : __('Continuar con PayPal')
	}
	return certificateCheckout.data ? __('Reiniciar pago seguro') : __('Continuar al pago seguro')
})

const hasCheckoutData = computed(() => {
	return selectedPaymentCurrency.value === 'USD'
		? !!paypalCheckout.data
		: !!certificateCheckout.data
})

const paymentStatusTitle = computed(() => {
	if (certificatePaymentStatus.value === 'approved' || certificatePaymentStatus.value === 'COMPLETED') {
		return __('Pago aprobado')
	}
	if (
		certificatePaymentStatus.value === 'pending' ||
		certificatePaymentStatus.value === 'in_process'
	) {
		return __('Pago en revisión')
	}
	return __('No pudimos confirmar el pago')
})

const paymentStatusMessage = computed(() => {
	if (certificatePaymentStatus.value === 'approved' || certificatePaymentStatus.value === 'COMPLETED') {
		return __('Tu certificado ya está desbloqueado. Te llevaremos a la pantalla de certificación.')
	}
	if (
		certificatePaymentStatus.value === 'pending' ||
		certificatePaymentStatus.value === 'in_process'
	) {
		return __('Mercado Pago está procesando la operación. Puedes actualizar el estado en unos segundos.')
	}
	return certificatePaymentMessage.value || __('Revisa los datos del método de pago e intenta nuevamente. Si el problema continúa, escribe a soporte@studybadge.com.')
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
					return __('Cuéntanos dónde conociste StudyBadge.')
				}
				if (!billingDetails.member_consent) {
					showConsentWarning.value = true
					return __('Autoriza el uso de tus datos para continuar con el pago.')
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
		return __('Cuéntanos dónde conociste StudyBadge.')
	}
	if (!billingDetails.member_consent) {
		showConsentWarning.value = true
		return __('Autoriza el uso de tus datos para continuar con el pago.')
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
	destroyPayPalButtons()
	paypalCheckout.data = null
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

const prepareSelectedCheckout = () => {
	if (selectedPaymentCurrency.value === 'USD') {
		preparePayPalCheckout()
		return
	}
	prepareCertificateCheckout()
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

function loadPayPal(clientId) {
	if (!clientId) {
		return Promise.reject(new Error(__('Falta configurar el Client ID de PayPal. Escribe a soporte@studybadge.com si necesitas ayuda.')))
	}
	if (window.paypal) {
		return Promise.resolve(window.paypal)
	}
	if (paypalLoader.value) {
		return paypalLoader.value
	}
	paypalLoader.value = new Promise((resolve, reject) => {
		const script = document.createElement('script')
		script.src = `https://www.paypal.com/sdk/js?client-id=${encodeURIComponent(clientId)}&currency=USD&intent=capture`
		script.onload = () => resolve(window.paypal)
		script.onerror = reject
		document.body.appendChild(script)
	})
	return paypalLoader.value
}

async function initMercadoPagoPaymentBrick() {
	if (!certificateCheckout.data?.public_key || !certificateCheckout.data?.preference_id) {
		toast.error(__('Mercado Pago no devolvió los datos del checkout. Intenta nuevamente o escribe a soporte@studybadge.com.'))
		return
	}
	brickLoading.value = true
	try {
		const MercadoPago = await loadMercadoPago()
		const mp = new MercadoPago(certificateCheckout.data.public_key, {
			locale: 'es-PE',
		})
		const bricksBuilder = mp.bricks()
		const containerId = isCertificateCheckout.value ? 'studybadge-mp-payment-brick' : 'studybadge-mp-payment-brick-standard'
		paymentBrickController.value = await bricksBuilder.create(
			'payment',
			containerId,
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
						toast.error(error?.message || __('Mercado Pago no pudo cargar. Revisa tu conexión o escribe a soporte@studybadge.com.'))
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
		toast.error(error?.message || __('No se pudo cargar Mercado Pago. Intenta nuevamente o escribe a soporte@studybadge.com.'))
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
		toast.success(__('Pago recibido por Mercado Pago. Esperando confirmación.'))
		return
	}
	toast.error(__('Mercado Pago no aprobó la operación. Intenta nuevamente o escribe a soporte@studybadge.com.'))
}

function handlePayPalPaymentResult(data) {
	certificatePaymentStatus.value = data.status
	certificatePaymentMessage.value = ''
	if (data.status === 'COMPLETED') {
		toast.success(__('Pago aprobado.'))
		setTimeout(() => {
			window.location.href = data.redirect_url
		}, 700)
		return
	}
	toast.error(__('PayPal no aprobó la operación. Intenta nuevamente o escribe a soporte@studybadge.com.'))
}

function preparePayPalCheckout() {
	const validationError = validateBillingDetails()
	if (validationError) {
		toast.error(validationError)
		return
	}
	destroyPaymentBrick()
	destroyPayPalButtons()
	certificateCheckout.data = null
	certificatePaymentStatus.value = ''
	certificatePaymentMessage.value = ''
	paypalCheckout.submit(
		{},
		{
			onSuccess(data) {
				capture('checkout_initiated', { type: props.type, gateway: 'paypal' })
				if (data.status === 'COMPLETED') {
					window.location.href = data.redirect_url
					return
				}
				nextTick(() => initPayPalButtons())
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

async function initPayPalButtons() {
	if (!paypalCheckout.data?.client_id || !paypalCheckout.data?.order_id) {
		toast.error(__('PayPal no devolvió los datos del checkout. Intenta nuevamente o escribe a soporte@studybadge.com.'))
		return
	}
	paypalLoading.value = true
	try {
		const paypal = await loadPayPal(paypalCheckout.data.client_id)
		const containerId = isCertificateCheckout.value
			? 'studybadge-paypal-buttons-certificate'
			: 'studybadge-paypal-buttons-standard'
		paypalButtonsController.value = paypal.Buttons({
			createOrder() {
				return paypalCheckout.data.order_id
			},
			onApprove(data) {
				return new Promise((resolve, reject) => {
					paypalCapture.submit(
						{
							payment: paypalCheckout.data.payment,
							order_id: data.orderID,
						},
						{
							onSuccess(result) {
								handlePayPalPaymentResult(result)
								resolve()
							},
							onError(err) {
								const message = err.messages?.[0] || err
								certificatePaymentStatus.value = 'FAILED'
								certificatePaymentMessage.value = message
								toast.error(message)
								reject(err)
							},
						}
					)
				})
			},
			onError(error) {
				toast.error(error?.message || __('PayPal no pudo cargar. Revisa tu conexión o escribe a soporte@studybadge.com.'))
			},
		})
		await paypalButtonsController.value.render(`#${containerId}`)
	} catch (error) {
		toast.error(error?.message || __('No se pudo cargar PayPal. Intenta nuevamente o escribe a soporte@studybadge.com.'))
	} finally {
		paypalLoading.value = false
	}
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

function destroyPayPalButtons() {
	if (paypalButtonsController.value?.close) {
		paypalButtonsController.value.close()
	}
	paypalButtonsController.value = null
}

function applyCouponCode() {
	if (!appliedCoupon.value) {
		toast.error(__('Ingresa un código de cupón.'))
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
				__('Completa el campo obligatorio: ') +
				field
					.replaceAll('_', ' ')
					.toLowerCase()
			)
	}

	if (billingDetails.gstin && !billingDetails.pan)
		return __('Ingresa un número PAN válido.')

	if (billingDetails.country == 'India' && !billingDetails.state)
		return __('Ingresa una provincia o región válida.')

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
		return __('Ingresa una provincia o región válida.')
}

const showError = (err) => {
	toast.error(err.messages?.[0] || err || __('No pudimos procesar la solicitud. Escríbenos a soporte@studybadge.com.'))
}

const changeCurrency = (country) => {
	billingDetails.country = country
	if (country === 'Peru' || country === 'Perú') {
		selectedPaymentCurrency.value = 'PEN'
	} else if (country) {
		selectedPaymentCurrency.value = 'USD'
	}
	orderSummary.reload()
}

const selectPaymentCurrency = (currency) => {
	selectedPaymentCurrency.value = currency
	certificateCheckout.data = null
	paypalCheckout.data = null
	destroyPaymentBrick()
	destroyPayPalButtons()
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
	destroyPayPalButtons()
})

usePageMeta(() => {
	return {
		title: pageTitle.value,
		icon: brand.favicon,
	}
})
</script>

<style scoped>
.billing-page {
	min-height: 100vh;
	background:
		radial-gradient(circle at 12% 0%, rgba(216, 165, 56, 0.14), transparent 28%),
		radial-gradient(circle at 90% 8%, rgba(10, 35, 81, 0.10), transparent 26%),
		linear-gradient(180deg, #f7f9fd 0%, #eef4fb 44%, #ffffff 100%);
	color: #172033;
}

.billing-topbar {
	position: sticky;
	top: 0;
	z-index: 10;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 14px;
	border-bottom: 1px solid rgba(10, 35, 81, 0.08);
	background: rgba(255, 255, 255, 0.86);
	padding: 12px 18px;
	backdrop-filter: blur(18px);
	-webkit-backdrop-filter: blur(18px);
}

.billing-breadcrumbs {
	height: 28px;
}

.support-chip {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	min-height: 34px;
	border-radius: 999px;
	border: 1px solid rgba(10, 35, 81, 0.12);
	background: #ffffff;
	padding: 0 12px;
	color: #0a2351;
	font-size: 12px;
	font-weight: 800;
	text-decoration: none;
	box-shadow: 0 8px 22px rgba(10, 35, 81, 0.07);
}

.support-chip:hover,
.support-box:hover,
.plus-callout:hover {
	text-decoration: none;
}

.certificate-checkout,
.standard-checkout {
	min-height: calc(100vh - 53px);
}

.certificate-band {
	position: relative;
	overflow: hidden;
	background:
		radial-gradient(circle at 76% 16%, rgba(216, 165, 56, 0.30), transparent 28%),
		radial-gradient(circle at 10% 84%, rgba(255, 255, 255, 0.13), transparent 30%),
		linear-gradient(135deg, #061b49 0%, #0a2351 52%, #12346f 100%);
}

.certificate-band::before {
	content: '';
	position: absolute;
	inset: 0;
	background:
		linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px),
		linear-gradient(180deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
	background-size: 54px 54px;
	mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.70), transparent 92%);
	pointer-events: none;
}

.certificate-band-grid {
	position: relative;
	z-index: 1;
	display: grid;
	grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
	gap: 26px;
	width: min(1120px, calc(100% - 40px));
	margin: 0 auto;
	padding: 44px 0 72px;
}

.certificate-hero-panel {
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 30px;
	background: rgba(255, 255, 255, 0.075);
	padding: 34px;
	box-shadow: 0 24px 60px rgba(0, 0, 0, 0.16);
	backdrop-filter: blur(18px);
	-webkit-backdrop-filter: blur(18px);
}

.certificate-eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	margin-bottom: 18px;
	border: 1px solid rgba(216, 165, 56, 0.32);
	border-radius: 999px;
	background: rgba(216, 165, 56, 0.16);
	padding: 8px 12px;
	color: #ffe7a8;
	font-size: 12px;
	font-weight: 900;
	letter-spacing: 0.04em;
	text-transform: uppercase;
}

.certificate-hero-panel h1 {
	max-width: 780px;
	margin: 0;
	color: #ffffff;
	font-size: clamp(36px, 5vw, 62px);
	font-weight: 950;
	letter-spacing: -0.055em;
	line-height: 0.98;
}

.certificate-hero-panel p {
	max-width: 720px;
	margin: 18px 0 0;
	color: rgba(232, 240, 255, 0.86);
	font-size: 16px;
	line-height: 1.75;
}

.certificate-proof-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 12px;
	margin-top: 28px;
}

.certificate-proof {
	display: flex;
	align-items: center;
	gap: 9px;
	min-height: 48px;
	border: 1px solid rgba(255, 255, 255, 0.13);
	border-radius: 16px;
	background: rgba(255, 255, 255, 0.10);
	padding: 12px;
	color: #ffffff;
	font-size: 13px;
	font-weight: 800;
}

.certificate-summary,
.certificate-card,
.standard-summary {
	border: 1px solid rgba(10, 35, 81, 0.09);
	border-radius: 28px;
	background: rgba(255, 255, 255, 0.94);
	box-shadow: 0 22px 54px rgba(10, 35, 81, 0.12);
}

.certificate-summary {
	padding: 26px;
	align-self: stretch;
}

.summary-top {
	display: flex;
	align-items: flex-start;
	gap: 14px;
}

.summary-icon,
.card-icon {
	width: 46px;
	height: 46px;
	flex: 0 0 auto;
	display: grid;
	place-items: center;
	border-radius: 16px;
	background: #eaf1fb;
	color: #0a2351;
}

.summary-kicker {
	color: #718198;
	font-size: 11px;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.summary-top h2 {
	margin: 4px 0 0;
	color: #172033;
	font-size: 20px;
	font-weight: 950;
	line-height: 1.18;
	letter-spacing: -0.02em;
}

.summary-total-card {
	display: flex;
	align-items: flex-end;
	justify-content: space-between;
	gap: 16px;
	margin-top: 24px;
	border-radius: 22px;
	background:
		radial-gradient(circle at 90% 0%, rgba(216, 165, 56, 0.22), transparent 40%),
		linear-gradient(135deg, #f8fbff 0%, #eef5ff 100%);
	border: 1px solid #e4edf8;
	padding: 18px;
}

.summary-total-card span,
.price-row span {
	display: block;
	color: #718198;
	font-size: 12px;
	font-weight: 900;
	text-transform: uppercase;
	letter-spacing: 0.04em;
}

.summary-total-card small {
	display: block;
	margin-top: 4px;
	color: #718198;
	font-size: 12px;
	font-weight: 700;
}

.summary-total-card strong {
	color: #0a2351;
	font-size: 34px;
	font-weight: 950;
	line-height: 1;
	letter-spacing: -0.04em;
	white-space: nowrap;
}

.currency-switch {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 6px;
	margin-top: 18px;
	border: 1px solid #dbe6f3;
	border-radius: 18px;
	background: #f3f7fc;
	padding: 6px;
}

.currency-option {
	min-height: 40px;
	border: 0;
	border-radius: 13px;
	background: transparent;
	color: #64748b;
	font-size: 13px;
	font-weight: 900;
	transition: 0.18s ease;
}

.currency-option-active {
	background: #ffffff;
	color: #0a2351;
	box-shadow: 0 8px 18px rgba(10, 35, 81, 0.10);
}

.plus-callout,
.support-box,
.name-note,
.gateway-tip {
	display: flex;
	align-items: flex-start;
	gap: 12px;
	border-radius: 20px;
	padding: 15px;
	font-size: 13px;
	line-height: 1.55;
}

.plus-callout {
	margin-top: 18px;
	border: 1px solid rgba(216, 165, 56, 0.35);
	background: #fff8e6;
	color: #6d4a0d;
}

.plus-callout svg,
.gateway-tip svg,
.name-note svg,
.support-box svg {
	flex: 0 0 auto;
	margin-top: 2px;
}

.plus-callout strong,
.gateway-tip strong,
.support-box strong {
	font-weight: 950;
}

.checkout-grid {
	display: grid;
	grid-template-columns: minmax(320px, 0.9fr) minmax(0, 1.1fr);
	gap: 26px;
	width: min(1120px, calc(100% - 40px));
	margin: -44px auto 0;
	padding-bottom: 72px;
	position: relative;
	z-index: 2;
}

.certificate-card {
	padding: 26px;
}

.card-heading {
	display: flex;
	align-items: flex-start;
	gap: 14px;
	margin-bottom: 24px;
}

.card-heading h2 {
	margin: 0;
	color: #172033;
	font-size: 20px;
	font-weight: 950;
	letter-spacing: -0.02em;
	line-height: 1.15;
}

.card-heading p {
	margin: 7px 0 0;
	color: #64748b;
	font-size: 14px;
	line-height: 1.55;
}

.form-stack,
.field-column {
	display: grid;
	gap: 16px;
}

.field-pair,
.standard-fields {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 16px;
}

.consent-control {
	line-height: 1.6;
}

.consent-warning {
	border: 1px solid #fecdd3;
	border-radius: 14px;
	background: #fff1f2;
	padding: 10px 12px;
	color: #be123c;
	font-size: 12px;
	font-weight: 800;
}

.certificate-primary {
	width: 100%;
	border-radius: 16px !important;
	background: #0a2351 !important;
	font-weight: 900 !important;
	box-shadow: 0 14px 28px rgba(10, 35, 81, 0.20);
}

.gateway-heading {
	align-items: center;
}

.gateway-icon {
	background: #fff4d6;
	color: #9a6a15;
}

.gateway-currency {
	margin-left: auto;
	border-radius: 999px;
	background: #eaf1fb;
	padding: 7px 10px;
	color: #0a2351;
	font-size: 12px;
	font-weight: 950;
}

.gateway-tip {
	margin-bottom: 18px;
	border: 1px solid #cfe0f4;
	background: #eef6ff;
	color: #0a2351;
}

.gateway-tip p {
	margin: 4px 0 0;
	color: #39516f;
}

.certificate-empty {
	display: flex;
	min-height: 320px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	border: 1.5px dashed rgba(10, 35, 81, 0.22);
	border-radius: 24px;
	background:
		radial-gradient(circle at 50% 0%, rgba(216, 165, 56, 0.12), transparent 32%),
		#f8fbff;
	padding: 28px;
	text-align: center;
}

.empty-icon {
	width: 68px;
	height: 68px;
	display: grid;
	place-items: center;
	border-radius: 22px;
	background: #eaf1fb;
	color: #0a2351;
}

.certificate-empty h3 {
	margin: 16px 0 6px;
	color: #172033;
	font-size: 17px;
	font-weight: 950;
}

.certificate-empty p {
	max-width: 380px;
	margin: 0;
	color: #64748b;
	font-size: 14px;
	line-height: 1.6;
}

.gateway-loading {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 26px 0;
	color: #64748b;
	font-size: 14px;
	font-weight: 800;
}

.payment-status {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 14px;
	margin-top: 18px;
	border-radius: 20px;
	padding: 16px;
	font-size: 14px;
}

.payment-status strong {
	display: block;
	font-weight: 950;
}

.payment-status p {
	margin: 4px 0 0;
	line-height: 1.55;
}

.payment-status-success {
	border: 1px solid #bbf7d0;
	background: #ecfdf5;
	color: #047857;
}

.payment-status-warning {
	border: 1px solid #fde68a;
	background: #fffbeb;
	color: #92400e;
}

.support-box {
	margin-top: 18px;
	border: 1px solid rgba(10, 35, 81, 0.12);
	background: #fbfdff;
	color: #41546e;
}

.support-box strong {
	color: #0a2351;
}

.standard-checkout {
	padding: 34px 20px 78px;
}

.standard-layout {
	display: grid;
	grid-template-columns: minmax(300px, 0.82fr) minmax(0, 1.18fr);
	gap: 26px;
	width: min(1120px, 100%);
	margin: 0 auto;
}

.standard-summary {
	position: sticky;
	top: 82px;
	align-self: start;
	padding: 24px;
}

.price-row {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	border-bottom: 1px solid #e4edf8;
	padding: 14px 0;
	color: #172033;
}

.price-row strong {
	font-weight: 900;
}

.discount-row strong {
	color: #047857;
}

.compact-total {
	margin-top: 16px;
}

.compact-total strong {
	font-size: 26px;
}

.coupon-box {
	margin-top: 18px;
	border-radius: 20px;
	background: #f8fbff;
	border: 1px solid #e4edf8;
	padding: 16px;
}

.coupon-box label {
	display: block;
	margin-bottom: 10px;
	color: #718198;
	font-size: 12px;
	font-weight: 900;
	text-transform: uppercase;
	letter-spacing: 0.04em;
}

.coupon-actions {
	display: flex;
	align-items: center;
	gap: 10px;
}

.coupon-input {
	flex: 1;
}

.name-note {
	margin-top: 18px;
	border: 1px solid rgba(216, 165, 56, 0.32);
	background: #fff8e6;
	color: #6d4a0d;
}

.standard-form {
	padding: 28px;
}

.standard-footer {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 18px;
	margin-top: 26px;
	border-top: 1px solid #e4edf8;
	padding-top: 20px;
}

.standard-footer .certificate-primary {
	width: auto;
	min-width: 190px;
}

.paypal-standard-box {
	margin-top: 22px;
	border: 1px solid #e4edf8;
	border-radius: 22px;
	background: #f8fbff;
	padding: 18px;
}

.standard-support {
	margin-top: 22px;
}

.permission-shell {
	width: min(900px, calc(100% - 40px));
	margin: 0 auto;
	padding: 42px 0;
}

:deep(input),
:deep(textarea),
:deep(select) {
	border-radius: 14px !important;
}

:global(:root[data-theme='dark']) .billing-page {
	background: #0f172a;
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .billing-topbar,
:global(:root[data-theme='dark']) .certificate-summary,
:global(:root[data-theme='dark']) .certificate-card,
:global(:root[data-theme='dark']) .standard-summary,
:global(:root[data-theme='dark']) .support-chip {
	border-color: rgba(255, 255, 255, 0.08);
	background: #111827;
	box-shadow: none;
}

:global(:root[data-theme='dark']) .summary-top h2,
:global(:root[data-theme='dark']) .card-heading h2,
:global(:root[data-theme='dark']) .certificate-empty h3 {
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .card-heading p,
:global(:root[data-theme='dark']) .certificate-empty p,
:global(:root[data-theme='dark']) .summary-kicker {
	color: #94a3b8;
}

:global(:root[data-theme='dark']) .summary-total-card,
:global(:root[data-theme='dark']) .certificate-empty,
:global(:root[data-theme='dark']) .coupon-box,
:global(:root[data-theme='dark']) .paypal-standard-box,
:global(:root[data-theme='dark']) .support-box {
	border-color: rgba(255, 255, 255, 0.08);
	background: rgba(255, 255, 255, 0.04);
}

@media (max-width: 980px) {
	.certificate-band-grid,
	.checkout-grid,
	.standard-layout {
		grid-template-columns: 1fr;
	}

	.checkout-grid {
		margin-top: -42px;
	}

	.standard-summary {
		position: static;
	}
}

@media (max-width: 720px) {
	.billing-topbar {
		align-items: flex-start;
		flex-direction: column;
	}

	.support-chip {
		width: 100%;
		justify-content: center;
	}

	.certificate-band-grid,
	.checkout-grid {
		width: min(100% - 28px, 1120px);
	}

	.certificate-band-grid {
		padding: 26px 0 62px;
	}

	.certificate-hero-panel,
	.certificate-summary,
	.certificate-card,
	.standard-summary {
		border-radius: 24px;
	}

	.certificate-hero-panel,
	.certificate-summary,
	.certificate-card,
	.standard-form,
	.standard-summary {
		padding: 20px;
	}

	.certificate-proof-grid,
	.field-pair,
	.standard-fields {
		grid-template-columns: 1fr;
	}

	.summary-total-card {
		align-items: flex-start;
		flex-direction: column;
	}

	.payment-status,
	.standard-footer {
		align-items: stretch;
		flex-direction: column;
	}

	.standard-footer .certificate-primary {
		width: 100%;
	}
}
</style>

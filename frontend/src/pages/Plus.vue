<template>
	<div>
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<Badge v-if="plusStatus.data?.active" theme="green">
				{{ __('Activo') }}
			</Badge>
		</header>

		<div class="mx-auto max-w-5xl px-5 py-8">
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
								{{ __('Certificados e IA sin limites para avanzar mejor.') }}
							</p>
						</div>
					</div>

					<div class="grid gap-3 sm:grid-cols-2">
						<div
							v-for="benefit in benefits"
							:key="benefit.label"
							class="flex items-start gap-3 rounded-md border p-4"
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
						v-if="plusStatus.data?.subscription?.status"
						class="mt-4 rounded-md bg-surface-gray-2 p-3 text-sm text-ink-gray-7"
					>
						{{ __('Estado') }}:
						<span class="font-medium text-ink-gray-9">
							{{ plusStatus.data.subscription.status }}
						</span>
					</div>

					<Button
						class="mt-5 w-full"
						variant="solid"
						size="md"
						:loading="activating"
						:disabled="plusStatus.data?.active"
						@click="activatePlus"
					>
						<template #prefix>
							<CreditCard class="size-4 stroke-1.5" />
						</template>
						{{
							plusStatus.data?.active
								? __('Plus activo')
								: __('Activar Plus con Mercado Pago')
						}}
					</Button>

					<Button
						v-if="plusStatus.data?.subscription?.init_point && !plusStatus.data?.active"
						class="mt-3 w-full"
						variant="outline"
						@click="openExistingCheckout"
					>
						{{ __('Continuar pago pendiente') }}
					</Button>

					<p class="mt-4 text-xs leading-5 text-ink-gray-5">
						{{
							__(
								'El cobro se procesa en Mercado Pago. Puedes cancelar la suscripcion desde Mercado Pago.'
							)
						}}
					</p>
				</aside>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject, ref } from 'vue'
import { Badge, Breadcrumbs, Button, createResource, toast, usePageMeta } from 'frappe-ui'
import {
	Award,
	Bot,
	CalendarDays,
	CheckCircle2,
	CreditCard,
	Crown,
	Sparkles,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const activating = ref(false)
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

const plusStatus = createResource({
	url: 'lms.lms.subscriptions.get_plus_status',
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

const formattedPrice = computed(() => {
	const plan = plusStatus.data?.plan
	if (!plan) return 'S/ 29'
	if (plan.currency === 'PEN') return `S/ ${Number(plan.amount).toFixed(0)}`
	return `${plan.currency} ${Number(plan.amount).toFixed(0)}`
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
	window.location.href = plusStatus.data.subscription.init_point
}

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

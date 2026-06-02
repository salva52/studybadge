<template>
	<div class="min-h-screen bg-surface-gray-1">
		<div class="mx-auto w-full max-w-5xl px-4 py-6 sm:px-6 lg:px-8">
			<header class="mb-6">
				<Breadcrumbs
					class="mb-5"
					:items="[{ label: __('Programa de Referidos'), route: { name: 'Referrals' } }]"
				/>

				<div class="rounded-2xl border border-outline-gray-2 bg-surface-white p-6 shadow-sm">
					<div class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_320px] lg:items-center">
						<div>
							<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-outline-gray-2 bg-surface-gray-1 px-3 py-1">
								<Gift class="size-4 text-ink-gray-7" />
								<span class="text-xs font-semibold text-ink-gray-7">
									{{ __('Referidos StudyBadge') }}
								</span>
							</div>

							<h1 class="text-3xl font-semibold tracking-tight text-ink-gray-9 sm:text-4xl">
								{{ __('Invita amigos y gana beneficios') }}
							</h1>

							<p class="mt-3 max-w-2xl text-base leading-7 text-ink-gray-6">
								{{ __('Comparte tu enlace. Cuando tus amigos creen una cuenta y verifiquen su correo, avanzas hacia recompensas como cursos gratis y StudyBadge Plus.') }}
							</p>
						</div>

						<div class="rounded-2xl border border-outline-gray-2 bg-surface-gray-1 p-5">
							<p class="text-sm font-medium text-ink-gray-6">
								{{ __('Amigos verificados') }}
							</p>

							<div class="mt-2 flex items-end gap-2">
								<span class="text-5xl font-semibold text-ink-gray-9">
									{{ verifiedCount }}
								</span>
								<span class="mb-2 text-sm font-medium text-ink-gray-5">
									{{ __('de 10') }}
								</span>
							</div>

							<p class="mt-3 text-sm leading-6 text-ink-gray-6">
								{{ nextRewardText }}
							</p>
						</div>
					</div>
				</div>
			</header>

			<div v-if="dashboard.data" class="space-y-6 pb-10">
				<section class="grid grid-cols-1 gap-4 md:grid-cols-3">
					<div class="info-card">
						<div class="info-icon">
							<LinkIcon class="size-5" />
						</div>
						<h3>{{ __('1. Comparte tu enlace') }}</h3>
						<p>{{ __('Envíalo por WhatsApp, redes sociales o a tus amigos directamente.') }}</p>
					</div>

					<div class="info-card">
						<div class="info-icon">
							<UserCheck class="size-5" />
						</div>
						<h3>{{ __('2. Tu amigo se registra') }}</h3>
						<p>{{ __('Debe crear su cuenta en StudyBadge usando tu enlace de referido.') }}</p>
					</div>

					<div class="info-card">
						<div class="info-icon">
							<MailCheck class="size-5" />
						</div>
						<h3>{{ __('3. Verifica su correo') }}</h3>
						<p>{{ __('Cuando confirme su email, contará como referido válido para tus premios.') }}</p>
					</div>
				</section>

				<section class="rounded-2xl border border-outline-gray-2 bg-surface-white p-5 shadow-sm">
					<div class="mb-5 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
						<div>
							<h2 class="text-xl font-semibold text-ink-gray-9">
								{{ __('Recompensas') }}
							</h2>
							<p class="mt-1 text-sm leading-6 text-ink-gray-6">
								{{ __('Mientras más amigos verificados consigas, mejores beneficios desbloqueas.') }}
							</p>
						</div>

						<div class="rounded-full bg-surface-gray-1 px-3 py-1 text-sm font-medium text-ink-gray-7">
							{{ verifiedCount }} / 10 {{ __('verificados') }}
						</div>
					</div>

					<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
						<div class="reward-card" :class="{ 'is-unlocked': verifiedCount >= 5 }">
							<div class="flex items-start justify-between gap-4">
								<div>
									<div class="reward-badge">
										<Ticket v-if="verifiedCount < 5" class="size-5" />
										<CheckCircle2 v-else class="size-5" />
										<span>{{ __('Meta 1') }}</span>
									</div>

									<h3>{{ __('5 amigos verificados') }}</h3>
									<p>{{ __('Gana un cupón para desbloquear un curso gratis valorizado en S/ 9.90.') }}</p>
								</div>

								<div class="reward-status" :class="{ 'complete': verifiedCount >= 5 }">
									{{ verifiedCount >= 5 ? __('Listo') : `${Math.max(5 - verifiedCount, 0)} ${__('faltan')}` }}
								</div>
							</div>
						</div>

						<div class="reward-card" :class="{ 'is-unlocked': verifiedCount >= 10 }">
							<div class="flex items-start justify-between gap-4">
								<div>
									<div class="reward-badge">
										<Crown v-if="verifiedCount < 10" class="size-5" />
										<CheckCircle2 v-else class="size-5" />
										<span>{{ __('Meta 2') }}</span>
									</div>

									<h3>{{ __('10 amigos verificados') }}</h3>
									<p>{{ __('Desbloquea 1 mes gratis de StudyBadge Plus para aprender con más herramientas.') }}</p>
								</div>

								<div class="reward-status" :class="{ 'complete': verifiedCount >= 10 }">
									{{ verifiedCount >= 10 ? __('Listo') : `${Math.max(10 - verifiedCount, 0)} ${__('faltan')}` }}
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="rounded-2xl border border-outline-gray-2 bg-surface-white p-5 shadow-sm">
					<div class="mb-4">
						<h2 class="text-xl font-semibold text-ink-gray-9">
							{{ __('Tu enlace de referido') }}
						</h2>
						<p class="mt-1 text-sm leading-6 text-ink-gray-6">
							{{ __('Copia este enlace y compártelo. Cada registro verificado sumará a tu progreso.') }}
						</p>
					</div>

					<div class="flex flex-col gap-3 sm:flex-row">
						<div class="relative flex-1">
							<input
								type="text"
								readonly
								:value="referralLink"
								class="w-full rounded-xl border border-outline-gray-2 bg-surface-gray-1 px-4 py-3 pe-10 text-sm text-ink-gray-8 outline-none transition focus:border-outline-gray-4 focus:bg-surface-white"
							/>
							<LinkIcon class="absolute right-3 top-1/2 size-4 -translate-y-1/2 text-ink-gray-4" />
						</div>

						<Button
							variant="solid"
							class="h-11 shrink-0 !bg-[#0a2251] hover:!bg-[#102f68]"
							@click="copyLink"
						>
							<template #prefix>
								<Copy class="size-4" />
							</template>
							{{ __('Copiar enlace') }}
						</Button>
					</div>

					<div class="mt-4 flex flex-col gap-3 sm:flex-row">
						<a
							:href="whatsappShareLink"
							target="_blank"
							rel="noopener noreferrer"
							class="share-button"
						>
							<MessageCircle class="size-4" />
							<span>{{ __('Compartir por WhatsApp') }}</span>
						</a>

						<a
							:href="twitterShareLink"
							target="_blank"
							rel="noopener noreferrer"
							class="share-button"
						>
							<Send class="size-4" />
							<span>{{ __('Compartir en Twitter') }}</span>
						</a>
					</div>
				</section>

				<section class="rounded-2xl border border-outline-gray-2 bg-surface-white p-5 shadow-sm">
					<div class="mb-5 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
						<div>
							<h2 class="text-xl font-semibold text-ink-gray-9">
								{{ __('Tu progreso') }}
							</h2>
							<p class="mt-1 text-sm leading-6 text-ink-gray-6">
								{{ __('Sigue avanzando hasta desbloquear todos los premios.') }}
							</p>
						</div>

						<p class="text-sm font-semibold text-ink-gray-8">
							{{ progressPercent }}%
						</p>
					</div>

					<div class="relative">
						<div class="h-3 overflow-hidden rounded-full bg-surface-gray-2">
							<div
								class="h-full rounded-full bg-[#0a2251] transition-all duration-700"
								:style="{ width: progressPercent + '%' }"
							></div>
						</div>

						<div class="mt-3 grid grid-cols-3 text-xs font-medium text-ink-gray-5">
							<span>0</span>
							<span class="text-center">{{ __('5 amigos') }}</span>
							<span class="text-right">{{ __('10 amigos') }}</span>
						</div>
					</div>
				</section>

				<section class="rounded-2xl border border-outline-gray-2 bg-surface-white p-5 shadow-sm">
					<div class="mb-5 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
						<div>
							<h2 class="text-xl font-semibold text-ink-gray-9">
								{{ __('Amigos invitados') }}
							</h2>
							<p class="mt-1 text-sm leading-6 text-ink-gray-6">
								{{ __('Aquí verás quiénes se registraron con tu enlace y su estado.') }}
							</p>
						</div>

						<div class="rounded-full bg-surface-gray-1 px-3 py-1 text-sm font-medium text-ink-gray-7">
							{{ dashboard.data.total_count }} {{ __('invitados') }}
						</div>
					</div>

					<div v-if="dashboard.data.referrals.length === 0" class="empty-state">
						<div class="empty-icon">
							<Users class="size-7" />
						</div>

						<h3>{{ __('Aún no tienes invitados') }}</h3>
						<p>{{ __('Comparte tu enlace para empezar a sumar amigos verificados y desbloquear recompensas.') }}</p>

						<Button variant="solid" @click="copyLink">
							<template #prefix>
								<Copy class="size-4" />
							</template>
							{{ __('Copiar mi enlace') }}
						</Button>
					</div>

					<ul v-else class="divide-y divide-outline-gray-2 overflow-hidden rounded-xl border border-outline-gray-2">
						<li
							v-for="ref in dashboard.data.referrals"
							:key="ref.referred_email"
							class="flex flex-col gap-3 bg-surface-white p-4 sm:flex-row sm:items-center sm:justify-between"
						>
							<div>
								<p class="text-sm font-semibold text-ink-gray-9">
									{{ ref.referred_email }}
								</p>
								<p class="mt-1 text-xs text-ink-gray-5">
									{{ ref.status === 'Verified' ? __('Correo verificado') : __('Pendiente de verificación') }}
								</p>
							</div>

							<div class="ref-status" :class="ref.status.toLowerCase()">
								<Clock v-if="ref.status === 'Pending'" class="size-4" />
								<CheckCircle v-else-if="ref.status === 'Verified'" class="size-4" />
								<span>{{ statusLabel(ref.status) }}</span>
							</div>
						</li>
					</ul>
				</section>
			</div>

			<div
				v-else
				class="flex min-h-[50vh] items-center justify-center"
			>
				<div class="rounded-2xl border border-outline-gray-2 bg-surface-white p-6 text-center shadow-sm">
					<p class="text-sm font-medium text-ink-gray-7">
						{{ __('Cargando referidos...') }}
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import { Breadcrumbs, Button, createResource, toast } from 'frappe-ui'
import {
	Ticket,
	Crown,
	Copy,
	Users,
	Clock,
	CheckCircle,
	CheckCircle2,
	Gift,
	Link as LinkIcon,
	UserCheck,
	MailCheck,
	MessageCircle,
	Send,
} from 'lucide-vue-next'

const dashboard = createResource({
	url: 'lms.lms.referral.get_referral_dashboard',
	auto: true,
})

const verifiedCount = computed(() => dashboard.data?.verified_count || 0)
const referralLink = computed(() => dashboard.data?.referral_link || '')

const progressPercent = computed(() => {
	return Math.min(Math.round((verifiedCount.value / 10) * 100), 100)
})

const nextRewardText = computed(() => {
	if (verifiedCount.value >= 10) {
		return __('Ya desbloqueaste todas las recompensas disponibles.')
	}

	if (verifiedCount.value >= 5) {
		return `${Math.max(10 - verifiedCount.value, 0)} ${__('amigos más para ganar 1 mes de StudyBadge Plus.')}`
	}

	return `${Math.max(5 - verifiedCount.value, 0)} ${__('amigos más para ganar tu primer curso gratis.')}`
})

const whatsappShareLink = computed(() => {
	const text = `Únete a StudyBadge con mi enlace y empieza a aprender con cursos prácticos: ${referralLink.value}`
	return `https://wa.me/?text=${encodeURIComponent(text)}`
})

const twitterShareLink = computed(() => {
	const text = `Estoy usando StudyBadge para aprender con cursos prácticos. Únete con mi enlace: ${referralLink.value}`
	return `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`
})

const statusLabel = (status) => {
	if (status === 'Verified') return __('Verificado')
	if (status === 'Pending') return __('Pendiente')
	return status
}

const copyLink = async () => {
	try {
		await navigator.clipboard.writeText(referralLink.value)

		toast({
			title: __('Enlace copiado'),
			text: __('Tu enlace de referido fue copiado al portapapeles.'),
			icon: 'check',
			iconClasses: 'text-green-500',
		})
	} catch (error) {
		toast({
			title: __('No se pudo copiar'),
			text: __('Copia el enlace manualmente desde el campo.'),
			icon: 'x',
			iconClasses: 'text-red-500',
		})
	}
}
</script>

<style scoped>
.info-card {
	@apply rounded-2xl border bg-surface-white p-5 shadow-sm transition;
	border-color: #dbe3f0;
}

.info-card:hover {
	border-color: #0a2251;
	box-shadow: 0 10px 30px rgba(10, 34, 81, 0.08);
}

.info-card h3 {
	@apply mt-4 text-base font-semibold;
	color: #0a2251;
}

.info-card p {
	@apply mt-2 text-sm leading-6 text-ink-gray-6;
}

.info-icon {
	@apply flex size-10 items-center justify-center rounded-xl border;
	background: #eef3fb;
	border-color: #d8e2f1;
	color: #0a2251;
}

.reward-card {
	@apply rounded-2xl border p-5 transition;
	background: #f8fafd;
	border-color: #dbe3f0;
}

.reward-card:hover {
	border-color: #0a2251;
	box-shadow: 0 10px 30px rgba(10, 34, 81, 0.08);
}

.reward-card.is-unlocked {
	background: #eef7f1;
	border-color: #b8e3c4;
}

.reward-badge {
	@apply mb-4 inline-flex items-center gap-2 rounded-full border bg-surface-white px-3 py-1 text-xs font-semibold;
	border-color: #dbe3f0;
	color: #0a2251;
}

.reward-card.is-unlocked .reward-badge {
	@apply bg-white text-green-700;
	border-color: #b8e3c4;
}

.reward-card h3 {
	@apply text-lg font-semibold;
	color: #0a2251;
}

.reward-card p {
	@apply mt-2 text-sm leading-6 text-ink-gray-6;
}

.reward-status {
	@apply shrink-0 rounded-full border bg-surface-white px-3 py-1 text-xs font-semibold;
	border-color: #dbe3f0;
	color: #0a2251;
}

.reward-status.complete {
	@apply border-green-200 bg-green-100 text-green-700;
}

.share-button {
	@apply inline-flex items-center justify-center gap-2 rounded-xl border px-4 py-2.5 text-sm font-semibold transition;
	background: #eef3fb;
	border-color: #d8e2f1;
	color: #0a2251;
}

.share-button:hover {
	background: #e2ebf8;
	border-color: #0a2251;
}

.empty-state {
	@apply flex flex-col items-center justify-center rounded-2xl border border-dashed px-6 py-12 text-center;
	background: #f8fafd;
	border-color: #cbd8ea;
}

.empty-icon {
	@apply mb-4 flex size-14 items-center justify-center rounded-2xl border bg-surface-white;
	border-color: #dbe3f0;
	color: #0a2251;
}

.empty-state h3 {
	@apply text-base font-semibold;
	color: #0a2251;
}

.empty-state p {
	@apply mb-5 mt-2 max-w-md text-sm leading-6 text-ink-gray-6;
}

.ref-status {
	@apply inline-flex w-fit items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold;
}

.ref-status.pending {
	@apply bg-orange-50 text-orange-700;
}

.ref-status.verified {
	@apply bg-green-50 text-green-700;
}
</style>
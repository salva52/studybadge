<template>
	<div
		v-if="isVisible"
		class="fixed bottom-3 left-3 right-3 z-[9999] max-h-[82dvh] overflow-hidden rounded-2xl border border-surface-gray-2/50 bg-white/90 shadow-[0_8px_30px_rgb(0,0,0,0.12)] backdrop-blur-xl transition-all duration-500 ease-out dark:border-white/10 dark:bg-[#0b1730]/90 sm:bottom-5 sm:left-auto sm:right-5 sm:w-[380px] sm:max-w-[calc(100vw-2rem)]"
		role="dialog"
		aria-live="polite"
	>
		<template v-if="!showCelebration">
			<!-- Header -->
			<div class="flex items-start justify-between gap-3 border-b border-surface-gray-2 px-4 py-3 dark:border-surface-gray-6 sm:px-5">
				<div class="flex min-w-0 items-center gap-3">
					<div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-sb-primary/10 to-sb-primary/30 shadow-inner dark:from-sb-primary/20 dark:to-sb-primary/40">
						<component :is="currentStepData.icon" class="h-5 w-5 text-sb-primary drop-shadow-sm" />
					</div>
					<div class="min-w-0">
						<p class="text-[11px] font-semibold uppercase tracking-wide text-sb-primary">
							Tour anti-perdida
						</p>
						<p class="truncate text-xs text-ink-gray-5 dark:text-ink-gray-3">
							Paso {{ currentStep + 1 }} de {{ steps.length }} · {{ currentStepData.label }}
						</p>
					</div>
				</div>

				<button
					@click="dismissTutorial"
					class="rounded-lg p-1.5 text-ink-gray-4 transition-colors hover:bg-surface-gray-2 hover:text-ink-gray-7 dark:hover:bg-surface-gray-6"
					aria-label="Cerrar tutorial"
				>
					<X class="h-4 w-4" />
				</button>
			</div>

			<!-- Content -->
			<div class="max-h-[48dvh] overflow-y-auto px-4 py-4 sm:max-h-[52dvh] sm:px-5">
				<h3 class="mb-2 text-base font-semibold leading-snug text-ink-gray-9 dark:text-ink-gray-1 sm:text-lg">
					{{ currentStepData.title }}
				</h3>
				<p class="text-sm leading-relaxed text-ink-gray-6 dark:text-ink-gray-3">
					{{ currentStepData.description }}
				</p>

				<div class="mt-4 rounded-xl bg-surface-gray-1 px-3 py-2 text-xs leading-relaxed text-ink-gray-5 dark:bg-surface-gray-6 dark:text-ink-gray-3">
					{{ currentStepData.tip }}
				</div>
			</div>

			<!-- Footer -->
			<div class="flex flex-col gap-3 border-t border-surface-gray-2 px-4 py-3 dark:border-surface-gray-6 sm:px-5">
				<!-- Progress indicators -->
				<div class="flex items-center gap-1">
					<div
						v-for="(_, index) in steps"
						:key="index"
						class="h-1.5 flex-1 rounded-full transition-colors duration-300"
						:class="index <= currentStep ? 'bg-sb-primary' : 'bg-surface-gray-3 dark:bg-surface-gray-5'"
					></div>
				</div>

				<!-- Actions -->
				<div class="flex items-center justify-between gap-2">
					<Button
						variant="ghost"
						class="text-ink-gray-5"
						@click="dismissTutorial"
					>
						Saltar tour
					</Button>

					<div class="flex gap-2">
						<Button
							v-if="currentStep > 0"
							variant="outline"
							@click="prevStep"
						>
							Atrás
						</Button>
						<Button
							variant="solid"
							class="transform transition-transform duration-200 hover:scale-105 active:scale-95 shadow-md hover:shadow-lg"
							@click="nextStep"
						>
							{{ currentStep === steps.length - 1 ? 'Terminar tour' : 'Siguiente' }}
						</Button>
					</div>
				</div>
			</div>
		</template>

		<!-- Completion / Easter egg -->
		<template v-else>
			<div class="relative overflow-hidden px-4 py-5 text-center sm:px-5">
				<div class="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
					<span v-for="n in 16" :key="n" class="confetti-piece"></span>
				</div>

				<button
					@click="dismissTutorial"
					class="absolute right-3 top-3 rounded-lg p-1.5 text-ink-gray-4 transition-colors hover:bg-surface-gray-2 hover:text-ink-gray-7 dark:hover:bg-surface-gray-6"
					aria-label="Cerrar bienvenida"
				>
					<X class="h-4 w-4" />
				</button>

				<div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-surface-gray-2 dark:bg-surface-gray-6">
					<PartyPopper class="h-6 w-6 text-sb-primary" />
				</div>

				<h3 class="text-lg font-semibold leading-snug text-ink-gray-9 dark:text-ink-gray-1">
					¡Ya estás dentro de StudyBadge! 🎉
				</h3>
				<p class="mx-auto mt-2 max-w-[300px] text-sm leading-relaxed text-ink-gray-6 dark:text-ink-gray-3">
					Sobreviviste al tutorial. Tu premio: no perderte en la plataforma como NPC en mapa nuevo.
				</p>

				<div class="duck-road my-4 rounded-xl bg-surface-gray-1 px-3 py-2 dark:bg-surface-gray-6" aria-hidden="true">
					<span class="duck-walk">🦆</span>
				</div>

				<div class="mb-4 rounded-xl border border-surface-gray-2 px-3 py-2 text-xs leading-relaxed text-ink-gray-5 dark:border-surface-gray-6 dark:text-ink-gray-3">
					Patito guía aprobado. Ahora sí, a aprender sin sufrir tanto.
				</div>

				<Button variant="solid" class="w-full" @click="dismissTutorial">
					Empezar a explorar
				</Button>
			</div>
		</template>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import {
	X,
	Home,
	Search,
	Bell,
	Gift,
	BookOpen,
	Users,
	Calendar,
	Bot,
	BrainCircuit,
	Mic,
	PartyPopper
} from 'lucide-vue-next'

const isVisible = ref(false)
const showCelebration = ref(false)
const currentStep = ref(0)
const router = useRouter()
const { isLoggedIn } = sessionStore()

const steps = [
	{
		label: 'Inicio',
		title: 'Hola, bienvenida rápida 👋',
		description: 'Sabemos que recién creas la cuenta y seguro odias los tutoriales. Pero míralo un minuto si no quieres perderte la plataforma: somos una plataforma de enseñanza y queremos enseñarte nuestra propia plataforma. Si fallamos en eso… ¿quiénes somos? 😅',
		tip: 'Promesa StudyBadge: corto, claro y sin hacerte sufrir.',
		icon: Home,
		routeName: 'Home'
	},
	{
		label: 'Buscar',
		title: 'Busca sin jugar a las escondidas',
		description: 'Aquí encuentras cursos, temas, grupos o herramientas sin tener que revisar toda la plataforma como detective cansado.',
		tip: 'Cuando no sepas dónde está algo, empieza por Buscar.',
		icon: Search,
		routeName: 'Search'
	},
	{
		label: 'Notificaciones',
		title: 'Tus avisos importantes',
		description: 'En Notificaciones verás recordatorios, respuestas, novedades y cosas que sí importan. Nada de “tu tía comentó una foto de 2014”.',
		tip: 'Revísalo para no perder entregas, mensajes o actualizaciones.',
		icon: Bell,
		routeName: 'Notifications'
	},
	{
		label: 'Referidos',
		title: 'Invita gente y gana beneficios',
		description: 'Comparte StudyBadge con amigos y revisa tus recompensas o beneficios por referir. Aprender con amigos siempre se siente menos castigo.',
		tip: 'Ideal si quieres traer a tu grupo y aprovechar promociones.',
		icon: Gift,
		routeName: 'Referrals'
	},
	{
		label: 'Cursos',
		title: 'Tus cursos viven aquí',
		description: 'Encuentra lecciones, módulos y materiales para avanzar a tu ritmo. Entras, eliges un curso y sigues aprendiendo sin dar mil vueltas.',
		tip: 'Úsalo cuando quieres estudiar algo concreto y tener todo ordenado.',
		icon: BookOpen,
		routeName: 'Courses'
	},
	{
		label: 'Sesiones IA',
		title: 'Habla con tus documentos',
		description: 'Crea una sesión, sube tus archivos y pregúntale a la IA sobre tu propio material. Es como estudiar con alguien que sí leyó el PDF completo.',
		tip: 'Sube apuntes, separatas o lecturas y convierte dudas en respuestas claras.',
		icon: Bot,
		routeName: 'AISessions'
	},
	{
		label: 'Calendario IA',
		title: 'Organiza tu estudio sin drama',
		description: 'Calendario IA te ayuda a ordenar tareas, fechas, sesiones y recordatorios. Básicamente: tu yo del futuro te va a decir “gracias”.',
		tip: 'Perfecto para no acordarte de una entrega cinco minutos antes.',
		icon: Calendar,
		routeName: 'StudyCalendar'
	},
	{
		label: 'Cursos IA',
		title: 'Arma tu plan con IA',
		description: 'Pídele ayuda a la IA para estudiar mejor, crear planes, ordenar temas o practicar lo que estás aprendiendo. Menos caos, más avance real.',
		tip: 'Útil cuando tienes mucho que estudiar y no sabes por dónde empezar.',
		icon: BrainCircuit,
		routeName: 'Study'
	},
	{
		label: 'Grupos',
		title: 'Aprende con más gente',
		description: 'En Grupos puedes conectar con otros estudiantes, seguir actividades compartidas y aprender en comunidad. Estudiar solo está bien, pero acompañado pesa menos.',
		tip: 'Úsalo para clases, retos, comunidades o actividades grupales.',
		icon: Users,
		routeName: 'Groups'
	},
	{
		label: 'Simulaciones IA',
		title: 'Practica antes del momento real',
		description: 'Aquí puedes simular entrevistas, preguntas o situaciones con IA para entrenar. Mejor equivocarte aquí que frente al profe, el reclutador o la vida misma.',
		tip: 'Entrena, mejora y llega con menos cara de “no estudié”.',
		icon: Mic,
		routeName: 'Practice'
	}
]

const currentStepData = computed(() => steps[currentStep.value])

onMounted(() => {
	// Only show for logged in users who haven't seen it yet
	if (isLoggedIn) {
		const hasSeenTutorial = localStorage.getItem('studybadge_has_seen_tutorial')
		if (!hasSeenTutorial) {
			isVisible.value = true
		}
	}
})

const nextStep = () => {
	if (currentStep.value < steps.length - 1) {
		currentStep.value++
		navigateToStep()
	} else {
		finishTutorial()
	}
}

const prevStep = () => {
	if (currentStep.value > 0) {
		currentStep.value--
		navigateToStep()
	}
}

const navigateToStep = () => {
	const routeName = steps[currentStep.value]?.routeName
	if (!routeName) return

	try {
		void router.push({ name: routeName }).catch(() => {})
	} catch {
		// If a route name changes later, the tutorial should not break the app.
	}
}

const finishTutorial = () => {
	showCelebration.value = true
	localStorage.setItem('studybadge_has_seen_tutorial', 'true')
}

const dismissTutorial = () => {
	isVisible.value = false
	localStorage.setItem('studybadge_has_seen_tutorial', 'true')
}
</script>

<style scoped>
.confetti-piece {
	position: absolute;
	top: -18px;
	width: 7px;
	height: 12px;
	border-radius: 3px;
	background: currentColor;
	color: rgb(99 102 241);
	opacity: 0;
	animation: confetti-fall 1.8s ease-in-out infinite;
}

.confetti-piece:nth-child(1) { left: 6%; animation-delay: 0s; color: rgb(236 72 153); }
.confetti-piece:nth-child(2) { left: 14%; animation-delay: .15s; color: rgb(34 197 94); }
.confetti-piece:nth-child(3) { left: 22%; animation-delay: .35s; color: rgb(59 130 246); }
.confetti-piece:nth-child(4) { left: 31%; animation-delay: .05s; color: rgb(245 158 11); }
.confetti-piece:nth-child(5) { left: 39%; animation-delay: .4s; color: rgb(168 85 247); }
.confetti-piece:nth-child(6) { left: 48%; animation-delay: .2s; color: rgb(20 184 166); }
.confetti-piece:nth-child(7) { left: 57%; animation-delay: .55s; color: rgb(239 68 68); }
.confetti-piece:nth-child(8) { left: 65%; animation-delay: .1s; color: rgb(99 102 241); }
.confetti-piece:nth-child(9) { left: 73%; animation-delay: .3s; color: rgb(34 197 94); }
.confetti-piece:nth-child(10) { left: 81%; animation-delay: .6s; color: rgb(245 158 11); }
.confetti-piece:nth-child(11) { left: 89%; animation-delay: .25s; color: rgb(59 130 246); }
.confetti-piece:nth-child(12) { left: 96%; animation-delay: .45s; color: rgb(236 72 153); }
.confetti-piece:nth-child(13) { left: 18%; animation-delay: .7s; color: rgb(20 184 166); }
.confetti-piece:nth-child(14) { left: 52%; animation-delay: .8s; color: rgb(168 85 247); }
.confetti-piece:nth-child(15) { left: 70%; animation-delay: .75s; color: rgb(239 68 68); }
.confetti-piece:nth-child(16) { left: 34%; animation-delay: .65s; color: rgb(99 102 241); }

.duck-road {
	position: relative;
	height: 38px;
	overflow: hidden;
}

.duck-walk {
	position: absolute;
	left: 0;
	top: 7px;
	font-size: 22px;
	animation: duck-walk 3.2s ease-in-out infinite;
}

@keyframes confetti-fall {
	0% {
		transform: translateY(-20px) rotate(0deg);
		opacity: 0;
	}
	15% {
		opacity: 1;
	}
	100% {
		transform: translateY(230px) rotate(260deg);
		opacity: 0;
	}
}

@keyframes duck-walk {
	0% {
		transform: translateX(-40px) rotate(-3deg);
	}
	50% {
		transform: translateX(150px) rotate(4deg);
	}
	100% {
		transform: translateX(330px) rotate(-3deg);
	}
}
</style>

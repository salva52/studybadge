<template>
	<div
		v-if="isVisible"
		class="fixed bottom-3 left-3 right-3 z-[9999] max-h-[78dvh] overflow-y-auto rounded-2xl border border-surface-gray-2 bg-surface-white shadow-xl transition-all duration-300 dark:border-surface-gray-6 dark:bg-surface-gray-7 sm:bottom-5 sm:left-auto sm:right-5 sm:w-[360px] sm:max-w-[calc(100vw-2rem)]"
		role="dialog"
		aria-live="polite"
	>
		<!-- Header -->
		<div class="flex items-start justify-between gap-3 border-b border-surface-gray-2 px-4 py-3 dark:border-surface-gray-6 sm:px-5">
			<div class="flex min-w-0 items-center gap-3">
				<div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-surface-gray-2 dark:bg-surface-gray-6">
					<component :is="currentStepData.icon" class="h-5 w-5 text-sb-primary" />
				</div>
				<div class="min-w-0">
					<p class="text-[11px] font-semibold uppercase tracking-wide text-sb-primary">
						Guía rápida
					</p>
					<p class="truncate text-p-sm text-ink-gray-5">
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
		<div class="px-4 py-4 sm:px-5">
			<h3 class="mb-2 text-lg font-semibold leading-snug text-ink-gray-9 dark:text-ink-gray-1">
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
			<div class="flex items-center gap-1.5">
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
					Saltar
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
						@click="nextStep"
					>
						{{ currentStep === steps.length - 1 ? 'Listo, ya soy pro' : 'Siguiente' }}
					</Button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import {
	X,
	Sparkles,
	BookOpen,
	Users,
	Calendar,
	Bot,
	BrainCircuit,
	Mic
} from 'lucide-vue-next'

const isVisible = ref(false)
const currentStep = ref(0)
const router = useRouter()
const { isLoggedIn } = sessionStore()

const steps = [
	{
		label: 'Bienvenida',
		title: 'Hola, bienvenida rápida 👋',
		description: 'Sabemos que recién creas tu cuenta y probablemente odias los tutoriales. Pero míralo un minuto: si somos una plataforma de enseñanza y no sabemos enseñarte nuestra propia plataforma… ¿quiénes somos? 😅',
		tip: 'Promesa StudyBadge: corto, claro y sin hacerte sufrir.',
		icon: Sparkles,
		routeName: 'Home'
	},
	{
		label: 'Cursos',
		title: 'Tus cursos viven aquí',
		description: 'Encuentra lecciones, módulos y materiales para avanzar a tu ritmo. Entras, eliges un curso y sigues aprendiendo sin dar mil vueltas.',
		tip: 'Ideal cuando quieres estudiar algo concreto y tener todo ordenado.',
		icon: BookOpen,
		routeName: 'Courses'
	},
	{
		label: 'Grupos',
		title: 'Aprende con más gente',
		description: 'Únete a grupos o cohortes, revisa actividades y mantente conectado con otros estudiantes. Aprender solo está bien, pero con comunidad duele menos.',
		tip: 'Úsalo para seguir clases, retos o actividades compartidas.',
		icon: Users,
		routeName: 'Groups'
	},
	{
		label: 'Calendario',
		title: 'Que no se te pase nada',
		description: 'Aquí puedes organizar fechas importantes, entregas, clases y recordatorios. Básicamente: tu yo del futuro te lo va a agradecer.',
		tip: 'Perfecto para no acordarte de una entrega cinco minutos antes.',
		icon: Calendar,
		routeName: 'StudyCalendar'
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
		label: 'Estudio IA',
		title: 'Arma tu plan con IA',
		description: 'Crea planes de estudio, cursos y materiales adaptados a lo que necesitas aprender. Menos caos, más avance real.',
		tip: 'Útil cuando no sabes por dónde empezar o tienes mucho por estudiar.',
		icon: BrainCircuit,
		routeName: 'Study'
	},
	{
		label: 'Práctica',
		title: 'Practica antes del momento real',
		description: 'Simula entrevistas o preguntas con IA para entrenar tus respuestas. Así llegas más preparado y con menos cara de “no estudié”.',
		tip: 'Entrena, equivócate aquí y mejora antes de que importe.',
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
		dismissTutorial()
	}
}

const prevStep = () => {
	if (currentStep.value > 0) {
		currentStep.value--
		navigateToStep()
	}
}

const navigateToStep = () => {
	const routeName = steps[currentStep.value].routeName
	if (routeName) {
		router.push({ name: routeName })
	}
}

const dismissTutorial = () => {
	isVisible.value = false
	localStorage.setItem('studybadge_has_seen_tutorial', 'true')
}
</script>

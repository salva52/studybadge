<template>
	<div class="min-h-screen bg-surface-gray-1">
		<div class="mx-auto flex w-full max-w-[1440px] flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
			<header class="grid gap-4 border-b border-outline-gray-1 pb-5 lg:grid-cols-[1.15fr_0.85fr]">
				<div class="flex min-w-0 flex-col gap-3">
					<div class="flex flex-wrap items-center gap-2">
						<span class="rounded bg-surface-blue-2 px-2 py-1 text-xs font-medium text-ink-blue-3">
							{{ __('Nuevo espacio') }}
						</span>
						<span class="text-sm text-ink-gray-6">{{ __('Estudio con TutorIA') }}</span>
					</div>
					<div>
						<h1 class="text-3xl font-semibold tracking-normal text-ink-gray-9 sm:text-4xl">
							{{ __('Estudio IA') }}
						</h1>
						<p class="mt-2 max-w-3xl text-base leading-7 text-ink-gray-7">
							{{
								__(
									'Convierte tu temario, apuntes o dudas en un plan de estudio, explicaciones guiadas, práctica, flashcards y simulacros.'
								)
							}}
						</p>
					</div>
				</div>
				<div class="grid grid-cols-3 gap-2 rounded-lg border border-outline-gray-1 bg-surface-white p-3 shadow-sm">
					<div v-for="metric in metrics" :key="metric.label" class="rounded-md bg-surface-gray-1 px-3 py-2">
						<div class="text-xs text-ink-gray-6">{{ metric.label }}</div>
						<div class="mt-1 text-xl font-semibold text-ink-gray-9">{{ metric.value }}</div>
					</div>
				</div>
			</header>

			<section class="grid gap-4 lg:grid-cols-[360px_1fr]">
				<aside class="flex flex-col gap-4">
					<div class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
						<div class="flex items-center justify-between gap-3">
							<div>
								<h2 class="text-base font-semibold text-ink-gray-9">{{ __('Objetivo') }}</h2>
								<p class="mt-1 text-sm text-ink-gray-6">{{ __('Elige el modo y pega tu material.') }}</p>
							</div>
							<Tooltip :text="__('Reiniciar')">
								<button
									class="grid h-9 w-9 place-items-center rounded-md text-ink-gray-7 hover:bg-surface-gray-2"
									@click="resetWorkspace"
								>
									<RotateCcw class="h-4 w-4 stroke-1.5" />
								</button>
							</Tooltip>
						</div>

						<div class="mt-4 grid grid-cols-2 gap-2">
							<button
								v-for="goal in goals"
								:key="goal.id"
								class="flex min-h-20 flex-col justify-between rounded-md border p-3 text-left transition"
								:class="
									studyGoal === goal.id
										? 'border-blue-500 bg-surface-blue-1 text-ink-blue-4'
										: 'border-outline-gray-1 bg-surface-white text-ink-gray-8 hover:bg-surface-gray-1'
								"
								@click="studyGoal = goal.id"
							>
								<component :is="goal.icon" class="h-4 w-4 stroke-1.5" />
								<span class="text-sm font-medium leading-5">{{ goal.label }}</span>
							</button>
						</div>

						<div class="mt-4 grid gap-3">
							<FormControl
								v-model="subject"
								:label="__('Curso o tema')"
								:placeholder="__('Ej. Cálculo II, anatomía, finanzas')"
							/>
							<FormControl
								v-model="examDate"
								type="date"
								:label="__('Fecha objetivo')"
							/>
							<div>
								<label class="mb-1 block text-sm text-ink-gray-7">{{ __('Nivel') }}</label>
								<select
									v-model="studentLevel"
									class="w-full rounded-md border border-outline-gray-2 bg-surface-white px-3 py-2 text-sm text-ink-gray-8 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
								>
									<option value="colegio">{{ __('Colegio') }}</option>
									<option value="preuniversitario">{{ __('Preuniversitario') }}</option>
									<option value="universitario">{{ __('Universitario') }}</option>
									<option value="profesional">{{ __('Profesional') }}</option>
								</select>
							</div>
							<div>
								<label class="mb-1 block text-sm text-ink-gray-7">{{ __('Temario, apuntes o consigna') }}</label>
								<textarea
									v-model="sourceMaterial"
									rows="9"
									class="w-full resize-y rounded-md border border-outline-gray-2 bg-surface-white px-3 py-2 text-sm leading-6 text-ink-gray-8 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
									:placeholder="__('Pega aquí sílabos, temas del parcial, apuntes, preguntas o lo que necesitas estudiar.')"
								/>
							</div>
							<div class="grid grid-cols-2 gap-2">
								<Button
									:label="__('Detectar temas')"
									:loading="loadingAction === 'topics'"
									@click="detectTopics"
								>
									<template #prefix>
										<ListChecks class="h-4 w-4 stroke-1.5" />
									</template>
								</Button>
								<Button
									:label="__('Crear plan')"
									variant="solid"
									:loading="loadingAction === 'plan'"
									@click="generatePlan"
								>
									<template #prefix>
										<CalendarDays class="h-4 w-4 stroke-1.5" />
									</template>
								</Button>
							</div>
						</div>
					</div>

					<div class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
						<div class="flex items-center justify-between gap-3">
							<h2 class="text-base font-semibold text-ink-gray-9">{{ __('Temas') }}</h2>
							<button
								class="text-sm font-medium text-ink-blue-3 hover:text-ink-blue-4"
								@click="addManualTopic"
							>
								{{ __('Agregar') }}
							</button>
						</div>
						<div class="mt-3 flex flex-col gap-2">
							<label
								v-for="topic in topics"
								:key="topic.id"
								class="flex cursor-pointer items-start gap-3 rounded-md border border-outline-gray-1 bg-surface-gray-1 p-3"
							>
								<input
									v-model="topic.done"
									type="checkbox"
									class="mt-1 rounded border-outline-gray-3 text-blue-600 focus:ring-blue-500"
									@change="persist"
								/>
								<span class="min-w-0 flex-1 text-sm leading-5 text-ink-gray-8">{{ topic.title }}</span>
							</label>
							<div v-if="!topics.length" class="rounded-md border border-dashed border-outline-gray-2 p-4 text-sm text-ink-gray-6">
								{{ __('Los temas detectados aparecerán aquí.') }}
							</div>
						</div>
					</div>
				</aside>

				<main class="flex min-w-0 flex-col gap-4">
					<nav class="flex flex-wrap gap-2 rounded-lg border border-outline-gray-1 bg-surface-white p-2 shadow-sm">
						<button
							v-for="tab in tabs"
							:key="tab.id"
							class="inline-flex min-h-9 items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition"
							:class="
								activeTab === tab.id
									? 'bg-surface-blue-2 text-ink-blue-4'
									: 'text-ink-gray-7 hover:bg-surface-gray-1'
							"
							@click="activeTab = tab.id"
						>
							<component :is="tab.icon" class="h-4 w-4 stroke-1.5" />
							{{ tab.label }}
						</button>
					</nav>

					<section v-if="activeTab === 'plan'" class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
						<div class="flex flex-wrap items-center justify-between gap-3">
							<div>
								<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Plan de estudio') }}</h2>
								<p class="mt-1 text-sm text-ink-gray-6">{{ __('Organizado según tu objetivo, nivel y tiempo disponible.') }}</p>
							</div>
							<Button
								:label="__('Rehacer plan')"
								:loading="loadingAction === 'plan'"
								@click="generatePlan"
							/>
						</div>
						<div class="mt-4 grid gap-3">
							<div
								v-for="(item, index) in studyPlan"
								:key="item.title + index"
								class="rounded-lg border border-outline-gray-1 p-4"
							>
								<div class="flex flex-wrap items-start justify-between gap-3">
									<div>
										<div class="text-sm font-medium text-ink-blue-3">{{ item.period || __('Bloque') }}</div>
										<h3 class="mt-1 text-base font-semibold text-ink-gray-9">{{ item.title }}</h3>
									</div>
									<span class="rounded bg-surface-gray-2 px-2 py-1 text-xs text-ink-gray-7">
										{{ item.duration || __('Flexible') }}
									</span>
								</div>
								<p class="mt-2 text-sm leading-6 text-ink-gray-7">{{ item.objective }}</p>
								<div class="mt-3 flex flex-wrap gap-2">
									<span
										v-for="topic in item.topics"
										:key="topic"
										class="rounded bg-surface-green-1 px-2 py-1 text-xs text-ink-green-3"
									>
										{{ topic }}
									</span>
								</div>
							</div>
							<div v-if="!studyPlan.length" class="rounded-lg border border-dashed border-outline-gray-2 p-8 text-center">
								<CalendarDays class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
								<p class="mt-3 text-sm text-ink-gray-6">{{ __('Crea un plan para ver tu ruta de estudio aquí.') }}</p>
							</div>
						</div>
					</section>

					<section v-if="activeTab === 'learn'" class="grid gap-4 xl:grid-cols-[1fr_360px]">
						<div class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
							<div class="flex flex-wrap items-center justify-between gap-3">
								<div>
									<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Explicación guiada') }}</h2>
									<p class="mt-1 text-sm text-ink-gray-6">{{ __('Elige un tema y genera una explicación con ejemplo.') }}</p>
								</div>
								<Button
									:label="__('Generar')"
									variant="solid"
									:loading="loadingAction === 'explain'"
									@click="generateExplanation"
								>
									<template #prefix>
										<Sparkles class="h-4 w-4 stroke-1.5" />
									</template>
								</Button>
							</div>
							<div class="mt-4 grid gap-3 sm:grid-cols-[1fr_auto]">
								<select
									v-model="selectedTopicId"
									class="rounded-md border border-outline-gray-2 bg-surface-white px-3 py-2 text-sm text-ink-gray-8 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
								>
									<option value="">{{ __('Selecciona un tema') }}</option>
									<option v-for="topic in topics" :key="topic.id" :value="topic.id">
										{{ topic.title }}
									</option>
								</select>
								<Button :label="__('Marcar aprendido')" @click="markSelectedTopicDone">
									<template #prefix>
										<CheckCircle2 class="h-4 w-4 stroke-1.5" />
									</template>
								</Button>
							</div>
							<div class="study-markdown mt-5 rounded-lg border border-outline-gray-1 bg-surface-gray-1 p-4" v-html="renderMarkdown(explanation)" />
						</div>

						<div class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
							<h2 class="text-base font-semibold text-ink-gray-9">{{ __('Flashcards') }}</h2>
							<p class="mt-1 text-sm text-ink-gray-6">{{ __('Tarjetas rápidas del tema seleccionado.') }}</p>
							<Button
								class="mt-3 w-full"
								:label="__('Crear flashcards')"
								:loading="loadingAction === 'flashcards'"
								@click="generateFlashcards"
							/>
							<div class="mt-4 flex flex-col gap-3">
								<button
									v-for="card in flashcards"
									:key="card.id"
									class="rounded-lg border border-outline-gray-1 bg-surface-gray-1 p-3 text-left"
									@click="card.open = !card.open"
								>
									<div class="text-sm font-medium text-ink-gray-9">{{ card.front }}</div>
									<div v-if="card.open" class="mt-2 text-sm leading-6 text-ink-gray-7">{{ card.back }}</div>
								</button>
							</div>
						</div>
					</section>

					<section v-if="activeTab === 'practice'" class="grid gap-4 xl:grid-cols-[1fr_360px]">
						<div class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
							<div class="flex flex-wrap items-center justify-between gap-3">
								<div>
									<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Práctica y simulacro') }}</h2>
									<p class="mt-1 text-sm text-ink-gray-6">{{ __('Genera ejercicios tipo parcial y recibe feedback inmediato.') }}</p>
								</div>
								<div class="flex gap-2">
									<Button :label="__('Práctica')" :loading="loadingAction === 'practice'" @click="generatePractice" />
									<Button :label="__('Quiz')" variant="solid" :loading="loadingAction === 'quiz'" @click="generateQuiz" />
								</div>
							</div>

							<div class="mt-4 flex flex-col gap-3">
								<div
									v-for="(exercise, index) in exercises"
									:key="exercise.id"
									class="rounded-lg border border-outline-gray-1 p-4"
								>
									<div class="text-sm font-semibold text-ink-gray-9">
										{{ index + 1 }}. {{ exercise.question }}
									</div>
									<div class="mt-3 grid gap-2">
										<button
											v-for="(option, optionIndex) in exercise.options"
											:key="option"
											class="rounded-md border px-3 py-2 text-left text-sm transition"
											:class="answerClass(exercise, optionIndex)"
											@click="answerExercise(exercise, optionIndex)"
										>
											{{ option }}
										</button>
									</div>
									<div v-if="exercise.selected !== null" class="mt-3 rounded-md bg-surface-gray-1 p-3 text-sm leading-6 text-ink-gray-7">
										{{ exercise.explanation }}
									</div>
								</div>
								<div v-if="!exercises.length" class="rounded-lg border border-dashed border-outline-gray-2 p-8 text-center">
									<ClipboardCheck class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
									<p class="mt-3 text-sm text-ink-gray-6">{{ __('Tus ejercicios aparecerán aquí.') }}</p>
								</div>
							</div>
						</div>

						<div class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
							<h2 class="text-base font-semibold text-ink-gray-9">{{ __('Notas de estudio') }}</h2>
							<p class="mt-1 text-sm text-ink-gray-6">{{ __('Pizarra simple para fórmulas, dudas y repasos.') }}</p>
							<textarea
								v-model="studyNotes"
								rows="16"
								class="mt-3 w-full resize-y rounded-md border border-outline-gray-2 bg-surface-gray-1 px-3 py-2 text-sm leading-6 text-ink-gray-8 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
								:placeholder="__('Escribe tus notas, errores frecuentes o fórmulas clave.')"
								@input="persist"
							/>
						</div>
					</section>

					<section v-if="activeTab === 'chat'" class="grid gap-4 xl:grid-cols-[1fr_360px]">
						<div class="flex h-[680px] flex-col rounded-lg border border-outline-gray-1 bg-surface-white shadow-sm">
							<div class="border-b border-outline-gray-1 p-4">
								<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Tutor de estudio') }}</h2>
								<p class="mt-1 text-sm text-ink-gray-6">{{ __('Pregunta sobre tu temario, tus ejercicios o tu estrategia para el parcial.') }}</p>
							</div>
							<div ref="chatScroller" class="flex-1 overflow-y-auto bg-surface-gray-1 p-4">
								<div class="flex flex-col gap-3">
									<div
										v-for="message in chatMessages"
										:key="message.id"
										class="max-w-[86%] rounded-lg px-4 py-3 text-sm leading-6 shadow-sm"
										:class="
											message.role === 'user'
												? 'self-end bg-surface-blue-2 text-ink-blue-4'
												: 'self-start border border-outline-gray-1 bg-surface-white text-ink-gray-8'
										"
										v-html="renderMarkdown(message.content)"
									/>
									<div v-if="loadingAction === 'chat'" class="self-start rounded-lg border border-outline-gray-1 bg-surface-white px-4 py-3 text-sm text-ink-gray-6">
										{{ __('TutorIA está pensando...') }}
									</div>
								</div>
							</div>
							<div class="border-t border-outline-gray-1 p-4">
								<div class="flex gap-2">
									<textarea
										v-model="chatInput"
										rows="2"
										class="min-h-11 flex-1 resize-none rounded-md border border-outline-gray-2 px-3 py-2 text-sm leading-5 text-ink-gray-8 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
										:placeholder="__('Pregunta algo o pide un repaso express.')"
										@keydown.enter.exact.prevent="sendChat"
									/>
									<Button variant="solid" :disabled="!chatInput.trim()" @click="sendChat">
										<template #icon>
											<SendHorizontal class="h-4 w-4 stroke-1.5" />
										</template>
									</Button>
								</div>
							</div>
						</div>

						<div class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
							<h2 class="text-base font-semibold text-ink-gray-9">{{ __('Prompts rápidos') }}</h2>
							<div class="mt-3 flex flex-col gap-2">
								<button
									v-for="prompt in quickPrompts"
									:key="prompt"
									class="rounded-md border border-outline-gray-1 bg-surface-gray-1 px-3 py-2 text-left text-sm leading-5 text-ink-gray-8 hover:bg-surface-gray-2"
									@click="chatInput = prompt"
								>
									{{ prompt }}
								</button>
							</div>
						</div>
					</section>

					<section v-if="activeTab === 'history'" class="rounded-lg border border-outline-gray-1 bg-surface-white p-4 shadow-sm">
						<div class="flex flex-wrap items-center justify-between gap-3">
							<div>
								<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Historial y estadísticas') }}</h2>
								<p class="mt-1 text-sm text-ink-gray-6">{{ __('Registro local de tus sesiones de estudio en este navegador.') }}</p>
							</div>
							<Button :label="__('Guardar sesión')" @click="saveSessionSnapshot">
								<template #prefix>
									<Save class="h-4 w-4 stroke-1.5" />
								</template>
							</Button>
						</div>
						<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
							<div
								v-for="entry in history"
								:key="entry.id"
								class="rounded-lg border border-outline-gray-1 p-4"
							>
								<div class="text-sm font-semibold text-ink-gray-9">{{ entry.subject || __('Sesión de estudio') }}</div>
								<div class="mt-1 text-xs text-ink-gray-6">{{ formatDate(entry.createdAt) }}</div>
								<div class="mt-3 grid grid-cols-3 gap-2 text-center">
									<div class="rounded bg-surface-gray-1 p-2">
										<div class="text-base font-semibold text-ink-gray-9">{{ entry.topics }}</div>
										<div class="text-xs text-ink-gray-6">{{ __('Temas') }}</div>
									</div>
									<div class="rounded bg-surface-gray-1 p-2">
										<div class="text-base font-semibold text-ink-gray-9">{{ entry.score }}%</div>
										<div class="text-xs text-ink-gray-6">{{ __('Quiz') }}</div>
									</div>
									<div class="rounded bg-surface-gray-1 p-2">
										<div class="text-base font-semibold text-ink-gray-9">{{ entry.cards }}</div>
										<div class="text-xs text-ink-gray-6">{{ __('Cards') }}</div>
									</div>
								</div>
							</div>
						</div>
						<div v-if="!history.length" class="mt-4 rounded-lg border border-dashed border-outline-gray-2 p-8 text-center">
							<History class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
							<p class="mt-3 text-sm text-ink-gray-6">{{ __('Guarda una sesión para empezar tu historial.') }}</p>
						</div>
					</section>
				</main>
			</section>
		</div>
	</div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { Button, FormControl, Tooltip, call, toast } from 'frappe-ui'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import {
	BookOpen,
	Brain,
	CalendarDays,
	CheckCircle2,
	ClipboardCheck,
	FileQuestion,
	GraduationCap,
	History,
	Layers,
	ListChecks,
	MessageSquareText,
	NotebookPen,
	RotateCcw,
	Save,
	SendHorizontal,
	Sparkles,
	Target,
} from 'lucide-vue-next'

const STORAGE_KEY = 'studybadge_study_workspace'
const HISTORY_KEY = 'studybadge_study_history'

const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true })

const goals = [
	{ id: 'parcial', label: __('Parcial / Final'), icon: FileQuestion },
	{ id: 'admision', label: __('Admisión'), icon: GraduationCap },
	{ id: 'repaso', label: __('Recordar'), icon: Brain },
	{ id: 'curso', label: __('Curso'), icon: BookOpen },
]

const tabs = [
	{ id: 'plan', label: __('Plan'), icon: CalendarDays },
	{ id: 'learn', label: __('Aprender'), icon: NotebookPen },
	{ id: 'practice', label: __('Practicar'), icon: ClipboardCheck },
	{ id: 'chat', label: __('Tutor'), icon: MessageSquareText },
	{ id: 'history', label: __('Historial'), icon: History },
]

const quickPrompts = [
	__('Explícame este tema como si me fuera a tomar un parcial mañana.'),
	__('Hazme 5 preguntas difíciles sobre mis temas y corrige mis respuestas.'),
	__('Resume mis apuntes en conceptos clave, fórmulas y errores frecuentes.'),
	__('Crea una estrategia de repaso para hoy con bloques de 25 minutos.'),
]

const activeTab = ref('plan')
const studyGoal = ref('parcial')
const subject = ref('')
const examDate = ref('')
const studentLevel = ref('universitario')
const sourceMaterial = ref('')
const topics = ref([])
const selectedTopicId = ref('')
const studyPlan = ref([])
const explanation = ref('')
const flashcards = ref([])
const exercises = ref([])
const studyNotes = ref('')
const chatMessages = ref([
	{
		id: Date.now(),
		role: 'assistant',
		content: __('Hola, soy TutorIA. Pega tu temario o cuéntame qué parcial estás preparando y armamos el estudio.'),
	},
])
const chatInput = ref('')
const history = ref([])
const loadingAction = ref('')
const chatScroller = ref(null)

const completedCount = computed(() => topics.value.filter((topic) => topic.done).length)
const quizScore = computed(() => {
	const answered = exercises.value.filter((exercise) => exercise.selected !== null)
	if (!answered.length) return 0
	const correct = answered.filter((exercise) => exercise.selected === exercise.correct).length
	return Math.round((correct / answered.length) * 100)
})
const metrics = computed(() => [
	{ label: __('Temas'), value: topics.value.length },
	{ label: __('Aprendidos'), value: completedCount.value },
	{ label: __('Quiz'), value: `${quizScore.value}%` },
])

const currentTopic = computed(() => {
	return topics.value.find((topic) => topic.id === selectedTopicId.value) || topics.value[0] || null
})

onMounted(() => {
	restoreWorkspace()
})

watch(
	[
		studyGoal,
		subject,
		examDate,
		studentLevel,
		sourceMaterial,
		topics,
		selectedTopicId,
		studyPlan,
		explanation,
		flashcards,
		exercises,
		studyNotes,
		chatMessages,
	],
	persist,
	{ deep: true }
)

const renderMarkdown = (text) => {
	if (!text) return `<p class="text-sm text-ink-gray-6">${__('Aún no hay contenido generado.')}</p>`
	return DOMPurify.sanitize(markdown.render(String(text)))
}

const makeId = () => `${Date.now()}-${Math.random().toString(16).slice(2)}`

const selectedGoalLabel = () => goals.find((goal) => goal.id === studyGoal.value)?.label || __('Estudiar')

const daysLeft = () => {
	if (!examDate.value) return null
	const today = new Date()
	const target = new Date(`${examDate.value}T23:59:59`)
	return Math.max(1, Math.ceil((target - today) / 86400000))
}

const buildContext = () => {
	const topicText = topics.value.map((topic) => `- ${topic.title}`).join('\n')
	return [
		`Objetivo: ${selectedGoalLabel()}`,
		`Curso o tema: ${subject.value || 'No especificado'}`,
		`Nivel: ${studentLevel.value}`,
		examDate.value ? `Fecha objetivo: ${examDate.value} (${daysLeft()} dias aprox.)` : 'Sin fecha objetivo',
		topicText ? `Temas actuales:\n${topicText}` : '',
		sourceMaterial.value ? `Material del estudiante:\n${sourceMaterial.value}` : '',
		studyNotes.value ? `Notas del estudiante:\n${studyNotes.value}` : '',
	]
		.filter(Boolean)
		.join('\n\n')
}

const askTutor = async (prompt, action) => {
	loadingAction.value = action
	try {
		const response = await call('studybadge_ai.ai_tutor.chat_with_tutor', {
			message: prompt,
			screen_text: buildContext(),
			history: JSON.stringify(
				chatMessages.value.slice(-8).map((message) => ({
					role: message.role === 'assistant' ? 'assistant' : 'user',
					content: message.content,
				}))
			),
		})
		return response?.reply || ''
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo conectar con TutorIA.'))
		return ''
	} finally {
		loadingAction.value = ''
	}
}

const parseJSONBlock = (text, fallback) => {
	if (!text) return fallback
	let value = text.trim()
	const fenced = value.match(/```(?:json)?\s*([\s\S]*?)```/)
	if (fenced) value = fenced[1].trim()
	const startArray = value.indexOf('[')
	const startObject = value.indexOf('{')
	if (startArray >= 0 && (startArray < startObject || startObject === -1)) {
		value = value.slice(startArray)
	} else if (startObject >= 0) {
		value = value.slice(startObject)
	}
	try {
		return JSON.parse(value)
	} catch {
		return fallback
	}
}

const normalizeTopics = (items) => {
	return (Array.isArray(items) ? items : [])
		.map((item) => (typeof item === 'string' ? item : item?.title || item?.tema || ''))
		.filter(Boolean)
		.slice(0, 14)
		.map((title) => ({
			id: makeId(),
			title,
			done: false,
		}))
}

const detectTopics = async () => {
	if (!sourceMaterial.value.trim() && !subject.value.trim()) {
		toast.warning(__('Agrega un tema o material primero.'))
		return
	}
	const reply = await askTutor(
		`Extrae de este material una lista de 6 a 12 temas concretos para estudiar. Devuelve SOLO JSON array de strings, sin markdown ni explicación.\n\n${buildContext()}`,
		'topics'
	)
	const parsed = parseJSONBlock(reply, [])
	const nextTopics = normalizeTopics(parsed)
	if (!nextTopics.length) {
		toast.error(__('No se pudieron detectar temas. Prueba con más contexto.'))
		return
	}
	topics.value = nextTopics
	selectedTopicId.value = topics.value[0]?.id || ''
	toast.success(__('Temas detectados.'))
}

const generatePlan = async () => {
	if (!topics.value.length) {
		await detectTopics()
		if (!topics.value.length) return
	}
	const reply = await askTutor(
		`Crea un plan de estudio personalizado para StudyBadge. Devuelve SOLO JSON array. Cada item debe tener:
{
  "period": "Dia 1" o "Semana 1",
  "title": "titulo breve",
  "duration": "tiempo estimado",
  "objective": "objetivo concreto",
  "topics": ["tema 1", "tema 2"]
}

Usa el contexto y ajusta al objetivo ${selectedGoalLabel()}.\n\n${buildContext()}`,
		'plan'
	)
	const parsed = parseJSONBlock(reply, [])
	if (!Array.isArray(parsed) || !parsed.length) {
		toast.error(__('No se pudo generar el plan.'))
		return
	}
	studyPlan.value = parsed.slice(0, 14).map((item, index) => ({
		period: item.period || item.week || item.day || `${__('Bloque')} ${index + 1}`,
		title: item.title || item.objective || `${__('Sesión')} ${index + 1}`,
		duration: item.duration || item.hours || '',
		objective: item.objective || item.tip || '',
		topics: Array.isArray(item.topics) ? item.topics.slice(0, 5) : [],
	}))
	activeTab.value = 'plan'
	toast.success(__('Plan creado.'))
}

const generateExplanation = async () => {
	if (!currentTopic.value) {
		toast.warning(__('Selecciona o detecta un tema primero.'))
		return
	}
	const reply = await askTutor(
		`Explica el tema "${currentTopic.value.title}" para un estudiante de nivel ${studentLevel.value}.
Formato markdown breve:
1. Idea central.
2. Conceptos clave.
3. Ejemplo resuelto paso a paso.
4. Errores frecuentes.
5. Mini checklist para saber si ya lo domina.

Contexto:\n${buildContext()}`,
		'explain'
	)
	if (reply) explanation.value = reply
}

const generateFlashcards = async () => {
	if (!currentTopic.value) {
		toast.warning(__('Selecciona un tema primero.'))
		return
	}
	const reply = await askTutor(
		`Crea 8 flashcards sobre "${currentTopic.value.title}". Devuelve SOLO JSON array con objetos {"front":"pregunta/concepto","back":"respuesta breve"}.\n\n${buildContext()}`,
		'flashcards'
	)
	const parsed = parseJSONBlock(reply, [])
	flashcards.value = (Array.isArray(parsed) ? parsed : [])
		.slice(0, 12)
		.map((card) => ({
			id: makeId(),
			front: card.front || card.question || '',
			back: card.back || card.answer || '',
			open: false,
		}))
		.filter((card) => card.front && card.back)
	if (!flashcards.value.length) toast.error(__('No se pudieron crear flashcards.'))
}

const normalizeExercises = (items) => {
	return (Array.isArray(items) ? items : [])
		.slice(0, 10)
		.map((item) => {
			const options = Array.isArray(item.options) ? item.options.filter(Boolean).slice(0, 4) : []
			return {
				id: makeId(),
				question: item.question || item.pregunta || '',
				options,
				correct: Math.max(0, Math.min(Number(item.correct ?? item.answerIndex ?? 0), Math.max(options.length - 1, 0))),
				explanation: item.explanation || item.explicacion || '',
				selected: null,
			}
		})
		.filter((item) => item.question && item.options.length >= 2)
}

const generatePractice = async () => {
	const reply = await askTutor(
		`Genera 5 ejercicios de practica tipo ${selectedGoalLabel()} sobre estos temas. Devuelve SOLO JSON array con {"question":"...","options":["A","B","C","D"],"correct":0,"explanation":"..."}.\n\n${buildContext()}`,
		'practice'
	)
	exercises.value = normalizeExercises(parseJSONBlock(reply, []))
	if (!exercises.value.length) toast.error(__('No se pudo crear práctica.'))
}

const generateQuiz = async () => {
	const reply = await askTutor(
		`Genera un simulacro de 8 preguntas tipo ${selectedGoalLabel()} con dificultad realista. Devuelve SOLO JSON array con {"question":"...","options":["A","B","C","D"],"correct":0,"explanation":"..."}.\n\n${buildContext()}`,
		'quiz'
	)
	exercises.value = normalizeExercises(parseJSONBlock(reply, []))
	if (!exercises.value.length) toast.error(__('No se pudo crear el quiz.'))
}

const answerExercise = (exercise, optionIndex) => {
	exercise.selected = optionIndex
	persist()
}

const answerClass = (exercise, optionIndex) => {
	if (exercise.selected === null) return 'border-outline-gray-1 bg-surface-white hover:bg-surface-gray-1 text-ink-gray-8'
	if (optionIndex === exercise.correct) return 'border-green-500 bg-surface-green-1 text-ink-green-4'
	if (optionIndex === exercise.selected) return 'border-red-400 bg-surface-red-1 text-ink-red-4'
	return 'border-outline-gray-1 bg-surface-white text-ink-gray-6'
}

const sendChat = async () => {
	const text = chatInput.value.trim()
	if (!text || loadingAction.value) return
	chatInput.value = ''
	chatMessages.value.push({ id: makeId(), role: 'user', content: text })
	await nextTick(scrollChat)
	const reply = await askTutor(text, 'chat')
	if (reply) {
		chatMessages.value.push({ id: makeId(), role: 'assistant', content: reply })
		await nextTick(scrollChat)
	}
}

const scrollChat = () => {
	if (chatScroller.value) chatScroller.value.scrollTop = chatScroller.value.scrollHeight
}

const markSelectedTopicDone = () => {
	if (!currentTopic.value) return
	currentTopic.value.done = true
	persist()
}

const addManualTopic = () => {
	const title = window.prompt(__('Nuevo tema'))
	if (!title?.trim()) return
	topics.value.push({ id: makeId(), title: title.trim(), done: false })
	if (!selectedTopicId.value) selectedTopicId.value = topics.value[0].id
}

const saveSessionSnapshot = () => {
	const entry = {
		id: makeId(),
		createdAt: new Date().toISOString(),
		subject: subject.value,
		topics: topics.value.length,
		score: quizScore.value,
		cards: flashcards.value.length,
	}
	history.value = [entry, ...history.value].slice(0, 12)
	localStorage.setItem(HISTORY_KEY, JSON.stringify(history.value))
	toast.success(__('Sesión guardada.'))
}

const formatDate = (value) => {
	return new Intl.DateTimeFormat(undefined, {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	}).format(new Date(value))
}

function persist() {
	const payload = {
		studyGoal: studyGoal.value,
		subject: subject.value,
		examDate: examDate.value,
		studentLevel: studentLevel.value,
		sourceMaterial: sourceMaterial.value,
		topics: topics.value,
		selectedTopicId: selectedTopicId.value,
		studyPlan: studyPlan.value,
		explanation: explanation.value,
		flashcards: flashcards.value,
		exercises: exercises.value,
		studyNotes: studyNotes.value,
		chatMessages: chatMessages.value,
	}
	localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
}

function restoreWorkspace() {
	try {
		const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
		studyGoal.value = saved.studyGoal || studyGoal.value
		subject.value = saved.subject || ''
		examDate.value = saved.examDate || ''
		studentLevel.value = saved.studentLevel || studentLevel.value
		sourceMaterial.value = saved.sourceMaterial || ''
		topics.value = saved.topics || []
		selectedTopicId.value = saved.selectedTopicId || topics.value[0]?.id || ''
		studyPlan.value = saved.studyPlan || []
		explanation.value = saved.explanation || ''
		flashcards.value = saved.flashcards || []
		exercises.value = saved.exercises || []
		studyNotes.value = saved.studyNotes || ''
		if (saved.chatMessages?.length) chatMessages.value = saved.chatMessages
	} catch {
		// Ignore invalid local workspace state.
	}

	try {
		history.value = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]')
	} catch {
		history.value = []
	}
}

function resetWorkspace() {
	subject.value = ''
	examDate.value = ''
	sourceMaterial.value = ''
	topics.value = []
	selectedTopicId.value = ''
	studyPlan.value = []
	explanation.value = ''
	flashcards.value = []
	exercises.value = []
	studyNotes.value = ''
	chatMessages.value = [
		{
			id: makeId(),
			role: 'assistant',
			content: __('Listo. Empecemos de nuevo con otro temario o parcial.'),
		},
	]
	persist()
}
</script>

<style scoped>
.study-markdown :deep(h1),
.study-markdown :deep(h2),
.study-markdown :deep(h3) {
	margin: 0.75rem 0 0.4rem;
	font-weight: 650;
	color: theme('colors.gray.900');
}

.study-markdown :deep(p),
.study-markdown :deep(li) {
	font-size: 0.925rem;
	line-height: 1.7;
	color: theme('colors.gray.700');
}

.study-markdown :deep(ul),
.study-markdown :deep(ol) {
	margin: 0.5rem 0 0.75rem 1.25rem;
}

.study-markdown :deep(strong) {
	color: theme('colors.gray.900');
}
</style>

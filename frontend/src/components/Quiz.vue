<template>
	<div v-if="quiz.data">
		<div v-if="quiz.data.duration && activeQuestion > 0 && !quizSubmission.data" class="flex flex-col gap-x-1 my-4 px-2">
			<div class="mb-2">
				<span class="text-ink-gray-9"> {{ __('Tiempo restante') }}: </span>
				<span class="font-semibold text-ink-gray-9" :class="{'text-red-500': timer < 60}">
					{{ formatTimer(timer) }}
				</span>
			</div>
			<ProgressBar :progress="timerProgress" />
		</div>

		<div v-if="activeQuestion == 0" class="mb-6">
			<div class="relative overflow-hidden bg-gradient-to-br from-white to-blue-50 dark:from-gray-800 dark:to-gray-900 shadow-sb-soft border border-gray-100 dark:border-gray-700 rounded-2xl p-6 md:p-8 text-center">
				<div class="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-blue-500 opacity-5 rounded-full blur-3xl pointer-events-none"></div>
				<div class="absolute bottom-0 left-0 -mb-10 -ml-10 w-32 h-32 bg-indigo-500 opacity-5 rounded-full blur-2xl pointer-events-none"></div>

				<div class="relative z-10">
					<div class="inline-flex bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 p-3 rounded-xl mb-4 shadow-sm">
						<ClipboardList class="w-8 h-8 stroke-1.5" />
					</div>
					<h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
						{{ quiz.data.title }}
					</h1>
					<p class="text-base text-gray-600 dark:text-gray-400 max-w-xl mx-auto mb-6 leading-relaxed">
						{{ __('Por favor, lee las siguientes instrucciones cuidadosamente antes de comenzar el cuestionario.') }}
					</p>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-3xl mx-auto text-left mb-8">
						<div class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-300">
							<div class="flex items-center gap-3 mb-2 text-amber-500">
								<AlertTriangle class="w-5 h-5" />
								<h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ __('¡Importante!') }}</h3>
							</div>
							<p class="text-sm text-gray-600 dark:text-gray-400">
								{{ __('No recargues la página ni cierres esta ventana. Si lo haces, el cuestionario se enviará automáticamente.') }}
							</p>
						</div>

						<div class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-300">
							<div class="flex items-center gap-3 mb-2 text-blue-500">
								<ListOrdered class="w-5 h-5" />
								<h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ __('Formato') }}</h3>
							</div>
							<p class="text-sm text-gray-600 dark:text-gray-400">
								{{ __('Este cuestionario consta de {0} preguntas.').format(questions.length) }}
							</p>
						</div>

						<div v-if="quiz.data?.duration" class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-300">
							<div class="flex items-center gap-3 mb-2 text-indigo-500">
								<Clock class="w-5 h-5" />
								<h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ __('Tiempo Límite') }}</h3>
							</div>
							<p class="text-sm text-gray-600 dark:text-gray-400">
								{{ __('Cuentas con {0} minutos para resolverlo. Al finalizar el tiempo, se enviará automáticamente.').format(quiz.data.duration) }}
							</p>
						</div>

						<div v-if="quiz.data.passing_percentage" class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-300">
							<div class="flex items-center gap-3 mb-2 text-emerald-500">
								<Target class="w-5 h-5" />
								<h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ __('Aprobación') }}</h3>
							</div>
							<p class="text-sm text-gray-600 dark:text-gray-400">
								{{ __('Tendrás que obtener un {0}% de respuestas correctas para aprobar.').format(quiz.data.passing_percentage) }}
							</p>
						</div>

						<div v-if="quiz.data.max_attempts" class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-300">
							<div class="flex items-center gap-3 mb-2 text-purple-500">
								<RotateCcw class="w-5 h-5" />
								<h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ __('Intentos') }}</h3>
							</div>
							<p class="text-sm text-gray-600 dark:text-gray-400">
								{{ __('Puedes intentar este cuestionario un máximo de {0}').format(
									quiz.data.max_attempts == 1
										? '1 vez'
										: `${quiz.data.max_attempts} veces`
								) }}
							</p>
						</div>
						
						<div v-if="quiz.data.enable_negative_marking" class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-300">
							<div class="flex items-center gap-3 mb-2 text-rose-500">
								<MinusCircle class="w-5 h-5" />
								<h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ __('Penalizaciones') }}</h3>
							</div>
							<p class="text-sm text-gray-600 dark:text-gray-400">
								{{ __('Se restarán {0} {1} de tu puntaje por cada respuesta incorrecta.').format(
									quiz.data.marks_to_cut,
									quiz.data.marks_to_cut == 1 ? 'punto' : 'puntos'
								) }}
							</p>
						</div>
					</div>

					<div class="flex flex-col sm:flex-row items-center justify-center gap-3">
						<Button
							v-if="!quiz.data.max_attempts || attempts.data?.length < quiz.data.max_attempts"
							variant="solid"
							class="px-8 py-2.5 text-base font-semibold shadow-md shadow-blue-500/20 hover:shadow-blue-500/40 transition-all transform hover:-translate-y-0.5 rounded-xl"
							@click="startQuiz"
						>
							<span>{{ inVideo ? __('Iniciar Cuestionario') : __('Comenzar Prueba') }}</span>
						</Button>
						
						<Button v-if="inVideo" @click="props.backToVideo()" variant="ghost" class="px-6 py-2.5 text-base rounded-xl">
							{{ __('Volver al Video') }}
						</Button>
					</div>
					
					<div
						v-if="quiz.data.max_attempts && attempts.data?.length >= quiz.data.max_attempts"
						class="mt-4 px-4 py-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-xl font-medium inline-block text-sm"
					>
						{{ __('Has superado el límite de intentos permitidos para este cuestionario.') }}
					</div>
				</div>
			</div>
		</div>
		<div v-else-if="!quizSubmission.data">
			<div v-for="(question, qtidx) in questions">
				<div
					v-if="qtidx == activeQuestion - 1 && questionDetails.data"
					class="border rounded-lg p-5"
				>
					<div class="flex justify-between">
						<div class="text-sm text-ink-gray-5">
							{{ __('Pregunta {0}').format(activeQuestion) }} -
							{{ getInstructions(questionDetails.data) }}
						</div>
						<div class="text-ink-gray-9 text-sm font-semibold item-left">
							{{ question.marks }}
							{{ question.marks == 1 ? __('Punto') : __('Puntos') }}
						</div>
					</div>
					<div
						class="text-ink-gray-9 font-semibold mt-2 leading-5"
						v-html="questionDetails.data.question"
					></div>
					<div v-if="questionDetails.data.type == 'Choices'" v-for="index in 4">
						<label
							v-if="questionDetails.data[`option_${index}`]"
							class="flex items-center bg-surface-gray-3 rounded-md p-3 mt-4 w-full cursor-pointer focus:border-blue-600"
						>
							<input
								v-if="!showAnswers.length && !questionDetails.data.multiple"
								type="radio"
								:name="encodeURIComponent(questionDetails.data.question)"
								class="w-3.5 h-3.5 text-ink-gray-9 focus:ring-outline-gray-modals"
								@change="markAnswer(index)"
								:checked="selectedOptions[index - 1]"
							/>

							<input
								v-else-if="!showAnswers.length && questionDetails.data.multiple"
								type="checkbox"
								:name="encodeURIComponent(questionDetails.data.question)"
								class="w-3.5 h-3.5 text-ink-gray-9 rounded-sm focus:ring-outline-gray-modals"
								@change="markAnswer(index)"
								:checked="selectedOptions[index - 1]"
							/>
							<div
								v-else-if="quiz.data.show_answers"
								v-for="(answer, idx) in showAnswers"
							>
								<div v-if="index - 1 == idx">
									<CheckCircle
										v-if="answer == 1"
										class="w-4 h-4 text-ink-green-2"
									/>
									<MinusCircle
										v-else-if="answer == 2"
										class="w-4 h-4 text-ink-green-2"
									/>
									<XCircle
										v-else-if="answer == 0"
										class="w-4 h-4 text-ink-red-3"
									/>
									<MinusCircle v-else class="w-4 h-4" />
								</div>
							</div>
							<span
								class="ms-2 text-ink-gray-9"
								v-html="questionDetails.data[`option_${index}`]"
							>
							</span>
						</label>
						<div
							v-if="questionDetails.data[`explanation_${index}`]"
							class="mt-2 text-xs text-ink-gray-7"
							v-show="showAnswers.length"
						>
							{{ questionDetails.data[`explanation_${index}`] }}
						</div>
					</div>
					<div v-else-if="questionDetails.data.type == 'User Input'">
						<FormControl
							v-model="possibleAnswer"
							type="textarea"
							:disabled="showAnswers.length ? true : false"
							class="my-2"
						/>
						<div v-if="showAnswers.length">
							<Badge v-if="showAnswers[0]" :label="__('Correct')" theme="green">
								<template #prefix>
									<CheckCircle class="w-4 h-4 text-ink-green-2 me-1" />
								</template>
							</Badge>
							<Badge v-else theme="red" :label="__('Incorrect')">
								<template #prefix>
									<XCircle class="w-4 h-4 text-ink-red-3 me-1" />
								</template>
							</Badge>
						</div>
					</div>
					<div v-else>
						<TextEditor
							class="mt-4"
							:content="possibleAnswer"
							@change="(val) => (possibleAnswer = val)"
							:editable="true"
							:fixedMenu="true"
							editorClass="prose-sm max-w-none border-b border-x border-outline-gray-modals bg-surface-gray-2 rounded-b-md py-1 px-2 min-h-[7rem]"
						/>
					</div>
					<div class="flex items-center justify-between mt-8">
						<Checkbox
							v-if="!quiz.data.show_answers"
							:label="__('Marcar para revisar')"
							:model-value="reviewQuestions.includes(activeQuestion) ? 1 : 0"
							@change="markForReview($event, activeQuestion)"
						/>
						<div
							v-if="!quiz.data.show_answers"
							class="flex items-center gap-x-2"
						>
							<Button
								@click="switchQuestion(activeQuestion - 1)"
								:disabled="activeQuestion == 1"
								class="rounded-full"
							>
								<template #icon>
									<ChevronLeft class="size-4 stroke-1.5" />
								</template>
							</Button>
							<span
								v-for="item in paginationWindow"
								:key="item"
								class="w-6 h-6 rounded-full flex items-center justify-center text-sm"
								:class="{
									'cursor-pointer': item !== '...',
									'bg-surface-gray-4 border border-outline-gray-5 font-medium':
										activeQuestion == item,
									'text-ink-gray-5': item === '...',
									'bg-surface-blue-3 text-ink-white':
										attemptedQuestions.includes(item) && activeQuestion != item,
									'bg-surface-gray-3 text-ink-gray-6':
										activeQuestion != item &&
										item !== '...' &&
										!attemptedQuestions.includes(item),
								}"
								@click="item !== '...' && switchQuestion(item)"
							>
								{{ item }}
							</span>

							<Button
								@click="switchQuestion(activeQuestion + 1)"
								:disabled="activeQuestion == questions.length"
								class="rounded-full"
							>
								<template #icon>
									<ChevronRight class="size-4 stroke-1.5" />
								</template>
							</Button>
						</div>
						<Button
							v-if="
								quiz.data.show_answers &&
								!showAnswers.length &&
								questionDetails.data.type != 'Open Ended'
							"
							class="ms-auto"
							@click="checkAnswer()"
						>
							<span>
								{{ __('Verificar') }}
							</span>
						</Button>
						<Button
							v-else-if="
								activeQuestion != questions.length && quiz.data.show_answers
							"
							@click="nextQuestion()"
							class="ms-auto"
						>
							<span>
								{{ __('Siguiente') }}
							</span>
						</Button>
						<Button
							variant="solid"
							v-else
							@click="handleSubmitClick()"
							class="ms-auto"
						>
							<span>
								{{ __('Enviar') }}
							</span>
						</Button>
					</div>
				</div>
			</div>
			<div v-if="reviewQuestions.length" class="border rounded-lg p-4 mt-4">
				<div class="font-semibold">
					{{ __('Preguntas marcadas para revisar') }}
				</div>
				<div class="flex items-center gap-x-2 mt-2">
					<div
						v-for="index in reviewQuestions"
						@click="switchQuestion(index)"
						class="w-6 h-6 rounded-full flex items-center justify-center text-sm cursor-pointer bg-surface-gray-3"
					>
						{{ index }}
					</div>
				</div>
			</div>
		</div>
		<div v-else class="border rounded-lg p-20 text-center space-y-2">
			<div class="text-lg font-semibold text-ink-gray-9">
				{{ __('Resumen del Cuestionario') }}
			</div>
			<div
				v-if="quizSubmission.data.is_open_ended"
				class="leading-5 text-ink-gray-7"
			>
				{{
					__(
						"Tu envío se ha guardado correctamente. El instructor lo revisará y calificará pronto, y recibirás una notificación con tu resultado final."
					)
				}}
			</div>
			<div v-else class="text-ink-gray-7">
				{{
					__(
						'Obtuviste un {0}% de respuestas correctas, con un puntaje de {1} sobre {2}'
					).format(
						Math.ceil(quizSubmission.data.percentage),
						quizSubmission.data.score,
						quizSubmission.data.score_out_of
					)
				}}
			</div>
			<div class="flex gap-x-2">
				<Button
					@click="resetQuiz()"
					class="mt-2"
					v-if="
						!quiz.data.max_attempts ||
						attempts?.data.length < quiz.data.max_attempts
					"
				>
					<span>
						{{ __('Intentar de nuevo') }}
					</span>
				</Button>
				<Button v-if="inVideo" @click="props.backToVideo()">
					{{ __('Resume Video') }}
				</Button>
			</div>
		</div>
		<div
			v-if="
				quiz.data.show_submission_history &&
				attempts?.data &&
				attempts.data.length > 0
			"
			class="mt-10"
		>
			<ListView
				:columns="getSubmissionColumns()"
				:rows="attempts?.data"
				row-key="name"
				:options="{
					selectable: false,
					showTooltip: false,
					emptyState: { title: __('No se encontraron envíos para este cuestionario') },
				}"
			>
			</ListView>
		</div>
	</div>
	<Dialog
		v-model="showSubmissionConfirmation"
		:options="{
			title: __('¿Estás seguro de que deseas enviar el cuestionario?'),
			actions: [
				{
					size: 'sm',
					label: __('Enviar'),
					variant: 'solid',
					onClick() {
						submitQuiz()
						showSubmissionConfirmation = false
					},
				},
			],
		}"
	>
		<template #body-content>
			<div class="border border-outline-gray-modals rounded-lg text-base">
				<div class="divide-y divide-outline-gray-modals">
					<div class="grid grid-cols-2 divide-x divide-outline-gray-modals">
						<div class="p-2">
							{{ __('Total de Preguntas') }}
						</div>
						<div class="p-2">
							{{ questions.length }}
						</div>
					</div>
					<div class="grid grid-cols-2 divide-x divide-outline-gray-modals">
						<div class="p-2">
							{{ __('Preguntas Contestadas') }}
						</div>
						<div class="p-2">
							{{ attemptedQuestions.length }}
						</div>
					</div>
					<div class="grid grid-cols-2 divide-x divide-outline-gray-modals">
						<div class="p-2">
							{{ __('Preguntas Sin Contestar') }}
						</div>
						<div class="p-2">
							{{ questions.length - attemptedQuestions.length }}
						</div>
					</div>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import {
	Badge,
	Button,
	call,
	Checkbox,
	createResource,
	Dialog,
	ListView,
	TextEditor,
	FormControl,
	toast,
} from 'frappe-ui'
import {
	computed,
	inject,
	onMounted,
	onUnmounted,
	reactive,
	ref,
	watch,
} from 'vue'
import {
	CheckCircle,
	ChevronLeft,
	ChevronRight,
	XCircle,
	MinusCircle,
	ClipboardList,
	AlertTriangle,
	ListOrdered,
	Clock,
	Target,
	RotateCcw
} from 'lucide-vue-next'
import { timeAgo } from '@/utils'
import ProgressBar from '@/components/ProgressBar.vue'

const user = inject('$user')
const activeQuestion = ref(0)
const currentQuestion = ref('')
const selectedOptions = ref([0, 0, 0, 0])
const showAnswers = reactive([])
let questions = reactive([])
const attemptedQuestions = ref([])
const reviewQuestions = ref([])
const showSubmissionConfirmation = ref(false)
const possibleAnswer = ref(null)
const timer = ref(0)
let timerInterval = null

const props = defineProps({
	quizName: {
		type: String,
		required: true,
	},
	inVideo: {
		type: Boolean,
		default: false,
	},
	backToVideo: {
		type: Function,
		default: () => {},
	},
})

onMounted(() => {
	window.addEventListener('pagehide', handlePageHide)
	window.addEventListener('beforeunload', handleBeforeUnload)
})

onUnmounted(() => {
	window.removeEventListener('pagehide', handlePageHide)
	window.removeEventListener('beforeunload', handleBeforeUnload)
})

const handlePageHide = () => {
	if (activeQuestion.value > 0 && !quizSubmission.data) {
		const params = new URLSearchParams({
			quiz: quiz.data.name,
			results: localStorage.getItem(quiz.data.title) || '[]',
		})

		navigator.sendBeacon(
			'/api/method/lms.lms.doctype.lms_quiz.lms_quiz.submit_quiz?' +
				params.toString()
		)
	}
}

const handleBeforeUnload = (event) => {
	if (activeQuestion.value > 0 && !quizSubmission.data) {
		if (attemptedQuestions.value.length) {
			switchQuestion(activeQuestion.value)
		}
		event.preventDefault()
		event.returnValue = ''
	}
}

const quiz = createResource({
	url: 'frappe.client.get',
	makeParams(values) {
		return {
			doctype: 'LMS Quiz',
			name: props.quizName,
		}
	},
	cache: ['quiz', props.quizName],
	auto: true,
	transform(data) {
		data.duration = parseInt(data.duration)
	},
	onSuccess(data) {
		populateQuestions()
		setupTimer()
	},
})

const populateQuestions = () => {
	let data = quiz.data
	if (data.shuffle_questions) {
		questions = shuffleArray(data.questions)
		if (data.limit_questions_to) {
			questions = questions.slice(0, data.limit_questions_to)
		}
	} else {
		questions = data.questions
	}
}

const setupTimer = () => {
	if (quiz.data.duration) {
		timer.value = quiz.data.duration * 60
	}
}

const startTimer = () => {
	timerInterval = setInterval(() => {
		timer.value--
		if (timer.value == 0) {
			clearInterval(timerInterval)
			submitQuiz()
		}
	}, 1000)
}

const formatTimer = (seconds) => {
	const hrs = Math.floor(seconds / 3600)
		.toString()
		.padStart(2, '0')
	const mins = Math.floor((seconds % 3600) / 60)
		.toString()
		.padStart(2, '0')
	const secs = (seconds % 60).toString().padStart(2, '0')
	return hrs != '00' ? `${hrs}:${mins}:${secs}` : `${mins}:${secs}`
}

const timerProgress = computed(() => {
	return (timer.value / (quiz.data.duration * 60)) * 100
})

const shuffleArray = (array) => {
	for (let i = array.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1))
		;[array[i], array[j]] = [array[j], array[i]]
	}
	return array
}

const attempts = createResource({
	url: 'frappe.client.get_list',
	makeParams(values) {
		return {
			doctype: 'LMS Quiz Submission',
			filters: {
				member: user.data?.name,
				quiz: quiz.data?.name,
			},
			fields: [
				'name',
				'creation',
				'score',
				'score_out_of',
				'percentage',
				'passing_percentage',
			],
			order_by: 'creation desc',
		}
	},
	transform(data) {
		data.forEach((submission, index) => {
			submission.creation = timeAgo(submission.creation)
			submission.idx = index + 1
		})
	},
})

watch(
	() => quiz.data,
	() => {
		if (quiz.data) {
			populateQuestions()
		}
		if (quiz.data && quiz.data.max_attempts) {
			attempts.reload()
			resetQuiz()
		}
	}
)

const quizSubmission = createResource({
	url: 'lms.lms.doctype.lms_quiz.lms_quiz.submit_quiz',
	makeParams(values) {
		return {
			quiz: quiz.data.name,
			results: localStorage.getItem(quiz.data.title) || '[]',
		}
	},
})

const questionDetails = createResource({
	url: 'lms.lms.utils.get_question_details',
	makeParams(values) {
		return {
			question: currentQuestion.value,
		}
	},
})

watch(activeQuestion, (value) => {
	if (value > 0) {
		currentQuestion.value = quiz.data.questions[value - 1].question
		questionDetails.reload(
			{},
			{
				onSuccess() {
					if (!quiz.data.show_answers) {
						loadSavedAnswers()
					}
				},
			}
		)
	}
})

const switchQuestion = (questionNumber) => {
	let answers = getAnswers()
	if (answers.length) {
		if (!attemptedQuestions.value.includes(activeQuestion.value)) {
			attemptedQuestions.value.push(activeQuestion.value)
		}
		addToLocalStorage()
		resetQuestion()
	}

	if (questionNumber < 1 || questionNumber > questions.length) return
	activeQuestion.value = questionNumber
}

const loadSavedAnswers = () => {
	let quizData = JSON.parse(localStorage.getItem(quiz.data.title))
	if (quizData) {
		let localQuestion = quizData.find(
			(q) => q.question_name == currentQuestion.value
		)
		if (localQuestion) {
			let localAnswers = localQuestion.answer
			if (localAnswers.length) {
				if (questionDetails.data.type == 'Choices') {
					localAnswers.forEach((answer) => {
						for (let i = 1; i <= 4; i++) {
							if (questionDetails.data[`option_${i}`] == answer) {
								selectedOptions.value[i - 1] = 1
							}
						}
					})
				} else {
					possibleAnswer.value = localAnswers[0]
				}
			}
		}
	}
}

watch(
	() => props.quizName,
	(newName) => {
		if (newName) {
			quiz.reload()
		}
	}
)

const startQuiz = () => {
	activeQuestion.value = 1
	localStorage.removeItem(quiz.data.title)
	if (quiz.data.duration) startTimer()
}

const markAnswer = (index) => {
	if (!questionDetails.data.multiple)
		selectedOptions.value.splice(
			0,
			selectedOptions.value.length,
			...[0, 0, 0, 0]
		)
	selectedOptions.value[index - 1] = selectedOptions.value[index - 1] ? 0 : 1
}

const getAnswers = () => {
	let answers = []
	const type = questionDetails.data.type
	if (type == 'Choices') {
		selectedOptions.value.forEach((value, index) => {
			if (selectedOptions.value[index])
				answers.push(questionDetails.data[`option_${index + 1}`])
		})
	} else {
		answers.push(possibleAnswer.value)
	}

	return answers
}

const checkAnswer = () => {
	let answers = getAnswers()
	if (!answers.length) {
		toast.warning(__('Please select an option'))
		return
	}

	createResource({
		url: 'lms.lms.doctype.lms_quiz.lms_quiz.check_answer',
		params: {
			quiz: quiz.data.name,
			question: currentQuestion.value,
			question_type: questionDetails.data.type,
			answers: JSON.stringify(answers),
		},
		auto: true,
		onSuccess(data) {
			let type = questionDetails.data.type
			if (type == 'Choices') {
				selectedOptions.value.forEach((option, index) => {
					if (option) {
						showAnswers[index] = option && data[index]
					} else if (data[index] == 2) {
						showAnswers[index] = 2
					} else {
						showAnswers[index] = undefined
					}
				})
			} else {
				showAnswers.push(data)
			}
			addToLocalStorage()
			if (!quiz.data.show_answers) {
				resetQuestion()
			}
		},
	})
}

const addToLocalStorage = () => {
	let quizData = JSON.parse(localStorage.getItem(quiz.data.title))
	let questionData = {
		question_name: currentQuestion.value,
		answer: getAnswers(),
	}
	if (quizData) {
		let existingQuestion = quizData.find(
			(q) => q.question_name == questionData.question_name
		)
		if (existingQuestion) {
			existingQuestion.answer = questionData.answer
		} else {
			quizData.push(questionData)
		}
	} else {
		quizData = [questionData]
	}
	localStorage.setItem(quiz.data.title, JSON.stringify(quizData))
}

const nextQuestion = () => {
	if (!quiz.data.show_answers) return
	if (questionDetails.data?.type == 'Open Ended') addToLocalStorage()
	resetQuestion()
}

const resetQuestion = () => {
	if (activeQuestion.value == quiz.data.questions.length) return
	activeQuestion.value = activeQuestion.value + 1
	selectedOptions.value.splice(0, selectedOptions.value.length, ...[0, 0, 0, 0])
	showAnswers.length = 0
	possibleAnswer.value = null
}

const submitQuiz = () => {
	if (!quiz.data.show_answers) {
		if (questionDetails.data.type == 'Open Ended' || getAnswers().length) {
			addToLocalStorage()
		}
		setTimeout(() => {
			createSubmission()
		}, 500)
		return
	}
	createSubmission()
}

const createSubmission = () => {
	quizSubmission.submit(
		{},
		{
			onSuccess(data) {
				markLessonProgress()
				if (quiz.data && quiz.data.max_attempts) attempts.reload()
				if (quiz.data.duration) clearInterval(timerInterval)
			},
			onError(err) {
				const errorTitle = err?.message || ''
				if (errorTitle.includes('MaximumAttemptsExceededError')) {
					const errorMessage = err.messages?.[0] || err
					toast.error(__(errorMessage))
					setTimeout(() => {
						window.location.reload()
					}, 3000)
				}
			},
		}
	)
}

const resetQuiz = () => {
	activeQuestion.value = 0
	selectedOptions.value.splice(0, selectedOptions.value.length, ...[0, 0, 0, 0])
	showAnswers.length = 0
	possibleAnswer.value = null
	attemptedQuestions.value = []
	quizSubmission.reset()
	populateQuestions()
	setupTimer()
}

const getInstructions = (question) => {
	if (question.type == 'Choices')
		if (question.multiple) return __('Choose all answers that apply')
		else return __('Choose one answer')
	else return __('Type your answer')
}

const markLessonProgress = () => {
	let pathname = window.location.pathname.split('/')
	if (!pathname.includes('courses'))
		pathname = window.parent.location.pathname.split('/')
	if (pathname[2] != 'courses') return
	let lessonIndex = pathname.pop().split('-')

	if (lessonIndex.length == 2) {
		call('lms.lms.api.mark_lesson_progress', {
			course: pathname[3],
			chapter_number: lessonIndex[0],
			lesson_number: lessonIndex[1],
		})
	}
}

const handleSubmitClick = () => {
	if (!quiz.data.show_answers) {
		if (attemptedQuestions.value.length) {
			switchQuestion(activeQuestion.value)
		}
		showSubmissionConfirmation.value = true
	} else {
		submitQuiz()
	}
}

const paginationWindow = computed(() => {
	const total = questions.length
	const current = activeQuestion.value
	const pages = []
	const size = 5

	let start = Math.floor((current - 1) / size) * size + 1
	let end = Math.min(start + size - 1, total)

	if (start > 1) {
		pages.push('...')
	}

	for (let i = start; i <= end; i++) {
		pages.push(i)
	}

	if (end < total) {
		pages.push('...')
	}

	return pages
})

const markForReview = (event, questionNumber) => {
	if (event.target.checked) {
		if (!reviewQuestions.value.includes(questionNumber)) {
			reviewQuestions.value.push(questionNumber)
		}
	} else {
		reviewQuestions.value = reviewQuestions.value.filter(
			(num) => num !== questionNumber
		)
	}
}

const getSubmissionColumns = () => {
	return [
		{
			label: 'No.',
			key: 'idx',
		},
		{
			label: 'Date',
			key: 'creation',
		},
		{
			label: 'Score',
			key: 'score',
			align: 'center',
		},
		{
			label: 'Score out of',
			key: 'score_out_of',
			align: 'center',
		},
		{
			label: 'Percentage',
			key: 'percentage',
			align: 'center',
		},
	]
}
</script>

<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content quiz-modal">
			<div class="modal-header">
				<h2><FileQuestion class="icon size-5" /> {{ __('Cuestionario') }}</h2>
				<button class="icon-btn" @click="close"><X class="size-5" /></button>
			</div>
			
			<div v-if="loading" class="loading-state">
				<div class="spinner"></div>
				<h3>{{ __('Creando tu Cuestionario...') }}</h3>
				<div class="loading-bar-wrapper">
					<div class="loading-bar-fill"></div>
				</div>
				<p class="fun-fact"><strong>{{ __('Dato Curioso:') }}</strong> {{ currentFact }}</p>
			</div>
			
			<div v-else-if="quizData && quizData.quiz && quizData.quiz.length > 0" class="quiz-body">
				<div v-if="currentIndex < quizData.quiz.length" class="question-container">
					<div class="progress-bar">
						<div class="progress-fill" :style="{ width: ((currentIndex) / quizData.quiz.length * 100) + '%' }"></div>
					</div>
					<span class="question-count">{{ __('Pregunta') }} {{ currentIndex + 1 }} {{ __('de') }} {{ quizData.quiz.length }}</span>
					
					<h3 class="question-text">{{ currentQuestion.question }}</h3>
					
					<div class="options-list">
						<button 
							v-for="(option, idx) in currentQuestion.options" 
							:key="idx" 
							class="option-btn"
							:class="{
								'selected': selectedOption === idx,
								'correct': hasAnswered && idx === currentQuestion.correct_index,
								'incorrect': hasAnswered && selectedOption === idx && selectedOption !== currentQuestion.correct_index
							}"
							@click="selectOption(idx)"
							:disabled="hasAnswered"
						>
							<span class="option-letter">{{ String.fromCharCode(65 + idx) }}</span>
							<span class="option-text">{{ option }}</span>
						</button>
					</div>
					
					<div v-if="hasAnswered" class="explanation-box" :class="isCorrect ? 'is-correct' : 'is-incorrect'">
						<p><strong>{{ isCorrect ? __('¡Correcto!') : __('Incorrecto.') }}</strong> {{ currentQuestion.explanation }}</p>
					</div>
					
					<button class="primary-btn next-btn" :disabled="!hasAnswered" @click="nextQuestion">
						{{ currentIndex === quizData.quiz.length - 1 ? __('Ver Resultados') : __('Siguiente') }} <ChevronRight class="size-4" />
					</button>
				</div>
				
				<div v-else class="results-container">
					<div class="score-circle">
						<span>{{ score }}</span>
						<small>/ {{ quizData.quiz.length }}</small>
					</div>
					<h3>{{ __('¡Cuestionario Completado!') }}</h3>
					<p>{{ score > quizData.quiz.length / 2 ? __('¡Buen trabajo!') : __('Sigue repasando el material.') }}</p>
					<button class="primary-btn mt-4" @click="close">{{ __('Cerrar') }}</button>
				</div>
			</div>
			<div v-else class="error-state">
				<p>{{ __('No se pudo cargar el cuestionario. Intenta de nuevo.') }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { FileQuestion, X, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
	show: Boolean,
	loading: Boolean,
	data: Object
})

const emit = defineEmits(['update:show'])

const currentIndex = ref(0)
const selectedOption = ref(null)
const hasAnswered = ref(false)
const score = ref(0)

const quizData = computed(() => {
	// data is expected to be a JSON object containing "quiz" array
	if (!props.data) return null
	if (props.data.quiz) return props.data
	// If it's a string, try parsing
	if (typeof props.data === 'string') {
		try { return JSON.parse(props.data) } catch (e) { return null }
	}
	return null
})

const currentQuestion = computed(() => {
	if (!quizData.value || !quizData.value.quiz || currentIndex.value >= quizData.value.quiz.length) return null
	return quizData.value.quiz[currentIndex.value]
})

const isCorrect = computed(() => {
	if (!currentQuestion.value) return false
	return selectedOption.value === currentQuestion.value.correct_index
})

watch(() => props.show, (newVal) => {
	if (newVal) {
		currentIndex.value = 0
		selectedOption.value = null
		hasAnswered.value = false
		score.value = 0
	}
})

const funFacts = [
	__('¿Sabías que el cerebro humano procesa imágenes 60,000 veces más rápido que el texto? ¡Por eso los memes son tan efectivos!'),
	__('Un estudiante promedio olvida el 50% de lo que lee en una hora. Por suerte, estás practicando con este cuestionario.'),
	__('¿Sabías que la palabra "Cuestionario" viene del latín "Quaestionarius", que sonaba a tortura? Tranquilo, este no lo es.'),
	__('Las abejas pueden reconocer rostros humanos. Así que si repruebas, al menos ellas te recordarán.'),
	__('El músculo más fuerte del cuerpo es el masetero (la mandíbula). Pero el cerebro quema el 20% de tus calorías diarias.'),
	__('Estudiar 15 minutos al día es más efectivo que estudiar 10 horas seguidas antes del examen. ¡Poco a poco!'),
	__('¿Sabías que los pulpos tienen tres corazones? Ideal para enamorarse de múltiples materias.'),
]

const currentFact = ref(funFacts[0])
let factInterval = null

function startFacts() {
	currentFact.value = funFacts[Math.floor(Math.random() * funFacts.length)]
	factInterval = setInterval(() => {
		let newFact = funFacts[Math.floor(Math.random() * funFacts.length)]
		while (newFact === currentFact.value) newFact = funFacts[Math.floor(Math.random() * funFacts.length)]
		currentFact.value = newFact
	}, 4000)
}

function stopFacts() {
	if (factInterval) clearInterval(factInterval)
}

watch(() => props.loading, (isL) => {
	if (isL) startFacts()
	else stopFacts()
}, { immediate: true })

onUnmounted(stopFacts)

function close() {
	emit('update:show', false)
}

function selectOption(idx) {
	if (hasAnswered.value) return
	selectedOption.value = idx
	hasAnswered.value = true
	if (idx === currentQuestion.value.correct_index) {
		score.value++
	}
}

function nextQuestion() {
	currentIndex.value++
	selectedOption.value = null
	hasAnswered.value = false
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,0.6); backdrop-filter: blur(4px); z-index: 100; display: flex; align-items: center; justify-content: center; padding: 1rem; }
.modal-content { background: #fff; width: 100%; max-width: 600px; border-radius: 16px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); display: flex; flex-direction: column; max-height: 90vh; overflow: hidden; }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 1.5rem; border-bottom: 1px solid #e2e8f0; }
.modal-header h2 { display: flex; align-items: center; gap: 0.5rem; font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0; }
.icon { color: #2563eb; }
.icon-btn { background: transparent; border: 0; cursor: pointer; color: #64748b; padding: 0.25rem; border-radius: 8px; transition: background 0.2s; }
.icon-btn:hover { background: #f1f5f9; color: #0f172a; }
.quiz-body { padding: 1.5rem; overflow-y: auto; }
.progress-bar { height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden; margin-bottom: 0.5rem; }
.progress-fill { height: 100%; background: #2563eb; transition: width 0.3s ease; }
.question-count { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.question-text { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin: 1rem 0 1.5rem; line-height: 1.4; }
.options-list { display: flex; flex-direction: column; gap: 0.75rem; }
.option-btn { display: flex; align-items: center; gap: 1rem; padding: 1rem; background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 12px; cursor: pointer; text-align: left; transition: all 0.2s ease; font-size: 1rem; color: #334155; }
.option-btn:hover:not(:disabled) { border-color: #93c5fd; background: #eff6ff; }
.option-letter { display: grid; place-items: center; width: 32px; height: 32px; background: #fff; border: 1px solid #cbd5e1; border-radius: 8px; font-weight: 800; color: #64748b; font-size: 0.9rem; flex-shrink: 0; }
.option-btn.selected { border-color: #3b82f6; background: #eff6ff; }
.option-btn.selected .option-letter { background: #3b82f6; border-color: #3b82f6; color: #fff; }
.option-btn.correct { border-color: #10b981; background: #ecfdf5; color: #065f46; }
.option-btn.correct .option-letter { background: #10b981; border-color: #10b981; color: #fff; }
.option-btn.incorrect { border-color: #ef4444; background: #fef2f2; color: #991b1b; opacity: 0.7; }
.option-btn:disabled { cursor: default; }
.explanation-box { margin-top: 1.5rem; padding: 1rem; border-radius: 12px; font-size: 0.95rem; line-height: 1.5; }
.explanation-box.is-correct { background: #ecfdf5; color: #065f46; }
.explanation-box.is-incorrect { background: #fef2f2; color: #991b1b; }
.primary-btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; background: #2563eb; color: #fff; border: 0; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 700; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
.primary-btn:hover:not(:disabled) { background: #1d4ed8; }
.primary-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.next-btn { width: 100%; margin-top: 1.5rem; }
.mt-4 { margin-top: 1.5rem; }
.results-container { text-align: center; padding: 2rem 1rem; }
.score-circle { width: 120px; height: 120px; margin: 0 auto 1.5rem; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 50%; border: 8px solid #2563eb; color: #2563eb; }
.score-circle span { font-size: 2.5rem; font-weight: 900; line-height: 1; }
.score-circle small { font-size: 1rem; font-weight: 700; opacity: 0.7; }
.results-container h3 { font-size: 1.75rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; }
.loading-state, .error-state { padding: 4rem 2rem; text-align: center; color: #64748b; }
.loading-state h3 { font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 1rem 0 0.5rem; }
.loading-bar-wrapper { width: 80%; margin: 1.5rem auto; height: 8px; background: #e2e8f0; border-radius: 999px; overflow: hidden; }
.loading-bar-fill { height: 100%; background: #2563eb; width: 0%; border-radius: 999px; animation: fakeProgress 10s ease-out forwards; }
@keyframes fakeProgress { 0% { width: 0%; } 100% { width: 95%; } }
.fun-fact { font-size: 0.95rem; color: #475569; max-width: 80%; margin: 1rem auto; line-height: 1.5; font-style: italic; min-height: 3rem; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
@keyframes spin { to { transform: rotate(360deg); } }
:root[data-theme="dark"] .modal-content { background: #1e293b; color: #f8fafc; }
:root[data-theme="dark"] .modal-header { border-color: #334155; }
:root[data-theme="dark"] .modal-header h2 { color: #f8fafc; }
:root[data-theme="dark"] .question-text { color: #f8fafc; }
:root[data-theme="dark"] .option-btn { background: #0f172a; border-color: #334155; color: #cbd5e1; }
:root[data-theme="dark"] .option-letter { background: #1e293b; border-color: #475569; }
:root[data-theme="dark"] .option-btn.selected { border-color: #3b82f6; background: rgba(59,130,246,0.1); }
:root[data-theme="dark"] .option-btn.correct { border-color: #10b981; background: rgba(16,185,129,0.1); color: #34d399; }
:root[data-theme="dark"] .option-btn.incorrect { border-color: #ef4444; background: rgba(239,68,68,0.1); color: #f87171; }
:root[data-theme="dark"] .explanation-box.is-correct { background: rgba(16,185,129,0.1); color: #34d399; }
:root[data-theme="dark"] .explanation-box.is-incorrect { background: rgba(239,68,68,0.1); color: #f87171; }

@keyframes slideUpSheet { from { transform: translateY(100%); } to { transform: translateY(0); } }

@media (max-width: 768px) {
	.modal-content.quiz-modal { 
		position: absolute; bottom: 0; left: 0; width: 100%; height: auto; max-height: 90vh;
		border-radius: 24px 24px 0 0; 
		animation: slideUpSheet 0.4s cubic-bezier(0.16, 1, 0.3, 1);
		margin: 0; border: none;
	}
	.modal-content::before {
		content: ''; display: block; width: 40px; height: 5px; background: #cbd5e1; border-radius: 4px; position: absolute; top: 12px; left: 50%; transform: translateX(-50%); z-index: 20;
	}
	.modal-header { padding-top: 1.75rem; }
}
:root[data-theme="dark"] .modal-content::before { background: #475569; }
</style>

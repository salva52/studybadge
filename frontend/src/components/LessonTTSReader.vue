<template>
	<Teleport v-if="segments.length" to="body">
		<div class="lesson-tts-floating">
			<button
				class="lesson-tts-mini-button"
				type="button"
				:title="miniButtonLabel"
				:aria-label="miniButtonLabel"
				@click="toggleReader"
			>
				<Headphones class="lesson-tts-svg" />
				<span v-if="hasStarted" class="lesson-tts-dot"></span>
			</button>

			<div v-if="isOpen" class="lesson-tts-panel">
				<div class="lesson-tts-header">
					<div class="lesson-tts-heading">
						<div class="lesson-tts-icon">
							<Headphones class="lesson-tts-svg" />
						</div>
						<div>
							<div class="lesson-tts-kicker">Lector IA</div>
							<div class="lesson-tts-title">
								{{ statusLabel }}
							</div>
						</div>
					</div>
					<div class="lesson-tts-actions">
						<button
							v-if="status !== 'playing'"
							class="lesson-tts-action lesson-tts-action-primary"
							type="button"
							:disabled="!speechSupported"
							@click="play"
						>
							<Play class="lesson-tts-svg" />
							<span>{{ primaryActionLabel }}</span>
						</button>
						<button
							v-else
							class="lesson-tts-action"
							type="button"
							:disabled="!speechSupported"
							aria-label="Pausar"
							@click="pause"
						>
							<Pause class="lesson-tts-svg" />
						</button>
						<button
							class="lesson-tts-action"
							type="button"
							:disabled="!hasStarted"
							aria-label="Detener"
							@click="stop"
						>
							<Square class="lesson-tts-svg" />
						</button>
						<button
							class="lesson-tts-action"
							type="button"
							aria-label="Cerrar"
							@click="isOpen = false"
						>
							<X class="lesson-tts-svg" />
						</button>
					</div>
				</div>

				<div v-if="!speechSupported" class="lesson-tts-warning">
					Tu navegador no permite lectura por voz en esta pantalla.
				</div>
				<div v-else class="lesson-tts-body">
					<div class="lesson-tts-progress-row">
						<span>{{ partLabel }}</span>
						<span>{{ Math.round(progress) }}%</span>
					</div>
					<div class="lesson-tts-progress">
						<div
							class="lesson-tts-progress-fill"
							:style="{ width: `${progress}%` }"
						></div>
					</div>

					<div class="lesson-tts-current" aria-live="polite">
						<span
							v-for="(token, index) in currentTokens"
							:key="`${currentIndex}-${index}`"
							:class="{ 'is-current-word': token.isWord && isCurrentToken(token) }"
						>
							{{ token.text }}
						</span>
					</div>

					<div class="lesson-tts-settings">
						<label v-if="voices.length" class="lesson-tts-field">
							<span>Voz</span>
							<select
								v-model="selectedVoiceURI"
								:disabled="status === 'playing'"
							>
								<option
									v-for="voice in spanishVoices"
									:key="voice.voiceURI"
									:value="voice.voiceURI"
								>
									{{ voice.name }} · {{ voice.lang }}
								</option>
							</select>
						</label>
						<label class="lesson-tts-field lesson-tts-rate">
							<span>Velocidad</span>
							<select v-model.number="rate" :disabled="status === 'playing'">
								<option :value="0.8">0.8x</option>
								<option :value="0.9">0.9x</option>
								<option :value="1">1x</option>
								<option :value="1.1">1.1x</option>
								<option :value="1.2">1.2x</option>
							</select>
						</label>
					</div>
				</div>
			</div>
		</div>
	</Teleport>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Headphones, Pause, Play, Square, X } from 'lucide-vue-next'

const props = defineProps({
	segments: {
		type: Array,
		required: true,
	},
	title: {
		type: String,
		default: '',
	},
})

const status = ref('idle')
const currentIndex = ref(0)
const currentChar = ref(0)
const voices = ref([])
const selectedVoiceURI = ref('')
const rate = ref(1)
const utterance = ref(null)
const isOpen = ref(false)

const speechSupported = computed(() => {
	return (
		typeof window !== 'undefined' &&
		'speechSynthesis' in window &&
		'SpeechSynthesisUtterance' in window
	)
})

const hasStarted = computed(() => status.value !== 'idle')
const currentText = computed(() => props.segments[currentIndex.value] || '')
const progress = computed(() => {
	if (!props.segments.length) return 0
	if (status.value === 'done') return 100
	const segmentProgress = currentText.value
		? Math.min(currentChar.value / currentText.value.length, 1)
		: 0
	return ((currentIndex.value + segmentProgress) / props.segments.length) * 100
})
const statusLabel = computed(() => {
	if (status.value === 'playing') return 'Leyendo ahora'
	if (status.value === 'paused') return 'Lectura pausada'
	if (status.value === 'done') return 'Lectura terminada'
	return props.title ? 'Escucha esta lección' : 'Escucha el contenido'
})
const primaryActionLabel = computed(() => {
	if (status.value === 'done') return 'Repetir'
	return hasStarted.value ? 'Continuar' : 'Escuchar'
})
const miniButtonLabel = computed(() => {
	if (status.value === 'playing') return 'Leyendo'
	if (status.value === 'paused') return 'Continuar audio'
	if (status.value === 'done') return 'Repetir audio'
	return 'Escuchar lección'
})
const partLabel = computed(() => {
	return `Parte ${currentIndex.value + 1} de ${props.segments.length}`
})
const spanishVoices = computed(() => {
	const filteredVoices = voices.value.filter((voice) =>
		voice.lang?.toLowerCase().startsWith('es')
	)
	return filteredVoices.length ? filteredVoices : voices.value
})

const currentTokens = computed(() => {
	let cursor = 0
	return currentText.value.split(/(\s+)/).filter(Boolean).map((text) => {
		const start = cursor
		cursor += text.length
		return {
			text,
			start,
			end: cursor,
			isWord: !/^\s+$/.test(text),
		}
	})
})

const isCurrentToken = (token) => {
	if (!token.isWord) return false
	return currentChar.value >= token.start && currentChar.value <= token.end
}

const loadVoices = () => {
	if (!speechSupported.value) return
	voices.value = window.speechSynthesis.getVoices()
	if (!selectedVoiceURI.value && voices.value.length) {
		const spanishVoice =
			voices.value.find((voice) => voice.lang === 'es-PE') ||
			voices.value.find((voice) => voice.lang?.startsWith('es-')) ||
			voices.value.find((voice) => voice.lang?.startsWith('es')) ||
			voices.value[0]
		selectedVoiceURI.value = spanishVoice.voiceURI
	}
}

const toggleReader = () => {
	isOpen.value = !isOpen.value
}

const getSelectedVoice = () => {
	return voices.value.find((voice) => voice.voiceURI === selectedVoiceURI.value)
}

const speakCurrentSegment = () => {
	if (!speechSupported.value || !currentText.value) return
	window.speechSynthesis.cancel()
	currentChar.value = 0

	const nextUtterance = new SpeechSynthesisUtterance(currentText.value)
	nextUtterance.lang = getSelectedVoice()?.lang || 'es-PE'
	nextUtterance.voice = getSelectedVoice() || null
	nextUtterance.rate = rate.value
	nextUtterance.pitch = 1
	nextUtterance.onboundary = (event) => {
		if (typeof event.charIndex === 'number') {
			currentChar.value = event.charIndex
		}
	}
	nextUtterance.onend = () => {
		if (status.value !== 'playing') return
		if (currentIndex.value < props.segments.length - 1) {
			currentIndex.value += 1
			speakCurrentSegment()
		} else {
			status.value = 'done'
			currentChar.value = currentText.value.length
		}
	}
	nextUtterance.onerror = () => {
		status.value = 'idle'
	}

	utterance.value = nextUtterance
	window.speechSynthesis.speak(nextUtterance)
}

const play = () => {
	if (!speechSupported.value) return
	if (status.value === 'paused') {
		status.value = 'playing'
		window.speechSynthesis.resume()
		return
	}
	if (status.value === 'done') {
		currentIndex.value = 0
	}
	status.value = 'playing'
	speakCurrentSegment()
}

const pause = () => {
	if (!speechSupported.value) return
	status.value = 'paused'
	window.speechSynthesis.pause()
}

const stop = () => {
	if (!speechSupported.value) return
	window.speechSynthesis.cancel()
	status.value = 'idle'
	currentIndex.value = 0
	currentChar.value = 0
	utterance.value = null
}

onMounted(() => {
	loadVoices()
	if (speechSupported.value) {
		window.speechSynthesis.addEventListener('voiceschanged', loadVoices)
	}
})

onBeforeUnmount(() => {
	stop()
	if (speechSupported.value) {
		window.speechSynthesis.removeEventListener('voiceschanged', loadVoices)
	}
})

watch(
	() => props.segments,
	() => {
		isOpen.value = false
		stop()
	}
)
</script>

<style scoped>
.lesson-tts-floating {
	position: fixed;
	right: 1.5rem;
	bottom: 104px;
	z-index: 2147483000;
	display: flex;
	flex-direction: column-reverse;
	align-items: flex-end;
	gap: 0.5rem;
	pointer-events: none;
}

.lesson-tts-mini-button {
	display: inline-flex;
	position: relative;
	align-items: center;
	justify-content: center;
	width: 2.375rem;
	height: 2.375rem;
	border: 1px solid rgba(0, 123, 255, 0.18);
	border-radius: 999px;
	background: #fff;
	color: var(--sb-primary, #007bff);
	box-shadow: 0 10px 22px rgba(6, 27, 73, 0.18);
	cursor: pointer;
	pointer-events: auto;
	transition:
		background 0.15s ease,
		border-color 0.15s ease,
		transform 0.15s ease;
}

.lesson-tts-mini-button:hover {
	border-color: rgba(0, 123, 255, 0.34);
	background: #f8fbff;
	transform: translateY(-1px);
}

.lesson-tts-dot {
	position: absolute;
	right: 0.25rem;
	top: 0.25rem;
	width: 0.45rem;
	height: 0.45rem;
	border: 2px solid #fff;
	border-radius: 999px;
	background: var(--sb-primary, #007bff);
}

.lesson-tts-svg {
	width: 1rem;
	height: 1rem;
	stroke-width: 2;
}

.lesson-tts-panel {
	width: min(calc(100vw - 2rem), 20rem);
	border: 1px solid rgba(0, 123, 255, 0.16);
	border-radius: 8px;
	background: #ffffff;
	padding: 0.75rem;
	box-shadow: 0 18px 38px rgba(6, 27, 73, 0.2);
	pointer-events: auto;
}

.lesson-tts-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
}

.lesson-tts-heading {
	display: flex;
	align-items: center;
	gap: 0.625rem;
	min-width: 0;
}

.lesson-tts-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 1.75rem;
	height: 1.75rem;
	border-radius: 999px;
	background: rgba(0, 123, 255, 0.1);
	color: var(--sb-primary, #007bff);
	flex-shrink: 0;
}

.lesson-tts-kicker {
	color: var(--sb-primary, #007bff);
	font-size: 0.625rem;
	font-weight: 700;
	text-transform: uppercase;
}

.lesson-tts-title {
	margin-top: 0.125rem;
	color: var(--sb-dark, #061b49);
	font-size: 0.8125rem;
	font-weight: 700;
}

.lesson-tts-actions {
	display: flex;
	align-items: center;
	gap: 0.25rem;
	flex-shrink: 0;
}

.lesson-tts-action {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.25rem;
	min-width: 1.875rem;
	height: 1.875rem;
	border: 1px solid rgba(6, 27, 73, 0.1);
	border-radius: 6px;
	background: #f8fafc;
	color: #334155;
	font-size: 0.75rem;
	font-weight: 600;
	cursor: pointer;
}

.lesson-tts-action:hover:not(:disabled) {
	background: #eef6ff;
	border-color: rgba(0, 123, 255, 0.22);
	color: var(--sb-primary, #007bff);
}

.lesson-tts-action:disabled {
	cursor: not-allowed;
	opacity: 0.45;
}

.lesson-tts-action-primary {
	min-width: 4.8rem;
	background: var(--sb-primary, #007bff);
	border-color: var(--sb-primary, #007bff);
	color: #fff;
}

.lesson-tts-action-primary:hover:not(:disabled) {
	background: #006be0;
	color: #fff;
}

.lesson-tts-warning {
	margin-top: 0.75rem;
	color: #9a3412;
	font-size: 0.875rem;
}

.lesson-tts-body {
	margin-top: 0.625rem;
}

.lesson-tts-progress-row {
	display: flex;
	justify-content: space-between;
	color: #64748b;
	font-size: 0.75rem;
	font-weight: 600;
}

.lesson-tts-progress {
	margin-top: 0.375rem;
	height: 0.25rem;
	overflow: hidden;
	border-radius: 999px;
	background: rgba(0, 123, 255, 0.12);
}

.lesson-tts-progress-fill {
	height: 100%;
	border-radius: inherit;
	background: var(--sb-primary, #007bff);
	transition: width 0.25s ease;
}

.lesson-tts-current {
	margin-top: 0.625rem;
	max-height: 3rem;
	overflow-y: auto;
	border-radius: 6px;
	background: #f8fafc;
	padding: 0.5rem 0.625rem;
	color: #374151;
	font-size: 0.8125rem;
	line-height: 1.45;
}

.is-current-word {
	border-radius: 4px;
	background: rgba(0, 123, 255, 0.16);
	color: var(--sb-dark, #061b49);
}

.lesson-tts-settings {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 5.5rem;
	gap: 0.5rem;
	margin-top: 0.625rem;
}

.lesson-tts-field {
	display: flex;
	flex-direction: column;
	gap: 0.25rem;
	color: #64748b;
	font-size: 0.6875rem;
	font-weight: 600;
}

.lesson-tts-field select {
	min-height: 1.875rem;
	width: 100%;
	border: 1px solid rgba(6, 27, 73, 0.12);
	border-radius: 6px;
	background: white;
	color: #374151;
	padding: 0 0.5rem;
	font-size: 0.8125rem;
}

@media (max-width: 640px) {
	.lesson-tts-floating {
		right: 1.5rem;
		bottom: 160px;
	}

	.lesson-tts-panel {
		width: min(calc(100vw - 1.5rem), 19rem);
	}

	.lesson-tts-settings {
		grid-template-columns: minmax(0, 1fr) 5.25rem;
	}
}
</style>

<template>
	<section v-if="segments.length" class="lesson-tts-reader">
		<div class="lesson-tts-header">
			<div>
				<div class="lesson-tts-kicker">{{ __('Lector IA') }}</div>
				<div class="lesson-tts-title">
					{{ statusLabel }}
				</div>
			</div>
			<div class="lesson-tts-actions">
				<Button
					v-if="status !== 'playing'"
					:disabled="!speechSupported"
					variant="solid"
					@click="play"
				>
					<template #prefix>
						<Play class="size-4" />
					</template>
					{{ primaryActionLabel }}
				</Button>
				<Button v-else :disabled="!speechSupported" @click="pause">
					<template #prefix>
						<Pause class="size-4" />
					</template>
					{{ __('Pausar') }}
				</Button>
				<Button :disabled="!hasStarted" @click="stop">
					<template #icon>
						<Square class="size-4" />
					</template>
				</Button>
			</div>
		</div>

		<div v-if="!speechSupported" class="lesson-tts-warning">
			{{ __('Tu navegador no permite lectura por voz en esta pantalla.') }}
		</div>
		<div v-else class="lesson-tts-body">
			<div class="lesson-tts-progress-row">
				<span>
					{{ __('Parte {0} de {1}', [currentIndex + 1, segments.length]) }}
				</span>
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
					<span>{{ __('Voz') }}</span>
					<select v-model="selectedVoiceURI" :disabled="status === 'playing'">
						<option
							v-for="voice in voices"
							:key="voice.voiceURI"
							:value="voice.voiceURI"
						>
							{{ voice.name }} · {{ voice.lang }}
						</option>
					</select>
				</label>
				<label class="lesson-tts-field">
					<span>{{ __('Velocidad') }}</span>
					<input
						v-model.number="rate"
						type="range"
						min="0.8"
						max="1.2"
						step="0.05"
						:disabled="status === 'playing'"
					/>
				</label>
			</div>
		</div>
	</section>
</template>

<script setup>
import { Button } from 'frappe-ui'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Pause, Play, Square } from 'lucide-vue-next'

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
	if (status.value === 'playing') return __('Leyendo ahora')
	if (status.value === 'paused') return __('Lectura pausada')
	if (status.value === 'done') return __('Lectura terminada')
	return props.title ? __('Escucha esta lección') : __('Escucha el contenido')
})
const primaryActionLabel = computed(() => {
	if (status.value === 'done') return __('Repetir')
	return hasStarted.value ? __('Continuar') : __('Escuchar')
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
	() => stop()
)
</script>

<style scoped>
.lesson-tts-reader {
	margin-top: 1.5rem;
	border: 1px solid rgba(0, 123, 255, 0.16);
	border-radius: 8px;
	background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
	padding: 1rem;
	box-shadow: 0 10px 24px rgba(6, 27, 73, 0.06);
}

.lesson-tts-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
}

.lesson-tts-kicker {
	color: var(--sb-primary, #007bff);
	font-size: 0.75rem;
	font-weight: 700;
	text-transform: uppercase;
}

.lesson-tts-title {
	margin-top: 0.125rem;
	color: var(--sb-dark, #061b49);
	font-size: 1rem;
	font-weight: 700;
}

.lesson-tts-actions {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	flex-shrink: 0;
}

.lesson-tts-warning {
	margin-top: 0.75rem;
	color: #9a3412;
	font-size: 0.875rem;
}

.lesson-tts-body {
	margin-top: 0.875rem;
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
	height: 0.375rem;
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
	margin-top: 0.875rem;
	border-radius: 8px;
	background: white;
	padding: 0.875rem;
	color: #374151;
	font-size: 0.95rem;
	line-height: 1.7;
}

.is-current-word {
	border-radius: 4px;
	background: rgba(0, 123, 255, 0.16);
	color: var(--sb-dark, #061b49);
}

.lesson-tts-settings {
	display: grid;
	grid-template-columns: minmax(0, 1.4fr) minmax(9rem, 0.6fr);
	gap: 0.75rem;
	margin-top: 0.875rem;
}

.lesson-tts-field {
	display: flex;
	flex-direction: column;
	gap: 0.35rem;
	color: #64748b;
	font-size: 0.75rem;
	font-weight: 600;
}

.lesson-tts-field select,
.lesson-tts-field input {
	min-height: 2rem;
	border: 1px solid rgba(6, 27, 73, 0.12);
	border-radius: 6px;
	background: white;
	color: #374151;
	font-size: 0.875rem;
}

.lesson-tts-field select {
	padding: 0 0.5rem;
}

@media (max-width: 640px) {
	.lesson-tts-header {
		flex-direction: column;
	}

	.lesson-tts-actions,
	.lesson-tts-settings {
		width: 100%;
	}

	.lesson-tts-settings {
		grid-template-columns: 1fr;
	}
}
</style>

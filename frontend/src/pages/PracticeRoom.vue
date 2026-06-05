<template>
	<div class="room-page">
		<header class="room-header">
			<div class="room-header-left">
				<div class="room-kicker">
					<span class="room-live-dot" :class="{ active: liveConnected }"></span>
					{{ liveConnected ? __('Voz Live activa') : __('Simulación IA') }}
				</div>

				<h1>{{ session?.title || __('Sala de práctica') }}</h1>

				<div class="room-meta">
					<span>{{ practiceTypeLabel }}</span>
					<span>{{ liveConnected ? __('Voz') : __('Chat') }}</span>
					<span>{{ elapsedTime }}</span>
				</div>
			</div>

			<div class="room-header-actions">
				<button class="room-ghost" @click="saveTranscript">
					<Save class="size-4" />
					<span>{{ __('Guardar') }}</span>
				</button>

				<button class="room-danger" :disabled="finishing" @click="finishSession">
					<Square class="size-4" />
					<span>{{ finishing ? __('Evaluando...') : __('Finalizar y ver resumen') }}</span>
				</button>
			</div>
		</header>

		<main class="room-layout">
			<section class="room-stage">
				<div v-if="hasFeedback" class="feedback-panel">
					<div class="feedback-head">
						<div class="feedback-score-wrap">
							<div class="feedback-score">{{ feedbackScore }}</div>
							<span>{{ feedbackScoreLabel }}</span>
						</div>

						<div class="feedback-copy">
							<div class="room-kicker">{{ __('Resumen final de la IA') }}</div>
							<h2>{{ __('Así te fue en la práctica') }}</h2>
							<p>{{ feedback.summary || __('La IA preparó una evaluación con tus fortalezas, puntos de mejora y próximos pasos.') }}</p>
						</div>
					</div>

					<div class="feedback-grid">
						<div class="feedback-card">
							<h3>{{ __('Fortalezas') }}</h3>
							<ul v-if="feedback.strengths?.length">
								<li v-for="item in feedback.strengths" :key="item">{{ item }}</li>
							</ul>
							<p v-else>{{ __('Aún no hay fortalezas detalladas.') }}</p>
						</div>

						<div class="feedback-card">
							<h3>{{ __('Por mejorar') }}</h3>
							<ul v-if="feedback.improvements?.length">
								<li v-for="item in feedback.improvements" :key="item">{{ item }}</li>
							</ul>
							<p v-else>{{ __('Aún no hay mejoras detalladas.') }}</p>
						</div>

						<div class="feedback-card">
							<h3>{{ __('Siguiente práctica') }}</h3>
							<ul v-if="feedback.next_steps?.length">
								<li v-for="item in feedback.next_steps" :key="item">{{ item }}</li>
							</ul>
							<p v-else>{{ __('Repite la simulación con un objetivo más específico.') }}</p>
						</div>
					</div>

					<div v-if="feedback.sample_better_answer" class="better-answer">
						<strong>{{ __('Ejemplo de mejor respuesta') }}</strong>
						<p>{{ feedback.sample_better_answer }}</p>
					</div>
				</div>

				<div class="meeting-grid">
					<div class="ai-tile">
						<div class="tile-topbar">
							<div class="tile-status" :class="{ live: liveConnected }">
								<span></span>
								{{ liveConnected ? __('Voz activa') : __('Modo chat') }}
							</div>

							<div class="call-time">
								<Radio class="size-4" />
								{{ micEnabled ? __('Escuchando') : __('En espera') }}
							</div>
						</div>

						<div class="ai-avatar-wrap">
							<div class="ai-avatar" :class="{ speaking: isAiSpeaking }">
								<Bot class="size-16" />
							</div>
						</div>

						<div class="tile-info">
							<h2>{{ interviewerLabel }}</h2>
							<p>
								{{ __('La IA hará preguntas, presionará con objeciones y evaluará tu desempeño al finalizar.') }}
							</p>
						</div>

						<div class="tile-name-bar">
							<Bot class="size-4" />
							<span>{{ interviewerLabel }}</span>
						</div>
					</div>

					<div class="participant-column">
						<div class="user-tile">
							<div class="user-tile-top">
								<div class="tile-status" :class="{ live: micEnabled }">
									<span></span>
									{{ micEnabled ? __('Micrófono activo') : __('Mic apagado') }}
								</div>
							</div>

							<div class="user-avatar">
								<User class="size-12" />
							</div>

							<h3>{{ __('Tú') }}</h3>

							<p>
								{{ micEnabled ? __('Responde con naturalidad por voz.') : __('Puedes responder por texto o activar voz.') }}
							</p>

							<div class="tile-name-bar user">
								<User class="size-4" />
								<span>{{ __('Tú') }}</span>
							</div>
						</div>

						<div class="practice-card">
							<div class="room-kicker">{{ __('Consejo rápido') }}</div>
							<h3>{{ quickTip.title }}</h3>
							<p>{{ quickTip.text }}</p>
						</div>
					</div>
				</div>

				<div v-if="liveError" class="room-warning">
					<CircleAlert class="size-4" />
					<span>{{ liveError }}</span>
				</div>

				<div class="room-controls">
					<button
						class="control-btn mic"
						:class="{ active: micEnabled }"
						:disabled="liveLoading"
						@click="toggleLiveVoice"
					>
						<span class="control-icon">
							<Mic v-if="!micEnabled" class="size-5" />
							<MicOff v-else class="size-5" />
						</span>

						<span>
							{{ liveLoading ? __('Conectando...') : micEnabled ? __('Apagar micrófono') : __('Activar voz') }}
						</span>
					</button>

					<button class="control-btn" @click="insertStarter">
						<span class="control-icon">
							<MessageSquare class="size-5" />
						</span>

						<span>{{ __('Sugerir inicio') }}</span>
					</button>

					<router-link :to="{ name: 'Practice' }" class="control-btn">
						<span class="control-icon">
							<LayoutList class="size-5" />
						</span>

						<span>{{ __('Nueva práctica') }}</span>
					</router-link>
				</div>
			</section>

			<aside class="room-side">
				<div class="side-section transcript-section">
					<div class="side-head">
						<div>
							<div class="room-kicker">{{ __('Chat de la sala') }}</div>
							<h2>{{ __('Conversación') }}</h2>
						</div>

						<div class="side-actions">
							<span class="message-count">{{ transcript.length }} {{ transcript.length === 1 ? __('mensaje') : __('mensajes') }}</span>
							<button class="side-icon" @click="saveTranscript" aria-label="Guardar transcripción">
								<Save class="size-4" />
							</button>
						</div>
					</div>

					<div ref="transcriptBox" class="transcript-box">
						<div v-if="!transcript.length" class="empty-transcript">
							<div class="empty-icon">
								<MessageSquare class="size-8" />
							</div>

							<h3>{{ __('Aún no hay mensajes') }}</h3>
							<p>{{ __('Empieza por texto o activa el micrófono para iniciar la simulación.') }}</p>
						</div>

						<div
							v-for="(line, index) in transcript"
							:key="index"
							class="transcript-line"
							:class="line.role"
						>
							<div class="line-role">
								{{ line.role === 'user' ? __('Tú') : __('IA') }}
							</div>

							<div class="line-content">
								{{ line.content }}
							</div>
						</div>
					</div>

					<div class="chat-compose">
						<textarea
							v-model="message"
							rows="3"
							:placeholder="__('Escribe tu respuesta...')"
							@keydown.enter.exact.prevent="sendMessage"
						/>

						<button class="room-primary" :disabled="!message.trim() || sending" @click="sendMessage">
							<Send class="size-4" />
							{{ sending ? __('Enviando...') : __('Enviar') }}
						</button>
					</div>
				</div>

				<div class="side-section notes-section">
					<div class="side-head compact">
						<div>
							<div class="room-kicker">{{ __('Notas') }}</div>
							<h2>{{ __('Apuntes privados') }}</h2>
						</div>
					</div>

					<textarea
						v-model="notes"
						class="notes-area"
						rows="6"
						:placeholder="__('Anota preguntas difíciles, objeciones, ideas o respuestas para mejorar.')"
					/>
				</div>
			</aside>
		</main>
	</div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { call, toast, usePageMeta } from 'frappe-ui'
import {
	Bot,
	CircleAlert,
	LayoutList,
	MessageSquare,
	Mic,
	MicOff,
	Radio,
	Save,
	Send,
	Square,
	User,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const props = defineProps({
	sessionId: {
		type: String,
		required: true,
	},
})

const { brand } = sessionStore()
const session = ref(null)
const transcript = ref([])
const feedback = ref(null)
const message = ref('')
const notes = ref('')
const sending = ref(false)
const finishing = ref(false)
const transcriptBox = ref(null)
const liveConnected = ref(false)
const liveLoading = ref(false)
const liveError = ref('')
const micEnabled = ref(false)
const liveSession = ref(null)
const mediaStream = ref(null)
const inputAudioContext = ref(null)
const outputAudioContext = ref(null)
const microphoneSource = ref(null)
const microphoneProcessor = ref(null)
const outputPlayTime = ref(0)
const liveSocketOpen = ref(false)
const audioStreaming = ref(false)
const isAiSpeaking = ref(false)
const elapsedTime = ref('00:00')

let speakingInterval = null
let timerInterval = null
let startedAt = Date.now()
let lastTurnWasComplete = true
let manualLiveStop = false

onMounted(() => {
	loadSession()
	updateElapsedTime()

	timerInterval = setInterval(updateElapsedTime, 1000)

	speakingInterval = setInterval(() => {
		if (outputAudioContext.value && outputPlayTime.value) {
			isAiSpeaking.value = outputAudioContext.value.currentTime < outputPlayTime.value + 0.5
		} else {
			isAiSpeaking.value = false
		}
	}, 200)
})

onBeforeUnmount(() => {
	stopLiveVoice()

	if (speakingInterval) {
		clearInterval(speakingInterval)
	}

	if (timerInterval) {
		clearInterval(timerInterval)
	}
})

const practiceTypeLabel = computed(() => {
	const labels = {
		interview: __('Entrevista laboral'),
		sales: __('Práctica de ventas'),
		english: __('Inglés conversacional'),
		marketing: __('Caso de marketing'),
		custom: __('Práctica personalizada'),
	}

	return labels[session.value?.practice_type] || __('Práctica IA')
})

const interviewerLabel = computed(() => {
	const labels = {
		interview: __('Entrevistador IA'),
		sales: __('Cliente IA'),
		english: __('Partner de conversación'),
		marketing: __('Cliente de marketing'),
		custom: __('Simulador IA'),
	}

	return labels[session.value?.practice_type] || __('Entrevistador IA')
})

const quickTip = computed(() => {
	const tips = {
		interview: {
			title: __('Responde con estructura'),
			text: __('Usa situación, acción y resultado. Evita respuestas demasiado largas.'),
		},
		sales: {
			title: __('Escucha antes de vender'),
			text: __('Haz preguntas, detecta dolor y conecta tu solución con un beneficio claro.'),
		},
		english: {
			title: __('Habla simple y claro'),
			text: __('No busques perfección. Prioriza fluidez, intención y frases naturales.'),
		},
		marketing: {
			title: __('Parte del objetivo'),
			text: __('Aclara público, oferta, canal y métrica antes de proponer una campaña.'),
		},
		custom: {
			title: __('Practica con intención'),
			text: __('Responde como si fuera una situación real y pide presión si quieres subir dificultad.'),
		},
	}

	return tips[session.value?.practice_type] || tips.custom
})

const hasFeedback = computed(() => feedback.value && Object.keys(feedback.value).length)

const feedbackScore = computed(() => {
	const rawScore = Number(feedback.value?.score || 0)
	return Number.isInteger(rawScore) ? rawScore : rawScore.toFixed(1)
})

const feedbackScoreLabel = computed(() => {
	const score = Number(feedback.value?.score || 0)

	if (score >= 9) return __('Excelente')
	if (score >= 7.5) return __('Muy bien')
	if (score >= 6) return __('Buen avance')
	if (score > 0) return __('Necesita práctica')
	return __('Evaluación')
})

usePageMeta(() => ({
	title: session.value?.title || __('Sala de práctica'),
	icon: brand.favicon,
}))

async function loadSession() {
	try {
		session.value = await call('studybadge_ai.ai_practice.get_practice_session', {
			session: props.sessionId,
		})

		transcript.value = session.value.transcript || []
		feedback.value = session.value.feedback || null
		notes.value = session.value.notes || ''
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo abrir la práctica.'))
	}
}

function updateElapsedTime() {
	const totalSeconds = Math.max(0, Math.floor((Date.now() - startedAt) / 1000))
	const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, '0')
	const seconds = String(totalSeconds % 60).padStart(2, '0')

	elapsedTime.value = `${minutes}:${seconds}`
}

function appendLine(role, content, append = false) {
	if (!content?.trim()) return

	const c = content.trim()
	const last = transcript.value[transcript.value.length - 1]

	if (append && last && last.role === role) {
		last.content += ' ' + c
	} else {
		transcript.value.push({
			role,
			content: c,
			timestamp: new Date().toISOString(),
		})
	}

	nextTick(() => {
		if (transcriptBox.value) {
			transcriptBox.value.scrollTop = transcriptBox.value.scrollHeight
		}
	})
}

function insertStarter() {
	const starters = {
		interview: __('Hola, gracias por la oportunidad. Estoy listo para comenzar la entrevista.'),
		sales: __('Hola, antes de proponerte algo me gustaría entender mejor tu situación.'),
		english: __('Hi, I am ready to practice. Please ask me a natural first question.'),
		marketing: __('Estoy listo para analizar el caso. Primero quiero entender el objetivo de negocio.'),
		custom: __('Estoy listo para empezar la simulación.'),
	}

	message.value = starters[session.value?.practice_type] || starters.custom
}

async function sendMessage() {
	const text = message.value.trim()

	if (!text || sending.value) return

	message.value = ''
	appendLine('user', text)
	sending.value = true

	try {
		const result = await call('studybadge_ai.ai_practice.send_practice_message', {
			session: props.sessionId,
			message: text,
			history: JSON.stringify(transcript.value.slice(0, -1)),
		})

		transcript.value = result.transcript || transcript.value

		if (result.fallback) {
			liveError.value = __('La IA no respondió desde el proveedor configurado. Dejé una respuesta guía para que puedas seguir por texto.')
		}
	} catch (error) {
		toast.error(error.messages?.[0] || __('La IA no pudo responder.'))
	} finally {
		sending.value = false

		nextTick(() => {
			if (transcriptBox.value) {
				transcriptBox.value.scrollTop = transcriptBox.value.scrollHeight
			}
		})
	}
}

async function saveTranscript(showToast = true) {
	try {
		await call('studybadge_ai.ai_practice.save_practice_transcript', {
			session: props.sessionId,
			transcript: JSON.stringify(transcript.value),
		})

		if (showToast) {
			toast.success(__('Transcripción guardada.'))
		}
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo guardar.'))
	}
}

async function finishSession() {
	if (finishing.value) return

	finishing.value = true

	await stopLiveVoice()

	try {
		await saveTranscript(false)

		const result = await call('studybadge_ai.ai_practice.finish_practice_session', {
			session: props.sessionId,
		})

		feedback.value = result.feedback || feedback.value
		session.value = result.session || session.value

		toast.success(__('Resumen final generado.'))
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo finalizar la práctica.'))
	} finally {
		finishing.value = false
	}
}

async function toggleLiveVoice() {
	if (micEnabled.value || liveConnected.value) {
		await stopLiveVoice()
		return
	}

	await startLiveVoice()
}

async function startLiveVoice() {
	liveLoading.value = true
	liveError.value = ''
	manualLiveStop = false

	try {
		const token = await call('studybadge_ai.ai_practice.create_live_token', {
			session: props.sessionId,
		})

		if (!token.live_supported || !token.token) {
			liveError.value = token.message || __('Voz no disponible. Continúa por texto.')
			liveLoading.value = false
			return
		}

		const liveEndpoint =
			token.endpoint ||
			'wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContentConstrained'
		const url = `${liveEndpoint}?access_token=${token.token}`
		const ws = new WebSocket(url)

		liveSession.value = ws

		ws.onopen = () => {
			const setupMessage = {
				setup: {
					model: `models/${token.model.replace('models/', '')}`,
					generationConfig: {
						responseModalities: ['AUDIO'],
					},
					systemInstruction:
						typeof token.config.systemInstruction === 'string'
							? { parts: [{ text: token.config.systemInstruction }] }
							: token.config.systemInstruction,
				},
			}

			ws.send(JSON.stringify(setupMessage))
		}

		ws.onmessage = async (event) => {
			try {
				let msg = event.data

				if (msg instanceof Blob) {
					msg = await msg.text()
				}

				const data = JSON.parse(msg)

				if (data.setupComplete) {
					liveConnected.value = true
					liveSocketOpen.value = true

					await startMicrophone()

					toast.success(__('Voz activada.'))
					liveLoading.value = false
				} else if (data.serverContent) {
					handleLiveMessage(data)
				} else if (data.error) {
					liveError.value = data.error.message || __('Error en servidor')
				}
			} catch (e) {
				console.error('Error parsing onmessage:', e)
			}
		}

		ws.onerror = () => {
			liveError.value = __('Live API tuvo un problema. Continúa por texto.')
			liveSocketOpen.value = false
			liveConnected.value = false
			stopMicrophoneOnly()
			liveLoading.value = false
		}

		ws.onclose = (event) => {
			if (!manualLiveStop && event.code !== 1000) {
				liveError.value =
					event.code === 1011
						? __('Live API cerró la sesión por un error interno. Intenta activar voz otra vez o continúa por texto.')
						: `${__('Conexión cerrada')}: ${event.code}${event.reason ? ` - ${event.reason}` : ''}`
			}

			liveConnected.value = false
			liveSocketOpen.value = false
			stopMicrophoneOnly()
			liveLoading.value = false
		}
	} catch (error) {
		liveError.value = error.messages?.[0] || error.message || __('No se pudo activar voz. Continúa por texto.')
		await stopLiveVoice()
		liveLoading.value = false
	}
}

async function startMicrophone() {
	if (!navigator.mediaDevices?.getUserMedia) {
		throw new Error(__('Tu navegador no permite usar micrófono aquí.'))
	}

	mediaStream.value = await navigator.mediaDevices.getUserMedia({
		audio: {
			echoCancellation: true,
			noiseSuppression: true,
			autoGainControl: true,
		},
	})

	inputAudioContext.value = new AudioContext()
	outputAudioContext.value = outputAudioContext.value || new AudioContext({ sampleRate: 24000 })

	if (inputAudioContext.value.state === 'suspended') {
		await inputAudioContext.value.resume()
	}

	if (outputAudioContext.value.state === 'suspended') {
		await outputAudioContext.value.resume()
	}

	microphoneSource.value = inputAudioContext.value.createMediaStreamSource(mediaStream.value)
	microphoneProcessor.value = inputAudioContext.value.createScriptProcessor(4096, 1, 1)
	audioStreaming.value = true

	microphoneProcessor.value.onaudioprocess = (event) => {
		if (!audioStreaming.value || !liveSocketOpen.value || !liveSession.value) return

		const input = event.inputBuffer.getChannelData(0)
		const pcm16 = resampleToPcm16(input, inputAudioContext.value.sampleRate, 16000)

		if (!pcm16.byteLength) return

		try {
			if (liveSession.value && liveSession.value.readyState === WebSocket.OPEN) {
				const realtimeInput = {
					realtimeInput: {
						audio: {
							mimeType: 'audio/pcm;rate=16000',
							data: arrayBufferToBase64(pcm16.buffer),
						},
					},
				}

				liveSession.value.send(JSON.stringify(realtimeInput))
			}
		} catch (e) {
			console.error('Live API send error:', e)
		}
	}

	microphoneSource.value.connect(microphoneProcessor.value)
	microphoneProcessor.value.connect(inputAudioContext.value.destination)
	micEnabled.value = true
}

function resampleToPcm16(float32, fromRate, toRate) {
	if (!float32?.length || !fromRate || !toRate) return new Int16Array()

	const ratio = fromRate / toRate
	const newLength = Math.floor(float32.length / ratio)
	const pcm = new Int16Array(newLength)

	for (let i = 0; i < newLength; i++) {
		const start = Math.floor(i * ratio)
		const end = Math.min(Math.floor((i + 1) * ratio), float32.length)
		let sum = 0

		for (let j = start; j < end; j++) {
			sum += float32[j]
		}

		const sample = Math.max(-1, Math.min(1, sum / Math.max(1, end - start)))
		pcm[i] = sample < 0 ? sample * 0x8000 : sample * 0x7fff
	}

	return pcm
}

function arrayBufferToBase64(buffer) {
	let binary = ''
	const bytes = new Uint8Array(buffer)
	const chunkSize = 0x8000

	for (let i = 0; i < bytes.length; i += chunkSize) {
		binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize))
	}

	return btoa(binary)
}

function base64ToInt16Array(base64) {
	const binary = atob(base64)
	const bytes = new Uint8Array(binary.length)

	for (let i = 0; i < binary.length; i++) {
		bytes[i] = binary.charCodeAt(i)
	}

	return new Int16Array(bytes.buffer)
}

function handleLiveMessage(message) {
	if (message?.serverContent?.turnComplete || message?.serverContent?.interrupted) {
		lastTurnWasComplete = true
	}

	const inputText = message?.serverContent?.inputTranscription?.text
	const outputText = message?.serverContent?.outputTranscription?.text

	if (inputText) {
		appendLine('user', inputText, false)
	}

	if (outputText) {
		appendLine('assistant', outputText, !lastTurnWasComplete)
		lastTurnWasComplete = false
	}

	const parts = message?.serverContent?.modelTurn?.parts || []

	for (const part of parts) {
		const inline = part.inlineData || part.inline_data

		if (inline?.data && inline?.mimeType?.startsWith('audio')) {
			playAudio(inline.data, inline.mimeType)
		}
	}
}

function playAudio(data, mimeType) {
	if (!data) return

	const rateMatch = String(mimeType || '').match(/rate=(\d+)/)
	const sampleRate = rateMatch ? Number(rateMatch[1]) : 24000
	const context = outputAudioContext.value || new AudioContext({ sampleRate })

	outputAudioContext.value = context

	const pcm = base64ToInt16Array(data)

	if (!pcm.length) return

	const buffer = context.createBuffer(1, pcm.length, sampleRate)
	const channel = buffer.getChannelData(0)

	for (let i = 0; i < pcm.length; i++) {
		channel[i] = pcm[i] / 32768
	}

	const source = context.createBufferSource()
	source.buffer = buffer
	source.connect(context.destination)

	const startAt = Math.max(context.currentTime, outputPlayTime.value || 0)

	source.start(startAt)
	outputPlayTime.value = startAt + buffer.duration
}

async function stopLiveVoice() {
	manualLiveStop = true
	stopMicrophoneOnly()

	try {
		liveSession.value?.close?.(1000, 'manual-stop')
	} catch {}

	liveSession.value = null
	liveConnected.value = false
	liveSocketOpen.value = false
}

function stopMicrophoneOnly() {
	audioStreaming.value = false

	try {
		if (microphoneProcessor.value) microphoneProcessor.value.onaudioprocess = null
		microphoneProcessor.value?.disconnect()
		microphoneSource.value?.disconnect()
	} catch {}

	mediaStream.value?.getTracks?.().forEach((track) => track.stop())

	const context = inputAudioContext.value

	if (context && context.state !== 'closed') {
		context.close().catch(() => {})
	}

	mediaStream.value = null
	inputAudioContext.value = null
	microphoneSource.value = null
	microphoneProcessor.value = null
	micEnabled.value = false
}
</script>

<style scoped>
.room-page {
	--room-bg: #f3f6fb;
	--room-surface: #ffffff;
	--room-surface-soft: #f8fafc;
	--room-ink: #071632;
	--room-muted: #526173;
	--room-soft: #7b8aa0;
	--room-border: #d9e4f2;
	--room-border-strong: #c7d6ea;
	--room-primary: #0a2251;
	--room-primary-hover: #12336f;
	--room-primary-soft: #e9f0fb;
	--room-green: #16a34a;
	--room-red: #dc2626;
	--room-red-soft: #fef2f2;
	--room-yellow: #f7c948;
	--room-shadow: 0 18px 48px rgba(7, 22, 50, 0.1);

	display: flex;
	height: 100vh;
	height: 100dvh;
	min-height: 100vh;
	flex-direction: column;
	background: var(--room-bg);
	color: var(--room-ink);
	overflow: hidden;
}

.room-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	min-height: 76px;
	padding: 0.9rem 1.1rem;
	border-bottom: 1px solid var(--room-border);
	background: rgba(255, 255, 255, 0.96);
	box-shadow: 0 10px 30px rgba(7, 22, 50, 0.04);
}

.room-header-left {
	min-width: 0;
}

.room-kicker {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	color: var(--room-primary);
	font-size: 0.7rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.room-live-dot {
	width: 8px;
	height: 8px;
	border-radius: 999px;
	background: #94a3b8;
}

.room-live-dot.active {
	background: var(--room-green);
	box-shadow: 0 0 0 6px rgba(22, 163, 74, 0.12);
}

.room-header h1 {
	margin: 0.18rem 0 0;
	max-width: 54vw;
	overflow: hidden;
	color: var(--room-ink);
	font-size: 1.08rem;
	font-weight: 950;
	line-height: 1.25;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.room-meta {
	display: flex;
	align-items: center;
	gap: 0.45rem;
	flex-wrap: wrap;
	margin-top: 0.45rem;
}

.room-meta span,
.message-count {
	display: inline-flex;
	align-items: center;
	border: 1px solid var(--room-border);
	border-radius: 999px;
	background: var(--room-surface-soft);
	padding: 0.25rem 0.55rem;
	color: var(--room-muted);
	font-size: 0.72rem;
	font-weight: 850;
}

.room-header-actions {
	display: flex;
	align-items: center;
	gap: 0.6rem;
	flex: 0 0 auto;
}

.room-layout {
	display: grid;
	flex: 1;
	grid-template-columns: minmax(0, 1fr) minmax(350px, 420px);
	gap: 1rem;
	min-height: 0;
	padding: 1rem;
	overflow: hidden;
}

.room-stage {
	display: flex;
	min-width: 0;
	min-height: 0;
	flex-direction: column;
	gap: 1rem;
	position: relative;
}

.meeting-grid {
	display: grid;
	flex: 1;
	grid-template-columns: minmax(0, 1fr) minmax(230px, 285px);
	gap: 1rem;
	min-height: 0;
}

.ai-tile,
.user-tile,
.practice-card,
.side-section,
.feedback-panel {
	border: 1px solid var(--room-border);
	background: var(--room-surface);
	box-shadow: var(--room-shadow);
}

.ai-tile,
.user-tile,
.practice-card {
	position: relative;
	overflow: hidden;
	border-radius: 24px;
}

.ai-tile {
	display: flex;
	min-height: 420px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	border-color: #16356b;
	background: var(--room-primary);
	padding: 2rem;
	text-align: center;
	color: #ffffff;
}

.tile-topbar,
.user-tile-top {
	position: absolute;
	z-index: 2;
	top: 1rem;
	left: 1rem;
	right: 1rem;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.75rem;
}

.tile-status,
.call-time {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	min-height: 30px;
	border: 1px solid rgba(255, 255, 255, 0.16);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.1);
	padding: 0.35rem 0.65rem;
	color: #eff6ff;
	font-size: 0.72rem;
	font-weight: 900;
	white-space: nowrap;
}

.user-tile .tile-status,
.practice-card .tile-status {
	border-color: var(--room-border);
	background: var(--room-surface-soft);
	color: var(--room-muted);
}

.tile-status span {
	width: 8px;
	height: 8px;
	border-radius: 999px;
	background: #94a3b8;
}

.tile-status.live span {
	background: var(--room-green);
	box-shadow: 0 0 0 6px rgba(22, 163, 74, 0.14);
}

.ai-avatar-wrap {
	position: relative;
	z-index: 1;
}

.ai-avatar,
.user-avatar {
	display: grid;
	place-items: center;
	border-radius: 999px;
	transition: 0.3s ease;
}

.ai-avatar {
	width: 150px;
	height: 150px;
	border: 1px solid rgba(255, 255, 255, 0.22);
	background: #ffffff;
	color: var(--room-primary);
	box-shadow: 0 20px 58px rgba(0, 0, 0, 0.22);
}

.ai-avatar.speaking {
	animation: pulse-ring 1.55s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}

@keyframes pulse-ring {
	0% {
		box-shadow:
			0 0 0 0 rgba(255, 255, 255, 0.46),
			0 20px 58px rgba(0, 0, 0, 0.22);
	}

	70% {
		box-shadow:
			0 0 0 30px rgba(255, 255, 255, 0),
			0 20px 58px rgba(0, 0, 0, 0.22);
	}

	100% {
		box-shadow:
			0 0 0 0 rgba(255, 255, 255, 0),
			0 20px 58px rgba(0, 0, 0, 0.22);
	}
}

.tile-info {
	position: relative;
	z-index: 1;
}

.ai-tile h2,
.user-tile h3,
.practice-card h3 {
	margin: 1rem 0 0;
	font-size: 1.4rem;
	font-weight: 950;
	letter-spacing: -0.035em;
}

.ai-tile h2 {
	color: #ffffff;
}

.ai-tile p,
.user-tile p,
.practice-card p {
	margin: 0.5rem auto 0;
	max-width: 36rem;
	font-size: 0.95rem;
	line-height: 1.6;
}

.ai-tile p {
	color: #dbeafe;
}

.user-tile p,
.practice-card p {
	color: var(--room-muted);
}

.participant-column {
	display: flex;
	min-height: 0;
	flex-direction: column;
	gap: 1rem;
}

.user-tile {
	display: flex;
	min-height: 255px;
	flex: 1;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 1rem;
	text-align: center;
}

.user-avatar {
	width: 92px;
	height: 92px;
	background: var(--room-primary-soft);
	color: var(--room-primary);
	box-shadow: 0 0 0 10px #f4f7fc;
}

.user-tile h3,
.practice-card h3 {
	color: var(--room-ink);
}

.practice-card {
	padding: 1rem;
	min-height: 155px;
}

.practice-card h3 {
	font-size: 1rem;
}

.practice-card p {
	font-size: 0.88rem;
}

.tile-name-bar {
	position: absolute;
	left: 1rem;
	right: 1rem;
	bottom: 1rem;
	z-index: 2;
	display: flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	max-width: calc(100% - 2rem);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.12);
	padding: 0.45rem 0.7rem;
	color: #ffffff;
	font-size: 0.78rem;
	font-weight: 900;
}

.tile-name-bar.user {
	border: 1px solid var(--room-border);
	background: var(--room-surface-soft);
	color: var(--room-muted);
}

.room-controls {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 0.65rem;
	width: fit-content;
	max-width: 100%;
	margin: 0 auto;
	border: 1px solid var(--room-border);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.96);
	padding: 0.6rem;
	box-shadow: var(--room-shadow);
}

.control-btn,
.room-primary,
.room-ghost,
.room-danger,
.side-icon {
	border: 0;
	cursor: pointer;
	text-decoration: none;
}

.control-btn,
.room-primary,
.room-ghost,
.room-danger {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	min-height: 44px;
	border-radius: 999px;
	padding: 0.7rem 1rem;
	font-size: 0.88rem;
	font-weight: 950;
	transition: 0.18s ease;
	white-space: nowrap;
}

.control-btn {
	border: 1px solid var(--room-border);
	background: var(--room-surface-soft);
	color: var(--room-primary);
}

.control-btn:hover {
	border-color: var(--room-border-strong);
	background: #eef4fc;
	transform: translateY(-1px);
}

.control-btn.active,
.control-btn.mic.active {
	border-color: var(--room-red);
	background: var(--room-red-soft);
	color: var(--room-red);
}

.control-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
}

.room-primary {
	width: 100%;
	border: 1px solid var(--room-primary);
	background: var(--room-primary);
	color: #ffffff;
}

.room-primary:hover:not(:disabled) {
	background: var(--room-primary-hover);
	transform: translateY(-1px);
}

.room-primary:disabled,
.room-danger:disabled,
.control-btn:disabled {
	cursor: not-allowed;
	opacity: 0.58;
}

.room-ghost {
	border: 1px solid var(--room-border);
	background: var(--room-surface-soft);
	color: var(--room-primary);
}

.room-ghost:hover {
	background: #eef4fc;
}

.room-danger {
	border: 1px solid var(--room-red);
	background: var(--room-red);
	color: #ffffff;
}

.room-danger:hover:not(:disabled) {
	background: #b91c1c;
}

.room-warning {
	display: flex;
	align-items: flex-start;
	gap: 0.55rem;
	border: 1px solid #f8d677;
	border-radius: 18px;
	background: #fff8db;
	color: #7a5400;
	padding: 0.85rem 1rem;
	font-size: 0.88rem;
	line-height: 1.5;
}

.room-side {
	display: flex;
	min-width: 0;
	min-height: 0;
	flex-direction: column;
	gap: 1rem;
}

.side-section {
	min-height: 0;
	overflow: hidden;
	border-radius: 24px;
}

.transcript-section {
	display: flex;
	flex: 1;
	flex-direction: column;
	min-height: 0;
}

.side-head {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	border-bottom: 1px solid var(--room-border);
	padding: 1rem;
	background: var(--room-surface);
}

.side-head.compact {
	padding-bottom: 0.85rem;
}

.side-head h2 {
	margin: 0.2rem 0 0;
	color: var(--room-ink);
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.02em;
}

.side-actions {
	display: flex;
	align-items: center;
	gap: 0.5rem;
}

.side-icon {
	display: grid;
	place-items: center;
	width: 36px;
	height: 36px;
	border: 1px solid var(--room-border);
	border-radius: 999px;
	background: var(--room-surface-soft);
	color: var(--room-primary);
	transition: 0.18s ease;
}

.side-icon:hover {
	background: #eef4fc;
}

.transcript-box {
	flex: 1;
	min-height: 0;
	overflow-y: auto;
	padding: 1rem;
	background: #fbfdff;
	scrollbar-width: thin;
	scrollbar-color: rgba(123, 138, 160, 0.5) transparent;
}

.empty-transcript {
	display: flex;
	height: 100%;
	min-height: 260px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	color: var(--room-soft);
	text-align: center;
}

.empty-icon {
	display: grid;
	place-items: center;
	width: 72px;
	height: 72px;
	margin-bottom: 1rem;
	border: 1px solid var(--room-border);
	border-radius: 24px;
	background: var(--room-primary-soft);
	color: var(--room-primary);
}

.empty-transcript h3 {
	margin: 0;
	color: var(--room-ink);
	font-size: 1rem;
	font-weight: 950;
}

.empty-transcript p {
	max-width: 260px;
	margin: 0.45rem 0 0;
	color: var(--room-soft);
	font-size: 0.88rem;
	line-height: 1.5;
}

.transcript-line {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	margin-bottom: 0.85rem;
}

.transcript-line.user {
	align-items: flex-end;
}

.line-role {
	margin-bottom: 0.3rem;
	color: var(--room-primary);
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.transcript-line.user .line-role {
	color: #9a6700;
}

.line-content {
	max-width: 88%;
	border: 1px solid var(--room-border);
	border-radius: 18px 18px 18px 6px;
	background: #ffffff;
	color: var(--room-ink);
	padding: 0.75rem 0.85rem;
	font-size: 0.9rem;
	line-height: 1.55;
	word-break: break-word;
	box-shadow: 0 8px 22px rgba(7, 22, 50, 0.05);
}

.transcript-line.user .line-content {
	border-color: var(--room-primary);
	border-radius: 18px 18px 6px 18px;
	background: var(--room-primary);
	color: #ffffff;
}

.chat-compose {
	border-top: 1px solid var(--room-border);
	padding: 1rem;
	background: var(--room-surface);
	flex-shrink: 0;
}

.chat-compose textarea,
.notes-area {
	width: 100%;
	resize: vertical;
	border: 1px solid var(--room-border);
	border-radius: 16px;
	background: var(--room-surface-soft);
	color: var(--room-ink);
	padding: 0.8rem;
	outline: none;
	font-size: 0.9rem;
	line-height: 1.5;
	transition: 0.18s ease;
}

.chat-compose textarea:focus,
.notes-area:focus {
	border-color: var(--room-primary);
	box-shadow: 0 0 0 4px rgba(10, 34, 81, 0.1);
}

.chat-compose textarea::placeholder,
.notes-area::placeholder {
	color: var(--room-soft);
}

.chat-compose .room-primary {
	margin-top: 0.65rem;
}

.notes-section {
	flex: 0 0 auto;
}

.notes-area {
	min-height: 135px;
	border: 0;
	border-top: 1px solid var(--room-border);
	border-radius: 0;
}

.feedback-panel {
	border-radius: 24px;
	padding: 1rem;
	color: var(--room-ink);
}

.feedback-head {
	display: flex;
	align-items: center;
	gap: 1rem;
}

.feedback-score-wrap {
	display: flex;
	align-items: center;
	gap: 0.7rem;
	flex: 0 0 auto;
	border: 1px solid #f0d674;
	border-radius: 999px;
	background: #fff8db;
	padding: 0.45rem 0.8rem 0.45rem 0.45rem;
	color: #5d4300;
	font-size: 0.82rem;
	font-weight: 950;
}

.feedback-score {
	display: grid;
	place-items: center;
	width: 64px;
	height: 64px;
	border-radius: 999px;
	background: var(--room-yellow);
	color: #392800;
	font-size: 1.65rem;
	font-weight: 950;
	flex: 0 0 auto;
}

.feedback-copy {
	min-width: 0;
}

.feedback-panel h2 {
	margin: 0.2rem 0 0;
	color: var(--room-ink);
	font-size: 1.25rem;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.feedback-panel p {
	margin: 0.45rem 0 0;
	color: var(--room-muted);
	line-height: 1.6;
}

.feedback-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 0.85rem;
	margin-top: 1rem;
}

.feedback-card {
	border: 1px solid var(--room-border);
	border-radius: 18px;
	background: var(--room-surface-soft);
	padding: 1rem;
}

.feedback-grid h3 {
	margin: 0;
	color: var(--room-primary);
	font-size: 0.82rem;
	font-weight: 950;
	text-transform: uppercase;
	letter-spacing: 0.06em;
}

.feedback-grid ul {
	margin: 0.55rem 0 0;
	padding-left: 1rem;
	color: var(--room-muted);
	font-size: 0.88rem;
	line-height: 1.6;
}

.better-answer {
	margin-top: 1rem;
	border: 1px solid var(--room-border);
	border-radius: 18px;
	background: #fbfdff;
	padding: 1rem;
}

.better-answer strong {
	color: var(--room-ink);
	font-size: 0.9rem;
	font-weight: 950;
}

@media (max-width: 1180px) {
	.room-page {
		height: auto;
		min-height: 100vh;
		overflow: visible;
	}

	.room-layout {
		grid-template-columns: 1fr;
		min-height: auto;
		overflow: visible;
	}

	.room-stage {
		min-height: auto;
	}

	.meeting-grid {
		grid-template-columns: minmax(0, 1fr) minmax(220px, 270px);
		min-height: 520px;
	}

	.room-side {
		min-height: 560px;
	}

	.transcript-section {
		min-height: 520px;
	}
}

@media (max-width: 820px) {
	.meeting-grid {
		grid-template-columns: 1fr;
		min-height: auto;
	}

	.ai-tile {
		min-height: 380px;
	}

	.participant-column {
		display: grid;
		grid-template-columns: 1fr 1fr;
	}

	.user-tile,
	.practice-card {
		min-height: 190px;
	}

	.room-controls {
		position: sticky;
		bottom: 0.75rem;
		z-index: 10;
	}
}

@media (max-width: 640px) {
	.room-page {
		min-height: 100vh;
	}

	.room-header {
		align-items: stretch;
		flex-direction: column;
		gap: 0.8rem;
		min-height: auto;
		padding: 0.9rem;
	}

	.room-header h1 {
		max-width: 100%;
		white-space: normal;
		font-size: 1rem;
		line-height: 1.35;
	}

	.room-header-actions {
		display: grid;
		grid-template-columns: 0.85fr 1.15fr;
		width: 100%;
	}

	.room-ghost,
	.room-danger {
		width: 100%;
		min-height: 42px;
		padding: 0.6rem 0.7rem;
		font-size: 0.8rem;
	}

	.room-layout {
		gap: 0.85rem;
		padding: 0.75rem;
	}

	.ai-tile,
	.user-tile,
	.practice-card,
	.side-section,
	.feedback-panel {
		border-radius: 18px;
	}

	.ai-tile {
		min-height: 310px;
		padding: 1.2rem;
	}

	.tile-topbar,
	.user-tile-top {
		top: 0.75rem;
		left: 0.75rem;
		right: 0.75rem;
	}

	.tile-status,
	.call-time {
		min-height: 28px;
		padding: 0.32rem 0.55rem;
		font-size: 0.68rem;
	}

	.ai-avatar {
		width: 108px;
		height: 108px;
	}

	.ai-tile h2 {
		font-size: 1.15rem;
	}

	.ai-tile p {
		max-width: 100%;
		font-size: 0.84rem;
	}

	.tile-name-bar {
		left: 0.75rem;
		right: 0.75rem;
		bottom: 0.75rem;
	}

	.participant-column {
		grid-template-columns: 1fr;
	}

	.user-tile {
		min-height: 145px;
		padding: 1rem;
	}

	.practice-card {
		min-height: auto;
	}

	.user-avatar {
		width: 62px;
		height: 62px;
	}

	.user-tile h3,
	.practice-card h3 {
		font-size: 1rem;
	}

	.user-tile p,
	.practice-card p {
		font-size: 0.8rem;
	}

	.room-controls {
		display: grid;
		grid-template-columns: 1fr;
		width: 100%;
		border-radius: 18px;
		padding: 0.75rem;
	}

	.control-btn {
		width: 100%;
		min-height: 46px;
	}

	.room-side {
		min-height: auto;
	}

	.transcript-section {
		height: 540px;
		min-height: 540px;
		max-height: none;
	}

	.side-head {
		padding: 0.85rem;
	}

	.side-actions .message-count {
		display: none;
	}

	.transcript-box {
		padding: 0.85rem;
	}

	.line-content {
		max-width: 92%;
		font-size: 0.86rem;
	}

	.chat-compose {
		padding: 0.85rem;
	}

	.chat-compose textarea {
		min-height: 96px;
	}

	.notes-area {
		min-height: 130px;
	}

	.feedback-head {
		align-items: flex-start;
		flex-direction: column;
	}

	.feedback-score-wrap {
		width: 100%;
	}

	.feedback-grid {
		grid-template-columns: 1fr;
	}
}
</style>

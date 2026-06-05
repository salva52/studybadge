<template>
	<div class="room-page">
		<header class="room-header">
			<div class="room-header-left">
				<div class="room-kicker">
					<span class="room-live-dot" :class="{ active: liveConnected }"></span>
					{{ liveConnected ? __('Voz Live activa') : __('Simulación IA') }}
				</div>

				<h1>{{ session?.title || __('Sala de práctica') }}</h1>
			</div>

			<div class="room-header-actions">
				<button class="room-ghost" @click="saveTranscript">
					<Save class="size-4" />
					<span>{{ __('Guardar') }}</span>
				</button>

				<button class="room-danger" :disabled="finishing" @click="finishSession">
					<Square class="size-4" />
					<span>{{ finishing ? __('Finalizando...') : __('Finalizar') }}</span>
				</button>
			</div>
		</header>

		<main class="room-layout">
			<section class="room-stage">
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
								{{ __('La IA hará preguntas, retará tus respuestas y mantendrá la simulación.') }}
							</p>
						</div>

						<div class="tile-name-bar">
							<Bot class="size-4" />
							<span>{{ interviewerLabel }}</span>
						</div>
					</div>

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
							{{ micEnabled ? __('Estás respondiendo por voz') : __('Puedes responder por texto o activar voz') }}
						</p>

						<div class="tile-name-bar user">
							<User class="size-4" />
							<span>{{ __('Tú') }}</span>
						</div>
					</div>
				</div>

				<div v-if="liveError" class="room-warning">
					<CircleAlert class="size-4" />
					<span>{{ liveError }}</span>
				</div>

				<div v-if="feedback && Object.keys(feedback).length" class="feedback-panel">
					<div class="feedback-head">
						<div class="feedback-score">{{ feedback.score || 0 }}</div>

						<div>
							<div class="room-kicker">{{ __('Resultado') }}</div>
							<h2>{{ __('Feedback final') }}</h2>
							<p>{{ feedback.summary }}</p>
						</div>
					</div>

					<div class="feedback-grid">
						<div class="feedback-card">
							<h3>{{ __('Fortalezas') }}</h3>
							<ul>
								<li v-for="item in feedback.strengths || []" :key="item">
									{{ item }}
								</li>
							</ul>
						</div>

						<div class="feedback-card">
							<h3>{{ __('Mejoras') }}</h3>
							<ul>
								<li v-for="item in feedback.improvements || []" :key="item">
									{{ item }}
								</li>
							</ul>
						</div>

						<div class="feedback-card">
							<h3>{{ __('Siguientes pasos') }}</h3>
							<ul>
								<li v-for="item in feedback.next_steps || []" :key="item">
									{{ item }}
								</li>
							</ul>
						</div>
					</div>

					<div v-if="feedback.sample_better_answer" class="better-answer">
						<strong>{{ __('Ejemplo de mejor respuesta') }}</strong>
						<p>{{ feedback.sample_better_answer }}</p>
					</div>
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

						<button class="side-icon" @click="saveTranscript" aria-label="Guardar transcripción">
							<Save class="size-4" />
						</button>
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
					<div class="side-head">
						<div>
							<div class="room-kicker">{{ __('Notas') }}</div>
							<h2>{{ __('Apuntes privados') }}</h2>
						</div>
					</div>

					<textarea
						v-model="notes"
						class="notes-area"
						rows="7"
						:placeholder="__('Anota preguntas difíciles, ideas o respuestas para mejorar.')"
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

let speakingInterval = null
let lastTurnWasComplete = true

onMounted(() => {
	loadSession()

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
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo abrir la práctica.'))
	}
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
		sales: __('Hola, me gustaría entender mejor tu situación antes de proponerte una solución.'),
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

async function saveTranscript() {
	try {
		await call('studybadge_ai.ai_practice.save_practice_transcript', {
			session: props.sessionId,
			transcript: JSON.stringify(transcript.value),
		})

		toast.success(__('Transcripción guardada.'))
	} catch (error) {
		toast.error(error.messages?.[0] || __('No se pudo guardar.'))
	}
}

async function finishSession() {
	finishing.value = true

	await stopLiveVoice()

	try {
		await saveTranscript()

		const result = await call('studybadge_ai.ai_practice.finish_practice_session', {
			session: props.sessionId,
		})

		feedback.value = result.feedback
		session.value = result.session

		toast.success(__('Práctica finalizada.'))
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

	try {
		const token = await call('studybadge_ai.ai_practice.create_live_token', {
			session: props.sessionId,
		})

		if (!token.live_supported || !token.token) {
			liveError.value = token.message || __('Voz no disponible. ContinÃºa por texto.')
			liveLoading.value = false
			return
		}

		const liveEndpoint =
			token.endpoint ||
			'wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContentConstrained'
		const url = `${liveEndpoint}?access_token=${encodeURIComponent(token.token)}`
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
					liveError.value = data.error.message || 'Error en servidor'
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
			liveError.value = `Conexión cerrada: ${event.code} - ${event.reason || 'Sin razón específica'}`
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
	stopMicrophoneOnly()

	try {
		liveSession.value?.close?.()
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
	--room-bg: #070b14;
	--room-panel: #111827;
	--room-panel-2: #0b1220;
	--room-panel-3: #151f32;
	--room-border: rgba(255, 255, 255, 0.1);
	--room-border-strong: rgba(255, 255, 255, 0.18);
	--room-text: #f8fafc;
	--room-muted: #cbd5e1;
	--room-soft: #94a3b8;
	--room-primary: #0a2251;
	--room-blue: #2563eb;
	--room-blue-soft: rgba(37, 99, 235, 0.14);
	--room-green: #22c55e;
	--room-red: #ef4444;
	--room-yellow: #f5b301;
	--room-shadow: 0 24px 70px rgba(0, 0, 0, 0.34);

	display: flex;
	height: 100vh;
	height: 100dvh;
	min-height: 100vh;
	flex-direction: column;
	background: var(--room-bg);
	color: var(--room-text);
	overflow: hidden;
}

.room-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	min-height: 72px;
	padding: 0.85rem 1rem;
	border-bottom: 1px solid var(--room-border);
	background: rgba(7, 11, 20, 0.92);
	backdrop-filter: blur(18px);
}

.room-header-left {
	min-width: 0;
}

.room-kicker {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	color: #93c5fd;
	font-size: 0.7rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.room-live-dot {
	width: 8px;
	height: 8px;
	border-radius: 999px;
	background: #64748b;
}

.room-live-dot.active {
	background: var(--room-green);
	box-shadow: 0 0 0 6px rgba(34, 197, 94, 0.14);
}

.room-header h1 {
	margin: 0.2rem 0 0;
	max-width: 56vw;
	overflow: hidden;
	color: #ffffff;
	font-size: 1.08rem;
	font-weight: 900;
	line-height: 1.25;
	text-overflow: ellipsis;
	white-space: nowrap;
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
	grid-template-columns: minmax(0, 1fr) minmax(360px, 410px);
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
	grid-template-columns: minmax(0, 1fr) 260px;
	gap: 1rem;
	min-height: 0;
}

.ai-tile,
.user-tile,
.side-section,
.feedback-panel {
	border: 1px solid var(--room-border);
	background: var(--room-panel);
	box-shadow: var(--room-shadow);
}

.ai-tile,
.user-tile {
	position: relative;
	overflow: hidden;
	border-radius: 22px;
}

.ai-tile {
	display: flex;
	min-height: 420px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 2rem;
	text-align: center;
}

.ai-tile::before {
	content: "";
	position: absolute;
	inset: auto -30% -34% -30%;
	height: 44%;
	background: radial-gradient(circle, rgba(37, 99, 235, 0.44), transparent 62%);
	pointer-events: none;
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
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 999px;
	background: rgba(15, 23, 42, 0.68);
	padding: 0.35rem 0.65rem;
	color: #dbeafe;
	font-size: 0.72rem;
	font-weight: 850;
	backdrop-filter: blur(12px);
	white-space: nowrap;
}

.tile-status span {
	width: 8px;
	height: 8px;
	border-radius: 999px;
	background: #94a3b8;
}

.tile-status.live span {
	background: var(--room-green);
	box-shadow: 0 0 0 6px rgba(34, 197, 94, 0.14);
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
	color: #ffffff;
	transition: 0.3s ease;
}

.ai-avatar {
	width: 150px;
	height: 150px;
	background: #2563eb;
	box-shadow:
		0 0 0 12px rgba(37, 99, 235, 0.12),
		0 24px 80px rgba(37, 99, 235, 0.28);
}

.ai-avatar.speaking {
	animation: pulse-ring 1.55s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}

@keyframes pulse-ring {
	0% {
		box-shadow:
			0 0 0 0 rgba(37, 99, 235, 0.65),
			0 0 0 12px rgba(37, 99, 235, 0.12),
			0 24px 80px rgba(37, 99, 235, 0.28);
	}

	70% {
		box-shadow:
			0 0 0 30px rgba(37, 99, 235, 0),
			0 0 0 12px rgba(37, 99, 235, 0.12),
			0 24px 80px rgba(37, 99, 235, 0.28);
	}

	100% {
		box-shadow:
			0 0 0 0 rgba(37, 99, 235, 0),
			0 0 0 12px rgba(37, 99, 235, 0.12),
			0 24px 80px rgba(37, 99, 235, 0.28);
	}
}

.tile-info {
	position: relative;
	z-index: 1;
}

.ai-tile h2,
.user-tile h3 {
	margin: 1rem 0 0;
	color: #ffffff;
	font-size: 1.4rem;
	font-weight: 950;
	letter-spacing: -0.035em;
}

.ai-tile p,
.user-tile p {
	margin: 0.5rem auto 0;
	max-width: 36rem;
	color: var(--room-muted);
	font-size: 0.95rem;
	line-height: 1.6;
}

.user-tile {
	display: flex;
	min-height: 220px;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 1rem;
	text-align: center;
}

.user-avatar {
	width: 92px;
	height: 92px;
	background: #1f2937;
	box-shadow: 0 0 0 10px rgba(255, 255, 255, 0.05);
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
	background: rgba(0, 0, 0, 0.42);
	padding: 0.45rem 0.7rem;
	color: #ffffff;
	font-size: 0.78rem;
	font-weight: 850;
	backdrop-filter: blur(12px);
}

.tile-name-bar.user {
	background: rgba(255, 255, 255, 0.08);
}

.room-controls {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 0.75rem;
	width: fit-content;
	max-width: 100%;
	margin: 0 auto;
	border: 1px solid var(--room-border);
	border-radius: 999px;
	background: rgba(15, 23, 42, 0.88);
	padding: 0.6rem;
	box-shadow: 0 18px 46px rgba(0, 0, 0, 0.34);
	backdrop-filter: blur(16px);
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
	font-weight: 900;
	transition: 0.18s ease;
	white-space: nowrap;
}

.control-btn {
	border: 1px solid rgba(255, 255, 255, 0.12);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
}

.control-btn:hover {
	background: rgba(255, 255, 255, 0.14);
	transform: translateY(-1px);
}

.control-btn.active,
.control-btn.mic.active {
	border-color: var(--room-red);
	background: var(--room-red);
	color: #ffffff;
}

.control-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
}

.room-primary {
	width: 100%;
	border: 1px solid var(--room-blue);
	background: var(--room-blue);
	color: #ffffff;
}

.room-primary:hover:not(:disabled) {
	background: #1d4ed8;
	transform: translateY(-1px);
}

.room-primary:disabled,
.room-danger:disabled,
.control-btn:disabled {
	cursor: not-allowed;
	opacity: 0.58;
}

.room-ghost {
	border: 1px solid rgba(255, 255, 255, 0.14);
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
}

.room-ghost:hover {
	background: rgba(255, 255, 255, 0.14);
}

.room-danger {
	border: 1px solid var(--room-red);
	background: var(--room-red);
	color: #ffffff;
}

.room-danger:hover:not(:disabled) {
	background: #dc2626;
}

.room-warning {
	display: flex;
	align-items: flex-start;
	gap: 0.55rem;
	border: 1px solid rgba(251, 191, 36, 0.32);
	border-radius: 18px;
	background: rgba(251, 191, 36, 0.12);
	color: #fde68a;
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
	border-radius: 22px;
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
	background: rgba(255, 255, 255, 0.02);
}

.side-head h2 {
	margin: 0.2rem 0 0;
	color: #ffffff;
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.02em;
}

.side-icon {
	display: grid;
	place-items: center;
	width: 36px;
	height: 36px;
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.08);
	color: #ffffff;
	transition: 0.18s ease;
}

.side-icon:hover {
	background: rgba(255, 255, 255, 0.14);
}

.transcript-box {
	flex: 1;
	min-height: 0;
	overflow-y: auto;
	padding: 1rem;
	scrollbar-width: thin;
	scrollbar-color: rgba(148, 163, 184, 0.5) transparent;
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
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.06);
	color: #93c5fd;
}

.empty-transcript h3 {
	margin: 0;
	color: #ffffff;
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
	color: #93c5fd;
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.transcript-line.user .line-role {
	color: #fbbf24;
}

.line-content {
	max-width: 88%;
	border-radius: 18px 18px 18px 6px;
	background: rgba(255, 255, 255, 0.08);
	color: #e5e7eb;
	padding: 0.75rem 0.85rem;
	font-size: 0.9rem;
	line-height: 1.55;
	word-break: break-word;
}

.transcript-line.user .line-content {
	border-radius: 18px 18px 6px 18px;
	background: var(--room-blue);
	color: #ffffff;
}

.chat-compose {
	border-top: 1px solid var(--room-border);
	padding: 1rem;
	background: rgba(255, 255, 255, 0.02);
	flex-shrink: 0;
}

.chat-compose textarea,
.notes-area {
	width: 100%;
	resize: vertical;
	border: 1px solid var(--room-border);
	border-radius: 16px;
	background: var(--room-panel-2);
	color: #ffffff;
	padding: 0.8rem;
	outline: none;
	font-size: 0.9rem;
	line-height: 1.5;
	transition: 0.18s ease;
}

.chat-compose textarea:focus,
.notes-area:focus {
	border-color: rgba(37, 99, 235, 0.8);
	box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.chat-compose textarea::placeholder,
.notes-area::placeholder {
	color: #64748b;
}

.chat-compose .room-primary {
	margin-top: 0.65rem;
}

.notes-section {
	flex: 0 0 auto;
}

.notes-area {
	min-height: 150px;
	border: 0;
	border-top: 1px solid var(--room-border);
	border-radius: 0;
}

.feedback-panel {
	border-radius: 22px;
	padding: 1rem;
	color: #e5e7eb;
}

.feedback-head {
	display: flex;
	align-items: center;
	gap: 1rem;
}

.feedback-score {
	display: grid;
	place-items: center;
	width: 74px;
	height: 74px;
	border-radius: 999px;
	background: var(--room-yellow);
	color: #3b2a00;
	font-size: 1.8rem;
	font-weight: 950;
	flex: 0 0 auto;
}

.feedback-panel h2 {
	margin: 0.2rem 0 0;
	color: #ffffff;
	font-size: 1.25rem;
	font-weight: 950;
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
	background: rgba(255, 255, 255, 0.05);
	padding: 1rem;
}

.feedback-grid h3 {
	margin: 0;
	color: #93c5fd;
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
	background: rgba(255, 255, 255, 0.06);
	padding: 1rem;
}

.better-answer strong {
	color: #ffffff;
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
		grid-template-columns: minmax(0, 1fr) 240px;
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

	.user-tile {
		min-height: 180px;
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
		grid-template-columns: 1fr 1fr;
		width: 100%;
	}

	.room-ghost,
	.room-danger {
		width: 100%;
		min-height: 40px;
		padding: 0.6rem 0.75rem;
		font-size: 0.82rem;
	}

	.room-layout {
		gap: 0.85rem;
		padding: 0.75rem;
	}

	.ai-tile,
	.user-tile,
	.side-section,
	.feedback-panel {
		border-radius: 18px;
	}

	.ai-tile {
		min-height: 300px;
		padding: 1.2rem;
	}

	.tile-topbar {
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

	.user-tile {
		min-height: 135px;
		padding: 1rem;
	}

	.user-avatar {
		width: 62px;
		height: 62px;
	}

	.user-tile h3 {
		font-size: 1rem;
	}

	.user-tile p {
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
		height: 520px;
		min-height: 520px;
		max-height: none;
	}

	.side-head {
		padding: 0.85rem;
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

	.feedback-grid {
		grid-template-columns: 1fr;
	}
}
</style>

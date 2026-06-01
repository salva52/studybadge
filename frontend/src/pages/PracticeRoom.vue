<template>
	<div class="room-page min-h-screen">
		<header class="room-header">
			<div class="min-w-0">
				<div class="room-kicker">{{ __('Simulación IA') }}</div>
				<h1>{{ session?.title || __('Sala de práctica') }}</h1>
			</div>
			<div class="room-header-actions">
				<button class="room-ghost" @click="saveTranscript">
					<Save class="size-4" /> {{ __('Guardar') }}
				</button>
				<button class="room-danger" :disabled="finishing" @click="finishSession">
					<Square class="size-4" /> {{ finishing ? __('Finalizando...') : __('Finalizar') }}
				</button>
			</div>
		</header>

		<main class="room-layout">
			<section class="room-stage">
				<div class="meeting-grid">
					<div class="ai-tile">
						<div class="tile-status" :class="{ live: liveConnected }">
							<span></span>{{ liveConnected ? __('Voz Live activa') : __('Modo chat') }}
						</div>
						<div class="call-time">
							<Radio class="size-4" /> {{ micEnabled ? __('Escuchando') : __('En espera') }}
						</div>
						<div class="ai-avatar">
							<Bot class="size-16" />
						</div>
						<h2>{{ interviewerLabel }}</h2>
						<p>{{ __('La IA hará preguntas, retará tus respuestas y mantendrá la simulación.') }}</p>
					</div>
					<div class="user-tile">
						<div class="user-avatar">
							<User class="size-12" />
						</div>
						<h3>{{ __('Tú') }}</h3>
						<p>{{ micEnabled ? __('Micrófono activo') : __('Puedes responder por texto o activar voz') }}</p>
					</div>
				</div>

				<div class="room-controls">
					<button class="control-btn" :class="{ active: micEnabled }" :disabled="liveLoading" @click="toggleLiveVoice">
						<Mic v-if="!micEnabled" class="size-5" />
						<MicOff v-else class="size-5" />
						{{ liveLoading ? __('Conectando...') : micEnabled ? __('Apagar micrófono') : __('Activar voz') }}
					</button>
					<button class="control-btn" @click="insertStarter">
						<MessageSquare class="size-5" /> {{ __('Sugerir inicio') }}
					</button>
					<router-link :to="{ name: 'Practice' }" class="control-btn">
						<LayoutList class="size-5" /> {{ __('Nueva práctica') }}
					</router-link>
				</div>

				<div v-if="liveError" class="room-warning">
					<CircleAlert class="size-4" /> {{ liveError }}
				</div>

				<div v-if="feedback && Object.keys(feedback).length" class="feedback-panel">
					<div class="feedback-score">{{ feedback.score || 0 }}</div>
					<div>
						<h2>{{ __('Feedback final') }}</h2>
						<p>{{ feedback.summary }}</p>
					</div>
					<div class="feedback-grid">
						<div>
							<h3>{{ __('Fortalezas') }}</h3>
							<ul><li v-for="item in feedback.strengths || []" :key="item">{{ item }}</li></ul>
						</div>
						<div>
							<h3>{{ __('Mejoras') }}</h3>
							<ul><li v-for="item in feedback.improvements || []" :key="item">{{ item }}</li></ul>
						</div>
						<div>
							<h3>{{ __('Siguientes pasos') }}</h3>
							<ul><li v-for="item in feedback.next_steps || []" :key="item">{{ item }}</li></ul>
						</div>
					</div>
					<div v-if="feedback.sample_better_answer" class="better-answer">
						<strong>{{ __('Ejemplo de mejor respuesta') }}</strong>
						<p>{{ feedback.sample_better_answer }}</p>
					</div>
				</div>
			</section>

			<aside class="room-side">
				<div class="side-section transcript-section">
					<div class="side-head">
						<div>
							<div class="room-kicker">{{ __('Transcripción') }}</div>
							<h2>{{ __('Conversación') }}</h2>
						</div>
						<button class="side-icon" @click="saveTranscript"><Save class="size-4" /></button>
					</div>
					<div ref="transcriptBox" class="transcript-box">
						<div v-if="!transcript.length" class="empty-transcript">
							<MessageSquare class="size-8" />
							<p>{{ __('Empieza por texto o activa el micrófono.') }}</p>
						</div>
						<div v-for="(line, index) in transcript" :key="index" class="transcript-line" :class="line.role">
							<div class="line-role">{{ line.role === 'user' ? __('Tú') : __('IA') }}</div>
							<div class="line-content">{{ line.content }}</div>
						</div>
					</div>
					<div class="chat-compose">
						<textarea v-model="message" rows="3" :placeholder="__('Escribe tu respuesta...')" @keydown.enter.exact.prevent="sendMessage" />
						<button class="room-primary" :disabled="!message.trim() || sending" @click="sendMessage">
							<Send class="size-4" /> {{ sending ? __('Enviando...') : __('Enviar') }}
						</button>
					</div>
				</div>

				<div class="side-section">
					<div class="side-head">
						<div>
							<div class="room-kicker">{{ __('Notas') }}</div>
							<h2>{{ __('Apuntes privados') }}</h2>
						</div>
					</div>
					<textarea v-model="notes" class="notes-area" rows="7" :placeholder="__('Anota preguntas difíciles, ideas o respuestas para mejorar.')" />
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

onMounted(loadSession)
onBeforeUnmount(stopLiveVoice)

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

function appendLine(role, content) {
	if (!content?.trim()) return
	transcript.value.push({
		role,
		content: content.trim(),
		timestamp: new Date().toISOString(),
	})
	nextTick(() => {
		if (transcriptBox.value) transcriptBox.value.scrollTop = transcriptBox.value.scrollHeight
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
			if (transcriptBox.value) transcriptBox.value.scrollTop = transcriptBox.value.scrollHeight
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
		
		const url = `wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=${token.token}`
		const ws = new WebSocket(url)
		liveSession.value = ws

		ws.onopen = () => {
			console.log('Live API WebSocket onopen')
			const setupMessage = {
				setup: {
					model: `models/${token.model.replace('models/', '')}`,
					generationConfig: {
						responseModalities: ["AUDIO"],
					},
					systemInstruction: typeof token.config.systemInstruction === 'string'
						? { parts: [{ text: token.config.systemInstruction }] }
						: token.config.systemInstruction
				}
			}
			console.log('Sending setup message:', JSON.stringify(setupMessage, null, 2))
			ws.send(JSON.stringify(setupMessage))
		}

		ws.onmessage = async (event) => {
			console.log('Live API raw message length:', typeof event.data === 'string' ? event.data.length : 'Blob')
			try {
				let msg = event.data
				if (msg instanceof Blob) {
					msg = await msg.text()
				}
				const data = JSON.parse(msg)
				if (data.setupComplete) {
					console.log('Setup complete received, starting microphone')
					liveConnected.value = true
					liveSocketOpen.value = true
					await startMicrophone()
					toast.success(__('Voz activada.'))
					liveLoading.value = false
				} else if (data.serverContent) {
					handleLiveMessage(data)
				} else if (data.error) {
					console.error('Live API Server Error Response:', data.error)
					liveError.value = data.error.message || 'Error en servidor'
				} else {
					console.log('Unknown message format:', data)
				}
			} catch (e) {
				console.error('Error parsing onmessage:', e)
			}
		}

		ws.onerror = (event) => {
			console.error('Live API onerror:', event)
			liveError.value = __('Live API tuvo un problema. Continúa por texto.')
			liveSocketOpen.value = false
			liveConnected.value = false
			stopMicrophoneOnly()
			liveLoading.value = false
		}

		ws.onclose = (event) => {
			console.error('Live API onclose: code=', event.code, 'reason=', event.reason)
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
						mediaChunks: [{
							mimeType: 'audio/pcm;rate=16000',
							data: arrayBufferToBase64(pcm16.buffer)
						}]
					}
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
		for (let j = start; j < end; j++) sum += float32[j]
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
	for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i)
	return new Int16Array(bytes.buffer)
}

function handleLiveMessage(message) {
	const inputText = message?.serverContent?.inputTranscription?.text
	const outputText = message?.serverContent?.outputTranscription?.text
	if (inputText) appendLine('user', inputText)
	if (outputText) appendLine('assistant', outputText)

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
	for (let i = 0; i < pcm.length; i++) channel[i] = pcm[i] / 32768
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
.room-page { display: flex; min-height: 100vh; min-height: 100dvh; flex-direction: column; background: radial-gradient(circle at 20% 0%, rgba(37, 99, 235, 0.22), transparent 34%), #080d19; color: white; overflow-x: hidden; }
.room-header { display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-height: 72px; padding: 0.9rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.08); background: rgba(15,23,42,0.92); backdrop-filter: blur(14px); }
.room-kicker { color: #93c5fd; font-size: 0.72rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0; }
.room-header h1 { margin-top: 0.15rem; max-width: 46rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 1.2rem; font-weight: 900; }
.room-header-actions { display: flex; gap: 0.6rem; }
.room-layout { display: grid; flex: 1; grid-template-columns: minmax(0, 1fr) minmax(340px, 390px); gap: 1rem; min-height: calc(100dvh - 72px); padding: 1rem; background: transparent; }
.room-stage { display: flex; min-width: 0; min-height: 0; flex-direction: column; }
.meeting-grid { display: grid; grid-template-columns: minmax(0, 1fr) 250px; gap: 1rem; flex: 1; min-height: 430px; }
.ai-tile, .user-tile, .side-section, .feedback-panel { border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; background: #111827; box-shadow: 0 24px 60px rgba(0,0,0,0.25); }
.ai-tile { position: relative; display: flex; min-height: 430px; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; text-align: center; overflow: hidden; }
.ai-tile::before { content: ""; position: absolute; inset: auto -20% -35% -20%; height: 50%; background: radial-gradient(circle, rgba(59,130,246,0.45), transparent 60%); pointer-events: none; }
.tile-status { position: absolute; top: 1rem; left: 1rem; display: inline-flex; align-items: center; gap: 0.45rem; border-radius: 999px; background: rgba(255,255,255,0.08); padding: 0.35rem 0.65rem; color: #cbd5e1; font-size: 0.75rem; font-weight: 800; }
.tile-status span { width: 8px; height: 8px; border-radius: 999px; background: #94a3b8; }
.tile-status.live span { background: #22c55e; box-shadow: 0 0 0 6px rgba(34,197,94,0.14); }
.call-time { position: absolute; top: 1rem; right: 1rem; display: inline-flex; align-items: center; gap: 0.45rem; border-radius: 999px; background: rgba(15,23,42,0.72); padding: 0.35rem 0.65rem; color: #dbeafe; font-size: 0.75rem; font-weight: 800; }
.ai-avatar, .user-avatar { display: grid; place-items: center; border-radius: 999px; background: linear-gradient(135deg, #2563eb, #0d6efd); color: white; box-shadow: 0 0 0 12px rgba(37,99,235,0.12), 0 24px 80px rgba(37,99,235,0.28); }
.ai-avatar { width: 148px; height: 148px; }
.user-avatar { width: 92px; height: 92px; background: #1f2937; box-shadow: 0 0 0 10px rgba(255,255,255,0.05); }
.ai-tile h2, .user-tile h3 { position: relative; margin-top: 1rem; font-size: 1.4rem; font-weight: 900; }
.ai-tile p, .user-tile p { position: relative; margin-top: 0.5rem; max-width: 34rem; color: #cbd5e1; line-height: 1.6; }
.user-tile { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1rem; text-align: center; }
.room-controls { position: sticky; bottom: 1rem; z-index: 5; display: flex; flex-wrap: wrap; justify-content: center; gap: 0.75rem; width: fit-content; max-width: 100%; margin: 1rem auto 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; background: rgba(15,23,42,0.86); padding: 0.6rem; box-shadow: 0 18px 46px rgba(0,0,0,0.32); backdrop-filter: blur(14px); }
.control-btn, .room-primary, .room-ghost, .room-danger { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; min-height: 42px; border-radius: 8px; padding: 0.65rem 0.9rem; font-weight: 850; transition: 0.2s ease; }
.control-btn { border: 1px solid rgba(255,255,255,0.12); background: rgba(255,255,255,0.08); color: white; }
.control-btn:hover { background: rgba(255,255,255,0.14); }
.control-btn.active { background: #dc2626; border-color: #dc2626; }
.room-primary { border: 1px solid #0d6efd; background: #0d6efd; color: white; }
.room-ghost { border: 1px solid rgba(255,255,255,0.16); background: rgba(255,255,255,0.08); color: white; }
.room-danger { border: 1px solid #dc2626; background: #dc2626; color: white; }
.room-warning { display: flex; align-items: center; gap: 0.5rem; border: 1px solid rgba(251,191,36,0.35); border-radius: 8px; background: rgba(251,191,36,0.12); color: #fde68a; padding: 0.75rem 1rem; }
.room-side { display: flex; flex-direction: column; gap: 1rem; min-width: 0; }
.side-section { min-height: 0; overflow: hidden; }
.transcript-section { display: flex; flex: 1; flex-direction: column; min-height: 0; }
.side-head { display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding: 1rem; }
.side-head h2 { margin-top: 0.15rem; font-size: 1rem; font-weight: 900; }
.side-icon { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 8px; background: rgba(255,255,255,0.08); color: white; }
.transcript-box { flex: 1; overflow-y: auto; padding: 1rem; }
.empty-transcript { display: grid; place-items: center; gap: 0.75rem; height: 100%; color: #94a3b8; text-align: center; }
.transcript-line { margin-bottom: 0.75rem; }
.line-role { margin-bottom: 0.25rem; color: #93c5fd; font-size: 0.72rem; font-weight: 900; text-transform: uppercase; }
.transcript-line.user .line-role { color: #fbbf24; text-align: right; }
.line-content { border-radius: 8px; background: rgba(255,255,255,0.08); color: #e5e7eb; padding: 0.65rem 0.75rem; line-height: 1.55; font-size: 0.9rem; }
.transcript-line.user .line-content { background: #0d6efd; color: white; }
.chat-compose { border-top: 1px solid rgba(255,255,255,0.08); padding: 1rem; }
.chat-compose textarea, .notes-area { width: 100%; resize: vertical; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; background: #0b1220; color: white; padding: 0.75rem; outline: none; line-height: 1.5; }
.chat-compose .room-primary { width: 100%; margin-top: 0.6rem; }
.notes-area { border: 0; border-radius: 0; min-height: 150px; }
.feedback-panel { margin-top: 1rem; padding: 1rem; color: #e5e7eb; }
.feedback-score { float: right; display: grid; place-items: center; width: 74px; height: 74px; border-radius: 999px; background: #fbbf24; color: #78350f; font-size: 1.8rem; font-weight: 950; }
.feedback-panel h2 { font-size: 1.25rem; font-weight: 900; }
.feedback-panel p { margin-top: 0.45rem; color: #cbd5e1; line-height: 1.6; }
.feedback-grid { clear: both; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin-top: 1rem; }
.feedback-grid h3 { color: #93c5fd; font-size: 0.85rem; font-weight: 900; }
.feedback-grid ul { margin-top: 0.5rem; padding-left: 1rem; color: #cbd5e1; line-height: 1.6; }
.better-answer { margin-top: 1rem; border-radius: 8px; background: rgba(255,255,255,0.07); padding: 1rem; }
@media (max-width: 1100px) {
	.room-layout, .meeting-grid { grid-template-columns: 1fr; }
	.room-layout { min-height: auto; }
	.transcript-section { height: 620px; }
	.user-tile { min-height: 210px; }
}
@media (max-width: 640px) {
	.room-header { align-items: stretch; flex-direction: column; }
	.room-header-actions { width: 100%; }
	.room-header-actions > * { flex: 1; }
	.feedback-grid { grid-template-columns: 1fr; }
}
</style>

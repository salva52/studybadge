<template>
  <div class="transcription-card-wrapper mt-4 mb-6">
    <!-- Vista inicial / Inactiva -->
    <div v-if="status === 'idle'" class="tc-idle group" @click="!loading && startTranscription()">
      <div class="tc-idle-bg"></div>
      <div class="tc-idle-content">
        <div class="tc-icon-wrapper">
          <div class="tc-icon-glow"></div>
          <Mic class="size-6 tc-icon-svg" />
        </div>
        <div class="tc-text-content">
          <h3 class="tc-title">{{ __('Transcribir clase') }}</h3>
          <p class="tc-subtitle">{{ __('Convierte tu clase en apuntes inteligentes con TutorIA.') }}</p>
        </div>
        <div class="tc-action-area">
          <button class="tc-start-btn" :disabled="loading" @click.stop="startTranscription">
            <Loader2 v-if="loading" class="size-4 animate-spin" />
            <span v-else>{{ __('Iniciar') }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Vista Activa (Grabando, Pausado, Procesando) -->
    <div v-else class="tc-active-state">
      <div class="tc-active-header">
        <div class="tc-status-badge" :class="status">
          <span v-if="status === 'recording'" class="recording-indicator">
            <span class="bar"></span><span class="bar"></span><span class="bar"></span>
          </span>
          <span v-else-if="status === 'paused'" class="paused-indicator">
            <Pause class="size-3" />
          </span>
          <Loader2 v-else-if="status === 'processing'" class="size-3 animate-spin" />
          <span class="status-label">{{ statusText }}</span>
        </div>
        <div class="tc-timer-display" :class="{ 'is-paused': status === 'paused' }">
          {{ formattedTime }} <span class="tc-timer-limit">/ 2:00:00</span>
        </div>
      </div>
      
      <div class="tc-controls-row" v-if="status === 'recording' || status === 'paused'">
        <div class="tc-language-selector">
          <select v-model="language" class="tc-select" :disabled="status !== 'idle' && status !== 'paused'">
            <option value="auto">{{ __('Detectar idioma auto') }}</option>
            <option value="es">{{ __('Español') }}</option>
            <option value="en">{{ __('Inglés') }}</option>
            <option value="pt">{{ __('Portugués') }}</option>
          </select>
        </div>
        
        <div class="tc-action-buttons">
          <button v-if="status === 'recording'" class="tc-btn-icon tc-btn-pause" @click="pauseTranscription" title="Pausar">
            <Pause class="size-5" />
          </button>
          <button v-if="status === 'paused'" class="tc-btn-icon tc-btn-resume" @click="resumeTranscription" title="Continuar">
            <Play class="size-5" />
          </button>
          <button class="tc-btn-icon tc-btn-finish" @click="finishTranscription" title="Finalizar transcripción">
            <Square class="size-4" />
            <span>{{ __('Terminar') }}</span>
          </button>
        </div>
      </div>

      <div class="tc-transcript-container">
        <div class="tc-transcript-glass" ref="transcriptBox">
          <div v-if="status === 'processing'" class="tc-processing-view">
            <div class="ai-orb"></div>
            <h4>{{ __('Analizando la clase...') }}</h4>
            <p>{{ __('Generando resumen inteligente, ideas clave y preguntas de examen.') }}</p>
          </div>
          <div v-else class="tc-transcript-content">
            <p v-if="!rawTranscript && status === 'recording'" class="tc-placeholder">{{ __('Escuchando atentamente...') }}</p>
            <p v-else-if="!rawTranscript && status === 'paused'" class="tc-placeholder">{{ __('Grabación pausada.') }}</p>
            <p v-else class="tc-transcript-text">{{ rawTranscript }}</p>
          </div>
        </div>
      </div>

      <div class="tc-footer" v-if="status === 'recording' || status === 'paused'">
        <p>{{ __('La transcripción es privada. Asegúrate de tener permiso para grabar.') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, nextTick, watch } from 'vue'
import { call, toast } from 'frappe-ui'
import { Mic, Pause, Play, Square, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  sessionName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['transcription-completed'])

const status = ref('idle') // idle, recording, paused, processing
const loading = ref(false)
const language = ref('auto')
const rawTranscript = ref('')
const timeElapsed = ref(0)
const transcriptionId = ref(null)

let mediaRecorder = null
let timerInterval = null
let audioChunks = []

const CHUNK_MS = 10000 // 10 seconds per chunk for faster-whisper

const statusText = computed(() => {
  if (status.value === 'recording') return __('Grabando')
  if (status.value === 'paused') return __('Pausado')
  if (status.value === 'processing') return __('Procesando')
  return ''
})

const formattedTime = computed(() => {
  const h = Math.floor(timeElapsed.value / 3600)
  const m = Math.floor((timeElapsed.value % 3600) / 60)
  const s = timeElapsed.value % 60
  return `${h ? h + ':' : ''}${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

const transcriptBox = ref(null)

watch(rawTranscript, () => {
  nextTick(() => {
    if (transcriptBox.value) {
      transcriptBox.value.scrollTop = transcriptBox.value.scrollHeight
    }
  })
})

async function startTranscription() {
  try {
    loading.value = true
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    // Create DB record
    const tId = await call('studybadge_ai.ai_sessions.start_transcription', {
      session: props.sessionName,
      language: language.value
    })
    transcriptionId.value = tId
    
    // Setup recorder
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.push(e.data)
        sendAudioChunk()
      }
    }
    
    mediaRecorder.start(CHUNK_MS)
    
    status.value = 'recording'
    startTimers()
    
  } catch (err) {
    console.error(err)
    if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
      toast.error(__('Permiso de micrófono denegado.'))
    } else {
      toast.error(__('No se pudo iniciar la transcripción.'))
    }
  } finally {
    loading.value = false
  }
}

async function sendAudioChunk() {
  if (!audioChunks.length || !transcriptionId.value) return
  
  const blob = new Blob(audioChunks, { type: 'audio/webm' })
  audioChunks = [] // Clear for next chunk
  
  const formData = new FormData()
  formData.append('file', blob, 'chunk.webm')
  formData.append('transcription_id', transcriptionId.value)
  
  try {
    const res = await fetch('/api/method/studybadge_ai.ai_sessions.process_transcription_chunk', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || ''
      },
      body: formData
    })
    const data = await res.json()
    if (data.message && typeof data.message === 'string') {
      rawTranscript.value = data.message
    }
  } catch (e) {
    console.error('Error sending chunk', e)
  }
}

async function pauseTranscription() {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.pause()
  }
  status.value = 'paused'
  clearInterval(timerInterval)
  await call('studybadge_ai.ai_sessions.pause_transcription', { transcription_id: transcriptionId.value })
}

async function resumeTranscription() {
  if (mediaRecorder && mediaRecorder.state === 'paused') {
    mediaRecorder.resume()
  }
  status.value = 'recording'
  startTimers()
  await call('studybadge_ai.ai_sessions.resume_transcription', { transcription_id: transcriptionId.value })
}

async function finishTranscription() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
    mediaRecorder.stream.getTracks().forEach(t => t.stop())
  }
  clearInterval(timerInterval)
  
  status.value = 'processing'
  
  try {
    const res = await call('studybadge_ai.ai_sessions.finish_transcription', { transcription_id: transcriptionId.value })
    if (res && res.status === 'Completed') {
      toast.success(__('Resumen inteligente generado con éxito.'))
      emit('transcription-completed', res)
    } else {
      toast.error(__('Hubo un error al generar el resumen.'))
    }
  } catch (e) {
    toast.error(__('Error al finalizar la transcripción.'))
  } finally {
    resetState()
  }
}

function startTimers() {
  timerInterval = setInterval(() => {
    timeElapsed.value++
    // Max 2 hours limit
    if (timeElapsed.value >= 7200) {
      toast.warning(__('Límite de 2 horas alcanzado.'))
      finishTranscription()
    }
  }, 1000)
}

function resetState() {
  status.value = 'idle'
  rawTranscript.value = ''
  timeElapsed.value = 0
  transcriptionId.value = null
  audioChunks = []
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stream.getTracks().forEach(t => t.stop())
  }
  mediaRecorder = null
  clearInterval(timerInterval)
}

onUnmounted(() => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stream.getTracks().forEach(t => t.stop())
  }
  clearInterval(timerInterval)
})
</script>

<style scoped>
.transcription-card-wrapper {
  position: relative;
  width: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* =========================================
   IDLE STATE (Premium Button Look)
========================================= */
.tc-idle {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

.tc-idle:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px -4px rgba(59, 130, 246, 0.15);
  border-color: #cbd5e1;
}

.tc-idle:active {
  transform: translateY(1px);
}

.tc-idle-bg {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(248,250,252,1) 0%, rgba(241,245,249,0.5) 100%);
  z-index: 0;
}

.tc-idle-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  padding: 16px 20px;
  gap: 16px;
}

.tc-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  box-shadow: 0 8px 16px rgba(37, 99, 235, 0.25);
  flex-shrink: 0;
}

.tc-icon-glow {
  position: absolute;
  inset: -2px;
  background: inherit;
  filter: blur(8px);
  opacity: 0;
  border-radius: inherit;
  transition: opacity 0.3s ease;
}

.tc-idle:hover .tc-icon-glow {
  opacity: 0.6;
}

.tc-icon-svg {
  color: white;
  z-index: 2;
}

.tc-text-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.tc-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px 0;
  letter-spacing: -0.01em;
}

.tc-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
  line-height: 1.3;
}

.tc-start-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 99px;
  padding: 8px 20px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 90px;
}

.tc-idle:hover .tc-start-btn {
  background: #1e293b;
}

/* =========================================
   ACTIVE STATE (Glassmorphism & Neon)
========================================= */
.tc-active-state {
  position: relative;
  background: #0f172a; /* Dark premium background */
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
  overflow: hidden;
  color: white;
}

.tc-active-state::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%; width: 200%; height: 200%;
  background: radial-gradient(circle at top right, rgba(59, 130, 246, 0.15), transparent 40%),
              radial-gradient(circle at bottom left, rgba(239, 68, 68, 0.1), transparent 40%);
  z-index: 0;
  pointer-events: none;
}

.tc-active-header, .tc-controls-row, .tc-transcript-container, .tc-footer {
  position: relative;
  z-index: 1;
}

.tc-active-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tc-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 6px 14px;
  border-radius: 99px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.tc-status-badge.recording { color: #f87171; border-color: rgba(248, 113, 113, 0.3); }
.tc-status-badge.paused { color: #fbbf24; }
.tc-status-badge.processing { color: #60a5fa; }

/* Animated Audio Bars */
.recording-indicator {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 12px;
}

.recording-indicator .bar {
  width: 3px;
  background: #ef4444;
  border-radius: 2px;
  animation: equalize 1s infinite alternate ease-in-out;
}

.recording-indicator .bar:nth-child(1) { height: 60%; animation-delay: 0s; }
.recording-indicator .bar:nth-child(2) { height: 100%; animation-delay: 0.3s; }
.recording-indicator .bar:nth-child(3) { height: 80%; animation-delay: 0.15s; }

@keyframes equalize {
  0% { height: 30%; }
  100% { height: 100%; }
}

.tc-timer-display {
  font-size: 1.5rem;
  font-weight: 300;
  font-variant-numeric: tabular-nums;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.tc-timer-display.is-paused {
  opacity: 0.6;
}

.tc-timer-limit {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.tc-controls-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tc-language-selector {
  flex: 1;
  max-width: 200px;
}

.tc-select {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.85rem;
  outline: none;
  appearance: none;
  transition: all 0.2s;
}

.tc-select:focus {
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(255, 255, 255, 0.1);
}

.tc-select option {
  background: #1e293b;
  color: white;
}

.tc-action-buttons {
  display: flex;
  gap: 12px;
}

.tc-btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.tc-btn-pause {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.tc-btn-pause:hover { background: rgba(255, 255, 255, 0.2); transform: scale(1.05); }

.tc-btn-resume {
  background: #f59e0b;
  color: #fff;
}

.tc-btn-resume:hover { background: #fbbf24; transform: scale(1.05); }

.tc-btn-finish {
  background: #ef4444;
  color: white;
  width: auto;
  padding: 0 20px;
  border-radius: 99px;
  gap: 8px;
  font-weight: 600;
  font-size: 0.85rem;
}

.tc-btn-finish:hover {
  background: #f87171;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.3);
}

.tc-transcript-container {
  margin-top: 10px;
}

.tc-transcript-glass {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  height: 140px;
  overflow-y: auto;
  padding: 16px;
  scroll-behavior: smooth;
}

.tc-transcript-glass::-webkit-scrollbar {
  width: 6px;
}

.tc-transcript-glass::-webkit-scrollbar-track {
  background: transparent;
}

.tc-transcript-glass::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.tc-transcript-content {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #e2e8f0;
}

.tc-placeholder {
  color: #64748b;
  font-style: italic;
  text-align: center;
  margin-top: 30px;
}

.tc-processing-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.ai-orb {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  margin-bottom: 12px;
  animation: pulse-orb 2s infinite ease-in-out;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
}

@keyframes pulse-orb {
  0% { transform: scale(0.9); opacity: 0.8; }
  50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 30px rgba(139, 92, 246, 0.8); }
  100% { transform: scale(0.9); opacity: 0.8; }
}

.tc-processing-view h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  color: #ffffff;
}

.tc-processing-view p {
  margin: 0;
  font-size: 0.8rem;
  color: #94a3b8;
}

.tc-footer {
  margin-top: 16px;
  text-align: center;
}

.tc-footer p {
  margin: 0;
  font-size: 0.75rem;
  color: #475569;
}
</style>

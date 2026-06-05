<template>
  <div class="transcription-widget my-4">
    <!-- Vista Inicial / Inactiva -->
    <button v-if="status === 'idle'" class="tw-idle-btn group" @click="!loading && startTranscription()" :disabled="loading">
      <Loader2 v-if="loading" class="size-4 animate-spin text-ink-gray-5" />
      <div v-else class="tw-icon-wrapper">
        <Mic class="size-4 text-white" />
      </div>
      <span class="tw-idle-text">{{ __('Grabar Clase con IA') }}</span>
    </button>

    <!-- Vista Activa (Grabando, Pausado, Procesando) -->
    <div v-else class="tw-active-bar">
      <!-- Indicador de Estado -->
      <div class="tw-status-indicator" :class="status">
        <span v-if="status === 'recording'" class="recording-dots">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        </span>
        <Pause v-else-if="status === 'paused'" class="size-4 text-amber-400" />
        <Loader2 v-else-if="status === 'processing'" class="size-4 animate-spin text-blue-400" />
      </div>

      <!-- Tiempo -->
      <div class="tw-timer" :class="{ 'opacity-50': status === 'paused' }">
        {{ formattedTime }}
      </div>

      <!-- Separador -->
      <div class="tw-divider" v-if="status !== 'processing'"></div>

      <!-- Controles (Idioma y Botones) -->
      <div class="tw-controls" v-if="status !== 'processing'">
        <select v-model="language" class="tw-lang-select" :disabled="status !== 'idle' && status !== 'paused'">
          <option value="auto">Auto</option>
          <option value="es">ES</option>
          <option value="en">EN</option>
          <option value="pt">PT</option>
        </select>
        
        <button v-if="status === 'recording'" class="tw-action-btn hover:text-amber-400" @click="pauseTranscription" title="Pausar">
          <Pause class="size-4" />
        </button>
        <button v-if="status === 'paused'" class="tw-action-btn hover:text-green-400" @click="resumeTranscription" title="Continuar">
          <Play class="size-4" />
        </button>
        <button class="tw-action-btn text-red-400 hover:text-red-300 ml-1" @click="finishTranscription" title="Terminar y resumir">
          <Square class="size-4" />
        </button>
      </div>
      
      <!-- Mensaje de Procesando -->
      <div v-if="status === 'processing'" class="tw-processing-text">
        {{ __('Generando apuntes en 2do plano...') }}
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
    audioChunks = []
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.push(e.data)
      }
    }
    
    mediaRecorder.start(1000) // Collect chunks every 1s locally
    
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

const isUploading = ref(false)

async function finishTranscription() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
    mediaRecorder.stream.getTracks().forEach(t => t.stop())
  }
  clearInterval(timerInterval)
  
  status.value = 'processing'
  
  // Wait a short time for the final ondataavailable event to fire
  await new Promise(resolve => setTimeout(resolve, 300))
  
  if (audioChunks.length > 0 && transcriptionId.value) {
    const blob = new Blob(audioChunks, { type: 'audio/webm' })
    audioChunks = []
    
    const formData = new FormData()
    formData.append('file', blob, 'class_audio.webm')
    formData.append('transcription_id', transcriptionId.value)
    
    try {
      await fetch('/api/method/studybadge_ai.ai_sessions.process_transcription_chunk', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'X-Frappe-CSRF-Token': window.csrf_token || ''
        },
        body: formData
      })
    } catch (e) {
      console.error('Error uploading final audio', e)
    }
  }
  
  try {
    const res = await call('studybadge_ai.ai_sessions.finish_transcription', { transcription_id: transcriptionId.value })
    if (res && (res.status === 'Completed' || res.status === 'Processing')) {
      toast.success(__('El resumen inteligente se está generando...'))
      emit('transcription-completed', res)
    } else {
      toast.error(__('Hubo un error al finalizar la transcripción.'))
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

<style scoped>
.transcription-widget {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

/* =========================================
   IDLE BUTTON
========================================= */
.tw-idle-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 99px;
  padding: 6px 16px 6px 6px;
  cursor: pointer;
  box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05);
  transition: all 0.2s ease;
}

.tw-idle-btn:hover:not(:disabled) {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px -2px rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
}

.tw-idle-btn:active:not(:disabled) {
  transform: translateY(0);
}

.tw-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.tw-idle-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}

/* =========================================
   ACTIVE BAR
========================================= */
.tw-active-bar {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background: #0f172a;
  border-radius: 99px;
  padding: 8px 16px;
  box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.3);
  color: #f8fafc;
  animation: slide-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes slide-in {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}

.tw-status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
}

.recording-dots {
  display: flex;
  gap: 3px;
  align-items: center;
  height: 14px;
}

.recording-dots .dot {
  width: 4px;
  height: 4px;
  background: #ef4444;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.recording-dots .dot:nth-child(1) { animation-delay: -0.32s; }
.recording-dots .dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.tw-timer {
  font-size: 0.9rem;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  letter-spacing: 0.02em;
}

.tw-divider {
  width: 1px;
  height: 16px;
  background: rgba(255, 255, 255, 0.15);
}

.tw-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tw-lang-select {
  background: transparent;
  color: #94a3b8;
  border: none;
  font-size: 0.75rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  padding: 0;
  margin-right: 4px;
  appearance: none;
}

.tw-lang-select option {
  background: #1e293b;
  color: white;
}

.tw-action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #cbd5e1;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.tw-action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.tw-processing-text {
  font-size: 0.8rem;
  font-weight: 500;
  color: #93c5fd;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>

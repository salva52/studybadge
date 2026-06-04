<template>
  <div class="transcription-card-wrapper mt-3 mb-3">
    <!-- Vista inicial / Inactiva -->
    <div v-if="status === 'idle'" class="transcription-card idle-state">
      <div class="tc-icon">
        <Mic class="size-5" />
      </div>
      <div class="tc-content">
        <strong>{{ __('Transcribir clase') }}</strong>
        <small>{{ __('Convierte tu clase en apuntes inteligentes para estudiar con TutorIA.') }}</small>
      </div>
      <button class="primary-btn tc-start-btn" @click="startTranscription" :disabled="loading">
        {{ loading ? __('Iniciando...') : __('Iniciar transcripción') }}
      </button>
    </div>

    <!-- Vista Activa (Grabando, Pausado, Procesando) -->
    <div v-else class="transcription-card active-state">
      <div class="tc-header">
        <div class="tc-status-indicator">
          <span class="pulse-dot" :class="{ recording: status === 'recording', paused: status === 'paused', processing: status === 'processing' }"></span>
          <span class="status-text">{{ statusText }}</span>
        </div>
        <div class="tc-timer">{{ formattedTime }} / 2:00:00</div>
      </div>
      
      <div class="tc-options" v-if="status === 'recording' || status === 'paused'">
        <select v-model="language" class="tc-select" :disabled="status !== 'idle' && status !== 'paused'">
          <option value="auto">{{ __('Detectar automáticamente') }}</option>
          <option value="es">{{ __('Español') }}</option>
          <option value="en">{{ __('Inglés') }}</option>
          <option value="pt">{{ __('Portugués') }}</option>
        </select>
      </div>

      <div class="tc-transcript-preview" ref="transcriptBox">
        <p v-if="!rawTranscript && status === 'recording'" class="text-muted">{{ __('Escuchando...') }}</p>
        <p v-else>{{ rawTranscript }}</p>
        <div v-if="status === 'processing'" class="tc-processing">
          <Loader2 class="size-4 spin" /> {{ __('Generando resumen inteligente...') }}
        </div>
      </div>

      <div class="tc-actions" v-if="status === 'recording' || status === 'paused'">
        <button v-if="status === 'recording'" class="secondary-btn" @click="pauseTranscription">
          <Pause class="size-4" /> {{ __('Pausar') }}
        </button>
        <button v-if="status === 'paused'" class="secondary-btn" @click="resumeTranscription">
          <Play class="size-4" /> {{ __('Continuar') }}
        </button>
        <button class="primary-btn finish-btn" @click="finishTranscription">
          <Square class="size-4" /> {{ __('Finalizar') }}
        </button>
      </div>
      
      <div class="tc-footer-notice" v-if="status === 'recording' || status === 'paused'">
        <small>{{ __('Recuerda tener permiso para grabar. La transcripción es privada.') }}</small>
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
let chunkInterval = null
let audioChunks = []

const CHUNK_MS = 10000 // 10 seconds per chunk for faster-whisper

const statusText = computed(() => {
  if (status.value === 'recording') return __('Grabando')
  if (status.value === 'paused') return __('Pausado')
  if (status.value === 'processing') return __('Procesando resumen')
  return ''
})

const formattedTime = computed(() => {
  const h = Math.floor(timeElapsed.value / 3600)
  const m = Math.floor((timeElapsed.value % 3600) / 60)
  const s = timeElapsed.value % 60
  return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
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
  
  try {
    const res = await fetch('/api/method/studybadge_ai.ai_sessions.process_transcription_chunk', {
      method: 'POST',
      headers: {
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
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.idle-state {
  display: flex;
  align-items: center;
  padding: 12px;
  gap: 12px;
}

.tc-icon {
  background: #f1f5f9;
  color: #3b82f6;
  padding: 8px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tc-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.tc-content strong {
  font-size: 0.9rem;
  color: #1e293b;
}

.tc-content small {
  font-size: 0.75rem;
  color: #64748b;
  line-height: 1.2;
}

.tc-start-btn {
  font-size: 0.8rem;
  padding: 6px 12px;
  white-space: nowrap;
}

.active-state {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tc-status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}

.pulse-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.pulse-dot.recording {
  background: #ef4444;
  animation: pulse-red 1.5s infinite;
}

.pulse-dot.paused {
  background: #f59e0b;
}

.pulse-dot.processing {
  background: #3b82f6;
  animation: pulse-blue 1.5s infinite;
}

.tc-timer {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  font-variant-numeric: tabular-nums;
}

.tc-options {
  display: flex;
  gap: 8px;
}

.tc-select {
  flex: 1;
  font-size: 0.8rem;
  padding: 6px;
  border-radius: 4px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
}

.tc-transcript-preview {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 10px;
  height: 100px;
  overflow-y: auto;
  font-size: 0.8rem;
  color: #334155;
  line-height: 1.4;
}

.tc-processing {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #3b82f6;
  font-weight: 500;
  justify-content: center;
  height: 100%;
}

.spin {
  animation: spin 1s linear infinite;
}

.tc-actions {
  display: flex;
  gap: 8px;
}

.tc-actions button {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  padding: 8px;
}

.finish-btn {
  background: #1e293b;
  color: white;
}

.tc-footer-notice {
  text-align: center;
  color: #94a3b8;
  font-size: 0.7rem;
}

@keyframes pulse-red {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

@keyframes pulse-blue {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(59, 130, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>

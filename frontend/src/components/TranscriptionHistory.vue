<template>
  <div class="transcription-history" v-if="transcriptions.length">
    <div class="th-title">{{ __('Historial de transcripciones') }}</div>
    <div class="th-list">
      <div v-for="t in transcriptions" :key="t.name" class="th-item">
        <div class="th-info">
          <strong>{{ t.title }}</strong>
          <small>{{ formatDate(t.started_at) }} · {{ formatDuration(t.duration) }} · {{ t.language }}</small>
        </div>
        <div class="th-actions">
          <button class="th-action-btn" title="Ver transcripción" @click="viewRaw(t)">
            <FileText class="size-3.5" />
          </button>
          <button class="th-action-btn delete-btn" title="Eliminar" @click="deleteTranscription(t)">
            <Trash2 class="size-3.5" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal para ver transcripción -->
    <div v-if="showModal" class="th-modal-backdrop" @click="showModal = false">
      <div class="th-modal" @click.stop>
        <div class="th-modal-header">
          <h3>{{ selectedTranscription?.title }}</h3>
          <button class="icon-btn" @click="showModal = false"><X class="size-4" /></button>
        </div>
        <div class="th-modal-body">
          <p v-if="loadingRaw" class="text-center"><Loader2 class="size-5 spin mx-auto" /></p>
          <p v-else-if="!rawContent" class="text-muted">{{ __('No hay transcripción disponible.') }}</p>
          <div v-else class="raw-text-content">{{ rawContent }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { call, toast } from 'frappe-ui'
import { FileText, Trash2, X, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  sessionName: {
    type: String,
    required: true
  },
  refreshTrigger: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['deleted', 'completed'])

const transcriptions = ref([])
const showModal = ref(false)
const selectedTranscription = ref(null)
const rawContent = ref('')
const loadingRaw = ref(false)

watch(() => props.sessionName, fetchTranscriptions)
watch(() => props.refreshTrigger, fetchTranscriptions)

onMounted(fetchTranscriptions)

async function fetchTranscriptions() {
  if (!props.sessionName) return
  try {
    const oldProcessing = transcriptions.value.some(t => t.status === 'Processing')
    transcriptions.value = await call('studybadge_ai.ai_sessions.list_transcriptions', { session: props.sessionName })
    const newProcessing = transcriptions.value.some(t => t.status === 'Processing')
    
    if (oldProcessing && !newProcessing) {
      toast.success(__('Resumen inteligente listo. Se agregó a tus fuentes.'))
      emit('completed')
    }
    
    if (newProcessing) {
      setTimeout(fetchTranscriptions, 5000)
    }
  } catch (e) {
    console.error(e)
  }
}

async function viewRaw(t) {
  selectedTranscription.value = t
  showModal.value = true
  loadingRaw.value = true
  rawContent.value = ''
  try {
    const full = await call('studybadge_ai.ai_sessions.get_transcription', { transcription_id: t.name })
    rawContent.value = full.raw_transcript
  } catch (e) {
    toast.error(__('No se pudo cargar la transcripción.'))
  } finally {
    loadingRaw.value = false
  }
}

async function deleteTranscription(t) {
  if (!confirm(__('¿Seguro que deseas eliminar esta transcripción?'))) return
  try {
    await call('studybadge_ai.ai_sessions.delete_transcription', { transcription_id: t.name })
    toast.success(__('Transcripción eliminada.'))
    emit('deleted')
    fetchTranscriptions()
  } catch (e) {
    toast.error(__('Error al eliminar.'))
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function formatDuration(seconds) {
  if (!seconds) return '0:00'
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.transcription-history {
  margin-top: 12px;
  margin-bottom: 12px;
}
.th-title {
  font-size: 0.75rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.th-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.th-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}
.th-info {
  display: flex;
  flex-direction: column;
}
.th-info strong {
  font-size: 0.8rem;
  color: #1e293b;
}
.th-info small {
  font-size: 0.7rem;
  color: #64748b;
}
.th-actions {
  display: flex;
  gap: 4px;
}
.th-action-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}
.th-action-btn:hover {
  background: #e2e8f0;
  color: #1e293b;
}
.th-action-btn.delete-btn:hover {
  background: #fee2e2;
  color: #ef4444;
}

.th-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.th-modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}
.th-modal-header {
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.th-modal-header h3 {
  margin: 0;
  font-size: 1rem;
}
.th-modal-body {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
}
.raw-text-content {
  white-space: pre-wrap;
  font-size: 0.85rem;
  color: #334155;
  line-height: 1.5;
}
.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>

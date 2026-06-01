<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content reading-modal">
			<div class="modal-header">
				<h2><MessageCircle class="icon size-5" /> {{ __('Lectura Guiada') }}</h2>
				<button class="icon-btn" @click="close"><X class="size-5" /></button>
			</div>
			
			<div class="split-view">
				<!-- Mobile Tabs -->
				<div class="mobile-tabs">
					<button class="tab-btn" :class="{ active: activeTab === 'doc' }" @click="activeTab = 'doc'">
						<FileText class="size-4" /> {{ __('Documento') }}
					</button>
					<button class="tab-btn" :class="{ active: activeTab === 'assistant' }" @click="activeTab = 'assistant'">
						<Bot class="size-4" /> {{ __('Asistente') }}
					</button>
				</div>
				
				<!-- Left Column: Document Viewer -->
				<div class="document-pane" :class="{ 'd-none': activeTab !== 'doc' && isMobile }">
					<div class="doc-toolbar">
						<div class="doc-selector-wrap">
							<FileText class="size-4 text-slate-400 doc-icon" />
							<select v-model="selectedMaterial" class="doc-select" v-if="materials && materials.length">
								<option :value="null">{{ __('Selecciona un documento') }}</option>
								<option v-for="mat in materials" :key="mat.file" :value="mat">
									{{ mat.file_name || mat.file.split('/').pop() }}
								</option>
							</select>
							<span v-else class="doc-title">{{ __('Sin documentos adjuntos') }}</span>
						</div>
					</div>
					
					<div v-if="selectedMaterial" class="pdf-container">
						<iframe :src="selectedMaterial.file" class="pdf-viewer" frameborder="0"></iframe>
					</div>
					<div v-else class="doc-content-placeholder">
						<FileText class="size-10 text-slate-300 mb-2" />
						<p>{{ __('Área de lectura del documento') }}</p>
						<small>{{ __('Selecciona un documento para empezar a leer. La IA generará preguntas sobre tu avance.') }}</small>
					</div>
				</div>
				
				<!-- Right Column: AI Guided Questions -->
				<div class="assistant-pane" :class="{ 'd-none': activeTab !== 'assistant' && isMobile }">
					<div class="assistant-header">
						<Bot class="size-5 text-blue-600" />
						<span>{{ __('Asistente de Lectura') }}</span>
					</div>
					
					<div class="assistant-body">
						<div v-if="loading" class="loading-state">
							<div class="typing-indicator"><span></span><span></span><span></span></div>
							<p>{{ __('Analizando tu avance...') }}</p>
						</div>
						
						<div v-else-if="readingData && readingData.question" class="question-card">
							<div v-if="readingData.evaluation" class="evaluation-box">
								<Bot class="size-4" />
								<p><strong>{{ __('Respuesta anterior:') }}</strong> {{ readingData.evaluation }}</p>
							</div>

							<span class="badge">{{ __('Reflexión') }}</span>
							<h3>{{ readingData.question }}</h3>
							
							<div v-if="readingData.hint" class="hint-box">
								<Lightbulb class="size-4 hint-icon" />
								<p>{{ readingData.hint }}</p>
							</div>
							
							<div class="response-area">
								<textarea v-model="userAnswer" rows="3" :placeholder="__('Escribe tu respuesta o reflexión aquí...')"></textarea>
								<button class="primary-btn mt-2 full-w" :disabled="!userAnswer.trim()" @click="$emit('verify-answer', userAnswer); userAnswer = ''">
									{{ __('Verificar respuesta') }}
								</button>
							</div>
						</div>
						
						<div v-else class="empty-state">
							<MessageCircle class="size-8 text-slate-300 mb-2" />
							<p>{{ __('Sigue leyendo. Aparecerán preguntas aquí para asegurar tu comprensión.') }}</p>
							<button class="secondary-btn mt-4" @click="$emit('request-question')">
								{{ __('Generar pregunta ahora') }}
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { MessageCircle, X, FileText, Bot, Lightbulb } from 'lucide-vue-next'

const props = defineProps({
	show: Boolean,
	loading: Boolean,
	data: Object,
	materials: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:show', 'request-question', 'verify-answer'])

const selectedMaterial = ref(null)
const activeTab = ref('doc') // 'doc' or 'assistant'
const isMobile = ref(false)
const userAnswer = ref('')

const checkMobile = () => { isMobile.value = window.innerWidth <= 768 }

onMounted(() => {
	checkMobile()
	window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
	window.removeEventListener('resize', checkMobile)
})

const readingData = computed(() => {
	if (!props.data) return null
	if (props.data.question) return props.data
	if (typeof props.data === 'string') {
		try { return JSON.parse(props.data) } catch (e) { return null }
	}
	return null
})

function close() {
	emit('update:show', false)
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,0.6); backdrop-filter: blur(4px); z-index: 100; display: flex; align-items: center; justify-content: center; padding: 1rem; }
.modal-content { background: #fff; width: 100%; max-width: 1100px; height: 85vh; border-radius: 16px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); display: flex; flex-direction: column; overflow: hidden; }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; background: #fff; z-index: 10; }
.modal-header h2 { display: flex; align-items: center; gap: 0.5rem; font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0; }
.icon { color: #2563eb; }
.icon-btn { background: transparent; border: 0; cursor: pointer; color: #64748b; padding: 0.25rem; border-radius: 8px; transition: background 0.2s; }
.icon-btn:hover { background: #f1f5f9; color: #0f172a; }

.split-view { display: flex; flex: 1; min-height: 0; }

.document-pane { flex: 2; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; background: #f8fafc; }
.doc-toolbar { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 1rem; background: #fff; border-bottom: 1px solid #e2e8f0; }
.doc-title { font-size: 0.85rem; font-weight: 700; color: #64748b; }
.doc-actions { display: flex; gap: 0.5rem; }
.doc-btn { background: transparent; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.35rem; color: #64748b; cursor: pointer; }
.doc-btn:hover { background: #f1f5f9; }

.doc-content-placeholder { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; text-align: center; color: #94a3b8; }
.doc-content-placeholder p { font-weight: 600; font-size: 1.1rem; color: #475569; margin: 0.5rem 0; }
.doc-content-placeholder small { max-width: 300px; line-height: 1.5; }

.assistant-pane { flex: 1; min-width: 320px; max-width: 400px; display: flex; flex-direction: column; background: #fff; }
.assistant-header { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; background: #eff6ff; border-bottom: 1px solid #bfdbfe; font-weight: 800; color: #1e3a8a; font-size: 0.95rem; }
.assistant-body { flex: 1; overflow-y: auto; padding: 1.5rem; display: flex; flex-direction: column; }

.question-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); animation: slideUp 0.3s ease-out; }
.badge { display: inline-block; background: #dbeafe; color: #1d4ed8; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; padding: 0.25rem 0.5rem; border-radius: 999px; margin-bottom: 0.75rem; letter-spacing: 0.05em; }
.question-card h3 { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-bottom: 1rem; line-height: 1.5; }

.hint-box { display: flex; gap: 0.5rem; background: #fefce8; border-radius: 8px; padding: 0.85rem; margin-bottom: 1rem; }
.hint-icon { color: #ca8a04; flex-shrink: 0; margin-top: 0.1rem; }
.hint-box p { font-size: 0.9rem; color: #854d0e; margin: 0; line-height: 1.4; }

.evaluation-box { display: flex; gap: 0.5rem; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 0.85rem; margin-bottom: 1.25rem; }
.evaluation-box .lucide { color: #059669; flex-shrink: 0; margin-top: 0.1rem; }
.evaluation-box p { font-size: 0.9rem; color: #065f46; margin: 0; line-height: 1.4; }

.response-area { margin-top: 1rem; border-top: 1px solid #f1f5f9; padding-top: 1rem; }
.response-area textarea { width: 100%; border: 1px solid #cbd5e1; border-radius: 8px; padding: 0.75rem; font-size: 0.95rem; color: #334155; resize: vertical; outline: none; transition: border-color 0.2s; }
.response-area textarea:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }

.primary-btn, .secondary-btn { display: inline-flex; justify-content: center; align-items: center; padding: 0.65rem 1rem; border-radius: 8px; font-weight: 700; font-size: 0.95rem; cursor: pointer; transition: all 0.2s; }
.primary-btn { background: #2563eb; color: #fff; border: 0; }
.primary-btn:hover { background: #1d4ed8; }
.secondary-btn { background: #fff; color: #334155; border: 1px solid #cbd5e1; }
.secondary-btn:hover { background: #f8fafc; border-color: #94a3b8; }
.full-w { width: 100%; }
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }

.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; color: #64748b; padding: 2rem; }
.empty-state p { font-size: 0.95rem; line-height: 1.5; margin-top: 0.5rem; }

.typing-indicator { display: flex; gap: 0.3rem; margin-bottom: 1rem; }
.typing-indicator span { display: block; width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; }
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

/* Document Viewer */
.doc-selector-wrap { display: flex; align-items: center; gap: 0.5rem; background: #f1f5f9; padding: 0.35rem 0.75rem; border-radius: 8px; flex: 1; }
.doc-select { flex: 1; background: transparent; border: none; outline: none; font-size: 0.9rem; font-weight: 600; color: #334155; cursor: pointer; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; }
.pdf-container { flex: 1; width: 100%; height: 100%; display: flex; }
.pdf-viewer { width: 100%; height: 100%; border: none; }

/* Mobile Tabs */
.mobile-tabs { display: none; padding: 0.5rem; background: #fff; border-bottom: 1px solid #e2e8f0; gap: 0.5rem; }
.tab-btn { flex: 1; display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.75rem; background: transparent; border: none; border-radius: 8px; font-weight: 600; font-size: 0.9rem; color: #64748b; cursor: pointer; transition: all 0.2s; }
.tab-btn.active { background: #eff6ff; color: #2563eb; }

@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUpSheet { from { transform: translateY(100%); } to { transform: translateY(0); } }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

@media (max-width: 768px) {
	.modal-content.reading-modal { 
		position: absolute; bottom: 0; left: 0; width: 100%; height: 90vh; 
		border-radius: 24px 24px 0 0; 
		animation: slideUpSheet 0.4s cubic-bezier(0.16, 1, 0.3, 1);
		margin: 0; max-width: 100%; border: none;
	}
	.modal-content::before {
		content: ''; display: block; width: 40px; height: 5px; background: #cbd5e1; border-radius: 4px; position: absolute; top: 12px; left: 50%; transform: translateX(-50%); z-index: 20;
	}
	.modal-header { padding-top: 1.75rem; }
	.split-view { flex-direction: column; }
	.mobile-tabs { display: flex; }
	.document-pane, .assistant-pane { flex: 1; max-width: 100%; height: 100%; border: none; }
	.d-none { display: none !important; }
}

:root[data-theme="dark"] .modal-content, :root[data-theme="dark"] .assistant-pane, :root[data-theme="dark"] .modal-header { background: #1e293b; color: #f8fafc; border-color: #334155; }
:root[data-theme="dark"] .modal-header h2 { color: #f8fafc; }
:root[data-theme="dark"] .document-pane { background: #0f172a; border-color: #334155; }
:root[data-theme="dark"] .doc-toolbar { background: #1e293b; border-color: #334155; }
:root[data-theme="dark"] .doc-btn { border-color: #475569; color: #94a3b8; }
:root[data-theme="dark"] .doc-btn:hover { background: #334155; }
:root[data-theme="dark"] .assistant-header { background: rgba(37,99,235,0.1); border-color: rgba(37,99,235,0.2); color: #60a5fa; }
:root[data-theme="dark"] .question-card { background: #0f172a; border-color: #334155; }
:root[data-theme="dark"] .question-card h3 { color: #f8fafc; }
:root[data-theme="dark"] .badge { background: rgba(37,99,235,0.2); color: #93c5fd; }
:root[data-theme="dark"] .hint-box { background: rgba(234,179,8,0.1); border-color: transparent; }
:root[data-theme="dark"] .hint-box p { color: #fde047; }
:root[data-theme="dark"] .evaluation-box { background: rgba(16,185,129,0.1); border-color: transparent; }
:root[data-theme="dark"] .evaluation-box p, :root[data-theme="dark"] .evaluation-box .lucide { color: #34d399; }
:root[data-theme="dark"] .doc-selector-wrap { background: #0f172a; }
:root[data-theme="dark"] .doc-select { color: #f8fafc; }
:root[data-theme="dark"] .mobile-tabs { background: #1e293b; border-color: #334155; }
:root[data-theme="dark"] .tab-btn { color: #94a3b8; }
:root[data-theme="dark"] .tab-btn.active { background: rgba(37,99,235,0.1); color: #60a5fa; }
:root[data-theme="dark"] .modal-content::before { background: #475569; }
</style>

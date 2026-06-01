<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content reading-modal">
			<div class="modal-header">
				<h2><MessageCircle class="icon size-5" /> {{ __('Lectura Guiada') }}</h2>
				<button class="icon-btn" @click="close"><X class="size-5" /></button>
			</div>
			
			<div class="split-view">
				<!-- Left Column: Document Viewer Placeholder (User will integrate actual PDF viewer here later) -->
				<div class="document-pane">
					<div class="doc-toolbar">
						<span class="doc-title">{{ __('Documento de Estudio') }}</span>
						<div class="doc-actions">
							<button class="doc-btn"><ZoomIn class="size-4" /></button>
							<button class="doc-btn"><ZoomOut class="size-4" /></button>
						</div>
					</div>
					<div class="doc-content-placeholder">
						<FileText class="size-10 text-slate-300 mb-2" />
						<p>{{ __('Área de lectura del documento') }}</p>
						<small>{{ __('A medida que avanzas, la IA generará preguntas sobre lo que estás leyendo.') }}</small>
					</div>
				</div>
				
				<!-- Right Column: AI Guided Questions -->
				<div class="assistant-pane">
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
							<span class="badge">{{ __('Reflexión') }}</span>
							<h3>{{ readingData.question }}</h3>
							
							<div v-if="readingData.hint" class="hint-box">
								<Lightbulb class="size-4 hint-icon" />
								<p>{{ readingData.hint }}</p>
							</div>
							
							<div class="response-area">
								<textarea rows="3" :placeholder="__('Escribe tu respuesta o reflexión aquí...')"></textarea>
								<button class="primary-btn mt-2 full-w">{{ __('Verificar respuesta') }}</button>
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
import { computed } from 'vue'
import { MessageCircle, X, FileText, ZoomIn, ZoomOut, Bot, Lightbulb } from 'lucide-vue-next'

const props = defineProps({
	show: Boolean,
	loading: Boolean,
	data: Object
})

const emit = defineEmits(['update:show', 'request-question'])

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

@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

@media (max-width: 768px) {
	.split-view { flex-direction: column; }
	.document-pane { flex: 1; border-right: none; border-bottom: 1px solid #e2e8f0; }
	.assistant-pane { flex: 1; max-width: 100%; }
	.modal-content { height: 95vh; }
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
:root[data-theme="dark"] .response-area { border-color: #334155; }
:root[data-theme="dark"] .response-area textarea { background: #1e293b; border-color: #475569; color: #f8fafc; }
</style>

<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content math-modal">
			<div class="modal-header">
				<h2><Sigma class="icon size-5" /> {{ __('Matemática Paso a Paso') }}</h2>
				<button class="icon-btn" @click="close"><X class="size-5" /></button>
			</div>
			
			<div v-if="loading" class="loading-state">
				<div class="spinner"></div>
				<p>{{ __('Resolviendo el problema...') }}</p>
			</div>
			
			<div v-else-if="mathData && mathData.steps" class="math-body">
				<div class="math-steps">
					<h3>{{ __('Desarrollo paso a paso:') }}</h3>
					<div v-for="(step, idx) in mathData.steps" :key="idx" class="math-step">
						<div class="step-number">{{ idx + 1 }}</div>
						<div class="step-content" v-html="renderMarkdown(step)"></div>
					</div>
				</div>
				
				<div class="math-solution">
					<h3>{{ __('Solución:') }}</h3>
					<div class="solution-content" v-html="renderMarkdown(mathData.solution || '')"></div>
				</div>
				
				<div v-if="mathData.practice_problem" class="practice-box">
					<h3>{{ __('¡Ahora inténtalo tú!') }}</h3>
					<p>{{ __('Problema de práctica similar:') }}</p>
					<div class="practice-content" v-html="renderMarkdown(mathData.practice_problem)"></div>
				</div>
			</div>
			
			<div v-else class="error-state">
				<p>{{ __('No se pudo cargar la solución matemática.') }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import { Sigma, X } from 'lucide-vue-next'
import MarkdownIt from 'markdown-it'
import mk from 'markdown-it-katex'
import DOMPurify from 'dompurify'
import 'katex/dist/katex.min.css'

const props = defineProps({
	show: Boolean,
	loading: Boolean,
	data: Object
})

const emit = defineEmits(['update:show'])

const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true }).use(mk)

const mathData = computed(() => {
	if (!props.data) return null
	if (props.data.steps) return props.data
	if (typeof props.data === 'string') {
		try { return JSON.parse(props.data) } catch (e) { return null }
	}
	return null
})

function close() {
	emit('update:show', false)
}

function renderMarkdown(text) {
	if (!text) return ''
	return DOMPurify.sanitize(markdown.render(String(text)), {
		ADD_TAGS: ['math', 'semantics', 'mrow', 'mi', 'mo', 'mn', 'msup', 'mspace', 'mtd', 'mtr', 'mtable', 'annotation', 'mfrac', 'msqrt', 'mroot', 'mstyle', 'merror', 'mpadded', 'mphantom', 'mfenced', 'menclose', 'msub', 'msubsup', 'munderover', 'mover', 'munder'],
		ADD_ATTR: ['display', 'xmlns', 'encoding', 'aria-hidden', 'class', 'style'],
	})
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,0.6); backdrop-filter: blur(4px); z-index: 100; display: flex; align-items: center; justify-content: center; padding: 1rem; }
.modal-content { background: #fff; width: 100%; max-width: 700px; border-radius: 16px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); display: flex; flex-direction: column; max-height: 90vh; overflow: hidden; }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 1.5rem; border-bottom: 1px solid #e2e8f0; }
.modal-header h2 { display: flex; align-items: center; gap: 0.5rem; font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0; }
.icon { color: #2563eb; }
.icon-btn { background: transparent; border: 0; cursor: pointer; color: #64748b; padding: 0.25rem; border-radius: 8px; transition: background 0.2s; }
.icon-btn:hover { background: #f1f5f9; color: #0f172a; }

.math-body { padding: 1.5rem; overflow-y: auto; }
.math-body h3 { font-size: 1.1rem; font-weight: 800; color: #1e293b; margin-bottom: 1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; display: inline-block; }

.math-steps { margin-bottom: 2rem; }
.math-step { display: flex; gap: 1rem; margin-bottom: 1.25rem; background: #f8fafc; padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0; }
.step-number { flex-shrink: 0; display: grid; place-items: center; width: 28px; height: 28px; background: #2563eb; color: white; font-weight: 900; font-size: 0.85rem; border-radius: 50%; }
.step-content { flex: 1; font-size: 1rem; line-height: 1.6; color: #334155; overflow-x: auto; }
.step-content :deep(.katex-display) { margin: 0.5rem 0; padding: 0.5rem 0; }

.math-solution { margin-bottom: 2rem; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.25rem; }
.math-solution h3 { color: #1e40af; border-color: #93c5fd; }
.solution-content { font-size: 1.1rem; font-weight: 600; color: #1e3a8a; overflow-x: auto; }

.practice-box { background: #fefce8; border: 1px solid #fef08a; border-radius: 12px; padding: 1.25rem; }
.practice-box h3 { color: #854d0e; border-color: #fde047; margin-bottom: 0.25rem; }
.practice-box p { color: #a16207; font-size: 0.9rem; font-weight: 600; margin-bottom: 1rem; }
.practice-content { font-size: 1.05rem; color: #713f12; overflow-x: auto; }

.loading-state, .error-state { padding: 4rem 2rem; text-align: center; color: #64748b; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

:root[data-theme="dark"] .modal-content { background: #1e293b; color: #f8fafc; }
:root[data-theme="dark"] .modal-header { border-color: #334155; }
:root[data-theme="dark"] .modal-header h2 { color: #f8fafc; }
:root[data-theme="dark"] .math-body h3 { color: #f8fafc; border-color: #475569; }
:root[data-theme="dark"] .math-step { background: #0f172a; border-color: #334155; }
:root[data-theme="dark"] .step-content { color: #cbd5e1; }
:root[data-theme="dark"] .math-solution { background: rgba(37,99,235,0.1); border-color: rgba(37,99,235,0.3); }
:root[data-theme="dark"] .math-solution h3, :root[data-theme="dark"] .solution-content { color: #93c5fd; }
:root[data-theme="dark"] .practice-box { background: rgba(234,179,8,0.1); border-color: rgba(234,179,8,0.3); }
:root[data-theme="dark"] .practice-box h3, :root[data-theme="dark"] .practice-box p, :root[data-theme="dark"] .practice-content { color: #fde047; }
</style>

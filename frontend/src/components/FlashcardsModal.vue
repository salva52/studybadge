<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content flashcards-modal">
			<div class="modal-header">
				<h2><Layers class="icon size-5" /> {{ __('Tarjetas de Estudio') }}</h2>
				<button class="icon-btn" @click="close"><X class="size-5" /></button>
			</div>
			
			<div v-if="loading" class="loading-state">
				<div class="spinner"></div>
				<p>{{ __('Creando tarjetas...') }}</p>
			</div>
			
			<div v-else-if="flashcardsData && flashcardsData.flashcards && flashcardsData.flashcards.length > 0" class="flashcards-body">
				<div class="progress-bar">
					<div class="progress-fill" :style="{ width: ((currentIndex) / flashcardsData.flashcards.length * 100) + '%' }"></div>
				</div>
				<span class="card-count">{{ __('Tarjeta') }} {{ currentIndex + 1 }} {{ __('de') }} {{ flashcardsData.flashcards.length }}</span>
				
				<div class="flashcard-container" @click="isFlipped = !isFlipped">
					<div class="flashcard" :class="{ 'is-flipped': isFlipped }">
						<div class="flashcard-face flashcard-front">
							<span class="face-label">{{ __('PREGUNTA') }}</span>
							<h3>{{ currentCard.front }}</h3>
							<p class="flip-hint">{{ __('Toca para voltear') }} <RotateCw class="size-4 inline" /></p>
						</div>
						<div class="flashcard-face flashcard-back">
							<span class="face-label">{{ __('RESPUESTA') }}</span>
							<p>{{ currentCard.back }}</p>
						</div>
					</div>
				</div>
				
				<div class="controls-row">
					<button class="control-btn prev" :disabled="currentIndex === 0" @click="prevCard">
						<ChevronLeft class="size-5" /> {{ __('Anterior') }}
					</button>
					<div class="knowledge-btns" :class="{ 'visible': isFlipped }">
						<button class="know-btn wrong" @click="nextCard">{{ __('Repasar luego') }}</button>
						<button class="know-btn right" @click="nextCard">{{ __('Lo sabía') }}</button>
					</div>
					<button class="control-btn next" :disabled="currentIndex === flashcardsData.flashcards.length - 1" @click="nextCard">
						{{ __('Siguiente') }} <ChevronRight class="size-5" />
					</button>
				</div>
			</div>
			
			<div v-else class="error-state">
				<p>{{ __('No se pudieron cargar las tarjetas. Intenta de nuevo.') }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Layers, X, ChevronLeft, ChevronRight, RotateCw } from 'lucide-vue-next'

const props = defineProps({
	show: Boolean,
	loading: Boolean,
	data: Object
})

const emit = defineEmits(['update:show'])

const currentIndex = ref(0)
const isFlipped = ref(false)

const flashcardsData = computed(() => {
	if (!props.data) return null
	if (props.data.flashcards) return props.data
	if (typeof props.data === 'string') {
		try { return JSON.parse(props.data) } catch (e) { return null }
	}
	return null
})

const currentCard = computed(() => {
	if (!flashcardsData.value || !flashcardsData.value.flashcards) return null
	return flashcardsData.value.flashcards[currentIndex.value]
})

watch(() => props.show, (newVal) => {
	if (newVal) {
		currentIndex.value = 0
		isFlipped.value = false
	}
})

function close() {
	emit('update:show', false)
}

function nextCard() {
	if (currentIndex.value < flashcardsData.value.flashcards.length - 1) {
		isFlipped.value = false
		setTimeout(() => { currentIndex.value++ }, 150)
	} else {
		close()
	}
}

function prevCard() {
	if (currentIndex.value > 0) {
		isFlipped.value = false
		setTimeout(() => { currentIndex.value-- }, 150)
	}
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

.flashcards-body { padding: 1.5rem; display: flex; flex-direction: column; align-items: center; }
.progress-bar { width: 100%; height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden; margin-bottom: 0.5rem; }
.progress-fill { height: 100%; background: #2563eb; transition: width 0.3s ease; }
.card-count { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; align-self: flex-start; margin-bottom: 1.5rem; }

.flashcard-container { width: 100%; aspect-ratio: 16/10; max-height: 400px; perspective: 1000px; cursor: pointer; margin-bottom: 2rem; }
.flashcard { width: 100%; height: 100%; position: relative; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); transform-style: preserve-3d; }
.flashcard.is-flipped { transform: rotateY(180deg); }
.flashcard-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2.5rem; text-align: center; box-shadow: 0 10px 30px rgba(15,23,42,0.08); border: 1px solid #e2e8f0; background: #fff; }
.flashcard-back { transform: rotateY(180deg); background: #f8fafc; border-color: #cbd5e1; }

.face-label { position: absolute; top: 1.5rem; font-size: 0.75rem; font-weight: 800; color: #94a3b8; letter-spacing: 0.1em; }
.flashcard-front h3 { font-size: 1.6rem; font-weight: 800; color: #0f172a; line-height: 1.4; margin: 0; }
.flashcard-back p { font-size: 1.25rem; font-weight: 500; color: #1e293b; line-height: 1.6; margin: 0; }
.flip-hint { position: absolute; bottom: 1.5rem; font-size: 0.8rem; color: #64748b; font-weight: 600; display: flex; align-items: center; gap: 0.35rem; }
.inline { display: inline; }

.controls-row { width: 100%; display: flex; justify-content: space-between; align-items: center; }
.control-btn { display: flex; align-items: center; gap: 0.25rem; background: transparent; border: 0; color: #64748b; font-weight: 700; font-size: 1rem; cursor: pointer; transition: color 0.2s; padding: 0.5rem; }
.control-btn:hover:not(:disabled) { color: #0f172a; }
.control-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.knowledge-btns { display: flex; gap: 1rem; opacity: 0; pointer-events: none; transition: opacity 0.3s; }
.knowledge-btns.visible { opacity: 1; pointer-events: auto; }
.know-btn { padding: 0.6rem 1.25rem; border-radius: 999px; font-weight: 700; font-size: 0.95rem; cursor: pointer; border: 0; transition: transform 0.2s, opacity 0.2s; }
.know-btn:hover { transform: scale(1.05); }
.know-btn:active { transform: scale(0.95); }
.know-btn.wrong { background: #fee2e2; color: #991b1b; }
.know-btn.right { background: #dcfce3; color: #166534; }

.loading-state, .error-state { padding: 4rem 2rem; text-align: center; color: #64748b; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

@keyframes slideUpSheet { from { transform: translateY(100%); } to { transform: translateY(0); } }

@media (max-width: 640px) {
	.modal-content.flashcards-modal { 
		position: absolute; bottom: 0; left: 0; width: 100%; height: auto; max-height: 90vh;
		border-radius: 24px 24px 0 0; 
		animation: slideUpSheet 0.4s cubic-bezier(0.16, 1, 0.3, 1);
		margin: 0; border: none;
	}
	.modal-content::before {
		content: ''; display: block; width: 40px; height: 5px; background: #cbd5e1; border-radius: 4px; position: absolute; top: 12px; left: 50%; transform: translateX(-50%); z-index: 20;
	}
	.modal-header { padding-top: 1.75rem; }
	.flashcard-container { aspect-ratio: 3/4; max-height: 60vh; }
	.controls-row { flex-wrap: wrap; justify-content: center; gap: 1rem; padding-bottom: env(safe-area-inset-bottom); }
	.control-btn.prev { order: 1; margin-right: auto; }
	.control-btn.next { order: 2; margin-left: auto; }
	.knowledge-btns { order: 3; width: 100%; justify-content: center; }
	.know-btn { min-height: 48px; flex: 1; display: flex; align-items: center; justify-content: center; }
}

:root[data-theme="dark"] .modal-content { background: #1e293b; color: #f8fafc; }
:root[data-theme="dark"] .modal-header { border-color: #334155; }
:root[data-theme="dark"] .modal-header h2 { color: #f8fafc; }
:root[data-theme="dark"] .flashcard-face { background: #0f172a; border-color: #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
:root[data-theme="dark"] .flashcard-back { background: #1e293b; }
:root[data-theme="dark"] .flashcard-front h3 { color: #f8fafc; }
:root[data-theme="dark"] .flashcard-back p { color: #e2e8f0; }
:root[data-theme="dark"] .know-btn.wrong { background: rgba(239,68,68,0.2); color: #fca5a5; }
:root[data-theme="dark"] .know-btn.right { background: rgba(34,197,94,0.2); color: #86efac; }
:root[data-theme="dark"] .modal-content::before { background: #475569; }
</style>

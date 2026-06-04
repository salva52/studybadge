<template>
	<div class="loading-state">
		<div class="spinner"></div>
		<h3>{{ title || __('Creando contenido...') }}</h3>
		<div class="loading-bar-wrapper">
			<div class="loading-bar-fill"></div>
		</div>
		<p class="fun-fact"><strong>{{ __('Dato Curioso:') }}</strong> {{ currentFact }}</p>
	</div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
	active: Boolean,
	title: String
})

const funFacts = [
	__('¿Sabías que el cerebro humano procesa imágenes 60,000 veces más rápido que el texto? ¡Por eso los mapas mentales son tan efectivos!'),
	__('Un estudiante promedio olvida el 50% de lo que lee en una hora. Por suerte, TutorIA está aquí para ayudarte a retenerlo.'),
	__('El músculo más fuerte del cuerpo es el masetero (la mandíbula). Pero tu cerebro quema el 20% de tus calorías diarias.'),
	__('Estudiar 15 minutos al día es más efectivo que estudiar 10 horas seguidas antes del examen. ¡Poco a poco!'),
	__('¿Sabías que los pulpos tienen tres corazones? Ideal para enamorarse de múltiples materias académicas.'),
	__('La música clásica de fondo puede mejorar tu concentración matemática. ¡Pruébalo la próxima vez!'),
	__('Tu cerebro tiene suficiente energía para encender una bombilla pequeña. ¡Úsala bien!'),
]

const currentFact = ref(funFacts[0])
let factInterval = null

function startFacts() {
	currentFact.value = funFacts[Math.floor(Math.random() * funFacts.length)]
	factInterval = setInterval(() => {
		let newFact = funFacts[Math.floor(Math.random() * funFacts.length)]
		while (newFact === currentFact.value) newFact = funFacts[Math.floor(Math.random() * funFacts.length)]
		currentFact.value = newFact
	}, 4000)
}

function stopFacts() {
	if (factInterval) clearInterval(factInterval)
}

watch(() => props.active, (isActive) => {
	if (isActive) startFacts()
	else stopFacts()
}, { immediate: true })

onUnmounted(stopFacts)
</script>

<style scoped>
.loading-state { padding: 4rem 2rem; text-align: center; color: #64748b; }
.loading-state h3 { font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 1rem 0 0.5rem; }
.loading-bar-wrapper { width: 80%; margin: 1.5rem auto; height: 8px; background: #e2e8f0; border-radius: 999px; overflow: hidden; }
.loading-bar-fill { height: 100%; background: #2563eb; width: 0%; border-radius: 999px; animation: fakeProgress 10s ease-out forwards; }
@keyframes fakeProgress { 0% { width: 0%; } 100% { width: 95%; } }
.fun-fact { font-size: 0.95rem; color: #475569; max-width: 80%; margin: 1rem auto; line-height: 1.5; font-style: italic; min-height: 3rem; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
@keyframes spin { to { transform: rotate(360deg); } }
:root[data-theme="dark"] .loading-state h3 { color: #f8fafc; }
</style>

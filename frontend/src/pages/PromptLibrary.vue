<template>
	<div class="prompt-page min-h-screen pb-14 bg-gray-50/50">
		<header class="prompt-header sticky top-0 z-10 flex items-center justify-between border-b px-4 py-3 bg-white/90 backdrop-blur-md shadow-sm">
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<router-link :to="{ name: 'Practice' }" class="prompt-top-link flex items-center gap-2 text-sm font-bold text-blue-700 hover:text-blue-800 transition-colors">
				<Video class="size-4" /> {{ __('Practicar') }}
			</router-link>
		</header>

		<main class="mx-auto max-w-6xl px-4 py-8">
			<!-- Hero Section -->
			<section class="prompt-hero mb-12 rounded-2xl bg-[#08204e] text-white p-8 md:p-12 shadow-xl relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-8">
				<div class="relative z-10 max-w-2xl">
					<div class="prompt-kicker flex items-center gap-2 text-amber-400 text-xs font-black uppercase tracking-wider mb-4">
						<Zap class="size-4" /> {{ __('Biblioteca de prompts') }}
					</div>
					<h1 class="text-3xl md:text-5xl font-black leading-tight mb-4">
						{{ __('Prompts listos para copiar, adaptar y usar en ChatGPT, Gemini o Claude.') }}
					</h1>
					<p class="text-blue-100 text-lg md:text-xl max-w-xl mb-8 leading-relaxed">
						{{ __('Ahorra horas creando contenido, estudiando, vendiendo, organizando ideas y generando imágenes con IA.') }}
					</p>
					<div class="flex flex-col sm:flex-row gap-4">
						<router-link :to="{ name: 'Plus' }" class="btn-primary-custom flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-bold text-[#08204e] bg-amber-400 hover:bg-amber-300 transition-colors shadow-lg shadow-amber-400/20">
							<Crown class="size-5" /> {{ __('Desbloquear Plus') }}
						</router-link>
						<button @click="scrollToPrompts" class="btn-secondary-custom flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-bold text-white border border-white/20 bg-white/5 hover:bg-white/10 transition-colors">
							{{ __('Ver prompts gratis') }} <ArrowDown class="size-4" />
						</button>
					</div>
				</div>
				<!-- Decoración de fondo -->
				<div class="absolute right-0 top-0 w-1/2 h-full opacity-20 pointer-events-none" style="background: radial-gradient(circle at center, #3b82f6 0%, transparent 70%);"></div>
			</section>

			<!-- Search and Filters -->
			<div id="prompts-section" class="mb-10 space-y-6">
				<div class="relative max-w-2xl mx-auto">
					<Search class="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-gray-400" />
					<input 
						v-model="searchQuery" 
						type="text" 
						class="w-full pl-12 pr-4 py-4 rounded-xl border border-gray-200 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-lg transition-all"
						:placeholder="__('Buscar prompts para vender, estudiar, crear contenido, imágenes...')"
					/>
				</div>

				<!-- Categorías -->
				<div class="flex flex-col gap-3">
					<span class="text-sm font-bold text-gray-500 uppercase tracking-wider">{{ __('Categorías') }}</span>
					<div class="flex flex-wrap gap-2">
						<button 
							v-for="cat in categories" 
							:key="cat"
							@click="selectedCategory = cat"
							:class="['px-4 py-2 rounded-full text-sm font-bold transition-all border', selectedCategory === cat ? 'bg-blue-600 text-white border-blue-600 shadow-md shadow-blue-600/20' : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300 hover:bg-blue-50']"
						>
							{{ cat }}
						</button>
					</div>
				</div>

				<!-- Objetivos -->
				<div class="flex flex-col gap-3 mt-4">
					<span class="text-sm font-bold text-gray-500 uppercase tracking-wider">{{ __('Objetivos') }}</span>
					<div class="flex flex-wrap gap-2">
						<button 
							v-for="obj in objectives" 
							:key="obj"
							@click="selectedObjective = obj"
							:class="['px-4 py-2 rounded-full text-sm font-bold transition-all border flex items-center gap-1.5', selectedObjective === obj ? 'bg-slate-800 text-white border-slate-800 shadow-md shadow-slate-800/20' : 'bg-white text-gray-600 border-gray-200 hover:border-slate-300 hover:bg-slate-50']"
						>
							<Target class="size-3.5" v-if="selectedObjective === obj"/> {{ obj }}
						</button>
					</div>
				</div>
			</div>

			<!-- Prompts Populares -->
			<section v-if="showPopular" class="mb-14">
				<div class="flex items-center gap-2 mb-6">
					<Star class="size-5 text-amber-500 fill-amber-500" />
					<h2 class="text-2xl font-black text-[#08204e]">{{ __('Prompts populares') }}</h2>
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
					<PromptCard v-for="prompt in popularPrompts" :key="prompt.id" :prompt="prompt" @view="openModal" @copy="copyPrompt" />
				</div>
			</section>

			<!-- All Prompts Grid -->
			<section>
				<h2 class="text-2xl font-black text-[#08204e] mb-6" v-if="searchQuery || selectedCategory !== 'Todos' || selectedObjective !== 'Todos'">{{ __('Resultados') }}</h2>
				<h2 class="text-2xl font-black text-[#08204e] mb-6" v-else>{{ __('Todos los prompts') }}</h2>
				
				<div v-if="filteredPrompts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
					<PromptCard v-for="prompt in filteredPrompts" :key="prompt.id" :prompt="prompt" @view="openModal" @copy="copyPrompt" />
				</div>

				<!-- Empty State -->
				<div v-else class="text-center py-20 px-4 bg-white rounded-2xl border border-gray-100 shadow-sm">
					<Search class="size-12 text-gray-300 mx-auto mb-4" />
					<h3 class="text-xl font-bold text-gray-900 mb-2">{{ __('No encontramos prompts con esa búsqueda.') }}</h3>
					<p class="text-gray-500">{{ __('Prueba con palabras como marketing, estudio, negocio, imágenes o productividad.') }}</p>
					<button @click="resetFilters" class="mt-6 text-blue-600 font-bold hover:underline">
						{{ __('Limpiar filtros') }}
					</button>
				</div>
			</section>

			<!-- Banner Plus -->
			<section class="mt-20 bg-gradient-to-br from-[#08204e] to-blue-900 rounded-2xl p-8 md:p-10 text-white shadow-xl flex flex-col md:flex-row items-center justify-between gap-8 relative overflow-hidden">
				<div class="relative z-10 max-w-xl">
					<h2 class="text-3xl font-black mb-3">{{ __('Desbloquea toda la biblioteca') }}</h2>
					<p class="text-blue-100 text-lg mb-6">{{ __('Accede a prompts premium para vender más, estudiar mejor, crear contenido y lanzar proyectos con IA.') }}</p>
					<ul class="space-y-3 mb-8 md:mb-0">
						<li class="flex items-center gap-3"><Check class="size-5 text-amber-400 flex-shrink-0" /> <span class="font-medium">100+ prompts premium</span></li>
						<li class="flex items-center gap-3"><Check class="size-5 text-amber-400 flex-shrink-0" /> <span class="font-medium">Nuevos prompts cada semana</span></li>
						<li class="flex items-center gap-3"><Check class="size-5 text-amber-400 flex-shrink-0" /> <span class="font-medium">Plantillas para negocios, estudio y contenido</span></li>
						<li class="flex items-center gap-3"><Check class="size-5 text-amber-400 flex-shrink-0" /> <span class="font-medium">Copiar y usar al instante</span></li>
					</ul>
				</div>
				<div class="relative z-10 flex-shrink-0 w-full md:w-auto">
					<router-link :to="{ name: 'Plus' }" class="flex items-center justify-center w-full md:w-auto gap-2 px-8 py-4 rounded-xl font-black text-[#08204e] bg-amber-400 hover:bg-amber-300 transition-transform hover:scale-105 shadow-xl shadow-amber-400/20 text-lg">
						<Crown class="size-6" /> {{ __('Desbloquear Plus') }}
					</router-link>
				</div>
				<div class="absolute right-[-10%] bottom-[-20%] w-[50%] h-[150%] bg-blue-600/20 rounded-full blur-3xl pointer-events-none"></div>
			</section>
		</main>

		<!-- Modal -->
		<Dialog :options="{ title: selectedPrompt?.title || '' }" v-model="isModalOpen">
			<template #body-content>
				<div v-if="selectedPrompt" class="p-1 space-y-6">
					<div class="flex items-center gap-2 text-sm font-bold text-blue-600 uppercase tracking-wider">
						<span>{{ selectedPrompt.category }}</span>
						<span class="text-gray-300">•</span>
						<span class="flex items-center gap-1 text-gray-500"><Clock class="size-3.5"/> {{ selectedPrompt.timeSaved }}</span>
					</div>
					
					<p class="text-gray-700 text-lg leading-relaxed">{{ selectedPrompt.description }}</p>
					
					<div v-if="selectedPrompt.variables?.length" class="bg-blue-50/50 border border-blue-100 rounded-lg p-4">
						<h4 class="text-sm font-bold text-gray-900 mb-3 flex items-center gap-1.5"><ArrowRight class="size-4 text-blue-500"/> {{ __('Variables necesarias') }}</h4>
						<div class="flex flex-wrap gap-2">
							<span v-for="variable in selectedPrompt.variables" :key="variable" class="px-2.5 py-1 bg-white border border-gray-200 rounded text-sm text-gray-600 font-medium font-mono shadow-sm">
								{{ '{' + '{' + variable + '}' + '}' }}
							</span>
						</div>
					</div>

					<div class="space-y-2">
						<h4 class="text-sm font-bold text-gray-900">{{ __('Prompt completo') }}</h4>
						<div class="relative group">
							<pre class="bg-gray-900 text-gray-100 p-4 md:p-5 rounded-xl whitespace-pre-wrap font-mono text-sm leading-relaxed overflow-x-auto shadow-inner">{{ selectedPrompt.prompt }}</pre>
							<button @click="copyPrompt(selectedPrompt.prompt)" class="absolute top-3 right-3 bg-white/10 hover:bg-white/20 text-white p-2 rounded-lg backdrop-blur-sm transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100 border border-white/10" :title="__('Copiar')">
								<Copy class="size-4" />
							</button>
						</div>
					</div>

					<div v-if="!selectedPrompt.isPremium" class="bg-amber-50 border border-amber-200 rounded-lg p-4">
						<h4 class="text-sm font-bold text-amber-900 mb-1">{{ __('Recomendación de uso') }}</h4>
						<p class="text-sm text-amber-800">{{ __('Copia este prompt y pégalo directamente en tu herramienta de IA favorita (ChatGPT, Claude o Gemini). Asegúrate de reemplazar las variables por tu información específica.') }}</p>
					</div>
					<div v-else class="bg-amber-50 border border-amber-200 rounded-lg p-5 flex flex-col sm:flex-row gap-4 items-center justify-between">
						<div>
							<h4 class="text-sm font-bold text-amber-900 mb-1 flex items-center gap-1"><Crown class="size-4 text-amber-600"/> {{ __('Prompt Premium') }}</h4>
							<p class="text-sm text-amber-800">{{ __('Desbloquea StudyBadge Plus para usar este y más de 100 prompts exclusivos.') }}</p>
						</div>
						<router-link :to="{ name: 'Plus' }" class="flex-shrink-0 px-5 py-2.5 bg-amber-400 text-amber-900 font-bold rounded-lg text-sm hover:bg-amber-500 transition-colors shadow-sm">
							{{ __('Desbloquear Plus') }}
						</router-link>
					</div>

					<div class="flex flex-col sm:flex-row gap-3 pt-2">
						<button v-if="!selectedPrompt.isPremium" @click="copyPrompt(selectedPrompt.prompt)" class="flex-1 flex justify-center items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-xl font-bold transition-colors shadow-md shadow-blue-600/20">
							<Copy class="size-5" /> {{ __('Copiar prompt') }}
						</button>
						<router-link v-else :to="{ name: 'Plus' }" class="flex-1 flex justify-center items-center gap-2 bg-amber-400 hover:bg-amber-500 text-amber-900 px-5 py-3 rounded-xl font-bold transition-colors shadow-md shadow-amber-400/20">
							<Crown class="size-5" /> {{ __('Desbloquear Plus') }}
						</router-link>
						
						<!-- Enlace para "Usar con IA" dentro del LMS -->
						<router-link :to="{ name: 'PracticeRoom' }" class="flex-1 flex justify-center items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-800 px-5 py-3 rounded-xl font-bold transition-colors border border-gray-200">
							<Zap class="size-5 text-amber-500" /> {{ __('Usar con IA') }}
						</router-link>
					</div>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Breadcrumbs, Dialog, toast, usePageMeta } from 'frappe-ui'
import { Check, Copy, Crown, Zap, Video, Search, ArrowDown, Target, Star, Clock, ArrowRight } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { promptsData } from '@/data/prompts'
import PromptCard from '@/components/PromptCard.vue'

const { brand } = sessionStore()

const breadcrumbs = computed(() => [
	{ label: __('Biblioteca de prompts'), route: { name: 'PromptLibrary' } },
])

usePageMeta(() => ({ title: __('Biblioteca de prompts'), icon: brand.favicon }))

// Filters State
const searchQuery = ref('')
const selectedCategory = ref('Todos')
const selectedObjective = ref('Todos')

// Constants
const categories = ['Todos', 'Productividad', 'Negocios', 'Marketing', 'Contenido', 'Estudio', 'Publicidad', 'Imágenes IA', 'Programación / IA']
const objectives = ['Todos', 'Ganar clientes', 'Ahorrar tiempo', 'Crear contenido', 'Estudiar mejor', 'Lanzar negocio', 'Crear imágenes']

// Popular Prompts
const popularPromptTitles = [
	"Plan de 100 primeros clientes",
	"Landing page que convierte",
	"30 Reels/TikToks virales",
	"Preparador de examen rápido"
]
const popularPrompts = computed(() => {
	return promptsData.filter(p => popularPromptTitles.includes(p.title))
})

// Filtered Prompts
const filteredPrompts = computed(() => {
	return promptsData.filter(prompt => {
		const matchSearch = prompt.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
							prompt.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
							prompt.category.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
							prompt.variables.some(v => v.toLowerCase().includes(searchQuery.value.toLowerCase()))
		const matchCat = selectedCategory.value === 'Todos' || prompt.category === selectedCategory.value
		const matchObj = selectedObjective.value === 'Todos' || prompt.objective === selectedObjective.value
		
		return matchSearch && matchCat && matchObj
	})
})

const showPopular = computed(() => {
	return searchQuery.value === '' && selectedCategory.value === 'Todos' && selectedObjective.value === 'Todos'
})

// Modal State
const isModalOpen = ref(false)
const selectedPrompt = ref(null)

function openModal(prompt) {
	selectedPrompt.value = prompt
	isModalOpen.value = true
}

function resetFilters() {
	searchQuery.value = ''
	selectedCategory.value = 'Todos'
	selectedObjective.value = 'Todos'
}

function scrollToPrompts() {
	document.getElementById('prompts-section')?.scrollIntoView({ behavior: 'smooth' })
}

async function copyPrompt(text) {
	try {
		await navigator.clipboard.writeText(text)
		toast.success(__('Copiado'), { description: __('El prompt se ha copiado al portapapeles.'), icon: Check })
	} catch (err) {
		toast.error(__('Error al copiar'), { description: __('No se pudo copiar el prompt.') })
	}
}
</script>

<style scoped>
:root[data-theme="dark"] .prompt-page {
	background-color: #0f172a;
}
:root[data-theme="dark"] .prompt-header {
	background-color: rgba(15, 23, 42, 0.9);
	border-color: #1e293b;
}
</style>

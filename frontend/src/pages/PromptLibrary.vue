<template>
	<div class="prompt-page min-h-screen pb-14">
		<header class="prompt-header sticky top-0 z-10 flex items-center justify-between border-b px-4 py-3 shadow-sm">
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<router-link :to="{ name: 'Practice' }" class="prompt-top-link">
				<Video class="size-4" /> {{ __('Practicar') }}
			</router-link>
		</header>

		<main class="mx-auto max-w-7xl px-5 py-8">
			<section class="prompt-hero">
				<div>
					<div class="prompt-kicker"><Zap class="size-4" /> {{ __('Biblioteca de prompts') }}</div>
					<h1>{{ __('Prompts listos para ahorrar horas') }}</h1>
					<p>{{ __('Productividad, negocios, contenido, marketing, estudio, publicidad e imágenes IA en un solo lugar.') }}</p>
				</div>
				<router-link v-if="library.data && !library.data.is_plus" :to="{ name: 'Plus' }" class="prompt-cta">
					<Crown class="size-4" /> {{ __('Desbloquear Plus') }}
				</router-link>
			</section>

			<div class="prompt-tabs">
				<button :class="{ active: selectedCategory === 'Todos' }" @click="selectedCategory = 'Todos'">{{ __('Todos') }}</button>
				<button v-for="category in library.data?.categories || []" :key="category" :class="{ active: selectedCategory === category }" @click="selectedCategory = category">
					{{ category }}
				</button>
			</div>

			<div v-if="library.loading" class="prompt-loading">{{ __('Cargando prompts...') }}</div>
			<div v-else class="prompt-grid">
				<article v-for="prompt in filteredPrompts" :key="`${prompt.category}-${prompt.title}`" class="prompt-card">
					<div class="prompt-card-head">
						<span>{{ prompt.category }}</span>
						<Lock v-if="prompt.locked" class="size-4 text-amber-500" />
						<CheckCircle2 v-else class="size-4 text-green-500" />
					</div>
					<h2>{{ prompt.title }}</h2>
					<p>{{ prompt.use_case }}</p>
					<div class="prompt-vars">
						<span v-for="variable in prompt.variables" :key="variable">{{ variable }}</span>
					</div>
					<pre>{{ prompt.locked ? prompt.prompt_preview : prompt.prompt }}</pre>
					<div class="prompt-actions">
						<button v-if="!prompt.locked" class="prompt-copy" @click="copyPrompt(prompt.prompt)">
							<Copy class="size-4" /> {{ __('Copiar') }}
						</button>
						<router-link v-else :to="{ name: 'Plus' }" class="prompt-copy locked">
							<Crown class="size-4" /> {{ __('Ver completo') }}
						</router-link>
					</div>
				</article>
			</div>
		</main>
	</div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Breadcrumbs, createResource, toast, usePageMeta } from 'frappe-ui'
import { CheckCircle2, Copy, Crown, Lock, Video, Zap } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const selectedCategory = ref('Todos')

const library = createResource({
	url: 'studybadge_ai.ai_practice.get_prompt_library',
	auto: true,
})

const breadcrumbs = computed(() => [
	{ label: __('Biblioteca de prompts'), route: { name: 'PromptLibrary' } },
])

const filteredPrompts = computed(() => {
	const prompts = library.data?.prompts || []
	if (selectedCategory.value === 'Todos') return prompts
	return prompts.filter((prompt) => prompt.category === selectedCategory.value)
})

usePageMeta(() => ({ title: __('Biblioteca de prompts'), icon: brand.favicon }))

async function copyPrompt(text) {
	await navigator.clipboard.writeText(text)
	toast.success(__('Prompt copiado.'))
}
</script>

<style scoped>
.prompt-page { background: #f6f8fc; color: #0f172a; }
.prompt-header { background: rgba(255,255,255,0.92); border-color: #e5e7eb; backdrop-filter: blur(12px); }
.prompt-top-link, .prompt-cta, .prompt-copy { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; min-height: 40px; border-radius: 8px; font-weight: 800; }
.prompt-top-link { color: #1d4ed8; font-size: 0.875rem; }
.prompt-hero { display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; border-radius: 8px; background: #061b49; color: white; padding: clamp(2rem, 5vw, 4rem); }
.prompt-kicker { display: flex; align-items: center; gap: 0.5rem; color: #fbbf24; font-size: 0.78rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0; }
.prompt-hero h1 { margin-top: 0.65rem; max-width: 780px; font-size: clamp(2.2rem, 5vw, 4.5rem); line-height: 1; font-weight: 900; letter-spacing: 0; }
.prompt-hero p { margin-top: 1rem; max-width: 650px; color: rgba(219, 234, 254, 0.88); font-size: 1.05rem; line-height: 1.65; }
.prompt-cta { flex-shrink: 0; background: #fbbf24; color: #78350f; padding: 0.65rem 1rem; }
.prompt-tabs { display: flex; gap: 0.5rem; overflow-x: auto; padding: 1.25rem 0; }
.prompt-tabs button { border: 1px solid #dbe3ef; border-radius: 999px; background: white; color: #475569; padding: 0.55rem 0.9rem; font-weight: 800; white-space: nowrap; }
.prompt-tabs button.active { background: #0d6efd; border-color: #0d6efd; color: white; }
.prompt-loading { padding: 3rem; text-align: center; color: #64748b; }
.prompt-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 1rem; }
.prompt-card { display: flex; min-height: 420px; flex-direction: column; border: 1px solid #e2e8f0; border-radius: 8px; background: white; padding: 1rem; box-shadow: 0 16px 38px rgba(15, 23, 42, 0.05); }
.prompt-card-head { display: flex; align-items: center; justify-content: space-between; color: #2563eb; font-size: 0.75rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0; }
.prompt-card h2 { margin-top: 0.75rem; font-size: 1.1rem; font-weight: 900; }
.prompt-card p { margin-top: 0.5rem; color: #64748b; line-height: 1.55; }
.prompt-vars { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.85rem; }
.prompt-vars span { border-radius: 999px; background: #eff6ff; color: #1d4ed8; padding: 0.25rem 0.55rem; font-size: 0.72rem; font-weight: 800; }
.prompt-card pre { flex: 1; margin-top: 1rem; white-space: pre-wrap; word-break: break-word; border-radius: 8px; background: #f8fafc; color: #334155; padding: 0.85rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.8rem; line-height: 1.55; }
.prompt-actions { display: flex; justify-content: flex-end; margin-top: 1rem; }
.prompt-copy { border: 1px solid #0d6efd; background: #0d6efd; color: white; padding: 0.55rem 0.85rem; }
.prompt-copy.locked { border-color: #f59e0b; background: #fef3c7; color: #92400e; }
:root[data-theme="dark"] .prompt-page { background: #0f172a; color: #e5e7eb; }
:root[data-theme="dark"] .prompt-header, :root[data-theme="dark"] .prompt-card, :root[data-theme="dark"] .prompt-tabs button { background: #111827; border-color: rgba(255,255,255,0.08); }
:root[data-theme="dark"] .prompt-card pre { background: #0b1220; color: #cbd5e1; }

@media (max-width: 768px) {
	.prompt-hero { padding: 1.25rem; align-items: flex-start; flex-direction: column; }
	.prompt-hero h1 { font-size: 1.75rem; margin-top: 0.5rem; }
	.prompt-hero p { font-size: 0.95rem; margin-top: 0.5rem; }
	.prompt-cta { width: 100%; justify-content: center; margin-top: 0.5rem; }
	.prompt-tabs { padding: 0.75rem 0; }
	.prompt-grid { grid-template-columns: 1fr; gap: 0.75rem; }
	.prompt-card { min-height: auto; padding: 1rem; }
	.prompt-card pre { max-height: 200px; overflow-y: auto; }
}
</style>

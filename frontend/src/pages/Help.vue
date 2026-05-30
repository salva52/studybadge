<template>
	<div class="min-h-screen bg-surface-gray-2 pb-12">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5 shadow-sm"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
		</header>

		<!-- Hero Section -->
		<div class="bg-gradient-to-br from-blue-900 to-indigo-900 text-white py-12 px-5 sm:py-16 sm:px-8 border-b border-indigo-800 shadow-inner relative overflow-hidden">
			<!-- Subtle background decoration -->
			<div class="absolute -top-24 -right-24 size-96 bg-blue-500 opacity-20 blur-3xl rounded-full"></div>
			<div class="absolute top-1/2 -left-24 size-64 bg-amber-500 opacity-20 blur-3xl rounded-full"></div>
			
			<div class="mx-auto max-w-5xl relative z-10">
				<div class="flex flex-col items-center text-center gap-4">
					<div class="rounded-2xl bg-white/10 p-4 ring-1 ring-white/20 backdrop-blur-md shadow-lg">
						<LifeBuoy class="size-10 stroke-1.5 text-blue-300" />
					</div>
					<div>
						<h1 class="text-4xl sm:text-5xl font-bold tracking-tight">
							Centro de <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-cyan-200">Ayuda</span>
						</h1>
						<p class="mt-4 text-lg sm:text-xl text-gray-300 max-w-2xl mx-auto font-medium">
							{{ __('Estamos aquí para apoyarte. Encuentra respuestas rápidas o contacta con nuestro equipo de soporte.') }}
						</p>
					</div>
				</div>
			</div>
		</div>

		<div class="mx-auto max-w-5xl px-5 py-10">
			<div class="space-y-12">
				
				<!-- Soporte Rápido -->
				<section>
					<h2 class="text-2xl font-bold text-ink-gray-9 mb-6 flex items-center gap-2">
						<Headset class="size-6 text-blue-600" />
						{{ __('¿Cómo podemos ayudarte?') }}
					</h2>
					
					<div class="grid gap-6 md:grid-cols-2">
						<!-- IA Bubble Info -->
						<div class="flex flex-col h-full rounded-2xl border border-blue-100 bg-surface-white p-6 sm:p-8 shadow-sm transition-all duration-300 hover:shadow-md hover:border-blue-200 relative overflow-hidden">
							<div class="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
								<Bot class="size-24 text-blue-600" />
							</div>
							<div class="rounded-xl bg-blue-50 w-fit p-3 mb-4">
								<Bot class="size-6 text-blue-600 stroke-1.5" />
							</div>
							<h3 class="text-xl font-bold text-ink-gray-9 mb-2">{{ __('Asistente de IA 24/7') }}</h3>
							<p class="text-ink-gray-6 mb-4 text-sm leading-relaxed flex-grow">
								{{ __('Nuestro asistente inteligente está disponible 24/7 para consultas generales o problemas con la plataforma en ') }}
								<strong>studybadge.com</strong>.
							</p>
							<div class="mt-auto pt-4 flex flex-col gap-3 border-t border-gray-100">
								<div class="flex items-start gap-2 text-xs text-amber-700 bg-amber-50 p-3 rounded-lg border border-amber-100">
									<Info class="size-4 shrink-0 mt-0.5" />
									<span>
										<strong>Nota importante:</strong> La burbuja de IA que ves en esta academia (academy.studybadge.com) es <em>exclusiva del Tutor IA</em> para resolver dudas de tus cursos, no para soporte técnico.
									</span>
								</div>
								<a
									href="https://studybadge.com"
									target="_blank"
									class="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-4 py-2 text-sm font-bold text-blue-600 shadow-sm ring-1 ring-inset ring-blue-200 hover:bg-blue-50 transition-colors w-full sm:w-auto"
								>
									<ExternalLink class="size-4" />
									{{ __('Ir a studybadge.com') }}
								</a>
							</div>
						</div>

						<!-- Correo Soporte -->
						<div class="flex flex-col h-full rounded-2xl border border-gray-200 bg-surface-white p-6 sm:p-8 shadow-sm transition-all duration-300 hover:shadow-md hover:border-gray-300 relative overflow-hidden">
							<div class="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
								<Mail class="size-24 text-gray-900" />
							</div>
							<div class="rounded-xl bg-gray-100 w-fit p-3 mb-4">
								<Mail class="size-6 text-gray-700 stroke-1.5" />
							</div>
							<h3 class="text-xl font-bold text-ink-gray-9 mb-2">{{ __('Contacto Directo') }}</h3>
							<p class="text-ink-gray-6 mb-4 text-sm leading-relaxed flex-grow">
								{{ __('¿Tienes un problema complejo, un error técnico, o una consulta sobre facturación? Nuestro equipo humano está listo para revisar tu caso a detalle.') }}
							</p>
							<div class="mt-auto pt-4 border-t border-gray-100">
								<a
									href="mailto:soporte@studybadge.com"
									class="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-bold text-white shadow-sm hover:bg-blue-700 transition-colors w-full sm:w-auto"
								>
									<Mail class="size-4" />
									{{ __('Escribir a soporte@studybadge.com') }}
								</a>
								<p class="text-xs text-gray-500 mt-3 text-center sm:text-left">
									{{ __('Respondemos de Lunes a Viernes en menos de 24 horas.') }}
								</p>
							</div>
						</div>
					</div>
				</section>

				<!-- Documentación Básica -->
				<section>
					<h2 class="text-2xl font-bold text-ink-gray-9 mb-6 flex items-center gap-2">
						<BookOpen class="size-6 text-amber-500" />
						{{ __('Guía Rápida / Preguntas Frecuentes') }}
					</h2>

					<div class="grid gap-4">
						<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
							<div class="flex items-start gap-4">
								<div class="rounded-full bg-blue-50 p-2 shrink-0">
									<GraduationCap class="size-5 text-blue-600 stroke-2" />
								</div>
								<div>
									<h3 class="font-bold text-ink-gray-9 text-lg">{{ __('¿Cómo empiezo un curso?') }}</h3>
									<p class="mt-2 text-sm text-ink-gray-6 leading-relaxed">
										Para empezar un curso, dirígete a la pestaña <strong>Cursos</strong> en el menú lateral. Haz clic en el curso que te interese y luego en el botón <strong>"Inscribirse"</strong> o <strong>"Empezar Curso"</strong>. Todo tu progreso se guardará automáticamente en tu perfil.
									</p>
								</div>
							</div>
						</div>

						<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
							<div class="flex items-start gap-4">
								<div class="rounded-full bg-amber-50 p-2 shrink-0">
									<Award class="size-5 text-amber-600 stroke-2" />
								</div>
								<div>
									<h3 class="font-bold text-ink-gray-9 text-lg">{{ __('¿Cómo obtengo mis certificaciones?') }}</h3>
									<p class="mt-2 text-sm text-ink-gray-6 leading-relaxed">
										Una vez que completes al 100% todas las lecciones y evaluaciones de un curso, se generará tu certificado automáticamente si cumples con los requisitos. Puedes descargarlo e integrarlo a LinkedIn desde la sección <strong>Certificaciones</strong> o desde tu perfil público.
									</p>
								</div>
							</div>
						</div>

						<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
							<div class="flex items-start gap-4">
								<div class="rounded-full bg-green-50 p-2 shrink-0">
									<User class="size-5 text-green-600 stroke-2" />
								</div>
								<div>
									<h3 class="font-bold text-ink-gray-9 text-lg">{{ __('¿Por qué debo completar mi perfil?') }}</h3>
									<p class="mt-2 text-sm text-ink-gray-6 leading-relaxed">
										Completar tu perfil con una foto, titular y biografía te permite acceder a una mejor experiencia. Además, un perfil completo es un requisito previo para ciertas actividades dentro de la plataforma y te ayuda a destacar ante reclutadores en los Rankings.
									</p>
								</div>
							</div>
						</div>
					</div>
				</section>
				
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import { Breadcrumbs, usePageMeta } from 'frappe-ui'
import {
	LifeBuoy,
	Headset,
	Bot,
	Mail,
	Info,
	ExternalLink,
	BookOpen,
	GraduationCap,
	Award,
	User
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()

const breadcrumbs = computed(() => [
	{
		label: __('Centro de Ayuda'),
		route: { name: 'Help' },
	},
])

usePageMeta(() => {
	return {
		title: __('Centro de Ayuda'),
		icon: brand.favicon,
	}
})
</script>

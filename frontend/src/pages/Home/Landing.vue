<template>
	<div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col font-sans">
		<!-- Navigation Bar -->
		<header class="w-full bg-white dark:bg-gray-800 shadow-sm border-b border-gray-100 dark:border-gray-700 py-4 px-6 flex justify-between items-center sticky top-0 z-50">
			<div class="flex items-center gap-2">
				<img :src="brand.favicon" alt="StudyBadge Logo" class="h-8 w-8" v-if="brand?.favicon" />
				<span class="text-xl font-extrabold text-blue-900 dark:text-white">StudyBadge</span>
			</div>
			<div class="flex items-center gap-4">
				<router-link :to="{ name: 'Courses' }" class="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 transition-colors">
					Ver Cursos
				</router-link>
				<a href="/login" class="text-sm font-semibold bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-full transition-colors shadow-md hover:shadow-lg">
					Iniciar Sesión
				</a>
			</div>
		</header>

		<!-- Hero Section -->
		<section class="flex-grow flex items-center justify-center relative overflow-hidden bg-white dark:bg-gray-900 px-6 py-20 lg:py-32">
			<!-- Decorative Background Blobs -->
			<div class="absolute top-0 right-0 -mr-32 -mt-32 w-[30rem] h-[30rem] rounded-full bg-blue-50 dark:bg-blue-900/20 blur-3xl opacity-60"></div>
			<div class="absolute bottom-0 left-0 -ml-32 -mb-32 w-[25rem] h-[25rem] rounded-full bg-indigo-50 dark:bg-indigo-900/20 blur-3xl opacity-60"></div>

			<div class="max-w-5xl mx-auto z-10 text-center flex flex-col items-center">
				<div class="inline-block bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 font-semibold px-4 py-1.5 rounded-full text-sm mb-6 border border-blue-100 dark:border-blue-800">
					🎉 La academia del futuro
				</div>
				
				<h1 class="text-5xl md:text-7xl font-extrabold text-gray-900 dark:text-white tracking-tight mb-8 leading-tight">
					Aprende habilidades reales.<br class="hidden md:block"/>
					<span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Impulsa tu carrera.</span>
				</h1>
				
				<p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mb-10 leading-relaxed">
					Únete a nuestra plataforma de aprendizaje interactivo. Desarrolla nuevas habilidades a tu propio ritmo, recibe tutorías con Inteligencia Artificial y obtén certificados verificables.
				</p>
				
				<div class="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
					<a href="/login" class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-bold text-lg px-8 py-4 rounded-xl shadow-xl shadow-blue-600/20 transition-all hover:-translate-y-1 hover:shadow-2xl">
						Empezar a Aprender
					</a>
					<router-link :to="{ name: 'Courses' }" class="w-full sm:w-auto bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-600 font-bold text-lg px-8 py-4 rounded-xl transition-all">
						Explorar Catálogo
					</router-link>
				</div>

				<!-- Stats / Trust Indicators -->
				<div class="mt-16 grid grid-cols-2 md:grid-cols-3 gap-8 md:gap-16 border-t border-gray-100 dark:border-gray-800 pt-10">
					<div class="flex flex-col items-center">
						<div class="text-3xl font-black text-gray-900 dark:text-white">100%</div>
						<div class="text-sm font-medium text-gray-500 mt-1">Online y Flexible</div>
					</div>
					<div class="flex flex-col items-center">
						<div class="text-3xl font-black text-gray-900 dark:text-white">TutorIA</div>
						<div class="text-sm font-medium text-gray-500 mt-1">Asistencia con IA</div>
					</div>
					<div class="flex flex-col items-center col-span-2 md:col-span-1">
						<div class="text-3xl font-black text-gray-900 dark:text-white">Certificados</div>
						<div class="text-sm font-medium text-gray-500 mt-1">Validados en la red</div>
					</div>
				</div>
			</div>
		</section>
	</div>
</template>

<script setup>
import { sessionStore } from '@/stores/session'
import { usePageMeta } from 'frappe-ui'

const { brand } = sessionStore()

usePageMeta(() => {
	return {
		title: __('Bienvenido a StudyBadge'),
		icon: brand?.favicon,
	}
})
</script>

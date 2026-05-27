<template>
	<header class="w-full bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 py-4 px-6 flex justify-between items-center sticky top-0 z-50">
		<div class="flex items-center gap-3">
			<img :src="brand?.favicon || '/assets/lms/images/studybadge/studybadge-logo.png'" alt="StudyBadge Logo" class="h-8 w-8" />
			<span class="text-xl font-extrabold text-[#061B49] dark:text-white tracking-tight">StudyBadge</span>
		</div>
		
		<!-- Desktop Nav -->
		<nav class="hidden md:flex items-center gap-8">
			<router-link :to="{ name: 'Courses' }" class="text-sm font-semibold text-gray-700 dark:text-gray-200 hover:text-[#007BFF] dark:hover:text-[#007BFF] transition-colors">
				Cursos
			</router-link>
			<a href="/certificates" class="text-sm font-semibold text-gray-700 dark:text-gray-200 hover:text-[#007BFF] dark:hover:text-[#007BFF] transition-colors">
				Certificados
			</a>
			<a href="/tutoria" class="text-sm font-semibold text-gray-700 dark:text-gray-200 hover:text-[#007BFF] dark:hover:text-[#007BFF] transition-colors">
				TutorIA
			</a>
			<a href="/instructors" class="text-sm font-semibold text-gray-700 dark:text-gray-200 hover:text-[#007BFF] dark:hover:text-[#007BFF] transition-colors">
				Para instructores
			</a>
		</nav>

		<div class="hidden md:flex items-center gap-4">
			<a href="/login" class="text-sm font-bold text-[#061B49] dark:text-gray-200 hover:text-[#007BFF] transition-colors">
				Iniciar sesión
			</a>
			<a href="/register" class="text-sm font-bold bg-[#007BFF] hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg transition-colors shadow-md hover:shadow-lg">
				Registrarse
			</a>
		</div>

		<!-- Mobile Nav Toggle (simplified) -->
		<div class="md:hidden flex items-center">
			<a href="/login" class="text-sm font-bold text-[#007BFF] dark:text-blue-400">
				Ingresar
			</a>
		</div>
	</header>
</template>

<script setup>
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
</script>

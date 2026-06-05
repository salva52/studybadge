<template>
	<FrappeUIProvider>
		<Layout class="isolate text-p-base">
			<router-view />
		</Layout>
		<InstallPrompt v-if="isMobile && !settings.data?.disable_pwa" />
		<Dialogs />
		<TutorIABubble v-if="showGlobalTutor" />
		<WelcomeTutorialModal />
	</FrappeUIProvider>
</template>
<script setup>
import TutorIABubble from '@/components/TutorIA/TutorIABubble.vue'
import WelcomeTutorialModal from '@/components/Modals/WelcomeTutorialModal.vue'
import { sessionStore } from '@/stores/session'
import { FrappeUIProvider } from 'frappe-ui'
import { Dialogs, createDialog } from '@/utils/dialogs'
import { computed, onUnmounted, onMounted, ref } from 'vue'
import { useScreenSize } from './utils/composables'
import { useSettings } from '@/stores/settings'
import { useRouter, useRoute } from 'vue-router'
import DesktopLayout from './components/Layouts/DesktopLayout.vue'
import MobileLayout from './components/Layouts/MobileLayout.vue'
import NoSidebarLayout from './components/Layouts/NoSidebarLayout.vue'
import InstallPrompt from './components/InstallPrompt.vue'

const { isMobile } = useScreenSize()
const router = useRouter()
const route = useRoute()
const noSidebar = ref(false)
const { settings } = useSettings()
const { isLoggedIn } = sessionStore()

const hiddenGlobalTutorRoutes = [
	'Lesson', 
	'LessonForm',
	'SCORMChapter',
	'Assignments', 
	'AssignmentSubmission', 
	'AssignmentSubmissionList',
	'Quizzes', 
	'QuizPage', 
	'QuizForm',
	'QuizSubmission',
	'QuizSubmissionList',
	'ProgrammingExercises',
	'ProgrammingExerciseSubmissions',
	'ProgrammingExerciseSubmission'
]

const showGlobalTutor = computed(() => {
	if (!isLoggedIn) return false
	if (hiddenGlobalTutorRoutes.includes(route.name)) return false
	return true
})

router.beforeEach((to, from, next) => {
	if (
		to.query.fromLesson ||
		to.path === '/persona' ||
		to.name === 'Teach' ||
		(!isLoggedIn && to.name === 'Courses')
	) {
		noSidebar.value = true
	} else {
		noSidebar.value = false
	}
	next()
})

const Layout = computed(() => {
	if (noSidebar.value) {
		return NoSidebarLayout
	}
	if (isMobile.value) {
		return MobileLayout
	}
	return DesktopLayout
})

onUnmounted(() => {
	noSidebar.value = false
})

onMounted(() => {
	const match = document.cookie.match(new RegExp("(^| )show_launch_fireworks=([^;]+)"))
	if (match && match[2] === "1") {
		// Clear cookie
		document.cookie = "show_launch_fireworks=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
		
		// Load confetti script dynamically
		const script = document.createElement('script')
		script.src = "https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"
		script.onload = () => {
			const duration = 5 * 1000
			const end = Date.now() + duration
			
			;(function frame() {
				window.confetti({
					particleCount: 5,
					angle: 60,
					spread: 55,
					origin: { x: 0 },
					colors: ['#0a2251', '#f5b301', '#ffffff']
				})
				window.confetti({
					particleCount: 5,
					angle: 120,
					spread: 55,
					origin: { x: 1 },
					colors: ['#0a2251', '#f5b301', '#ffffff']
				})

				if (Date.now() < end) {
					requestAnimationFrame(frame)
				}
			}())
		}
		document.head.appendChild(script)

		// Show congratulatory dialog
		setTimeout(() => {
			createDialog({
				title: '¡Felicidades!',
				message: '¡Reclamaste tu mes Plus por lanzamiento! Disfrútalo.',
				actions: [
					{
						label: 'Genial',
						theme: 'blue',
						onClick: (dialog) => {
							dialog.show = false
						}
					}
				]
			})
		}, 800)
	}
})
</script>

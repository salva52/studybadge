<template>
	<FrappeUIProvider>
		<Layout class="isolate text-p-base">
			<router-view />
		</Layout>
		<InstallPrompt v-if="isMobile && !settings.data?.disable_pwa" />
		<Dialogs />
		<TutorIABubble v-if="showGlobalTutor" />
	</FrappeUIProvider>
</template>
<script setup>
import TutorIABubble from '@/components/TutorIA/TutorIABubble.vue'
import { sessionStore } from '@/stores/session'
import { FrappeUIProvider } from 'frappe-ui'
import { Dialogs } from '@/utils/dialogs'
import { computed, onUnmounted, ref } from 'vue'
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
	if (to.query.fromLesson || to.path === '/persona' || to.path === '/landing') {
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
</script>

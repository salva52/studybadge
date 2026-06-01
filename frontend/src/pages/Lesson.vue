<template>
	<div v-if="lesson.data" class="">
		<header
			class="sticky top-0 z-10 flex items-center justify-between gap-4 border-b bg-white/95 backdrop-blur-sm px-4 py-3 sm:px-6 shadow-sm"
		>
			<div class="min-w-0 flex-1">
				<Breadcrumbs class="h-7 truncate-breadcrumbs" :items="breadcrumbs" />
			</div>
			<div class="flex shrink-0 items-center gap-x-2">
				<Tooltip v-if="canGoZen()" :text="__('Zen Mode')">
					<Button @click="goFullScreen()">
						<template #icon>
							<Focus class="w-4 h-4 stroke-2" />
						</template>
					</Button>
				</Tooltip>
				<Button v-if="isAdmin" @click="showVideoStats()">
					<template #icon>
						<TrendingUp class="size-4 stroke-1.5" />
					</template>
				</Button>
				<CertificationLinks :courseName="courseName" />
				<Button v-if="lesson.data.prev" @click="switchLesson('prev')">
					<template #prefix>
						<ChevronLeft class="w-4 h-4 stroke-1" />
					</template>
					<span>
						{{ __('Anterior') }}
					</span>
				</Button>

				<router-link
					v-if="allowEdit()"
					:to="{
						name: 'LessonForm',
						params: {
							courseName: courseName,
							chapterNumber: props.chapterNumber,
							lessonNumber: props.lessonNumber,
						},
					}"
				>
					<Button>
						{{ __('Editar') }}
					</Button>
				</router-link>

				<Button v-if="lesson.data.next" @click="switchLesson('next')">
					<template #suffix>
						<ChevronRight class="w-4 h-4 stroke-1" />
					</template>
						<span>
						{{ __('Siguiente') }}
					</span>
				</Button>

				<router-link
					v-else
					:to="{
						name: 'CourseDetail',
						params: { courseName: courseName },
					}"
				>
					<Button>
						{{ __('Volver al Curso') }}
					</Button>
				</router-link>
			</div>
		</header>
		<div class="lesson-layout">
			<div v-if="lesson.data.no_preview" class="border-e">
				<div class="shadow rounded-md w-3/4 mt-10 mx-auto text-center p-4">
					<div class="flex items-center justify-center mt-4 gap-x-2">
						<LockKeyholeIcon class="size-4 stroke-2 text-ink-gray-5" />
						<div class="text-lg font-semibold text-ink-gray-7">
							{{ __('Esta lección está bloqueada') }}
						</div>
					</div>
					<div class="mt-1 mb-4 text-ink-gray-7">
						{{
							__(
								'Esta lección no está disponible para vista previa. Inscríbete en el curso para acceder.'
							)
						}}
					</div>
					<Button
						v-if="user.data && !lesson.data.disable_self_learning"
						@click="enrollStudent()"
						variant="solid"
					>
						{{ __('Empezar a Aprender') }}
					</Button>
					<Badge
						theme="blue"
						size="lg"
						v-else-if="lesson.data.disable_self_learning"
						class="mt-2"
					>
						{{ __('Contacta al administrador para inscribirte en este curso.') }}
					</Badge>
					<Button v-else @click="redirectToLogin()">
						<template #prefix>
							<LogIn class="w-4 h-4 stroke-1" />
						</template>
						{{ __('Iniciar sesión') }}
					</Button>
				</div>
			</div>
			<div
				v-else
				ref="lessonContainer"
				class="lesson-content-area"
				:class="{
					'overflow-y-auto': zenModeEnabled,
				}"
			>
				<div
					class="lesson-content-inner"
					:class="{
						'w-full md:w-3/5 mx-auto border-none !pt-10': zenModeEnabled,
					}"
				>
					<div class="lesson-article min-w-0 max-w-full">
						<div
							class="flex flex-col space-y-3 md:space-y-0 md:flex-row md:items-center justify-between"
						>
							<div class="flex flex-col">
								<h1 class="lesson-title">
									{{ lesson.data.title }}
								</h1>

								<div
									v-if="zenModeEnabled"
									class="relative flex items-center gap-x-2 text-sm mt-1 text-ink-gray-7 group w-fit mt-2"
								>
									<span>
										{{ lesson.data.chapter_title }} -
										{{ lesson.data.course_title }}
									</span>
									<Info class="size-3" />
									<div
										class="hidden group-hover:block rounded bg-gray-900 px-2 py-1 text-xs text-white shadow-xl absolute start-0 top-full mt-2"
									>
										{{ Math.ceil(lesson.data.membership.progress) }}%
										{{ __('completado') }}
									</div>
								</div>
							</div>

							<div
								v-if="zenModeEnabled"
								class="flex items-center gap-x-2 mt-2 md:mt-0"
							>
								<Button @click="showDiscussionsInZenMode()">
									<template #icon>
										<MessageCircleQuestion class="w-4 h-4 stroke-1.5" />
									</template>
								</Button>
								<Button v-if="lesson.data.prev" @click="switchLesson('prev')">
									<template #prefix>
										<ChevronLeft class="w-4 h-4 stroke-1" />
									</template>
									<span>
										{{ __('Anterior') }}
									</span>
								</Button>

								<router-link
									v-if="allowEdit()"
									:to="{
										name: 'LessonForm',
										params: {
											courseName: courseName,
											chapterNumber: props.chapterNumber,
											lessonNumber: props.lessonNumber,
										},
									}"
								>
									<Button>
										{{ __('Editar') }}
									</Button>
								</router-link>

								<Button v-if="lesson.data.next" @click="switchLesson('next')">
									<template #suffix>
										<ChevronRight class="w-4 h-4 stroke-1" />
									</template>
									<span>
										{{ __('Siguiente') }}
									</span>
								</Button>

								<router-link
									v-else
									:to="{
										name: 'CourseDetail',
										params: { courseName: courseName },
									}"
								>
									<Button>
										{{ __('Volver al Curso') }}
									</Button>
								</router-link>
							</div>
						</div>

						<div v-if="!zenModeEnabled" class="lesson-meta">
							<span
								class="h-6 me-1"
								:class="{
									'avatar-group overlap': lesson.data.instructors?.length > 1,
								}"
							>
								<UserAvatar
									v-for="instructor in lesson.data.instructors"
									:user="instructor"
								/>
							</span>
							<CourseInstructors
								v-if="lesson.data?.instructors"
								:instructors="lesson.data.instructors"
							/>
						</div>

						<LessonTTSReader
							v-if="lessonSpeechSegments.length"
							:title="lesson.data.title"
							:segments="lessonSpeechSegments"
						/>

						<div
							v-if="
								lesson.data.instructor_content &&
								JSON.parse(lesson.data.instructor_content)?.blocks?.length >
									1 &&
								allowInstructorContent()
							"
							class="bg-surface-gray-2 p-3 rounded-md mt-6"
						>
							<div class="text-ink-gray-5 font-medium">
								{{ __('Notas del Instructor') }}
							</div>
							<div
								id="instructor-content"
								class="ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal"
							></div>
						</div>
						<div
							v-else-if="lesson.data.instructor_notes"
							class="ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal mt-8"
						>
							<LessonContent :content="lesson.data.instructor_notes" />
						</div>
						<div
							v-if="lesson.data.content"
							@mouseup="toggleInlineMenu"
							class="lesson-body ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal min-w-0 overflow-x-auto break-words"
						>
							<div id="editor"></div>
						</div>
						<div
							v-else
							class="lesson-body ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal min-w-0 overflow-x-auto break-words"
						>
							<LessonContent
								v-if="lesson.data?.body"
								:content="lesson.data.body"
								:youtube="lesson.data.youtube"
								:quizId="lesson.data.quiz_id"
							/>
						</div>
					</div>
					<div
						v-if="lesson.data && (allowDiscussions || tabs.length > 1)"
						class="lesson-discussions"
						ref="discussionsContainer"
					>
						<TabButtons
							v-if="tabs.length > 1"
							:buttons="tabs"
							v-model="currentTab"
							class="w-fit mb-10"
						/>
						<Notes
							v-if="currentTab === 'Notes'"
							:lesson="lesson.data?.name"
							v-model:notes="notes"
							@updateNotes="updateNotes"
						/>
						<Discussions
							v-else-if="allowDiscussions"
							:title="'Questions'"
							:doctype="'Course Lesson'"
							:docname="lesson.data.name"
							:key="lesson.data.name"
							:emptyStateText="
								__('Haz una pregunta para obtener ayuda de la comunidad.')
							"
						/>
					</div>
				</div>
			</div>
			<aside class="lesson-sidebar">
				<div class="lesson-sidebar-inner">
					<div class="sidebar-course-header">
						<div class="sidebar-course-title">
							{{ lesson.data.course_title }}
						</div>
						<div
							v-if="user && lesson.data.membership"
							class="sidebar-progress-section"
						>
							<div class="sidebar-progress-label">
								<span>{{ __('Tu progreso') }}</span>
								<span class="sidebar-progress-value">{{ Math.ceil(lessonProgress) }}%</span>
							</div>
							<ProgressBar
								:progress="lessonProgress"
							/>
						</div>
					</div>
					<div class="sidebar-outline-scroll">
						<CourseOutline
							:courseName="courseName"
							:key="chapterNumber"
							:getProgress="lesson.data.membership ? true : false"
							:completedLesson="completedLesson"
						/>
					</div>
					<CourseTutor
						v-if="lesson.data?.studybadge_tutor_enabled && user?.data"
						:courseName="courseName"
						:courseTitle="lesson.data?.course_title || ''"
						:lessonTitle="lesson.data?.title || ''"
						:lessonContent="getLessonTextContent()"
					/>
				</div>
			</aside>
		</div>
	</div>
	<InlineLessonMenu
		v-if="lesson.data?.name"
		v-model="showInlineMenu"
		:lesson="lesson.data?.name"
		v-model:notes="notes"
		@updateNotes="updateNotes"
	/>
	<VideoStatistics
		v-if="isAdmin"
		v-model="showStatsDialog"
		:lessonName="lesson.data?.name"
		:lessonTitle="lesson.data?.title"
	/>
</template>
<script setup>
import {
	Badge,
	Breadcrumbs,
	Button,
	call,
	createListResource,
	createResource,
	TabButtons,
	Tooltip,
	usePageMeta,
	toast,
} from 'frappe-ui'
import {
	computed,
	watch,
	inject,
	ref,
	onMounted,
	onBeforeUnmount,
	nextTick,
} from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
	ChevronLeft,
	ChevronRight,
	LockKeyholeIcon,
	LogIn,
	Focus,
	Info,
	MessageCircleQuestion,
	TrendingUp,
} from 'lucide-vue-next'
import {
	getEditorTools,
	enablePlyr,
	highlightText,
	sanitizeEditorJs,
	htmlToText,
} from '@/utils'
import { sessionStore } from '@/stores/session'
import { useSidebar } from '@/stores/sidebar'
import EditorJS from '@editorjs/editorjs'
import LessonContent from '@/components/LessonContent.vue'
import LessonTTSReader from '@/components/LessonTTSReader.vue'
import CourseInstructors from '@/components/CourseInstructors.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import Discussions from '@/components/Discussions.vue'
import CertificationLinks from '@/components/CertificationLinks.vue'
import VideoStatistics from '@/components/Modals/VideoStatistics.vue'
import CourseOutline from '@/components/CourseOutline.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import Notes from '@/components/Notes/Notes.vue'
import InlineLessonMenu from '@/components/Notes/InlineLessonMenu.vue'
import CourseTutor from '@/components/TutorIA/CourseTutor.vue'
import { getLmsRoute } from '@/utils/basePath'

const user = inject('$user')
const socket = inject('$socket')
const router = useRouter()
const route = useRoute()
const allowDiscussions = ref(false)
const editor = ref(null)
const instructorEditor = ref(null)
const lessonProgress = ref(0)
const lessonContainer = ref(null)
const zenModeEnabled = ref(false)
const showStatsDialog = ref(false)
const hasQuiz = ref(false)
const discussionsContainer = ref(null)
const timer = ref(0)
const { brand } = sessionStore()
const sidebarStore = useSidebar()
const plyrSources = ref([])
const showInlineMenu = ref(false)
const currentTab = ref(null)
const completedLesson = ref(null)
let timerInterval = null

const tabs = ref([])

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
	chapterNumber: {
		type: String,
		required: true,
	},
	lessonNumber: {
		type: String,
		required: true,
	},
})

onMounted(() => {
	startTimer()
	sidebarStore.isSidebarCollapsed = true
	document.addEventListener('fullscreenchange', attachFullscreenEvent)
	socket.on('update_lesson_progress', (data) => {
		if (data.course === props.courseName) {
			lessonProgress.value = data.progress
		}
	})
})

const getLessonTextContent = () => {
	return lessonSpeechSegments.value.join('\n').substring(0, 3000)
}

const lessonSpeechSegments = computed(() => {
	if (!lesson.data) return []
	const segments = lesson.data.content
		? getEditorSpeechSegments(lesson.data.content)
		: getLegacySpeechSegments(lesson.data.body || '')
	if (lesson.data.title) {
		return [lesson.data.title, ...segments].filter(Boolean)
	}
	return segments
})

const getEditorSpeechSegments = (content) => {
	try {
		const blocks = JSON.parse(content)?.blocks || []
		return blocks.flatMap(getBlockSpeechSegments).filter(Boolean)
	} catch {
		return []
	}
}

const getBlockSpeechSegments = (block) => {
	const data = block?.data || {}
	if (['paragraph', 'header'].includes(block.type)) {
		return splitSpeechText(stripHtml(data.text))
	}
	if (block.type === 'list') {
		return flattenListItems(data.items).flatMap((item) =>
			splitSpeechText(stripHtml(item))
		)
	}
	if (block.type === 'checklist') {
		return (data.items || []).flatMap((item) =>
			splitSpeechText(stripHtml(item.text))
		)
	}
	if (block.type === 'quote') {
		return splitSpeechText(
			stripHtml([data.text, data.caption].filter(Boolean).join('. '))
		)
	}
	if (block.type === 'table') {
		return (data.content || []).flatMap((row) =>
			splitSpeechText(row.map(stripHtml).join(', '))
		)
	}
	if (block.type === 'markdown') {
		return getLegacySpeechSegments(data.markdown || data.text || '')
	}
	return []
}

const flattenListItems = (items = []) => {
	return items.flatMap((item) => {
		if (typeof item === 'string') return item
		return [
			item.content || item.text || '',
			...flattenListItems(item.items || []),
		]
	})
}

const getLegacySpeechSegments = (content) => {
	if (!content) return []
	return content
		.split(/\n{2,}/)
		.filter((block) => !block.includes('{{'))
		.flatMap((block) => splitSpeechText(stripMarkdown(block)))
}

const splitSpeechText = (text) => {
	return normalizeSpeechText(text)
		.split(/(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡0-9])/)
		.map((segment) => segment.trim())
		.filter((segment) => segment.length > 3)
		.slice(0, 80)
}

const normalizeSpeechText = (text = '') => {
	return text
		.replace(/\s+/g, ' ')
		.replace(/\s+([,.;:!?])/g, '$1')
		.trim()
}

const stripHtml = (value = '') => {
	return normalizeSpeechText(htmlToText(String(value)))
}

const stripMarkdown = (value = '') => {
	return stripHtml(
		String(value)
			.replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1')
			.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
			.replace(/[`*_>#-]/g, ' ')
	)
}

const attachFullscreenEvent = () => {
	if (document.fullscreenElement) {
		zenModeEnabled.value = true
		allowDiscussions.value = false
	} else {
		zenModeEnabled.value = false
		if (!hasQuiz.value) {
			allowDiscussions.value = true
		}
	}
}

onBeforeUnmount(() => {
	document.removeEventListener('fullscreenchange', attachFullscreenEvent)
	sidebarStore.isSidebarCollapsed = false
	trackVideoWatchDuration()
})

const lesson = createResource({
	url: 'lms.lms.utils.get_lesson',
	makeParams(values) {
		return {
			course: props.courseName,
			chapter: values ? values.chapter : props.chapterNumber,
			lesson: values ? values.lesson : props.lessonNumber,
		}
	},
	auto: true,
})

const setupLesson = (data) => {
	if (Object.keys(data).length === 0) {
		router.push({
			name: 'CourseDetail',
			params: { courseName: props.courseName },
		})
		return
	}
	if (data.is_scorm_package) {
		router.push({
			name: 'SCORMChapter',
			params: {
				courseName: props.courseName,
				chapterName: data.chapter_name,
			},
		})
	}
	lessonProgress.value = data.membership?.progress
	if (data.content) editor.value = renderEditor('editor', data.content)
	if (
		data.instructor_content &&
		JSON.parse(data.instructor_content)?.blocks?.length > 1
	)
		instructorEditor.value = renderEditor(
			'instructor-content',
			data.instructor_content
		)
	editor.value?.isReady.then(() => {
		checkIfDiscussionsAllowed()
	})
	checkQuiz()
}

const checkQuiz = () => {
	if (!editor.value && lesson.body) {
		const quizRegex = /\{\{ Quiz\(".*"\) \}\}/
		hasQuiz.value = quizRegex.test(lesson.body)
		if (!hasQuiz.value && !zenModeEnabled) {
			allowDiscussions.value = true
		} else {
			allowDiscussions.value = false
		}
	}
}

const renderEditor = (holder, content) => {
	if (document.getElementById(holder))
		document.getElementById(holder).innerHTML = ''
	return new EditorJS({
		holder: holder,
		tools: getEditorTools(),
		data: sanitizeEditorJs(JSON.parse(content)),
		readOnly: true,
		defaultBlock: 'embed',
		i18n: {
			direction: document.documentElement.dir === 'rtl' ? 'rtl' : 'ltr',
		},
	})
}

const markProgress = () => {
	if (user.data && lesson.data && !lesson.data.progress) {
		progress.submit(
			{},
			{
				onError(err) {
					console.error(err)
				},
			}
		)
	}
}

const progress = createResource({
	url: 'lms.lms.doctype.course_lesson.course_lesson.save_progress',
	makeParams() {
		return {
			lesson: lesson.data.name,
			course: props.courseName,
		}
	},
	onSuccess(data) {
		lessonProgress.value = data
		completedLesson.value = lesson.data?.name
	},
})

const notes = createListResource({
	doctype: 'LMS Lesson Note',
	filters: {
		lesson: lesson.data?.name,
		member: user.data?.name,
	},
	fields: ['name', 'color', 'highlighted_text', 'note'],
	cache: ['notes', lesson.data?.name, user.data?.name],
	onSuccess(data) {
		data.forEach((note) => {
			setTimeout(() => {
				highlightText(note)
			}, 500)
		})
	},
})

const breadcrumbs = computed(() => {
	let crumbs = [{ label: __('Cursos'), route: { name: 'Courses' } }]
	crumbs.push({
		label: lesson?.data?.course_title,
		route: { name: 'CourseDetail', params: { courseName: props.courseName } },
	})
	crumbs.push({
		label: lesson?.data?.title,
		route: {
			name: 'Lesson',
			params: {
				courseName: props.courseName,
				chapterNumber: props.chapterNumber,
				lessonNumber: props.lessonNumber,
			},
		},
	})
	return crumbs
})

const switchLesson = (direction) => {
	trackVideoWatchDuration()
	let lessonIndex =
		direction === 'prev'
			? lesson.data.prev.split('.')
			: lesson.data.next.split('.')

	router.push({
		name: 'Lesson',
		params: {
			courseName: props.courseName,
			chapterNumber: lessonIndex[0],
			lessonNumber: lessonIndex[1],
		},
	})
}

watch(
	[() => route.params.chapterNumber, () => route.params.lessonNumber],
	async (
		[newChapterNumber, newLessonNumber],
		[oldChapterNumber, oldLessonNumber]
	) => {
		if (newChapterNumber || newLessonNumber) {
			plyrSources.value = []
			await nextTick()
			resetLessonState(newChapterNumber, newLessonNumber)
			updateNotes()
			checkIfDiscussionsAllowed()
			checkQuiz()
		}
	}
)

const resetLessonState = (newChapterNumber, newLessonNumber) => {
	editor.value = null
	instructorEditor.value = null
	allowDiscussions.value = false
	lesson.submit({
		chapter: newChapterNumber,
		lesson: newLessonNumber,
	})
	clearInterval(timerInterval)
	timer.value = 0
}

const trackVideoWatchDuration = () => {
	if (!lesson.data.membership) return
	let videoDetails = getVideoDetails()
	videoDetails = videoDetails.concat(getPlyrSourceDetails())
	call('lms.lms.api.track_video_watch_duration', {
		lesson: lesson.data.name,
		videos: videoDetails,
	})
}

const getVideoDetails = () => {
	let details = []
	const videos = document.querySelectorAll('video')
	if (videos.length > 0) {
		videos.forEach((video) => {
			if (video.currentTime == video.duration) markProgress()
			details.push({
				source: video.src,
				watch_time: video.currentTime,
			})
		})
	}
	return details
}

const getPlyrSourceDetails = () => {
	let details = []
	plyrSources.value.forEach((source) => {
		if (source.currentTime == source.duration) markProgress()
		let src = cleanYouTubeUrl(source.source)
		details.push({
			source: src,
			watch_time: source.currentTime,
		})
	})
	return details
}

const cleanYouTubeUrl = (url) => {
	if (!url) return url
	const urlObj = new URL(url)
	urlObj.searchParams.delete('t')
	return urlObj.toString()
}

watch(
	() => lesson.data,
	async (data) => {
		setupLesson(data)
		startTimer()
		await getPlyrSource()
		updateNotes()
		const hasVideoListener =
			plyrSources.value.length > 0 || !!document.querySelector('video')
		if (data.icon == 'icon-youtube' && hasVideoListener) {
			clearInterval(timerInterval)
		}
	}
)

const getPlyrSource = async () => {
	await nextTick()
	if (plyrSources.value.length == 0) {
		plyrSources.value = await enablePlyr()
	}
	updateVideoWatchDuration()
}

const updateVideoWatchDuration = () => {
	if (lesson.data.videos && lesson.data.videos.length > 0) {
		lesson.data.videos.forEach((video) => {
			if (video.source.includes('youtube') || video.source.includes('vimeo')) {
				updatePlyrVideoTime(video)
			} else {
				updateVideoTime(video)
			}
		})
	}
	attachVideoEndedListeners()
}

const attachVideoEndedListeners = () => {
	const onVideoEnded = () => {
		markProgress()
		trackVideoWatchDuration()
	}

	document.querySelectorAll('video').forEach((video) => {
		if (!video._lmsEndedAttached) {
			video.addEventListener('ended', onVideoEnded)
			video._lmsEndedAttached = true
		}
	})

	plyrSources.value.forEach((plyrSource) => {
		if (!plyrSource._lmsEndedAttached) {
			plyrSource.on('ended', onVideoEnded)
			plyrSource.on('statechange', (event) => {
				if (event.detail?.code === 0) onVideoEnded()
			})
			plyrSource._lmsEndedAttached = true
		}
	})
}

const updatePlyrVideoTime = (video) => {
	plyrSources.value.forEach((plyrSource) => {
		let lastWatchedTime = 0
		let isSeeking = false

		plyrSource.on('ready', () => {
			if (plyrSource.source === video.source) {
				plyrSource.embed.seekTo(video.watch_time, true)
				plyrSource.play()
				plyrSource.pause()
			}
		})
	})
}

const updateVideoTime = (video) => {
	const videos = document.querySelectorAll('video')
	if (videos.length > 0) {
		videos.forEach((vid) => {
			if (vid.src === video.source) {
				let watch_time = video.watch_time < vid.duration ? video.watch_time : 0
				if (vid.readyState >= 1) {
					vid.currentTime = watch_time
				} else {
					vid.addEventListener('loadedmetadata', () => {
						vid.currentTime = watch_time
					})
				}
			}
		})
	}
}

const startTimer = () => {
	if (!lesson.data?.membership) return
	timerInterval = setInterval(() => {
		timer.value++
		if (timer.value == 30) {
			clearInterval(timerInterval)
			markProgress()
		}
	}, 1000)
}

onBeforeUnmount(() => {
	clearInterval(timerInterval)
})

const checkIfDiscussionsAllowed = () => {
	hasQuiz.value = false
	if (lesson.data?.content) {
		try {
			JSON.parse(lesson.data.content)?.blocks?.forEach((block) => {
				if (block.type === 'quiz') {
					hasQuiz.value = true
				}
			})
		} catch {
			// legacy markdown lessons
		}
	}

	if (
		!hasQuiz.value &&
		!zenModeEnabled.value &&
		(lesson.data?.membership ||
			user.data?.is_moderator ||
			user.data?.is_instructor)
	) {
		allowDiscussions.value = true
	} else {
		allowDiscussions.value = false
	}
}

const isAdmin = computed(() => {
	let isInstructor = lesson.data?.instructors?.includes(user.data?.name)
	return user.data?.is_moderator || isInstructor
})

const allowEdit = () => {
	if (window.read_only_mode) return false
	return isAdmin.value
}

const allowInstructorContent = () => {
	if (window.read_only_mode) return false
	return isAdmin.value
}

const enrollment = createResource({
	url: 'frappe.client.insert',
	makeParams() {
		return {
			doc: {
				doctype: 'LMS Enrollment',
				course: props.courseName,
				member: user.data?.name,
			},
		}
	},
})

const enrollStudent = () => {
	enrollment.submit(
		{},
		{
			onSuccess() {
				window.location.reload()
			},
			onError(err) {
				toast.error(__(err.messages?.[0] || err))
				console.error(err)
			},
		}
	)
}

const toggleInlineMenu = async () => {
	showInlineMenu.value = false
	await nextTick()
	let selection = window.getSelection()
	if (selection.toString()) {
		showInlineMenu.value = true
	}
}

const showVideoStats = () => {
	showStatsDialog.value = true
}

const canGoZen = () => {
	if (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	)
		return true
	if (lesson.data?.membership) return true
	return false
}

const goFullScreen = () => {
	if (lessonContainer.value.requestFullscreen) {
		lessonContainer.value.requestFullscreen()
	} else if (lessonContainer.value.mozRequestFullScreen) {
		lessonContainer.value.mozRequestFullScreen()
	} else if (lessonContainer.value.webkitRequestFullscreen) {
		lessonContainer.value.webkitRequestFullscreen()
	} else if (lessonContainer.value.msRequestFullscreen) {
		lessonContainer.value.msRequestFullscreen()
	}
}

const showDiscussionsInZenMode = () => {
	if (allowDiscussions.value) {
		allowDiscussions.value = false
	} else {
		allowDiscussions.value = true
		currentTab.value = 'Community'
		scrollDiscussionsIntoView()
	}
}

const scrollDiscussionsIntoView = () => {
	nextTick(() => {
		discussionsContainer.value?.scrollIntoView({
			behavior: 'smooth',
			block: 'center',
			inline: 'nearest',
		})
	})
}

const updateNotes = () => {
	if (!user.data) return
	notes.update({
		filters: {
			lesson: lesson.data?.name,
			member: user.data?.name,
		},
	})
	notes.reload()
}

watch(allowDiscussions, () => {
	if (!isAdmin.value) {
		if (!tabs.value.find((tab) => tab.value === 'Notes')) {
			tabs.value.push({
				label: __('Notes'),
				value: 'Notes',
			})
		}
		currentTab.value = 'Notes'
	} else {
		currentTab.value = allowDiscussions.value ? 'Community' : null
	}
	if (allowDiscussions.value) {
		if (!tabs.value.find((tab) => tab.value === 'Community')) {
			tabs.value.push({
				label: __('Community'),
				value: 'Community',
			})
		}
	}
})

const redirectToLogin = () => {
	window.location.href = `/login?redirect-to=${getLmsRoute(
		`courses/${props.courseName}`
	)}`
}

usePageMeta(() => {
	return {
		title: lesson?.data?.title,
		icon: brand.favicon,
	}
})
</script>
<style>
/* ==============================================
   LESSON PAGE — Layout
   ============================================== */

.lesson-layout {
	display: grid;
	grid-template-columns: 1fr;
	height: calc(100vh - 53px);
}

@media (min-width: 768px) {
	.lesson-layout {
		grid-template-columns: 1fr 340px;
	}
}

@media (min-width: 1280px) {
	.lesson-layout {
		grid-template-columns: 1fr 380px;
	}
}

/* ==============================================
   LESSON PAGE — Content Area
   ============================================== */

.lesson-content-area {
	background: var(--sb-white, #fff);
	overflow-y: auto;
	scroll-behavior: smooth;
}

.lesson-content-inner {
	border-inline-end: 1px solid rgba(6, 27, 73, 0.06);
	padding-top: 2.5rem;
	padding-bottom: 5rem;
	min-height: 100%;
}

.lesson-article {
	padding: 0 2rem;
	max-width: 52rem;
	margin: 0 auto;
	width: 100%;
}

@media (min-width: 768px) {
	.lesson-article {
		padding: 0 3rem;
	}
}

/* ==============================================
   LESSON PAGE — Title & Meta
   ============================================== */

.lesson-title {
	font-size: 2rem;
	font-weight: 800;
	color: var(--sb-dark, #061B49);
	line-height: 1.2;
	letter-spacing: -0.02em;
	margin: 0;
}

@media (min-width: 768px) {
	.lesson-title {
		font-size: 2.25rem;
	}
}

.lesson-meta {
	display: flex;
	align-items: center;
	margin-top: 1rem;
	padding-bottom: 1.75rem;
	border-bottom: 1px solid rgba(6, 27, 73, 0.08);
	margin-bottom: 0.5rem;
}

/* ==============================================
   LESSON PAGE — Body (EditorJS / Markdown)
   ============================================== */

.lesson-body {
	margin-top: 2rem;
}

/* Headings inside EditorJS */
.lesson-body .ce-header {
	font-weight: 700;
	color: var(--sb-dark, #061B49);
	line-height: 1.3;
	margin-top: 2.5rem;
	margin-bottom: 0.75rem;
	padding-bottom: 0.5rem;
	border-bottom: 2px solid rgba(0, 123, 255, 0.1);
}

.lesson-body .ce-header[data-placeholder]::before {
	color: #9ca3af;
}

.lesson-body h2.ce-header {
	font-size: 1.5rem;
}

.lesson-body h3.ce-header {
	font-size: 1.25rem;
	border-bottom: none;
}

.lesson-body h4.ce-header {
	font-size: 1.1rem;
	border-bottom: none;
}

/* Paragraphs */
.lesson-body .ce-paragraph {
	font-size: 1.0625rem;
	line-height: 1.85;
	color: #374151;
	margin-bottom: 0.25rem;
}

/* Lists */
.lesson-body .cdx-list {
	padding-left: 1.5rem;
	margin: 1rem 0;
}

.lesson-body .cdx-list__item {
	font-size: 1.0625rem;
	line-height: 1.85;
	color: #374151;
	padding: 0.15rem 0;
}

/* Quote/callout blocks */
.lesson-body .cdx-quote {
	border-left: 4px solid var(--sb-primary, #007BFF);
	background: rgba(0, 123, 255, 0.04);
	padding: 1rem 1.25rem;
	border-radius: 0 8px 8px 0;
	margin: 1.5rem 0;
}

.lesson-body .cdx-quote__text {
	font-size: 1.0625rem;
	line-height: 1.75;
	color: #374151;
	font-style: italic;
}

/* Images */
.lesson-body .image-tool__image-picture img,
.lesson-body .cdx-simple-image img {
	border-radius: 12px;
	border: 1px solid rgba(6, 27, 73, 0.08);
	box-shadow: 0 2px 8px rgba(6, 27, 73, 0.06);
	margin: 1.5rem 0;
}

/* Links */
.lesson-body a {
	color: var(--sb-primary, #007BFF);
	text-decoration: underline;
	text-decoration-color: rgba(0, 123, 255, 0.3);
	text-underline-offset: 3px;
	font-weight: 500;
	transition: all 0.15s ease;
}

.lesson-body a:hover {
	color: var(--sb-medium, #0A84FF);
	text-decoration-color: var(--sb-medium, #0A84FF);
}

/* Bold text */
.lesson-body b,
.lesson-body strong {
	color: var(--sb-dark, #061B49);
	font-weight: 600;
}

/* ==============================================
   LESSON PAGE — Discussions Section
   ============================================== */

.lesson-discussions {
	margin-top: 3rem;
	padding: 2rem 0 5rem;
	border-top: 2px solid rgba(6, 27, 73, 0.06);
	padding-left: 2rem;
	padding-right: 2rem;
}

@media (min-width: 768px) {
	.lesson-discussions {
		padding-left: 3rem;
		padding-right: 3rem;
	}
}

/* ==============================================
   LESSON PAGE — Sidebar
   ============================================== */

.lesson-sidebar {
	display: none;
	background: linear-gradient(180deg, #f9fafb 0%, #f3f4f6 100%);
	border-inline-start: 1px solid rgba(6, 27, 73, 0.06);
	overflow: hidden;
}

@media (min-width: 768px) {
	.lesson-sidebar {
		display: block;
	}
}

.lesson-sidebar-inner {
	position: sticky;
	top: 0;
	height: calc(100vh - 53px);
	display: flex;
	flex-direction: column;
	overflow: hidden;
}

.sidebar-course-header {
	padding: 1.25rem 1.25rem 1rem;
	background: white;
	border-bottom: 1px solid rgba(6, 27, 73, 0.06);
	flex-shrink: 0;
}

.sidebar-course-title {
	font-size: 1.05rem;
	font-weight: 700;
	color: var(--sb-dark, #061B49);
	line-height: 1.3;
	letter-spacing: -0.01em;
}

.sidebar-progress-section {
	margin-top: 0.875rem;
}

.sidebar-progress-label {
	display: flex;
	justify-content: space-between;
	align-items: center;
	font-size: 0.8125rem;
	color: #6b7280;
	margin-bottom: 0.375rem;
}

.sidebar-progress-value {
	font-weight: 600;
	color: var(--sb-primary, #007BFF);
}

.sidebar-outline-scroll {
	flex: 1;
	overflow-y: auto;
	padding: 0.5rem 0;
	scroll-behavior: smooth;
}

.sidebar-outline-scroll::-webkit-scrollbar {
	width: 4px;
}

.sidebar-outline-scroll::-webkit-scrollbar-track {
	background: transparent;
}

.sidebar-outline-scroll::-webkit-scrollbar-thumb {
	background: rgba(6, 27, 73, 0.12);
	border-radius: 4px;
}

/* ==============================================
   Legacy styles (preserved)
   ============================================== */

.avatar-group {
	display: inline-flex;
	align-items: center;
}

.avatar-group .avatar {
	transition: margin 0.1s ease-in-out;
}

.truncate-breadcrumbs {
	min-width: 0;
	flex: 1;
}

.truncate-breadcrumbs :deep(.whitespace-nowrap) {
	overflow: hidden;
	text-overflow: ellipsis;
}
.truncate-breadcrumbs :deep(.whitespace-nowrap a) {
	overflow: hidden;
	text-overflow: ellipsis;
	display: block;
}
.truncate-breadcrumbs :deep(.whitespace-nowrap a span) {
	overflow: hidden;
	text-overflow: ellipsis;
	display: block;
}

.lesson-content p {
	margin-bottom: 1.25rem;
	line-height: 1.8;
	font-size: 1.0625rem;
}

.lesson-content li {
	line-height: 1.8;
	font-size: 1.0625rem;
}

.lesson-content ol {
	list-style: auto;
	margin: revert;
	padding: 1rem;
}

.lesson-content ul {
	list-style: auto;
	padding: 1rem;
	margin: revert;
}

.lesson-content img {
	border: 1px solid theme('colors.gray.200');
	border-radius: 0.5rem;
}

.lesson-content code {
	display: block;
	overflow-x: auto;
	padding: 1rem 1.25rem;
	background: #011627;
	color: #d6deeb;
	border-radius: 0.5rem;
	margin: 1rem 0;
}

.lesson-content a {
	color: theme('colors.gray.900');
	text-decoration: underline;
	font-weight: 500;
}

.embed-tool__caption,
.cdx-simple-image__caption {
	display: none;
}

.ce-block__content {
	max-width: unset;
}

.codex-editor__redactor {
	padding-bottom: 0px !important;
}

.codeBoxHolder {
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	align-items: flex-start;
}

.codeBoxTextArea {
	width: 100%;
	min-height: 30px;
	padding: 10px;
	border-radius: 2px 2px 2px 0;
	border: none !important;
	outline: none !important;
	font: 14px monospace;
}

.codeBoxSelectDiv {
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	align-items: flex-start;
	position: relative;
}

.codeBoxSelectInput {
	border-radius: 0 0 20px 2px;
	padding: 2px 26px;
	padding-top: 0;
	padding-inline-end: 0;
	text-align: start;
	cursor: pointer;
	border: none !important;
	outline: none !important;
}

.codeBoxSelectDropIcon {
	position: absolute !important;
	inset-inline-start: 10px !important;
	bottom: 0 !important;
	width: unset !important;
	height: unset !important;
	font-size: 16px !important;
}

.codeBoxSelectPreview {
	display: none;
	flex-direction: column;
	justify-content: flex-start;
	align-items: flex-start;
	border-radius: 2px;
	box-shadow: 0 3px 15px -3px rgba(13, 20, 33, 0.13);
	position: absolute;
	top: 100%;
	margin: 5px 0;
	max-height: 30vh;
	overflow-x: hidden;
	overflow-y: auto;
	z-index: 10000;
}

.codeBoxSelectItem {
	width: 100%;
	padding: 5px 20px;
	margin: 0;
	cursor: pointer;
}

.codeBoxSelectItem:hover {
	opacity: 0.7;
}

.codeBoxSelectedItem {
	background-color: lightblue !important;
}

.codeBoxShow {
	display: flex !important;
}

.dark {
	color: #abb2bf;
	background-color: #282c34;
}

.light {
	color: #383a42;
	background-color: #fafafa;
}

.codeBoxTextArea {
	line-height: 1.7;
}

.tc-table {
	border-inline-start: 1px solid #e8e8eb;
}

.plyr__volume input[type='range'] {
	display: none;
}

.plyr__control--overlaid {
	background: radial-gradient(
		circle,
		rgba(0, 0, 0, 0.4) 0%,
		rgba(0, 0, 0, 0.5) 50%
	);
}

.plyr__control:hover {
	background: none;
}

.plyr--video {
	border: 1px solid theme('colors.gray.200');
	border-radius: 8px;
}

:root {
	--plyr-range-fill-background: white;
	--plyr-video-control-background-hover: transparent;
}

/* ==============================================
   Dark Mode — Lesson Page Overrides
   ============================================== */

:root[data-theme="dark"] .lesson-title,
.dark .lesson-title {
	color: #f3f4f6;
}

:root[data-theme="dark"] .lesson-body .ce-paragraph,
.dark .lesson-body .ce-paragraph {
	color: #d1d5db;
}

:root[data-theme="dark"] .lesson-body .ce-header,
.dark .lesson-body .ce-header {
	color: #f3f4f6;
	border-bottom-color: rgba(59, 130, 246, 0.15);
}

:root[data-theme="dark"] .lesson-body .cdx-list__item,
.dark .lesson-body .cdx-list__item {
	color: #d1d5db;
}

:root[data-theme="dark"] .lesson-body b,
:root[data-theme="dark"] .lesson-body strong,
.dark .lesson-body b,
.dark .lesson-body strong {
	color: #f3f4f6;
}

:root[data-theme="dark"] .lesson-meta,
.dark .lesson-meta {
	border-bottom-color: rgba(255, 255, 255, 0.08);
}

:root[data-theme="dark"] .lesson-content-inner,
.dark .lesson-content-inner {
	border-inline-end-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .lesson-sidebar,
.dark .lesson-sidebar {
	background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
	border-inline-start-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .sidebar-course-header,
.dark .sidebar-course-header {
	background: rgba(255, 255, 255, 0.03);
	border-bottom-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .sidebar-course-title,
.dark .sidebar-course-title {
	color: #f3f4f6;
}

:root[data-theme="dark"] .lesson-discussions,
.dark .lesson-discussions {
	border-top-color: rgba(255, 255, 255, 0.06);
}

:root[data-theme="dark"] .lesson-body .cdx-quote,
.dark .lesson-body .cdx-quote {
	background: rgba(59, 130, 246, 0.08);
	border-left-color: var(--sb-primary, #3b82f6);
}

:root[data-theme="dark"] .lesson-body .cdx-quote__text,
.dark .lesson-body .cdx-quote__text {
	color: #d1d5db;
}
</style>

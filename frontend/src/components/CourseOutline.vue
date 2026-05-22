<template>
	<div class="">
		<div
			v-if="title && (outline.data?.length || allowEdit)"
			class="flex items-center justify-between gap-x-2 mb-4 px-2"
			:class="{
				'sticky top-0 z-10 bg-surface-white border-b px-3 py-2.5 sm:px-5':
					allowEdit,
			}"
		>
			<div
				class="font-semibold text-lg leading-5 text-ink-gray-9"
				:class="{ 'font-medium text-p-base': allowEdit }"
			>
				{{ __(title) }}
			</div>
			<Button size="sm" v-if="allowEdit" @click="openChapterModal()">
				<template #prefix>
					<Plus class="size-4 stroke-1.5" />
				</template>
				{{ __('Añadir') }}
			</Button>
		</div>
		<div
			:class="{
				'bg-white dark:bg-gray-800 shadow-sb-soft border border-gray-100 dark:border-gray-700 rounded-2xl p-4': showOutline && outline.data?.length,
			}"
		>
			<Draggable
				:list="outline.data"
				:disabled="!allowEdit"
				item-key="name"
				group="chapters"
				@end="updateChapterOrder"
			>
				<template #item="{ element: chapter, index }">
					<div class="chapter-item">
						<Disclosure
							v-slot="{ open }"
							:key="chapter.name"
							:defaultOpen="openChapterDetail(chapter.idx)"
						>
							<DisclosureButton
								ref=""
								class="flex items-center w-full p-2 group"
							>
								<ChevronRight
									:class="{
										'rotate-90': open,
										'rtl:rotate-180': !open,
										hidden: chapter.is_scorm_package,
										open: index == 1,
									}"
									class="h-4 w-4 text-ink-gray-9 stroke-1 transform duration-200"
								/>
								<div
									class="text-base text-start text-ink-gray-9 font-medium leading-5 ms-2"
									@click="redirectToChapter(chapter)"
								>
									{{ chapter.title }}
								</div>
								<div class="flex ms-auto gap-x-4">
									<Tooltip :text="__('Editar Capítulo')" placement="bottom">
										<FilePenLine
											v-if="allowEdit"
											@click.prevent="openChapterModal(chapter)"
											class="h-4 w-4 text-ink-gray-9 invisible group-hover:visible"
										/>
									</Tooltip>
									<Tooltip :text="__('Eliminar Capítulo')" placement="bottom">
										<Trash2
											v-if="allowEdit"
											@click.prevent="trashChapter(chapter.name)"
											class="h-4 w-4 text-ink-red-3 invisible group-hover:visible"
										/>
									</Tooltip>
								</div>
								<Check
									v-if="
										chapter.is_scorm_package && isScormChapterComplete(chapter)
									"
									class="h-4 w-4 text-green-700"
								/>
							</DisclosureButton>
							<DisclosurePanel v-if="!chapter.is_scorm_package">
								<Draggable
									v-if="!chapter.is_scorm_package"
									:list="chapter.lessons"
									:disabled="!allowEdit"
									item-key="name"
									group="items"
									@end="updateOutline"
									:data-chapter="chapter.name"
								>
									<template #item="{ element: lesson }">
										<div
											class="outline-lesson ps-8 py-2 pe-4 rounded-lg transition-colors mb-1"
											:class="
												isActiveLesson(lesson.number) ? 'bg-blue-50 dark:bg-blue-900/30 !text-blue-700 dark:!text-blue-300 font-semibold' : 'text-ink-gray-9 hover:bg-gray-50 dark:hover:bg-gray-800'
											"
										>
											<router-link
												:to="{
													name: allowEdit ? 'LessonForm' : 'Lesson',
													params: {
														courseName: courseName,
														chapterNumber: lesson.number.split('-')[0],
														lessonNumber: lesson.number.split('-')[1],
													},
												}"
											>
												<div class="flex items-center text-sm leading-5 group">
													<MonitorPlay
														v-if="lesson.icon === 'icon-youtube'"
														class="h-4 w-4 stroke-1 me-2"
													/>
													<HelpCircle
														v-else-if="lesson.icon === 'icon-quiz'"
														class="h-4 w-4 stroke-1 me-2"
													/>
													<NotebookPen
														v-else-if="lesson.icon === 'icon-assignment'"
														class="h-4 w-4 stroke-1 me-2"
													/>
													<SquareCode
														v-else-if="lesson.icon === 'icon-code'"
														class="h-4 w-4 stroke-1 me-2"
													/>
													<FileText
														v-else-if="lesson.icon === 'icon-list'"
														class="h-4 w-4 text-ink-gray-9 stroke-1 me-2"
													/>
													{{ lesson.title }}
													<Trash2
														v-if="allowEdit"
														@click.prevent="
															trashLesson(lesson.name, chapter.name)
														"
														class="h-4 w-4 text-ink-red-3 ms-auto invisible group-hover:visible"
													/>
													<Check
														v-if="lesson.is_complete"
														class="h-4 w-4 text-green-700 ms-2"
													/>
												</div>
											</router-link>
										</div>
									</template>
								</Draggable>
								<div v-if="allowEdit" class="flex mt-2 mb-4 ps-8">
									<router-link
										v-if="!chapter.is_scorm_package"
										:to="{
											name: 'LessonForm',
											params: {
												courseName: courseName,
												chapterNumber: chapter.idx,
												lessonNumber: chapter.lessons.length + 1,
											},
										}"
									>
										<Button>
											{{ __('Añadir Lección') }}
										</Button>
									</router-link>
								</div>
							</DisclosurePanel>
						</Disclosure>
					</div>
				</template>
			</Draggable>
		</div>
	</div>
	<ChapterModal
		v-if="user.data"
		v-model="showChapterModal"
		v-model:outline="outline"
		:course="courseName"
		:chapterDetail="getCurrentChapter()"
	/>
</template>
<script setup>
import { Button, createResource, Tooltip, toast } from 'frappe-ui'
import { getCurrentInstance, inject, ref, watch } from 'vue'
import Draggable from 'vuedraggable'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import {
	Check,
	ChevronRight,
	FileText,
	FilePenLine,
	HelpCircle,
	MonitorPlay,
	NotebookPen,
	Plus,
	SquareCode,
	Trash2,
} from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import ChapterModal from '@/components/Modals/ChapterModal.vue'

const route = useRoute()
const router = useRouter()
const user = inject('$user')
const showChapterModal = ref(false)
const currentChapter = ref(null)
const app = getCurrentInstance()
const { $dialog } = app.appContext.config.globalProperties

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
	showOutline: {
		type: Boolean,
		default: false,
	},
	title: {
		type: String,
		default: '',
	},
	allowEdit: {
		type: Boolean,
		default: false,
	},
	getProgress: {
		type: Boolean,
		default: false,
	},
	completedLesson: {
		type: String,
		default: null,
	},
})

const outline = createResource({
	url: 'lms.lms.utils.get_course_outline',
	cache: ['course_outline', props.courseName],
	makeParams() {
		return {
			course: props.courseName,
			progress: props.getProgress,
		}
	},
	auto: true,
})

watch(
	() => props.courseName,
	() => {
		outline.reload()
	}
)

watch(
	() => props.completedLesson,
	(lessonName) => {
		if (!lessonName || !outline.data) return
		for (const chapter of outline.data) {
			const found = chapter.lessons?.find((l) => l.name === lessonName)
			if (found) {
				found.is_complete = true
				break
			}
		}
	}
)

const deleteLesson = createResource({
	url: 'lms.lms.api.delete_lesson',
	makeParams(values) {
		return {
			lesson: values.lesson,
			chapter: values.chapter,
		}
	},
	onSuccess() {
		outline.reload()
		toast.success(__('Lección eliminada exitosamente'))
	},
})

const updateLessonIndex = createResource({
	url: 'lms.lms.api.update_lesson_index',
	makeParams(values) {
		return {
			lesson: values.lesson,
			sourceChapter: values.sourceChapter,
			targetChapter: values.targetChapter,
			idx: values.idx,
		}
	},
	onSuccess() {
		toast.success(__('Lección movida exitosamente'))
	},
})

const updateChapterIndex = createResource({
	url: 'lms.lms.api.update_chapter_index',
	makeParams(values) {
		return {
			chapter: values.chapter,
			course: values.course,
			idx: values.idx,
		}
	},
	onSuccess() {
		toast.success(__('Capítulo movido exitosamente'))
	},
})

const trashLesson = (lessonName, chapterName) => {
	$dialog({
		title: __('¿Eliminar esta lección?'),
		message: __(
			'Eliminar esta lección la removerá permanentemente del curso. Esta acción no se puede deshacer. ¿Estás seguro de que deseas continuar?'
		),
		actions: [
			{
				label: __('Eliminar'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					deleteLesson.submit({
						lesson: lessonName,
						chapter: chapterName,
					})
					close()
				},
			},
		],
	})
}

const openChapterDetail = (index) => {
	const activeChapter = route.params.chapterNumber
	return activeChapter ? index == activeChapter : index == 1
}

const openChapterModal = (chapter = null) => {
	currentChapter.value = chapter
	showChapterModal.value = true
}

const getCurrentChapter = () => {
	return currentChapter.value
}

const updateOutline = (e) => {
	updateLessonIndex.submit({
		lesson: e.item.__draggable_context.element.name,
		sourceChapter: e.from.dataset.chapter,
		targetChapter: e.to.dataset.chapter,
		idx: e.newIndex,
	})
}

const updateChapterOrder = (e) => {
	updateChapterIndex.submit({
		chapter: e.item.__draggable_context.element.name,
		course: props.courseName,
		idx: e.newIndex,
	})
}

const deleteChapter = createResource({
	url: 'lms.lms.api.delete_chapter',
	makeParams(values) {
		return {
			chapter: values.chapter,
		}
	},
	onSuccess() {
		outline.reload()
		toast.success(__('Capítulo eliminado exitosamente'))
	},
})

const trashChapter = (chapterName) => {
	$dialog({
		title: __('¿Eliminar este capítulo?'),
		message: __(
			'Eliminar este capítulo también eliminará todas sus lecciones y lo removerá permanentemente del curso. Esta acción no se puede deshacer. ¿Estás seguro de que deseas continuar?'
		),
		actions: [
			{
				label: __('Eliminar'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					deleteChapter.submit({ chapter: chapterName })
					close()
				},
			},
		],
	})
}

const redirectToChapter = (chapter) => {
	if (!chapter.is_scorm_package) return
	event.preventDefault()
	if (props.allowEdit) return
	if (!user.data) {
		toast.success(__('Por favor inscríbete en el curso para ver esta lección'))
		return
	}

	router.push({
		name: 'SCORMChapter',
		params: {
			courseName: props.courseName,
			chapterName: chapter.name,
		},
	})
}

const isScormChapterComplete = (chapter) => {
	return chapter.lessons?.length && chapter.lessons.every((l) => l.is_complete)
}

const isActiveLesson = (lessonNumber) => {
	return (
		route.params.chapterNumber == lessonNumber.split('-')[0] &&
		route.params.lessonNumber == lessonNumber.split('-')[1]
	)
}
</script>

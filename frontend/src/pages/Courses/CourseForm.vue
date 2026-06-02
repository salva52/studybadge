<template>
	<div class="min-h-screen bg-surface-gray-1">
		<div
			v-if="courseResource.doc"
			class="mx-auto w-full max-w-[1440px] px-4 py-6 sm:px-6 lg:px-8"
		>
			<div class="mb-6">
				<div class="flex flex-col gap-2">
					<p class="text-xs font-medium uppercase tracking-wide text-ink-gray-5">
						{{ __('Course setup') }}
					</p>
					<div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
						<div>
							<h1 class="text-2xl font-semibold text-ink-gray-9">
								{{ courseResource.doc.title || __('Create a better course') }}
							</h1>
							<p class="mt-1 max-w-2xl text-sm leading-6 text-ink-gray-6">
								{{ __('Organiza la información del curso, configura la publicación y deja todo listo para tus estudiantes.') }}
							</p>
						</div>

						<div class="flex items-center gap-2 rounded-xl border border-outline-gray-2 bg-surface-white px-3 py-2 shadow-sm">
							<div
								class="size-2.5 rounded-full"
								:class="isDirty ? 'bg-orange-400' : 'bg-green-500'"
							></div>
							<span class="text-sm font-medium text-ink-gray-7">
								{{ isDirty ? __('Unsaved changes') : __('Saved') }}
							</span>
						</div>
					</div>
				</div>
			</div>

			<div class="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1fr)_360px]">
				<main class="min-w-0 space-y-6 pb-10">
					<section class="course-section">
						<SectionHeader
							:title="__('Details')"
							:description="__('Empieza con la información principal que verán los estudiantes.')"
						/>

						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<FormControl
								v-model="courseResource.doc.title"
								:label="__('Title')"
								:required="true"
								@input="makeFormDirty()"
							/>

							<Link
								v-model="courseResource.doc.category"
								doctype="LMS Category"
								:label="__('Category')"
								:inlineCreate="true"
								:onCreate="createCategory"
								@update:modelValue="makeFormDirty()"
							/>
						</div>

						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<MultiSelect
								v-if="user.data?.is_moderator"
								v-model="instructors"
								doctype="User"
								:label="__('Instructors')"
								url="lms.lms.api.search_users_by_role"
								:searchParams="{
									roles: JSON.stringify(['Course Creator', 'Batch Evaluator']),
								}"
								:onCreate="
									() => {
										memberModalRoles = ['course_creator']
										showMemberModal = true
									}
								"
								:required="true"
								@update:modelValue="makeFormDirty()"
							/>

							<div
								v-else
								class="rounded-xl border border-outline-gray-2 bg-surface-gray-1 p-4"
							>
								<div class="text-xs font-medium text-ink-gray-5">
									{{ __('Instructor') }}
								</div>
								<div class="mt-1 text-sm font-semibold text-ink-gray-8">
									{{ user.data?.full_name || user.data?.name }}
								</div>
							</div>

							<div>
								<label class="mb-1.5 block text-sm font-medium text-ink-gray-7">
									{{ __('Tags') }}
								</label>

								<div
									class="flex min-h-10 w-full cursor-text flex-wrap items-center gap-1.5 rounded-lg border border-outline-gray-2 bg-surface-gray-1 px-2.5 py-2 transition focus-within:border-outline-gray-4 focus-within:bg-surface-white focus-within:shadow-sm"
									@click="$refs.tagInput?.focus()"
								>
									<button
										v-for="tag in parsedTags"
										:key="tag"
										type="button"
										class="inline-flex items-center gap-1 rounded-md border border-outline-gray-2 bg-surface-white py-1 pe-1.5 ps-2 text-sm leading-5 text-ink-gray-7 transition hover:bg-surface-gray-2"
										@click.stop="removeTag(tag)"
									>
										<span>{{ tag }}</span>
										<X class="size-3.5 shrink-0 stroke-1.5" />
									</button>

									<input
										id="tags"
										ref="tagInput"
										v-model="newTag"
										type="text"
										:placeholder="
											!parsedTags.length
												? __('Add a keyword and press enter')
												: ''
										"
										class="min-w-[8rem] flex-1 border-none bg-transparent p-0 text-base outline-none placeholder:text-ink-gray-4 focus:ring-0"
										@keyup.enter="updateTags()"
									/>
								</div>

								<p class="mt-1.5 text-xs text-ink-gray-5">
									{{ __('Usa palabras clave para que los estudiantes encuentren mejor tu curso.') }}
								</p>
							</div>
						</div>

						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<Uploader
								v-model="courseResource.doc.image"
								:label="__('Course Image')"
								:required="false"
								@update:modelValue="makeFormDirty()"
							/>

							<ColorSwatches
								v-model="courseResource.doc.card_gradient"
								:label="__('Color')"
								:description="
									__(
										'Select a fallback color for the course card when no image is set.'
									)
								"
								class="w-full"
								@update:modelValue="makeFormDirty()"
							/>
						</div>
					</section>

					<section class="course-section">
						<SectionHeader
							:title="__('Publishing Settings')"
							:description="__('Controla cuándo y cómo se muestra tu curso en la plataforma.')"
						/>

						<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
							<div
								v-if="user.data?.is_moderator"
								class="settings-card"
							>
								<Switch
									size="sm"
									v-model="courseResource.doc.published"
									:label="__('Published')"
									:description="__('Make the course visible to all users.')"
									@change="makeFormDirty()"
								/>

								<FormControl
									v-model="courseResource.doc.published_on"
									:label="__('Published On')"
									type="date"
									@change="makeFormDirty()"
								/>
							</div>

							<div
								v-if="user.data?.is_moderator"
								class="settings-card"
							>
								<Switch
									size="sm"
									v-model="courseResource.doc.upcoming"
									:label="__('Upcoming')"
									:description="
										__(
											'Mark the course as upcoming but not yet open for enrollment.'
										)
									"
									@change="makeFormDirty()"
								/>

								<Switch
									size="sm"
									v-model="courseResource.doc.featured"
									:label="__('Featured')"
									:description="__('Highlight the course on the homepage.')"
									@change="makeFormDirty()"
								/>

								<Switch
									size="sm"
									v-model="selfEnrollment"
									:label="__('Allow Self Enrollment')"
									:description="
										__('Allow users to enroll in this course on their own.')
									"
								/>
							</div>

							<div
								v-else
								class="settings-card md:col-span-2"
							>
								<Switch
									size="sm"
									v-model="selfEnrollment"
									:label="__('Allow Self Enrollment')"
									:description="
										__('Allow users to enroll in this course on their own after approval.')
									"
								/>
							</div>
						</div>
					</section>

					<section class="course-section">
						<SectionHeader
							:title="__('About the Course')"
							:description="__('Explica el valor del curso de forma clara, atractiva y fácil de entender.')"
						/>

						<FormControl
							v-model="courseResource.doc.short_introduction"
							type="textarea"
							:rows="4"
							:label="__('Short Introduction')"
							:placeholder="
								__(
									'A one line introduction to the course that appears on the course card'
								)
							"
							:required="true"
							@change="makeFormDirty()"
						/>

						<div>
							<div class="mb-1.5 text-sm font-medium text-ink-gray-7">
								{{ __('Course Description') }}
								<span class="text-ink-red-3">*</span>
							</div>

							<div class="overflow-hidden rounded-xl border border-outline-gray-2 bg-surface-white">
								<TextEditor
									:content="courseResource.doc.description"
									@change="
										(val) => {
											courseResource.doc.description = val
											makeFormDirty()
										}
									"
									:editable="true"
									:fixedMenu="true"
									editorClass="prose-sm max-w-none bg-surface-white py-3 px-3 min-h-[10rem]"
								/>
							</div>
						</div>

						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<FormControl
								v-model="courseResource.doc.video_link"
								:label="__('Preview Video')"
								:description="
									__(
										'Paste a YouTube link of a short video introducing the course.'
									)
								"
								@input="makeFormDirty()"
							/>

							<MultiSelect
								v-model="related_courses"
								doctype="LMS Course"
								:label="__('Related Courses')"
								:filters="{ name: ['!=', courseResource.doc?.name] }"
								:onCreate="
									(close) => {
										router.push({
											name: 'Courses',
											query: { newCourse: '1' },
										})
									}
								"
								@update:modelValue="makeFormDirty()"
							/>
						</div>
					</section>

					<section class="course-section">
						<SectionHeader
							:title="__('Pricing and Certification')"
							:description="__('Define si el curso será gratuito, de pago o si tendrá certificado.')"
						/>

						<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
							<div class="settings-card">
								<Switch
									size="sm"
									v-model="courseResource.doc.paid_course"
									:label="__('Paid Course')"
									:description="__('Charge a fee for course access.')"
									@change="makeFormDirty()"
								/>
							</div>

							<div class="settings-card">
								<Switch
									size="sm"
									v-model="courseResource.doc.enable_certification"
									:label="__('Completion Certificate')"
									:description="__('Issue a certificate on course completion.')"
									@change="makeFormDirty()"
								/>
							</div>

							<div class="settings-card">
								<Switch
									size="sm"
									v-model="courseResource.doc.paid_certificate"
									:label="__('Paid Certificate')"
									:description="__('Charge a fee for the certificate.')"
									@change="makeFormDirty()"
								/>
							</div>
						</div>

						<div
							v-if="
								courseResource.doc.paid_course ||
								courseResource.doc.paid_certificate
							"
							class="rounded-xl border border-outline-gray-2 bg-surface-gray-1 p-4"
						>
							<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
								<FormControl
									v-model="courseResource.doc.course_price"
									:label="__('Amount')"
									@input="makeFormDirty()"
								/>

								<FormControl
									type="select"
									v-model="courseResource.doc.currency"
									:options="courseCurrencyOptions"
									:label="__('Currency')"
									:required="
										courseResource.doc.paid_course ||
										courseResource.doc.paid_certificate
									"
									@update:modelValue="makeFormDirty()"
								/>
							</div>

							<p class="mt-3 text-sm leading-6 text-ink-gray-6">
								{{ __('Puedes configurar tu precio en soles o dólares; nosotros haremos la conversión para compradores internacionales.') }}
							</p>
						</div>
					</section>

					<section class="course-section">
						<SectionHeader
							:title="__('Meta Tags')"
							:description="__('Mejora cómo aparece tu curso en buscadores y al compartirlo.')"
						/>

						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<FormControl
								v-model="meta.description"
								:label="__('Meta Description')"
								type="textarea"
								:rows="6"
								@input="makeFormDirty()"
							/>

							<FormControl
								v-model="meta.keywords"
								:label="__('Meta Keywords')"
								type="textarea"
								:rows="6"
								:placeholder="__('Comma separated keywords for SEO')"
								@input="makeFormDirty()"
							/>
						</div>
					</section>
				</main>

				<aside class="min-w-0">
					<div class="sticky top-24 space-y-4">
						<div class="rounded-2xl border border-outline-gray-2 bg-surface-white p-4 shadow-sm">
							<div class="mb-4">
								<h2 class="text-base font-semibold text-ink-gray-9">
									{{ __('Course structure') }}
								</h2>
								<p class="mt-1 text-sm leading-5 text-ink-gray-6">
									{{ __('Ordena capítulos y lecciones para que el curso sea fácil de seguir.') }}
								</p>
							</div>

							<div class="max-h-[calc(100vh-14rem)] overflow-y-auto pe-1">
								<CourseOutline
									:courseName="courseResource.doc.name"
									:title="__('Chapters')"
									:allowEdit="true"
								/>
							</div>
						</div>
					</div>
				</aside>
			</div>
		</div>

		<div
			v-else
			class="flex min-h-screen items-center justify-center bg-surface-gray-1 px-4"
		>
			<div class="rounded-2xl border border-outline-gray-2 bg-surface-white p-6 text-center shadow-sm">
				<p class="text-sm font-medium text-ink-gray-7">
					{{ __('Loading course...') }}
				</p>
			</div>
		</div>

		<NewMemberModal
			v-model="showMemberModal"
			:defaultRoles="memberModalRoles"
			@created="onMemberCreated"
		/>
	</div>
</template>

<script setup>
import {
	TextEditor,
	Switch,
	createResource,
	createDocumentResource,
	FormControl,
	usePageMeta,
	toast,
} from 'frappe-ui'
import {
	computed,
	inject,
	onMounted,
	onBeforeUnmount,
	ref,
	reactive,
	watch,
	getCurrentInstance,
	defineComponent,
	h,
} from 'vue'
import { getMetaInfo, updateMetaInfo, createLMSCategory } from '@/utils'
import { X } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import Link from '@/components/Controls/Link.vue'
import CourseOutline from '@/components/CourseOutline.vue'
import MultiSelect from '@/components/Controls/MultiSelect.vue'
import ColorSwatches from '@/components/Controls/ColorSwatches.vue'
import Uploader from '@/components/Controls/Uploader.vue'
import NewMemberModal from '@/components/Modals/NewMemberModal.vue'

const SectionHeader = defineComponent({
	name: 'SectionHeader',
	props: {
		title: {
			type: String,
			required: true,
		},
		description: {
			type: String,
			default: '',
		},
	},
	setup(props) {
		return () =>
			h('div', { class: 'mb-5 border-b border-outline-gray-2 pb-4' }, [
				h('h2', { class: 'text-lg font-semibold text-ink-gray-9' }, props.title),
				props.description
					? h(
							'p',
							{ class: 'mt-1 text-sm leading-6 text-ink-gray-6' },
							props.description
						)
					: null,
			])
	},
})

const user = inject('$user')
const newTag = ref('')
const router = useRouter()
const instructors = ref([])
const related_courses = ref([])
const app = getCurrentInstance()
const { $dialog } = app.appContext.config.globalProperties
const isDirty = ref(false)
const showMemberModal = ref(false)

const courseCurrencyOptions = [
	{ label: 'S/ PEN', value: 'PEN' },
	{ label: '$ USD', value: 'USD' },
]

const props = defineProps({
	course: {
		type: Object,
	},
})

const meta = reactive({
	description: '',
	keywords: '',
})

const courseResource = createDocumentResource({
	doctype: 'LMS Course',
	name: props.course.data?.name,
	auto: true,
})

const selfEnrollment = computed({
	get: () => !courseResource.doc?.disable_self_learning,
	set: (val) => {
		courseResource.doc.disable_self_learning = !val
		makeFormDirty()
	},
})

const evaluatorLinkRef = ref(null)
const memberModalRoles = ref(['course_creator'])

const parsedTags = computed(() => {
	const tags = courseResource.doc?.tags
	return tags ? tags.split(', ').filter(Boolean) : []
})

watch(
	() => courseResource.doc,
	() => {
		getMetaInfo('courses', courseResource.doc?.name, meta)
		updateCourseData()
		checkPermission()
	}
)

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		router.push({ name: 'Courses' })
	}
	window.addEventListener('keydown', keyboardShortcut)
})

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
})

const updateCourseData = () => {
	if (!courseResource.doc) return

	Object.keys(courseResource.doc).forEach((key) => {
		if (key == 'instructors') {
			instructors.value = []
			courseResource.doc.instructors?.forEach((instructor) => {
				instructors.value.push(instructor.instructor)
			})
		} else if (key == 'related_courses') {
			related_courses.value = []
			courseResource.doc.related_courses?.forEach((course) => {
				related_courses.value.push(course.course)
			})
		}
	})

	let checkboxes = [
		'published',
		'upcoming',
		'disable_self_learning',
		'paid_course',
		'featured',
		'enable_certification',
		'paid_certificate',
	]

	for (let idx in checkboxes) {
		let key = checkboxes[idx]
		courseResource.doc[key] = courseResource.doc[key] ? true : false
	}
}

const submitCourse = () => {
	return updateCourse()
}

const onMemberCreated = (user) => {
	if (memberModalRoles.value.includes('batch_evaluator')) {
		courseResource.doc.evaluator = user.name
		evaluatorLinkRef.value?.reload()
		makeFormDirty()
	} else {
		instructors.value = [...instructors.value, user.name]
		makeFormDirty()
	}
}

const updateCourse = () => {
	const nextInstructors = user.data?.is_moderator
		? instructors.value
		: [user.data?.name]

	return courseResource.setValue.submit(
		{
			...courseResource.doc,
			published: user.data?.is_moderator ? courseResource.doc.published : false,
			featured: user.data?.is_moderator ? courseResource.doc.featured : false,
			upcoming: user.data?.is_moderator ? courseResource.doc.upcoming : false,
			instructors: nextInstructors.filter(Boolean).map((instructor) => ({
				instructor: instructor,
			})),
			related_courses: related_courses.value.map((course) => ({
				course: course,
			})),
		},
		{
			onSuccess() {
				updateMetaInfo('courses', courseResource.doc?.name, meta)
				toast.success(__('Course updated successfully'))
				isDirty.value = false
				courseResource.reload()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
				console.error(err)
			},
		}
	)
}

const keyboardShortcut = (e) => {
	if (
		e.key === 's' &&
		(e.ctrlKey || e.metaKey) &&
		!e.target.classList.contains('ProseMirror')
	) {
		submitCourse()
		e.preventDefault()
	}
}

const deleteCourse = createResource({
	url: 'lms.lms.api.delete_course',
	makeParams(values) {
		return {
			course: courseResource.doc?.name,
		}
	},
	onSuccess() {
		toast.success(__('Course deleted successfully'))
		router.push({ name: 'Courses' })
	},
})

const trashCourse = () => {
	$dialog({
		title: __('Delete Course'),
		message: __(
			'Deleting the course will also delete all its chapters and lessons. Are you sure you want to delete this course?'
		),
		actions: [
			{
				label: __('Delete'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					deleteCourse.submit()
					close()
				},
			},
		],
	})
}

const updateTags = () => {
	const cleanTag = newTag.value?.trim()

	if (!cleanTag) return

	const currentTags = parsedTags.value

	if (!currentTags.includes(cleanTag)) {
		courseResource.doc.tags = courseResource.doc.tags
			? `${courseResource.doc.tags}, ${cleanTag}`
			: cleanTag
		makeFormDirty()
	}

	newTag.value = ''
}

const removeTag = (tag) => {
	courseResource.doc.tags = courseResource.doc.tags
		?.split(', ')
		.filter((t) => t !== tag)
		.join(', ')

	newTag.value = ''
	makeFormDirty()
}

const checkPermission = () => {
	if (!courseResource.doc) return

	let user_is_instructor = false

	if (user.data?.is_moderator) return

	instructors.value?.forEach((instructor) => {
		if (!user_is_instructor && instructor == user.data?.name) {
			user_is_instructor = true
		}
	})

	if (!user_is_instructor) {
		router.push({ name: 'Courses' })
	}
}

const createCategory = (name, done) => {
	createLMSCategory(name).then((categoryName) => {
		if (!categoryName) return
		courseResource.doc.category = categoryName
		done()
		makeFormDirty()
	})
}

const makeFormDirty = () => {
	isDirty.value = true
}

defineExpose({
	submitCourse,
	trashCourse,
	isDirty,
})
</script>

<style scoped>
.course-section {
	@apply rounded-2xl border border-outline-gray-2 bg-surface-white p-5 shadow-sm;
}

.settings-card {
	@apply flex flex-col gap-4 rounded-xl border border-outline-gray-2 bg-surface-gray-1 p-4;
}
</style>
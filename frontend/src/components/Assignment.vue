<template>
	<div
		v-if="assignment.data"
		:class="showTitle ? 'grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6 items-start' : 'flex flex-col gap-6 p-4'"
	>
		<div
			class="bg-white dark:bg-gray-800 shadow-sb-soft border border-gray-100 dark:border-gray-700 rounded-2xl p-6 md:p-8"
		>
			<div v-if="showTitle" class="text-lg font-semibold mb-5 text-ink-gray-9">
				<div v-if="submissionName === 'new'">
					{{ __('Submission by') }} {{ user.data?.full_name }}
				</div>
				<div v-else>
					{{ __('Submission by') }} {{ submissionResource.doc?.member_name }}
				</div>
			</div>
			<div class="flex items-center gap-x-4 mb-6 pb-4 border-b border-gray-100 dark:border-gray-700">
				<div class="bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 p-3 rounded-full flex-shrink-0">
					<FileText class="w-6 h-6 stroke-1.5" />
				</div>
				<div class="text-2xl font-bold text-ink-gray-9">
					{{ assignment.data.title }}
				</div>
			</div>
			<div
				v-html="assignment.data.question"
				class="ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal"
			></div>
		</div>

		<div class="flex flex-col space-y-6">
			<div class="bg-white dark:bg-gray-800 shadow-sb-soft border border-gray-100 dark:border-gray-700 rounded-2xl p-6 space-y-5">
				<div class="flex items-center justify-between">
					<div class="text-lg font-semibold text-ink-gray-9">
						{{ __('Tu Trabajo') }}
					</div>
					<div class="flex items-center gap-x-2">
						<Badge v-if="isDirty" theme="orange">
							{{ __('Not Saved') }}
						</Badge>
						<Badge
							v-else-if="submissionResource.doc?.status"
							:theme="statusTheme"
							size="lg"
						>
							{{ submissionResource.doc?.status }}
						</Badge>
						<Button
							v-if="canModifyAssignment || canGradeSubmission"
							variant="solid"
							@click="submitAssignment()"
						>
							{{ __('Save') }}
						</Button>
					</div>
				</div>
				<div
					v-if="
						submissionName != 'new' &&
						!['Pass', 'Fail'].includes(submissionResource.doc?.status) &&
						submissionResource.doc?.owner == user.data?.name
					"
					class="bg-surface-blue-2 text-ink-blue-2 p-3 rounded-md leading-5 text-sm"
				>
					{{ __("You've successfully submitted the assignment.") }}
					{{
						__(
							"Once the moderator grades your submission, you'll find the details here."
						)
					}}
					{{ __('Feel free to make edits to your submission if needed.') }}
				</div>
				<div v-if="showUploader()" class="bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700 rounded-xl p-5">
					<div class="font-semibold mb-1 text-ink-gray-9 text-base">
						{{ __('Subir Tarea') }}
					</div>
					<div class="text-ink-gray-5 text-sm mb-4">
						{{
							assignment.data.type == 'Document'
								? __('Se permiten archivos PDF y documentos Word (.doc, .docx)')
								: __('Solo se permiten archivos de tipo {0}').format(assignment.data.type)
						}}
					</div>
					<FileUploader
						v-if="!attachment"
						:fileTypes="getType()"
						:uploadArgs="{
							private: true,
						}"
						:validateFile="
							(file) =>
								validateFile(file, true, assignment.data.type.toLowerCase())
						"
						@success="(file) => saveSubmission(file)"
					>
						<template #default="{ uploading, progress, openFileSelector }">
							<Button @click="openFileSelector" :loading="uploading" variant="outline" class="w-full">
								<template #prefix>
									<FileText class="w-4 h-4 stroke-1.5" />
								</template>
								{{
									uploading
										? __('Subiendo {0}%').format(progress)
										: __('Subir Archivo')
								}}
							</Button>
						</template>
					</FileUploader>
					<div v-else>
						<div class="flex items-center justify-between text-ink-gray-7 border border-gray-200 dark:border-gray-700 rounded-lg p-2 pe-3">
							<a
								:href="attachment"
								target="_blank"
								class="cursor-pointer !no-underline text-sm leading-5 flex-1 overflow-hidden"
							>
								<div class="flex items-center">
									<div class="bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400 rounded-md p-2 me-3">
										<FileText class="h-5 w-5 stroke-1.5" />
									</div>
									<span class="truncate" :title="attachment.split('/').pop()">
										{{ attachment.split('/').pop() }}
									</span>
								</div>
							</a>
							<Button
								v-if="canModifyAssignment"
								@click="removeSubmission()"
								variant="ghost"
								class="text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20"
							>
								<template #icon>
									<X class="w-4 h-4" />
								</template>
							</Button>
						</div>
					</div>
				</div>
				<div v-else-if="assignment.data.type == 'URL'">
					<div class="text-xs text-ink-gray-5 mb-1">
						{{ __('Enter a URL') }}
					</div>
					<FormControl
						v-model="answer"
						type="text"
						:readonly="!canModifyAssignment"
					/>
				</div>
				<div v-else>
					<div class="text-sm mb-2 font-medium text-ink-gray-9">
						{{ __('Escribe tu respuesta aquí') }}
					</div>
					<TextEditor
						:content="answer"
						@change="(val) => (answer = val)"
						:editable="true"
						:fixedMenu="true"
						:readonly="!canModifyAssignment"
						:uploadArgs="{
							private: true,
						}"
						editorClass="prose-sm max-w-none border-b border-x border-outline-gray-modals bg-surface-gray-2 rounded-b-md py-1 px-2 min-h-[7rem]"
					/>
				</div>

				<!-- Chat con el Evaluador -->
				<div
					v-if="user.data?.name == submissionResource.doc?.owner && (chatHistory.length > 0 || submissionResource.doc?.comments)"
					class="mt-8 bg-white dark:bg-gray-800 shadow-sb-soft border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden"
				>
					<!-- Header -->
					<div class="flex items-center gap-x-3 px-5 py-4 border-b border-gray-100 dark:border-gray-700 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20">
						<div class="bg-blue-600 text-white p-2 rounded-full">
							<MessageCircleQuestion class="w-5 h-5" />
						</div>
						<div class="text-base font-semibold text-ink-gray-9">
							Retroalimentación y Chat
						</div>
					</div>

					<div class="p-5 flex flex-col space-y-4">
						<!-- Legacy or First Feedback -->
						<div v-if="chatHistory.length === 0 && submissionResource.doc?.comments" class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-xl border border-blue-100 dark:border-blue-800 text-sm leading-7 self-start max-w-[95%]">
							<div class="font-semibold text-xs text-blue-700 dark:text-blue-400 mb-2 flex items-center gap-x-1.5">
								<GraduationCap class="w-3.5 h-3.5" />
								Evaluador de StudyBadge
							</div>
							<div v-html="submissionResource.doc.comments" class="text-ink-gray-9"></div>
						</div>

						<!-- Chat History -->
						<div v-for="(msg, idx) in chatHistory" :key="idx"
							class="p-4 rounded-xl text-sm leading-7 max-w-[95%]"
							:class="msg.role === 'model'
								? 'bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 self-start'
								: 'bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 self-end'"
						>
							<div class="font-semibold text-xs mb-2 flex items-center gap-x-1.5"
								:class="msg.role === 'model' ? 'text-blue-700 dark:text-blue-400' : 'text-gray-600 dark:text-gray-400'"
							>
								<GraduationCap v-if="msg.role === 'model'" class="w-3.5 h-3.5" />
								{{ msg.role === 'model' ? 'Evaluador de StudyBadge' : 'Tú' }}
							</div>
							<div v-html="msg.content" class="text-ink-gray-9"></div>
						</div>

						<!-- Pending state -->
						<div v-if="submissionResource.doc?.ai_status === 'Pending'" class="flex items-center gap-x-2 text-sm text-blue-600 dark:text-blue-400 italic mt-1 animate-pulse self-start">
							<div class="flex gap-x-1">
								<span class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
								<span class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
								<span class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
							</div>
							El evaluador está escribiendo...
						</div>

						<!-- Reply Input -->
						<div v-if="replyCount < 3 && submissionResource.doc?.ai_status !== 'Pending'" class="mt-2 pt-4 border-t border-gray-100 dark:border-gray-700 flex flex-col">
							<div class="text-xs text-ink-gray-5 mb-3">
								Puedes responder o pedir que reconsideren tu calificación ({{ 3 - replyCount }} intentos restantes).
							</div>
							<FormControl v-model="chatMessage" type="textarea" placeholder="Escribe tu mensaje aquí..." class="mb-3" />
							<Button @click="submitReply" variant="solid" class="self-end" :loading="isSendingReply" :disabled="!chatMessage">
								Enviar Respuesta
							</Button>
						</div>
						<div v-else-if="replyCount >= 3" class="mt-2 pt-4 border-t border-gray-100 dark:border-gray-700 text-xs text-ink-gray-5 text-center">
							Has alcanzado el límite máximo de respuestas para esta evaluación.
						</div>
					</div>
				</div>

				<!-- Grading -->
				<div v-if="canGradeSubmission" class="mt-8 space-y-4">
					<div class="font-semibold mb-2 text-ink-gray-9">
						{{ __('Grading') }}
					</div>
					<FormControl
						v-if="submissionResource.doc"
						v-model="submissionResource.doc.status"
						:label="__('Grade')"
						type="select"
						:options="submissionStatusOptions"
					/>
					<div>
						<div class="text-sm text-ink-gray-5 mb-1">
							{{ __('Comments') }}
						</div>
						<TextEditor
							:content="comments"
							@change="
								(val) => {
									comments = val
									isDirty = true
								}
							"
							:editable="true"
							:fixedMenu="true"
							:uploadArgs="{
								private: true,
							}"
							editorClass="prose-sm max-w-none border-b border-x border-outline-gray-modals bg-surface-gray-2 rounded-b-md py-1 px-2 min-h-[7rem]"
						/>
					</div>
				</div>

			</div>
		</div>
	</div>
</template>
<script setup>
import {
	Badge,
	Button,
	call,
	createResource,
	createDocumentResource,
	FileUploader,
	FormControl,
	TextEditor,
	toast,
} from 'frappe-ui'
import { computed, inject, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { FileText, GraduationCap, MessageCircleQuestion, X } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { validateFile } from '@/utils'

const answer = ref(null)
const attachment = ref(null)
const comments = ref(null)
const router = useRouter()
const user = inject('$user')
const isDirty = ref(false)

const chatMessage = ref('')
const isSendingReply = ref(false)

const chatHistory = computed(() => {
	if (!submissionResource.doc?.ai_chat_history) return []
	try {
		return JSON.parse(submissionResource.doc.ai_chat_history)
	} catch (e) {
		return []
	}
})

const replyCount = computed(() => {
	return submissionResource.doc?.ai_reply_count || 0
})

const submitReply = () => {
	if (!chatMessage.value.trim()) return
	isSendingReply.value = true
	call('studybadge_ai.ai_grading.submit_student_reply', {
		submission_name: props.submissionName,
		message: chatMessage.value
	}).then(() => {
		chatMessage.value = ''
		toast.success(__('Reply sent to AI Evaluator'))
		submissionResource.reload()
	}).catch((err) => {
		toast.error(err.messages?.[0] || err)
	}).finally(() => {
		isSendingReply.value = false
	})
}

const props = defineProps({
	assignmentID: {
		type: String,
		required: true,
	},
	submissionName: {
		type: String,
		default: 'new',
	},
	showTitle: {
		type: Boolean,
		default: true,
	},
})

onMounted(() => {
	window.addEventListener('keydown', keyboardShortcut)
})

const keyboardShortcut = (e) => {
	if (e.key === 's' && (e.ctrlKey || e.metaKey)) {
		submitAssignment()
		e.preventDefault()
	}
}

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
})

const assignment = createResource({
	url: 'frappe.client.get',
	params: {
		doctype: 'LMS Assignment',
		name: props.assignmentID,
	},
	auto: true,
	onSuccess(data) {
		if (props.submissionName != 'new') {
			submissionResource.reload()
		}
	},
})

const submissionResource = createDocumentResource({
	doctype: 'LMS Assignment Submission',
	name: props.submissionName,
	auto: false,
	onError(err) {
		toast.error(err.messages?.[0] || err)
	},
})

watch(submissionResource, () => {
	if (!submissionResource.doc) return
	if (submissionResource.doc.answer) {
		answer.value = submissionResource.doc.answer
	}
	if (submissionResource.doc.assignment_attachment) {
		attachment.value = submissionResource.doc.assignment_attachment
	}
	if (submissionResource.doc.comments) {
		comments.value = submissionResource.doc.comments
	}
})

const submitAssignment = () => {
	if (props.submissionName != 'new') {
		updateSubmission()
	} else {
		addNewSubmission()
	}
}

const prepareSubmissionDoc = () => {
	let doc = {
		doctype: 'LMS Assignment Submission',
		assignment: props.assignmentID,
		member: user.data?.name,
	}
	if (!showUploader()) {
		doc.answer = answer.value
	} else {
		doc.assignment_attachment = attachment.value
	}
	return doc
}

const addNewSubmission = () => {
	let doc = prepareSubmissionDoc()
	if (!doc.assignment_attachment && !doc.answer) {
		toast.error(
			__('Please provide an answer or upload a file before submitting.')
		)
		return
	}
	call('frappe.client.insert', {
		doc: doc,
	})
		.then((data) => {
			toast.success(__('Assignment submitted successfully'))
			router.push({
				name: 'AssignmentSubmission',
				params: {
					assignmentID: props.assignmentID,
					submissionName: data.name,
				},
				query: { fromLesson: router.currentRoute.value.query.fromLesson },
			})
			markLessonProgress()
			isDirty.value = false
			submissionResource.name = data.name
			submissionResource.reload()
		})
		.catch((err) => {
			toast.error(err.messages?.[0] || err)
			console.error(err)
		})
}

const updateSubmission = () => {
	let evaluator =
		submissionResource.doc && submissionResource.doc.owner != user.data?.name
			? user.data?.name
			: null

	let status = submissionResource.doc?.status
	if (submissionResource.doc?.owner == user.data?.name) {
		status = 'Not Graded'
	}

	submissionResource.setValue.submit(
		{
			...submissionResource.doc,
			status: status,
			evaluator: evaluator,
			comments: comments.value,
			answer: answer.value,
			assignment_attachment: attachment.value,
		},
		{
			onSuccess(data) {
				isDirty.value = false
				toast.success(__('Changes saved successfully'))
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
				console.error(err)
			},
		}
	)
}

const saveSubmission = (file) => {
	isDirty.value = true
	attachment.value = file.file_url
}

const markLessonProgress = () => {
	let pathname = window.location.pathname.split('/')
	if (!pathname.includes('courses'))
		pathname = window.parent.location.pathname.split('/')
	if (pathname[2] != 'courses') return
	let lessonIndex = pathname.pop().split('-')

	if (lessonIndex.length == 2) {
		call('lms.lms.api.mark_lesson_progress', {
			course: pathname[3],
			chapter_number: lessonIndex[0],
			lesson_number: lessonIndex[1],
		})
	}
}

const getType = () => {
	const type = assignment.data?.type
	if (type == 'Image') {
		return ['image/*']
	} else if (type == 'Document') {
		return [
			'.doc',
			'.docx',
			'.xml',
			'.pdf',
			'application/msword',
			'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
			'application/pdf',
		]
	} else if (type == 'PDF') {
		return ['.pdf']
	}
}

const removeSubmission = () => {
	isDirty.value = true
	attachment.value = null
}

const canGradeSubmission = computed(() => {
	return (
		(user.data?.is_moderator ||
			user.data?.is_evaluator ||
			user.data?.is_instructor) &&
		props.submissionName != 'new' &&
		router.currentRoute.value.name == 'AssignmentSubmission'
	)
})

const canModifyAssignment = computed(() => {
	if (props.submissionName == 'new') {
		return true
	} else if (
		submissionResource.doc?.owner == user.data?.name &&
		['Not Graded', 'Fail'].includes(submissionResource.doc?.status)
	) {
		return true
	}
	return false
})

const submissionStatusOptions = computed(() => {
	return [
		{ label: 'Not Graded', value: 'Not Graded' },
		{ label: 'Pass', value: 'Pass' },
		{ label: 'Fail', value: 'Fail' },
	]
})

const statusTheme = computed(() => {
	if (!submissionResource.doc) {
		return 'orange'
	} else if (submissionResource.doc.status == 'Pass') {
		return 'green'
	} else if (submissionResource.doc.status == 'Not Graded') {
		return 'blue'
	} else {
		return 'red'
	}
})

const showUploader = () => {
	return ['PDF', 'Image', 'Document'].includes(assignment.data?.type)
}
</script>

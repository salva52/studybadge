<template>
	<div class="group-detail-page min-h-screen bg-[#f7f9fc] px-4 py-5 md:px-6">
		<header class="detail-header">
			<Button
				variant="ghost"
				class="back-button"
				@click="router.push({ name: 'Groups' })"
			>
				<template #icon><ArrowLeft class="size-4" /></template>
			</Button>

			<div class="header-copy">
				<p class="eyebrow">
					{{ groupDetails.data?.type === 'Course' ? 'Grupo de curso' : 'Grupo privado' }}
				</p>
				<h1>{{ groupDetails.data?.title || 'Cargando...' }}</h1>
				<p>
					{{ groupDetails.data?.member_count || 0 }} miembros activos en este espacio de estudio
				</p>
			</div>

			<Button
				v-if="isAdmin"
				variant="solid"
				class="primary-button"
				@click="showInviteModal = true"
			>
				<template #icon><UserPlus class="size-4" /></template>
				Invitar
			</Button>
		</header>

		<div class="detail-layout">
			<!-- Chat Area -->
			<section class="chat-shell">
				<div class="chat-topbar">
					<div>
						<p class="chat-kicker">Chat del grupo</p>
						<h2>Conversación principal</h2>
					</div>
					<div class="live-pill">
						<span></span>
						Activo
					</div>
				</div>

				<!-- Messages Container -->
				<div class="messages-area" ref="messagesContainer">
					<div v-if="messages.loading" class="messages-loading">
						<Spinner class="size-7 text-[#0d1e3e]" />
						<p>Cargando mensajes...</p>
					</div>

					<div v-else-if="!messages.data || messages.data.length === 0" class="empty-chat">
						<div class="empty-chat-icon">
							<Send class="size-7" />
						</div>
						<h3>Empieza la conversación</h3>
						<p>Escribe el primer mensaje para coordinar, estudiar o compartir ideas con tu grupo.</p>
					</div>

					<template v-else>
						<div
							v-for="msg in messages.data"
							:key="msg.name"
							class="message-row"
							:class="msg.user === currentUser ? 'is-current' : 'is-other'"
						>
							<UserAvatar :user="msg" class="message-avatar" />

							<div
								class="message-bubble"
								:class="msg.user === currentUser ? 'current-bubble' : 'other-bubble'"
							>
								<p
									v-if="msg.user !== currentUser"
									class="message-author"
								>
									{{ msg.full_name || msg.user }}
								</p>

								<div v-if="msg.attachment" class="mb-2 max-w-full">
									<img v-if="isImage(msg.attachment)" :src="msg.attachment" class="rounded-lg max-h-60 object-contain cursor-pointer" @click="openAttachment(msg.attachment)"/>
									<a v-else :href="msg.attachment" target="_blank" class="flex items-center gap-2 text-blue-500 hover:underline bg-white/10 p-2 rounded-lg">
										<FileText class="size-4"/>
										<span class="text-xs truncate">Ver Documento</span>
									</a>
								</div>

								<p v-if="msg.content" class="message-content">{{ msg.content }}</p>

								<p
									class="message-time"
									:class="msg.user === currentUser ? 'current-time' : 'other-time'"
								>
									{{ formatTime(msg.creation) }}
								</p>
							</div>
						</div>
					</template>
				</div>

				<!-- Message Input Wrapper -->
				<div class="composer-wrapper flex flex-col border-t border-outline-gray-2 bg-white rounded-b-3xl">
					<!-- Preview Section -->
					<div v-if="attachmentPreview" class="p-3 pb-0">
						<div class="relative inline-block border border-outline-gray-2 rounded-lg p-2 bg-surface-gray-1">
							<button class="absolute -top-2 -right-2 bg-white border border-outline-gray-2 text-ink-gray-5 hover:text-red-500 rounded-full p-0.5 shadow-sm" @click="attachmentPreview = null; attachmentName = ''">
								<X class="size-3" />
							</button>
							<img v-if="isImage(attachmentPreview)" :src="attachmentPreview" class="h-16 w-auto object-contain rounded" />
							<div v-else class="flex flex-col items-center justify-center w-20 h-16">
								<FileText class="size-6 text-blue-500 mb-1"/>
								<span class="text-[10px] text-ink-gray-7 truncate w-full text-center">{{ attachmentName || 'Documento' }}</span>
							</div>
						</div>
					</div>

					<!-- Message Input -->
					<div class="composer">
						<FileUploader
							:fileTypes="['image/*', 'application/pdf']"
							:validateFile="validateFile"
							@success="(file) => handleFileUploadSuccess(file)"
						>
							<template v-slot="{ file, progress, uploading, openFileSelector }">
								<Button
									variant="ghost"
									class="attach-button shrink-0"
									@click="openFileSelector"
									:loading="uploading"
								>
									<Paperclip class="size-5 text-ink-gray-5" />
								</Button>
							</template>
						</FileUploader>

						<FormControl
							v-model="newMessage"
							placeholder="Escribe un mensaje para tu grupo..."
							type="textarea"
							class="composer-input"
							:rows="1"
							autoresize
							@keydown.enter.prevent="sendMessage"
						/>

						<Button
							variant="solid"
							class="send-button"
							:disabled="!newMessage.trim() && !attachmentPreview"
							:loading="sending"
							@click="sendMessage"
						>
							<Send class="size-4" />
						</Button>
					</div>
				</div>
			</section>

			<!-- Sidebar Info -->
			<aside class="side-panel">
				<div class="info-card group/edit">
					<div class="card-heading">
						<div>
							<p class="side-kicker">Información</p>
							<h3>Acerca del grupo</h3>
						</div>

						<button
							v-if="isAdmin"
							@click="openEditModal"
							class="icon-button opacity-0 group-hover/edit:opacity-100"
							title="Editar Grupo"
						>
							<Settings class="size-4" />
						</button>
					</div>

					<p class="description-text">
						{{ groupDetails.data?.description || 'Sin descripción por ahora.' }}
					</p>
				</div>

				<div class="info-card members-card">
					<div class="card-heading">
						<div>
							<p class="side-kicker">Comunidad</p>
							<h3>Miembros</h3>
						</div>

						<span class="count-pill">
							{{ groupDetails.data?.members?.length || 0 }}
						</span>
					</div>

					<div
						v-if="!groupDetails.data?.members || groupDetails.data.members.length === 0"
						class="empty-members"
					>
						Aún no hay miembros visibles.
					</div>

					<div v-else class="members-list">
						<div
							v-for="member in groupDetails.data?.members"
							:key="member.user"
							class="member-row group/member"
						>
							<UserAvatar :user="member" class="member-avatar" />

							<div class="member-info">
								<p>{{ member.full_name || member.user }}</p>
								<span>{{ member.role }}</span>
							</div>

							<button
								v-if="isAdmin && member.user !== currentUser"
								class="remove-button opacity-0 group-hover/member:opacity-100"
								title="Eliminar miembro"
								@click="removeMember(member.user)"
							>
								<X class="size-4" />
							</button>
						</div>
					</div>
				</div>
			</aside>
		</div>

		<!-- Invite Modal -->
		<Dialog v-model="showInviteModal" :options="{ title: 'Invitar Miembro' }">
			<template #body-content>
				<div class="modal-form">
					<FormControl
						type="email"
						label="Correo Electrónico"
						v-model="inviteEmail"
						placeholder="usuario@ejemplo.com"
					/>

					<div class="select-field">
						<label>Rol</label>
						<select v-model="inviteRole">
							<option value="Member">Miembro</option>
							<option value="Admin">Administrador</option>
						</select>
					</div>
				</div>
			</template>

			<template #actions>
				<Button
					variant="solid"
					class="primary-button w-full"
					:loading="inviting"
					@click="sendInvite"
					:disabled="!inviteEmail"
				>
					Enviar invitación
				</Button>
			</template>
		</Dialog>

		<!-- Edit Group Modal -->
		<Dialog v-model="showEditModal" :options="{ title: 'Editar Grupo' }">
			<template #body-content>
				<div class="modal-form">
					<FormControl
						type="text"
						label="Nombre del Grupo"
						v-model="editGroup.title"
					/>

					<FormControl
						type="textarea"
						label="Descripción"
						v-model="editGroup.description"
						rows="3"
					/>
				</div>
			</template>

			<template #actions>
				<div class="modal-actions">
					<Button
						variant="outline"
						class="danger-button"
						:loading="deleting"
						@click="deleteGroup"
					>
						Eliminar
					</Button>

					<Button
						variant="solid"
						class="primary-button flex-1"
						:loading="saving"
						@click="saveGroup"
						:disabled="!editGroup.title"
					>
						Guardar cambios
					</Button>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { Button, FormControl, Dialog, createResource, Spinner, toast, call, FileUploader } from 'frappe-ui'
import { ArrowLeft, Send, UserPlus, X, Settings, Paperclip, FileText } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { sessionStore } from '@/stores/session'
import UserAvatar from '@/components/UserAvatar.vue'
import dayjs from '@/utils/dayjs'

const props = defineProps({
	groupName: {
		type: String,
		required: true
	}
})

const router = useRouter()
const { user } = sessionStore()
const currentUser = computed(() => user)

const messagesContainer = ref(null)
const newMessage = ref('')
const attachmentPreview = ref(null)
const attachmentName = ref('')
const sending = ref(false)
const showInviteModal = ref(false)
const inviteEmail = ref('')
const inviteRole = ref('Member')
const inviting = ref(false)

const showEditModal = ref(false)
const editGroup = ref({ title: '', description: '' })
const saving = ref(false)
const deleting = ref(false)

const groupDetails = createResource({
	url: 'lms.lms.groups.get_group_details',
	params: { group: props.groupName },
	auto: true,
	onSuccess(data) {
		data.member_count = data.members?.length || 0
	}
})

const messages = createResource({
	url: 'lms.lms.groups.get_messages',
	params: { group: props.groupName, limit_start: 0, limit_page_length: 50 },
	auto: true,
	onSuccess() {
		scrollToBottom()
	}
})

const isAdmin = computed(() => {
	const member = groupDetails.data?.members?.find(m => m.user === currentUser.value)
	return member?.role === 'Admin'
})

const formatTime = (timeStr) => {
	if (!timeStr) return ''
	return dayjs(timeStr).format('HH:mm')
}

const scrollToBottom = async () => {
	await nextTick()
	if (messagesContainer.value) {
		messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
	}
}

const handleFileUploadSuccess = async (file) => {
	attachmentPreview.value = file.file_url
	attachmentName.value = file.file_name
}

const sendMessage = async () => {
	if ((!newMessage.value.trim() && !attachmentPreview.value) || sending.value) return

	try {
		sending.value = true
		const content = newMessage.value
		const attachmentUrl = attachmentPreview.value
		
		newMessage.value = ''
		attachmentPreview.value = null
		attachmentName.value = ''

		const res = await call('lms.lms.groups.send_message', {
			group: props.groupName,
			content: content,
			attachment: attachmentUrl
		})

		if (res) {
			if (!messages.data) messages.data = []
			messages.data.push(res)
			scrollToBottom()
		}
	} catch (e) {
		toast.error('Error al enviar mensaje')
	} finally {
		sending.value = false
	}
}

const isImage = (url) => {
	if (!url) return false
	return url.match(/\.(jpeg|jpg|gif|png|webp|svg)$/i) != null
}

const openAttachment = (url) => {
	window.open(url, '_blank')
}

const validateFile = (file) => {
	if (file.size > 2 * 1024 * 1024) { // 2MB
		toast.error('El archivo no puede pesar más de 2MB')
		return 'El archivo no puede pesar más de 2MB'
	}
	return null
}

const sendInvite = async () => {
	try {
		inviting.value = true
		await call('lms.lms.groups.invite_user', {
			group: props.groupName,
			email: inviteEmail.value,
			role: inviteRole.value
		})

		toast.success('Invitación enviada')
		showInviteModal.value = false
		inviteEmail.value = ''
	} catch (e) {
		console.error(e)
		toast.error('Error al invitar (Asegúrate de que el usuario exista)')
	} finally {
		inviting.value = false
	}
}

const removeMember = async (email) => {
	if (!confirm('¿Estás seguro de eliminar a este miembro del grupo?')) return

	try {
		await call('lms.lms.groups.remove_member', {
			group: props.groupName,
			email: email
		})
		toast.success('Miembro eliminado')
		groupDetails.reload()
	} catch (e) {
		toast.error('Error al eliminar miembro')
	}
}

const openEditModal = () => {
	editGroup.value = {
		title: groupDetails.data?.title || '',
		description: groupDetails.data?.description || ''
	}
	showEditModal.value = true
}

const saveGroup = async () => {
	try {
		saving.value = true
		const res = await call('lms.lms.groups.update_group', {
			group: props.groupName,
			title: editGroup.value.title,
			description: editGroup.value.description
		})
		toast.success('Grupo actualizado')
		showEditModal.value = false
		if (res !== props.groupName) {
			router.push({ name: 'GroupDetail', params: { groupName: res } })
		} else {
			groupDetails.reload()
		}
	} catch (e) {
		toast.error('Error al actualizar grupo')
	} finally {
		saving.value = false
	}
}

const deleteGroup = async () => {
	if (!confirm('¿Estás seguro de eliminar este grupo? Esta acción borrará todos los mensajes y no se puede deshacer.')) return
	try {
		deleting.value = true
		await call('lms.lms.groups.delete_group', { group: props.groupName })
		toast.success('Grupo eliminado')
		router.push({ name: 'Groups' })
	} catch (e) {
		toast.error('Error al eliminar grupo')
	} finally {
		deleting.value = false
	}
}

// Polling for new messages (Simple MVP approach)
let pollInterval

onMounted(() => {
	pollInterval = setInterval(() => {
		messages.reload()
	}, 5000)
})

onUnmounted(() => {
	clearInterval(pollInterval)
})
</script>

<style scoped>
.group-detail-page {
	color: #0d1e3e;
}

.detail-header {
	display: flex;
	align-items: center;
	gap: 16px;
	background: #ffffff;
	border: 1px solid #dbe4f0;
	border-radius: 28px;
	padding: 18px;
	box-shadow: 0 18px 45px rgba(13, 30, 62, 0.07);
}

.header-copy {
	flex: 1;
	min-width: 0;
}

.eyebrow,
.chat-kicker,
.side-kicker {
	margin-bottom: 4px;
	font-size: 12px;
	font-weight: 800;
	letter-spacing: 0.08em;
	text-transform: uppercase;
	color: #64748b;
}

.detail-header h1 {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	font-size: 28px;
	font-weight: 900;
	line-height: 1.1;
	letter-spacing: -0.04em;
	color: #0d1e3e;
}

.detail-header p:not(.eyebrow) {
	margin-top: 5px;
	font-size: 14px;
	color: #64748b;
}

.detail-layout {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 340px;
	gap: 22px;
	height: calc(100vh - 132px);
	margin-top: 22px;
	padding-bottom: 4px;
}

.chat-shell {
	display: flex;
	min-height: 0;
	flex-direction: column;
	overflow: hidden;
	background: #ffffff;
	border: 1px solid #dbe4f0;
	border-radius: 30px;
	box-shadow: 0 18px 45px rgba(13, 30, 62, 0.07);
}

.chat-topbar {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	padding: 18px 20px;
	border-bottom: 1px solid #e5edf6;
	background: #ffffff;
}

.chat-topbar h2 {
	font-size: 18px;
	font-weight: 900;
	letter-spacing: -0.03em;
	color: #0d1e3e;
}

.live-pill {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	border-radius: 999px;
	border: 1px solid #dbe4f0;
	background: #f8fafc;
	padding: 8px 12px;
	font-size: 12px;
	font-weight: 800;
	color: #64748b;
}

.live-pill span {
	width: 8px;
	height: 8px;
	border-radius: 999px;
	background: #16a34a;
}

.messages-area {
	flex: 1;
	display: flex;
	flex-direction: column;
	gap: 14px;
	overflow-y: auto;
	padding: 22px;
	background: #f7f9fc;
}

.messages-loading,
.empty-chat {
	margin: auto;
	text-align: center;
	color: #64748b;
}

.messages-loading {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 12px;
}

.empty-chat {
	max-width: 420px;
}

.empty-chat-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 64px;
	height: 64px;
	margin-bottom: 14px;
	border-radius: 22px;
	border: 1px solid #dbe4f0;
	background: #ffffff;
	color: #0d1e3e;
	box-shadow: 0 12px 30px rgba(13, 30, 62, 0.06);
}

.empty-chat h3 {
	font-size: 20px;
	font-weight: 900;
	letter-spacing: -0.03em;
	color: #0d1e3e;
}

.empty-chat p {
	margin-top: 7px;
	font-size: 14px;
	line-height: 1.6;
	color: #64748b;
}

.message-row {
	display: flex;
	gap: 10px;
	max-width: min(760px, 86%);
}

.message-row.is-current {
	align-self: flex-end;
	flex-direction: row-reverse;
}

.message-row.is-other {
	align-self: flex-start;
}

.message-avatar {
	width: 34px;
	height: 34px;
	flex-shrink: 0;
	margin-top: 2px;
}

.message-bubble {
	padding: 13px 15px;
	border-radius: 22px;
	box-shadow: 0 10px 24px rgba(13, 30, 62, 0.06);
}

.current-bubble {
	border-top-right-radius: 8px;
	background: #0d1e3e;
	border: 1px solid #0d1e3e;
	color: #ffffff;
}

.other-bubble {
	border-top-left-radius: 8px;
	background: #ffffff;
	border: 1px solid #dbe4f0;
	color: #0d1e3e;
}

.message-author {
	margin-bottom: 5px;
	font-size: 12px;
	font-weight: 900;
	color: #0d1e3e;
}

.message-content {
	white-space: pre-wrap;
	word-break: break-word;
	font-size: 14.5px;
	line-height: 1.6;
}

.message-time {
	margin-top: 6px;
	text-align: right;
	font-size: 11px;
	font-weight: 700;
}

.current-time {
	color: rgba(255, 255, 255, 0.65);
}

.other-time {
	color: #94a3b8;
}

.composer {
	display: flex;
	align-items: flex-end;
	gap: 12px;
	padding: 14px;
	border-top: 1px solid #e5edf6;
	background: #ffffff;
}

.composer-input {
	flex: 1;
	border-radius: 20px;
	background: #f8fafc;
	border: 1px solid #dbe4f0;
	padding: 4px 14px;
}

.composer-input :deep(textarea) {
	min-height: 44px !important;
	border: 0 !important;
	background: transparent !important;
	box-shadow: none !important;
	resize: none !important;
	color: #0d1e3e !important;
	font-size: 15px !important;
	line-height: 1.5 !important;
}

.composer-input:focus-within {
	border-color: #0d1e3e;
	box-shadow: 0 0 0 3px rgba(13, 30, 62, 0.08);
}

.side-panel {
	display: flex;
	min-height: 0;
	flex-direction: column;
	gap: 16px;
}

.info-card {
	background: #ffffff;
	border: 1px solid #dbe4f0;
	border-radius: 26px;
	padding: 18px;
	box-shadow: 0 18px 45px rgba(13, 30, 62, 0.06);
}

.members-card {
	flex: 1;
	min-height: 0;
	overflow: hidden;
	display: flex;
	flex-direction: column;
}

.card-heading {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 14px;
	margin-bottom: 14px;
}

.card-heading h3 {
	font-size: 17px;
	font-weight: 900;
	letter-spacing: -0.03em;
	color: #0d1e3e;
}

.description-text {
	white-space: pre-wrap;
	font-size: 14px;
	line-height: 1.65;
	color: #64748b;
}

.count-pill {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-width: 34px;
	height: 34px;
	padding: 0 10px;
	border-radius: 999px;
	border: 1px solid #dbe4f0;
	background: #f8fafc;
	font-size: 12px;
	font-weight: 900;
	color: #0d1e3e;
}

.members-list {
	display: flex;
	flex-direction: column;
	gap: 10px;
	overflow-y: auto;
	padding-right: 3px;
}

.member-row {
	display: flex;
	align-items: center;
	gap: 11px;
	padding: 10px;
	border: 1px solid transparent;
	border-radius: 18px;
	transition: background 160ms ease, border-color 160ms ease;
}

.member-row:hover {
	background: #f8fafc;
	border-color: #e5edf6;
}

.member-avatar {
	width: 36px;
	height: 36px;
	flex-shrink: 0;
}

.member-info {
	min-width: 0;
	flex: 1;
}

.member-info p {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	font-size: 14px;
	font-weight: 850;
	color: #0d1e3e;
}

.member-info span {
	font-size: 12px;
	font-weight: 700;
	color: #64748b;
}

.empty-members {
	border: 1px dashed #cbd5e1;
	border-radius: 18px;
	background: #f8fafc;
	padding: 18px;
	font-size: 14px;
	text-align: center;
	color: #64748b;
}

.back-button,
.icon-button,
.remove-button {
	display: inline-flex !important;
	align-items: center !important;
	justify-content: center !important;
	border-radius: 16px !important;
	border: 1px solid #dbe4f0 !important;
	background: #ffffff !important;
	color: #0d1e3e !important;
	transition: background 160ms ease, border-color 160ms ease, color 160ms ease;
}

.back-button {
	width: 44px;
	height: 44px;
	flex-shrink: 0;
}

.icon-button,
.remove-button {
	width: 34px;
	height: 34px;
}

.back-button:hover,
.icon-button:hover {
	background: #f8fafc !important;
	border-color: #b8c7dc !important;
}

.remove-button {
	color: #b42318 !important;
	border-color: #f3c7c3 !important;
}

.remove-button:hover {
	background: #fff5f5 !important;
}

.primary-button,
.send-button {
	border-radius: 16px !important;
	background: #0d1e3e !important;
	border: 1px solid #0d1e3e !important;
	color: #ffffff !important;
	font-weight: 850 !important;
	box-shadow: 0 10px 24px rgba(13, 30, 62, 0.16);
}

.primary-button:hover,
.send-button:hover {
	background: #142b57 !important;
	border-color: #142b57 !important;
}

.send-button {
	width: 48px !important;
	height: 48px !important;
	padding: 0 !important;
	flex-shrink: 0;
	border-radius: 18px !important;
}

.send-button:disabled {
	opacity: 0.45;
	box-shadow: none;
}

.modal-form {
	display: flex;
	flex-direction: column;
	gap: 16px;
}

.modal-form :deep(input),
.modal-form :deep(textarea),
.select-field select {
	width: 100%;
	border-radius: 16px !important;
	border: 1px solid #dbe4f0 !important;
	background: #f8fafc !important;
	color: #0d1e3e !important;
}

.modal-form :deep(input:focus),
.modal-form :deep(textarea:focus),
.select-field select:focus {
	outline: none !important;
	border-color: #0d1e3e !important;
	box-shadow: 0 0 0 3px rgba(13, 30, 62, 0.08) !important;
}

.select-field {
	display: flex;
	flex-direction: column;
	gap: 6px;
}

.select-field label {
	font-size: 12px;
	font-weight: 800;
	color: #64748b;
}

.select-field select {
	height: 42px;
	padding: 0 12px;
	font-size: 14px;
}

.modal-actions {
	display: flex;
	gap: 10px;
	width: 100%;
}

.danger-button {
	flex: 1;
	border-radius: 16px !important;
	background: #ffffff !important;
	color: #b42318 !important;
	border: 1px solid #f3c7c3 !important;
	font-weight: 850 !important;
}

.danger-button:hover {
	background: #fff5f5 !important;
}

@media (max-width: 1024px) {
	.detail-layout {
		grid-template-columns: 1fr;
		height: auto;
		min-height: calc(100vh - 132px);
	}

	.chat-shell {
		min-height: calc(100vh - 160px);
	}

	.side-panel {
		display: none;
	}
}

@media (max-width: 720px) {
	.detail-header {
		align-items: flex-start;
		border-radius: 24px;
		padding: 16px;
	}

	.detail-header h1 {
		font-size: 22px;
	}

	.detail-header p:not(.eyebrow) {
		font-size: 13px;
	}

	.primary-button {
		padding-inline: 12px !important;
	}

	.chat-topbar {
		padding: 16px;
	}

	.messages-area {
		padding: 16px;
	}

	.message-row {
		max-width: 94%;
	}

	.composer {
		padding: 12px;
	}

	.modal-actions {
		flex-direction: column;
	}
}
</style>
<template>
	<div class="group-detail-page px-6 py-4">
		<header>
			<div class="flex items-center gap-4 pb-4">
				<Button variant="ghost" @click="router.push({ name: 'Groups' })">
					<template #icon><ArrowLeft class="size-4" /></template>
				</Button>
				<div class="flex-1">
					<h1 class="text-2xl font-bold text-ink-gray-9">{{ groupDetails.data?.title || 'Cargando...' }}</h1>
					<p class="text-sm text-ink-gray-5">{{ groupDetails.data?.member_count || 0 }} miembros • {{ groupDetails.data?.type === 'Course' ? 'Grupo de Curso' : 'Grupo Privado' }}</p>
				</div>
				<Button
					v-if="isAdmin"
					variant="solid"
					@click="showInviteModal = true"
				>
					<template #icon><UserPlus class="size-4" /></template>
					Invitar Miembros
				</Button>
			</div>
		</header>

		<div class="flex h-[calc(100vh-140px)] gap-6 mt-4 pb-4">
			<!-- Chat Area -->
			<div class="flex-1 flex flex-col bg-surface-white border border-outline-gray-2 rounded-xl shadow-sm overflow-hidden">
				
				<!-- Messages Container -->
				<div class="flex-1 overflow-y-auto p-4 flex flex-col gap-4 bg-surface-gray-1" ref="messagesContainer">
					<div v-if="messages.loading" class="flex justify-center p-4">
						<Spinner class="size-6 text-ink-gray-4" />
					</div>
					
					<div
						v-for="msg in messages.data"
						:key="msg.name"
						class="flex gap-3 max-w-[85%]"
						:class="msg.user === currentUser ? 'self-end flex-row-reverse' : 'self-start'"
					>
						<UserAvatar :user="msg" class="size-8 shrink-0 mt-1" />
						<div :class="msg.user === currentUser ? 'bg-blue-600 text-white rounded-l-2xl rounded-tr-2xl' : 'bg-white border border-outline-gray-2 text-ink-gray-9 rounded-r-2xl rounded-tl-2xl'" class="p-3 shadow-sm">
							<p v-if="msg.user !== currentUser" class="text-xs font-semibold mb-1" :class="msg.user === currentUser ? 'text-blue-100' : 'text-blue-600'">
								{{ msg.full_name || msg.user }}
							</p>
							<p class="whitespace-pre-wrap break-words text-sm">{{ msg.content }}</p>
							<p class="text-[10px] mt-1 text-right" :class="msg.user === currentUser ? 'text-blue-200' : 'text-ink-gray-4'">
								{{ formatTime(msg.creation) }}
							</p>
						</div>
					</div>
				</div>

				<!-- Message Input -->
				<div class="p-3 border-t border-outline-gray-2 bg-white flex gap-2 items-end">
					<FormControl
						v-model="newMessage"
						placeholder="Escribe un mensaje..."
						type="textarea"
						class="flex-1"
						:rows="1"
						autoresize
						@keydown.enter.prevent="sendMessage"
					/>
					<Button
						variant="solid"
						class="mb-1"
						:disabled="!newMessage.trim()"
						:loading="sending"
						@click="sendMessage"
					>
						<Send class="size-4" />
					</Button>
				</div>
			</div>

			<!-- Sidebar Info -->
			<div class="w-80 hidden lg:flex flex-col gap-4">
				<div class="bg-surface-white border border-outline-gray-2 rounded-xl p-4 shadow-sm">
					<h3 class="font-semibold text-ink-gray-9 mb-2">Acerca del Grupo</h3>
					<p class="text-sm text-ink-gray-6">{{ groupDetails.data?.description || 'Sin descripción.' }}</p>
				</div>

				<div class="bg-surface-white border border-outline-gray-2 rounded-xl p-4 shadow-sm flex-1 overflow-y-auto">
					<h3 class="font-semibold text-ink-gray-9 mb-3 flex items-center justify-between">
						Miembros ({{ groupDetails.data?.members?.length || 0 }})
					</h3>
					<div class="flex flex-col gap-3">
						<div v-for="member in groupDetails.data?.members" :key="member.user" class="flex items-center gap-2">
							<UserAvatar :user="member" class="size-8" />
							<div class="flex-1 min-w-0">
								<p class="text-sm font-medium text-ink-gray-9 truncate">{{ member.full_name || member.user }}</p>
								<p class="text-xs text-ink-gray-5">{{ member.role }}</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Invite Modal -->
		<Dialog v-model="showInviteModal" :options="{ title: 'Invitar Miembro' }">
			<template #body-content>
				<div class="space-y-4">
					<FormControl
						type="email"
						label="Correo Electrónico"
						v-model="inviteEmail"
						placeholder="usuario@ejemplo.com"
					/>
					<div class="flex flex-col gap-1">
						<label class="text-xs text-ink-gray-5">Rol</label>
						<select v-model="inviteRole" class="form-input text-sm rounded-md border-outline-gray-2">
							<option value="Member">Miembro</option>
							<option value="Admin">Administrador</option>
						</select>
					</div>
				</div>
			</template>
			<template #actions>
				<Button
					variant="solid"
					class="w-full"
					:loading="inviting"
					@click="sendInvite"
					:disabled="!inviteEmail"
				>
					Enviar Invitación
				</Button>
			</template>
		</Dialog>

	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { Button, FormControl, Dialog, createResource, Spinner, toast } from 'frappe-ui'
import { ArrowLeft, Send, UserPlus } from 'lucide-vue-next'
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
const sending = ref(false)
const showInviteModal = ref(false)
const inviteEmail = ref('')
const inviteRole = ref('Member')
const inviting = ref(false)

const groupDetails = createResource({
	url: 'lms.lms.groups.get_group_details',
	params: { group: props.groupName },
	auto: true,
	onSuccess(data) {
		data.member_count = data.members?.length || 0;
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

const sendMessage = async () => {
	if (!newMessage.value.trim() || sending.value) return
	
	try {
		sending.value = true
		const content = newMessage.value
		newMessage.value = ''
		
		const res = await fetch('/api/method/lms.lms.groups.send_message', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				group: props.groupName,
				content: content
			})
		}).then(r => r.json())
		
		if (res.message) {
			if (!messages.data) messages.data = []
			messages.data.push(res.message)
			scrollToBottom()
		}
	} catch (e) {
		toast.error('Error al enviar mensaje')
	} finally {
		sending.value = false
	}
}

const sendInvite = async () => {
	try {
		inviting.value = true
		await fetch('/api/method/lms.lms.groups.invite_user', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				group: props.groupName,
				email: inviteEmail.value,
				role: inviteRole.value
			})
		}).then(async r => {
			const data = await r.json()
			if(data.exc) throw new Error(data._server_messages)
			return data
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

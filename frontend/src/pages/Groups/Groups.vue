<template>
	<Layout>
		<template #header>
			<div class="flex items-center justify-between py-4">
				<h1 class="text-3xl font-bold text-ink-gray-9">Mis Grupos</h1>
				<Button
					variant="solid"
					@click="showCreateModal = true"
				>
					<template #icon><Plus class="size-4" /></template>
					Crear Grupo Privado
				</Button>
			</div>
		</template>

		<div class="mt-6 flex flex-col gap-8">
			<!-- Pending Invitations -->
			<section v-if="invitations.data && invitations.data.length > 0">
				<h2 class="text-xl font-semibold text-ink-gray-8 mb-4">Invitaciones Pendientes</h2>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
					<div
						v-for="inv in invitations.data"
						:key="inv.name"
						class="bg-surface-white border border-outline-gray-2 rounded-xl p-5 shadow-sm"
					>
						<h3 class="text-lg font-medium text-ink-gray-9">{{ inv.title }}</h3>
						<p class="text-ink-gray-5 text-sm mt-1 mb-4">{{ inv.description }}</p>
						<div class="flex gap-2">
							<Button variant="solid" @click="respondInv(inv.group, 'Accepted')" class="flex-1 bg-green-600 hover:bg-green-700">Aceptar</Button>
							<Button variant="outline" @click="respondInv(inv.group, 'Rejected')" class="flex-1 text-red-600 border-red-200 hover:bg-red-50">Rechazar</Button>
						</div>
					</div>
				</div>
			</section>

			<!-- Active Groups -->
			<section>
				<h2 class="text-xl font-semibold text-ink-gray-8 mb-4">Tus Grupos</h2>
				<div v-if="groups.loading" class="flex justify-center p-8">
					<Spinner class="size-8 text-ink-gray-4" />
				</div>
				<div v-else-if="!groups.data || groups.data.length === 0" class="text-center p-12 bg-surface-gray-2 rounded-xl">
					<MessageCircle class="size-12 text-ink-gray-4 mx-auto mb-3" />
					<h3 class="text-lg font-medium text-ink-gray-8">Aún no estás en ningún grupo</h3>
					<p class="text-ink-gray-5 mt-1">Crea un grupo privado o únete a un curso para empezar a conversar.</p>
				</div>
				<div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
					<router-link
						v-for="group in groups.data"
						:key="group.name"
						:to="{ name: 'GroupDetail', params: { groupName: group.name } }"
						class="group bg-surface-white border border-outline-gray-2 hover:border-blue-300 rounded-xl p-5 shadow-sm transition-all hover:shadow-md block relative overflow-hidden"
					>
						<div class="absolute top-0 left-0 w-1 h-full" :class="group.type === 'Course' ? 'bg-blue-500' : 'bg-purple-500'"></div>
						<div class="flex justify-between items-start mb-2 pl-2">
							<h3 class="text-lg font-bold text-ink-gray-9 group-hover:text-blue-600 transition-colors">{{ group.title }}</h3>
							<Badge :theme="group.type === 'Course' ? 'blue' : 'purple'">{{ group.type === 'Course' ? 'Curso' : 'Privado' }}</Badge>
						</div>
						<p class="text-ink-gray-5 text-sm line-clamp-2 pl-2">{{ group.description }}</p>
						<div class="mt-4 pt-4 border-t border-outline-gray-2 flex items-center justify-between text-sm pl-2">
							<span class="text-ink-gray-5 flex items-center gap-1"><Users class="size-4"/> {{ group.member_count }} miembros</span>
							<span class="text-ink-gray-4">{{ group.role }}</span>
						</div>
					</router-link>
				</div>
			</section>
		</div>

		<!-- Create Group Modal -->
		<Dialog v-model="showCreateModal" :options="{ title: 'Crear Grupo Privado' }">
			<template #body-content>
				<div class="space-y-4">
					<Input
						type="text"
						label="Nombre del Grupo"
						v-model="newGroup.title"
						placeholder="Ej. Grupo de Estudio Python"
					/>
					<Textarea
						label="Descripción"
						v-model="newGroup.description"
						placeholder="¿De qué trata este grupo?"
						rows="3"
					/>
				</div>
			</template>
			<template #actions>
				<Button
					variant="solid"
					class="w-full"
					:loading="creating"
					@click="createGroup"
					:disabled="!newGroup.title"
				>
					Crear Grupo
				</Button>
			</template>
		</Dialog>

	</Layout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Layout from '@/components/Layouts/MainLayout.vue'
import { Button, Input, Textarea, Dialog, Badge, createResource, Spinner, toast } from 'frappe-ui'
import { Plus, Users, MessageCircle } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

const showCreateModal = ref(false)
const creating = ref(false)
const newGroup = reactive({
	title: '',
	description: ''
})

const groups = createResource({
	url: 'studybadge.lms.lms.groups.get_groups',
	auto: true
})

const invitations = createResource({
	url: 'studybadge.lms.lms.groups.get_pending_invitations',
	auto: true
})

const respondInv = async (groupName, response) => {
	try {
		await fetch('/api/method/studybadge.lms.lms.groups.respond_invitation', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ group: groupName, response })
		}).then(r => r.json())
		toast.success(response === 'Accepted' ? 'Te has unido al grupo' : 'Invitación rechazada')
		invitations.reload()
		groups.reload()
	} catch (e) {
		toast.error('Ocurrió un error')
	}
}

const createGroup = async () => {
	try {
		creating.value = true
		const res = await fetch('/api/method/studybadge.lms.lms.groups.create_group', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				title: newGroup.title,
				description: newGroup.description,
				type: 'Private'
			})
		}).then(r => r.json())
		
		toast.success('Grupo creado exitosamente')
		showCreateModal.value = false
		groups.reload()
		newGroup.title = ''
		newGroup.description = ''
		
		if (res.message) {
			router.push({ name: 'GroupDetail', params: { groupName: res.message } })
		}
	} catch (e) {
		toast.error('Error al crear grupo')
	} finally {
		creating.value = false
	}
}
</script>

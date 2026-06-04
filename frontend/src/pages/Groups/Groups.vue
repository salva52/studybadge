<template>
	<div class="groups-page min-h-screen bg-[#f7f9fc] px-4 py-5 md:px-6">
		<header class="groups-header">
			<div>
				<p class="eyebrow">StudyBadge Groups</p>
				<h1>Mis grupos</h1>
				<p class="header-subtitle">
					Organiza tus grupos de estudio, clases y conversaciones con alumnos.
				</p>
			</div>

			<Button
				variant="solid"
				class="primary-button"
				@click="showCreateModal = true"
			>
				<template #icon><Plus class="size-4" /></template>
				Crear grupo
			</Button>
		</header>

		<main class="groups-content">
			<!-- Pending Invitations -->
			<section v-if="invitations.data && invitations.data.length > 0" class="section-card">
				<div class="section-heading">
					<div>
						<p class="section-kicker">Pendiente</p>
						<h2>Invitaciones</h2>
					</div>
					<span class="count-pill">{{ invitations.data.length }}</span>
				</div>

				<div class="invitation-grid">
					<div
						v-for="inv in invitations.data"
						:key="inv.name"
						class="invitation-card"
					>
						<div class="card-icon">
							<MessageCircle class="size-5" />
						</div>

						<h3>{{ inv.title }}</h3>
						<p>{{ inv.description || 'Te invitaron a unirte a este grupo de estudio.' }}</p>

						<div class="invitation-actions">
							<Button
								variant="solid"
								class="accept-button"
								@click="respondInv(inv.group, 'Accepted')"
							>
								Aceptar
							</Button>
							<Button
								variant="outline"
								class="reject-button"
								@click="respondInv(inv.group, 'Rejected')"
							>
								Rechazar
							</Button>
						</div>
					</div>
				</div>
			</section>

			<!-- Active Groups -->
			<section class="section-card">
				<div class="section-heading">
					<div>
						<p class="section-kicker">Tus espacios</p>
						<h2>Grupos activos</h2>
					</div>
				</div>

				<div v-if="groups.loading" class="loading-state">
					<Spinner class="size-8 text-[#0d1e3e]" />
					<p>Cargando tus grupos...</p>
				</div>

				<div v-else-if="!groups.data || groups.data.length === 0" class="empty-state">
					<div class="empty-icon">
						<MessageCircle class="size-8" />
					</div>
					<h3>Aún no estás en ningún grupo</h3>
					<p>
						Crea un grupo privado o únete a un curso para empezar a conversar y estudiar en comunidad.
					</p>
					<Button
						variant="solid"
						class="primary-button mt-5"
						@click="showCreateModal = true"
					>
						<template #icon><Plus class="size-4" /></template>
						Crear mi primer grupo
					</Button>
				</div>

				<div v-else class="groups-grid">
					<router-link
						v-for="group in groups.data"
						:key="group.name"
						:to="{ name: 'GroupDetail', params: { groupName: group.name } }"
						class="group-card"
					>
						<div class="group-card-top">
							<div class="group-icon">
								<MessageCircle class="size-5" />
							</div>

							<span class="type-pill">
								{{ group.type === 'Course' ? 'Curso' : 'Privado' }}
							</span>
						</div>

						<div class="group-card-body">
							<h3>{{ group.title }}</h3>
							<p>{{ group.description || 'Grupo de estudio en StudyBadge.' }}</p>
						</div>

						<div class="group-card-footer">
							<span>
								<Users class="size-4" />
								{{ group.member_count }} miembros
							</span>
							<span class="role-pill">{{ group.role }}</span>
						</div>
					</router-link>
				</div>
			</section>

			<!-- Create Group Modal -->
			<Dialog v-model="showCreateModal" :options="{ title: 'Crear Grupo Privado' }">
				<template #body-content>
					<div class="modal-form">
						<FormControl
							type="text"
							label="Nombre del Grupo"
							v-model="newGroup.title"
							placeholder="Ej. Grupo de estudio de Economía"
						/>
						<FormControl
							type="textarea"
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
						class="primary-button w-full"
						:loading="creating"
						@click="createGroup"
						:disabled="!newGroup.title"
					>
						Crear grupo
					</Button>
				</template>
			</Dialog>
		</main>
	</div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Button, FormControl, Dialog, createResource, Spinner, toast, call } from 'frappe-ui'
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
	url: 'lms.lms.groups.get_groups',
	auto: true
})

const invitations = createResource({
	url: 'lms.lms.groups.get_pending_invitations',
	auto: true
})

const respondInv = async (groupName, response) => {
	try {
		await call('lms.lms.groups.respond_invitation', { group: groupName, response })
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
		const res = await call('lms.lms.groups.create_group', {
			title: newGroup.title,
			description: newGroup.description,
			group_type: 'Private'
		})

		toast.success('Grupo creado exitosamente')
		showCreateModal.value = false
		groups.reload()
		newGroup.title = ''
		newGroup.description = ''

		if (res) {
			router.push({ name: 'GroupDetail', params: { groupName: res } })
		}
	} catch (e) {
		toast.error('Error al crear grupo')
	} finally {
		creating.value = false
	}
}
</script>

<style scoped>
.groups-page {
	color: #0d1e3e;
}

.groups-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 24px;
	background: #ffffff;
	border: 1px solid #dbe4f0;
	border-radius: 28px;
	padding: 24px;
	box-shadow: 0 18px 45px rgba(13, 30, 62, 0.07);
}

.eyebrow {
	margin-bottom: 6px;
	font-size: 12px;
	font-weight: 800;
	letter-spacing: 0.08em;
	text-transform: uppercase;
	color: #64748b;
}

.groups-header h1 {
	font-size: 34px;
	line-height: 1.05;
	font-weight: 900;
	letter-spacing: -0.04em;
	color: #0d1e3e;
}

.header-subtitle {
	margin-top: 8px;
	max-width: 580px;
	font-size: 15px;
	line-height: 1.6;
	color: #64748b;
}

.groups-content {
	display: flex;
	flex-direction: column;
	gap: 22px;
	margin-top: 22px;
}

.section-card {
	background: #ffffff;
	border: 1px solid #dbe4f0;
	border-radius: 28px;
	padding: 24px;
	box-shadow: 0 18px 45px rgba(13, 30, 62, 0.06);
}

.section-heading {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	margin-bottom: 20px;
}

.section-kicker {
	margin-bottom: 4px;
	font-size: 12px;
	font-weight: 800;
	letter-spacing: 0.08em;
	text-transform: uppercase;
	color: #64748b;
}

.section-heading h2 {
	font-size: 22px;
	font-weight: 900;
	letter-spacing: -0.03em;
	color: #0d1e3e;
}

.count-pill,
.type-pill,
.role-pill {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border-radius: 999px;
	border: 1px solid #dbe4f0;
	background: #f7f9fc;
	color: #0d1e3e;
	font-size: 12px;
	font-weight: 800;
}

.count-pill {
	width: 34px;
	height: 34px;
}

.type-pill {
	padding: 7px 11px;
}

.role-pill {
	padding: 6px 10px;
	color: #64748b;
}

.invitation-grid,
.groups-grid {
	display: grid;
	grid-template-columns: repeat(1, minmax(0, 1fr));
	gap: 16px;
}

@media (min-width: 768px) {
	.invitation-grid,
	.groups-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (min-width: 1200px) {
	.invitation-grid,
	.groups-grid {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}
}

.invitation-card,
.group-card {
	position: relative;
	display: block;
	border: 1px solid #dbe4f0;
	border-radius: 24px;
	background: #ffffff;
	padding: 20px;
	text-decoration: none;
	box-shadow: 0 12px 30px rgba(13, 30, 62, 0.05);
	transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.invitation-card:hover,
.group-card:hover {
	transform: translateY(-3px);
	border-color: #b8c7dc;
	box-shadow: 0 22px 45px rgba(13, 30, 62, 0.09);
}

.card-icon,
.group-icon,
.empty-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	background: #f1f5f9;
	color: #0d1e3e;
	border: 1px solid #dbe4f0;
}

.card-icon,
.group-icon {
	width: 44px;
	height: 44px;
	border-radius: 16px;
}

.empty-icon {
	width: 64px;
	height: 64px;
	border-radius: 22px;
	margin: 0 auto 16px;
}

.invitation-card h3,
.group-card h3 {
	margin-top: 16px;
	font-size: 18px;
	font-weight: 900;
	letter-spacing: -0.03em;
	color: #0d1e3e;
}

.invitation-card p,
.group-card p {
	margin-top: 7px;
	font-size: 14px;
	line-height: 1.6;
	color: #64748b;
}

.invitation-actions {
	display: flex;
	gap: 10px;
	margin-top: 18px;
}

.group-card-top {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 14px;
}

.group-card-body {
	min-height: 104px;
}

.group-card-body p {
	display: -webkit-box;
	overflow: hidden;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
}

.group-card-footer {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 12px;
	margin-top: 18px;
	padding-top: 16px;
	border-top: 1px solid #e5edf6;
	font-size: 13px;
	color: #64748b;
}

.group-card-footer span {
	display: inline-flex;
	align-items: center;
	gap: 6px;
}

.loading-state,
.empty-state {
	border: 1px dashed #cbd5e1;
	border-radius: 24px;
	background: #f8fafc;
	padding: 42px 24px;
	text-align: center;
}

.loading-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 12px;
	color: #64748b;
}

.empty-state h3 {
	font-size: 20px;
	font-weight: 900;
	letter-spacing: -0.03em;
	color: #0d1e3e;
}

.empty-state p {
	max-width: 520px;
	margin: 8px auto 0;
	font-size: 15px;
	line-height: 1.6;
	color: #64748b;
}

.primary-button,
.accept-button {
	border-radius: 16px !important;
	background: #0d1e3e !important;
	color: #ffffff !important;
	border: 1px solid #0d1e3e !important;
	font-weight: 800 !important;
	box-shadow: 0 10px 24px rgba(13, 30, 62, 0.16);
}

.primary-button:hover,
.accept-button:hover {
	background: #142b57 !important;
	border-color: #142b57 !important;
}

.reject-button {
	border-radius: 16px !important;
	background: #ffffff !important;
	color: #b42318 !important;
	border: 1px solid #f3c7c3 !important;
	font-weight: 800 !important;
}

.reject-button:hover {
	background: #fff5f5 !important;
}

.modal-form {
	display: flex;
	flex-direction: column;
	gap: 16px;
}

.modal-form :deep(input),
.modal-form :deep(textarea) {
	border-radius: 16px !important;
	border-color: #dbe4f0 !important;
	background: #f8fafc !important;
	color: #0d1e3e !important;
}

.modal-form :deep(input:focus),
.modal-form :deep(textarea:focus) {
	border-color: #0d1e3e !important;
	box-shadow: 0 0 0 3px rgba(13, 30, 62, 0.08) !important;
}

@media (max-width: 720px) {
	.groups-header {
		flex-direction: column;
		align-items: stretch;
		border-radius: 24px;
		padding: 20px;
	}

	.groups-header h1 {
		font-size: 30px;
	}

	.section-card {
		padding: 18px;
		border-radius: 24px;
	}

	.invitation-actions {
		flex-direction: column;
	}
}
</style>
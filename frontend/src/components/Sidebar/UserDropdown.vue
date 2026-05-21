<template>
	<div class="p-2">
		<Dropdown :options="userDropdownOptions">
			<template v-slot="{ open, close }">
				<button
					class="flex h-12 py-2 items-center rounded-md duration-300 ease-in-out"
					:class="
						isCollapsed
							? 'px-0 w-auto'
							: open
							? 'bg-white/15 shadow-sm px-2 w-52'
							: 'hover:bg-white/10 px-2 w-52'
					"
				>
					<img
						v-if="branding.data?.banner_image"
						:src="branding.data?.banner_image.file_url"
						class="w-9 h-9 rounded-lg flex-shrink-0 object-contain"
					/>
					<img v-else :src="'/assets/lms/images/studybadge/studybadge-logo.png'" class="w-9 h-9 rounded-lg flex-shrink-0 object-contain" alt="StudyBadge" />
					<div
						class="flex flex-1 flex-col text-start duration-300 ease-in-out"
						:class="
							isCollapsed
								? 'opacity-0 ms-0 w-0 overflow-hidden'
								: 'opacity-100 ms-2 w-auto'
						"
					>
						<div class="text-base font-medium text-white leading-none">
							<span
								v-if="
									branding.data?.app_name && branding.data?.app_name != 'Frappe'
								"
							>
								{{ branding.data?.app_name }}
							</span>
							<span v-else> StudyBadge </span>
						</div>
						<div
							v-if="userResource.data"
							class="mt-1 text-sm text-blue-200/70 leading-none"
						>
							{{ convertToTitleCase(userResource.data?.full_name) }}
						</div>
					</div>
					<div
						class="duration-300 ease-in-out"
						:class="
							isCollapsed
								? 'opacity-0 ms-0 w-0 overflow-hidden'
								: 'opacity-100 ms-2 w-auto'
						"
					>
						<ChevronDown class="h-4 w-4 text-blue-200/70" />
					</div>
				</button>
			</template>
		</Dropdown>
	</div>
	<SettingsModal
		v-if="userResource.data?.is_moderator"
		v-model="showSettingsModal"
	/>
</template>

<script setup>
import { sessionStore } from '@/stores/session'
import { call, Dropdown, toast } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { convertToTitleCase } from '@/utils'
import { applyTheme, toggleTheme, theme } from '@/utils/theme'
import { usersStore } from '@/stores/user'
import { useSettings } from '@/stores/settings'
import { markRaw, watch, ref, onMounted, computed } from 'vue'
import { createDialog } from '@/utils/dialogs'
import Apps from '@/components/Sidebar/Apps.vue'
import Configuration from '@/components/Sidebar/Configuration.vue'
import FrappeCloudIcon from '@/components/Icons/FrappeCloudIcon.vue'
import LMSLogo from '@/components/Icons/LMSLogo.vue'
import SettingsModal from '@/components/Settings/Settings.vue'
import {
	ChevronDown,
	LogIn,
	LogOut,
	Moon,
	User,
	Settings,
	Sun,
	Trash2,
} from 'lucide-vue-next'

const router = useRouter()
const { logout, branding } = sessionStore()
let { userResource } = usersStore()
const settingsStore = useSettings()
let { isLoggedIn } = sessionStore()
const showSettingsModal = ref(false)
const frappeCloudBaseEndpoint = 'https://frappecloud.com'
const $dialog = createDialog

const props = defineProps({
	isCollapsed: {
		type: Boolean,
		default: false,
	},
})

onMounted(() => {
	if (['light', 'dark'].includes(theme.value)) {
		applyTheme(theme.value)
	}
})

watch(
	() => settingsStore.isSettingsOpen,
	(value) => {
		showSettingsModal.value = value
	}
)

const userDropdownOptions = computed(() => {
	return [
		{
			group: '',
			items: [
				{
					icon: User,
					label: 'Mi Perfil',
					onClick: () => {
						router.push(`/user/${userResource.data?.username}`)
					},
					condition: () => {
						return isLoggedIn
					},
				},
				{
					icon: theme.value === 'light' ? Moon : Sun,
					label: 'Cambiar Tema',
					onClick: () => {
						toggleTheme()
					},
				},
				{
					component: markRaw(Apps),
					condition: () => {
						let cookies = new URLSearchParams(
							document.cookie.split('; ').join('&')
						)
						let system_user = cookies.get('system_user')
						if (system_user === 'yes') return true
						else return false
					},
				},
				{
					icon: Settings,
					label: 'Ajustes',
					onClick: () => {
						settingsStore.isSettingsOpen = true
					},
					condition: () => {
						return userResource.data?.is_moderator
					},
				},
				{
					component: markRaw(Configuration),
					condition: () => {
						return userResource.data?.is_moderator
					},
				},
				{
					label: 'Borrar Datos de Prueba',
					icon: Trash2,
					onClick: () => {
						clearDemoDataConfirmation()
					},
					condition: () => {
						return (
							userResource.data?.is_moderator &&
							settingsStore.settings.data?.demo_data_present
						)
					},
				},
				{
					icon: FrappeCloudIcon,
					label: 'Iniciar sesión en Frappe Cloud',
					onClick: () => {
						$dialog({
							title: __('¿Iniciar sesión en Frappe Cloud?'),
							message: __(
								'¿Estás seguro de que deseas iniciar sesión en tu panel de Frappe Cloud?'
							),
							actions: [
								{
									label: __('Confirmar'),
									variant: 'solid',
									onClick(close) {
										loginToFrappeCloud()
										close()
									},
								},
							],
						})
					},
					condition: () => {
						return (
							userResource.data?.is_system_manager &&
							userResource.data?.is_fc_site
						)
					},
				},
				{
					icon: LogOut,
					label: 'Cerrar sesión',
					onClick: () => {
						logout.submit().then(() => {
							isLoggedIn = false
						})
					},
					condition: () => {
						return isLoggedIn
					},
				},
				{
					icon: LogIn,
					label: 'Iniciar sesión',
					onClick: () => {
						window.location.href = '/login'
					},
					condition: () => {
						return !isLoggedIn
					},
				},
			],
		},
	]
})

const loginToFrappeCloud = () => {
	let redirect_to = '/dashboard/sites/' + userResource.data.sitename
	window.open(`${frappeCloudBaseEndpoint}${redirect_to}`, '_blank')
}

const clearDemoDataConfirmation = () => {
	$dialog({
		title: __('¿Confirmar borrado de datos de prueba?'),
		message: __(
			'¿Estás seguro de que deseas borrar los datos de prueba? Esto eliminará el curso "A guide to Frappe Learning" junto con todos sus datos asociados. Esta acción no se puede deshacer.'
		),
		actions: [
			{
				label: __('Confirmar'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					clearDemoData()
					close()
				},
			},
		],
	})
}

const clearDemoData = () => {
	call('lms.lms.api.clear_demo_data')
		.then(() => {
			window.location.href = '/lms'
			toast.success(__('Datos de prueba borrados correctamente'))
		})
		.catch((error) => {
			toast.error(__(error.message || 'Error al borrar datos de prueba'))
			console.error('Error clearing demo data:', error)
		})
}
</script>

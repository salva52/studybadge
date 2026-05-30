<template>
	<button
		v-if="link && !link.onlyMobile"
		class="group flex w-full min-h-10 cursor-pointer items-center rounded-xl duration-300 ease-out focus:outline-none focus:transition-none focus-visible:ring-2 focus-visible:ring-white/30 mb-1"
		:class="
			isActive ? 'bg-white/15 shadow-sm font-semibold text-white' : 'text-white/80 hover:bg-white/10 hover:text-white'
		"
		@click="handleClick"
	>
		<div
			class="flex items-center w-full duration-300 ease-in-out group"
			:class="isCollapsed ? 'p-2 relative justify-center' : 'px-3 py-2'"
		>
			<Tooltip :text="__(link.label)" placement="right">
				<slot name="icon">
					<span class="grid h-6 w-6 flex-shrink-0 place-items-center transition-transform duration-300 group-hover:scale-[1.15]">
						<component
							:is="icons[link.icon]"
							class="h-4 w-4 stroke-[1.8px] transition-colors duration-300"
							:class="isActive ? 'text-white' : 'text-white/60 group-hover:text-white/90'"
						/>
					</span>
				</slot>
			</Tooltip>
			<span
				class="flex-shrink-0 text-[14px] duration-300 ease-out"
				:class="
					isCollapsed
						? 'ms-0 w-0 overflow-hidden opacity-0'
						: 'ms-3 w-auto opacity-100'
				"
			>
				{{ __(link.label) }}
			</span>
			<span
				v-if="link.count && !isCollapsed"
				class="!ms-auto flex items-center justify-center min-w-5 h-5 px-1.5 rounded-full text-[11px] font-bold transition-colors duration-300"
				:class="
					isCollapsed && link.count > 9
						? 'absolute top-[2px] end-0 bg-white text-sb-dark'
						: (isActive ? 'bg-white/20 text-white' : 'bg-white/10 text-white/70 group-hover:bg-white/20 group-hover:text-white')
				"
			>
				{{ link.count }}
			</span>
			<div
				v-if="showControls && !isCollapsed"
				class="flex items-center gap-x-2 !ms-auto block text-xs text-blue-200/50 group-hover:visible invisible"
			>
				<component
					:is="icons['Edit']"
					class="h-3 w-3 stroke-1.5 text-blue-200/60"
					@click.stop="openModal(link)"
				/>
				<component
					:is="icons['X']"
					class="h-3 w-3 stroke-1.5 text-blue-200/60"
					@click.stop="deletePage(link)"
				/>
			</div>
		</div>
	</button>
	<ContactUsEmail v-model="showContactForm" />
</template>
<script setup>
import { Tooltip } from 'frappe-ui'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import ContactUsEmail from '@/components/ContactUsEmail.vue'
import * as icons from 'lucide-vue-next'

const router = useRouter()
const emit = defineEmits(['openModal', 'deletePage'])
const showContactForm = ref(false)

const props = defineProps({
	link: {
		type: Object,
		required: true,
	},
	isCollapsed: {
		type: Boolean,
		default: false,
	},
	showControls: {
		type: Boolean,
		default: false,
	},
	activeTab: {
		type: String,
		default: '',
	},
})

function handleClick() {
	if (router.hasRoute(props.link.to)) {
		router.push({ name: props.link.to })
	} else if (props.link.to?.includes('@')) {
		showContactForm.value = true
	} else if (props.link.to) {
		if (props.link.to.startsWith('http')) {
			window.open(props.link.to, '_blank')
			return
		}
		window.location.href = `/${props.link.to}`
	}
}

const isActive = computed(() => {
	return (
		props.link?.activeFor?.includes(router.currentRoute.value.name) ||
		(props.activeTab && props.link?.label?.includes(props.activeTab))
	)
})

const openModal = (link) => {
	emit('openModal', link)
}

const deletePage = (link) => {
	emit('deletePage', link)
}
</script>

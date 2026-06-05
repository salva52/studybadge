<template>
	<div class="study-calendar-page">
		<header class="calendar-header">
			<div class="header-copy">
				<span class="header-kicker">{{ __('StudyBadge Plus') }}</span>
				<h1>{{ __('Calendario') }}</h1>
				<p>{{ __('Toca una fecha para crear un evento. Los dias con actividades quedan marcados automaticamente.') }}</p>
			</div>

			<div class="header-actions">
				<button class="soft-button" type="button" @click="goToday">
					<span>{{ __('Hoy') }}</span>
				</button>
				<button class="icon-button" :title="__('Recargar')" type="button" @click="loadDashboard">
					<RefreshCw class="size-4" />
				</button>
				<button class="primary-button" type="button" @click="openCreateForDay(selectedDate)">
					<Plus class="size-4" />
					<span>{{ __('Nuevo') }}</span>
				</button>
			</div>
		</header>

		<section class="coach-strip">
			<div class="coach-icon">
				<Sparkles class="size-4" />
			</div>
			<div class="coach-copy">
				<strong>{{ __('Guia IA') }}</strong>
				<p>{{ generatedMessage || coachMessage?.message || __('Crea un evento y conectalo con una Sesion IA para preparar examenes, tareas o practicas.') }}</p>
			</div>
			<button
				v-if="access?.is_plus"
				class="soft-button"
				type="button"
				:disabled="!nextEvent || generating"
				@click="generateCoachMessage(nextEvent)"
			>
				<Wand2 class="size-4" />
				<span>{{ generating ? __('Generando...') : __('Generar') }}</span>
			</button>
			<router-link v-else :to="{ name: 'Plus' }" class="soft-button plus-link">
				<Crown class="size-4" />
				<span>{{ __('Activar Plus') }}</span>
			</router-link>
		</section>

		<div v-if="loading" class="loading-state">
			<Loader2 class="size-5 spin" />
			<span>{{ __('Cargando calendario...') }}</span>
		</div>

		<template v-else>
			<main class="calendar-shell">
				<section class="calendar-card">
					<div class="month-toolbar">
						<button class="round-button" type="button" :title="__('Mes anterior')" @click="moveMonth(-1)">
							<ChevronLeft class="size-5" />
						</button>
						<div class="month-title">
							<strong>{{ monthLabel }}</strong>
							<small>{{ visibleEvents.length }} {{ visibleEvents.length === 1 ? __('evento') : __('eventos') }}</small>
						</div>
						<button class="round-button" type="button" :title="__('Mes siguiente')" @click="moveMonth(1)">
							<ChevronRight class="size-5" />
						</button>
					</div>

					<div class="calendar-grid" role="grid">
						<div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>

						<button
							v-for="cell in monthCells"
							:key="cell.key"
							type="button"
							class="day-cell"
							:class="{
								muted: !cell.inMonth,
								today: cell.isToday,
								selected: selectedDate === cell.key,
								'has-events': !!eventsByDay[cell.key]?.length,
								'draft-day': showEventModal && draftDate === cell.key,
							}"
							@click="openCreateForDay(cell.key)"
						>
							<span class="day-number">{{ cell.day }}</span>

							<div v-if="eventsByDay[cell.key]?.length" class="event-markers" :aria-label="__('Eventos del dia')">
								<span
									v-for="event in eventsByDay[cell.key].slice(0, 4)"
									:key="event.name"
									:class="['event-dot', event.event_type]"
								></span>
							</div>

							<div v-if="eventsByDay[cell.key]?.[0]" class="event-preview">
								<span :class="['preview-pill', eventsByDay[cell.key][0].event_type]">
									{{ formatTime(eventsByDay[cell.key][0].start_datetime) }}
								</span>
								<strong>{{ eventsByDay[cell.key][0].title }}</strong>
							</div>

							<span v-if="eventsByDay[cell.key]?.length > 1" class="event-count">
								+{{ eventsByDay[cell.key].length - 1 }}
							</span>
						</button>
					</div>
				</section>

				<section class="agenda-card">
					<div class="agenda-head">
						<div>
							<strong>{{ selectedDateLabel }}</strong>
							<small>{{ selectedDayEvents.length ? __('Eventos marcados en este dia') : __('No hay eventos en este dia') }}</small>
						</div>
						<button class="primary-button compact" type="button" @click="openCreateForDay(selectedDate)">
							<Plus class="size-4" />
							<span>{{ __('Agregar') }}</span>
						</button>
					</div>

					<div v-if="selectedDayEvents.length" class="event-list">
						<article v-for="event in selectedDayEvents" :key="event.name" class="event-row">
							<div :class="['type-line', event.event_type]"></div>
							<div class="event-body">
								<div class="event-title-line">
									<strong>{{ event.title }}</strong>
									<span>{{ eventTypeLabel(event.event_type) }}</span>
								</div>
								<p>
									<Clock3 class="size-3.5" />
									{{ formatTime(event.start_datetime) }} - {{ formatTime(event.end_datetime || event.start_datetime) }}
									<span v-if="event.subject"> · {{ event.subject }}</span>
									<span v-if="event.linked_ai_session"> · {{ __('Sesion IA') }}</span>
								</p>
							</div>
							<div class="row-actions">
								<router-link
									v-if="event.linked_ai_session"
									class="icon-button"
									:title="__('Practicar con IA')"
									:to="{ name: 'AISessionRoom', params: { sessionId: event.linked_ai_session } }"
								>
									<Bot class="size-4" />
								</router-link>
								<button class="icon-button" type="button" :title="__('Editar')" @click="editEvent(event)">
									<Pencil class="size-4" />
								</button>
								<button class="icon-button danger" type="button" :title="__('Eliminar')" @click="removeEvent(event)">
									<Trash2 class="size-4" />
								</button>
							</div>
						</article>
					</div>

					<div v-else class="empty-day" @click="openCreateForDay(selectedDate)">
						<CalendarDays class="size-5" />
						<div>
							<strong>{{ __('Toca para crear un evento') }}</strong>
							<small>{{ __('Ejemplo: Examen de Matematica Basica, tarea o sesion de practica.') }}</small>
						</div>
					</div>
				</section>

				<section class="upcoming-card">
					<div class="upcoming-head">
						<strong>{{ __('Proximos eventos') }}</strong>
						<small>{{ upcomingEvents.length }}</small>
					</div>
					<div class="upcoming-list">
						<button v-for="event in upcomingEvents" :key="event.name" class="upcoming-item" type="button" @click="focusEvent(event)">
							<span :class="['type-chip', event.event_type]">{{ eventTypeLabel(event.event_type) }}</span>
							<strong>{{ event.title }}</strong>
							<small>{{ formatDateTime(event.start_datetime) }}</small>
						</button>
						<div v-if="!upcomingEvents.length" class="empty-small">{{ __('Nada pendiente por ahora.') }}</div>
					</div>
				</section>
			</main>
		</template>

		<Teleport to="body">
			<div v-if="showEventModal" class="modal-backdrop" @click.self="closeModal">
				<section class="event-modal" role="dialog" aria-modal="true">
					<div class="modal-handle"></div>

					<header class="modal-head">
						<button class="text-button" type="button" @click="closeModal">{{ __('Cancelar') }}</button>
						<strong>{{ editingEvent ? __('Editar evento') : __('Nuevo evento') }}</strong>
						<button class="text-button save-text" type="button" :disabled="saving || (!access?.can_create_event && !editingEvent)" @click="saveEvent">
							{{ saving ? __('Guardando...') : __('Guardar') }}
						</button>
					</header>

					<form class="modal-form" @submit.prevent="saveEvent">
						<div class="picked-date">
							<CalendarDays class="size-5" />
							<div>
								<strong>{{ draftDateLabel }}</strong>
								<small>{{ __('El evento se marcara en esta fecha del calendario.') }}</small>
							</div>
						</div>

						<label class="field title-field">
							<span>{{ __('Titulo') }}</span>
							<input v-model="draft.title" required :placeholder="__('Examen de Matematica Basica')" />
						</label>

						<div class="field">
							<span>{{ __('Tipo') }}</span>
							<div class="type-tabs">
								<button
									v-for="type in eventTypes"
									:key="type.value"
									type="button"
									:class="['type-tab', { active: draft.event_type === type.value }]"
									@click="draft.event_type = type.value"
								>
									{{ type.label }}
								</button>
							</div>
						</div>

						<label class="field ai-field">
							<span>{{ __('Sesion IA') }}</span>
							<select v-model="draft.linked_ai_session">
								<option value="">{{ __('Sin vincular') }}</option>
								<option v-for="session in sessions" :key="session.name" :value="session.name">
									{{ session.title || session.name }}
								</option>
							</select>
							<small>{{ __('Opcional, pero recomendado para estudiar con tus documentos.') }}</small>
						</label>

						<div class="time-card">
							<label class="field">
								<span>{{ __('Fecha') }}</span>
								<input v-model="draftDate" type="date" required />
							</label>
							<div class="time-row">
								<label class="field">
									<span>{{ __('Inicio') }}</span>
									<input v-model="draftStartTime" type="time" required />
								</label>
								<label class="field">
									<span>{{ __('Fin') }}</span>
									<input v-model="draftEndTime" type="time" required />
								</label>
							</div>
							<div class="duration-tabs">
								<button type="button" @click="setDuration(30)">30 min</button>
								<button type="button" @click="setDuration(60)">1 h</button>
								<button type="button" @click="setDuration(120)">2 h</button>
							</div>
						</div>

						<button class="more-options" type="button" @click="showExtraFields = !showExtraFields">
							<span>{{ showExtraFields ? __('Ocultar detalles') : __('Agregar curso o tema') }}</span>
							<ChevronRight class="size-4" :class="{ rotated: showExtraFields }" />
						</button>

						<div v-show="showExtraFields" class="extra-fields">
							<label class="field">
								<span>{{ __('Curso') }}</span>
								<input v-model="draft.subject" :placeholder="__('Matematica Basica')" />
							</label>
							<label class="field">
								<span>{{ __('Tema') }}</span>
								<input v-model="draft.topic" :placeholder="__('Matrices y metodo de Gauss')" />
							</label>
						</div>

						<button class="modal-save-button" type="submit" :disabled="saving || (!access?.can_create_event && !editingEvent)">
							<Save class="size-4" />
							<span>{{ saving ? __('Guardando...') : editingEvent ? __('Guardar cambios') : __('Crear evento') }}</span>
						</button>
					</form>
				</section>
			</div>
		</Teleport>
	</div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { call, toast, usePageMeta } from 'frappe-ui'
import {
	Bot,
	CalendarDays,
	ChevronLeft,
	ChevronRight,
	Clock3,
	Crown,
	Loader2,
	Pencil,
	Plus,
	RefreshCw,
	Save,
	Sparkles,
	Trash2,
	Wand2,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const route = useRoute()
const { brand } = sessionStore()

const loading = ref(true)
const saving = ref(false)
const generating = ref(false)
const access = ref(null)
const sessions = ref([])
const events = ref([])
const coachMessage = ref(null)
const generatedMessage = ref('')
const editingEvent = ref(null)
const showEventModal = ref(false)
const showExtraFields = ref(false)
const selectedDate = ref(dateKey(new Date()))
const monthCursor = ref(startOfMonth(new Date()))
const draft = ref(makeDraft(selectedDate.value))

const eventTypes = [
	{ value: 'exam', label: __('Examen') },
	{ value: 'task', label: __('Tarea') },
	{ value: 'delivery', label: __('Entrega') },
	{ value: 'class', label: __('Clase') },
	{ value: 'practice', label: __('Practica') },
	{ value: 'reminder', label: __('Recordatorio') },
]

const weekdays = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']

const draftDate = computed({
	get() {
		return String(draft.value.start_datetime || '').slice(0, 10) || selectedDate.value || dateKey(new Date())
	},
	set(value) {
		if (!value) return
		const startTime = draftStartTime.value || '09:00'
		draft.value.start_datetime = `${value}T${startTime}`
		draft.value.end_datetime = `${value}T${addMinutesToTime(startTime, getCurrentDuration() || 60)}`
		selectedDate.value = value
		monthCursor.value = startOfMonth(parseDate(value))
	},
})

const draftStartTime = computed({
	get() {
		return String(draft.value.start_datetime || '').slice(11, 16) || '09:00'
	},
	set(value) {
		if (!value) return
		const date = draftDate.value || dateKey(new Date())
		draft.value.start_datetime = `${date}T${value}`

		if (!draft.value.end_datetime || parseDate(draft.value.end_datetime) <= parseDate(draft.value.start_datetime)) {
			draft.value.end_datetime = `${date}T${addMinutesToTime(value, 60)}`
		}
	},
})

const draftEndTime = computed({
	get() {
		return String(draft.value.end_datetime || '').slice(11, 16) || addMinutesToTime(draftStartTime.value, 60)
	},
	set(value) {
		if (!value) return
		const date = draftDate.value || dateKey(new Date())
		draft.value.end_datetime = `${date}T${value}`
	},
})

usePageMeta(() => ({ title: __('Calendario'), icon: brand.favicon }))

onMounted(loadDashboard)

watch(
	() => draft.value.linked_ai_session,
	(sessionName) => {
		const session = sessions.value.find((item) => item.name === sessionName)
		if (!session) return
		if (!draft.value.subject) draft.value.subject = session.academic_context || ''
		if (!draft.value.topic) draft.value.topic = session.goal || session.desired_topics || ''
		if (!draft.value.title) draft.value.title = `${eventTypeLabel(draft.value.event_type)} - ${session.title || session.name}`
		if (draft.value.subject || draft.value.topic) showExtraFields.value = true
	}
)

const eventsByDay = computed(() => {
	return events.value.reduce((map, event) => {
		const key = dateKey(parseDate(event.start_datetime))
		if (!map[key]) map[key] = []
		map[key].push(event)
		map[key].sort((a, b) => parseDate(a.start_datetime) - parseDate(b.start_datetime))
		return map
	}, {})
})

const monthCells = computed(() => {
	const first = startOfMonth(monthCursor.value)
	const offset = (first.getDay() + 6) % 7
	const start = new Date(first)
	start.setDate(first.getDate() - offset)

	return Array.from({ length: 42 }, (_, index) => {
		const date = new Date(start)
		date.setDate(start.getDate() + index)
		return {
			key: dateKey(date),
			day: date.getDate(),
			inMonth: date.getMonth() === monthCursor.value.getMonth(),
			isToday: dateKey(date) === dateKey(new Date()),
		}
	})
})

const monthLabel = computed(() => {
	return monthCursor.value.toLocaleDateString(undefined, { month: 'long', year: 'numeric' })
})

const selectedDateLabel = computed(() => {
	return parseDate(selectedDate.value).toLocaleDateString(undefined, {
		weekday: 'long',
		day: 'numeric',
		month: 'long',
	})
})

const draftDateLabel = computed(() => {
	return parseDate(draftDate.value).toLocaleDateString(undefined, {
		weekday: 'long',
		day: 'numeric',
		month: 'long',
		year: 'numeric',
	})
})

const selectedDayEvents = computed(() => eventsByDay.value[selectedDate.value] || [])

const visibleEvents = computed(() => {
	return events.value.filter((event) => {
		const date = parseDate(event.start_datetime)
		return date.getMonth() === monthCursor.value.getMonth() && date.getFullYear() === monthCursor.value.getFullYear()
	})
})

const upcomingEvents = computed(() => {
	const now = new Date()
	return events.value
		.filter((event) => parseDate(event.start_datetime) >= now && event.status !== 'cancelled')
		.sort((a, b) => parseDate(a.start_datetime) - parseDate(b.start_datetime))
		.slice(0, 8)
})

const nextEvent = computed(() => upcomingEvents.value[0] || events.value[0])

async function api(method, params = {}) {
	try {
		return await call(`studybadge_ai.study_calendar.${method}`, params)
	} catch (error) {
		toast.error(error.messages?.[0] || error.message || __('No se pudo completar la accion.'))
		throw error
	}
}

async function loadDashboard() {
	loading.value = true
	try {
		const data = await api('get_calendar_dashboard')
		access.value = data.access
		sessions.value = data.sessions || []
		events.value = data.events || []
		coachMessage.value = data.coach_message
		applyRouteDraft()
	} finally {
		loading.value = false
	}
}

async function refreshDashboard() {
	const data = await api('get_calendar_dashboard')
	access.value = data.access
	sessions.value = data.sessions || sessions.value
	events.value = data.events || []
	coachMessage.value = data.coach_message
}

function applyRouteDraft() {
	const sessionName = route.query.session
	if (!sessionName) return

	const session = sessions.value.find((item) => item.name === sessionName)
	const eventType = route.query.type || 'exam'
	const date = route.query.date || selectedDate.value

	selectedDate.value = date
	monthCursor.value = startOfMonth(parseDate(date))
	draft.value = {
		...makeDraft(date),
		linked_ai_session: sessionName,
		title: session ? `${eventTypeLabel(eventType)} - ${session.title || session.name}` : '',
		subject: session?.academic_context || '',
		topic: session?.goal || session?.desired_topics || '',
		event_type: eventType,
	}
	showExtraFields.value = !!(draft.value.subject || draft.value.topic)
	showEventModal.value = true
}

function makeDraft(date = dateKey(new Date())) {
	const start = defaultStartForDate(date)
	const end = new Date(start.getTime() + 60 * 60 * 1000)
	return {
		title: '',
		event_type: 'exam',
		subject: '',
		topic: '',
		difficulty: 'medium',
		importance: 'high',
		start_datetime: formatInputDate(start),
		end_datetime: formatInputDate(end),
		linked_ai_session: '',
		reminder_enabled: true,
		reminder_time: '1_day_before',
	}
}

function openCreateForDay(key = selectedDate.value) {
	selectedDate.value = key
	monthCursor.value = startOfMonth(parseDate(key))
	editingEvent.value = null
	draft.value = makeDraft(key)
	showExtraFields.value = false
	showEventModal.value = true
}

function editEvent(event) {
	editingEvent.value = event
	selectedDate.value = dateKey(parseDate(event.start_datetime))
	monthCursor.value = startOfMonth(parseDate(event.start_datetime))
	draft.value = {
		title: event.title || '',
		event_type: event.event_type || 'exam',
		subject: event.subject || '',
		topic: event.topic || '',
		difficulty: event.difficulty || 'medium',
		importance: event.importance || 'high',
		start_datetime: formatInputDate(parseDate(event.start_datetime)),
		end_datetime: formatInputDate(parseDate(event.end_datetime || event.start_datetime)),
		linked_ai_session: event.linked_ai_session || '',
		reminder_enabled: event.reminder_enabled === undefined ? true : !!event.reminder_enabled,
		reminder_time: event.reminder_time || '1_day_before',
	}
	showExtraFields.value = !!(draft.value.subject || draft.value.topic)
	showEventModal.value = true
}

function closeModal() {
	if (saving.value) return
	showEventModal.value = false
	editingEvent.value = null
	showExtraFields.value = false
}

async function saveEvent() {
	saving.value = true
	try {
		const payload = {
			...draft.value,
			start_datetime: toServerDatetime(draft.value.start_datetime),
			end_datetime: toServerDatetime(draft.value.end_datetime),
			reminder_enabled: draft.value.reminder_enabled ? 1 : 0,
		}

		if (editingEvent.value) {
			await api('update_study_calendar_event', { event: editingEvent.value.name, data: payload })
			toast.success(__('Evento actualizado.'))
		} else {
			await api('create_study_calendar_event', { data: payload })
			toast.success(__('Evento creado.'))
		}

		selectedDate.value = draftDate.value
		monthCursor.value = startOfMonth(parseDate(draftDate.value))
		showEventModal.value = false
		editingEvent.value = null
		showExtraFields.value = false
		await refreshDashboard()
	} finally {
		saving.value = false
	}
}

async function removeEvent(event) {
	if (!confirm(__('Eliminar este evento del calendario?'))) return
	await api('delete_study_calendar_event', { event: event.name })
	toast.success(__('Evento eliminado.'))
	await refreshDashboard()
	if (editingEvent.value?.name === event.name) closeModal()
}

async function generateCoachMessage(event) {
	if (!event) return
	generating.value = true
	try {
		const response = await api('generate_motivation_message', { event: event.name })
		generatedMessage.value = response.message
		toast.success(__('Coach IA listo.'))
	} finally {
		generating.value = false
	}
}

function goToday() {
	const today = dateKey(new Date())
	selectedDate.value = today
	monthCursor.value = startOfMonth(new Date())
}

function moveMonth(delta) {
	const next = new Date(monthCursor.value)
	next.setMonth(next.getMonth() + delta)
	monthCursor.value = startOfMonth(next)
}

function focusEvent(event) {
	const date = parseDate(event.start_datetime)
	monthCursor.value = startOfMonth(date)
	selectedDate.value = dateKey(date)
}

function eventTypeLabel(type) {
	return {
		exam: __('Examen'),
		task: __('Tarea'),
		delivery: __('Entrega'),
		class: __('Clase'),
		practice: __('Practica'),
		reminder: __('Recordatorio'),
	}[type] || __('Evento')
}

function formatDateTime(value) {
	return parseDate(value).toLocaleString(undefined, {
		day: '2-digit',
		month: 'short',
		hour: '2-digit',
		minute: '2-digit',
	})
}

function formatTime(value) {
	return parseDate(value).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })
}

function setDuration(minutes) {
	const start = parseDate(draft.value.start_datetime)
	const end = new Date(start.getTime() + minutes * 60 * 1000)
	draft.value.end_datetime = formatInputDate(end)
}

function getCurrentDuration() {
	const start = parseDate(draft.value.start_datetime)
	const end = parseDate(draft.value.end_datetime)
	const minutes = Math.round((end - start) / 60000)
	return Number.isFinite(minutes) && minutes > 0 ? minutes : 60
}

function addMinutesToTime(value, minutes) {
	const [hours = '09', mins = '00'] = String(value || '09:00').split(':')
	const date = new Date(2000, 0, 1, Number(hours), Number(mins) + minutes)
	return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

function defaultStartForDate(value) {
	const key = typeof value === 'string' ? value.slice(0, 10) : dateKey(value)
	const today = dateKey(new Date())

	if (key === today) return roundToHour(new Date())

	const date = parseDate(key)
	date.setHours(9, 0, 0, 0)
	return date
}

function startOfMonth(date) {
	return new Date(date.getFullYear(), date.getMonth(), 1)
}

function roundToHour(date = new Date()) {
	const next = new Date(date)
	next.setMinutes(0, 0, 0)
	if (next <= new Date()) next.setHours(next.getHours() + 1)
	return next
}

function parseDate(value) {
	if (value instanceof Date) return value
	let str = String(value || '').trim()
	if (str.length === 10) str += 'T00:00:00'
	return new Date(str.replace(' ', 'T'))
}

function dateKey(date) {
	const d = parseDate(date)
	const month = String(d.getMonth() + 1).padStart(2, '0')
	const day = String(d.getDate()).padStart(2, '0')
	return `${d.getFullYear()}-${month}-${day}`
}

function formatInputDate(date) {
	const d = parseDate(date)
	const month = String(d.getMonth() + 1).padStart(2, '0')
	const day = String(d.getDate()).padStart(2, '0')
	const hours = String(d.getHours()).padStart(2, '0')
	const minutes = String(d.getMinutes()).padStart(2, '0')
	return `${d.getFullYear()}-${month}-${day}T${hours}:${minutes}`
}

function toServerDatetime(value) {
	return String(value || '').replace('T', ' ')
}
</script>

<style scoped>
.study-calendar-page {
	min-height: 100dvh;
	background: #f5f5f7;
	color: #111827;
	padding: 1rem;
}

.calendar-header,
.coach-strip,
.calendar-shell {
	width: min(1320px, 100%);
	margin: 0 auto;
}

.calendar-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	margin-bottom: 0.75rem;
}

.header-copy {
	min-width: 0;
}

.header-kicker {
	display: inline-flex;
	width: fit-content;
	border: 1px solid #e5e7eb;
	border-radius: 999px;
	background: #ffffff;
	color: #6b7280;
	padding: 0.25rem 0.6rem;
	font-size: 0.72rem;
	font-weight: 800;
}

.calendar-header h1 {
	margin: 0.35rem 0 0.12rem;
	font-size: clamp(2rem, 4vw, 3.25rem);
	line-height: 0.95;
	letter-spacing: -0.06em;
}

.calendar-header p,
.coach-copy p,
.event-body p,
.agenda-head small,
.upcoming-head small,
.month-title small,
.empty-small,
.empty-day small,
.ai-field small,
.picked-date small {
	color: #6b7280;
}

.calendar-header p {
	max-width: 660px;
	margin: 0;
	font-size: 0.95rem;
}

.header-actions,
.coach-strip,
.coach-copy,
.agenda-head,
.upcoming-head,
.row-actions,
.event-body p,
.event-markers,
.duration-tabs,
.time-row {
	display: flex;
	align-items: center;
	gap: 0.55rem;
}

.header-actions {
	flex-shrink: 0;
}

.primary-button,
.soft-button,
.icon-button,
.round-button,
.text-button,
.modal-save-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.45rem;
	border: 1px solid transparent;
	border-radius: 999px;
	font-weight: 800;
	line-height: 1;
	cursor: pointer;
	transition: background 0.16s ease, border-color 0.16s ease, transform 0.16s ease;
}

.primary-button {
	min-height: 42px;
	background: #111827;
	color: #ffffff;
	padding: 0 1rem;
}

.primary-button:hover:not(:disabled),
.modal-save-button:hover:not(:disabled) {
	background: #000000;
}

.soft-button,
.icon-button,
.round-button {
	background: #ffffff;
	border-color: #e5e7eb;
	color: #111827;
}

.soft-button:hover:not(:disabled),
.icon-button:hover,
.round-button:hover {
	background: #f9fafb;
	border-color: #d1d5db;
}

.soft-button {
	min-height: 40px;
	padding: 0 0.85rem;
	font-size: 0.86rem;
	text-decoration: none;
}

.icon-button,
.round-button {
	width: 42px;
	height: 42px;
	padding: 0;
	flex: 0 0 auto;
}

.round-button {
	width: 46px;
	height: 46px;
	background: #f5f5f7;
}

.icon-button.danger {
	color: #b42318;
}

.icon-button.danger:hover {
	background: #fef3f2;
	border-color: #fecaca;
}

.primary-button:disabled,
.soft-button:disabled,
.text-button:disabled,
.modal-save-button:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.compact {
	min-height: 38px;
	padding: 0 0.85rem;
	font-size: 0.85rem;
}

.coach-strip {
	grid-template-columns: auto minmax(0, 1fr) auto;
	margin-bottom: 0.85rem;
	border: 1px solid #e5e7eb;
	border-radius: 24px;
	background: #ffffff;
	padding: 0.85rem;
	box-shadow: 0 10px 30px rgba(17, 24, 39, 0.05);
}

.coach-icon {
	display: grid;
	width: 42px;
	height: 42px;
	place-items: center;
	border-radius: 14px;
	background: #f3f4f6;
	color: #111827;
}

.coach-copy {
	align-items: flex-start;
	flex-direction: column;
	gap: 0.1rem;
	min-width: 0;
}

.coach-copy p {
	overflow: hidden;
	display: -webkit-box;
	margin: 0;
	font-size: 0.9rem;
	line-height: 1.35;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
}

.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 0.55rem;
	min-height: 420px;
	color: #6b7280;
}

.spin {
	animation: spin 0.9s linear infinite;
}

.calendar-shell {
	display: grid;
	grid-template-columns: minmax(0, 1fr) minmax(270px, 320px);
	grid-template-areas:
		'calendar upcoming'
		'agenda upcoming';
	gap: 0.85rem;
	align-items: start;
}

.calendar-card,
.agenda-card,
.upcoming-card {
	border: 1px solid #e5e7eb;
	border-radius: 28px;
	background: #ffffff;
	box-shadow: 0 14px 40px rgba(17, 24, 39, 0.06);
}

.calendar-card {
	grid-area: calendar;
	padding: 0.9rem;
}

.month-toolbar {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr) auto;
	align-items: center;
	gap: 1rem;
	margin-bottom: 0.8rem;
}

.month-title {
	display: grid;
	justify-items: center;
	gap: 0.15rem;
	text-align: center;
	text-transform: capitalize;
}

.month-title strong {
	font-size: clamp(1.25rem, 2vw, 1.75rem);
	letter-spacing: -0.04em;
}

.calendar-grid {
	display: grid;
	grid-template-columns: repeat(7, minmax(0, 1fr));
	gap: 0.38rem;
}

.weekday {
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 32px;
	color: #9ca3af;
	font-size: 0.73rem;
	font-weight: 900;
	text-transform: uppercase;
}

.day-cell {
	position: relative;
	display: grid;
	grid-template-rows: auto auto minmax(0, 1fr);
	align-content: start;
	gap: 0.38rem;
	min-height: clamp(82px, 7.2vw, 112px);
	border: 1px solid #f0f0f0;
	border-radius: 19px;
	background: #ffffff;
	padding: 0.58rem;
	text-align: left;
	cursor: pointer;
	transition: background 0.16s ease, border-color 0.16s ease, transform 0.16s ease, box-shadow 0.16s ease;
}

.day-cell:hover {
	background: #fafafa;
	border-color: #d1d5db;
	transform: translateY(-1px);
}

.day-cell.muted {
	background: #fbfbfc;
	color: #c0c4cc;
}

.day-cell.selected,
.day-cell.draft-day {
	border-color: #111827;
	box-shadow: inset 0 0 0 1px #111827;
}

.day-cell.has-events {
	background: #fdfdfd;
}

.day-number {
	display: grid;
	width: 31px;
	height: 31px;
	place-items: center;
	border-radius: 999px;
	font-size: 0.9rem;
	font-weight: 850;
}

.day-cell.today .day-number {
	background: #111827;
	color: #ffffff;
}

.day-cell.selected:not(.today) .day-number,
.day-cell.draft-day:not(.today) .day-number {
	background: #e5e7eb;
	color: #111827;
}

.event-markers {
	gap: 0.22rem;
	min-height: 8px;
}

.event-dot {
	width: 7px;
	height: 7px;
	border-radius: 999px;
	background: #6b7280;
}

.event-preview {
	min-width: 0;
	display: grid;
	align-content: start;
	gap: 0.25rem;
	margin-top: 0.1rem;
}

.event-preview strong {
	overflow: hidden;
	color: #111827;
	font-size: 0.78rem;
	font-weight: 800;
	line-height: 1.1;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.preview-pill,
.type-chip,
.event-title-line span {
	width: fit-content;
	border-radius: 999px;
	padding: 0.2rem 0.45rem;
	font-size: 0.68rem;
	font-weight: 900;
	line-height: 1;
}

.event-count {
	position: absolute;
	right: 0.65rem;
	top: 0.72rem;
	border-radius: 999px;
	background: #f3f4f6;
	color: #6b7280;
	padding: 0.12rem 0.35rem;
	font-size: 0.66rem;
	font-weight: 900;
}

.event-dot.exam,
.preview-pill.exam,
.type-line.exam,
.type-chip.exam,
.event-title-line span.exam {
	background: #fee2e2;
	color: #b42318;
}

.event-dot.task,
.preview-pill.task,
.type-line.task,
.type-chip.task,
.event-title-line span.task {
	background: #dbeafe;
	color: #175cd3;
}

.event-dot.delivery,
.preview-pill.delivery,
.type-line.delivery,
.type-chip.delivery,
.event-title-line span.delivery {
	background: #fef3c7;
	color: #b54708;
}

.event-dot.class,
.preview-pill.class,
.type-line.class,
.type-chip.class,
.event-title-line span.class {
	background: #dcfce7;
	color: #027a48;
}

.event-dot.practice,
.preview-pill.practice,
.type-line.practice,
.type-chip.practice,
.event-title-line span.practice {
	background: #ede9fe;
	color: #5925dc;
}

.event-dot.reminder,
.preview-pill.reminder,
.type-line.reminder,
.type-chip.reminder,
.event-title-line span.reminder {
	background: #e0f2fe;
	color: #026aa2;
}

.agenda-card {
	grid-area: agenda;
	padding: 1rem;
}

.agenda-head,
.upcoming-head {
	justify-content: space-between;
	margin-bottom: 0.75rem;
}

.agenda-head > div,
.upcoming-head {
	min-width: 0;
}

.agenda-head strong,
.upcoming-head strong {
	font-size: 1.05rem;
	letter-spacing: -0.02em;
	text-transform: capitalize;
}

.agenda-head small,
.upcoming-head small {
	display: block;
	margin-top: 0.15rem;
	font-size: 0.82rem;
}

.event-list {
	display: grid;
	gap: 0.55rem;
}

.event-row {
	display: grid;
	grid-template-columns: 7px minmax(0, 1fr) auto;
	gap: 0.65rem;
	align-items: stretch;
	border: 1px solid #f0f0f0;
	border-radius: 18px;
	background: #ffffff;
	padding: 0.7rem;
}

.type-line {
	width: 7px;
	border-radius: 999px;
}

.event-body {
	min-width: 0;
}

.event-title-line {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
	min-width: 0;
}

.event-title-line strong,
.upcoming-item strong {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.event-title-line span {
	background: #f3f4f6;
	color: #6b7280;
	white-space: nowrap;
}

.event-body p {
	gap: 0.32rem;
	flex-wrap: wrap;
	margin: 0.25rem 0 0;
	font-size: 0.82rem;
	font-weight: 700;
}

.empty-day {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	border: 1px dashed #d1d5db;
	border-radius: 18px;
	background: #fafafa;
	padding: 1rem;
	cursor: pointer;
}

.empty-day strong {
	display: block;
}

.upcoming-card {
	grid-area: upcoming;
	position: sticky;
	top: 1rem;
	padding: 1rem;
}

.upcoming-list {
	display: grid;
	gap: 0.5rem;
	max-height: 620px;
	overflow: auto;
	padding-right: 0.1rem;
}

.upcoming-item {
	display: grid;
	gap: 0.28rem;
	border: 1px solid #f0f0f0;
	border-radius: 18px;
	background: #ffffff;
	padding: 0.75rem;
	text-align: left;
	cursor: pointer;
}

.upcoming-item:hover {
	border-color: #d1d5db;
	background: #fafafa;
}

.upcoming-item small {
	color: #6b7280;
	font-weight: 700;
}

.empty-small {
	border: 1px dashed #d1d5db;
	border-radius: 16px;
	padding: 0.9rem;
	font-weight: 750;
}

.modal-backdrop {
	position: fixed;
	inset: 0;
	z-index: 1000;
	display: flex;
	align-items: center;
	justify-content: center;
	background: rgba(17, 24, 39, 0.38);
	padding: 1rem;
}

.event-modal {
	width: min(560px, 100%);
	max-height: min(92dvh, 760px);
	overflow: hidden;
	border: 1px solid #e5e7eb;
	border-radius: 30px;
	background: #ffffff;
	box-shadow: 0 30px 80px rgba(17, 24, 39, 0.2);
}

.modal-handle {
	display: none;
	width: 42px;
	height: 5px;
	border-radius: 999px;
	background: #d1d5db;
	margin: 0.7rem auto 0;
}

.modal-head {
	display: grid;
	grid-template-columns: 1fr auto 1fr;
	align-items: center;
	gap: 0.5rem;
	border-bottom: 1px solid #f0f0f0;
	padding: 0.9rem 1rem;
}

.modal-head strong {
	text-align: center;
	font-size: 1rem;
}

.text-button {
	min-height: 36px;
	background: transparent;
	color: #2563eb;
	padding: 0 0.35rem;
	font-size: 0.9rem;
}

.modal-head .text-button:first-child {
	justify-self: start;
	margin-left: -0.35rem;
}

.save-text {
	justify-self: end;
	font-weight: 900;
}

.modal-form {
	display: grid;
	gap: 0.85rem;
	max-height: calc(min(92dvh, 760px) - 62px);
	overflow: auto;
	padding: 1rem;
}

.picked-date {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	border: 1px solid #e5e7eb;
	border-radius: 20px;
	background: #f9fafb;
	padding: 0.85rem;
}

.picked-date svg {
	color: #2563eb;
}

.picked-date strong {
	display: block;
	color: #111827;
	font-weight: 900;
	text-transform: capitalize;
}

.picked-date div {
	min-width: 0;
}

.picked-date small {
	display: block;
	margin-top: 0.12rem;
}

.field {
	display: grid;
	gap: 0.35rem;
	min-width: 0;
}

.field > span {
	color: #6b7280;
	font-size: 0.78rem;
	font-weight: 850;
}

.field input,
.field select {
	width: 100%;
	min-height: 48px;
	border: 1px solid #e5e7eb;
	border-radius: 16px;
	background: #ffffff;
	color: #111827;
	padding: 0 0.9rem;
	font: inherit;
	font-size: 0.95rem;
	outline: none;
	transition: border-color 0.16s ease, box-shadow 0.16s ease;
}

.title-field input {
	min-height: 54px;
	font-size: 1.02rem;
	font-weight: 760;
}

.field input:focus,
.field select:focus {
	border-color: #111827;
	box-shadow: 0 0 0 4px rgba(17, 24, 39, 0.08);
}

.type-tabs,
.duration-tabs {
	display: flex;
	gap: 0.45rem;
	overflow-x: auto;
	padding-bottom: 0.05rem;
}

.type-tab,
.duration-tabs button,
.more-options {
	border: 1px solid #e5e7eb;
	border-radius: 999px;
	background: #ffffff;
	color: #374151;
	padding: 0 0.8rem;
	font-weight: 850;
	white-space: nowrap;
	cursor: pointer;
}

.type-tab {
	min-height: 38px;
}

.type-tab.active {
	background: #111827;
	border-color: #111827;
	color: #ffffff;
}

.time-card,
.extra-fields {
	display: grid;
	gap: 0.75rem;
	border: 1px solid #f0f0f0;
	border-radius: 20px;
	background: #fbfbfc;
	padding: 0.85rem;
}

.time-row {
	align-items: flex-start;
}

.time-row .field {
	flex: 1;
}

.duration-tabs button {
	min-height: 34px;
	font-size: 0.82rem;
}

.duration-tabs button:hover,
.more-options:hover {
	border-color: #d1d5db;
	background: #f9fafb;
}

.more-options {
	display: flex;
	align-items: center;
	justify-content: space-between;
	width: 100%;
	min-height: 44px;
	border-radius: 16px;
}

.more-options svg {
	transition: transform 0.16s ease;
}

.more-options svg.rotated {
	transform: rotate(90deg);
}

.modal-save-button {
	min-height: 52px;
	background: #111827;
	color: #ffffff;
	font-size: 0.95rem;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

@media (max-width: 1100px) {
	.calendar-shell {
		grid-template-columns: 1fr;
		grid-template-areas:
			'calendar'
			'agenda'
			'upcoming';
	}

	.upcoming-card {
		position: static;
	}

	.upcoming-list {
		grid-template-columns: repeat(2, minmax(0, 1fr));
		max-height: none;
	}
}

@media (max-width: 760px) {
	.study-calendar-page {
		padding: 0.75rem;
	}

	.calendar-header {
		align-items: flex-start;
	}

	.calendar-header h1 {
		font-size: 2rem;
	}

	.calendar-header p,
	.header-kicker {
		display: none;
	}

	.header-actions {
		gap: 0.35rem;
	}

	.header-actions .primary-button span,
	.coach-strip .soft-button span {
		display: none;
	}

	.coach-strip {
		grid-template-columns: minmax(0, 1fr) auto;
		border-radius: 20px;
		padding: 0.75rem;
	}

	.coach-icon {
		display: none;
	}

	.coach-copy p {
		-webkit-line-clamp: 1;
	}

	.calendar-card,
	.agenda-card,
	.upcoming-card {
		border-radius: 22px;
	}

	.calendar-card {
		padding: 0.7rem;
	}

	.month-toolbar {
		gap: 0.55rem;
		margin-bottom: 0.5rem;
	}

	.round-button {
		width: 40px;
		height: 40px;
	}

	.month-title strong {
		font-size: 1.25rem;
	}

	.calendar-grid {
		gap: 0.28rem;
	}

	.weekday {
		min-height: 28px;
		font-size: 0.64rem;
	}

	.day-cell {
		min-height: 68px;
		border-radius: 15px;
		padding: 0.42rem;
		gap: 0.22rem;
	}

	.day-number {
		width: 28px;
		height: 28px;
		font-size: 0.82rem;
	}

	.event-preview {
		display: none;
	}

	.event-count {
		top: auto;
		right: 0.45rem;
		bottom: 0.42rem;
		font-size: 0.6rem;
	}

	.agenda-head {
		align-items: flex-start;
	}

	.event-row {
		grid-template-columns: 6px minmax(0, 1fr);
		border-radius: 16px;
	}

	.row-actions {
		grid-column: 2;
		justify-content: flex-start;
	}

	.upcoming-list {
		grid-template-columns: 1fr;
	}

	.modal-backdrop {
		align-items: flex-end;
		padding: 0;
	}

	.event-modal {
		width: 100%;
		max-height: 92dvh;
		border-radius: 28px 28px 0 0;
		border-bottom: 0;
	}

	.modal-handle {
		display: block;
	}

	.modal-form {
		padding: 0.9rem;
	}

	.time-row {
		gap: 0.5rem;
	}
}

@media (max-width: 430px) {
	.study-calendar-page {
		padding: 0.55rem;
	}

	.calendar-shell {
		gap: 0.6rem;
	}

	.calendar-header h1 {
		font-size: 1.65rem;
	}

	.soft-button,
	.primary-button,
	.icon-button {
		min-height: 40px;
	}

	.icon-button,
	.header-actions .primary-button {
		width: 40px;
		padding: 0;
	}

	.calendar-card,
	.agenda-card,
	.upcoming-card {
		box-shadow: none;
	}

	.day-cell {
		min-height: 58px;
		border-radius: 13px;
		padding: 0.32rem;
	}

	.day-number {
		width: 24px;
		height: 24px;
		font-size: 0.76rem;
	}

	.event-dot {
		width: 5px;
		height: 5px;
	}

	.event-markers {
		gap: 0.15rem;
	}

	.event-count {
		display: none;
	}

	.modal-head {
		padding: 0.75rem 0.85rem;
	}

	.modal-head .text-button:first-child {
		margin-left: -0.25rem;
	}

	.field input,
	.field select {
		min-height: 46px;
	}

	.time-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
	}

	.duration-tabs {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}

	.duration-tabs button {
		padding: 0;
	}
}
</style>

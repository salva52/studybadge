<template>
	<div class="study-calendar-page">
		<header class="calendar-header">
			<div>
				<div class="eyebrow">
					<Crown class="size-4" />
					<span>{{ __('Coach IA Plus') }}</span>
				</div>
				<h1>{{ __('Calendario Inteligente') }}</h1>
				<p>{{ __('Sesiones IA, examenes, tareas y recordatorios en un solo lugar.') }}</p>
			</div>
			<div class="header-actions">
				<button class="icon-button" :title="__('Recargar')" @click="loadDashboard">
					<RefreshCw class="size-5" />
				</button>
				<button class="primary-button" @click="startCreate()">
					<Plus class="size-4" />
					<span>{{ __('Nuevo evento') }}</span>
				</button>
			</div>
		</header>

		<section class="coach-strip">
			<div class="coach-icon">
				<Sparkles class="size-5" />
			</div>
			<div class="coach-copy">
				<strong>{{ __('Mi guia de estudio') }}</strong>
				<p>{{ generatedMessage || coachMessage?.message }}</p>
			</div>
			<button v-if="access?.is_plus" class="secondary-button" :disabled="!nextEvent || generating" @click="generateCoachMessage(nextEvent)">
				<Wand2 class="size-4" />
				<span>{{ generating ? __('Generando...') : __('Generar mensaje IA') }}</span>
			</button>
			<router-link v-else :to="{ name: 'Plus' }" class="secondary-button plus-link">
				<Crown class="size-4" />
				<span>{{ __('Activar Plus') }}</span>
			</router-link>
		</section>

		<div v-if="loading" class="loading-state">
			<Loader2 class="size-6 spin" />
			<span>{{ __('Cargando calendario...') }}</span>
		</div>

		<template v-else>
			<div class="calendar-layout">
				<main class="calendar-main">
					<div class="month-toolbar">
						<button class="icon-button" :title="__('Mes anterior')" @click="moveMonth(-1)">
							<ChevronLeft class="size-5" />
						</button>
						<div>
							<strong>{{ monthLabel }}</strong>
							<small>{{ visibleEvents.length }} {{ __('eventos') }}</small>
						</div>
						<button class="icon-button" :title="__('Mes siguiente')" @click="moveMonth(1)">
							<ChevronRight class="size-5" />
						</button>
					</div>

					<div class="calendar-grid">
						<div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
						<button
							v-for="cell in monthCells"
							:key="cell.key"
							class="day-cell"
							:class="{ muted: !cell.inMonth, today: cell.isToday, selected: selectedDate === cell.key }"
							@click="selectDay(cell.key)"
						>
							<span class="day-number">{{ cell.day }}</span>
							<div class="day-events">
								<span v-for="event in eventsByDay[cell.key]?.slice(0, 3)" :key="event.name" :class="['event-dot', event.event_type]">
									{{ event.title }}
								</span>
							</div>
						</button>
					</div>

					<section class="day-agenda">
						<div class="section-head">
							<div>
								<strong>{{ selectedDateLabel }}</strong>
								<small>{{ selectedDayEvents.length ? __('Eventos del dia') : __('Sin eventos') }}</small>
							</div>
							<button class="secondary-button compact" @click="startCreate(selectedDate)">
								<Plus class="size-4" />
								<span>{{ __('Agregar') }}</span>
							</button>
						</div>

						<div v-if="selectedDayEvents.length" class="event-list">
							<article v-for="event in selectedDayEvents" :key="event.name" class="event-row">
								<div :class="['type-mark', event.event_type]"></div>
								<div class="event-body">
									<div class="event-title-line">
										<strong>{{ event.title }}</strong>
										<span>{{ eventTypeLabel(event.event_type) }}</span>
									</div>
									<p>{{ event.subject || __('Sin curso') }} <span v-if="event.topic">- {{ event.topic }}</span></p>
									<div class="event-meta">
										<span><Clock3 class="size-3.5" /> {{ formatTime(event.start_datetime) }}</span>
										<span><Flag class="size-3.5" /> {{ importanceLabel(event.importance) }}</span>
										<span v-if="event.linked_ai_session"><MessagesSquare class="size-3.5" /> {{ __('Sesion IA') }}</span>
									</div>
								</div>
								<div class="row-actions">
									<router-link
										v-if="event.linked_ai_session"
										class="icon-button"
										:title="__('Practicar con IA')"
										:to="{ name: 'AISessionRoom', params: { sessionId: event.linked_ai_session } }"
									>
										<Bot class="size-5" />
									</router-link>
									<button class="icon-button" :title="__('Editar')" @click="editEvent(event)">
										<Pencil class="size-4" />
									</button>
									<button class="icon-button danger" :title="__('Eliminar')" @click="removeEvent(event)">
										<Trash2 class="size-4" />
									</button>
								</div>
							</article>
						</div>
						<div v-else class="empty-day">
							<CalendarDays class="size-5" />
							<span>{{ __('Agenda un examen, tarea o recordatorio de estudio.') }}</span>
						</div>
					</section>
				</main>

				<aside class="planner-panel">
					<section class="plan-status">
						<div>
							<strong>{{ access?.is_plus ? __('Plus activo') : __('Plan gratuito') }}</strong>
							<small v-if="access?.is_plus">{{ __('Eventos ilimitados y Coach IA personalizado') }}</small>
							<small v-else>{{ access?.events_used || 0 }}/{{ access?.free_event_limit || 5 }} {{ __('eventos gratis') }}</small>
						</div>
						<Crown v-if="access?.is_plus" class="size-5 gold" />
						<LockKeyhole v-else class="size-5 muted-icon" />
					</section>

					<form class="event-form" @submit.prevent="saveEvent">
						<div class="form-head">
							<div>
								<strong>{{ editingEvent ? __('Editar evento') : __('Crear evento') }}</strong>
								<small>{{ __('Vinculalo con una Sesion IA si corresponde.') }}</small>
							</div>
							<button v-if="editingEvent" type="button" class="icon-button" :title="__('Cancelar')" @click="resetDraft">
								<X class="size-4" />
							</button>
						</div>

						<label>
							<span>{{ __('Titulo') }}</span>
							<input v-model="draft.title" required :placeholder="__('Examen de Matematica Basica')" />
						</label>

						<div class="two-cols">
							<label>
								<span>{{ __('Tipo') }}</span>
								<select v-model="draft.event_type">
									<option v-for="type in eventTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
								</select>
							</label>
							<label>
								<span>{{ __('Curso') }}</span>
								<input v-model="draft.subject" :placeholder="__('Matematica Basica')" />
							</label>
						</div>

						<label>
							<span>{{ __('Tema especifico') }}</span>
							<input v-model="draft.topic" :placeholder="__('Matrices y metodo de Gauss')" />
						</label>

						<div class="two-cols">
							<label>
								<span>{{ __('Inicio') }}</span>
								<input v-model="draft.start_datetime" type="datetime-local" required />
							</label>
							<label>
								<span>{{ __('Fin') }}</span>
								<input v-model="draft.end_datetime" type="datetime-local" />
							</label>
						</div>

						<div class="two-cols">
							<label>
								<span>{{ __('Dificultad') }}</span>
								<select v-model="draft.difficulty">
									<option value="low">{{ __('Baja') }}</option>
									<option value="medium">{{ __('Media') }}</option>
									<option value="high">{{ __('Alta') }}</option>
								</select>
							</label>
							<label>
								<span>{{ __('Importancia') }}</span>
								<select v-model="draft.importance">
									<option value="low">{{ __('Baja') }}</option>
									<option value="medium">{{ __('Media') }}</option>
									<option value="high">{{ __('Alta') }}</option>
								</select>
							</label>
						</div>

						<label>
							<span>{{ __('Sesion IA vinculada') }}</span>
							<select v-model="draft.linked_ai_session">
								<option value="">{{ __('Sin vincular') }}</option>
								<option v-for="session in sessions" :key="session.name" :value="session.name">
									{{ session.title || session.name }}
								</option>
							</select>
						</label>

						<div class="reminder-row">
							<label class="check-row">
								<input v-model="draft.reminder_enabled" type="checkbox" />
								<span>{{ __('Recordatorio') }}</span>
							</label>
							<select v-model="draft.reminder_time" :disabled="!draft.reminder_enabled">
								<option value="same_day">{{ __('Mismo dia') }}</option>
								<option value="night_before">{{ __('Noche anterior') }}</option>
								<option value="1_day_before">{{ __('1 dia antes') }}</option>
								<option value="2_days_before">{{ __('2 dias antes') }}</option>
							</select>
						</div>

						<button class="primary-button full" :disabled="saving || (!access?.can_create_event && !editingEvent)">
							<Save class="size-4" />
							<span>{{ saving ? __('Guardando...') : editingEvent ? __('Guardar cambios') : __('Crear evento') }}</span>
						</button>
					</form>

					<section class="upcoming-panel">
						<div class="section-head compact-head">
							<strong>{{ __('Proximos eventos') }}</strong>
							<small>{{ upcomingEvents.length }}</small>
						</div>
						<div class="upcoming-list">
							<button v-for="event in upcomingEvents" :key="event.name" class="upcoming-item" @click="focusEvent(event)">
								<span :class="['type-pill', event.event_type]">{{ eventTypeLabel(event.event_type) }}</span>
								<strong>{{ event.title }}</strong>
								<small>{{ formatDateTime(event.start_datetime) }}</small>
							</button>
							<div v-if="!upcomingEvents.length" class="empty-small">{{ __('Nada pendiente por ahora.') }}</div>
						</div>
					</section>
				</aside>
			</div>
		</template>
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
	Flag,
	Loader2,
	LockKeyhole,
	MessagesSquare,
	Pencil,
	Plus,
	RefreshCw,
	Save,
	Sparkles,
	Trash2,
	Wand2,
	X,
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
const selectedDate = ref(dateKey(new Date()))
const monthCursor = ref(startOfMonth(new Date()))

const eventTypes = [
	{ value: 'exam', label: __('Examen') },
	{ value: 'task', label: __('Tarea') },
	{ value: 'delivery', label: __('Entrega') },
	{ value: 'class', label: __('Clase') },
	{ value: 'practice', label: __('Practica') },
	{ value: 'reminder', label: __('Recordatorio') },
]

const weekdays = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']

const draft = ref(makeDraft())

usePageMeta(() => ({ title: __('Calendario Inteligente'), icon: brand.favicon }))

onMounted(loadDashboard)

watch(
	() => draft.value.linked_ai_session,
	(sessionName) => {
		const session = sessions.value.find((item) => item.name === sessionName)
		if (!session) return
		if (!draft.value.subject) draft.value.subject = session.academic_context || ''
		if (!draft.value.topic) draft.value.topic = session.goal || session.desired_topics || ''
		if (!draft.value.title) draft.value.title = `${eventTypeLabel(draft.value.event_type)} - ${session.title || session.name}`
	}
)

const eventsByDay = computed(() => {
	return events.value.reduce((map, event) => {
		const key = dateKey(parseDate(event.start_datetime))
		if (!map[key]) map[key] = []
		map[key].push(event)
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

function applyRouteDraft() {
	const sessionName = route.query.session
	if (!sessionName) return
	const session = sessions.value.find((item) => item.name === sessionName)
	const eventType = route.query.type || 'exam'
	draft.value = {
		...makeDraft(),
		linked_ai_session: sessionName,
		title: session ? `${eventTypeLabel(eventType)} - ${session.title || session.name}` : '',
		subject: session?.academic_context || '',
		topic: session?.goal || session?.desired_topics || '',
		event_type: eventType,
	}
	if (route.query.date) {
		draft.value.start_datetime = `${route.query.date}T09:00`
		draft.value.end_datetime = `${route.query.date}T10:00`
	}
}

function makeDraft(date = new Date(Date.now() + 24 * 60 * 60 * 1000)) {
	const start = roundToHour(date)
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

function startCreate(date) {
	editingEvent.value = null
	draft.value = makeDraft(date ? parseDate(`${date} 09:00:00`) : undefined)
}

function editEvent(event) {
	editingEvent.value = event
	draft.value = {
		title: event.title || '',
		event_type: event.event_type || 'exam',
		subject: event.subject || '',
		topic: event.topic || '',
		difficulty: event.difficulty || 'medium',
		importance: event.importance || 'medium',
		start_datetime: formatInputDate(parseDate(event.start_datetime)),
		end_datetime: formatInputDate(parseDate(event.end_datetime || event.start_datetime)),
		linked_ai_session: event.linked_ai_session || '',
		reminder_enabled: !!event.reminder_enabled,
		reminder_time: event.reminder_time || '1_day_before',
	}
}

function resetDraft() {
	editingEvent.value = null
	draft.value = makeDraft()
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
		resetDraft()
		const data = await api('get_calendar_dashboard')
		access.value = data.access
		events.value = data.events || []
		coachMessage.value = data.coach_message
	} finally {
		saving.value = false
	}
}

async function removeEvent(event) {
	if (!confirm(__('Eliminar este evento del calendario?'))) return
	await api('delete_study_calendar_event', { event: event.name })
	toast.success(__('Evento eliminado.'))
	const data = await api('get_calendar_dashboard')
	access.value = data.access
	events.value = data.events || []
	coachMessage.value = data.coach_message
	if (editingEvent.value?.name === event.name) resetDraft()
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

function selectDay(key) {
	selectedDate.value = key
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

function importanceLabel(value) {
	return {
		low: __('Baja'),
		medium: __('Media'),
		high: __('Alta'),
	}[value] || __('Media')
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
	return new Date(String(value || '').replace(' ', 'T'))
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
	min-height: 100vh;
	background: #f5f8fc;
	color: #0f172a;
	padding: 1.5rem;
}

.calendar-header,
.coach-strip,
.calendar-layout {
	max-width: 1440px;
	margin: 0 auto;
}

.calendar-header {
	display: flex;
	align-items: flex-end;
	justify-content: space-between;
	gap: 1rem;
	padding: 0.8rem 0 1rem;
}

.eyebrow,
.event-meta span,
.type-pill,
.event-title-line span {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
}

.eyebrow {
	width: fit-content;
	border: 1px solid #f1c95b;
	border-radius: 999px;
	background: #fff8dd;
	color: #8a5c00;
	padding: 0.35rem 0.65rem;
	font-size: 0.76rem;
	font-weight: 800;
}

.calendar-header h1 {
	margin: 0.65rem 0 0.2rem;
	font-size: clamp(2rem, 4vw, 3.4rem);
	line-height: 1;
	letter-spacing: 0;
}

.calendar-header p,
.coach-copy p,
.event-body p,
.event-meta,
.planner-panel small,
.month-toolbar small,
.section-head small,
.empty-day,
.empty-small {
	color: #64748b;
}

.header-actions,
.row-actions,
.section-head,
.month-toolbar,
.reminder-row {
	display: flex;
	align-items: center;
	gap: 0.7rem;
}

.primary-button,
.secondary-button,
.icon-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.45rem;
	border: 1px solid transparent;
	border-radius: 8px;
	font-weight: 800;
	line-height: 1;
	transition: 0.18s ease;
}

.primary-button {
	min-height: 42px;
	background: #0a2251;
	color: white;
	padding: 0 1rem;
}

.primary-button:hover:not(:disabled) {
	background: #12356e;
}

.secondary-button,
.icon-button {
	background: white;
	border-color: #dbe5f0;
	color: #0f172a;
}

.icon-button.danger {
	color: #b91c1c;
}

.icon-button.danger:hover {
	border-color: #fecaca;
	background: #fef2f2;
}

.secondary-button {
	min-height: 40px;
	padding: 0 0.9rem;
}

.icon-button {
	width: 40px;
	height: 40px;
	padding: 0;
}

.primary-button:disabled,
.secondary-button:disabled {
	opacity: 0.55;
	cursor: not-allowed;
}

.full {
	width: 100%;
}

.compact {
	min-height: 34px;
	padding: 0 0.7rem;
	font-size: 0.82rem;
}

.coach-strip {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr) auto;
	align-items: center;
	gap: 0.85rem;
	border: 1px solid #dbe5f0;
	border-radius: 8px;
	background: white;
	padding: 1rem;
	box-shadow: 0 14px 32px rgba(15, 23, 42, 0.06);
}

.coach-icon {
	display: grid;
	width: 42px;
	height: 42px;
	place-items: center;
	border-radius: 8px;
	background: #fff4bf;
	color: #8a5c00;
}

.coach-copy strong,
.event-body strong,
.form-head strong,
.plan-status strong,
.section-head strong,
.month-toolbar strong,
.upcoming-item strong {
	color: #0f172a;
}

.coach-copy p {
	margin: 0.2rem 0 0;
	line-height: 1.55;
}

.plus-link {
	text-decoration: none;
}

.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 0.6rem;
	min-height: 48vh;
	color: #64748b;
}

.spin {
	animation: spin 0.9s linear infinite;
}

.calendar-layout {
	display: grid;
	grid-template-columns: minmax(0, 1fr) minmax(340px, 420px);
	gap: 1rem;
	margin-top: 1rem;
}

.calendar-main,
.planner-panel {
	min-width: 0;
}

.month-toolbar {
	justify-content: space-between;
	border: 1px solid #dbe5f0;
	border-radius: 8px;
	background: white;
	padding: 0.75rem;
}

.month-toolbar > div {
	display: grid;
	text-align: center;
}

.calendar-grid {
	display: grid;
	grid-template-columns: repeat(7, minmax(0, 1fr));
	gap: 1px;
	overflow: hidden;
	border: 1px solid #dbe5f0;
	border-radius: 8px;
	background: #dbe5f0;
	margin-top: 0.75rem;
}

.weekday {
	background: #eef3f8;
	color: #475569;
	font-size: 0.72rem;
	font-weight: 900;
	padding: 0.55rem;
	text-align: center;
	text-transform: uppercase;
}

.day-cell {
	display: grid;
	align-content: start;
	gap: 0.45rem;
	min-height: 118px;
	border: 0;
	background: white;
	padding: 0.6rem;
	text-align: left;
	cursor: pointer;
}

.day-cell:hover,
.day-cell.selected {
	background: #f8fbff;
	outline: 2px solid #0a2251;
	outline-offset: -2px;
}

.day-cell.muted {
	background: #f8fafc;
	color: #94a3b8;
}

.day-cell.today .day-number {
	background: #0a2251;
	color: white;
}

.day-number {
	display: grid;
	width: 28px;
	height: 28px;
	place-items: center;
	border-radius: 8px;
	font-size: 0.82rem;
	font-weight: 900;
}

.day-events {
	display: grid;
	gap: 0.28rem;
	min-width: 0;
}

.event-dot {
	overflow: hidden;
	border-radius: 6px;
	padding: 0.25rem 0.35rem;
	font-size: 0.7rem;
	font-weight: 800;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.event-dot.exam,
.type-mark.exam,
.type-pill.exam {
	background: #fee2e2;
	color: #991b1b;
}

.event-dot.task,
.type-mark.task,
.type-pill.task {
	background: #dbeafe;
	color: #1e3a8a;
}

.event-dot.delivery,
.type-mark.delivery,
.type-pill.delivery {
	background: #fef3c7;
	color: #92400e;
}

.event-dot.class,
.type-mark.class,
.type-pill.class {
	background: #dcfce7;
	color: #166534;
}

.event-dot.practice,
.type-mark.practice,
.type-pill.practice {
	background: #ede9fe;
	color: #5b21b6;
}

.event-dot.reminder,
.type-mark.reminder,
.type-pill.reminder {
	background: #e0f2fe;
	color: #075985;
}

.day-agenda,
.event-form,
.plan-status,
.upcoming-panel {
	border: 1px solid #dbe5f0;
	border-radius: 8px;
	background: white;
}

.day-agenda {
	margin-top: 0.75rem;
	padding: 1rem;
}

.section-head {
	justify-content: space-between;
}

.section-head > div,
.form-head > div,
.plan-status > div {
	display: grid;
	gap: 0.2rem;
}

.event-list {
	display: grid;
	gap: 0.6rem;
	margin-top: 0.85rem;
}

.event-row {
	display: grid;
	grid-template-columns: 8px minmax(0, 1fr) auto;
	gap: 0.75rem;
	border: 1px solid #e3ebf4;
	border-radius: 8px;
	padding: 0.75rem;
}

.type-mark {
	width: 8px;
	border-radius: 999px;
}

.event-body {
	min-width: 0;
}

.event-title-line {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.6rem;
}

.event-title-line span,
.type-pill {
	border-radius: 999px;
	padding: 0.22rem 0.5rem;
	font-size: 0.68rem;
	font-weight: 900;
}

.event-body p {
	margin: 0.25rem 0 0;
}

.event-meta {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
	margin-top: 0.5rem;
	font-size: 0.76rem;
	font-weight: 750;
}

.empty-day,
.empty-small {
	display: flex;
	align-items: center;
	gap: 0.45rem;
	padding: 1rem 0;
	font-weight: 750;
}

.planner-panel {
	display: grid;
	align-content: start;
	gap: 0.85rem;
}

.plan-status {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 0.85rem;
}

.gold {
	color: #b7791f;
}

.muted-icon {
	color: #94a3b8;
}

.event-form {
	display: grid;
	gap: 0.75rem;
	padding: 1rem;
}

.form-head {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 0.8rem;
}

.event-form label {
	display: grid;
	gap: 0.35rem;
}

.event-form label > span,
.check-row span {
	color: #475569;
	font-size: 0.78rem;
	font-weight: 900;
}

.event-form input,
.event-form select {
	width: 100%;
	min-height: 40px;
	border: 1px solid #dbe5f0;
	border-radius: 8px;
	background: #f8fafc;
	color: #0f172a;
	padding: 0 0.7rem;
	font: inherit;
}

.two-cols {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 0.65rem;
}

.check-row {
	display: inline-flex !important;
	grid-template-columns: auto 1fr;
	align-items: center;
	gap: 0.45rem !important;
}

.check-row input {
	width: 16px;
	min-height: 16px;
}

.reminder-row {
	justify-content: space-between;
}

.reminder-row select {
	max-width: 190px;
}

.upcoming-panel {
	padding: 1rem;
}

.compact-head {
	margin-bottom: 0.65rem;
}

.upcoming-list {
	display: grid;
	gap: 0.5rem;
}

.upcoming-item {
	display: grid;
	gap: 0.25rem;
	border: 1px solid #e3ebf4;
	border-radius: 8px;
	background: #f8fafc;
	padding: 0.7rem;
	text-align: left;
}

.upcoming-item:hover {
	border-color: #0a2251;
	background: white;
}

.upcoming-item .type-pill {
	width: fit-content;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

@media (max-width: 1100px) {
	.calendar-layout {
		grid-template-columns: 1fr;
	}
}

@media (max-width: 760px) {
	.study-calendar-page {
		padding: 0.9rem;
	}

	.calendar-header,
	.coach-strip {
		align-items: stretch;
		grid-template-columns: 1fr;
	}

	.calendar-header {
		display: grid;
	}

	.header-actions {
		justify-content: space-between;
	}

	.calendar-grid {
		grid-template-columns: repeat(1, minmax(0, 1fr));
	}

	.weekday {
		display: none;
	}

	.day-cell {
		min-height: auto;
	}

	.day-cell.muted {
		display: none;
	}

	.two-cols {
		grid-template-columns: 1fr;
	}

	.event-row {
		grid-template-columns: 8px minmax(0, 1fr);
	}

	.row-actions {
		grid-column: 2;
	}
}
</style>

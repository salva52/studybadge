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
/* ─── Base ─────────────────────────────────────────────────── */
.study-calendar-page {
	height: 100vh;
	overflow: hidden;
	display: grid;
	grid-template-rows: auto auto 1fr;
	gap: 0;
	background: #f9fafb;
	color: #111827;
	font-size: 0.875rem;
	padding: 1rem 1.25rem;
	box-sizing: border-box;
}

/* ─── Header ────────────────────────────────────────────────── */
.calendar-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	padding-bottom: 0.75rem;
	max-width: 1440px;
	width: 100%;
	margin: 0 auto;
}

.eyebrow {
	display: inline-flex;
	align-items: center;
	gap: 0.3rem;
	font-size: 0.7rem;
	font-weight: 700;
	letter-spacing: 0.06em;
	text-transform: uppercase;
	color: #92400e;
	background: #fef3c7;
	border: 1px solid #fde68a;
	border-radius: 4px;
	padding: 0.2rem 0.55rem;
	margin-bottom: 0.35rem;
}

.calendar-header h1 {
	margin: 0;
	font-size: clamp(1.25rem, 2.5vw, 1.75rem);
	font-weight: 700;
	letter-spacing: -0.03em;
	line-height: 1.1;
	color: #111827;
}

.calendar-header p {
	margin: 0.15rem 0 0;
	color: #6b7280;
	font-size: 0.78rem;
}

.header-actions {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	flex-shrink: 0;
}

/* ─── Coach Strip ───────────────────────────────────────────── */
.coach-strip {
	display: grid;
	grid-template-columns: 36px minmax(0, 1fr) auto;
	align-items: center;
	gap: 0.75rem;
	background: white;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
	padding: 0.65rem 0.9rem;
	margin-bottom: 0.75rem;
	max-width: 1440px;
	width: 100%;
	margin-left: auto;
	margin-right: auto;
}

.coach-icon {
	display: grid;
	width: 36px;
	height: 36px;
	place-items: center;
	border-radius: 6px;
	background: #fef9ee;
	color: #92400e;
	border: 1px solid #fde68a;
	flex-shrink: 0;
}

.coach-copy strong {
	font-size: 0.78rem;
	font-weight: 700;
	color: #111827;
}

.coach-copy p {
	margin: 0.1rem 0 0;
	font-size: 0.75rem;
	color: #6b7280;
	line-height: 1.4;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

/* ─── Buttons ───────────────────────────────────────────────── */
.primary-button,
.secondary-button,
.icon-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.35rem;
	border: 1px solid transparent;
	border-radius: 6px;
	font-weight: 600;
	font-size: 0.8rem;
	line-height: 1;
	cursor: pointer;
	transition: background 0.12s, border-color 0.12s, opacity 0.12s;
	white-space: nowrap;
}

.primary-button {
	height: 34px;
	background: #111827;
	color: white;
	padding: 0 0.85rem;
}

.primary-button:hover:not(:disabled) {
	background: #1f2937;
}

.secondary-button {
	height: 34px;
	background: white;
	border-color: #d1d5db;
	color: #374151;
	padding: 0 0.85rem;
}

.secondary-button:hover:not(:disabled) {
	background: #f9fafb;
	border-color: #9ca3af;
}

.icon-button {
	width: 34px;
	height: 34px;
	background: white;
	border-color: #d1d5db;
	color: #374151;
	padding: 0;
}

.icon-button:hover {
	background: #f3f4f6;
}

.icon-button.danger {
	color: #dc2626;
}

.icon-button.danger:hover {
	background: #fef2f2;
	border-color: #fca5a5;
}

.primary-button:disabled,
.secondary-button:disabled {
	opacity: 0.45;
	cursor: not-allowed;
}

.full {
	width: 100%;
}

.compact {
	height: 30px;
	padding: 0 0.6rem;
	font-size: 0.76rem;
}

.plus-link {
	text-decoration: none;
}

/* ─── Loading ───────────────────────────────────────────────── */
.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	color: #9ca3af;
	font-size: 0.8rem;
}

.spin {
	animation: spin 0.9s linear infinite;
}

/* ─── Layout ────────────────────────────────────────────────── */
.calendar-layout {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 340px;
	gap: 0.75rem;
	max-width: 1440px;
	width: 100%;
	margin: 0 auto;
	min-height: 0;
	overflow: hidden;
}

.calendar-main {
	display: grid;
	grid-template-rows: auto auto 1fr;
	gap: 0.5rem;
	min-height: 0;
	overflow: hidden;
}

.planner-panel {
	display: grid;
	grid-template-rows: auto 1fr auto;
	gap: 0.5rem;
	min-height: 0;
	overflow: hidden;
}

/* ─── Month Toolbar ─────────────────────────────────────────── */
.month-toolbar {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
	background: white;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
	padding: 0.5rem 0.75rem;
}

.month-toolbar > div {
	text-align: center;
}

.month-toolbar strong {
	display: block;
	font-size: 0.85rem;
	font-weight: 700;
	color: #111827;
	text-transform: capitalize;
}

.month-toolbar small {
	font-size: 0.68rem;
	color: #9ca3af;
}

/* ─── Calendar Grid ─────────────────────────────────────────── */
.calendar-grid {
	display: grid;
	grid-template-columns: repeat(7, minmax(0, 1fr));
	gap: 1px;
	background: #e5e7eb;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
	overflow: hidden;
}

.weekday {
	background: #f3f4f6;
	color: #9ca3af;
	font-size: 0.65rem;
	font-weight: 700;
	letter-spacing: 0.06em;
	text-transform: uppercase;
	padding: 0.4rem;
	text-align: center;
}

.day-cell {
	display: grid;
	align-content: start;
	gap: 0.2rem;
	background: white;
	padding: 0.4rem;
	text-align: left;
	cursor: pointer;
	border: 0;
	min-height: 0;
	transition: background 0.1s;
}

.day-cell:hover {
	background: #f9fafb;
}

.day-cell.selected {
	background: #f0f9ff;
	outline: 2px solid #111827;
	outline-offset: -2px;
}

.day-cell.muted {
	background: #fafafa;
	color: #d1d5db;
}

.day-cell.today .day-number {
	background: #111827;
	color: white;
}

.day-number {
	display: grid;
	width: 22px;
	height: 22px;
	place-items: center;
	border-radius: 4px;
	font-size: 0.72rem;
	font-weight: 700;
}

.day-events {
	display: grid;
	gap: 0.15rem;
	min-width: 0;
}

.event-dot {
	overflow: hidden;
	border-radius: 3px;
	padding: 0.12rem 0.3rem;
	font-size: 0.6rem;
	font-weight: 600;
	text-overflow: ellipsis;
	white-space: nowrap;
}

/* ─── Day Agenda ────────────────────────────────────────────── */
.day-agenda {
	background: white;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
	padding: 0.75rem;
	min-height: 0;
	overflow-y: auto;
}

.section-head {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
}

.section-head > div,
.form-head > div,
.plan-status > div {
	display: grid;
	gap: 0.1rem;
}

.section-head strong,
.form-head strong,
.plan-status strong {
	font-size: 0.82rem;
	font-weight: 700;
	color: #111827;
}

.section-head small,
.form-head small,
.month-toolbar small,
.planner-panel small {
	font-size: 0.68rem;
	color: #9ca3af;
}

.event-list {
	display: grid;
	gap: 0.45rem;
	margin-top: 0.65rem;
}

.event-row {
	display: grid;
	grid-template-columns: 3px minmax(0, 1fr) auto;
	gap: 0.6rem;
	border: 1px solid #f3f4f6;
	border-radius: 6px;
	padding: 0.6rem;
	align-items: start;
}

.type-mark {
	width: 3px;
	border-radius: 999px;
	align-self: stretch;
}

.event-body {
	min-width: 0;
}

.event-title-line {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
}

.event-title-line strong {
	font-size: 0.8rem;
	font-weight: 600;
	color: #111827;
}

.event-title-line span,
.type-pill {
	border-radius: 3px;
	padding: 0.15rem 0.4rem;
	font-size: 0.62rem;
	font-weight: 700;
	letter-spacing: 0.03em;
}

.event-body p {
	margin: 0.2rem 0 0;
	font-size: 0.72rem;
	color: #6b7280;
}

.event-meta {
	display: flex;
	flex-wrap: wrap;
	gap: 0.4rem;
	margin-top: 0.35rem;
	font-size: 0.68rem;
	color: #9ca3af;
}

.event-meta span {
	display: inline-flex;
	align-items: center;
	gap: 0.2rem;
}

.row-actions {
	display: flex;
	align-items: center;
	gap: 0.3rem;
}

.empty-day,
.empty-small {
	display: flex;
	align-items: center;
	gap: 0.4rem;
	padding: 0.75rem 0;
	color: #9ca3af;
	font-size: 0.76rem;
}

/* ─── Plan Status ───────────────────────────────────────────── */
.plan-status {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 0.65rem 0.75rem;
	background: white;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
}

.gold {
	color: #d97706;
}

.muted-icon {
	color: #d1d5db;
}

/* ─── Event Form ────────────────────────────────────────────── */
.event-form {
	display: grid;
	gap: 0.5rem;
	padding: 0.75rem;
	background: white;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
	overflow-y: auto;
	min-height: 0;
}

.form-head {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 0.6rem;
}

.event-form label {
	display: grid;
	gap: 0.25rem;
}

.event-form label > span,
.check-row span {
	font-size: 0.7rem;
	font-weight: 600;
	color: #6b7280;
	letter-spacing: 0.02em;
	text-transform: uppercase;
}

.event-form input,
.event-form select {
	width: 100%;
	height: 32px;
	border: 1px solid #e5e7eb;
	border-radius: 5px;
	background: #f9fafb;
	color: #111827;
	padding: 0 0.6rem;
	font: inherit;
	font-size: 0.8rem;
	transition: border-color 0.12s;
	box-sizing: border-box;
}

.event-form input:focus,
.event-form select:focus {
	outline: none;
	border-color: #6b7280;
	background: white;
}

.two-cols {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 0.45rem;
}

.check-row {
	display: inline-flex !important;
	align-items: center;
	gap: 0.4rem !important;
}

.check-row input {
	width: 14px;
	min-height: 14px;
}

.reminder-row {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
}

.reminder-row select {
	max-width: 160px;
}

/* ─── Upcoming Panel ────────────────────────────────────────── */
.upcoming-panel {
	padding: 0.65rem 0.75rem;
	background: white;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
	min-height: 0;
	overflow-y: auto;
}

.compact-head {
	display: flex;
	align-items: center;
	justify-content: space-between;
	margin-bottom: 0.5rem;
}

.compact-head strong {
	font-size: 0.78rem;
	font-weight: 700;
	color: #111827;
}

.compact-head small {
	font-size: 0.68rem;
	background: #f3f4f6;
	color: #6b7280;
	border-radius: 999px;
	padding: 0.1rem 0.45rem;
}

.upcoming-list {
	display: grid;
	gap: 0.35rem;
}

.upcoming-item {
	display: grid;
	gap: 0.18rem;
	border: 1px solid #f3f4f6;
	border-radius: 6px;
	background: #fafafa;
	padding: 0.5rem 0.6rem;
	text-align: left;
	cursor: pointer;
	transition: border-color 0.12s, background 0.12s;
}

.upcoming-item:hover {
	border-color: #d1d5db;
	background: white;
}

.upcoming-item .type-pill {
	width: fit-content;
}

.upcoming-item strong {
	font-size: 0.76rem;
	font-weight: 600;
	color: #111827;
}

.upcoming-item small {
	font-size: 0.67rem;
	color: #9ca3af;
}

/* ─── Event Type Colors ─────────────────────────────────────── */
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
	color: #1e40af;
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

/* ─── Animations ────────────────────────────────────────────── */
@keyframes spin {
	to { transform: rotate(360deg); }
}

/* ─── Tablet ────────────────────────────────────────────────── */
@media (max-width: 1100px) {
	.study-calendar-page {
		height: auto;
		overflow: auto;
		grid-template-rows: auto auto auto;
	}

	.calendar-layout {
		grid-template-columns: 1fr;
		overflow: visible;
	}

	.calendar-main {
		overflow: visible;
	}

	.planner-panel {
		grid-template-rows: auto auto auto;
		overflow: visible;
	}

	.day-agenda,
	.event-form,
	.upcoming-panel {
		overflow: visible;
	}
}

/* ─── Mobile ────────────────────────────────────────────────── */
@media (max-width: 640px) {
	.study-calendar-page {
		padding: 0.75rem;
		gap: 0;
	}

	.calendar-header {
		flex-wrap: wrap;
		padding-bottom: 0.6rem;
	}

	.calendar-header h1 {
		font-size: 1.2rem;
	}

	.header-actions {
		width: 100%;
		justify-content: space-between;
	}

	.coach-strip {
		grid-template-columns: 36px minmax(0, 1fr);
		gap: 0.6rem;
	}

	.coach-strip > .secondary-button,
	.coach-strip > .router-link {
		grid-column: 1 / -1;
		width: 100%;
	}

	.coach-copy p {
		white-space: normal;
		overflow: visible;
	}

	.calendar-layout {
		gap: 0.6rem;
	}

	.calendar-grid {
		grid-template-columns: repeat(7, minmax(0, 1fr));
	}

	.day-cell {
		min-height: 42px;
		padding: 0.3rem;
	}

	.day-events {
		display: none;
	}

	.weekday {
		font-size: 0.6rem;
		padding: 0.3rem 0.2rem;
	}

	.two-cols {
		grid-template-columns: 1fr;
	}

	.event-row {
		grid-template-columns: 3px minmax(0, 1fr);
	}

	.row-actions {
		grid-column: 2;
	}

	.month-toolbar {
		padding: 0.45rem 0.6rem;
	}

	.plan-status {
		padding: 0.5rem 0.65rem;
	}
}
</style>
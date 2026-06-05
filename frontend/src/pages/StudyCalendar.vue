<template>
	<div class="study-calendar-page">
		<header class="calendar-header">
			<div class="header-copy">
				<span class="header-kicker">{{ __('Coach IA Plus') }}</span>
				<h1>{{ __('Calendario Inteligente') }}</h1>
				<p>{{ __('Organiza sesiones, examenes, tareas y recordatorios desde un solo panel.') }}</p>
			</div>

			<div class="header-actions">
				<button class="icon-button" :title="__('Recargar')" @click="loadDashboard">
					<RefreshCw class="size-4" />
				</button>
				<button class="primary-button" @click="startCreate()">
					<Plus class="size-4" />
					<span>{{ __('Nuevo evento') }}</span>
				</button>
			</div>
		</header>

		<section class="coach-strip">
			<div class="coach-icon">
				<Sparkles class="size-4" />
			</div>
			<div class="coach-copy">
				<strong>{{ __('Mi guia de estudio') }}</strong>
				<p>{{ generatedMessage || coachMessage?.message || __('Crea o vincula un evento para recibir una recomendacion de estudio.') }}</p>
			</div>
			<button
				v-if="access?.is_plus"
				class="secondary-button"
				:disabled="!nextEvent || generating"
				@click="generateCoachMessage(nextEvent)"
			>
				<Wand2 class="size-4" />
				<span>{{ generating ? __('Generando...') : __('Generar IA') }}</span>
			</button>
			<router-link v-else :to="{ name: 'Plus' }" class="secondary-button plus-link">
				<Crown class="size-4" />
				<span>{{ __('Activar Plus') }}</span>
			</router-link>
		</section>

		<div v-if="loading" class="loading-state">
			<Loader2 class="size-5 spin" />
			<span>{{ __('Cargando calendario...') }}</span>
		</div>

		<template v-else>
			<div class="calendar-layout">
				<main class="calendar-main">
					<div class="month-toolbar">
						<button class="icon-button" :title="__('Mes anterior')" @click="moveMonth(-1)">
							<ChevronLeft class="size-4" />
						</button>
						<div class="month-title">
							<strong>{{ monthLabel }}</strong>
							<small>{{ visibleEvents.length }} {{ __('eventos') }}</small>
						</div>
						<button class="icon-button" :title="__('Mes siguiente')" @click="moveMonth(1)">
							<ChevronRight class="size-4" />
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
								<span
									v-for="event in eventsByDay[cell.key]?.slice(0, 2)"
									:key="event.name"
									:class="['event-dot', event.event_type]"
								>
									{{ event.title }}
								</span>
								<span v-if="eventsByDay[cell.key]?.length > 2" class="event-more">
									+{{ eventsByDay[cell.key].length - 2 }}
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
										<Bot class="size-4" />
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
							<CalendarDays class="size-4" />
							<span>{{ __('Agenda un examen, tarea o recordatorio de estudio.') }}</span>
						</div>
					</section>
				</main>

				<aside class="planner-panel">
					<section class="plan-status">
						<div>
							<strong>{{ access?.is_plus ? __('Plus activo') : __('Plan gratuito') }}</strong>
							<small v-if="access?.is_plus">{{ __('Coach IA y eventos ilimitados') }}</small>
							<small v-else>{{ access?.events_used || 0 }}/{{ access?.free_event_limit || 5 }} {{ __('eventos gratis') }}</small>
						</div>
						<Crown v-if="access?.is_plus" class="size-4 gold" />
						<LockKeyhole v-else class="size-4 muted-icon" />
					</section>

					<form class="event-form" @submit.prevent="saveEvent">
						<div class="form-head">
							<div>
								<strong>{{ editingEvent ? __('Editar evento') : __('Crear evento') }}</strong>
								<small>{{ __('Conectalo con una Sesion IA.') }}</small>
							</div>
							<button v-if="editingEvent" type="button" class="icon-button" :title="__('Cancelar')" @click="resetDraft">
								<X class="size-4" />
							</button>
						</div>

						<label class="field-wide">
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

						<label class="field-wide">
							<span>{{ __('Tema') }}</span>
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

						<button type="button" class="advanced-toggle" @click="showAdvanced = !showAdvanced">
							<Settings2 class="size-3.5" />
							<span>{{ showAdvanced ? __('Ocultar opciones') : __('Opciones opcionales') }}</span>
							<ChevronDown class="size-3.5" :style="{ marginLeft: 'auto', transition: 'transform 0.2s', transform: showAdvanced ? 'rotate(180deg)' : 'none' }" />
						</button>

						<div v-show="showAdvanced" class="advanced-fields">
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

							<label class="field-wide">
								<span>{{ __('Sesion IA') }}</span>
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
	ChevronDown,
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
	Settings2,
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
const showAdvanced = ref(false)
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
.advanced-toggle {
	display: flex;
	align-items: center;
	gap: 6px;
	width: 100%;
	background: #f8fafc;
	border: 1px dashed #cbd5e1;
	border-radius: 8px;
	padding: 8px 12px;
	color: #64748b;
	font-size: 0.8rem;
	font-weight: 600;
	cursor: pointer;
	margin-top: 4px;
	transition: all 0.2s;
}

.advanced-toggle:hover {
	background: #f1f5f9;
	color: #475569;
	border-color: #94a3b8;
}

.advanced-fields {
	display: flex;
	flex-direction: column;
	gap: 0.75rem;
	padding: 12px;
	background: #f8fafc;
	border: 1px solid #e2e8f0;
	border-radius: 8px;
	margin-top: -4px;
}

.study-calendar-page {
	height: 100vh;
	min-height: 720px;
	overflow: hidden;
	display: grid;
	grid-template-rows: auto auto minmax(0, 1fr);
	gap: 0.75rem;
	background: #f6f7f9;
	color: #101828;
	padding: 1rem;
}

.calendar-header,
.coach-strip,
.calendar-layout {
	width: min(1480px, 100%);
	margin: 0 auto;
}

.calendar-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	min-height: 64px;
}

.header-copy {
	min-width: 0;
}

.header-kicker {
	display: inline-flex;
	align-items: center;
	width: fit-content;
	border: 1px solid #d9dee7;
	border-radius: 999px;
	background: #ffffff;
	color: #475467;
	padding: 0.22rem 0.55rem;
	font-size: 0.7rem;
	font-weight: 700;
	letter-spacing: 0.01em;
}

.calendar-header h1 {
	margin: 0.3rem 0 0.1rem;
	font-size: clamp(1.45rem, 2.8vw, 2.3rem);
	line-height: 1.05;
	letter-spacing: -0.03em;
	color: #101828;
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
	color: #667085;
}

.calendar-header p {
	max-width: 620px;
	margin: 0;
	font-size: 0.88rem;
	line-height: 1.35;
}

.header-actions,
.row-actions,
.section-head,
.month-toolbar,
.reminder-row,
.event-meta span,
.type-pill,
.event-title-line span {
	display: flex;
	align-items: center;
	gap: 0.5rem;
}

.header-actions {
	flex-shrink: 0;
}

.primary-button,
.secondary-button,
.icon-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.45rem;
	border: 1px solid transparent;
	border-radius: 10px;
	font-weight: 700;
	line-height: 1;
	transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
}

.primary-button {
	min-height: 38px;
	background: #111827;
	color: #ffffff;
	padding: 0 0.9rem;
}

.primary-button:hover:not(:disabled) {
	background: #000000;
}

.secondary-button,
.icon-button {
	background: #ffffff;
	border-color: #d0d5dd;
	color: #101828;
}

.secondary-button:hover:not(:disabled),
.icon-button:hover {
	background: #f9fafb;
	border-color: #98a2b3;
}

.icon-button.danger {
	color: #b42318;
}

.icon-button.danger:hover {
	border-color: #fecdca;
	background: #fffbfa;
}

.secondary-button {
	min-height: 36px;
	padding: 0 0.75rem;
	font-size: 0.84rem;
}

.icon-button {
	width: 36px;
	height: 36px;
	padding: 0;
	flex: 0 0 auto;
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
	min-height: 32px;
	padding: 0 0.65rem;
	font-size: 0.8rem;
}

.plus-link {
	text-decoration: none;
}

.coach-strip {
	display: grid;
	grid-template-columns: auto minmax(0, 1fr) auto;
	align-items: center;
	gap: 0.75rem;
	border: 1px solid #d9dee7;
	border-radius: 14px;
	background: #ffffff;
	padding: 0.65rem 0.75rem;
	box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.coach-icon {
	display: grid;
	width: 34px;
	height: 34px;
	place-items: center;
	border-radius: 10px;
	background: #f2f4f7;
	color: #344054;
}

.coach-copy {
	min-width: 0;
}

.coach-copy strong,
.event-body strong,
.form-head strong,
.plan-status strong,
.section-head strong,
.month-toolbar strong,
.upcoming-item strong {
	color: #101828;
}

.coach-copy p {
	overflow: hidden;
	display: -webkit-box;
	margin: 0.12rem 0 0;
	font-size: 0.86rem;
	line-height: 1.35;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
}

.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 0.55rem;
	color: #667085;
}

.spin {
	animation: spin 0.9s linear infinite;
}

.calendar-layout {
	min-height: 0;
	display: grid;
	grid-template-columns: minmax(0, 1fr) minmax(330px, 390px);
	gap: 0.75rem;
}

.calendar-main,
.planner-panel {
	min-width: 0;
	min-height: 0;
}

.calendar-main {
	display: grid;
	grid-template-rows: auto minmax(300px, 1fr) minmax(118px, 0.38fr);
	gap: 0.75rem;
}

.month-toolbar {
	justify-content: space-between;
	border: 1px solid #d9dee7;
	border-radius: 14px;
	background: #ffffff;
	padding: 0.55rem;
	box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.month-title {
	display: grid;
	text-align: center;
	gap: 0.05rem;
	text-transform: capitalize;
}

.calendar-grid {
	min-height: 0;
	display: grid;
	grid-template-columns: repeat(7, minmax(0, 1fr));
	grid-auto-rows: minmax(0, 1fr);
	gap: 1px;
	overflow: hidden;
	border: 1px solid #d9dee7;
	border-radius: 14px;
	background: #e4e7ec;
	box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.weekday {
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 28px;
	background: #f2f4f7;
	color: #667085;
	font-size: 0.66rem;
	font-weight: 800;
	text-transform: uppercase;
}

.day-cell {
	position: relative;
	display: grid;
	grid-template-rows: auto minmax(0, 1fr);
	gap: 0.25rem;
	min-height: 0;
	border: 0;
	background: #ffffff;
	padding: 0.45rem;
	text-align: left;
	cursor: pointer;
}

.day-cell:hover,
.day-cell.selected {
	background: #f9fafb;
	outline: 2px solid #111827;
	outline-offset: -2px;
}

.day-cell.muted {
	background: #fbfcfe;
	color: #98a2b3;
}

.day-cell.today .day-number {
	background: #111827;
	color: #ffffff;
}

.day-number {
	display: grid;
	width: 24px;
	height: 24px;
	place-items: center;
	border-radius: 8px;
	font-size: 0.78rem;
	font-weight: 800;
}

.day-events {
	display: grid;
	align-content: start;
	gap: 0.2rem;
	min-width: 0;
	overflow: hidden;
}

.event-dot {
	overflow: hidden;
	border: 1px solid transparent;
	border-radius: 7px;
	padding: 0.16rem 0.3rem;
	font-size: 0.66rem;
	font-weight: 700;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.event-more {
	width: fit-content;
	border-radius: 999px;
	background: #f2f4f7;
	color: #475467;
	padding: 0.1rem 0.32rem;
	font-size: 0.66rem;
	font-weight: 800;
}

.event-dot.exam,
.type-mark.exam,
.type-pill.exam {
	background: #fef3f2;
	color: #b42318;
}

.event-dot.task,
.type-mark.task,
.type-pill.task {
	background: #eff8ff;
	color: #175cd3;
}

.event-dot.delivery,
.type-mark.delivery,
.type-pill.delivery {
	background: #fffaeb;
	color: #b54708;
}

.event-dot.class,
.type-mark.class,
.type-pill.class {
	background: #ecfdf3;
	color: #027a48;
}

.event-dot.practice,
.type-mark.practice,
.type-pill.practice {
	background: #f4f3ff;
	color: #5925dc;
}

.event-dot.reminder,
.type-mark.reminder,
.type-pill.reminder {
	background: #f0f9ff;
	color: #026aa2;
}

.day-agenda,
.event-form,
.plan-status,
.upcoming-panel {
	border: 1px solid #d9dee7;
	border-radius: 14px;
	background: #ffffff;
	box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.day-agenda {
	min-height: 0;
	display: grid;
	grid-template-rows: auto minmax(0, 1fr);
	padding: 0.75rem;
	overflow: hidden;
}

.section-head {
	justify-content: space-between;
	min-width: 0;
}

.section-head > div,
.form-head > div,
.plan-status > div {
	display: grid;
	gap: 0.12rem;
	min-width: 0;
}

.event-list {
	min-height: 0;
	display: grid;
	align-content: start;
	gap: 0.45rem;
	margin-top: 0.55rem;
	overflow: auto;
	padding-right: 0.15rem;
}

.event-row {
	display: grid;
	grid-template-columns: 7px minmax(0, 1fr) auto;
	gap: 0.55rem;
	border: 1px solid #eaecf0;
	border-radius: 12px;
	padding: 0.55rem;
}

.type-mark {
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

.event-title-line span,
.type-pill {
	border-radius: 999px;
	padding: 0.16rem 0.42rem;
	font-size: 0.64rem;
	font-weight: 800;
	white-space: nowrap;
}

.event-body p {
	overflow: hidden;
	margin: 0.18rem 0 0;
	font-size: 0.8rem;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.event-meta {
	flex-wrap: wrap;
	gap: 0.45rem;
	margin-top: 0.35rem;
	font-size: 0.72rem;
	font-weight: 700;
}

.row-actions {
	justify-content: flex-end;
	gap: 0.35rem;
}

.empty-day,
.empty-small {
	display: flex;
	align-items: center;
	gap: 0.45rem;
	padding: 0.65rem 0;
	font-size: 0.84rem;
	font-weight: 700;
}

.planner-panel {
	display: grid;
	grid-template-rows: auto minmax(0, 1fr) minmax(120px, 0.35fr);
	align-content: start;
	gap: 0.75rem;
}

.plan-status {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 0.65rem 0.75rem;
}

.gold {
	color: #b54708;
}

.muted-icon {
	color: #98a2b3;
}

.event-form {
	min-height: 0;
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	align-content: start;
	gap: 0.55rem;
	padding: 0.75rem;
	overflow: hidden;
}

.form-head,
.field-wide,
.reminder-row,
.event-form .full {
	grid-column: 1 / -1;
}

.form-head {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 0.6rem;
}

.event-form label {
	display: grid;
	gap: 0.26rem;
	min-width: 0;
}

.event-form label > span,
.check-row span {
	color: #475467;
	font-size: 0.7rem;
	font-weight: 800;
}

.event-form input,
.event-form select {
	width: 100%;
	min-height: 34px;
	border: 1px solid #d0d5dd;
	border-radius: 9px;
	background: #ffffff;
	color: #101828;
	padding: 0 0.6rem;
	font: inherit;
	font-size: 0.82rem;
	outline: none;
}

.event-form input:focus,
.event-form select:focus {
	border-color: #111827;
	box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.08);
}

.two-cols {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 0.55rem;
	grid-column: 1 / -1;
}

.check-row {
	display: inline-flex !important;
	grid-template-columns: auto 1fr;
	align-items: center;
	gap: 0.45rem !important;
}

.check-row input {
	width: 15px;
	min-height: 15px;
}

.reminder-row {
	justify-content: space-between;
	gap: 0.55rem;
}

.reminder-row select {
	max-width: 180px;
}

.upcoming-panel {
	min-height: 0;
	display: grid;
	grid-template-rows: auto minmax(0, 1fr);
	padding: 0.75rem;
	overflow: hidden;
}

.compact-head {
	margin-bottom: 0.45rem;
}

.upcoming-list {
	min-height: 0;
	display: grid;
	align-content: start;
	gap: 0.4rem;
	overflow: auto;
	padding-right: 0.15rem;
}

.upcoming-item {
	display: grid;
	gap: 0.18rem;
	border: 1px solid #eaecf0;
	border-radius: 10px;
	background: #ffffff;
	padding: 0.5rem;
	text-align: left;
}

.upcoming-item:hover {
	border-color: #111827;
	background: #f9fafb;
}

.upcoming-item .type-pill {
	width: fit-content;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

@media (max-width: 1180px) {
	.study-calendar-page {
		min-height: 820px;
		overflow: auto;
	}

	.calendar-layout {
		grid-template-columns: 1fr;
	}

	.calendar-main {
		grid-template-rows: auto minmax(360px, 46vh) minmax(120px, auto);
	}

	.planner-panel {
		grid-template-columns: minmax(0, 1fr) minmax(320px, 390px);
		grid-template-rows: auto minmax(0, auto);
	}

	.plan-status {
		grid-column: 1 / -1;
	}

	.event-form {
		grid-column: 1;
	}

	.upcoming-panel {
		grid-column: 2;
	}
}

@media (max-width: 760px) {
	.study-calendar-page {
		height: auto;
		min-height: 100dvh;
		padding: 0.75rem;
		gap: 0.6rem;
		overflow: auto;
	}

	.calendar-header {
		align-items: flex-start;
		gap: 0.7rem;
	}

	.calendar-header h1 {
		font-size: 1.45rem;
	}

	.calendar-header p {
		display: none;
	}

	.header-actions {
		gap: 0.45rem;
	}

	.primary-button {
		min-height: 36px;
		padding: 0 0.75rem;
	}

	.coach-strip {
		grid-template-columns: minmax(0, 1fr) auto;
		padding: 0.65rem;
	}

	.coach-icon {
		display: none;
	}

	.coach-copy p {
		-webkit-line-clamp: 1;
	}

	.calendar-layout {
		gap: 0.6rem;
	}

	.calendar-main {
		gap: 0.6rem;
		grid-template-rows: auto 300px minmax(104px, auto);
	}

	.month-toolbar,
	.day-agenda,
	.event-form,
	.plan-status,
	.upcoming-panel {
		border-radius: 12px;
	}

	.calendar-grid {
		border-radius: 12px;
	}

	.weekday {
		min-height: 24px;
		font-size: 0.58rem;
	}

	.day-cell {
		padding: 0.28rem;
		gap: 0.12rem;
	}

	.day-number {
		width: 20px;
		height: 20px;
		border-radius: 6px;
		font-size: 0.7rem;
	}

	.event-dot {
		max-width: 100%;
		padding: 0;
		border: 0;
		background: currentColor !important;
		color: currentColor !important;
		height: 5px;
		width: 5px;
		border-radius: 999px;
		text-indent: -999px;
	}

	.event-more {
		padding: 0;
		background: transparent;
		font-size: 0.58rem;
	}

	.day-agenda {
		padding: 0.65rem;
	}

	.event-row {
		grid-template-columns: 6px minmax(0, 1fr);
		gap: 0.45rem;
		padding: 0.5rem;
	}

	.row-actions {
		grid-column: 2;
		justify-content: flex-start;
	}

	.planner-panel {
		grid-template-columns: 1fr;
		grid-template-rows: auto auto auto;
		gap: 0.6rem;
	}

	.event-form {
		grid-template-columns: 1fr;
		padding: 0.65rem;
		gap: 0.5rem;
	}

	.two-cols {
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 0.45rem;
	}

	.event-form input,
	.event-form select {
		min-height: 33px;
		font-size: 0.8rem;
		padding: 0 0.45rem;
	}

	.reminder-row {
		align-items: center;
	}

	.reminder-row select {
		max-width: 165px;
	}

	.upcoming-panel {
		max-height: 180px;
	}
}

@media (max-width: 430px) {
	.header-kicker {
		display: none;
	}

	.calendar-header {
		min-height: auto;
	}

	.calendar-header h1 {
		margin: 0;
		font-size: 1.25rem;
	}

	.header-actions .primary-button span,
	.coach-strip .secondary-button span {
		display: none;
	}

	.coach-strip {
		grid-template-columns: minmax(0, 1fr) auto;
	}

	.calendar-main {
		grid-template-rows: auto 270px minmax(96px, auto);
	}

	.event-meta {
		gap: 0.3rem;
	}

	.two-cols {
		grid-template-columns: 1fr;
	}
}
</style>

<template>
	<div class="instructor-page">
		<header class="instructor-header">
			<div>
				<p>{{ __('Panel de instructor') }}</p>
				<h1>{{ pageTitle }}</h1>
			</div>
			<Button v-if="activeView === 'courses'" variant="solid" @click="newCourse">
				<template #prefix><Plus class="size-4" /></template>
				{{ __('Crear curso') }}
			</Button>
		</header>

		<nav class="instructor-tabs">
			<router-link v-for="item in nav" :key="item.to" :to="{ name: item.to }">
				<component :is="item.icon" class="size-4" />
				<span>{{ item.label }}</span>
			</router-link>
		</nav>

		<section v-if="loading" class="instructor-empty">{{ __('Cargando...') }}</section>

		<section v-else-if="activeView === 'dashboard'" class="instructor-grid">
			<div v-for="metric in metrics" :key="metric.label" class="metric-card">
				<span>{{ metric.label }}</span>
				<strong>{{ metric.value }}</strong>
			</div>
			<div class="panel-wide">
				<h2>{{ __('Últimas ventas') }}</h2>
				<DataTable :columns="saleColumns" :rows="dashboard.latest_sales || []" />
			</div>
			<div class="panel-wide">
				<h2>{{ __('Alertas de revisión') }}</h2>
				<DataTable :columns="reviewColumns" :rows="dashboard.latest_reviews || []" />
			</div>
		</section>

		<section v-else-if="activeView === 'courses'" class="panel-wide">
			<DataTable :columns="courseColumns" :rows="courses" />
		</section>

		<section v-else-if="activeView === 'sales'" class="panel-wide">
			<DataTable :columns="saleColumns" :rows="sales" />
		</section>

		<section v-else-if="activeView === 'students'" class="panel-wide">
			<DataTable :columns="studentColumns" :rows="students" />
		</section>

		<section v-else-if="activeView === 'wallet'" class="wallet-layout">
			<div class="wallet-summary">
				<div class="metric-card">
					<span>{{ __('Saldo disponible') }}</span>
					<strong>S/ {{ money(wallet.profile?.available_balance) }}</strong>
				</div>
				<div class="metric-card">
					<span>{{ __('Saldo pendiente') }}</span>
					<strong>S/ {{ money(wallet.profile?.pending_balance) }}</strong>
				</div>
				<div class="metric-card">
					<span>{{ __('Retirado') }}</span>
					<strong>S/ {{ money(wallet.profile?.withdrawn_balance) }}</strong>
				</div>
			</div>
			<p class="wallet-note">{{ __('Retiro mínimo: S/20. Tiempo máximo de retiro: 72 horas. Promedio estimado: 1-2 horas.') }}</p>
			<div class="panel-wide">
				<h2>{{ __('Movimientos') }}</h2>
				<DataTable :columns="ledgerColumns" :rows="wallet.ledger || []" />
			</div>
		</section>

		<section v-else-if="activeView === 'withdrawals'" class="wallet-layout">
			<form class="withdrawal-form" @submit.prevent="requestWithdrawal">
				<FormControl v-model="withdrawalAmount" :label="__('Monto a retirar')" type="number" />
				<Button variant="solid" :loading="saving" type="submit">{{ __('Solicitar retiro') }}</Button>
				<p>{{ __('Retiro mínimo: S/20. Tiempo máximo de retiro: 72 horas. Promedio estimado: 1-2 horas.') }}</p>
			</form>
			<div class="panel-wide">
				<DataTable :columns="withdrawalColumns" :rows="withdrawals" />
			</div>
		</section>

		<section v-else-if="activeView === 'payout'" class="payout-card">
			<form class="payout-form" @submit.prevent="savePayout">
				<div class="payout-grid">
					<FormControl v-model="payout.bank_name" :label="__('Banco')" required />
					<div>
						<label class="field-label">{{ __('Tipo de cuenta') }}</label>
						<select v-model="payout.account_type" class="select-field">
							<option value="Savings">{{ __('Ahorros') }}</option>
							<option value="Checking">{{ __('Corriente') }}</option>
							<option value="Other">{{ __('Otra') }}</option>
						</select>
					</div>
					<FormControl v-model="payout.account_number" :label="__('Número de cuenta')" />
					<FormControl v-model="payout.cci" label="CCI" required />
					<FormControl v-model="payout.account_holder_name" :label="__('Titular de la cuenta')" required />
					<FormControl v-model="payout.account_holder_document" :label="__('Documento del titular')" />
				</div>
				<Button variant="solid" :loading="saving" type="submit">{{ __('Guardar cuenta') }}</Button>
			</form>
		</section>
	</div>
</template>

<script setup>
import { Button, FormControl, call, toast, usePageMeta } from 'frappe-ui'
import { computed, inject, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BookOpen, CreditCard, LayoutDashboard, Plus, ReceiptText, Users, Wallet } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import DataTable from '@/components/InstructorDataTable.vue'

const route = useRoute()
const router = useRouter()
const user = inject('$user')
const { brand } = sessionStore()

const loading = ref(false)
const saving = ref(false)
const dashboard = ref({})
const courses = ref([])
const sales = ref([])
const students = ref([])
const wallet = ref({})
const withdrawals = ref([])
const withdrawalAmount = ref('')
const payout = reactive({
	bank_name: '',
	account_type: 'Savings',
	account_number: '',
	cci: '',
	account_holder_name: '',
	account_holder_document: '',
	currency: 'PEN',
})

const nav = [
	{ label: __('Dashboard'), to: 'InstructorDashboard', icon: LayoutDashboard },
	{ label: __('Cursos'), to: 'InstructorCourses', icon: BookOpen },
	{ label: __('Ventas'), to: 'InstructorSales', icon: ReceiptText },
	{ label: __('Alumnos'), to: 'InstructorStudents', icon: Users },
	{ label: __('Wallet'), to: 'InstructorWallet', icon: Wallet },
	{ label: __('Retiros'), to: 'InstructorWithdrawals', icon: CreditCard },
	{ label: __('Cuenta'), to: 'InstructorPayout', icon: CreditCard },
]

const activeView = computed(() => route.meta.instructorView || 'dashboard')
const pageTitle = computed(() => nav.find((item) => item.to === route.name)?.label || __('Dashboard'))

const money = (value) => Number(value || 0).toFixed(2)

const metrics = computed(() => [
	{ label: __('Cursos creados'), value: dashboard.value.course_count || 0 },
	{ label: __('Cursos en revisión'), value: dashboard.value.under_review_courses || 0 },
	{ label: __('Cursos publicados'), value: dashboard.value.published_courses || 0 },
	{ label: __('Ventas totales'), value: dashboard.value.total_sales || 0 },
	{ label: __('Alumnos inscritos'), value: dashboard.value.students || 0 },
	{ label: __('Saldo disponible'), value: `S/ ${money(dashboard.value.available_balance)}` },
])

const courseColumns = [
	{ label: __('Curso'), key: 'title' },
	{ label: __('Estado'), key: 'status' },
	{ label: __('Publicado'), key: 'published' },
	{ label: __('Alumnos'), key: 'enrollments' },
	{ label: __('Precio'), key: 'course_price' },
]
const saleColumns = [
	{ label: __('Curso'), key: 'course' },
	{ label: __('Alumno'), key: 'student' },
	{ label: __('Fuente'), key: 'sale_source' },
	{ label: __('Total'), key: 'gross_amount' },
	{ label: __('Ganancia'), key: 'instructor_amount' },
	{ label: __('Fecha'), key: 'purchased_at' },
]
const reviewColumns = [
	{ label: __('Curso'), key: 'course' },
	{ label: __('Estado'), key: 'status' },
	{ label: __('Score'), key: 'ai_score' },
	{ label: __('Resumen'), key: 'ai_summary' },
]
const studentColumns = [
	{ label: __('Alumno'), key: 'member_name' },
	{ label: __('Curso'), key: 'course_title' },
	{ label: __('Progreso'), key: 'progress' },
	{ label: __('Último acceso'), key: 'modified' },
]
const ledgerColumns = [
	{ label: __('Tipo'), key: 'transaction_type' },
	{ label: __('Curso'), key: 'course' },
	{ label: __('Neto'), key: 'net_amount' },
	{ label: __('Ganancia'), key: 'instructor_amount' },
	{ label: __('Estado'), key: 'status' },
	{ label: __('Fecha'), key: 'posting_date' },
]
const withdrawalColumns = [
	{ label: __('Solicitud'), key: 'name' },
	{ label: __('Monto'), key: 'requested_amount' },
	{ label: __('Estado'), key: 'status' },
	{ label: __('Solicitado'), key: 'requested_at' },
	{ label: __('Pagado'), key: 'paid_at' },
]

const load = async () => {
	if (!user.data?.is_instructor && !user.data?.is_moderator) {
		router.push({ name: 'Courses' })
		return
	}
	loading.value = true
	try {
		if (activeView.value === 'dashboard') dashboard.value = await call('studybadge_ai.instructor_review.get_instructor_dashboard')
		if (activeView.value === 'courses') courses.value = await call('studybadge_ai.instructor_review.get_instructor_courses')
		if (activeView.value === 'sales') sales.value = await call('studybadge_ai.instructor_review.get_instructor_sales')
		if (activeView.value === 'students') students.value = await call('studybadge_ai.instructor_review.get_instructor_students')
		if (activeView.value === 'wallet') wallet.value = await call('studybadge_ai.instructor_review.get_wallet')
		if (activeView.value === 'withdrawals') withdrawals.value = await call('studybadge_ai.instructor_review.list_withdrawals')
		if (activeView.value === 'payout') {
			const account = await call('studybadge_ai.instructor_review.get_payout_account')
			Object.assign(payout, { account_type: 'Savings', currency: 'PEN', ...account })
		}
	} catch (error) {
		toast.error(error.messages?.[0] || __('No pudimos cargar el panel'))
	} finally {
		loading.value = false
	}
}

const newCourse = () => {
	router.push({ name: 'Courses', query: { newCourse: '1' } })
}

const requestWithdrawal = async () => {
	saving.value = true
	try {
		await call('studybadge_ai.instructor_review.request_withdrawal', { amount: withdrawalAmount.value })
		toast.success(__('Retiro solicitado'))
		withdrawalAmount.value = ''
		withdrawals.value = await call('studybadge_ai.instructor_review.list_withdrawals')
	} catch (error) {
		toast.error(error.messages?.[0] || __('No pudimos solicitar el retiro'))
	} finally {
		saving.value = false
	}
}

const savePayout = async () => {
	saving.value = true
	try {
		const account = await call('studybadge_ai.instructor_review.save_payout_account', { data: { ...payout } })
		Object.assign(payout, account)
		toast.success(__('Cuenta de retiro guardada'))
	} catch (error) {
		toast.error(error.messages?.[0] || __('No pudimos guardar la cuenta'))
	} finally {
		saving.value = false
	}
}

onMounted(load)
watch(() => route.name, load)

usePageMeta(() => ({
	title: pageTitle.value,
	icon: brand.favicon,
}))
</script>

<style scoped>
.instructor-page {
	padding: 24px;
	min-height: 100vh;
	background: #f6f8fb;
}
.instructor-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	margin-bottom: 18px;
}
.instructor-header p {
	margin: 0 0 4px;
	text-transform: uppercase;
	font-size: 12px;
	font-weight: 900;
	color: #0d6efd;
}
.instructor-header h1 {
	font-size: 28px;
	font-weight: 900;
	margin: 0;
}
.instructor-tabs {
	display: flex;
	gap: 8px;
	overflow-x: auto;
	margin-bottom: 20px;
}
.instructor-tabs a {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	padding: 9px 12px;
	border: 1px solid #d0d5dd;
	border-radius: 8px;
	background: white;
	color: #344054;
	font-weight: 750;
	text-decoration: none;
	white-space: nowrap;
}
.instructor-tabs a.router-link-active {
	background: #061b49;
	border-color: #061b49;
	color: white;
}
.instructor-grid,
.wallet-summary {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 14px;
}
.metric-card,
.panel-wide,
.payout-card,
.withdrawal-form {
	background: white;
	border: 1px solid #e4e7ec;
	border-radius: 8px;
	padding: 18px;
	box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}
.metric-card span {
	display: block;
	color: #667085;
	font-size: 13px;
	font-weight: 750;
	margin-bottom: 8px;
}
.metric-card strong {
	font-size: 28px;
	font-weight: 900;
	color: #101828;
}
.panel-wide {
	grid-column: 1 / -1;
}
.panel-wide h2 {
	font-size: 17px;
	font-weight: 900;
	margin: 0 0 12px;
}
.wallet-layout {
	display: grid;
	gap: 14px;
}
.wallet-note,
.withdrawal-form p {
	color: #475467;
	margin: 0;
}
.withdrawal-form {
	display: grid;
	grid-template-columns: minmax(180px, 320px) auto;
	align-items: end;
	gap: 12px;
}
.withdrawal-form p {
	grid-column: 1 / -1;
}
.payout-form {
	display: grid;
	gap: 18px;
}
.payout-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 14px;
}
.field-label {
	display: block;
	font-size: 12px;
	color: #667085;
	margin-bottom: 6px;
}
.select-field {
	width: 100%;
	border: 1px solid #d0d5dd;
	border-radius: 8px;
	padding: 9px 10px;
	background: white;
}
.instructor-empty {
	background: white;
	border: 1px solid #e4e7ec;
	border-radius: 8px;
	padding: 48px;
	text-align: center;
	color: #667085;
}
@media (max-width: 780px) {
	.instructor-grid,
	.wallet-summary,
	.payout-grid,
	.withdrawal-form {
		grid-template-columns: 1fr;
	}
}
</style>

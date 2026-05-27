<template>
	<div v-if="!isLoggedIn" class="min-h-screen bg-[#F5F7FB] dark:bg-gray-900 font-sans flex flex-col absolute inset-0 z-50 overflow-y-auto">
		<PublicNavbar />
		
		<!-- Hero Section -->
		<div class="relative overflow-hidden bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-800 pt-16 pb-24 md:pt-24 md:pb-32">
			<!-- Decorative Background -->
			<div class="absolute top-[-10%] right-[-5%] w-[40%] h-[60%] rounded-full bg-[#007BFF]/5 blur-3xl"></div>
			<div class="absolute bottom-[-10%] left-[-5%] w-[40%] h-[60%] rounded-full bg-[#F5B301]/5 blur-3xl"></div>
			
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
				<div class="text-center max-w-3xl mx-auto">
					<h1 class="text-4xl md:text-6xl font-extrabold text-[#061B49] dark:text-white tracking-tight leading-tight mb-6">
						Aprende habilidades reales.<br />
						<span class="text-[#007BFF]">Obtén certificados verificables.</span>
					</h1>
					<p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-10 leading-relaxed">
						Explora cursos cortos, prácticos y diseñados para ayudarte a crecer profesionalmente, mejorar tu CV y avanzar a tu ritmo.
					</p>
					
					<div class="flex flex-col sm:flex-row items-center justify-center gap-4">
						<button @click="scrollToCourses" class="w-full sm:w-auto px-8 py-3.5 bg-[#007BFF] hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all hover:-translate-y-0.5 text-lg">
							Explorar cursos
						</button>
						<a href="/certificates" class="w-full sm:w-auto px-8 py-3.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 font-bold rounded-xl shadow-sm hover:shadow transition-all text-lg flex justify-center items-center">
							Ver cómo funcionan
						</a>
					</div>
				</div>
				
				<!-- Hero Floating Cards -->
				<div class="hidden md:flex justify-center gap-6 mt-16 flex-wrap">
					<div class="flex items-center gap-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md px-5 py-3 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
						<div class="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg text-[#007BFF]"><GraduationCap class="size-5" /></div>
						<span class="font-semibold text-sm text-gray-700 dark:text-gray-200">Certificado incluido</span>
					</div>
					<div class="flex items-center gap-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md px-5 py-3 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
						<div class="p-2 bg-amber-100 dark:bg-amber-900/50 rounded-lg text-[#F5B301]"><Sparkles class="size-5" /></div>
						<span class="font-semibold text-sm text-gray-700 dark:text-gray-200">TutorIA disponible</span>
					</div>
					<div class="flex items-center gap-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md px-5 py-3 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
						<div class="p-2 bg-green-100 dark:bg-green-900/50 rounded-lg text-green-600"><Clock class="size-5" /></div>
						<span class="font-semibold text-sm text-gray-700 dark:text-gray-200">Cursos cortos</span>
					</div>
					<div class="flex items-center gap-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md px-5 py-3 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
						<div class="p-2 bg-purple-100 dark:bg-purple-900/50 rounded-lg text-purple-600"><CheckCircle2 class="size-5" /></div>
						<span class="font-semibold text-sm text-gray-700 dark:text-gray-200">Proyecto final</span>
					</div>
				</div>
			</div>
		</div>

		<!-- Courses Section -->
		<div id="courses-section" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 w-full">
			<!-- Search & Chips -->
			<div class="mb-10 flex flex-col items-center">
				<div class="w-full max-w-3xl relative mb-6">
					<Search class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 size-5" />
					<input 
						v-model="title" 
						@input="updateCourses()"
						type="text" 
						class="w-full pl-12 pr-4 py-4 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-[#007BFF] focus:border-transparent dark:bg-gray-800 dark:text-white text-lg transition-shadow outline-none"
						placeholder="Buscar IA, Excel, ventas, marketing..."
					/>
				</div>
				
				<!-- Chips -->
				<div class="flex flex-wrap justify-center gap-2 max-w-4xl">
					<button 
						v-for="chip in ['IA', 'Negocios', 'Excel', 'Power BI', 'Marketing', 'Ventas', 'Emprendimiento', 'Productividad']"
						@click="title = chip; updateCourses()"
						:class="['px-4 py-1.5 rounded-full text-sm font-medium transition-colors border', title === chip ? 'bg-[#007BFF] text-white border-[#007BFF]' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700']"
					>
						{{ chip }}
					</button>
					<button v-if="title" @click="title=''; updateCourses()" class="px-4 py-1.5 rounded-full text-sm font-medium text-red-500 hover:bg-red-50 transition-colors border border-transparent">Limpiar</button>
				</div>
			</div>

			<!-- Filters Row -->
			<div class="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
				<TabButtons :buttons="courseTabs" v-model="currentTab" class="w-fit" />
				<div class="flex items-center gap-3">
					<Select
						v-if="categories.length"
						v-model="currentCategory"
						:options="categories"
						:placeholder="__('Categoría')"
						@update:modelValue="updateCourses()"
						class="w-48"
					/>
					<label class="flex items-center gap-2 cursor-pointer text-sm font-medium text-gray-700 dark:text-gray-300">
						<input type="checkbox" v-model="certification" @change="updateCourses()" class="rounded text-[#007BFF] focus:ring-[#007BFF] size-4">
						Solo certificados
					</label>
				</div>
			</div>

			<!-- Course List -->
			<div v-if="courses.data?.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
				<router-link v-for="course in courses.data" :to="{ name: 'CourseDetail', params: { courseName: course.name } }">
					<CourseCard :course="course" :isPublic="true" />
				</router-link>
			</div>
			<EmptyStateLayout v-else-if="!courses.list.loading" name="Courses" />
			<div v-if="!courses.list.loading && courses.hasNextPage" class="flex justify-center mt-10">
				<Button @click="courses.next()" size="lg">
					{{ __('Cargar Más') }}
				</Button>
			</div>
		</div>

		<!-- Benefits Section -->
		<div class="bg-white dark:bg-gray-800 py-20 border-y border-gray-100 dark:border-gray-800">
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<h2 class="text-3xl font-extrabold text-center text-[#061B49] dark:text-white mb-12">Todo lo que necesitas para aprender mejor</h2>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
					<div class="p-6 bg-[#F5F7FB] dark:bg-gray-900 rounded-2xl">
						<div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 text-[#007BFF] rounded-xl flex items-center justify-center mb-4"><Clock class="size-6" /></div>
						<h3 class="text-xl font-bold mb-2 dark:text-white">Cursos cortos y prácticos</h3>
						<p class="text-gray-600 dark:text-gray-400">Ve directo al grano con lecciones optimizadas que respetan tu tiempo.</p>
					</div>
					<div class="p-6 bg-[#F5F7FB] dark:bg-gray-900 rounded-2xl">
						<div class="w-12 h-12 bg-amber-100 dark:bg-amber-900/30 text-[#F5B301] rounded-xl flex items-center justify-center mb-4"><Award class="size-6" /></div>
						<h3 class="text-xl font-bold mb-2 dark:text-white">Certificados verificables</h3>
						<p class="text-gray-600 dark:text-gray-400">Obtén credenciales que puedes añadir directamente a LinkedIn.</p>
					</div>
					<div class="p-6 bg-[#F5F7FB] dark:bg-gray-900 rounded-2xl">
						<div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 text-purple-600 rounded-xl flex items-center justify-center mb-4"><Sparkles class="size-6" /></div>
						<h3 class="text-xl font-bold mb-2 dark:text-white">TutorIA para resolver dudas</h3>
						<p class="text-gray-600 dark:text-gray-400">Nuestro asistente inteligente está disponible 24/7 para ayudarte.</p>
					</div>
					<div class="p-6 bg-[#F5F7FB] dark:bg-gray-900 rounded-2xl">
						<div class="w-12 h-12 bg-green-100 dark:bg-green-900/30 text-green-600 rounded-xl flex items-center justify-center mb-4"><CheckSquare class="size-6" /></div>
						<h3 class="text-xl font-bold mb-2 dark:text-white">Tareas y proyectos</h3>
						<p class="text-gray-600 dark:text-gray-400">Aplica lo que aprendes inmediatamente con ejercicios reales.</p>
					</div>
					<div class="p-6 bg-[#F5F7FB] dark:bg-gray-900 rounded-2xl">
						<div class="w-12 h-12 bg-rose-100 dark:bg-rose-900/30 text-rose-600 rounded-xl flex items-center justify-center mb-4"><Play class="size-6" /></div>
						<h3 class="text-xl font-bold mb-2 dark:text-white">Aprende a tu ritmo</h3>
						<p class="text-gray-600 dark:text-gray-400">Sin horarios fijos. Estudia cuando quieras y donde quieras.</p>
					</div>
					<div class="p-6 bg-[#F5F7FB] dark:bg-gray-900 rounded-2xl">
						<div class="w-12 h-12 bg-teal-100 dark:bg-teal-900/30 text-teal-600 rounded-xl flex items-center justify-center mb-4"><Target class="size-6" /></div>
						<h3 class="text-xl font-bold mb-2 dark:text-white">Enfocado en habilidades</h3>
						<p class="text-gray-600 dark:text-gray-400">Contenido diseñado específicamente para el mercado laboral actual.</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Certificates Section -->
		<div class="bg-[#F5B301]/10 dark:bg-[#F5B301]/5 py-20 relative overflow-hidden">
			<div class="absolute right-0 bottom-0 opacity-10 pointer-events-none transform translate-x-1/4 translate-y-1/4">
				<Award class="w-96 h-96 text-[#F5B301]" />
			</div>
			<div class="max-w-4xl mx-auto px-4 text-center relative z-10">
				<h2 class="text-3xl md:text-4xl font-extrabold text-[#061B49] dark:text-white mb-6">Demuestra lo que sabes</h2>
				<p class="text-lg md:text-xl text-gray-700 dark:text-gray-300 mb-10 leading-relaxed max-w-2xl mx-auto">
					Completa cursos, supera actividades y obtén certificados digitales que puedes compartir en tu CV, LinkedIn o portafolio.
				</p>
				<a href="/certificates" class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-[#F5B301] hover:bg-yellow-500 text-yellow-950 font-bold rounded-xl shadow-lg hover:shadow-xl transition-all hover:-translate-y-0.5 text-lg">
					Ver galería de certificados <ArrowRight class="size-5" />
				</a>
			</div>
		</div>

		<!-- Final CTA -->
		<div class="bg-[#061B49] py-24 text-center px-4">
			<h2 class="text-3xl md:text-5xl font-extrabold text-white mb-6">Empieza hoy con una habilidad nueva.</h2>
			<button @click="scrollToCourses" class="px-10 py-4 bg-[#007BFF] hover:bg-blue-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all hover:-translate-y-0.5 text-xl mt-4">
				Explorar cursos
			</button>
		</div>
	</div>

	<!-- Original Authenticated Layout -->
	<div v-else class="h-full">
		<LayoutHeader>
			<template #left-header>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #right-header>
				<Dropdown placement="right" side="bottom" v-if="canCreateCourse()" :options="courseMenu">
					<template v-slot="{ open }">
						<Button variant="solid">
							<template #prefix><Plus class="size-4 stroke-1.5" /></template>
							{{ __('Crear') }}
							<template #suffix>
								<ChevronDown :class="['ms-1 size-4 transform stroke-1.5 transition-transform', open ? 'rotate-180' : '']" />
							</template>
						</Button>
					</template>
				</Dropdown>
			</template>
		</LayoutHeader>
		
		<div class="bg-gray-50 dark:bg-gray-900 min-h-screen p-4 md:p-8 pb-12">
			<!-- Page Header / Hero -->
			<div class="mb-8 relative overflow-hidden rounded-xl bg-gray-900 p-8 md:p-12 text-white shadow-md">
				<div class="absolute top-0 right-0 -mr-20 -mt-20 w-72 h-72 rounded-full bg-white opacity-10 blur-3xl"></div>
				<div class="absolute bottom-0 left-10 w-48 h-48 rounded-full bg-white opacity-10 blur-2xl"></div>
				
				<div class="relative z-10 flex flex-col md:flex-row items-center gap-6">
					<div class="flex-1">
						<h1 class="text-3xl md:text-5xl font-extrabold mb-4 text-white">{{ __('¡Descubre tu próximo gran logro!') }}</h1>
						<p class="text-blue-100 dark:text-gray-300 text-lg max-w-xl leading-relaxed">{{ __('Explora nuestro catálogo de cursos, desarrolla nuevas habilidades y lleva tu carrera al siguiente nivel. Aprender nunca fue tan divertido.') }}</p>
					</div>
					<div class="hidden md:flex items-center justify-center w-32 h-32 rounded-full bg-white/20 backdrop-blur-md border border-white/30 shadow-xl">
						<BookOpen class="w-16 h-16 text-white" />
					</div>
				</div>
			</div>

			<!-- Filters -->
			<div class="mb-8 flex flex-col justify-between space-y-4 lg:flex-row lg:items-center lg:space-y-0 bg-white dark:bg-gray-800 p-3 md:p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
				<TabButtons :buttons="courseTabs" v-model="currentTab" class="w-fit" />

				<div class="flex flex-col space-y-3 lg:flex-row lg:items-center lg:gap-x-3 lg:space-y-0">
					<div class="grid grid-cols-2 gap-2">
						<FormControl v-model="title" :placeholder="__('Buscar')" type="text" class="w-full" @input="updateCourses()" />
						<Select v-if="categories.length" v-model="currentCategory" :options="categories" :placeholder="__('Categoría')" @update:modelValue="updateCourses()" />
					</div>

					<Tooltip :text="__('Mostrar solo cursos con certificado')">
						<FormControl type="checkbox" v-model="certification" :label="__('Certificación')" @change="updateCourses()" />
					</Tooltip>
				</div>
			</div>
			
			<div v-if="courses.data?.length" class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
				<router-link v-for="course in courses.data" :to="{ name: 'CourseDetail', params: { courseName: course.name } }">
					<CourseCard :course="course" />
				</router-link>
			</div>
			<EmptyStateLayout v-else-if="!courses.list.loading" name="Courses" />
			<div v-if="!courses.list.loading && courses.hasNextPage" class="flex justify-center mt-5">
				<Button @click="courses.next()">{{ __('Cargar Más') }}</Button>
			</div>
		</div>
	</div>

	<NewCourseModal v-if="showCourseModal" v-model="showCourseModal" :courses="courses" />
	<CourseImportModal v-if="showCourseImportModal" v-model="showCourseImportModal" />
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	call,
	createListResource,
	Dropdown,
	FormControl,
	Select,
	TabButtons,
	Tooltip,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { ChevronDown, Plus, BookOpen, GraduationCap, Sparkles, Clock, CheckCircle2, Search, CheckSquare, Play, Target, ArrowRight } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { canCreateCourse } from '@/utils'
import CourseCard from '@/components/CourseCard.vue'
import EmptyStateLayout from '@/components/Layouts/EmptyStateLayout.vue'
import LayoutHeader from '@/components/Layouts/LayoutHeader.vue'
import PublicNavbar from '@/components/PublicNavbar.vue'
import { useRouter } from 'vue-router'
import NewCourseModal from '@/pages/Courses/NewCourseModal.vue'
import CourseImportModal from '@/pages/Courses/CourseImportModal.vue'

const user = inject('$user')
const dayjs = inject('$dayjs')
const start = ref(0)
const pageLength = ref(30)
const categories = ref([
	{
		label: '',
		value: null,
	},
])
const currentCategory = ref(null)
const title = ref('')
const certification = ref(false)
const filters = ref({})
const currentTab = ref('live')
const { brand, isLoggedIn } = sessionStore()
const courseCount = ref(0)
const router = useRouter()
const showCourseModal = ref(false)
const showCourseImportModal = ref(false)

const scrollToCourses = () => {
	document.getElementById('courses-section')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
	setFiltersFromQuery()
	updateCourses()
	getCourseCount()
})

const setFiltersFromQuery = () => {
	let queries = new URLSearchParams(location.search)
	title.value = queries.get('title') || ''
	currentCategory.value = queries.get('category') || null
	certification.value = queries.get('certification') || false
	if (queries.get('newCourse') == '1') {
		showCourseModal.value = true
	}
}

const courses = createListResource({
	doctype: 'LMS Course',
	url: 'lms.lms.utils.get_courses',
	cache: ['courses', user.data?.name],
	pageLength: pageLength.value,
	start: start.value,
})

const setCategories = (data) => {
	let allCategories = data.map((course) => course.category)
	allCategories = allCategories.filter(
		(category, index) => allCategories.indexOf(category) === index && category
	)
	if (categories.value.length <= allCategories.length) {
		updateCategories(data)
	}
}

const getCourseCount = () => {
	if (!user.data) return
	if (!user.data.is_moderator) return
	call('frappe.client.get_count', {
		doctype: 'LMS Course',
	}).then((data) => {
		courseCount.value = data
	})
}

const updateCourses = () => {
	updateFilters()
	courses.update({
		filters: filters.value,
	})
	courses.reload().then((data) => {
		setCategories(data)
	})
}

const updateFilters = () => {
	updateCategoryFilter()
	updateTitleFilter()
	updateCertificationFilter()
	updateTabFilter()
	updateStudentFilter()
	setQueryParams()
}

const updateCategoryFilter = () => {
	if (currentCategory.value) {
		filters.value['category'] = currentCategory.value
	} else {
		delete filters.value['category']
	}
}

const updateTitleFilter = () => {
	if (title.value) {
		filters.value['title'] = ['like', `%${title.value}%`]
	} else {
		delete filters.value['title']
	}
}

const updateCertificationFilter = () => {
	if (certification.value) {
		filters.value['certification'] = 1
	} else {
		delete filters.value['certification']
	}
}

const updateTabFilter = () => {
	delete filters.value['live']
	delete filters.value['created']
	delete filters.value['published_on']
	delete filters.value['upcoming']

	if (currentTab.value == 'enrolled' && user.data?.is_student) {
		filters.value['enrolled'] = 1
		delete filters.value['published']
	} else {
		delete filters.value['published']
		delete filters.value['enrolled']

		if (currentTab.value == 'live') {
			filters.value['published'] = 1
			filters.value['upcoming'] = 0
			filters.value['live'] = 1
		} else if (currentTab.value == 'upcoming') {
			filters.value['upcoming'] = 1
		} else if (currentTab.value == 'new') {
			filters.value['published'] = 1
			filters.value['published_on'] = [
				'>=',
				dayjs().add(-3, 'month').format('YYYY-MM-DD'),
			]
		} else if (currentTab.value == 'created') {
			filters.value['created'] = 1
		} else if (currentTab.value == 'unpublished') {
			filters.value['published'] = 0
		}
	}
}

const updateStudentFilter = () => {
	if (!user.data || (user.data?.is_student && currentTab.value != 'enrolled')) {
		filters.value['published'] = 1
	}
}

const setQueryParams = () => {
	let queries = new URLSearchParams(location.search)
	let filterKeys = {
		title: title.value,
		category: currentCategory.value,
		certification: certification.value,
	}

	Object.keys(filterKeys).forEach((key) => {
		if (filterKeys[key]) {
			queries.set(key, filterKeys[key])
		} else {
			queries.delete(key)
		}
	})

	let queryString = ''
	if (queries.toString()) {
		queryString = `?${queries.toString()}`
	}

	history.replaceState({}, '', `${location.pathname}${queryString}`)
}

const updateCategories = (data) => {
	data.forEach((course) => {
		if (
			course.category &&
			!categories.value.find((category) => category.value === course.category)
		)
			categories.value.push({
				label: course.category,
				value: course.category,
			})
	})
}

watch(currentTab, () => {
	updateCourses()
})

const courseTabs = computed(() => {
	let tabs = [
		{
			label: __('Activos'),
			value: 'live',
		},
		{
			label: __('Nuevos'),
			value: 'new',
		},
		{
			label: __('Próximos'),
			value: 'upcoming',
		},
	]
	if (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	) {
		tabs.push({ label: __('Destacados'), value: 'created' })
		tabs.push({ label: __('Sin Publicar'), value: 'unpublished' })
	} else if (user.data) {
		tabs.push({ label: __('Inscritos'), value: 'enrolled' })
	}
	return tabs
})

const courseMenu = computed(() => {
	return [
		{
			label: __('Nuevo Curso'),
			icon: 'book-open',
			onClick() {
				showCourseModal.value = true
			},
		},
		{
			label: __('Importar con Data Import'),
			icon: 'upload',
			onClick() {
				router.push({
					name: 'NewDataImport',
					params: { doctype: 'LMS Course' },
				})
			},
		},
		{
			label: __('Importar con ZIP'),
			icon: 'folder-plus',
			onClick() {
				showCourseImportModal.value = true
			},
		},
	]
})

const breadcrumbs = computed(() => [
	{
		label: __('Cursos'),
		route: { name: 'Courses' },
	},
])

usePageMeta(() => {
	return {
		title: __('Cursos'),
		icon: brand.favicon,
	}
})
</script>

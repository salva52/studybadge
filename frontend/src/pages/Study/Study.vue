<template>
	<div class="study-page">
		<div class="mx-auto flex w-full max-w-[1500px] flex-col gap-6 px-4 py-5 sm:px-6 lg:px-8">
			<!-- ═══════════ HERO HEADER ═══════════ -->
			<header class="study-hero">
				<div class="hero-decoration">
					<div class="hero-orb hero-orb--1"></div>
					<div class="hero-orb hero-orb--2"></div>
					<div class="hero-orb hero-orb--3"></div>
				</div>
				<div class="hero-content">
					<div class="hero-text">
						<div v-if="!isDashboard" class="hero-breadcrumb">
							<router-link :to="{ name: 'Study' }" class="hero-breadcrumb-link">
								{{ __('Cursos IA') }}
							</router-link>
							<span v-if="pageTitle" class="hero-breadcrumb-sep">/</span>
							<span v-if="pageTitle" class="hero-breadcrumb-current">{{ pageTitle }}</span>
						</div>
						<h1 class="hero-title">{{ headerTitle }}</h1>
						<p class="hero-subtitle">{{ headerSubtitle }}</p>
					</div>
					<div class="hero-actions">
						<nav class="hero-nav">
							<router-link
								v-for="item in topNav"
								:key="item.name"
								:to="{ name: item.name }"
								class="nav-pill"
								:class="route.name === item.name ? 'nav-pill--active' : ''"
							>
								<component :is="item.icon" class="h-4 w-4 stroke-1.5" />
								<span class="nav-pill-label">{{ item.label }}</span>
							</router-link>
						</nav>
					</div>
				</div>
			</header>

			<!-- ═══════════ SKELETON ═══════════ -->
			<div v-if="isPageLoading" class="study-skeleton-wrapper">
				<section class="grid gap-6 xl:grid-cols-[1fr_360px]">
					<div class="flex flex-col gap-6">
						<div class="s-panel skeleton-panel" style="height: 180px;"></div>
						<div class="s-panel skeleton-panel" style="height: 400px;"></div>
					</div>
					<aside class="flex flex-col gap-6">
						<div class="s-panel skeleton-panel" style="height: 200px;"></div>
						<div class="s-panel skeleton-panel" style="height: 300px;"></div>
					</aside>
				</section>
			</div>

			<!-- ═══════════ DASHBOARD ═══════════ -->
			<section v-else-if="isDashboard" class="grid gap-6 xl:grid-cols-[1fr_360px]">
				<div class="flex flex-col gap-6">
					<!-- FLOW CARDS -->
					<div class="s-panel s-panel--flush">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker"><Sparkles class="h-3.5 w-3.5 stroke-1.5" /> {{ __('Empieza en 4 pasos') }}</div>
								<h2 class="s-panel-title">{{ __('Crear curso IA') }}</h2>
								<p class="s-panel-desc">{{ __('Elige el objetivo que más se parece a tu situación. La IA ordenará tus apuntes en módulos, lecciones y práctica guiada.') }}</p>
							</div>
							<Button variant="solid" :label="__('Crear curso IA')" @click="startFlow('parcial')" />
						</div>
						<div class="flow-grid">
							<button
								v-for="flow in flows"
								:key="flow.id"
								class="flow-card group"
								@click="startFlow(flow.id)"
							>
								<div class="flow-icon" :class="`flow-icon--${flow.id}`">
									<component :is="flow.icon" class="h-5 w-5 stroke-1.5" />
								</div>
								<div class="flow-info">
									<h3 class="flow-card-title">{{ flow.label }}</h3>
									<p class="flow-card-desc">{{ flow.description }}</p>
								</div>
								<ArrowRight class="flow-arrow" />
							</button>
						</div>
					</div>

					<!-- RECENT COURSES -->
					<div class="s-panel s-panel--flush">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker"><Clock class="h-3.5 w-3.5 stroke-1.5" /> {{ __('Continúa aprendiendo') }}</div>
								<h2 class="s-panel-title">{{ __('Cursos recientes') }}</h2>
							</div>
							<Button :label="__('Actualizar')" :loading="loading === 'dashboard'" @click="loadDashboard">
								<template #prefix><RefreshCw class="h-4 w-4 stroke-1.5" /></template>
							</Button>
						</div>
						<div class="courses-grid">
							<div v-for="session in sessions.slice(0, 6)" :key="session.name" class="course-card">
								<div class="course-card-top">
									<div class="min-w-0">
										<span class="course-tag" :class="`course-tag--${session.flow_id || session.goal || 'parcial'}`">{{ flowLabel(session.flow_id || session.goal) }}</span>
										<h3 class="course-card-title">{{ session.title || session.name }}</h3>
										<p class="course-card-date">
											<Clock class="h-3.5 w-3.5 stroke-1.5" />
											{{ __('Última actividad') }} · {{ formatDate(session.modified) }}
										</p>
									</div>
									<div class="course-progress-ring">
										<svg viewBox="0 0 36 36">
											<path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
											<path class="ring-fill" :stroke-dasharray="`${courseProgress(session)}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
										</svg>
										<span class="ring-text">{{ courseProgress(session) }}%</span>
									</div>
								</div>
								<div class="course-progress-bar">
									<div class="progress-track">
										<div class="progress-fill" :style="{ width: `${courseProgress(session)}%` }" />
									</div>
									<span class="progress-label">{{ courseProgress(session) }}% {{ __('completado') }}</span>
								</div>
								<div class="course-next">
									<div class="course-next-icon"><PlayCircle class="h-4 w-4 stroke-1.5" /></div>
									<div class="min-w-0">
										<div class="course-next-label">{{ __('Siguiente lección') }}</div>
										<div class="course-next-title">{{ flattenLessons(session.course_structure || fallbackCourseStructure(session))[nextLessonIndex(session)]?.title || __('Abrir curso') }}</div>
									</div>
								</div>
								<div class="course-actions">
									<Button :label="__('Continuar')" variant="solid" @click="openRoom(session.name, nextLessonIndex(session))" />
									<Button :label="__('Ver módulos')" @click="openPlan(session.name)" />
									<Button :label="__('Borrar')" variant="subtle" theme="red" @click="deleteSession(session.name)">
										<template #prefix><Trash2 class="h-3.5 w-3.5 stroke-1.5" /></template>
									</Button>
								</div>
							</div>
							<div v-if="!sessions.length" class="s-empty lg:col-span-2">
								<div class="s-empty-icon"><BookOpen class="h-8 w-8 stroke-1.5" /></div>
								<h3 class="s-empty-title">{{ __('Aún no tienes cursos IA') }}</h3>
								<p class="s-empty-desc">{{ __('Elige un modo de estudio arriba para crear tu primer curso con apuntes, PDFs o temas del parcial.') }}</p>
							</div>
						</div>
					</div>
				</div>

				<!-- SIDEBAR -->
				<aside class="flex flex-col gap-6">
					<div class="s-panel s-panel--flush">
						<div class="sidebar-header">
							<BarChart3 class="h-4 w-4 stroke-1.5" />
							<h2 class="sidebar-title">{{ __('Tu avance') }}</h2>
						</div>
						<div class="metrics-grid">
							<div v-for="metric in dashboardMetrics" :key="metric.label" class="metric-card">
								<div class="metric-value">{{ metric.value }}</div>
								<div class="metric-label">{{ metric.label }}</div>
							</div>
						</div>
					</div>
					<div class="s-panel s-panel--flush">
						<div class="sidebar-header">
							<Star class="h-4 w-4 stroke-1.5" />
							<h2 class="sidebar-title">{{ __('Explicaciones favoritas') }}</h2>
							<router-link :to="{ name: 'StudyExplanations' }" class="sidebar-link">{{ __('Ver todas') }}</router-link>
						</div>
						<div class="fav-list">
							<router-link
								v-for="explanation in explanations.slice(0, 5)"
								:key="explanation.name"
								:to="{ name: 'StudyExplanations' }"
								class="fav-item"
							>
								<BookMarked class="h-4 w-4 shrink-0 stroke-1.5" />
								<div class="min-w-0">
									<div class="fav-item-title">{{ explanation.topic || __('Sin tema') }}</div>
									<div class="fav-item-date">{{ formatDate(explanation.creation) }}</div>
								</div>
							</router-link>
							<div v-if="!explanations.length" class="s-mini-empty">
								<BookMarked class="h-5 w-5 stroke-1.5" />
								<span>{{ __('Guarda una explicación importante desde una lección para repasarla luego.') }}</span>
							</div>
						</div>
					</div>
				</aside>
			</section>

			<!-- ═══════════ FLOW BUILDER ═══════════ -->
			<section v-else-if="isFlow" class="flow-wizard">
				<!-- Stepper Responsive (Horizontal en Móvil, Vertical en Escritorio) -->
				<aside class="wizard-sidebar s-panel s-panel--flush">
					<div class="builder-header hidden xl:flex">
						<Wand2 class="h-5 w-5 stroke-1.5" />
						<div>
							<div class="s-kicker">{{ __('Constructor guiado') }}</div>
							<h2 class="s-panel-title">{{ __('Crea tu curso IA') }}</h2>
						</div>
					</div>
					<div class="steps-list wizard-steps">
						<button class="s-step" :class="activeFlowStep === 1 ? 'is-active' : (currentSession ? 'is-done' : 'is-locked')" @click="goToStep(1)">
							<span class="s-step-num">1</span>
							<div class="hidden xl:block text-left">
								<div class="s-step-title">{{ __('Datos básicos') }}</div>
								<p class="s-step-desc">{{ currentSession ? __('Curso creado') : __('Ponle nombre y contexto') }}</p>
							</div>
						</button>
						<button class="s-step" :class="activeFlowStep === 2 ? 'is-active' : (hasCourseSeed ? 'is-done' : 'is-locked')" @click="goToStep(2)" :disabled="!currentSession && !hasCourseSeed">
							<span class="s-step-num">2</span>
							<div class="hidden xl:block text-left">
								<div class="s-step-title">{{ __('Material y temas') }}</div>
								<p class="s-step-desc">{{ __('Analiza archivos o texto base') }}</p>
							</div>
						</button>
						<button class="s-step" :class="activeFlowStep === 3 ? 'is-active' : (currentSession?.profile_questions?.length ? 'is-done' : 'is-locked')" @click="goToStep(3)" :disabled="!canGenerateQuestions">
							<span class="s-step-num">3</span>
							<div class="hidden xl:block text-left">
								<div class="s-step-title">{{ __('Perfil de aprendizaje') }}</div>
								<p class="s-step-desc">{{ __('Genera preguntas de nivel') }}</p>
							</div>
						</button>
						<button class="s-step" :class="activeFlowStep === 4 ? 'is-active' : (currentSession?.course_structure?.modules?.length ? 'is-done' : 'is-locked')" @click="goToStep(4)" :disabled="!canCreateFullCourse">
							<span class="s-step-num">4</span>
							<div class="hidden xl:block text-left">
								<div class="s-step-title">{{ __('Crear el curso') }}</div>
								<p class="s-step-desc">{{ __('Genera módulos y lecciones') }}</p>
							</div>
						</button>
					</div>
				</aside>

				<div class="wizard-content relative">
					<Transition name="fade-slide" mode="out-in">
					<!-- Step 1 -->
					<div v-if="activeFlowStep === 1" class="wizard-step">
						<div class="s-panel s-panel--flush">
							<div class="s-panel-header">
								<div>
									<div class="s-kicker">{{ __('Paso 1 de 4') }}</div>
									<h2 class="s-panel-title">{{ __('Datos básicos del curso') }}</h2>
									<p class="s-panel-desc">{{ __('Ponle nombre al curso y pega cualquier texto base que ya tengas.') }}</p>
								</div>
							</div>
							<div class="form-grid">
								<FormControl v-model="draft.title" :label="__('Nombre del curso')" :placeholder="__('Ej. Parcial de cálculo')" />
								<FormControl v-model="draft.academic_context" :label="__('Curso o contexto')" :placeholder="__('Ej. Universidad, curso, ciclo')" />
								<FormControl v-model="draft.exam_date" type="date" :label="__('Fecha objetivo (Opcional)')" />
								<div>
									<label class="s-label">{{ __('Nivel') }}</label>
									<select v-model="draft.student_level" class="s-select">
										<option value="colegio">{{ __('Colegio') }}</option>
										<option value="preuniversitario">{{ __('Preuniversitario') }}</option>
										<option value="universitario">{{ __('Universitario') }}</option>
										<option value="profesional">{{ __('Profesional') }}</option>
									</select>
								</div>
								<FormControl class="md:col-span-2" v-model="draft.desired_topics" :label="__('Temas obligatorios')" :placeholder="__('Separados por coma, opcional')" />
								<div class="md:col-span-2">
									<label class="s-label">{{ __('Texto manual') }}</label>
									<textarea v-model="draft.manual_text" class="s-textarea" rows="7" :placeholder="__('Pega sílabos, apuntes, ejercicios o temas del parcial.')" />
								</div>
							</div>
							<div class="wizard-actions">
								<div></div>
								<Button :label="currentSession ? __('Guardar y continuar') : __('Crear curso y continuar')" variant="solid" :loading="loading === 'create'" @click="createOrUpdateSession" />
							</div>
						</div>
						
						<!-- Admission search -->
						<div v-if="flowId === 'admision'" class="s-panel s-panel--flush mt-6">
							<div class="s-panel-header">
								<div>
									<div class="s-kicker">{{ __('Opcional') }}</div>
									<h2 class="s-panel-title">{{ __('Buscar temario de admisión') }}</h2>
									<p class="s-panel-desc">{{ __('La IA trae una base de temas para convertirla en curso.') }}</p>
								</div>
							</div>
							<div class="form-grid form-grid--inline">
								<FormControl v-model="university" :placeholder="__('Universidad')" />
								<FormControl v-model="career" :placeholder="__('Carrera, opcional')" />
								<Button :label="__('Buscar')" :loading="loading === 'search'" @click="searchTemario" />
							</div>
							<div v-if="searchResult" class="s-markdown-block" v-html="renderMarkdown(searchResult)" />
						</div>
					</div>

					<!-- Step 2 -->
					<div v-else-if="activeFlowStep === 2" class="wizard-step">
						<div class="s-panel s-panel--flush">
							<div class="s-panel-header">
								<div>
									<div class="s-kicker">{{ __('Paso 2 de 4') }}</div>
									<h2 class="s-panel-title">{{ __('Materiales y temas') }}</h2>
									<p class="s-panel-desc">{{ __('Sube archivos de apuntes o PDFs. Si no tienes ninguno, simplemente haz clic en "Analizar material" para continuar.') }}</p>
								</div>
								<div class="flex flex-wrap gap-2">
									<FileUploader
										ref="fileUploader"
										class="hidden"
										:fileTypes="['.pdf', '.doc', '.docx', 'image/*', '.txt', '.md']"
										:uploadArgs="{ private: true }"
										:validateFile="validateFile"
										@success="handleFileUploaded"
									/>
									<Button :label="__('Subir archivo')" @click="openUploader">
										<template #prefix><Upload class="h-4 w-4 stroke-1.5" /></template>
									</Button>
									<Button :label="__('Analizar material')" variant="solid" :loading="loading === 'analyze'" @click="analyzeMaterial" />
								</div>
							</div>
							<div v-if="loading === 'analyze'" class="s-loader">
								<div class="s-loader-spinner"></div>
								{{ __('Analizando material y ordenando temas...') }}
							</div>
							<div class="grid gap-6 md:grid-cols-2 p-5">
								<div>
									<h3 class="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2"><FileText class="h-4 w-4 stroke-1.5 text-indigo-500" /> {{ __('Archivos subidos') }}</h3>
									<div class="materials-list mt-0 pt-0">
										<div v-for="material in currentSession?.materials || []" :key="material.idx" class="material-item">
											<div class="material-icon"><FileText class="h-4 w-4 stroke-1.5" /></div>
											<div class="min-w-0">
												<div class="material-name">{{ material.file_name }}</div>
												<div class="material-meta">{{ material.file_type }} · {{ material.analysis_status }}</div>
											</div>
										</div>
										<div v-if="!currentSession?.materials?.length" class="s-empty-sm">
											<Upload class="h-6 w-6 stroke-1.5" />
											<p>{{ __('Agrega material para mejorar el curso. También puedes usar solo el texto manual del paso 1.') }}</p>
										</div>
									</div>
								</div>
								<div>
									<h3 class="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2"><Layers class="h-4 w-4 stroke-1.5 text-indigo-500" /> {{ __('Temas detectados') }}</h3>
									<div class="flex flex-col gap-2">
										<div v-for="topic in currentSession?.topics || []" :key="topic.title || topic" class="topic-chip">
											<CheckCircle2 class="h-3.5 w-3.5 stroke-1.5" />
											{{ topic.title || topic }}
										</div>
										<div v-if="!currentSession?.topics?.length" class="s-mini-empty">
											<Layers class="h-5 w-5 stroke-1.5" />
											<span>{{ __('Cuando analices tu material, aquí aparecerán los temas base.') }}</span>
										</div>
									</div>
								</div>
							</div>
							<div class="wizard-actions">
								<Button :label="__('Atrás')" @click="goToStep(1)" />
								<Button :label="__('Continuar')" variant="solid" :disabled="!hasCourseSeed" @click="goToStep(3)" />
							</div>
						</div>
					</div>

					<!-- Step 3 -->
					<div v-else-if="activeFlowStep === 3" class="wizard-step">
						<div class="s-panel s-panel--flush">
							<div class="s-panel-header">
								<div>
									<div class="s-kicker">{{ __('Paso 3 de 4') }}</div>
									<h2 class="s-panel-title">{{ __('Perfil de aprendizaje') }}</h2>
									<p class="s-panel-desc">{{ __('Genera preguntas breves para que la IA adapte dificultad, ritmo y ejemplos a tu nivel.') }}</p>
								</div>
								<div class="flex flex-wrap gap-2">
									<Button :label="__('Generar preguntas')" :loading="loading === 'questions'" @click="generateQuestions" />
								</div>
							</div>
							<div class="p-5 flex flex-col gap-4">
								<div v-for="question in currentSession?.profile_questions || []" :key="question.id" class="profile-q">
									<div class="profile-q-text">{{ question.question }}</div>
									<select v-model="profileAnswers[question.id]" class="s-select s-select--sm max-w-md">
										<option value="">{{ __('Selecciona una opción') }}</option>
										<option v-for="option in question.options || []" :key="option.label" :value="option.label">{{ option.label }}</option>
									</select>
								</div>
								<div v-if="!currentSession?.profile_questions?.length" class="s-mini-empty">
									<UserCog class="h-5 w-5 stroke-1.5" />
									<span>{{ __('Pulsa "Generar preguntas" para completar tu perfil.') }}</span>
								</div>
							</div>
							<div class="wizard-actions">
								<Button :label="__('Atrás')" @click="goToStep(2)" />
								<Button :label="__('Guardar perfil y continuar')" variant="solid" :disabled="!currentSession?.profile_questions?.length" :loading="loading === 'profile'" @click="saveProfileAndContinue" />
							</div>
						</div>
					</div>

					<!-- Step 4 -->
					<div v-else-if="activeFlowStep === 4" class="wizard-step">
						<div class="s-panel s-panel--flush">
							<div class="s-panel-header">
								<div>
									<div class="s-kicker">{{ __('Paso 4 de 4') }}</div>
									<h2 class="s-panel-title">{{ __('Crear el curso') }}</h2>
									<p class="s-panel-desc">{{ __('Genera la malla completa de módulos y lecciones basados en tu material y perfil.') }}</p>
								</div>
							</div>
							<div class="p-5">
								<div v-if="loading === 'plan'" class="s-loader mb-4">
									<div class="s-loader-spinner"></div>
									{{ __('Creando módulos, lecciones y ruta de estudio...') }}
								</div>
								<div v-else class="step-instruction mb-6">
									<CheckCircle2 class="h-5 w-5 stroke-1.5 text-green-500" />
									<span class="font-medium text-slate-700">{{ __('Todo listo para generar el curso completo. ¿Comenzamos?') }}</span>
								</div>
							</div>
							<div class="wizard-actions">
								<Button :label="__('Atrás')" @click="goToStep(3)" />
								<Button :label="__('Generar Curso Mágico')" variant="solid" theme="indigo" size="lg" :disabled="!canCreateFullCourse" :loading="loading === 'plan'" @click="generatePlan" />
							</div>
						</div>
					</div>
					</Transition>
				</div>
			</section>

			<!-- ═══════════ PLAN VIEW ═══════════ -->
			<section v-else-if="isPlan" class="grid gap-6 xl:grid-cols-[1fr_340px]">
				<div class="s-panel s-panel--flush">
					<div class="s-panel-header">
						<div>
							<div class="s-kicker">{{ __('Curso IA personal') }}</div>
							<h2 class="s-panel-title">{{ courseStructure.courseTitle || currentSession?.title }}</h2>
							<p class="s-panel-desc">{{ currentSession?.profile_summary || courseStructure.courseGoal || __('Malla curricular generada por TutorIA.') }}</p>
						</div>
						<div class="flex flex-wrap gap-2">
							<Button :label="__('Continuar')" variant="solid" @click="openRoom(currentSession.name, nextLessonIndex(currentSession))" />
							<Button :label="__('Rehacer plan')" :loading="loading === 'plan'" @click="generatePlan" />
						</div>
					</div>
					<div class="plan-progress">
						<div class="plan-progress-header">
							<span class="plan-progress-label">{{ __('Progreso total') }}</span>
							<span class="plan-progress-pct">{{ courseProgress(currentSession) }}%</span>
						</div>
						<div class="progress-track progress-track--lg">
							<div class="progress-fill" :style="{ width: `${courseProgress(currentSession)}%` }" />
						</div>
					</div>
					<div class="modules-list">
						<div v-for="(module, moduleIndex) in courseStructure.modules || []" :key="module.title || moduleIndex" class="module-card">
							<div class="module-header">
								<div>
									<div class="s-kicker">{{ module.period || `${__('Módulo')} ${moduleIndex + 1}` }}</div>
									<h3 class="module-title">{{ module.title }}</h3>
									<p class="module-obj">{{ module.objective }}</p>
								</div>
								<span class="module-badge">{{ module.lessons?.length || 0 }} {{ __('lecciones') }}</span>
							</div>
							<div class="lessons-list">
								<button
									v-for="lesson in module.lessons || []"
									:key="lesson.key || lesson.title"
									class="lesson-row"
									@click="openRoom(currentSession.name, lessonGlobalIndex(lesson))"
								>
									<div class="lesson-left">
										<div class="lesson-check" :class="isLessonDone(lesson) ? 'is-done' : ''">
											<CheckCircle2 class="h-4 w-4 stroke-1.5" />
										</div>
										<div class="min-w-0">
											<div class="lesson-title">{{ lesson.title }}</div>
											<p class="lesson-obj">{{ lesson.objective }}</p>
										</div>
									</div>
									<div class="lesson-meta">
										<span class="lesson-duration"><Clock class="h-3 w-3 stroke-1.5" /> {{ lesson.duration || __('30 min') }}</span>
										<span class="lesson-diff">{{ lesson.difficulty || __('medio') }}</span>
									</div>
								</button>
							</div>
						</div>
						<div v-if="!lessonsFlat.length" class="s-empty">
							<div class="s-empty-icon"><ClipboardCheck class="h-8 w-8 stroke-1.5" /></div>
							<h3 class="s-empty-title">{{ __('El curso aún no tiene lecciones') }}</h3>
							<p class="s-empty-desc">{{ __('Vuelve al constructor y crea el plan completo.') }}</p>
						</div>
					</div>
				</div>
				<aside class="s-panel s-panel--flush h-fit">
					<div class="sidebar-header">
						<BarChart3 class="h-4 w-4 stroke-1.5" />
						<h2 class="sidebar-title">{{ __('Resumen del curso') }}</h2>
					</div>
					<div class="summary-stats">
						<div class="summary-stat">
							<div class="summary-stat-label">{{ __('Lecciones') }}</div>
							<div class="summary-stat-value">{{ lessonsFlat.length }}</div>
						</div>
						<div class="summary-stat">
							<div class="summary-stat-label">{{ __('Progreso') }}</div>
							<div class="summary-stat-value">{{ courseProgress(currentSession) }}%</div>
						</div>
						<div class="summary-stat summary-stat--highlight">
							<div class="summary-stat-label">{{ __('Siguiente paso') }}</div>
							<div class="summary-stat-next">{{ lessonsFlat[nextLessonIndex(currentSession)]?.title || __('Revisar módulos') }}</div>
						</div>
					</div>
				</aside>
			</section>

			<!-- ═══════════ ROOM VIEW ═══════════ -->
			<section v-else-if="isRoom" class="grid gap-6 xl:grid-cols-[1fr_360px]">
				<div class="flex flex-col gap-6">
					<!-- Room header -->
					<div class="s-panel s-panel--flush room-header-panel">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker">{{ activeLesson.moduleTitle || __('Lección') }}</div>
								<h2 class="s-panel-title">{{ lessonPack.lessonTitle || activeTopicTitle }}</h2>
								<p class="s-panel-desc">{{ lessonPack.learningObjective || activeLesson.objective || __('Aprende con explicación, práctica, quiz, tutor y diagrama.') }}</p>
							</div>
							<div class="flex flex-wrap gap-2">
								<Button :label="__('Regenerar')" :loading="loading === 'pack'" @click="generatePack(true)">
									<template #prefix><RefreshCw class="h-4 w-4 stroke-1.5" /></template>
								</Button>
								<Button :label="__('Diagrama')" :loading="loading === 'diagram'" @click="generateDiagram">
									<template #prefix><GitBranch class="h-4 w-4 stroke-1.5" /></template>
								</Button>
								<Button :label="__('Guardar favorito')" @click="saveCurrentExplanation">
									<template #prefix><Star class="h-4 w-4 stroke-1.5" /></template>
								</Button>
							</div>
						</div>
						<div v-if="loading === 'lesson'" class="s-loader mb-4">
							<div class="s-loader-spinner"></div>
							{{ __('Preparando tu lección personalizada...') }}
						</div>
					</div>

					<div class="room-steps-sticky">
						<div class="room-steps">
							<div class="room-step is-active">
								<span class="room-step-num">1</span>
								<div>
									<strong>{{ __('Aprende') }}</strong>
									<p>{{ __('Idea clave y explicación') }}</p>
								</div>
							</div>
							<div class="room-step">
								<span class="room-step-num">2</span>
								<div>
									<strong>{{ __('Practica') }}</strong>
									<p>{{ __('Ejercicios con feedback') }}</p>
								</div>
							</div>
							<div class="room-step">
								<span class="room-step-num">3</span>
								<div>
									<strong>{{ __('Comprueba') }}</strong>
									<p>{{ __('Quiz y checklist') }}</p>
								</div>
							</div>
						</div>
					</div>

					<!-- Explanation -->
					<div class="s-panel s-panel--flush" @mouseup="captureSelection">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker">{{ __('Paso 1') }}</div>
								<h2 class="s-panel-title">{{ __('Entiende el tema') }}</h2>
								<p class="s-panel-desc">{{ __('Lee de arriba hacia abajo. Si seleccionas un texto, el tutor puede explicarlo.') }}</p>
							</div>
						</div>
						<img v-if="diagramUrl" :src="diagramUrl" class="diagram-img" />
						<div v-if="lessonPack.lessonTitle || lessonPack.sections?.length" class="lesson-content">
							<div class="key-idea">
								<div class="key-idea-label"><Lightbulb class="h-4 w-4 stroke-1.5" /> {{ __('Idea clave') }}</div>
								<div class="key-idea-text markdown-inline" v-html="renderInlineMarkdown(lessonPack.keyIdea || __('Esta lección ya está lista para estudiar.'))" />
							</div>
							<div v-if="lessonPack.conceptCards?.length" class="concept-grid">
								<div v-for="card in lessonPack.conceptCards" :key="card.title" class="concept-card">
									<h3 class="concept-title markdown-inline" v-html="renderInlineMarkdown(card.title)" />
									<p class="concept-body markdown-inline" v-html="renderInlineMarkdown(card.body)" />
									<div v-if="card.formula" class="concept-formula markdown-inline" v-html="renderInlineMarkdown(card.formula)" />
								</div>
							</div>
							<div v-for="(section, index) in lessonPack.sections || []" :key="section.title" class="content-block">
								<div class="content-block-header">
									<span class="content-num">{{ index + 1 }}</span>
									<div>
										<h3 class="content-title markdown-inline" v-html="renderInlineMarkdown(section.title)" />
										<p class="content-summary markdown-inline" v-html="renderInlineMarkdown(section.summary)" />
									</div>
								</div>
								<ul class="content-points">
									<li v-for="point in section.keyPoints || []" :key="point">
										<span class="point-dot" />
										<span class="markdown-inline" v-html="renderInlineMarkdown(point)" />
									</li>
								</ul>
							</div>
							<div v-if="lessonWorkedExamples.length" class="content-block">
								<h3 class="content-title">{{ __('Ejemplo resuelto paso a paso') }}</h3>
								<div v-for="example in lessonWorkedExamples" :key="example.title || example.problem" class="worked-example">
									<div class="example-title markdown-inline" v-html="renderInlineMarkdown(example.title || example.problem)" />
									<p v-if="example.problem" class="example-problem markdown-inline" v-html="renderInlineMarkdown(example.problem)" />
									<ol class="example-steps">
										<li v-for="(step, index) in exampleSteps(example)" :key="index">
											<span class="content-num content-num--sm">{{ index + 1 }}</span>
											<span class="markdown-inline" v-html="renderInlineMarkdown(step)" />
										</li>
									</ol>
									<div v-if="exampleAnswer(example)" class="example-answer">
										<CheckCircle2 class="h-4 w-4 stroke-1.5" />
										<span class="markdown-inline" v-html="renderInlineMarkdown(exampleAnswer(example))" />
									</div>
								</div>
							</div>
							<div v-if="lessonPack.commonMistakes?.length" class="content-block">
								<h3 class="content-title">{{ __('Errores frecuentes') }}</h3>
								<div class="mistakes-list">
									<div v-for="mistake in lessonPack.commonMistakes" :key="mistake.mistake" class="mistake-item">
										<div class="mistake-bad"><AlertTriangle class="h-3.5 w-3.5 stroke-1.5" /> <span class="markdown-inline" v-html="renderInlineMarkdown(mistake.mistake)" /></div>
										<div class="mistake-fix markdown-inline" v-html="renderInlineMarkdown(mistake.fix)" />
									</div>
								</div>
							</div>
						</div>
						<div v-else class="s-empty">
							<div class="s-empty-icon"><RotateCcw class="h-8 w-8 stroke-1.5" /></div>
							<h3 class="s-empty-title">{{ __('Prepararemos esta lección automáticamente') }}</h3>
							<p class="s-empty-desc">{{ __('Si tarda, usa "Regenerar" para pedir una nueva versión.') }}</p>
						</div>
					</div>

					<!-- Practice Flow -->
					<div class="practice-flow mt-12">
						<div class="practice-flow-header">
							<div class="practice-flow-icon">
								<Zap class="h-6 w-6 stroke-1.5 text-indigo-500" />
							</div>
							<h3 class="practice-flow-title">{{ __('¿Estás preparado para practicar?') }}</h3>
							<p class="practice-flow-desc">{{ __('Pon a prueba lo que acabas de aprender. Completa los ejercicios guiados y luego demuestra tu dominio en el Quiz Final.') }}</p>
						</div>

						<div class="practice-flow-steps flex flex-col gap-8 mt-8">
							<div class="s-panel s-panel--flush practice-card">
								<div class="s-panel-header practice-card-header bg-indigo-50/30">
									<div>
										<div class="s-kicker text-indigo-600">{{ __('Paso 2') }}</div>
										<h2 class="s-panel-title text-indigo-900">{{ __('Práctica Guiada') }}</h2>
										<p class="s-panel-desc text-indigo-700/80">{{ __('Responde y revisa la explicación de cada opción. Ideal para asentar conocimientos.') }}</p>
									</div>
									<Button :label="__('Generar Práctica')" :loading="loading === 'exercises'" @click="generateExercises" variant="solid" theme="indigo">
										<template #prefix><Zap class="h-4 w-4 stroke-1.5" /></template>
									</Button>
								</div>
								<ExerciseList :items="lessonPack.practice?.length ? lessonPack.practice : exercises" @answer="handleAnswer" />
							</div>

							<div class="s-panel s-panel--flush practice-card">
								<div class="s-panel-header practice-card-header bg-violet-50/30">
									<div>
										<div class="s-kicker text-violet-600">{{ __('Paso 3') }}</div>
										<h2 class="s-panel-title text-violet-900">{{ __('Quiz Final') }}</h2>
										<p class="s-panel-desc text-violet-700/80">{{ __('Comprueba si puedes pasar a la siguiente lección respondiendo correctamente.') }}</p>
									</div>
									<Button :label="__('Generar Quiz')" :loading="loading === 'quiz'" @click="generateQuiz" variant="solid" theme="gray">
										<template #prefix><Trophy class="h-4 w-4 stroke-1.5" /></template>
									</Button>
								</div>
								<ExerciseList :items="lessonPack.quiz?.length ? lessonPack.quiz : quiz" @answer="handleQuizAnswer" />
								<div v-if="activeQuiz.length" class="quiz-score-banner">
									<Trophy class="h-7 w-7 stroke-1.5 text-amber-500" />
									<div class="flex flex-col">
										<span class="text-xs font-semibold text-amber-700/70 uppercase tracking-wider">{{ __('Puntaje final') }}</span>
										<strong class="text-2xl font-black text-amber-900 leading-none mt-1">{{ quizScore }}%</strong>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Room sidebar -->
				<aside class="flex flex-col gap-6 room-sidebar">
					<div v-if="isTutorExpanded" class="tutor-backdrop" @click="isTutorExpanded = false"></div>
					<div class="s-panel s-panel--flush tutor-panel" :class="{ 'is-expanded': isTutorExpanded }">
						<div class="sidebar-header flex justify-between items-center w-full">
							<div class="flex items-center gap-2">
								<MessageCircle class="h-4 w-4 stroke-1.5" />
								<h2 class="sidebar-title m-0">{{ __('Tutor contextual') }}</h2>
							</div>
							<button class="text-slate-400 hover:text-indigo-600 transition-colors bg-transparent border-none cursor-pointer" @click="isTutorExpanded = !isTutorExpanded" :title="__('Expandir/Contraer')">
								<Minimize2 v-if="isTutorExpanded" class="h-4 w-4 stroke-1.5" />
								<Maximize2 v-else class="h-4 w-4 stroke-1.5" />
							</button>
						</div>
						<p class="chat-hint">{{ __('Pregunta dudas o selecciona texto de la lección para pedir una explicación.') }}</p>
						<div ref="chatBox" class="chat-box">
							<div
								v-for="message in chatMessages"
								:key="message.id || message.content"
								class="chat-msg"
								:class="message.role === 'user' ? 'chat-msg--user' : 'chat-msg--ai'"
								v-html="renderMarkdown(message.content)"
							/>
						</div>
						<div class="chat-input-row">
							<textarea v-model="chatInput" class="s-textarea s-textarea--sm" rows="2" :placeholder="__('Pregunta sobre este tema')" @keydown.enter.exact.prevent="sendChat" />
							<Button :disabled="!chatInput.trim()" :loading="loading === 'chat'" @click="sendChat">
								<template #icon><SendHorizontal class="h-4 w-4 stroke-1.5" /></template>
							</Button>
						</div>
					</div>
					<div class="s-panel s-panel--flush">
						<div class="sidebar-header">
							<ListChecks class="h-4 w-4 stroke-1.5" />
							<h2 class="sidebar-title">{{ __('Checklist de dominio') }}</h2>
						</div>
						<div v-if="lessonPack.masteryChecklist?.length" class="checklist">
							<label v-for="item in lessonPack.masteryChecklist" :key="item" class="checklist-item">
								<input type="checkbox" class="checklist-box" @change="markProgress({ explanation_viewed: true })" />
								<span>{{ item }}</span>
							</label>
						</div>
						<div v-else class="s-mini-empty">
							<ListChecks class="h-5 w-5 stroke-1.5" />
							<span>{{ __('Termina la explicación para ver qué debes dominar.') }}</span>
						</div>
					</div>
					<div class="s-panel s-panel--flush">
						<div class="sidebar-header">
							<NotebookPen class="h-4 w-4 stroke-1.5" />
							<h2 class="sidebar-title">{{ __('Notas rápidas') }}</h2>
						</div>
						<textarea v-model="whiteboardText" class="s-textarea" rows="8" :placeholder="__('Fórmulas, dudas, errores frecuentes...')" @input="saveWhiteboard" />
					</div>
				</aside>
				<button class="tutor-fab" @click="isTutorExpanded = true" :title="__('Abrir tutor')">
					<MessageCircle class="h-5 w-5 stroke-1.5" />
					<span>{{ __('Tutor') }}</span>
				</button>
			</section>

			<!-- ═══════════ HISTORY ═══════════ -->
			<section v-else-if="isHistory" class="s-panel s-panel--flush">
				<div class="s-panel-header">
					<div>
						<div class="s-kicker"><History class="h-3.5 w-3.5 stroke-1.5" /> {{ __('Biblioteca') }}</div>
						<h2 class="s-panel-title">{{ __('Todos tus cursos IA') }}</h2>
						<p class="s-panel-desc">{{ __('Reanuda, revisa módulos o elimina cursos que ya no necesites.') }}</p>
					</div>
					<Button :label="__('Actualizar')" :loading="loading === 'dashboard'" @click="loadDashboard">
						<template #prefix><RefreshCw class="h-4 w-4 stroke-1.5" /></template>
					</Button>
				</div>
				<div class="courses-grid courses-grid--3">
					<div v-for="session in sessions" :key="session.name" class="course-card">
						<span class="course-tag" :class="`course-tag--${session.flow_id || session.goal || 'parcial'}`">{{ flowLabel(session.flow_id || session.goal) }}</span>
						<h3 class="course-card-title">{{ session.title || session.name }}</h3>
						<p class="course-card-date"><Clock class="h-3.5 w-3.5 stroke-1.5" /> {{ formatDate(session.modified) }}</p>
						<div class="course-progress-bar">
							<div class="progress-track">
								<div class="progress-fill" :style="{ width: `${courseProgress(session)}%` }" />
							</div>
						</div>
						<div class="course-actions">
							<Button :label="__('Continuar')" variant="solid" @click="openRoom(session.name, nextLessonIndex(session))" />
							<Button :label="__('Módulos')" @click="openPlan(session.name)" />
							<Button :label="__('Borrar')" variant="subtle" theme="red" @click="deleteSession(session.name)">
								<template #prefix><Trash2 class="h-3.5 w-3.5 stroke-1.5" /></template>
							</Button>
						</div>
					</div>
					<div v-if="!sessions.length" class="s-empty md:col-span-2 xl:col-span-3">
						<div class="s-empty-icon"><History class="h-8 w-8 stroke-1.5" /></div>
						<h3 class="s-empty-title">{{ __('Aún no hay historial') }}</h3>
						<p class="s-empty-desc">{{ __('Tus cursos aparecerán aquí cuando crees el primero.') }}</p>
					</div>
				</div>
			</section>

			<!-- ═══════════ STATISTICS ═══════════ -->
			<section v-else-if="isStatistics" class="stats-grid">
				<div v-for="metric in statisticsMetrics" :key="metric.label" class="stat-card">
					<div class="stat-card-label">{{ metric.label }}</div>
					<div class="stat-card-value">{{ metric.value }}</div>
					<div class="progress-track progress-track--sm">
						<div class="progress-fill" style="width: 50%" />
					</div>
				</div>
			</section>

			<!-- ═══════════ EXPLANATIONS ═══════════ -->
			<section v-else-if="isExplanations" class="s-panel s-panel--flush">
				<div class="s-panel-header">
					<div>
						<div class="s-kicker"><Star class="h-3.5 w-3.5 stroke-1.5" /> {{ __('Favoritos') }}</div>
						<h2 class="s-panel-title">{{ __('Explicaciones guardadas') }}</h2>
						<p class="s-panel-desc">{{ __('Aquí quedan las lecciones o fragmentos que quieras repasar después.') }}</p>
					</div>
				</div>
				<div class="explanations-list">
					<div v-for="item in explanations" :key="item.name" class="explanation-card">
						<div class="explanation-header">
							<div>
								<h3 class="explanation-title">{{ item.topic }}</h3>
								<p class="explanation-date">{{ formatDate(item.creation) }}</p>
							</div>
							<Button :label="__('Borrar')" variant="subtle" theme="red" @click="deleteExplanation(item.name)">
								<template #prefix><Trash2 class="h-3.5 w-3.5 stroke-1.5" /></template>
							</Button>
						</div>
						<div class="s-markdown-block" v-html="renderMarkdown(item.content)" />
					</div>
					<div v-if="!explanations.length" class="s-empty">
						<div class="s-empty-icon"><LibraryBig class="h-8 w-8 stroke-1.5" /></div>
						<h3 class="s-empty-title">{{ __('No guardaste explicaciones todavía') }}</h3>
						<p class="s-empty-desc">{{ __('En una lección, usa "Guardar favorito" para traerla aquí.') }}</p>
					</div>
				</div>
			</section>

			<!-- ═══════════ WHITEBOARD ═══════════ -->
			<section v-else-if="isWhiteboard" class="grid gap-6 xl:grid-cols-[1fr_340px]">
				<div class="s-panel s-panel--flush">
					<div class="s-panel-header">
						<div>
							<div class="s-kicker">{{ __('Espacio libre') }}</div>
							<h2 class="s-panel-title">{{ __('Pizarra') }}</h2>
							<p class="s-panel-desc">{{ __('Escribe fórmulas, dudas, pasos de solución o un resumen rápido.') }}</p>
						</div>
					</div>
					<textarea v-model="whiteboardText" class="s-textarea s-textarea--full" :placeholder="__('Escribe aquí tu resolución, fórmulas o lluvia de ideas.')" @input="saveWhiteboard" />
				</div>
				<aside class="s-panel s-panel--flush h-fit">
					<div class="sidebar-header">
						<Wand2 class="h-4 w-4 stroke-1.5" />
						<h2 class="sidebar-title">{{ __('Acciones IA') }}</h2>
					</div>
					<p class="chat-hint">{{ __('Convierte tus notas sueltas en una guía clara o revisa posibles errores.') }}</p>
					<div class="wb-actions">
						<Button :label="__('Ordenar mis notas')" :loading="loading === 'whiteboard'" @click="askWhiteboard('organiza')" />
						<Button :label="__('Encontrar errores')" :loading="loading === 'whiteboard'" @click="askWhiteboard('errores')" />
					</div>
					<div v-if="whiteboardResponse" class="s-markdown-block" v-html="renderMarkdown(whiteboardResponse)" />
				</aside>
			</section>
		</div>
	</div>
</template>

<script setup>
import { computed, defineComponent, h, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, FileUploader, FormControl, call, toast } from 'frappe-ui'
import MarkdownIt from 'markdown-it'
import mk from 'markdown-it-katex'
import 'katex/dist/katex.min.css'
import DOMPurify from 'dompurify'
import {
	AlertTriangle,
	ArrowRight,
	BarChart3,
	BookMarked,
	BookOpen,
	Brain,
	CalendarDays,
	CheckCircle2,
	ClipboardCheck,
	Clock,
	FileQuestion,
	FileText,
	GitBranch,
	GraduationCap,
	History,
	Layers,
	LibraryBig,
	Lightbulb,
	ListChecks,
	Maximize2,
	MessageCircle,
	Minimize2,
	NotebookPen,
	PanelTop,
	PlayCircle,
	RefreshCw,
	RotateCcw,
	SendHorizontal,
	Sparkles,
	Star,
	Trash2,
	Trophy,
	Upload,
	UserCog,
	Wand2,
	Zap,
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true }).use(mk)

const flows = [
	{ id: 'parcial', label: __('Parcial / Final'), icon: FileQuestion, description: __('Tengo un examen próximo y quiero practicar.') },
	{ id: 'admision', label: __('Admisión'), icon: GraduationCap, description: __('Busco prepararme para un proceso de admisión universitaria.') },
	{ id: 'recordar', label: __('Recordar'), icon: Brain, description: __('Ya estudié esto antes y quiero reforzar la memoria.') },
	{ id: 'cero', label: __('Desde cero'), icon: BookOpen, description: __('No sé nada del tema y quiero aprender desde el principio.') },
]

const topNav = [
	{ name: 'Study', label: __('Inicio'), icon: PanelTop },
	{ name: 'StudyHistory', label: __('Historial'), icon: History },
	{ name: 'StudyStatistics', label: __('Estadísticas'), icon: BarChart3 },
	{ name: 'StudyExplanations', label: __('Explicaciones'), icon: LibraryBig },
	{ name: 'StudyWhiteboard', label: __('Pizarra'), icon: NotebookPen },
]

const loading = ref('')
const sessions = ref([])
const explanations = ref([])
const currentSession = ref(null)
const profileAnswers = ref({})
const university = ref('')
const career = ref('')
const searchResult = ref('')
const fileUploader = ref(null)
const diagramUrl = ref('')
const exercises = ref([])
const quiz = ref([])
const lessonPack = ref({})
const activeLesson = ref({})
const chatMessages = ref([])
const chatInput = ref('')
const chatBox = ref(null)
const isTutorExpanded = ref(false)
const whiteboardText = ref(localStorage.getItem('studybadge_whiteboard') || '')
const whiteboardResponse = ref('')
const isPageLoading = ref(true)

const activeFlowStep = ref(1)

const draft = ref({
	title: '',
	academic_context: '',
	exam_date: '',
	student_level: 'universitario',
	desired_topics: '',
	manual_text: '',
})

const pageName = computed(() => route.name)
const flowId = computed(() => route.params.flowId || currentSession.value?.flow_id || 'parcial')
const sessionId = computed(() => route.params.sessionId)
const topicIndex = computed(() => Number(route.params.topicIndex || 0))
const isDashboard = computed(() => pageName.value === 'Study')
const isFlow = computed(() => pageName.value === 'StudyFlow')
const isPlan = computed(() => pageName.value === 'StudyPlan')
const isRoom = computed(() => pageName.value === 'StudyRoom')
const isHistory = computed(() => pageName.value === 'StudyHistory')
const isStatistics = computed(() => pageName.value === 'StudyStatistics')
const isExplanations = computed(() => pageName.value === 'StudyExplanations')
const isWhiteboard = computed(() => pageName.value === 'StudyWhiteboard')

const activeTopic = computed(() => (currentSession.value?.topics || [])[topicIndex.value] || null)
const activeTopicTitle = computed(() => activeLesson.value?.title || activeTopic.value?.title || activeTopic.value || __('Tema de estudio'))
const courseStructure = computed(() => currentSession.value?.course_structure || fallbackCourseStructure(currentSession.value))
const lessonsFlat = computed(() => flattenLessons(courseStructure.value))
const activeQuiz = computed(() => lessonPack.value?.quiz?.length ? lessonPack.value.quiz : quiz.value)
const hasCourseSeed = computed(() => {
	const session = currentSession.value
	if (!session) return false
	return Boolean((session.topics || []).length || session.manual_text || session.desired_topics || draft.value.manual_text || draft.value.desired_topics)
})
const canGenerateQuestions = computed(() => Boolean(currentSession.value && hasCourseSeed.value))
const canCreateFullCourse = computed(() => Boolean(currentSession.value && hasCourseSeed.value && currentSession.value?.profile_questions?.length))
const quizScore = computed(() => {
	if (!activeQuiz.value.length) return 0
	const answered = activeQuiz.value.filter((item) => item.selected !== undefined)
	if (!answered.length) return 0
	const correct = answered.filter((item) => item.selected === Number(item.correct || 0)).length
	return Math.round((correct / activeQuiz.value.length) * 100)
})
const lessonWorkedExamples = computed(() => {
	const direct = lessonPack.value?.workedExamples || []
	if (direct.length) return direct
	return (lessonPack.value?.sections || [])
		.filter((section) => section.workedExample)
		.map((section, index) => ({
			title: section.title || `${__('Ejemplo')} ${index + 1}`,
			problem: section.summary || '',
			steps: Array.isArray(section.workedExample) ? section.workedExample : [section.workedExample],
			answer: section.answer || section.result || '',
		}))
})
const studyPackMarkdown = computed(() => {
	const pack = currentSession.value?.study_pack || {}
	if (!pack.sections?.length) return __('Genera un pack de estudio para ver la explicación completa.')
	return pack.sections.map((section, index) => {
		const points = (section.keyPoints || []).map((point) => `- ${point}`).join('\n')
		return `## ${index + 1}. ${section.title || __('Sección')}\n\n${section.summary || ''}\n\n${points}\n\n${section.workedExample ? `### ${__('Ejemplo resuelto')}\n${section.workedExample}` : ''}`
	}).join('\n\n')
})
const dashboardMetrics = computed(() => [
	{ label: __('Sesiones'), value: sessions.value.length },
	{ label: __('Temas'), value: sessions.value.reduce((total, item) => total + (item.topics?.length || 0), 0) },
	{ label: __('Horas'), value: Math.round(sessions.value.reduce((total, item) => total + (item.study_time_seconds || 0), 0) / 3600) },
])
const statisticsMetrics = computed(() => [
	...dashboardMetrics.value,
	{ label: __('Explicaciones'), value: explanations.value.length },
	{ label: __('Quiz promedio'), value: `${averageQuiz.value}%` },
	{ label: __('Planes'), value: sessions.value.filter((item) => item.weekly_plan?.length).length },
])
const averageQuiz = computed(() => {
	const scored = sessions.value.filter((item) => item.quiz_score)
	if (!scored.length) return 0
	return Math.round(scored.reduce((total, item) => total + Number(item.quiz_score || 0), 0) / scored.length)
})
const headerTitle = computed(() => {
	if (isFlow.value) return flowLabel(flowId.value)
	if (isPlan.value) return __('Malla del curso')
	if (isRoom.value) return __('Lección guiada')
	if (isHistory.value) return __('Historial')
	if (isStatistics.value) return __('Estadísticas')
	if (isExplanations.value) return __('Explicaciones guardadas')
	if (isWhiteboard.value) return __('Pizarra IA')
	return __('Cursos IA')
})
const headerSubtitle = computed(() => {
	if (isDashboard.value) return __('Crea cursos propios con IA, organizados en módulos, lecciones y práctica paso a paso.')
	if (isFlow.value) return __('Te guiamos desde tus materiales hasta un curso completo listo para estudiar.')
	if (isRoom.value) return __('Aprende una lección con explicación, práctica, quiz, tutor y diagrama.')
	return __('Todo se guarda en StudyBadge para que puedas retomarlo luego.')
})
const pageTitle = computed(() => (isDashboard.value ? '' : headerTitle.value))

onMounted(async () => {
	isPageLoading.value = true
	try {
		await loadDashboard()
		await loadRouteSession()
	} finally {
		isPageLoading.value = false
	}
})

watch(() => route.fullPath, loadRouteSession)

function sanitizeRenderedMarkdown(html) {
	return DOMPurify.sanitize(html, {
		ADD_TAGS: ['math', 'mrow', 'mi', 'mo', 'mn', 'ms', 'mspace', 'mtext', 'menclose', 'merror', 'mfrac', 'mpadded', 'mphantom', 'mroot', 'mrow', 'msqrt', 'mstyle', 'mmultiscripts', 'mover', 'mprescripts', 'msub', 'msubsup', 'msup', 'munder', 'munderover', 'none', 'semantics', 'annotation', 'annotation-xml'],
		ADD_ATTR: ['mathvariant', 'mathcolor', 'mathsize', 'mathbackground', 'dir', 'display', 'class', 'style', 'aria-hidden', 'xmlns', 'encoding'],
	})
}

function renderMarkdown(text) {
	if (!text) return ''
	return sanitizeRenderedMarkdown(markdown.render(String(text)))
}

function renderInlineMarkdown(text) {
	if (!text) return ''
	return sanitizeRenderedMarkdown(markdown.renderInline(String(text)))
}

function exampleSteps(example = {}) {
	const steps = example.steps || example.solutionSteps || example.solution || example.workedExample || []
	if (Array.isArray(steps)) return steps.filter(Boolean)
	return String(steps).split(/\n+/).map((step) => step.trim()).filter(Boolean)
}

function exampleAnswer(example = {}) {
	return example.answer || example.result || example.finalAnswer || ''
}

function flowLabel(id) {
	return flows.find((flow) => flow.id === id)?.label || __('Estudiar')
}

function formatDate(value) {
	if (!value) return ''
	return new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date(value))
}

async function api(method, params = {}, state = '') {
	if (state) loading.value = state
	try {
		return await call(`studybadge_ai.ai_study.${method}`, params)
	} catch (error) {
		toast.error(error.messages?.[0] || error.message || __('Ocurrió un error.'))
		throw error
	} finally {
		if (state) loading.value = ''
	}
}

async function loadDashboard() {
	loading.value = 'dashboard'
	try {
		sessions.value = await api('list_sessions')
		explanations.value = await api('list_explanations')
	} finally {
		loading.value = ''
	}
}

async function loadRouteSession() {
	if (!sessionId.value) return
	currentSession.value = await api('get_session', { name: sessionId.value })
	applySessionToDraft()
	exercises.value = markSelectable(currentSession.value.exercises || [])
	quiz.value = markSelectable(currentSession.value.quiz_questions || [])
	lessonPack.value = currentSession.value.study_pack || {}
	activeLesson.value = lessonsFlat.value[topicIndex.value] || {}
	chatMessages.value = (currentSession.value.chat_history || []).map((item, index) => ({ ...item, id: index }))
	if (isRoom.value) {
		await loadLesson()
	}
}

function applySessionToDraft() {
	if (!currentSession.value) return
	draft.value = {
		title: currentSession.value.title || '',
		academic_context: currentSession.value.academic_context || '',
		exam_date: currentSession.value.exam_date || '',
		student_level: currentSession.value.student_level || 'universitario',
		desired_topics: currentSession.value.desired_topics || '',
		manual_text: currentSession.value.manual_text || '',
	}
	profileAnswers.value = currentSession.value.profile_answers || {}
}

function startFlow(id) {
	router.push({ name: 'StudyFlow', params: { flowId: id } })
}

async function createOrUpdateSession() {
	if (currentSession.value) {
		currentSession.value = await api('update_session', { name: currentSession.value.name, data: draft.value }, 'create')
		toast.success(__('Curso actualizado.'))
		goToStep(2)
		return
	}
	currentSession.value = await api('create_session', { data: { ...draft.value, flow_id: flowId.value, goal: flowId.value } }, 'create')
	toast.success(__('Curso creado.'))
	goToStep(2)
}

async function saveProfileAndContinue() {
	if (!currentSession.value) return
	loading.value = 'profile'
	try {
		currentSession.value = await api('update_session', { name: currentSession.value.name, data: { profile_answers: profileAnswers.value } })
		goToStep(4)
	} finally {
		loading.value = ''
	}
}

function goToStep(step) {
	if (step === 2 && !currentSession.value && !hasCourseSeed.value) return
	if (step === 3 && !canGenerateQuestions.value) return
	if (step === 4 && !canCreateFullCourse.value) return
	activeFlowStep.value = step
	window.scrollTo({ top: 0, behavior: 'smooth' })
}

function openPlan(name) {
	router.push({ name: 'StudyPlan', params: { sessionId: name } })
}

function openRoom(name, index = 0) {
	router.push({ name: 'StudyRoom', params: { sessionId: name, topicIndex: index } })
}

function flattenLessons(structure = {}) {
	const lessons = []
	;(structure.modules || []).forEach((module, moduleIndex) => {
		;(module.lessons || []).forEach((lesson, lessonIndex) => {
			lessons.push({ ...lesson, moduleTitle: module.title, moduleIndex, lessonIndex })
		})
	})
	return lessons
}

function fallbackCourseStructure(session) {
	const topics = session?.topics || []
	return {
		courseTitle: session?.title || __('Curso IA personal'),
		courseGoal: session?.goal || '',
		modules: [
			{
				title: __('Módulo principal'),
				objective: __('Dominar los temas detectados.'),
				lessons: topics.map((topic, index) => ({
					key: `lesson-${index + 1}`,
					title: topic.title || topic,
					objective: topic.why || __('Aprender y practicar este tema.'),
					difficulty: topic.difficulty || __('medio'),
					duration: __('30 min'),
				})),
			},
		],
	}
}

function lessonGlobalIndex(lesson) {
	return Math.max(0, lessonsFlat.value.findIndex((item) => (item.key && item.key === lesson.key) || item.title === lesson.title))
}

function isLessonDone(lesson) {
	return Boolean(currentSession.value?.lesson_progress?.[lesson.key]?.completed || currentSession.value?.completed_topics?.[lesson.key])
}

function courseProgress(session) {
	const lessons = flattenLessons(session?.course_structure || fallbackCourseStructure(session))
	if (!lessons.length) return 0
	const progress = session?.lesson_progress || {}
	const completed = lessons.filter((lesson) => progress[lesson.key]?.completed || session?.completed_topics?.[lesson.key]).length
	return Math.round((completed / lessons.length) * 100)
}

function nextLessonIndex(session) {
	const lessons = flattenLessons(session?.course_structure || fallbackCourseStructure(session))
	const progress = session?.lesson_progress || {}
	const index = lessons.findIndex((lesson) => !progress[lesson.key]?.completed && !session?.completed_topics?.[lesson.key])
	return index >= 0 ? index : 0
}

function validateFile(file) {
	const ext = file.name.split('.').pop().toLowerCase()
	if (!['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'webp', 'txt', 'md'].includes(ext)) {
		return __('Usa PDF, imágenes, Word o texto.')
	}
	if (file.size > 25 * 1024 * 1024) return __('El archivo supera 25 MB.')
}

function openUploader() {
	const input = fileUploader.value?.$el?.querySelector('input[type="file"]')
	input?.click()
}

async function handleFileUploaded(file) {
	if (!currentSession.value) return
	currentSession.value = await api('upload_material', { session: currentSession.value.name, file_url: file.file_url })
	toast.success(__('Archivo agregado.'))
}

async function searchTemario() {
	const result = await api('search_university_temario', { university: university.value, career: career.value }, 'search')
	searchResult.value = result.content
	draft.value.manual_text = [draft.value.manual_text, result.content].filter(Boolean).join('\n\n')
}

async function analyzeMaterial() {
	currentSession.value = await api('analyze_material', { session: currentSession.value.name }, 'analyze')
	toast.success(__('Material analizado.'))
}

async function generateQuestions() {
	if (!canGenerateQuestions.value) {
		toast.warning(__('Primero agrega temas, texto o material analizado.'))
		return
	}
	const result = await api('generate_profile_questions', { session: currentSession.value.name }, 'questions')
	currentSession.value.profile_questions = result.questions
	toast.success(__('Preguntas generadas.'))
}

async function generatePlan() {
	if (!canCreateFullCourse.value) {
		toast.warning(__('Completa el perfil de aprendizaje antes de crear el curso.'))
		return
	}
	const result = await api('generate_plan', { session: currentSession.value.name, profile_answers: profileAnswers.value }, 'plan')
	currentSession.value = result.session
	toast.success(__('Plan creado.'))
	router.push({ name: 'StudyPlan', params: { sessionId: currentSession.value.name } })
}

async function loadLesson() {
	if (!currentSession.value) return
	const result = await api('get_lesson', { session: currentSession.value.name, topic_index: topicIndex.value, auto_generate: 1 }, 'lesson')
	activeLesson.value = result.lesson || activeLesson.value
	lessonPack.value = normalizeLessonPack(result.study_pack || {})
	currentSession.value.study_pack = lessonPack.value
	if (result.cached === false) toast.success(__('Lección preparada y guardada automáticamente.'))
}

async function generatePack(force = false) {
	const result = await api('generate_study_pack', { session: currentSession.value.name, topic: activeTopicTitle.value, level: currentSession.value.student_level, topic_index: topicIndex.value, lesson_key: activeLesson.value?.key, force }, 'pack')
	activeLesson.value = result.lesson || activeLesson.value
	lessonPack.value = normalizeLessonPack(result.study_pack || {})
	currentSession.value.study_pack = lessonPack.value
}

async function generateDiagram() {
	const result = await api('generate_diagram_image', { session: currentSession.value.name, topic: activeTopicTitle.value }, 'diagram')
	diagramUrl.value = `data:${result.mime_type};base64,${result.image_base64}`
}

async function generateExercises() {
	const result = await api('generate_exercises', { session: currentSession.value.name, topic: activeTopicTitle.value, difficulty: 'medio' }, 'exercises')
	exercises.value = markSelectable(result.exercises || [])
	lessonPack.value.practice = exercises.value
}

async function generateQuiz() {
	const result = await api('generate_quiz', { session: currentSession.value.name, topic: activeTopicTitle.value }, 'quiz')
	quiz.value = markSelectable(result.quiz || [])
	lessonPack.value.quiz = quiz.value
}

function markSelectable(items) {
	return (items || []).map((item) => ({ ...item, selected: item.selected ?? undefined }))
}

function handleAnswer({ item, index }) {
	item.selected = index
	markProgress({ exercises_answered: true })
}

async function handleQuizAnswer({ item, index }) {
	item.selected = index
	const completed = activeQuiz.value.every((q) => q.selected !== undefined)
	await api('update_session', {
		name: currentSession.value.name,
		data: { quiz_questions: activeQuiz.value, quiz_score: quizScore.value, quiz_done: completed },
	})
	if (completed) await markProgress({ quiz_completed: true, completed: true, quiz_score: quizScore.value })
}

async function sendChat() {
	const text = chatInput.value.trim()
	if (!text) return
	chatMessages.value.push({ id: Date.now(), role: 'user', content: text })
	chatInput.value = ''
	await nextTick(scrollChat)
	const result = await api('chat', { session: currentSession.value.name, message: text, history: chatMessages.value }, 'chat')
	chatMessages.value = result.history.map((item, index) => ({ ...item, id: index }))
	await nextTick(scrollChat)
}

function scrollChat() {
	if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}

function captureSelection() {
	const text = window.getSelection()?.toString()?.trim()
	if (text && text.length > 12) {
		chatInput.value = `${__('Explícame este fragmento')}: ${text}`
	}
}

async function saveCurrentExplanation() {
	await api('save_explanation', { session: currentSession.value.name, topic: activeTopicTitle.value, content: JSON.stringify(lessonPack.value, null, 2) })
	toast.success(__('Explicación guardada.'))
	await loadDashboard()
}

async function markProgress(data) {
	if (!currentSession.value || !activeLesson.value?.key) return
	const result = await api('record_lesson_progress', { session: currentSession.value.name, lesson_key: activeLesson.value.key, data })
	currentSession.value = result.session || currentSession.value
}

function normalizeLessonPack(pack = {}) {
	return {
		lessonTitle: pack.lessonTitle || pack.title || activeLesson.value?.title || activeTopicTitle.value,
		learningObjective: pack.learningObjective || activeLesson.value?.objective || '',
		difficulty: pack.difficulty || activeLesson.value?.difficulty || 'medio',
		estimatedTime: pack.estimatedTime || activeLesson.value?.duration || '30 min',
		keyIdea: pack.keyIdea || '',
		conceptCards: pack.conceptCards || [],
		sections: pack.sections || [],
		workedExamples: pack.workedExamples || [],
		commonMistakes: pack.commonMistakes || [],
		practice: markSelectable(pack.practice || []),
		quiz: markSelectable(pack.quiz || []),
		masteryChecklist: pack.masteryChecklist || [],
	}
}

async function deleteSession(name) {
	if (!window.confirm(__('¿Borrar este curso IA y sus explicaciones guardadas?'))) return
	await api('delete_session', { name })
	toast.success(__('Curso borrado.'))
	if (currentSession.value?.name === name) currentSession.value = null
	await loadDashboard()
	if (route.params.sessionId === name) router.push({ name: 'Study' })
}

async function deleteExplanation(name) {
	await api('delete_explanation', { name })
	explanations.value = explanations.value.filter((item) => item.name !== name)
}

function saveWhiteboard() {
	localStorage.setItem('studybadge_whiteboard', whiteboardText.value)
}

async function askWhiteboard(mode) {
	const session = currentSession.value || sessions.value[0]
	if (!session) {
		toast.warning(__('Crea un curso primero.'))
		return
	}
	const prompt = mode === 'errores'
		? `${__('Encuentra errores o huecos en estas notas')}:\n${whiteboardText.value}`
		: `${__('Organiza estas notas como guía de estudio')}:\n${whiteboardText.value}`
	const result = await api('chat', { session: session.name, message: prompt, history: [] }, 'whiteboard')
	whiteboardResponse.value = result.reply
}

const ExerciseList = defineComponent({
	props: { items: { type: Array, default: () => [] } },
	emits: ['answer'],
	setup(props, { emit }) {
		const cls = (item, index) => {
			if (item.selected === undefined) return 'quiz-option quiz-option--default'
			if (index === Number(item.correct || 0)) return 'quiz-option quiz-option--correct'
			if (index === item.selected) return 'quiz-option quiz-option--wrong'
			return 'quiz-option quiz-option--dimmed'
		}
		const icon = (item, index) => {
			if (item.selected === undefined) return null
			if (index === Number(item.correct || 0)) return h('span', { class: 'quiz-option-icon quiz-option-icon--correct' }, '✓')
			if (index === item.selected) return h('span', { class: 'quiz-option-icon quiz-option-icon--wrong' }, '✗')
			return null
		}
		return () => h('div', { class: 'exercise-list' }, props.items.length
			? props.items.map((item, itemIndex) => h('div', { class: 'exercise-item' }, [
				h('div', { class: 'exercise-question-row' }, [
					h('span', { class: 'exercise-question-num' }, String(itemIndex + 1)),
					h('span', { class: 'exercise-question-text markdown-inline', innerHTML: renderInlineMarkdown(item.question) }),
				]),
				h('div', { class: 'exercise-options' }, (item.options || []).map((option, index) =>
					h('button', {
						class: cls(item, index),
						onClick: () => emit('answer', { item, index }),
						disabled: item.selected !== undefined,
					}, [
						h('span', { class: 'quiz-option-letter' }, String.fromCharCode(65 + index)),
						h('span', { class: 'quiz-option-content markdown-inline', innerHTML: renderInlineMarkdown(option) }),
						icon(item, index),
					])
				)),
				item.selected !== undefined && item.explanation
					? h('div', { class: 'exercise-explanation' }, [
						h('div', { class: 'exercise-explanation-label' }, [
							h('span', { class: 'exercise-explanation-icon' }, '💡'),
							h('span', {}, __('Explicación')),
						]),
						h('p', { class: 'exercise-explanation-text markdown-inline', innerHTML: renderInlineMarkdown(item.explanation) }),
					])
					: null,
			]))
			: h('div', { class: 's-empty-sm' }, [
				h('span', { class: 'text-ink-gray-5' }, __('Genera contenido para empezar.')),
			]))
	},
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════
   STUDYBADGE STUDY PAGE — UI REDESIGN
   Mantiene lógica original. Mejora PC + móvil.
   Color principal: #0A2251
   ═══════════════════════════════════════════════ */

.study-page {
	min-height: 100vh;
	background:
		radial-gradient(circle at top left, rgba(10, 34, 81, 0.08), transparent 34rem),
		linear-gradient(180deg, #f5f8fc 0%, #eef4fb 42%, #f8fafc 100%);
	color: #0f172a;
}

/* ═══════════════════════════════════════════════
   HERO
   ═══════════════════════════════════════════════ */

.study-hero {
	position: relative;
	overflow: hidden;
	border-radius: 28px;
	background: #0a2251;
	padding: 2rem;
	color: #ffffff;
	box-shadow: 0 24px 60px rgba(10, 34, 81, 0.16);
	isolation: isolate;
}

.study-hero::before {
	content: '';
	position: absolute;
	inset: 0;
	background:
		radial-gradient(circle at 88% 12%, rgba(245, 179, 1, 0.28), transparent 17rem),
		radial-gradient(circle at 16% 84%, rgba(255, 255, 255, 0.14), transparent 20rem);
	z-index: -2;
}

.study-hero::after {
	content: '';
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(rgba(255, 255, 255, 0.055) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255, 255, 255, 0.055) 1px, transparent 1px);
	background-size: 34px 34px;
	mask-image: linear-gradient(90deg, transparent, #000 15%, #000 85%, transparent);
	opacity: 0.45;
	z-index: -1;
}

.hero-decoration {
	position: absolute;
	inset: 0;
	pointer-events: none;
	overflow: hidden;
}

.hero-orb {
	position: absolute;
	border-radius: 999px;
	filter: blur(52px);
	opacity: 0.28;
}

.hero-orb--1 {
	top: -42px;
	right: -26px;
	width: 210px;
	height: 210px;
	background: #f5b301;
}

.hero-orb--2 {
	left: 8%;
	bottom: -70px;
	width: 230px;
	height: 230px;
	background: rgba(255, 255, 255, 0.28);
}

.hero-orb--3 {
	top: 42%;
	right: 26%;
	width: 120px;
	height: 120px;
	background: rgba(88, 166, 255, 0.45);
}

.hero-content {
	position: relative;
	z-index: 1;
	display: grid;
	grid-template-columns: minmax(0, 1fr) auto;
	gap: 1.5rem;
	align-items: end;
}

.hero-text {
	min-width: 0;
	display: flex;
	flex-direction: column;
	gap: 0.65rem;
}

.hero-breadcrumb {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	width: fit-content;
	border: 1px solid rgba(255, 255, 255, 0.18);
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.1);
	padding: 0.45rem 0.7rem;
	font-size: 0.76rem;
	font-weight: 800;
	backdrop-filter: blur(14px);
}

.hero-breadcrumb-link {
	color: rgba(255, 255, 255, 0.92);
	text-decoration: none;
	transition: color 0.18s ease;
}

.hero-breadcrumb-link:hover {
	color: #ffffff;
}

.hero-breadcrumb-sep {
	color: rgba(255, 255, 255, 0.42);
}

.hero-breadcrumb-current {
	color: rgba(255, 255, 255, 0.7);
}

.hero-title {
	margin: 0;
	max-width: 780px;
	color: #ffffff;
	font-size: clamp(2rem, 4.8vw, 4.25rem);
	font-weight: 950;
	letter-spacing: -0.06em;
	line-height: 1.02;
}

.hero-subtitle {
	margin: 0;
	max-width: 640px;
	color: rgba(255, 255, 255, 0.78);
	font-size: 1rem;
	line-height: 1.75;
}

.hero-actions {
	display: flex;
	justify-content: flex-end;
	min-width: 0;
}

.hero-nav {
	display: flex;
	flex-wrap: wrap;
	justify-content: flex-end;
	gap: 0.5rem;
	max-width: 520px;
}

.nav-pill {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.45rem;
	min-height: 40px;
	border-radius: 999px;
	border: 1px solid rgba(255, 255, 255, 0.18);
	background: rgba(255, 255, 255, 0.08);
	padding: 0.62rem 0.85rem;
	color: rgba(255, 255, 255, 0.84);
	font-size: 0.82rem;
	font-weight: 900;
	text-decoration: none;
	backdrop-filter: blur(14px);
	transition:
		transform 0.18s ease,
		background 0.18s ease,
		border-color 0.18s ease,
		color 0.18s ease,
		box-shadow 0.18s ease;
}

.nav-pill:hover {
	transform: translateY(-1px);
	border-color: rgba(255, 255, 255, 0.32);
	background: rgba(255, 255, 255, 0.14);
	color: #ffffff;
}

.nav-pill--active {
	border-color: rgba(255, 255, 255, 0.42);
	background: #ffffff;
	color: #0a2251;
	box-shadow: 0 16px 34px rgba(0, 0, 0, 0.16);
}

.nav-pill-label {
	display: inline;
}

/* ═══════════════════════════════════════════════
   PANELS
   ═══════════════════════════════════════════════ */

.s-panel {
	position: relative;
	overflow: hidden;
	border: 1px solid rgba(148, 163, 184, 0.22);
	border-radius: 24px;
	background: rgba(255, 255, 255, 0.9);
	box-shadow:
		0 16px 42px rgba(15, 23, 42, 0.055),
		0 1px 0 rgba(255, 255, 255, 0.85) inset;
	backdrop-filter: blur(16px);
	transition:
		transform 0.2s ease,
		box-shadow 0.2s ease,
		border-color 0.2s ease,
		background 0.2s ease;
}

.s-panel:hover {
	border-color: rgba(10, 34, 81, 0.16);
	box-shadow:
		0 24px 54px rgba(15, 23, 42, 0.075),
		0 1px 0 rgba(255, 255, 255, 0.85) inset;
}

.s-panel--flush > * {
	padding-left: 1.35rem;
	padding-right: 1.35rem;
}

.s-panel--flush > *:first-child {
	padding-top: 1.35rem;
}

.s-panel--flush > *:last-child {
	padding-bottom: 1.35rem;
}

.s-panel--locked {
	background: rgba(248, 250, 252, 0.84);
	opacity: 0.72;
}

.s-panel--locked :deep(button),
.s-panel--locked .s-select,
.s-panel--locked .s-textarea {
	cursor: not-allowed;
}

.s-panel-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
	border-bottom: 1px solid rgba(226, 232, 240, 0.86);
	padding-bottom: 1.05rem;
}

.s-panel-title {
	margin: 0.25rem 0 0;
	color: #0a2251;
	font-size: 1.18rem;
	font-weight: 950;
	letter-spacing: -0.035em;
	line-height: 1.15;
}

.s-panel-desc {
	margin: 0.35rem 0 0;
	max-width: 46rem;
	color: #64748b;
	font-size: 0.9rem;
	line-height: 1.65;
}

.s-kicker {
	display: inline-flex;
	align-items: center;
	gap: 0.4rem;
	width: fit-content;
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.07);
	padding: 0.36rem 0.62rem;
	color: #0a2251;
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

/* ═══════════════════════════════════════════════
   FLOW CARDS
   ═══════════════════════════════════════════════ */

.flow-grid {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 0.9rem;
	padding-top: 1rem;
}

.flow-card {
	position: relative;
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	gap: 0.85rem;
	min-height: 150px;
	border: 1px solid rgba(226, 232, 240, 0.95);
	border-radius: 22px;
	background:
		linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 252, 0.86));
	padding: 1.15rem;
	text-align: left;
	cursor: pointer;
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease,
		background 0.18s ease;
}

.flow-card::after {
	content: '';
	position: absolute;
	inset: auto 1rem 0.85rem 1rem;
	height: 3px;
	border-radius: 999px;
	background: linear-gradient(90deg, #0a2251, rgba(245, 179, 1, 0.8));
	opacity: 0;
	transform: scaleX(0.6);
	transform-origin: left;
	transition: 0.18s ease;
}

.flow-card:hover {
	transform: translateY(-3px);
	border-color: rgba(10, 34, 81, 0.18);
	background: #ffffff;
	box-shadow: 0 20px 42px rgba(10, 34, 81, 0.1);
}

.flow-card:hover::after {
	opacity: 1;
	transform: scaleX(1);
}

.flow-icon {
	display: grid;
	width: 46px;
	height: 46px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 17px;
	box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
}

.flow-icon--parcial {
	background: rgba(245, 179, 1, 0.18);
	color: #8a6100;
}

.flow-icon--admision {
	background: rgba(10, 34, 81, 0.1);
	color: #0a2251;
}

.flow-icon--recordar {
	background: rgba(99, 102, 241, 0.1);
	color: #4338ca;
}

.flow-icon--cero {
	background: rgba(34, 197, 94, 0.12);
	color: #15803d;
}

.flow-info {
	min-width: 0;
	flex: 1;
}

.flow-card-title {
	margin: 0;
	color: #0f172a;
	font-size: 0.95rem;
	font-weight: 950;
	letter-spacing: -0.025em;
	line-height: 1.18;
}

.flow-card-desc {
	margin: 0.35rem 0 0;
	color: #64748b;
	font-size: 0.82rem;
	line-height: 1.5;
}

.flow-arrow {
	position: absolute;
	top: 1.3rem;
	right: 1.15rem;
	width: 18px;
	height: 18px;
	flex-shrink: 0;
	color: #cbd5e1;
	transition: transform 0.18s ease, color 0.18s ease;
}

.flow-card:hover .flow-arrow {
	transform: translateX(4px);
	color: #0a2251;
}

/* ═══════════════════════════════════════════════
   COURSE CARDS
   ═══════════════════════════════════════════════ */

.courses-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 1rem;
	padding-top: 1rem;
}

.courses-grid--3 {
	grid-template-columns: repeat(3, minmax(0, 1fr));
}

.course-card {
	position: relative;
	display: flex;
	min-width: 0;
	flex-direction: column;
	gap: 0.9rem;
	border: 1px solid rgba(226, 232, 240, 0.96);
	border-radius: 24px;
	background: #ffffff;
	padding: 1.1rem;
	box-shadow: 0 12px 30px rgba(15, 23, 42, 0.045);
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease;
}

.course-card::before {
	content: '';
	position: absolute;
	top: 1rem;
	bottom: 1rem;
	left: 0;
	width: 4px;
	border-radius: 999px;
	background: #0a2251;
	opacity: 0.85;
}

.course-card:hover {
	transform: translateY(-2px);
	border-color: rgba(10, 34, 81, 0.18);
	box-shadow: 0 22px 46px rgba(10, 34, 81, 0.09);
}

.course-card-top {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 0.9rem;
	min-width: 0;
}

.course-tag {
	display: inline-flex;
	align-items: center;
	width: fit-content;
	border-radius: 999px;
	padding: 0.28rem 0.6rem;
	font-size: 0.65rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.course-tag--parcial {
	background: rgba(245, 179, 1, 0.16);
	color: #7a5600;
}

.course-tag--admision {
	background: rgba(10, 34, 81, 0.09);
	color: #0a2251;
}

.course-tag--recordar {
	background: rgba(99, 102, 241, 0.1);
	color: #4338ca;
}

.course-tag--cero {
	background: rgba(34, 197, 94, 0.12);
	color: #166534;
}

.course-card-title {
	margin: 0.48rem 0 0;
	color: #0f172a;
	font-size: 1.08rem;
	font-weight: 950;
	letter-spacing: -0.04em;
	line-height: 1.18;
}

.course-card-date {
	display: flex;
	align-items: center;
	gap: 0.35rem;
	margin: 0.4rem 0 0;
	color: #64748b;
	font-size: 0.78rem;
	font-weight: 700;
}

.course-progress-ring {
	position: relative;
	width: 54px;
	height: 54px;
	flex: 0 0 auto;
}

.course-progress-ring svg {
	width: 54px;
	height: 54px;
	transform: rotate(-90deg);
}

.ring-bg {
	fill: none;
	stroke: #e2e8f0;
	stroke-width: 3.5;
}

.ring-fill {
	fill: none;
	stroke: #0a2251;
	stroke-linecap: round;
	stroke-width: 3.5;
}

.ring-text {
	position: absolute;
	inset: 0;
	display: grid;
	place-items: center;
	color: #0a2251;
	font-size: 0.72rem;
	font-weight: 950;
}

.course-progress-bar {
	display: grid;
	gap: 0.45rem;
}

.progress-track {
	overflow: hidden;
	width: 100%;
	height: 8px;
	border-radius: 999px;
	background: #e8eef6;
}

.progress-track--sm {
	height: 6px;
}

.progress-track--lg {
	height: 10px;
}

.progress-fill {
	height: 100%;
	border-radius: inherit;
	background: linear-gradient(90deg, #0a2251, #17437f);
	box-shadow: 0 0 18px rgba(10, 34, 81, 0.26);
	transition: width 0.25s ease;
}

.progress-label {
	color: #64748b;
	font-size: 0.75rem;
	font-weight: 800;
}

.course-next {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	border-radius: 18px;
	background: #f5f8fc;
	padding: 0.75rem;
}

.course-next-icon {
	display: grid;
	width: 36px;
	height: 36px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 14px;
	background: #0a2251;
	color: #ffffff;
}

.course-next-label {
	color: #64748b;
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.course-next-title {
	overflow: hidden;
	color: #0f172a;
	font-size: 0.86rem;
	font-weight: 900;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.course-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.55rem;
}

/* ═══════════════════════════════════════════════
   SIDEBAR / METRICS
   ═══════════════════════════════════════════════ */

.sidebar-header {
	display: flex;
	align-items: center;
	gap: 0.55rem;
	border-bottom: 1px solid rgba(226, 232, 240, 0.82);
	padding: 1rem 1.25rem;
	color: #0a2251;
}

.sidebar-title {
	margin: 0;
	color: #0a2251;
	font-size: 0.95rem;
	font-weight: 950;
	letter-spacing: -0.02em;
}

.metrics-grid,
.stats-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 0.75rem;
	padding-top: 1rem;
}

.metric-card,
.stat-card {
	border: 1px solid rgba(226, 232, 240, 0.9);
	border-radius: 20px;
	background: #ffffff;
	padding: 1rem;
	text-align: center;
	box-shadow: 0 12px 26px rgba(15, 23, 42, 0.045);
}

.metric-value,
.stat-card-value {
	color: #0a2251;
	font-size: 1.6rem;
	font-weight: 950;
	letter-spacing: -0.05em;
	line-height: 1;
}

.metric-label,
.stat-card-label {
	margin-top: 0.35rem;
	color: #64748b;
	font-size: 0.72rem;
	font-weight: 900;
	letter-spacing: 0.04em;
	text-transform: uppercase;
}

.sidebar-link {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.75rem;
	border-radius: 16px;
	padding: 0.75rem;
	color: #334155;
	text-decoration: none;
	transition: background 0.18s ease, color 0.18s ease;
}

.sidebar-link:hover {
	background: #f5f8fc;
	color: #0a2251;
}

/* ═══════════════════════════════════════════════
   BUILDER / STEPS / FORMS
   ═══════════════════════════════════════════════ */

.builder-header {
	border-bottom: 1px solid rgba(226, 232, 240, 0.86);
	padding: 1.25rem;
}

.builder-desc {
	margin-top: 0.35rem;
	color: #64748b;
	font-size: 0.9rem;
	line-height: 1.6;
}

.steps-list {
	display: grid;
	gap: 0.75rem;
	padding: 1rem;
}

.s-step {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	border: 1px solid transparent;
	border-radius: 18px;
	padding: 0.8rem;
	color: #64748b;
	transition: 0.18s ease;
}

.s-step-num {
	display: grid;
	width: 32px;
	height: 32px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 13px;
	background: #e8eef6;
	color: #64748b;
	font-size: 0.82rem;
	font-weight: 950;
}

.s-step-title {
	color: inherit;
	font-size: 0.86rem;
	font-weight: 950;
}

.s-step-desc {
	margin-top: 0.15rem;
	color: #94a3b8;
	font-size: 0.76rem;
	line-height: 1.45;
}

.s-step.is-active {
	border-color: rgba(10, 34, 81, 0.16);
	background: rgba(10, 34, 81, 0.055);
	color: #0a2251;
}

.s-step.is-active .s-step-num {
	background: #0a2251;
	color: #ffffff;
}

.s-step.is-done {
	background: rgba(34, 197, 94, 0.07);
	color: #166534;
}

.s-step.is-done .s-step-num {
	background: #22c55e;
	color: #ffffff;
}

.s-step.is-locked {
	opacity: 0.55;
}

.step-instruction {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding-top: 1rem;
	color: #475569;
	font-size: 0.86rem;
	font-weight: 800;
}

.step-instruction svg {
	color: #22c55e;
	flex-shrink: 0;
}

.form-grid {
	display: grid;
	gap: 0.9rem;
	padding-top: 1rem;
}

.form-grid--inline {
	grid-template-columns: 1fr 1fr auto;
}

.s-label {
	display: block;
	margin-bottom: 0.4rem;
	color: #334155;
	font-size: 0.8rem;
	font-weight: 900;
}

.s-select,
.s-textarea {
	width: 100%;
	border: 1px solid rgba(203, 213, 225, 0.9);
	border-radius: 16px;
	background: #ffffff;
	padding: 0.72rem 0.85rem;
	color: #0f172a;
	font-size: 0.9rem;
	outline: none;
	transition:
		border-color 0.16s ease,
		box-shadow 0.16s ease,
		background 0.16s ease;
}

.s-select:focus,
.s-textarea:focus {
	border-color: rgba(10, 34, 81, 0.5);
	box-shadow: 0 0 0 4px rgba(10, 34, 81, 0.1);
}

.s-select--sm {
	border-radius: 14px;
	padding: 0.52rem 0.7rem;
	font-size: 0.82rem;
}

.s-textarea {
	min-height: 120px;
	resize: vertical;
	line-height: 1.65;
}

.s-textarea--sm {
	min-height: 48px;
}

.s-textarea--full {
	min-height: 560px;
	border-radius: 0;
	border-right: 0;
	border-bottom: 0;
	border-left: 0;
}

/* ═══════════════════════════════════════════════
   MATERIALS / CHIPS / MINI EMPTY
   ═══════════════════════════════════════════════ */

.materials-list {
	display: flex;
	flex-direction: column;
	gap: 0.6rem;
	padding-top: 0.85rem;
}

.material-item {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	border: 1px solid rgba(226, 232, 240, 0.88);
	border-radius: 18px;
	background: #f8fafc;
	padding: 0.75rem;
}

.material-icon {
	display: grid;
	width: 38px;
	height: 38px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 15px;
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.material-name {
	color: #0f172a;
	font-size: 0.86rem;
	font-weight: 900;
}

.material-meta {
	margin-top: 0.1rem;
	color: #64748b;
	font-size: 0.75rem;
	font-weight: 700;
}

.topic-chip {
	display: inline-flex;
	align-items: center;
	gap: 0.35rem;
	border: 1px solid rgba(10, 34, 81, 0.1);
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.055);
	padding: 0.42rem 0.65rem;
	color: #0a2251;
	font-size: 0.78rem;
	font-weight: 900;
}

.s-mini-empty,
.s-empty-sm {
	display: flex;
	align-items: center;
	gap: 0.65rem;
	border: 1px dashed rgba(148, 163, 184, 0.5);
	border-radius: 18px;
	background: #f8fafc;
	padding: 0.9rem;
	color: #64748b;
	font-size: 0.84rem;
	line-height: 1.5;
}

/* ═══════════════════════════════════════════════
   PLAN / MODULES / LESSONS
   ═══════════════════════════════════════════════ */

.plan-progress {
	padding-top: 1rem;
}

.plan-progress-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	margin-bottom: 0.65rem;
}

.plan-progress-label {
	color: #334155;
	font-size: 0.86rem;
	font-weight: 950;
}

.plan-progress-pct {
	color: #0a2251;
	font-size: 0.86rem;
	font-weight: 950;
}

.modules-list,
.lessons-list {
	display: flex;
	flex-direction: column;
	gap: 0.85rem;
	padding-top: 1rem;
}

.module-card {
	overflow: hidden;
	border: 1px solid rgba(226, 232, 240, 0.92);
	border-radius: 22px;
	background: #ffffff;
	box-shadow: 0 14px 32px rgba(15, 23, 42, 0.045);
}

.module-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
	border-bottom: 1px solid rgba(226, 232, 240, 0.86);
	background: #f8fafc;
	padding: 1rem 1.1rem;
}

.module-badge {
	display: inline-flex;
	align-items: center;
	border-radius: 999px;
	background: rgba(10, 34, 81, 0.08);
	padding: 0.3rem 0.55rem;
	color: #0a2251;
	font-size: 0.68rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.module-title {
	margin: 0.35rem 0 0;
	color: #0f172a;
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.module-obj,
.lesson-obj {
	margin: 0.25rem 0 0;
	color: #64748b;
	font-size: 0.83rem;
	line-height: 1.55;
}

.lesson-row {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
	border: 1px solid rgba(226, 232, 240, 0.9);
	border-radius: 18px;
	background: #ffffff;
	padding: 0.9rem;
	transition: border-color 0.18s ease, background 0.18s ease;
}

.lesson-row:hover {
	border-color: rgba(10, 34, 81, 0.16);
	background: #f8fafc;
}

.lesson-left {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	min-width: 0;
}

.lesson-check {
	display: grid;
	width: 34px;
	height: 34px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 14px;
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.lesson-content {
	min-width: 0;
}

.lesson-title {
	margin: 0;
	color: #0f172a;
	font-size: 0.94rem;
	font-weight: 950;
	line-height: 1.25;
}

.lesson-meta {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	gap: 0.45rem;
	margin-top: 0.4rem;
}

.lesson-duration,
.lesson-diff {
	display: inline-flex;
	align-items: center;
	gap: 0.3rem;
	border-radius: 999px;
	background: #f1f5f9;
	padding: 0.25rem 0.52rem;
	color: #64748b;
	font-size: 0.72rem;
	font-weight: 800;
}

/* ═══════════════════════════════════════════════
   ROOM / STUDY LESSON
   ═══════════════════════════════════════════════ */

.room-header-panel {
	background: #ffffff;
}

.room-steps-sticky {
	position: sticky;
	top: 0.75rem;
	z-index: 20;
	border: 1px solid rgba(226, 232, 240, 0.86);
	border-radius: 22px;
	background: rgba(255, 255, 255, 0.88);
	padding: 0.65rem;
	box-shadow: 0 18px 44px rgba(15, 23, 42, 0.075);
	backdrop-filter: blur(18px);
}

.room-steps {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 0.55rem;
}

.room-step {
	display: flex;
	align-items: center;
	gap: 0.55rem;
	border: 1px solid rgba(226, 232, 240, 0.9);
	border-radius: 16px;
	background: #ffffff;
	padding: 0.65rem;
	color: #64748b;
	font-size: 0.78rem;
	font-weight: 900;
	transition: 0.18s ease;
}

.room-step.is-active {
	border-color: rgba(10, 34, 81, 0.18);
	background: rgba(10, 34, 81, 0.065);
	color: #0a2251;
}

.room-step.is-done {
	color: #166534;
	background: rgba(34, 197, 94, 0.08);
}

.room-step-num {
	display: grid;
	width: 28px;
	height: 28px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 11px;
	background: #e8eef6;
	font-size: 0.76rem;
	font-weight: 950;
}

.room-step.is-active .room-step-num {
	background: #0a2251;
	color: #ffffff;
}

.room-step.is-done .room-step-num {
	background: #22c55e;
	color: #ffffff;
}

.room-sidebar {
	position: sticky;
	top: 1rem;
	max-height: calc(100vh - 2rem);
	overflow-y: auto;
	scrollbar-width: thin;
}

.lesson-content {
	display: grid;
	gap: 1rem;
}

.content-block,
.concept-card,
.key-idea,
.worked-example,
.mistake-item,
.example-problem,
.example-answer {
	border: 1px solid rgba(226, 232, 240, 0.9);
	border-radius: 22px;
	background: #ffffff;
	padding: 1rem;
	box-shadow: 0 12px 30px rgba(15, 23, 42, 0.04);
}

.content-block-header {
	display: flex;
	align-items: center;
	gap: 0.65rem;
	margin-bottom: 0.65rem;
}

.content-num,
.content-num--sm {
	display: grid;
	width: 34px;
	height: 34px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 14px;
	background: #0a2251;
	color: #ffffff;
	font-size: 0.82rem;
	font-weight: 950;
}

.content-num--sm {
	width: 28px;
	height: 28px;
	border-radius: 11px;
	font-size: 0.72rem;
}

.content-title,
.concept-title,
.example-title {
	margin: 0;
	color: #0a2251;
	font-size: 1rem;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.content-summary,
.concept-body,
.example-steps,
.example-answer,
.content-points {
	color: #475569;
	font-size: 0.9rem;
	line-height: 1.72;
}

.content-points {
	margin: 0.65rem 0 0;
	padding-left: 1.1rem;
}

.key-idea {
	display: flex;
	gap: 0.85rem;
	background: rgba(10, 34, 81, 0.055);
}

.key-idea-label {
	color: #0a2251;
	font-size: 0.72rem;
	font-weight: 950;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.key-idea-text {
	margin-top: 0.2rem;
	color: #334155;
	font-size: 0.92rem;
	font-weight: 750;
	line-height: 1.6;
}

.point-dot {
	margin-top: 0.42rem;
	width: 9px;
	height: 9px;
	flex: 0 0 auto;
	border-radius: 999px;
	background: #f5b301;
	box-shadow: 0 0 0 5px rgba(245, 179, 1, 0.16);
}

.concept-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 1rem;
}

.concept-formula {
	margin-top: 0.75rem;
	border-radius: 16px;
	background: #f8fafc;
	padding: 0.8rem;
	color: #0a2251;
	font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
	font-size: 0.85rem;
	overflow-x: auto;
}

.diagram-img {
	width: 100%;
	border-radius: 20px;
	border: 1px solid rgba(226, 232, 240, 0.9);
	background: #ffffff;
}

.mistakes-list {
	display: grid;
	gap: 0.85rem;
}

.mistake-bad {
	color: #b91c1c;
	font-weight: 900;
}

.mistake-fix {
	margin-top: 0.35rem;
	color: #166534;
	font-weight: 850;
}

/* ═══════════════════════════════════════════════
   PRACTICE / QUIZ / EXERCISES
   ═══════════════════════════════════════════════ */

.practice-flow {
	position: relative;
}

.practice-flow-header {
	display: flex;
	flex-direction: column;
	align-items: center;
	border: 1px dashed rgba(10, 34, 81, 0.18);
	border-radius: 24px;
	background: rgba(10, 34, 81, 0.04);
	padding: 2.2rem 1.5rem;
	text-align: center;
}

.practice-flow-icon {
	display: grid;
	width: 58px;
	height: 58px;
	place-items: center;
	border-radius: 22px;
	background: #0a2251;
	color: #ffffff;
	box-shadow: 0 18px 34px rgba(10, 34, 81, 0.2);
}

.practice-flow-title {
	margin: 1rem 0 0;
	color: #0a2251;
	font-size: 1.35rem;
	font-weight: 950;
	letter-spacing: -0.04em;
}

.practice-flow-desc {
	margin: 0.45rem auto 0;
	max-width: 560px;
	color: #64748b;
	font-size: 0.92rem;
	line-height: 1.65;
}

.practice-flow-steps {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 0.9rem;
	margin-top: 1.25rem;
	width: 100%;
}

.practice-card {
	overflow: hidden;
}

.practice-card-header {
	background: #f8fafc !important;
}

.exercise-list {
	display: grid;
	gap: 1rem;
	padding: 1rem 1.25rem;
}

.exercise-item {
	border: 1px solid rgba(226, 232, 240, 0.92);
	border-radius: 22px;
	background: #ffffff;
	padding: 1.1rem;
	box-shadow: 0 12px 28px rgba(15, 23, 42, 0.045);
}

.exercise-question-row {
	display: flex;
	gap: 0.75rem;
	align-items: flex-start;
}

.exercise-question-num {
	display: grid;
	width: 32px;
	height: 32px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 13px;
	background: #0a2251;
	color: #ffffff;
	font-size: 0.78rem;
	font-weight: 950;
}

.exercise-question-text {
	color: #0f172a;
	font-size: 0.95rem;
	font-weight: 900;
	line-height: 1.45;
}

.exercise-options {
	display: grid;
	gap: 0.55rem;
	margin-top: 0.9rem;
}

.quiz-option {
	display: flex;
	align-items: flex-start;
	gap: 0.65rem;
	width: 100%;
	min-height: 48px;
	border: 1px solid rgba(226, 232, 240, 0.92);
	border-radius: 16px;
	background: #f8fafc;
	padding: 0.75rem 0.85rem;
	color: #334155;
	text-align: left;
	cursor: pointer;
	transition:
		transform 0.16s ease,
		border-color 0.16s ease,
		background 0.16s ease;
}

.quiz-option:hover {
	transform: translateY(-1px);
	border-color: rgba(10, 34, 81, 0.2);
	background: #ffffff;
}

.quiz-option-letter {
	display: grid;
	width: 30px;
	height: 30px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 12px;
	background: #e8eef6;
	color: #0a2251;
	font-size: 0.75rem;
	font-weight: 950;
}

.quiz-option-content {
	flex: 1;
	min-width: 0;
	font-size: 0.88rem;
	line-height: 1.45;
}

.quiz-option-icon {
	margin-left: auto;
	display: grid;
	width: 26px;
	height: 26px;
	flex: 0 0 auto;
	place-items: center;
	border-radius: 999px;
	font-size: 0.82rem;
	font-weight: 950;
}

.quiz-option-icon--correct {
	background: rgba(34, 197, 94, 0.14);
	color: #15803d;
}

.quiz-option-icon--wrong {
	background: rgba(239, 68, 68, 0.13);
	color: #b91c1c;
}

.quiz-option--correct {
	border-color: rgba(34, 197, 94, 0.42);
	background: rgba(34, 197, 94, 0.08);
}

.quiz-option--wrong {
	border-color: rgba(239, 68, 68, 0.36);
	background: rgba(239, 68, 68, 0.07);
}

.quiz-option--dimmed {
	opacity: 0.6;
}

.exercise-explanation {
	display: flex;
	gap: 0.65rem;
	margin-top: 0.9rem;
	border-radius: 16px;
	background: rgba(10, 34, 81, 0.055);
	padding: 0.8rem;
}

.exercise-explanation-icon {
	color: #0a2251;
}

.exercise-explanation-label {
	color: #0a2251;
	font-size: 0.75rem;
	font-weight: 950;
	letter-spacing: 0.05em;
	text-transform: uppercase;
}

.exercise-explanation-text {
	margin-top: 0.2rem;
	color: #334155;
	font-size: 0.86rem;
	line-height: 1.55;
}

.quiz-score-banner {
	display: flex;
	align-items: center;
	gap: 0.9rem;
	margin: 1rem 1.25rem 1.25rem;
	border: 1px solid rgba(245, 179, 1, 0.3);
	border-radius: 22px;
	background: rgba(245, 179, 1, 0.11);
	padding: 1rem;
}

/* ═══════════════════════════════════════════════
   CHAT / TUTOR
   ═══════════════════════════════════════════════ */

.tutor-panel {
	overflow: hidden;
}

.chat-hint {
	margin: 0;
	padding: 1rem 1.25rem 0;
	color: #64748b;
	font-size: 0.86rem;
	line-height: 1.55;
}

.chat-box {
	display: flex;
	height: 340px;
	flex-direction: column;
	gap: 0.75rem;
	overflow-y: auto;
	padding: 1rem 1.25rem;
	scrollbar-width: thin;
}

.chat-msg {
	max-width: 88%;
	border-radius: 20px;
	padding: 0.85rem 0.95rem;
	font-size: 0.88rem;
	line-height: 1.6;
	box-shadow: 0 10px 24px rgba(15, 23, 42, 0.045);
}

.chat-msg--user {
	align-self: flex-end;
	border-bottom-right-radius: 8px;
	background: #0a2251;
	color: #ffffff;
}

.chat-msg--ai {
	align-self: flex-start;
	border: 1px solid rgba(226, 232, 240, 0.9);
	border-bottom-left-radius: 8px;
	background: #ffffff;
	color: #334155;
}

.chat-input-row {
	display: flex;
	gap: 0.6rem;
	border-top: 1px solid rgba(226, 232, 240, 0.86);
	padding: 1rem 1.25rem;
}

.tutor-backdrop {
	position: fixed;
	inset: 0;
	z-index: 998;
	background: rgba(15, 23, 42, 0.42);
	backdrop-filter: blur(6px);
}

.tutor-panel.is-expanded {
	position: fixed;
	top: 50%;
	left: 50%;
	z-index: 999;
	width: min(920px, calc(100vw - 2rem));
	height: min(760px, calc(100dvh - 2rem));
	max-height: none;
	transform: translate(-50%, -50%);
	border-radius: 28px;
	box-shadow: 0 34px 90px rgba(0, 0, 0, 0.34);
}

.tutor-panel.is-expanded .chat-box {
	height: calc(100% - 155px);
}

.tutor-fab {
	position: fixed;
	right: 1rem;
	bottom: 1rem;
	z-index: 50;
	display: none;
}

/* ═══════════════════════════════════════════════
   CHECKLIST / STATS / EXPLANATIONS / WHITEBOARD
   ═══════════════════════════════════════════════ */

.checklist,
.fav-list,
.explanations-list {
	display: grid;
	gap: 0.75rem;
	padding-top: 1rem;
}

.checklist-box,
.fav-item,
.explanation-card {
	border: 1px solid rgba(226, 232, 240, 0.92);
	border-radius: 20px;
	background: #ffffff;
	padding: 0.9rem;
	box-shadow: 0 12px 28px rgba(15, 23, 42, 0.045);
}

.checklist-item {
	display: flex;
	align-items: flex-start;
	gap: 0.6rem;
	color: #334155;
	font-size: 0.88rem;
	line-height: 1.55;
}

.fav-item-title,
.explanation-title {
	color: #0f172a;
	font-size: 0.92rem;
	font-weight: 950;
	line-height: 1.35;
}

.fav-item-date,
.explanation-date {
	margin-top: 0.25rem;
	color: #64748b;
	font-size: 0.75rem;
	font-weight: 750;
}

.explanation-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
}

.wb-actions {
	display: grid;
	gap: 0.6rem;
	padding: 1rem 1.25rem;
}

/* ═══════════════════════════════════════════════
   EMPTY / LOADER / MARKDOWN
   ═══════════════════════════════════════════════ */

.s-empty {
	display: grid;
	place-items: center;
	min-height: 280px;
	padding: 2rem;
	text-align: center;
}

.s-empty-icon {
	display: grid;
	width: 70px;
	height: 70px;
	place-items: center;
	border-radius: 26px;
	background: rgba(10, 34, 81, 0.08);
	color: #0a2251;
}

.s-empty-title {
	margin: 1rem 0 0;
	color: #0a2251;
	font-size: 1.15rem;
	font-weight: 950;
	letter-spacing: -0.03em;
}

.s-empty-desc {
	margin: 0.45rem auto 0;
	max-width: 420px;
	color: #64748b;
	font-size: 0.9rem;
	line-height: 1.65;
}

.s-loader {
	display: grid;
	min-height: 260px;
	place-items: center;
	padding: 2rem;
}

.s-loader-spinner {
	width: 38px;
	height: 38px;
	border: 4px solid #e2e8f0;
	border-top-color: #0a2251;
	border-radius: 999px;
	animation: sb-spin 0.8s linear infinite;
}

@keyframes sb-spin {
	to {
		transform: rotate(360deg);
	}
}

.s-markdown-block {
	color: #334155;
	font-size: 0.9rem;
	line-height: 1.75;
}

.s-markdown-block :deep(h1),
.s-markdown-block :deep(h2),
.s-markdown-block :deep(h3) {
	color: #0a2251;
	font-weight: 950;
	letter-spacing: -0.035em;
	line-height: 1.18;
}

.s-markdown-block :deep(h1) {
	font-size: 1.45rem;
}

.s-markdown-block :deep(h2) {
	font-size: 1.25rem;
}

.s-markdown-block :deep(h3) {
	font-size: 1.05rem;
}

.s-markdown-block :deep(p) {
	margin: 0.65rem 0;
}

.s-markdown-block :deep(ul),
.s-markdown-block :deep(ol) {
	margin: 0.6rem 0 0.75rem 1.25rem;
}

.s-markdown-block :deep(code) {
	border-radius: 8px;
	background: #f1f5f9;
	padding: 0.12rem 0.35rem;
	color: #0a2251;
	font-size: 0.88em;
}

.s-markdown-block :deep(pre) {
	overflow-x: auto;
	border-radius: 18px;
	background: #08172c;
	padding: 1rem;
	color: #e5edf8;
}

.markdown-inline :deep(p) {
	display: inline;
	margin: 0;
	color: inherit;
	font: inherit;
}

.markdown-inline :deep(.katex) {
	font-size: 1.02em;
}

.markdown-inline :deep(.katex-display),
.chat-msg :deep(.katex-display),
.s-markdown-block :deep(.katex-display) {
	overflow-x: auto;
	overflow-y: hidden;
	margin: 0.75rem 0;
	padding: 0.25rem 0;
}

/* ═══════════════════════════════════════════════
   DARK MODE
   ═══════════════════════════════════════════════ */

:global(:root[data-theme='dark']) .study-page,
:global(.dark) .study-page {
	background:
		radial-gradient(circle at top left, rgba(245, 179, 1, 0.08), transparent 32rem),
		linear-gradient(180deg, #07111f 0%, #081827 48%, #07111f 100%);
	color: #e5edf8;
}

:global(:root[data-theme='dark']) .study-hero,
:global(.dark) .study-hero {
	background: #0a2251;
	box-shadow: 0 24px 60px rgba(0, 0, 0, 0.34);
}

:global(:root[data-theme='dark']) .s-panel,
:global(:root[data-theme='dark']) .course-card,
:global(:root[data-theme='dark']) .flow-card,
:global(:root[data-theme='dark']) .metric-card,
:global(:root[data-theme='dark']) .stat-card,
:global(:root[data-theme='dark']) .module-card,
:global(:root[data-theme='dark']) .lesson-row,
:global(:root[data-theme='dark']) .content-block,
:global(:root[data-theme='dark']) .concept-card,
:global(:root[data-theme='dark']) .worked-example,
:global(:root[data-theme='dark']) .exercise-item,
:global(:root[data-theme='dark']) .chat-msg--ai,
:global(:root[data-theme='dark']) .checklist-box,
:global(:root[data-theme='dark']) .fav-item,
:global(:root[data-theme='dark']) .explanation-card,
:global(.dark) .s-panel,
:global(.dark) .course-card,
:global(.dark) .flow-card,
:global(.dark) .metric-card,
:global(.dark) .stat-card,
:global(.dark) .module-card,
:global(.dark) .lesson-row,
:global(.dark) .content-block,
:global(.dark) .concept-card,
:global(.dark) .worked-example,
:global(.dark) .exercise-item,
:global(.dark) .chat-msg--ai,
:global(.dark) .checklist-box,
:global(.dark) .fav-item,
:global(.dark) .explanation-card {
	border-color: rgba(148, 163, 184, 0.16);
	background: rgba(15, 23, 42, 0.72);
	box-shadow: 0 18px 46px rgba(0, 0, 0, 0.22);
}

:global(:root[data-theme='dark']) .s-panel-title,
:global(:root[data-theme='dark']) .sidebar-title,
:global(:root[data-theme='dark']) .course-card-title,
:global(:root[data-theme='dark']) .flow-card-title,
:global(:root[data-theme='dark']) .module-title,
:global(:root[data-theme='dark']) .lesson-title,
:global(:root[data-theme='dark']) .content-title,
:global(:root[data-theme='dark']) .concept-title,
:global(:root[data-theme='dark']) .example-title,
:global(:root[data-theme='dark']) .fav-item-title,
:global(:root[data-theme='dark']) .explanation-title,
:global(.dark) .s-panel-title,
:global(.dark) .sidebar-title,
:global(.dark) .course-card-title,
:global(.dark) .flow-card-title,
:global(.dark) .module-title,
:global(.dark) .lesson-title,
:global(.dark) .content-title,
:global(.dark) .concept-title,
:global(.dark) .example-title,
:global(.dark) .fav-item-title,
:global(.dark) .explanation-title {
	color: #f8fafc;
}

:global(:root[data-theme='dark']) .s-panel-desc,
:global(:root[data-theme='dark']) .flow-card-desc,
:global(:root[data-theme='dark']) .course-card-date,
:global(:root[data-theme='dark']) .progress-label,
:global(:root[data-theme='dark']) .module-obj,
:global(:root[data-theme='dark']) .lesson-obj,
:global(:root[data-theme='dark']) .content-summary,
:global(:root[data-theme='dark']) .concept-body,
:global(:root[data-theme='dark']) .chat-hint,
:global(:root[data-theme='dark']) .s-empty-desc,
:global(.dark) .s-panel-desc,
:global(.dark) .flow-card-desc,
:global(.dark) .course-card-date,
:global(.dark) .progress-label,
:global(.dark) .module-obj,
:global(.dark) .lesson-obj,
:global(.dark) .content-summary,
:global(.dark) .concept-body,
:global(.dark) .chat-hint,
:global(.dark) .s-empty-desc {
	color: #94a3b8;
}

:global(:root[data-theme='dark']) .s-kicker,
:global(:root[data-theme='dark']) .topic-chip,
:global(:root[data-theme='dark']) .course-next-icon,
:global(.dark) .s-kicker,
:global(.dark) .topic-chip,
:global(.dark) .course-next-icon {
	background: rgba(245, 179, 1, 0.14);
	color: #f8c84e;
}

:global(:root[data-theme='dark']) .course-next,
:global(:root[data-theme='dark']) .material-item,
:global(:root[data-theme='dark']) .module-header,
:global(:root[data-theme='dark']) .quiz-option,
:global(:root[data-theme='dark']) .s-mini-empty,
:global(:root[data-theme='dark']) .room-steps-sticky,
:global(.dark) .course-next,
:global(.dark) .material-item,
:global(.dark) .module-header,
:global(.dark) .quiz-option,
:global(.dark) .s-mini-empty,
:global(.dark) .room-steps-sticky {
	border-color: rgba(148, 163, 184, 0.16);
	background: rgba(15, 23, 42, 0.58);
}

:global(:root[data-theme='dark']) .s-select,
:global(:root[data-theme='dark']) .s-textarea,
:global(.dark) .s-select,
:global(.dark) .s-textarea {
	border-color: rgba(148, 163, 184, 0.22);
	background: rgba(2, 6, 23, 0.42);
	color: #e5edf8;
}

:global(:root[data-theme='dark']) .progress-track,
:global(:root[data-theme='dark']) .ring-bg,
:global(.dark) .progress-track,
:global(.dark) .ring-bg {
	background: rgba(148, 163, 184, 0.18);
	stroke: rgba(148, 163, 184, 0.25);
}

/* ═══════════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════════ */

@media (max-width: 1280px) {
	.flow-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.courses-grid--3 {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 1024px) {
	.hero-content {
		grid-template-columns: 1fr;
		align-items: start;
	}

	.hero-actions {
		justify-content: flex-start;
		width: 100%;
	}

	.hero-nav {
		justify-content: flex-start;
		max-width: none;
	}

	.courses-grid {
		grid-template-columns: 1fr;
	}

	.room-sidebar {
		position: static;
		max-height: none;
		overflow: visible;
	}

	.concept-grid,
	.practice-flow-steps {
		grid-template-columns: 1fr;
	}
}

@media (max-width: 768px) {
	.study-page > div {
		padding-inline: 1rem;
		padding-top: 1rem;
		gap: 1rem;
	}

	.study-hero {
		border-radius: 24px;
		padding: 1.25rem;
	}

	.hero-title {
		font-size: clamp(1.65rem, 9vw, 2.35rem);
		letter-spacing: -0.055em;
	}

	.hero-subtitle {
		font-size: 0.9rem;
		line-height: 1.6;
	}

	.hero-breadcrumb {
		font-size: 0.7rem;
	}

	.hero-nav {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		width: 100%;
	}

	.nav-pill {
		width: 100%;
		min-height: 42px;
		padding: 0.65rem 0.72rem;
	}

	.nav-pill-label {
		display: inline;
	}

	.s-panel {
		border-radius: 22px;
	}

	.s-panel-header {
		flex-direction: column;
		align-items: stretch;
		gap: 0.8rem;
	}

	.s-panel-header > *:last-child {
		width: 100%;
	}

	.s-panel--flush > * {
		padding-left: 1rem;
		padding-right: 1rem;
	}

	.s-panel--flush > *:first-child {
		padding-top: 1rem;
	}

	.s-panel--flush > *:last-child {
		padding-bottom: 1rem;
	}

	.s-panel-title {
		font-size: 1.05rem;
	}

	.s-panel-desc {
		font-size: 0.84rem;
	}

	.flow-grid,
	.courses-grid,
	.courses-grid--3,
	.metrics-grid,
	.stats-grid {
		grid-template-columns: 1fr;
	}

	.flow-card {
		min-height: auto;
		border-radius: 20px;
	}

	.course-card {
		border-radius: 22px;
		padding: 1rem;
	}

	.course-card-top {
		gap: 0.75rem;
	}

	.course-progress-ring {
		display: none;
	}

	.course-actions {
		display: grid;
		grid-template-columns: 1fr;
	}

	.course-actions > * {
		width: 100%;
	}

	.form-grid,
	.form-grid--inline {
		grid-template-columns: 1fr;
	}

	.room-steps-sticky {
		position: relative;
		top: auto;
	}

	.room-steps {
		grid-template-columns: 1fr;
	}

	.lesson-row {
		flex-direction: column;
	}

	.lesson-meta {
		gap: 0.35rem;
	}

	.chat-box {
		height: 280px;
	}

	.chat-msg {
		max-width: 94%;
		font-size: 0.84rem;
	}

	.chat-input-row {
		flex-direction: column;
	}

	.exercise-list {
		padding: 1rem;
	}

	.exercise-item {
		padding: 1rem;
	}

	.quiz-option {
		min-height: 46px;
		padding: 0.65rem 0.72rem;
	}

	.tutor-panel.is-expanded {
		inset: 0;
		width: 100vw;
		height: 100dvh;
		max-width: none;
		transform: none;
		border-radius: 0;
	}

	.tutor-panel.is-expanded .chat-box {
		height: calc(100dvh - 165px);
	}

	.s-textarea--full {
		min-height: 340px;
	}

	.explanation-header {
		flex-direction: column;
	}

	.summary-stats {
		grid-template-columns: 1fr;
	}
}

@media (max-width: 480px) {
	.study-page > div {
		padding-inline: 0.75rem;
	}

	.study-hero {
		border-radius: 20px;
		padding: 1rem;
	}

	.hero-title {
		font-size: 1.55rem;
	}

	.hero-subtitle {
		font-size: 0.84rem;
	}

	.hero-nav {
		grid-template-columns: 1fr;
		gap: 0.45rem;
	}

	.nav-pill {
		justify-content: flex-start;
	}

	.flow-icon {
		width: 42px;
		height: 42px;
		border-radius: 15px;
	}

	.course-next {
		align-items: flex-start;
	}

	.metric-card,
	.stat-card {
		padding: 0.85rem;
	}

	.metric-value,
	.stat-card-value {
		font-size: 1.35rem;
	}

	.exercise-question-num,
	.quiz-option-letter {
		width: 28px;
		height: 28px;
	}

	.exercise-question-text {
		font-size: 0.88rem;
	}

	.quiz-option-content {
		font-size: 0.82rem;
	}

	.content-block,
	.concept-card,
	.key-idea,
	.worked-example,
	.mistake-item {
		border-radius: 18px;
		padding: 0.85rem;
	}
}
</style>

<style>
/* ─── EXERCISES & QUIZ (UNSCOPED FOR RENDER FUNCTION) ─── */
.exercise-list {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	padding: 1rem 1.25rem 0.5rem;
}
.exercise-item {
	padding: 1.25rem;
	border-radius: 12px;
	border: 1px solid #e2e8f0;
	background: #fff;
	transition: box-shadow 0.2s ease;
}
.exercise-item:hover {
	box-shadow: 0 2px 12px rgba(15, 23, 42, 0.05);
}
.exercise-question-row {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
}
.exercise-question-num {
	display: grid;
	width: 28px;
	height: 28px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 50%;
	background: linear-gradient(135deg, #6366f1, #818cf8);
	color: #fff;
	font-size: 0.75rem;
	font-weight: 800;
}
.exercise-question-text {
	font-size: 0.9rem;
	font-weight: 600;
	line-height: 1.6;
	color: #0f172a;
	padding-top: 3px;
	word-break: break-word;
}
.exercise-options {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	margin-top: 1rem;
}
.exercise-explanation {
	margin-top: 1rem;
	padding: 0.875rem 1rem;
	border-radius: 10px;
	background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
	border: 1px solid #bbf7d0;
}
.exercise-explanation-label {
	display: flex;
	align-items: center;
	gap: 0.375rem;
	font-size: 0.75rem;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 0.04em;
	color: #166534;
}
.exercise-explanation-icon { font-size: 0.9rem; }
.exercise-explanation-text {
	font-size: 0.84rem;
	line-height: 1.65;
	color: #14532d;
	margin-top: 0.375rem;
}

.quiz-option {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	padding: 0.75rem 1rem;
	border-radius: 10px;
	border: 1.5px solid transparent;
	font-size: 0.875rem;
	text-align: left;
	cursor: pointer;
	transition: all 0.2s ease;
	width: 100%;
	min-height: 48px;
	position: relative;
}
.quiz-option:disabled {
	cursor: default;
}
.quiz-option-letter {
	display: grid;
	width: 28px;
	height: 28px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 8px;
	font-size: 0.75rem;
	font-weight: 800;
	transition: all 0.2s ease;
}
.quiz-option-content {
	flex: 1;
	min-width: 0;
	word-break: break-word;
	line-height: 1.5;
}
.quiz-option-icon {
	display: grid;
	width: 22px;
	height: 22px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 50%;
	font-size: 0.7rem;
	font-weight: 900;
}
.quiz-option-icon--correct {
	background: #22c55e;
	color: #fff;
}
.quiz-option-icon--wrong {
	background: #ef4444;
	color: #fff;
}
.quiz-option--default {
	border-color: #e2e8f0;
	background: #fff;
	color: #334155;
}
.quiz-option--default:hover:not(:disabled) {
	border-color: #a5b4fc;
	background: #eef2ff;
	transform: translateX(4px);
	box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1);
}
.quiz-option--default .quiz-option-letter {
	background: #f1f5f9;
	color: #64748b;
}
.quiz-option--default:hover:not(:disabled) .quiz-option-letter {
	background: #6366f1;
	color: #fff;
}
.quiz-option--correct {
	border-color: #86efac;
	background: #f0fdf4;
	color: #166534;
}
.quiz-option--correct .quiz-option-letter {
	background: #22c55e;
	color: #fff;
}
.quiz-option--wrong {
	border-color: #fca5a5;
	background: #fef2f2;
	color: #991b1b;
}
.quiz-option--wrong .quiz-option-letter {
	background: #ef4444;
	color: #fff;
}
.quiz-option--dimmed {
	border-color: #f1f5f9;
	background: #fafafa;
	color: #94a3b8;
}
.quiz-option--dimmed .quiz-option-letter {
	background: #f1f5f9;
	color: #cbd5e1;
}

.quiz-score {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	margin-top: 0.75rem;
	padding: 0.75rem 1rem;
	border-radius: 10px;
	background: linear-gradient(135deg, #eef2ff, #e0e7ff);
	border: 1px solid #c7d2fe;
	font-size: 0.9rem;
	color: #4338ca;
}

/* Skeleton Study */
.study-skeleton-wrapper {
	animation: pulse 1.5s infinite;
}

.skeleton-panel {
	background: var(--surface);
	border-radius: 1.5rem;
	width: 100%;
}

@keyframes pulse {
	0% { opacity: 0.6; }
	50% { opacity: 0.3; }
	100% { opacity: 0.6; }
}

/* Flow Wizard */
.flow-wizard {
	display: grid;
	gap: 1.5rem;
	grid-template-columns: 1fr;
}
@media (min-width: 1280px) {
	.flow-wizard {
		grid-template-columns: 340px 1fr;
		align-items: start;
	}
}

.wizard-sidebar {
	display: flex;
	flex-direction: column;
}
@media (max-width: 1279px) {
	.wizard-sidebar {
		padding: 1rem;
		border-radius: 1rem;
	}
	.wizard-steps {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		gap: 0.5rem;
	}
	.wizard-steps .s-step {
		flex: 1;
		justify-content: center;
		padding: 0.5rem;
	}
	.wizard-steps .s-step-num {
		margin: 0;
	}
}

.wizard-content {
	min-height: 400px;
}

.wizard-step {
	width: 100%;
}

.wizard-actions {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-top: 1.5rem;
	padding-top: 1.5rem;
	border-top: 1px solid var(--border);
}

/* Transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
	transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-slide-enter-from {
	opacity: 0;
	transform: translateX(15px);
}
.fade-slide-leave-to {
	opacity: 0;
	transform: translateX(-15px);
}

.s-step:disabled {
	cursor: not-allowed;
	opacity: 0.7;
}
</style>

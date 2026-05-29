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
						<div class="hero-breadcrumb">
							<router-link :to="{ name: 'Study' }" class="hero-breadcrumb-link">
								{{ __('Estudio IA') }}
							</router-link>
							<span v-if="pageTitle" class="hero-breadcrumb-sep">/</span>
							<span v-if="pageTitle" class="hero-breadcrumb-current">{{ pageTitle }}</span>
						</div>
						<h1 class="hero-title">{{ headerTitle }}</h1>
						<p class="hero-subtitle">{{ headerSubtitle }}</p>
					</div>
					<div class="hero-actions">
						<Button v-if="isDashboard" variant="solid" :label="__('Crear curso IA')" @click="startFlow('parcial')" class="hero-cta">
							<template #prefix><BookOpen class="h-4 w-4 stroke-1.5" /></template>
						</Button>
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

			<!-- ═══════════ DASHBOARD ═══════════ -->
			<section v-if="isDashboard" class="grid gap-6 xl:grid-cols-[1fr_360px]">
				<div class="flex flex-col gap-6">
					<!-- FLOW CARDS -->
					<div class="s-panel s-panel--flush">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker"><Sparkles class="h-3.5 w-3.5 stroke-1.5" /> {{ __('Empieza en 4 pasos') }}</div>
								<h2 class="s-panel-title">{{ __('Mis cursos IA') }}</h2>
								<p class="s-panel-desc">{{ __('Crea un curso desde tus apuntes, deja que la IA lo ordene en módulos y continúa cada lección con práctica guiada.') }}</p>
							</div>
							<Button variant="solid" :label="__('Crear mi primer curso')" @click="startFlow('parcial')" />
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
								<p class="s-empty-desc">{{ __('Crea uno con tus apuntes, PDFs o temas del parcial. Te guiaremos paso a paso.') }}</p>
								<Button class="mt-4" variant="solid" :label="__('Crear curso IA')" @click="startFlow('parcial')" />
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
			<section v-else-if="isFlow" class="grid gap-6 xl:grid-cols-[340px_1fr]">
				<aside class="s-panel s-panel--flush h-fit">
					<div class="builder-header">
						<Wand2 class="h-5 w-5 stroke-1.5" />
						<div>
							<div class="s-kicker">{{ __('Constructor guiado') }}</div>
							<h2 class="s-panel-title">{{ __('Crea tu curso IA') }}</h2>
						</div>
					</div>
					<p class="builder-desc">{{ __('Completa estos pasos. Cada avance desbloquea el siguiente sin perder tu progreso.') }}</p>
					<div class="steps-list">
						<div class="s-step" :class="currentSession ? 'is-done' : 'is-active'">
							<span class="s-step-num">1</span>
							<div>
								<div class="s-step-title">{{ __('Datos básicos') }}</div>
								<p class="s-step-desc">{{ currentSession ? __('Curso creado') : __('Ponle nombre y contexto') }}</p>
							</div>
						</div>
						<div class="s-step" :class="currentSession?.topics?.length ? 'is-done' : currentSession ? 'is-active' : ''">
							<span class="s-step-num">2</span>
							<div>
								<div class="s-step-title">{{ __('Material y temas') }}</div>
								<p class="s-step-desc">{{ __('Sube archivos o pega texto') }}</p>
							</div>
						</div>
						<div class="s-step" :class="currentSession?.profile_questions?.length ? 'is-done' : currentSession?.topics?.length ? 'is-active' : ''">
							<span class="s-step-num">3</span>
							<div>
								<div class="s-step-title">{{ __('Perfil') }}</div>
								<p class="s-step-desc">{{ __('Adapta el curso a tu nivel') }}</p>
							</div>
						</div>
						<div class="s-step" :class="currentSession?.course_structure?.modules?.length ? 'is-done' : currentSession?.profile_questions?.length ? 'is-active' : ''">
							<span class="s-step-num">4</span>
							<div>
								<div class="s-step-title">{{ __('Curso listo') }}</div>
								<p class="s-step-desc">{{ __('Genera módulos y lecciones') }}</p>
							</div>
						</div>
					</div>
				</aside>

				<div class="flex flex-col gap-6">
					<!-- Step 1 -->
					<div class="s-panel s-panel--flush">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker">{{ __('Paso 1') }}</div>
								<h2 class="s-panel-title">{{ __('Datos básicos del curso') }}</h2>
								<p class="s-panel-desc">{{ __('Con esto la IA entiende qué estás preparando y cuánto contexto tiene.') }}</p>
							</div>
							<Button :label="currentSession ? __('Guardar cambios') : __('Crear curso')" variant="solid" :loading="loading === 'create'" @click="createOrUpdateSession" />
						</div>
						<div class="form-grid">
							<FormControl v-model="draft.title" :label="__('Nombre del curso')" :placeholder="__('Ej. Parcial de cálculo')" />
							<FormControl v-model="draft.academic_context" :label="__('Curso o contexto')" :placeholder="__('Ej. Universidad, curso, ciclo')" />
							<FormControl v-model="draft.exam_date" type="date" :label="__('Fecha objetivo')" />
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
					</div>

					<!-- Admission search -->
					<div v-if="flowId === 'admision'" class="s-panel s-panel--flush">
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

					<!-- Step 2 -->
					<div class="s-panel s-panel--flush">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker">{{ __('Paso 2') }}</div>
								<h2 class="s-panel-title">{{ __('Materiales y temas') }}</h2>
								<p class="s-panel-desc">{{ __('Sube PDF, imágenes o Word. Luego analiza para detectar los temas del curso.') }}</p>
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
								<Button :label="__('Subir archivo')" :disabled="!currentSession" @click="openUploader">
									<template #prefix><Upload class="h-4 w-4 stroke-1.5" /></template>
								</Button>
								<Button :label="__('Analizar material')" variant="solid" :disabled="!currentSession" :loading="loading === 'analyze'" @click="analyzeMaterial" />
							</div>
						</div>
						<div v-if="loading === 'analyze'" class="s-loader">
							<div class="s-loader-spinner"></div>
							{{ __('Analizando material y ordenando temas...') }}
						</div>
						<div class="materials-list">
							<div v-for="material in currentSession?.materials || []" :key="material.idx" class="material-item">
								<div class="material-icon"><FileText class="h-4 w-4 stroke-1.5" /></div>
								<div class="min-w-0">
									<div class="material-name">{{ material.file_name }}</div>
									<div class="material-meta">{{ material.file_type }} · {{ material.analysis_status }}</div>
								</div>
							</div>
							<div v-if="!currentSession?.materials?.length" class="s-empty-sm">
								<Upload class="h-6 w-6 stroke-1.5" />
								<h3>{{ currentSession ? __('Agrega material para mejorar el curso') : __('Primero crea el curso') }}</h3>
								<p>{{ currentSession ? __('También puedes usar solo el texto manual del paso 1.') : __('Así se activará la subida de archivos.') }}</p>
							</div>
						</div>
					</div>

					<!-- Steps 3 & 4 -->
					<div class="s-panel s-panel--flush">
						<div class="s-panel-header">
							<div>
								<div class="s-kicker">{{ __('Pasos 3 y 4') }}</div>
								<h2 class="s-panel-title">{{ __('Perfil y creación del curso') }}</h2>
								<p class="s-panel-desc">{{ __('Responde unas preguntas rápidas y crea la malla de módulos y lecciones.') }}</p>
							</div>
							<div class="flex flex-wrap gap-2">
								<Button :label="__('Crear preguntas')" :disabled="!currentSession" :loading="loading === 'questions'" @click="generateQuestions" />
								<Button :label="__('Crear curso completo')" variant="solid" :disabled="!currentSession" :loading="loading === 'plan'" @click="generatePlan" />
							</div>
						</div>
						<div v-if="loading === 'plan'" class="s-loader">
							<div class="s-loader-spinner"></div>
							{{ __('Creando módulos, lecciones y ruta de estudio...') }}
						</div>
						<div class="twin-grid">
							<div class="twin-card">
								<div class="twin-card-header">
									<Layers class="h-4 w-4 stroke-1.5" />
									<h3>{{ __('Temas detectados') }}</h3>
								</div>
								<div class="twin-card-body">
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
							<div class="twin-card">
								<div class="twin-card-header">
									<UserCog class="h-4 w-4 stroke-1.5" />
									<h3>{{ __('Perfil de aprendizaje') }}</h3>
								</div>
								<div class="twin-card-body">
									<div v-for="question in currentSession?.profile_questions || []" :key="question.id" class="profile-q">
										<div class="profile-q-text">{{ question.question }}</div>
										<select v-model="profileAnswers[question.id]" class="s-select s-select--sm">
											<option value="">{{ __('Selecciona una opción') }}</option>
											<option v-for="option in question.options || []" :key="option.label" :value="option.label">{{ option.label }}</option>
										</select>
									</div>
									<div v-if="!currentSession?.profile_questions?.length" class="s-mini-empty">
										<UserCog class="h-5 w-5 stroke-1.5" />
										<span>{{ __('Pulsa "Crear preguntas" cuando ya tengas temas detectados.') }}</span>
									</div>
								</div>
							</div>
						</div>
					</div>
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
					<div class="s-panel s-panel--flush">
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
						<div v-if="loading === 'lesson'" class="s-loader">
							<div class="s-loader-spinner"></div>
							{{ __('Preparando tu lección personalizada...') }}
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
								<div class="key-idea-text">{{ lessonPack.keyIdea || __('Esta lección ya está lista para estudiar.') }}</div>
							</div>
							<div v-if="lessonPack.conceptCards?.length" class="concept-grid">
								<div v-for="card in lessonPack.conceptCards" :key="card.title" class="concept-card">
									<h3 class="concept-title">{{ card.title }}</h3>
									<p class="concept-body">{{ card.body }}</p>
									<div v-if="card.formula" class="concept-formula">{{ card.formula }}</div>
								</div>
							</div>
							<div v-for="(section, index) in lessonPack.sections || []" :key="section.title" class="content-block">
								<div class="content-block-header">
									<span class="content-num">{{ index + 1 }}</span>
									<div>
										<h3 class="content-title">{{ section.title }}</h3>
										<p class="content-summary">{{ section.summary }}</p>
									</div>
								</div>
								<ul class="content-points">
									<li v-for="point in section.keyPoints || []" :key="point">
										<span class="point-dot" />
										<span>{{ point }}</span>
									</li>
								</ul>
							</div>
							<div v-if="lessonPack.workedExamples?.length" class="content-block">
								<h3 class="content-title">{{ __('Ejemplo resuelto paso a paso') }}</h3>
								<div v-for="example in lessonPack.workedExamples" :key="example.title || example.problem" class="worked-example">
									<div class="example-title">{{ example.title || example.problem }}</div>
									<p v-if="example.problem" class="example-problem">{{ example.problem }}</p>
									<ol class="example-steps">
										<li v-for="(step, index) in example.steps || []" :key="index">
											<span class="content-num content-num--sm">{{ index + 1 }}</span>
											<span>{{ step }}</span>
										</li>
									</ol>
									<div v-if="example.answer" class="example-answer">
										<CheckCircle2 class="h-4 w-4 stroke-1.5" />
										{{ example.answer }}
									</div>
								</div>
							</div>
							<div v-if="lessonPack.commonMistakes?.length" class="content-block">
								<h3 class="content-title">{{ __('Errores frecuentes') }}</h3>
								<div class="mistakes-list">
									<div v-for="mistake in lessonPack.commonMistakes" :key="mistake.mistake" class="mistake-item">
										<div class="mistake-bad"><AlertTriangle class="h-3.5 w-3.5 stroke-1.5" /> {{ mistake.mistake }}</div>
										<div class="mistake-fix">{{ mistake.fix }}</div>
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

					</div>
				</div>

				<!-- Room sidebar -->
				<aside class="flex flex-col gap-6 room-sidebar">
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
							<NotebookPen class="h-4 w-4 stroke-1.5" />
							<h2 class="sidebar-title">{{ __('Notas rápidas') }}</h2>
						</div>
						<textarea v-model="whiteboardText" class="s-textarea" rows="8" :placeholder="__('Fórmulas, dudas, errores frecuentes...')" @input="saveWhiteboard" />
					</div>
				</aside>
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
const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true })

const flows = [
	{ id: 'parcial', label: __('Parcial / Final'), icon: FileQuestion, description: __('Plan intensivo, ejercicios tipo evaluación y quiz final.') },
	{ id: 'admision', label: __('Admisión'), icon: GraduationCap, description: __('Busca temarios universitarios y arma preparación por áreas.') },
	{ id: 'recordar', label: __('Recordar'), icon: Brain, description: __('Recupera temas olvidados con práctica y memoria activa.') },
	{ id: 'cero', label: __('Desde cero'), icon: BookOpen, description: __('Construye una ruta desde tus apuntes o un tema inicial.') },
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
const quizScore = computed(() => {
	if (!activeQuiz.value.length) return 0
	const answered = activeQuiz.value.filter((item) => item.selected !== undefined)
	if (!answered.length) return 0
	const correct = answered.filter((item) => item.selected === Number(item.correct || 0)).length
	return Math.round((correct / activeQuiz.value.length) * 100)
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
	return __('Estudio IA')
})
const headerSubtitle = computed(() => {
	if (isDashboard.value) return __('Crea cursos propios con IA, organizados en módulos, lecciones y práctica paso a paso.')
	if (isFlow.value) return __('Te guiamos desde tus materiales hasta un curso completo listo para estudiar.')
	if (isRoom.value) return __('Aprende una lección con explicación, práctica, quiz, tutor y diagrama.')
	return __('Todo se guarda en StudyBadge para que puedas retomarlo luego.')
})
const pageTitle = computed(() => (isDashboard.value ? '' : headerTitle.value))

onMounted(async () => {
	await loadDashboard()
	await loadRouteSession()
})

watch(() => route.fullPath, loadRouteSession)

function renderMarkdown(text) {
	if (!text) return ''
	return DOMPurify.sanitize(markdown.render(String(text)))
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
		return
	}
	currentSession.value = await api('create_session', { data: { ...draft.value, flow_id: flowId.value, goal: flowId.value } }, 'create')
	toast.success(__('Curso creado.'))
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
	const result = await api('generate_profile_questions', { session: currentSession.value.name }, 'questions')
	currentSession.value.profile_questions = result.questions
	toast.success(__('Preguntas generadas.'))
}

async function generatePlan() {
	if (!currentSession.value) return
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
		return () => h('div', { class: 'exercise-list' }, props.items.length
			? props.items.map((item, itemIndex) => h('div', { class: 'exercise-item' }, [
				h('div', { class: 'exercise-question' }, `${itemIndex + 1}. ${item.question}`),
				h('div', { class: 'exercise-options' }, (item.options || []).map((option, index) =>
					h('button', {
						class: cls(item, index),
						onClick: () => emit('answer', { item, index }),
					}, [
						h('span', { class: 'quiz-option-letter' }, String.fromCharCode(65 + index)),
						h('span', {}, option),
					])
				)),
				item.selected !== undefined ? h('div', { class: 'exercise-explanation' }, item.explanation || '') : null,
			]))
			: h('div', { class: 's-empty-sm' }, [
				h('span', { class: 'text-ink-gray-5' }, __('Genera contenido para empezar.')),
			]))
	},
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════
   STUDY PAGE — PREMIUM DESIGN SYSTEM
   ═══════════════════════════════════════════════ */

.study-page {
	min-height: 100vh;
	background: linear-gradient(180deg, #f0f4ff 0%, #f8fafc 30%, #f1f5f9 100%);
	color: var(--ink-gray-9, #111827);
}

/* ─── HERO ─── */
.study-hero {
	position: relative;
	overflow: hidden;
	border-radius: 16px;
	background: linear-gradient(135deg, #092150 0%, #12336e 100%);
	padding: 1.75rem 2rem;
	color: white;
}

.hero-decoration {
	position: absolute;
	inset: 0;
	pointer-events: none;
	overflow: hidden;
}
.hero-orb {
	position: absolute;
	border-radius: 50%;
	filter: blur(60px);
	opacity: 0.25;
}
.hero-orb--1 { top: -30px; right: -10px; width: 180px; height: 180px; background: #f59e0b; animation: float 8s ease-in-out infinite; }
.hero-orb--2 { bottom: -40px; left: 8%; width: 160px; height: 160px; background: #8b5cf6; animation: float 10s ease-in-out infinite reverse; }
.hero-orb--3 { top: 40%; right: 25%; width: 90px; height: 90px; background: #ec4899; animation: float 6s ease-in-out infinite 1s; }

@keyframes float {
	0%, 100% { transform: translateY(0) scale(1); }
	50% { transform: translateY(-15px) scale(1.05); }
}

.hero-content {
	position: relative;
	z-index: 1;
	display: flex;
	flex-direction: column;
	gap: 1.25rem;
}
@media (min-width: 1024px) {
	.hero-content { flex-direction: row; align-items: flex-end; justify-content: space-between; }
}

.hero-text { display: flex; flex-direction: column; gap: 0.5rem; }

.hero-breadcrumb { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; }
.hero-breadcrumb-link { color: #a5b4fc; text-decoration: none; font-weight: 500; transition: color 0.15s; }
.hero-breadcrumb-link:hover { color: #c7d2fe; }
.hero-breadcrumb-sep { color: rgba(165, 180, 252, 0.4); }
.hero-breadcrumb-current { color: rgba(199, 210, 254, 0.7); }

.hero-title {
	font-size: 2rem;
	font-weight: 800;
	letter-spacing: -0.02em;
	line-height: 1.15;
	background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}
.hero-subtitle { font-size: 0.9rem; line-height: 1.6; color: rgba(199, 210, 254, 0.8); max-width: 480px; }

.hero-actions { display: flex; flex-direction: column; gap: 0.75rem; align-items: flex-start; }
@media (min-width: 1024px) { .hero-actions { align-items: flex-end; } }

.hero-cta { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }

.hero-nav { display: flex; flex-wrap: wrap; gap: 0.375rem; }

.nav-pill {
	display: inline-flex;
	align-items: center;
	gap: 0.375rem;
	padding: 0.4rem 0.75rem;
	border-radius: 9999px;
	font-size: 0.8rem;
	font-weight: 500;
	text-decoration: none;
	transition: all 0.2s ease;
	border: 1px solid rgba(255, 255, 255, 0.1);
	color: rgba(199, 210, 254, 0.8);
	background: rgba(255, 255, 255, 0.06);
	backdrop-filter: blur(8px);
}
.nav-pill:hover {
	background: rgba(255, 255, 255, 0.12);
	color: white;
}
.nav-pill--active {
	background: rgba(255, 255, 255, 0.18);
	border-color: rgba(255, 255, 255, 0.25);
	color: white;
	box-shadow: 0 0 12px rgba(99, 102, 241, 0.2);
}
.nav-pill-label { display: none; }
@media (min-width: 640px) { .nav-pill-label { display: inline; } }

/* ─── PANELS ─── */
.s-panel {
	border: 1px solid #e2e8f0;
	border-radius: 14px;
	background: #ffffff;
	box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
	transition: box-shadow 0.3s ease;
}
.s-panel:hover { box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06); }
.s-panel--flush > * { padding-left: 1.25rem; padding-right: 1.25rem; }
.s-panel--flush > *:first-child { padding-top: 1.25rem; }
.s-panel--flush > *:last-child { padding-bottom: 1.25rem; }

.s-panel-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
	padding-bottom: 1rem;
	border-bottom: 1px solid #f1f5f9;
}
@media (max-width: 768px) { .s-panel-header { flex-direction: column; } }

.s-panel-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 0.25rem; }
.s-panel-desc { font-size: 0.85rem; line-height: 1.55; color: #64748b; margin-top: 0.25rem; max-width: 42rem; }

.s-kicker {
	display: inline-flex;
	align-items: center;
	gap: 0.375rem;
	font-size: 0.7rem;
	font-weight: 700;
	letter-spacing: 0.06em;
	text-transform: uppercase;
	color: #6366f1;
}

/* ─── FLOW CARDS ─── */
.flow-grid { display: grid; gap: 0.75rem; padding-top: 1rem; }
@media (min-width: 640px) { .flow-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1280px) { .flow-grid { grid-template-columns: repeat(4, 1fr); } }

.flow-card {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	padding: 1rem;
	border-radius: 12px;
	border: 1px solid #e2e8f0;
	background: #fff;
	text-align: left;
	transition: all 0.2s ease;
	cursor: pointer;
	position: relative;
}
.flow-card:hover {
	border-color: #a5b4fc;
	box-shadow: 0 8px 24px rgba(99, 102, 241, 0.08);
	transform: translateY(-2px);
}

.flow-icon {
	display: grid;
	width: 40px;
	height: 40px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 10px;
}
.flow-icon--parcial { background: #fef3c7; color: #d97706; }
.flow-icon--admision { background: #dbeafe; color: #2563eb; }
.flow-icon--recordar { background: #f3e8ff; color: #9333ea; }
.flow-icon--cero { background: #dcfce7; color: #16a34a; }

.flow-info { min-width: 0; flex: 1; }
.flow-card-title { font-size: 0.875rem; font-weight: 700; color: #0f172a; }
.flow-card-desc { font-size: 0.8rem; line-height: 1.45; color: #64748b; margin-top: 0.25rem; }

.flow-arrow {
	width: 16px;
	height: 16px;
	flex-shrink: 0;
	color: #cbd5e1;
	margin-top: 2px;
	transition: transform 0.2s ease, color 0.2s ease;
}
.flow-card:hover .flow-arrow { transform: translateX(3px); color: #6366f1; }

/* ─── COURSE CARDS ─── */
.courses-grid { display: grid; gap: 1rem; padding-top: 1rem; }
@media (min-width: 1024px) { .courses-grid { grid-template-columns: repeat(2, 1fr); } }
.courses-grid--3 { }
@media (min-width: 768px) { .courses-grid--3 { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1280px) { .courses-grid--3 { grid-template-columns: repeat(3, 1fr); } }

.course-card {
	border: 1px solid #e2e8f0;
	border-radius: 12px;
	background: #fff;
	padding: 1.125rem;
	display: flex;
	flex-direction: column;
	gap: 0.875rem;
	transition: all 0.2s ease;
}
.course-card:hover {
	border-color: #c7d2fe;
	box-shadow: 0 6px 24px rgba(99, 102, 241, 0.06);
}

.course-card-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; }

.course-tag {
	display: inline-block;
	padding: 0.2rem 0.5rem;
	border-radius: 6px;
	font-size: 0.65rem;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 0.04em;
}
.course-tag--parcial { background: #fef3c7; color: #92400e; }
.course-tag--admision { background: #dbeafe; color: #1e40af; }
.course-tag--recordar { background: #f3e8ff; color: #7e22ce; }
.course-tag--cero { background: #dcfce7; color: #166534; }

.course-card-title {
	font-size: 1.05rem;
	font-weight: 700;
	color: #0f172a;
	margin-top: 0.375rem;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}
.course-card-date { display: flex; align-items: center; gap: 0.375rem; font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem; }

.course-progress-ring { width: 48px; height: 48px; flex-shrink: 0; position: relative; }
.course-progress-ring svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: #e2e8f0; stroke-width: 3; }
.ring-fill { fill: none; stroke: #6366f1; stroke-width: 3; stroke-linecap: round; transition: stroke-dasharray 0.6s ease; }
.ring-text { position: absolute; inset: 0; display: grid; place-items: center; font-size: 0.65rem; font-weight: 700; color: #4f46e5; }

.course-progress-bar { display: flex; flex-direction: column; gap: 0.375rem; }
.progress-label { font-size: 0.7rem; color: #94a3b8; text-align: right; }

.progress-track { height: 6px; border-radius: 9999px; background: #e2e8f0; overflow: hidden; }
.progress-track--lg { height: 8px; }
.progress-track--sm { height: 4px; margin-top: 0.75rem; }
.progress-fill {
	height: 100%;
	border-radius: 9999px;
	background: linear-gradient(90deg, #6366f1, #8b5cf6);
	transition: width 0.6s ease;
}

.course-next {
	display: flex;
	align-items: center;
	gap: 0.625rem;
	padding: 0.75rem;
	border-radius: 10px;
	background: #f8fafc;
	border: 1px solid #f1f5f9;
}
.course-next-icon {
	display: grid;
	width: 32px;
	height: 32px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 8px;
	background: #e0e7ff;
	color: #4f46e5;
}
.course-next-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }
.course-next-title { font-size: 0.85rem; font-weight: 600; color: #0f172a; margin-top: 0.125rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.course-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; }

/* ─── SIDEBAR ─── */
.sidebar-header {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 1rem 1.25rem;
	border-bottom: 1px solid #f1f5f9;
	color: #6366f1;
}
.sidebar-title { font-size: 0.9rem; font-weight: 700; color: #0f172a; flex: 1; }
.sidebar-link { font-size: 0.8rem; font-weight: 600; color: #6366f1; text-decoration: none; }
.sidebar-link:hover { text-decoration: underline; }

.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; padding: 1rem 1.25rem; }
.metric-card { text-align: center; padding: 0.875rem 0.5rem; border-radius: 10px; background: #f8fafc; border: 1px solid #f1f5f9; }
.metric-value { font-size: 1.5rem; font-weight: 800; color: #0f172a; }
.metric-label { font-size: 0.7rem; color: #94a3b8; margin-top: 0.25rem; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }

.fav-list { padding: 0.625rem 1.25rem; display: flex; flex-direction: column; gap: 0.375rem; }
.fav-item {
	display: flex;
	align-items: flex-start;
	gap: 0.625rem;
	padding: 0.625rem 0.75rem;
	border-radius: 8px;
	text-decoration: none;
	color: #6366f1;
	transition: background 0.15s;
}
.fav-item:hover { background: #f8fafc; }
.fav-item-title { font-size: 0.85rem; font-weight: 600; color: #0f172a; }
.fav-item-date { font-size: 0.7rem; color: #94a3b8; margin-top: 0.125rem; }

/* ─── BUILDER STEPS ─── */
.builder-header { display: flex; align-items: center; gap: 0.75rem; padding: 1.25rem; color: #6366f1; border-bottom: 1px solid #f1f5f9; }
.builder-desc { font-size: 0.85rem; line-height: 1.55; color: #64748b; padding: 0.75rem 1.25rem 0; }

.steps-list { display: flex; flex-direction: column; gap: 0.5rem; padding: 1rem 1.25rem; }

.s-step {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	padding: 0.75rem;
	border-radius: 10px;
	border: 1px solid #e2e8f0;
	background: #fff;
	color: #94a3b8;
	transition: all 0.2s ease;
}
.s-step.is-active { border-color: #a5b4fc; background: #eef2ff; color: #1f2937; }
.s-step.is-done { border-color: #86efac; background: #f0fdf4; color: #166534; }

.s-step-num {
	display: grid;
	width: 26px;
	height: 26px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 50%;
	background: #f1f5f9;
	font-size: 0.75rem;
	font-weight: 700;
	color: #64748b;
}
.s-step.is-active .s-step-num { background: #6366f1; color: #fff; }
.s-step.is-done .s-step-num { background: #22c55e; color: #fff; }

.s-step-title { font-size: 0.85rem; font-weight: 600; color: inherit; }
.s-step-desc { font-size: 0.75rem; color: #94a3b8; margin-top: 0.125rem; }
.s-step.is-active .s-step-desc { color: #6366f1; }
.s-step.is-done .s-step-desc { color: #16a34a; }

/* ─── FORMS ─── */
.form-grid { display: grid; gap: 0.875rem; padding-top: 1rem; }
@media (min-width: 768px) { .form-grid { grid-template-columns: repeat(2, 1fr); } }
.form-grid--inline { grid-template-columns: 1fr 1fr auto; padding-top: 1rem; }

.s-label { display: block; font-size: 0.8rem; font-weight: 600; color: #475569; margin-bottom: 0.375rem; }

.s-select, .s-textarea {
	width: 100%;
	border-radius: 8px;
	border: 1px solid #e2e8f0;
	background: #fff;
	padding: 0.5rem 0.75rem;
	font-size: 0.875rem;
	outline: none;
	transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.s-select:focus, .s-textarea:focus {
	border-color: #6366f1;
	box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
.s-select--sm { padding: 0.375rem 0.625rem; font-size: 0.8rem; }
.s-textarea { resize: vertical; line-height: 1.6; }
.s-textarea--sm { min-height: 44px; }
.s-textarea--full { min-height: 520px; border-radius: 0; border-left: 0; border-right: 0; border-bottom: 0; }

/* ─── MATERIALS ─── */
.materials-list { display: flex; flex-direction: column; gap: 0.5rem; padding-top: 0.75rem; }
.material-item {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	padding: 0.75rem;
	border-radius: 8px;
	background: #f8fafc;
	border: 1px solid #f1f5f9;
}
.material-icon { display: grid; width: 32px; height: 32px; flex-shrink: 0; place-items: center; border-radius: 8px; background: #e0e7ff; color: #6366f1; }
.material-name { font-size: 0.85rem; font-weight: 600; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.material-meta { font-size: 0.7rem; color: #94a3b8; margin-top: 0.125rem; }

/* ─── TWIN CARDS ─── */
.twin-grid { display: grid; gap: 1rem; padding-top: 1rem; }
@media (min-width: 1280px) { .twin-grid { grid-template-columns: repeat(2, 1fr); } }

.twin-card { border-radius: 10px; background: #f8fafc; border: 1px solid #f1f5f9; overflow: hidden; }
.twin-card-header { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; border-bottom: 1px solid #f1f5f9; color: #6366f1; }
.twin-card-header h3 { font-size: 0.85rem; font-weight: 700; color: #0f172a; }
.twin-card-body { padding: 0.75rem 1rem; display: flex; flex-direction: column; gap: 0.5rem; }

.topic-chip {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 0.75rem;
	border-radius: 8px;
	background: #ecfdf5;
	color: #065f46;
	font-size: 0.8rem;
	font-weight: 500;
}

.profile-q { padding: 0.75rem; border-radius: 8px; background: #fff; border: 1px solid #e2e8f0; }
.profile-q-text { font-size: 0.85rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem; }

/* ─── PLAN VIEW ─── */
.plan-progress { padding-top: 1rem; }
.plan-progress-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; }
.plan-progress-label { font-size: 0.85rem; font-weight: 600; color: #0f172a; }
.plan-progress-pct { font-size: 0.85rem; font-weight: 700; color: #6366f1; }

.modules-list { display: flex; flex-direction: column; gap: 1rem; padding-top: 1rem; }

.module-card {
	border: 1px solid #e2e8f0;
	border-radius: 12px;
	background: #fff;
	overflow: hidden;
}
.module-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 0.75rem;
	padding: 1rem 1.25rem;
	border-bottom: 1px solid #f1f5f9;
	background: #fafbff;
}
.module-title { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-top: 0.25rem; }
.module-obj { font-size: 0.8rem; line-height: 1.5; color: #64748b; margin-top: 0.25rem; }
.module-badge {
	display: inline-flex;
	align-items: center;
	padding: 0.25rem 0.625rem;
	border-radius: 9999px;
	font-size: 0.7rem;
	font-weight: 700;
	background: #eef2ff;
	color: #4f46e5;
	white-space: nowrap;
}

.lessons-list { display: flex; flex-direction: column; gap: 0.375rem; padding: 0.75rem; }

.lesson-row {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 0.75rem;
	padding: 0.75rem;
	border-radius: 10px;
	border: 1px solid transparent;
	text-align: left;
	transition: all 0.15s ease;
	cursor: pointer;
}
.lesson-row:hover { background: #f8fafc; border-color: #e2e8f0; }

.lesson-left { display: flex; align-items: flex-start; gap: 0.75rem; min-width: 0; }

.lesson-check {
	display: grid;
	width: 28px;
	height: 28px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 50%;
	background: #f1f5f9;
	color: #cbd5e1;
	transition: all 0.2s;
}
.lesson-check.is-done { background: #dcfce7; color: #22c55e; }

.lesson-title { font-size: 0.875rem; font-weight: 600; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lesson-obj { font-size: 0.8rem; line-height: 1.4; color: #94a3b8; margin-top: 0.125rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

.lesson-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem; flex-shrink: 0; }
.lesson-duration { display: flex; align-items: center; gap: 0.25rem; font-size: 0.7rem; font-weight: 500; padding: 0.2rem 0.5rem; border-radius: 6px; background: #eef2ff; color: #4f46e5; }
.lesson-diff { font-size: 0.65rem; color: #94a3b8; }

/* ─── SUMMARY SIDEBAR ─── */
.summary-stats { display: flex; flex-direction: column; gap: 0.5rem; padding: 0.75rem 1.25rem; }
.summary-stat { padding: 0.75rem; border-radius: 8px; background: #f8fafc; border: 1px solid #f1f5f9; }
.summary-stat-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }
.summary-stat-value { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-top: 0.25rem; }
.summary-stat--highlight { background: #eef2ff; border-color: #c7d2fe; }
.summary-stat-next { font-size: 0.85rem; font-weight: 600; color: #4f46e5; margin-top: 0.25rem; }

/* ─── ROOM STEPS ─── */
.room-steps { display: grid; gap: 0.5rem; padding-top: 1rem; }
@media (min-width: 768px) { .room-steps { grid-template-columns: repeat(3, 1fr); } }

.room-step {
	display: flex;
	align-items: flex-start;
	gap: 0.625rem;
	padding: 0.75rem;
	border-radius: 10px;
	border: 1px solid #e2e8f0;
	background: #fff;
	color: #94a3b8;
}
.room-step.is-active { border-color: #a5b4fc; background: #eef2ff; color: #1f2937; }

.room-step-num {
	display: grid;
	width: 24px;
	height: 24px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 50%;
	background: #f1f5f9;
	font-size: 0.7rem;
	font-weight: 700;
	color: #64748b;
}
.room-step.is-active .room-step-num { background: #6366f1; color: #fff; }

.room-step strong { font-size: 0.85rem; }
.room-step p { font-size: 0.75rem; margin-top: 0.125rem; }

/* ─── LESSON CONTENT ─── */
.diagram-img { width: 100%; border-radius: 10px; border: 1px solid #e2e8f0; margin-top: 1rem; }

.lesson-content { display: flex; flex-direction: column; gap: 1.25rem; padding-top: 1rem; }

.key-idea {
	padding: 1rem 1.25rem;
	border-radius: 12px;
	background: linear-gradient(135deg, #eef2ff, #e0e7ff);
	border: 1px solid #c7d2fe;
}
.key-idea-label { display: flex; align-items: center; gap: 0.375rem; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #4338ca; }
.key-idea-text { font-size: 0.95rem; font-weight: 500; line-height: 1.6; color: #312e81; margin-top: 0.5rem; }

.concept-grid { display: grid; gap: 0.75rem; }
@media (min-width: 768px) { .concept-grid { grid-template-columns: repeat(2, 1fr); } }

.concept-card {
	padding: 1rem;
	border-radius: 10px;
	border: 1px solid #e2e8f0;
	background: #fff;
}
.concept-title { font-size: 0.95rem; font-weight: 700; color: #0f172a; }
.concept-body { font-size: 0.85rem; line-height: 1.6; color: #475569; margin-top: 0.5rem; }
.concept-formula { margin-top: 0.75rem; padding: 0.5rem 0.75rem; border-radius: 6px; background: #f8fafc; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #334155; border: 1px solid #f1f5f9; }

.content-block {
	padding: 1rem;
	border-radius: 10px;
	border: 1px solid #e2e8f0;
	background: #fff;
}
.content-block-header { display: flex; align-items: flex-start; gap: 0.75rem; }
.content-num {
	display: grid;
	width: 26px;
	height: 26px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 50%;
	background: #eef2ff;
	font-size: 0.7rem;
	font-weight: 700;
	color: #4f46e5;
}
.content-num--sm { width: 22px; height: 22px; font-size: 0.65rem; }
.content-title { font-size: 1rem; font-weight: 700; color: #0f172a; }
.content-summary { font-size: 0.85rem; line-height: 1.6; color: #475569; margin-top: 0.375rem; }

.content-points { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.75rem; }
.content-points li { display: flex; align-items: flex-start; gap: 0.625rem; font-size: 0.85rem; line-height: 1.55; color: #475569; }
.point-dot { width: 6px; height: 6px; flex-shrink: 0; border-radius: 50%; background: #6366f1; margin-top: 7px; }

.worked-example { margin-top: 1rem; padding: 1rem; border-radius: 10px; background: #f8fafc; border: 1px solid #f1f5f9; }
.example-title { font-size: 0.9rem; font-weight: 700; color: #0f172a; }
.example-problem { font-size: 0.85rem; line-height: 1.55; color: #475569; margin-top: 0.5rem; }
.example-steps { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.75rem; }
.example-steps li { display: flex; align-items: flex-start; gap: 0.625rem; font-size: 0.85rem; line-height: 1.55; }
.example-answer { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.75rem; padding: 0.625rem 0.75rem; border-radius: 8px; background: #ecfdf5; color: #065f46; font-size: 0.85rem; font-weight: 600; }

.mistakes-list { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.75rem; }
.mistake-item { padding: 0.75rem; border-radius: 8px; background: #fef2f2; border: 1px solid #fecaca; }
.mistake-bad { display: flex; align-items: center; gap: 0.375rem; font-size: 0.85rem; font-weight: 600; color: #dc2626; }
.mistake-fix { font-size: 0.8rem; line-height: 1.5; color: #7f1d1d; margin-top: 0.25rem; }

/* ─── EXERCISES & QUIZ ─── */
.exercise-list { display: flex; flex-direction: column; gap: 0.875rem; padding-top: 0.75rem; }
.exercise-item { padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0; background: #fff; }
.exercise-question { font-size: 0.875rem; font-weight: 700; line-height: 1.5; color: #0f172a; }
.exercise-options { display: flex; flex-direction: column; gap: 0.375rem; margin-top: 0.75rem; }
.exercise-explanation { margin-top: 0.75rem; padding: 0.625rem 0.75rem; border-radius: 8px; background: #f8fafc; font-size: 0.8rem; line-height: 1.55; color: #475569; border: 1px solid #f1f5f9; }

.quiz-option {
	display: flex;
	align-items: center;
	gap: 0.625rem;
	padding: 0.625rem 0.75rem;
	border-radius: 8px;
	border: 1px solid transparent;
	font-size: 0.85rem;
	text-align: left;
	cursor: pointer;
	transition: all 0.15s ease;
}
.quiz-option-letter {
	display: grid;
	width: 24px;
	height: 24px;
	flex-shrink: 0;
	place-items: center;
	border-radius: 6px;
	font-size: 0.7rem;
	font-weight: 700;
}
.quiz-option--default { border-color: #e2e8f0; background: #fff; color: #334155; }
.quiz-option--default:hover { border-color: #a5b4fc; background: #eef2ff; }
.quiz-option--default .quiz-option-letter { background: #f1f5f9; color: #64748b; }
.quiz-option--correct { border-color: #86efac; background: #f0fdf4; color: #166534; }
.quiz-option--correct .quiz-option-letter { background: #22c55e; color: #fff; }
.quiz-option--wrong { border-color: #fca5a5; background: #fef2f2; color: #991b1b; }
.quiz-option--wrong .quiz-option-letter { background: #ef4444; color: #fff; }
.quiz-option--dimmed { border-color: #f1f5f9; background: #fafafa; color: #94a3b8; }
.quiz-option--dimmed .quiz-option-letter { background: #f1f5f9; color: #cbd5e1; }

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

/* ─── CHAT ─── */
.chat-hint { font-size: 0.8rem; color: #94a3b8; line-height: 1.5; padding: 0.5rem 1.25rem 0; }

.chat-box {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	height: 360px;
	overflow-y: auto;
	padding: 0.75rem 1.25rem;
	margin-top: 0.5rem;
	border-top: 1px solid #f1f5f9;
	border-bottom: 1px solid #f1f5f9;
	background: #fafbff;
}
.chat-msg { max-width: 85%; padding: 0.5rem 0.75rem; border-radius: 10px; font-size: 0.85rem; line-height: 1.55; }
.chat-msg--user { align-self: flex-end; background: #6366f1; color: white; border-bottom-right-radius: 4px; }
.chat-msg--ai { align-self: flex-start; background: #fff; color: #334155; border: 1px solid #e2e8f0; border-bottom-left-radius: 4px; }

.chat-input-row { display: flex; gap: 0.5rem; padding: 0.75rem 1.25rem; }

/* ─── CHECKLIST ─── */
.checklist { display: flex; flex-direction: column; gap: 0.375rem; padding: 0.75rem 1.25rem; }
.checklist-item {
	display: flex;
	align-items: flex-start;
	gap: 0.625rem;
	padding: 0.625rem 0.75rem;
	border-radius: 8px;
	background: #f8fafc;
	font-size: 0.85rem;
	line-height: 1.5;
	cursor: pointer;
	transition: background 0.15s;
}
.checklist-item:hover { background: #f1f5f9; }
.checklist-box { margin-top: 2px; accent-color: #6366f1; }

/* ─── STATISTICS ─── */
.stats-grid { display: grid; gap: 0.75rem; }
@media (min-width: 768px) { .stats-grid { grid-template-columns: repeat(3, 1fr); } }

.stat-card {
	padding: 1.25rem;
	border-radius: 14px;
	border: 1px solid #e2e8f0;
	background: #fff;
	box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}
.stat-card-label { font-size: 0.85rem; color: #64748b; }
.stat-card-value { font-size: 2rem; font-weight: 800; color: #0f172a; margin-top: 0.5rem; }

/* ─── EXPLANATIONS ─── */
.explanations-list { display: flex; flex-direction: column; gap: 0.75rem; padding-top: 0.75rem; }
.explanation-card { border: 1px solid #e2e8f0; border-radius: 10px; background: #fff; padding: 1rem; }
.explanation-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; }
.explanation-title { font-size: 1rem; font-weight: 700; color: #0f172a; }
.explanation-date { font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem; }

/* ─── WHITEBOARD ─── */
.wb-actions { display: flex; flex-direction: column; gap: 0.5rem; padding: 0.75rem 1.25rem; }

/* ─── EMPTY STATES ─── */
.s-empty {
	border: 2px dashed #e2e8f0;
	border-radius: 12px;
	padding: 2.5rem 2rem;
	text-align: center;
	background: #fafbff;
}
.s-empty-icon { display: grid; place-items: center; width: 56px; height: 56px; margin: 0 auto; border-radius: 50%; background: #eef2ff; color: #6366f1; }
.s-empty-title { font-size: 1rem; font-weight: 700; color: #0f172a; margin-top: 0.75rem; }
.s-empty-desc { font-size: 0.85rem; color: #64748b; margin-top: 0.25rem; }

.s-empty-sm {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.5rem;
	padding: 1.5rem;
	border: 1px dashed #e2e8f0;
	border-radius: 10px;
	text-align: center;
	color: #94a3b8;
	font-size: 0.85rem;
}

.s-mini-empty {
	display: flex;
	align-items: center;
	gap: 0.625rem;
	padding: 0.75rem;
	border-radius: 8px;
	background: #f8fafc;
	font-size: 0.8rem;
	color: #94a3b8;
	line-height: 1.5;
}

/* ─── LOADER ─── */
.s-loader {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	margin-top: 0.75rem;
	padding: 0.875rem 1rem;
	border-radius: 10px;
	background: #eef2ff;
	border: 1px solid #c7d2fe;
	font-size: 0.85rem;
	font-weight: 600;
	color: #4338ca;
}
.s-loader-spinner {
	width: 20px;
	height: 20px;
	border: 2.5px solid #c7d2fe;
	border-top-color: #6366f1;
	border-radius: 50%;
	animation: spin 0.7s linear infinite;
	flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── MARKDOWN ─── */
.s-markdown-block {
	margin-top: 0.75rem;
	padding: 1rem;
	border-radius: 10px;
	background: #f8fafc;
	border: 1px solid #f1f5f9;
}
.s-markdown-block :deep(h1),
.s-markdown-block :deep(h2),
.s-markdown-block :deep(h3) {
	margin: 0.85rem 0 0.45rem;
	font-weight: 700;
	color: #0f172a;
}
.s-markdown-block :deep(p),
.s-markdown-block :deep(li) {
	font-size: 0.9rem;
	line-height: 1.7;
	color: #334155;
}
.s-markdown-block :deep(ul),
.s-markdown-block :deep(ol) {
	margin: 0.5rem 0 0.75rem 1.25rem;
}

@media (max-width: 768px) {
	.s-panel-header { flex-direction: column; }
	.lesson-row { flex-direction: column; }
	.form-grid--inline { grid-template-columns: 1fr; }
}/* Practice Flow Layout */
.practice-flow {
	position: relative;
}
.practice-flow-header {
	text-align: center;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 2.5rem 2rem;
	background: linear-gradient(to bottom, rgba(249, 250, 251, 0), rgba(243, 244, 246, 0.6));
	border-radius: 16px;
	border: 1px dashed rgba(209, 213, 219, 0.8);
}
.practice-flow-icon {
	width: 56px;
	height: 56px;
	border-radius: 50%;
	background: rgba(99, 102, 241, 0.1);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: 1.25rem;
	box-shadow: 0 0 0 6px rgba(99, 102, 241, 0.05);
}
.practice-flow-title {
	font-size: 1.35rem;
	font-weight: 700;
	color: #111827;
	margin-bottom: 0.5rem;
}
.practice-flow-desc {
	color: #4b5563;
	font-size: 0.95rem;
	max-width: 480px;
	line-height: 1.6;
}
.practice-card {
	border: 1px solid rgba(229, 231, 235, 1);
	box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
	overflow: hidden;
	transition: all 0.3s ease;
}
.practice-card:hover {
	box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
	border-color: rgba(209, 213, 219, 1);
	transform: translateY(-2px);
}
.practice-card-header {
	border-bottom: 1px solid rgba(229, 231, 235, 0.5);
	padding: 1.5rem 1.75rem !important;
}
.quiz-score-banner {
	display: flex;
	align-items: center;
	gap: 1.25rem;
	margin: 1.5rem;
	padding: 1.25rem 1.5rem;
	background: linear-gradient(to right, #fffbeb, #fef3c7);
	border: 1px solid #fde68a;
	border-radius: 12px;
	box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);
}

/* Sidebar & Tutor Expansion */
.room-sidebar {
	position: sticky;
	top: 1.5rem;
	align-self: flex-start;
	max-height: calc(100vh - 3rem);
	overflow-y: auto;
	scrollbar-width: thin;
	scrollbar-color: #cbd5e1 transparent;
	padding-right: 0.25rem;
	margin-right: -0.25rem;
}
.room-sidebar::-webkit-scrollbar {
	width: 4px;
}
.room-sidebar::-webkit-scrollbar-thumb {
	background-color: #cbd5e1;
	border-radius: 4px;
}
.tutor-panel {
	transition: all 0.3s ease;
}
.tutor-panel.is-expanded {
	position: fixed;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	width: 90vw;
	max-width: 800px;
	height: 85vh;
	z-index: 50;
	box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
	display: flex;
	flex-direction: column;
}
.tutor-panel.is-expanded .chat-box {
	max-height: none !important;
	flex: 1;
	overflow-y: auto;
}
.tutor-backdrop {
	position: fixed;
	inset: 0;
	background: rgba(15, 23, 42, 0.5);
	backdrop-filter: blur(4px);
	z-index: 49;
}
</style>

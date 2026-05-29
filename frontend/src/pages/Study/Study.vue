<template>
	<div class="min-h-screen bg-surface-gray-1 text-ink-gray-9">
		<div class="mx-auto flex w-full max-w-[1500px] flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
			<header class="study-hero flex flex-col gap-5 rounded-xl border border-outline-gray-1 bg-surface-white p-5 shadow-sm lg:flex-row lg:items-end lg:justify-between">
				<div>
					<div class="flex flex-wrap items-center gap-2 text-sm text-ink-gray-6">
						<router-link :to="{ name: 'Study' }" class="font-medium text-ink-blue-4">
							{{ __('Estudio IA') }}
						</router-link>
						<span v-if="pageTitle">/</span>
						<span v-if="pageTitle">{{ pageTitle }}</span>
					</div>
					<h1 class="mt-2 text-3xl font-semibold tracking-normal text-ink-gray-9 sm:text-4xl">
						{{ headerTitle }}
					</h1>
					<p class="mt-2 max-w-3xl text-base leading-7 text-ink-gray-7">
						{{ headerSubtitle }}
					</p>
				</div>
				<div class="flex flex-col gap-3">
					<Button v-if="isDashboard" variant="solid" :label="__('Crear curso IA')" @click="startFlow('parcial')">
						<template #prefix><BookOpen class="h-4 w-4 stroke-1.5" /></template>
					</Button>
					<nav class="flex flex-wrap gap-2">
						<router-link
							v-for="item in topNav"
							:key="item.name"
							:to="{ name: item.name }"
							class="inline-flex min-h-9 items-center gap-2 rounded-md border px-3 py-2 text-sm font-medium transition"
							:class="route.name === item.name ? 'border-blue-200 bg-surface-blue-2 text-ink-blue-4' : 'border-outline-gray-1 bg-surface-white text-ink-gray-7 hover:bg-surface-gray-2'"
						>
							<component :is="item.icon" class="h-4 w-4 stroke-1.5" />
							{{ item.label }}
						</router-link>
					</nav>
				</div>
			</header>

			<section v-if="isDashboard" class="grid gap-5 xl:grid-cols-[1fr_360px]">
				<div class="flex flex-col gap-5">
					<div class="study-panel p-5">
						<div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
							<div>
								<div class="study-kicker">{{ __('Empieza en 4 pasos') }}</div>
								<h2 class="mt-1 text-2xl font-semibold">{{ __('Mis cursos IA') }}</h2>
								<p class="mt-2 max-w-2xl text-sm leading-6 text-ink-gray-6">
									{{ __('Crea un curso desde tus apuntes, deja que la IA lo ordene en módulos y continúa cada lección con práctica guiada.') }}
								</p>
							</div>
							<Button variant="solid" :label="__('Crear mi primer curso')" @click="startFlow('parcial')" />
						</div>
						<div class="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
							<button
								v-for="flow in flows"
								:key="flow.id"
								class="study-action-card group"
								@click="startFlow(flow.id)"
							>
								<div class="flex items-start gap-3">
									<div class="study-icon">
										<component :is="flow.icon" class="h-5 w-5 stroke-1.5" />
									</div>
									<div>
										<h3 class="text-sm font-semibold text-ink-gray-9">{{ flow.label }}</h3>
										<p class="mt-1 text-sm leading-5 text-ink-gray-6">{{ flow.description }}</p>
									</div>
								</div>
							</button>
						</div>
					</div>

					<div class="study-panel p-5">
						<div class="flex flex-wrap items-center justify-between gap-3">
							<div>
								<div class="study-kicker">{{ __('Continúa aprendiendo') }}</div>
								<h2 class="mt-1 text-xl font-semibold">{{ __('Cursos recientes') }}</h2>
							</div>
							<Button :label="__('Actualizar')" :loading="loading === 'dashboard'" @click="loadDashboard" />
						</div>
						<div class="mt-4 grid gap-4 lg:grid-cols-2">
							<div v-for="session in sessions.slice(0, 6)" :key="session.name" class="study-course-card">
								<div class="flex items-start justify-between gap-3">
									<div class="min-w-0">
										<div class="text-xs font-medium text-ink-blue-4">{{ flowLabel(session.flow_id || session.goal) }}</div>
										<h3 class="mt-1 truncate text-lg font-semibold">{{ session.title || session.name }}</h3>
										<p class="mt-1 text-sm text-ink-gray-6">{{ __('Última actividad') }} · {{ formatDate(session.modified) }}</p>
									</div>
									<span class="study-badge">{{ courseProgress(session) }}%</span>
								</div>
								<div class="mt-4">
									<div class="flex items-center justify-between text-xs text-ink-gray-6">
										<span>{{ __('Progreso del curso') }}</span>
										<span>{{ courseProgress(session) }}% {{ __('completado') }}</span>
									</div>
									<div class="mt-2 h-2 overflow-hidden rounded-full bg-surface-gray-2">
										<div class="h-full rounded-full bg-blue-500" :style="{ width: `${courseProgress(session)}%` }" />
									</div>
								</div>
								<div class="mt-4 rounded-md bg-surface-gray-1 p-3">
									<div class="text-xs text-ink-gray-6">{{ __('Siguiente lección') }}</div>
									<div class="mt-1 truncate text-sm font-medium text-ink-gray-9">
										{{ flattenLessons(session.course_structure || fallbackCourseStructure(session))[nextLessonIndex(session)]?.title || __('Abrir curso') }}
									</div>
								</div>
								<div class="mt-4 flex flex-wrap gap-2">
									<Button :label="__('Continuar')" variant="solid" @click="openRoom(session.name, nextLessonIndex(session))" />
									<Button :label="__('Ver módulos')" @click="openPlan(session.name)" />
									<Button :label="__('Borrar')" variant="subtle" @click="deleteSession(session.name)" />
								</div>
							</div>
							<div v-if="!sessions.length" class="study-empty lg:col-span-2">
								<BookOpen class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
								<h3 class="mt-3 text-base font-semibold text-ink-gray-9">{{ __('Aún no tienes cursos IA') }}</h3>
								<p class="mt-1 text-sm text-ink-gray-6">{{ __('Crea uno con tus apuntes, PDFs o temas del parcial. Te guiaremos paso a paso.') }}</p>
								<Button class="mt-4" variant="solid" :label="__('Crear curso IA')" @click="startFlow('parcial')" />
							</div>
						</div>
					</div>
				</div>

				<aside class="flex flex-col gap-5">
					<div class="study-panel p-4">
						<h2 class="text-base font-semibold">{{ __('Tu avance') }}</h2>
						<div class="mt-3 grid grid-cols-3 gap-2">
							<div v-for="metric in dashboardMetrics" :key="metric.label" class="rounded-md bg-surface-gray-1 px-3 py-3 text-center">
								<div class="text-xs text-ink-gray-6">{{ metric.label }}</div>
								<div class="mt-1 text-xl font-semibold">{{ metric.value }}</div>
							</div>
						</div>
					</div>
					<div class="study-panel p-4">
						<div class="flex items-center justify-between gap-3">
							<h2 class="text-base font-semibold">{{ __('Explicaciones favoritas') }}</h2>
							<router-link :to="{ name: 'StudyExplanations' }" class="text-sm font-medium text-ink-blue-4">{{ __('Ver') }}</router-link>
						</div>
						<div class="mt-3 flex flex-col gap-2">
							<router-link
								v-for="explanation in explanations.slice(0, 5)"
								:key="explanation.name"
								:to="{ name: 'StudyExplanations' }"
								class="rounded-md bg-surface-gray-1 p-3 text-sm hover:bg-surface-gray-2"
							>
								<div class="font-medium text-ink-gray-9">{{ explanation.topic || __('Sin tema') }}</div>
								<div class="mt-1 text-xs text-ink-gray-6">{{ formatDate(explanation.creation) }}</div>
							</router-link>
							<div v-if="!explanations.length" class="study-mini-empty">{{ __('Guarda una explicación importante desde una lección para repasarla luego.') }}</div>
						</div>
					</div>
				</aside>
			</section>

			<section v-else-if="isFlow" class="grid gap-5 xl:grid-cols-[340px_1fr]">
				<aside class="study-panel h-fit p-4">
					<div class="study-kicker">{{ __('Constructor guiado') }}</div>
					<h2 class="mt-1 text-xl font-semibold">{{ __('Crea tu curso IA') }}</h2>
					<p class="mt-2 text-sm leading-6 text-ink-gray-6">{{ __('Completa estos pasos. Cada avance desbloquea el siguiente sin perder tu progreso.') }}</p>
					<div class="mt-5 flex flex-col gap-3">
						<div class="study-step" :class="currentSession ? 'is-done' : 'is-active'">
							<span>1</span>
							<div>
								<div class="font-medium">{{ __('Datos básicos') }}</div>
								<p>{{ currentSession ? __('Curso creado') : __('Ponle nombre y contexto') }}</p>
							</div>
						</div>
						<div class="study-step" :class="currentSession?.topics?.length ? 'is-done' : currentSession ? 'is-active' : ''">
							<span>2</span>
							<div>
								<div class="font-medium">{{ __('Material y temas') }}</div>
								<p>{{ __('Sube archivos o pega texto') }}</p>
							</div>
						</div>
						<div class="study-step" :class="currentSession?.profile_questions?.length ? 'is-done' : currentSession?.topics?.length ? 'is-active' : ''">
							<span>3</span>
							<div>
								<div class="font-medium">{{ __('Perfil') }}</div>
								<p>{{ __('Adapta el curso a tu nivel') }}</p>
							</div>
						</div>
						<div class="study-step" :class="currentSession?.course_structure?.modules?.length ? 'is-done' : currentSession?.profile_questions?.length ? 'is-active' : ''">
							<span>4</span>
							<div>
								<div class="font-medium">{{ __('Curso listo') }}</div>
								<p>{{ __('Genera módulos y lecciones') }}</p>
							</div>
						</div>
					</div>
				</aside>

				<div class="flex flex-col gap-5">
					<div class="study-panel p-5">
						<div class="study-section-heading">
							<div>
								<div class="study-kicker">{{ __('Paso 1') }}</div>
								<h2>{{ __('Datos básicos del curso') }}</h2>
								<p>{{ __('Con esto la IA entiende qué estás preparando y cuánto contexto tiene.') }}</p>
							</div>
							<Button :label="currentSession ? __('Guardar cambios') : __('Crear curso')" variant="solid" :loading="loading === 'create'" @click="createOrUpdateSession" />
						</div>
						<div class="mt-4 grid gap-3 md:grid-cols-2">
							<FormControl v-model="draft.title" :label="__('Nombre del curso')" :placeholder="__('Ej. Parcial de cálculo')" />
							<FormControl v-model="draft.academic_context" :label="__('Curso o contexto')" :placeholder="__('Ej. Universidad, curso, ciclo')" />
							<FormControl v-model="draft.exam_date" type="date" :label="__('Fecha objetivo')" />
							<div>
								<label class="mb-1 block text-sm text-ink-gray-7">{{ __('Nivel') }}</label>
								<select v-model="draft.student_level" class="study-input">
									<option value="colegio">{{ __('Colegio') }}</option>
									<option value="preuniversitario">{{ __('Preuniversitario') }}</option>
									<option value="universitario">{{ __('Universitario') }}</option>
									<option value="profesional">{{ __('Profesional') }}</option>
								</select>
							</div>
							<FormControl class="md:col-span-2" v-model="draft.desired_topics" :label="__('Temas obligatorios')" :placeholder="__('Separados por coma, opcional')" />
							<div class="md:col-span-2">
								<label class="mb-1 block text-sm text-ink-gray-7">{{ __('Texto manual') }}</label>
								<textarea v-model="draft.manual_text" class="study-textarea" rows="7" :placeholder="__('Pega sílabos, apuntes, ejercicios o temas del parcial.')" />
							</div>
						</div>
					</div>

					<div v-if="flowId === 'admision'" class="study-panel p-5">
						<div class="study-section-heading">
							<div>
								<div class="study-kicker">{{ __('Opcional') }}</div>
								<h2>{{ __('Buscar temario de admisión') }}</h2>
								<p>{{ __('La IA trae una base de temas para convertirla en curso.') }}</p>
							</div>
						</div>
						<div class="mt-4 grid gap-3 md:grid-cols-[1fr_1fr_auto]">
							<FormControl v-model="university" :placeholder="__('Universidad')" />
							<FormControl v-model="career" :placeholder="__('Carrera, opcional')" />
							<Button :label="__('Buscar')" :loading="loading === 'search'" @click="searchTemario" />
						</div>
						<div v-if="searchResult" class="study-markdown mt-4 rounded-lg bg-surface-gray-1 p-4" v-html="renderMarkdown(searchResult)" />
					</div>

					<div class="study-panel p-5">
						<div class="study-section-heading">
							<div>
								<div class="study-kicker">{{ __('Paso 2') }}</div>
								<h2>{{ __('Materiales y temas') }}</h2>
								<p>{{ __('Sube PDF, imágenes o Word. Luego analiza para detectar los temas del curso.') }}</p>
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
						<div v-if="loading === 'analyze'" class="study-loader mt-4">{{ __('Analizando material y ordenando temas...') }}</div>
						<div class="mt-4 grid gap-2">
							<div v-for="material in currentSession?.materials || []" :key="material.idx" class="flex items-center justify-between gap-3 rounded-md bg-surface-gray-1 px-3 py-3">
								<div class="min-w-0">
									<div class="truncate text-sm font-medium">{{ material.file_name }}</div>
									<div class="text-xs text-ink-gray-6">{{ material.file_type }} · {{ material.analysis_status }}</div>
								</div>
								<FileText class="h-4 w-4 shrink-0 stroke-1.5 text-ink-gray-5" />
							</div>
							<div v-if="!currentSession?.materials?.length" class="study-empty">
								<Upload class="mx-auto h-7 w-7 stroke-1.5 text-ink-gray-5" />
								<h3 class="mt-2 text-sm font-semibold">{{ currentSession ? __('Agrega material para mejorar el curso') : __('Primero crea el curso') }}</h3>
								<p class="mt-1 text-sm text-ink-gray-6">{{ currentSession ? __('También puedes usar solo el texto manual del paso 1.') : __('Así se activará la subida de archivos.') }}</p>
							</div>
						</div>
					</div>

					<div class="study-panel p-5">
						<div class="study-section-heading">
							<div>
								<div class="study-kicker">{{ __('Pasos 3 y 4') }}</div>
								<h2>{{ __('Perfil y creación del curso') }}</h2>
								<p>{{ __('Responde unas preguntas rápidas y crea la malla de módulos y lecciones.') }}</p>
							</div>
							<div class="flex flex-wrap gap-2">
								<Button :label="__('Crear preguntas')" :disabled="!currentSession" :loading="loading === 'questions'" @click="generateQuestions" />
								<Button :label="__('Crear curso completo')" variant="solid" :disabled="!currentSession" :loading="loading === 'plan'" @click="generatePlan" />
							</div>
						</div>
						<div v-if="loading === 'plan'" class="study-loader mt-4">{{ __('Creando módulos, lecciones y ruta de estudio...') }}</div>
						<div class="mt-4 grid gap-4 xl:grid-cols-2">
							<div class="rounded-lg bg-surface-gray-1 p-4">
								<h3 class="text-sm font-semibold text-ink-gray-8">{{ __('Temas detectados') }}</h3>
								<div class="mt-3 flex flex-col gap-2">
									<div v-for="topic in currentSession?.topics || []" :key="topic.title || topic" class="rounded-md bg-surface-green-1 px-3 py-2 text-sm text-ink-green-4">
										{{ topic.title || topic }}
									</div>
									<div v-if="!currentSession?.topics?.length" class="study-mini-empty">{{ __('Cuando analices tu material, aquí aparecerán los temas base.') }}</div>
								</div>
							</div>
							<div class="rounded-lg bg-surface-gray-1 p-4">
								<h3 class="text-sm font-semibold text-ink-gray-8">{{ __('Perfil de aprendizaje') }}</h3>
								<div class="mt-3 flex flex-col gap-3">
									<div v-for="question in currentSession?.profile_questions || []" :key="question.id" class="rounded-md border border-outline-gray-1 bg-surface-white p-3">
										<div class="text-sm font-medium">{{ question.question }}</div>
										<select v-model="profileAnswers[question.id]" class="study-input mt-2">
											<option value="">{{ __('Selecciona una opción') }}</option>
											<option v-for="option in question.options || []" :key="option.label" :value="option.label">{{ option.label }}</option>
										</select>
									</div>
									<div v-if="!currentSession?.profile_questions?.length" class="study-mini-empty">{{ __('Pulsa “Crear preguntas” cuando ya tengas temas detectados.') }}</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</section>

			<section v-else-if="isPlan" class="grid gap-5 xl:grid-cols-[1fr_340px]">
				<div class="study-panel p-5">
					<div class="flex flex-wrap items-start justify-between gap-3">
						<div>
							<div class="study-kicker">{{ __('Curso IA personal') }}</div>
							<h2 class="mt-1 text-2xl font-semibold">{{ courseStructure.courseTitle || currentSession?.title }}</h2>
							<p class="mt-2 max-w-3xl text-sm leading-6 text-ink-gray-6">{{ currentSession?.profile_summary || courseStructure.courseGoal || __('Malla curricular generada por TutorIA.') }}</p>
						</div>
						<div class="flex flex-wrap gap-2">
							<Button :label="__('Continuar')" variant="solid" @click="openRoom(currentSession.name, nextLessonIndex(currentSession))" />
							<Button :label="__('Rehacer plan')" :loading="loading === 'plan'" @click="generatePlan" />
						</div>
					</div>
					<div class="mt-5 rounded-lg bg-surface-gray-1 p-4">
						<div class="flex items-center justify-between text-sm">
							<span class="font-medium">{{ __('Progreso total') }}</span>
							<span class="text-ink-gray-6">{{ courseProgress(currentSession) }}%</span>
						</div>
						<div class="mt-2 h-2 overflow-hidden rounded-full bg-surface-white">
							<div class="h-full rounded-full bg-blue-500" :style="{ width: `${courseProgress(currentSession)}%` }" />
						</div>
					</div>
					<div class="mt-5 grid gap-4">
						<div v-for="(module, moduleIndex) in courseStructure.modules || []" :key="module.title || moduleIndex" class="study-module-card">
							<div class="flex flex-wrap items-start justify-between gap-3">
								<div>
									<div class="study-kicker">{{ module.period || `${__('Módulo')} ${moduleIndex + 1}` }}</div>
									<h3 class="mt-1 text-lg font-semibold">{{ module.title }}</h3>
									<p class="mt-1 text-sm leading-6 text-ink-gray-6">{{ module.objective }}</p>
								</div>
								<span class="study-badge">{{ module.lessons?.length || 0 }} {{ __('lecciones') }}</span>
							</div>
							<div class="mt-4 grid gap-2">
								<button
									v-for="lesson in module.lessons || []"
									:key="lesson.key || lesson.title"
									class="study-lesson-row"
									@click="openRoom(currentSession.name, lessonGlobalIndex(lesson))"
								>
									<div class="flex min-w-0 items-start gap-3">
										<div class="study-lesson-check" :class="isLessonDone(lesson) ? 'is-done' : ''">
											<CheckCircle2 class="h-4 w-4 stroke-1.5" />
										</div>
										<div class="min-w-0">
											<div class="truncate text-sm font-semibold text-ink-gray-9">{{ lesson.title }}</div>
											<p class="mt-1 line-clamp-2 text-sm leading-5 text-ink-gray-6">{{ lesson.objective }}</p>
										</div>
									</div>
									<div class="flex shrink-0 flex-col items-end gap-1">
										<span class="rounded bg-surface-blue-1 px-2 py-1 text-xs text-ink-blue-4">{{ lesson.duration || __('30 min') }}</span>
										<span class="text-xs text-ink-gray-5">{{ lesson.difficulty || __('medio') }}</span>
									</div>
								</button>
							</div>
						</div>
						<div v-if="!lessonsFlat.length" class="study-empty">
							<ClipboardCheck class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
							<h3 class="mt-2 text-base font-semibold">{{ __('El curso aún no tiene lecciones') }}</h3>
							<p class="mt-1 text-sm text-ink-gray-6">{{ __('Vuelve al constructor y crea el plan completo.') }}</p>
						</div>
					</div>
				</div>
				<aside class="study-panel h-fit p-4">
					<h2 class="text-base font-semibold">{{ __('Resumen del curso') }}</h2>
					<div class="mt-3 flex flex-col gap-2">
						<div class="rounded-md bg-surface-gray-1 p-3">
							<div class="text-xs text-ink-gray-6">{{ __('Lecciones') }}</div>
							<div class="mt-1 text-2xl font-semibold">{{ lessonsFlat.length }}</div>
						</div>
						<div class="rounded-md bg-surface-gray-1 p-3">
							<div class="text-xs text-ink-gray-6">{{ __('Progreso') }}</div>
							<div class="mt-1 text-2xl font-semibold">{{ courseProgress(currentSession) }}%</div>
						</div>
						<div class="rounded-md bg-surface-blue-1 p-3">
							<div class="text-xs text-ink-blue-4">{{ __('Siguiente paso') }}</div>
							<div class="mt-1 text-sm font-medium text-ink-blue-4">{{ lessonsFlat[nextLessonIndex(currentSession)]?.title || __('Revisar módulos') }}</div>
						</div>
					</div>
				</aside>
			</section>

			<section v-else-if="isRoom" class="grid gap-5 xl:grid-cols-[1fr_360px]">
				<div class="flex flex-col gap-5">
					<div class="study-panel p-5">
						<div class="flex flex-wrap items-start justify-between gap-3">
							<div>
								<div class="study-kicker">{{ activeLesson.moduleTitle || __('Lección') }}</div>
								<h2 class="mt-1 text-2xl font-semibold">{{ lessonPack.lessonTitle || activeTopicTitle }}</h2>
								<p class="mt-2 max-w-3xl text-sm leading-6 text-ink-gray-6">{{ lessonPack.learningObjective || activeLesson.objective || __('Aprende con explicación, práctica, quiz, tutor y diagrama.') }}</p>
							</div>
							<div class="flex flex-wrap gap-2">
								<Button :label="__('Regenerar')" :loading="loading === 'pack'" @click="generatePack(true)" />
								<Button :label="__('Diagrama')" :loading="loading === 'diagram'" @click="generateDiagram" />
								<Button :label="__('Guardar favorito')" @click="saveCurrentExplanation" />
							</div>
						</div>
						<div class="mt-5 grid gap-3 md:grid-cols-3">
							<div class="study-room-step is-active">
								<span>1</span>
								<div>
									<strong>{{ __('Aprende') }}</strong>
									<p>{{ __('Idea clave y explicación') }}</p>
								</div>
							</div>
							<div class="study-room-step">
								<span>2</span>
								<div>
									<strong>{{ __('Practica') }}</strong>
									<p>{{ __('Ejercicios con feedback') }}</p>
								</div>
							</div>
							<div class="study-room-step">
								<span>3</span>
								<div>
									<strong>{{ __('Comprueba') }}</strong>
									<p>{{ __('Quiz y checklist') }}</p>
								</div>
							</div>
						</div>
						<div v-if="loading === 'lesson'" class="study-loader mt-5">
							{{ __('Preparando tu lección personalizada...') }}
						</div>
					</div>

					<div class="study-panel p-5" @mouseup="captureSelection">
						<div class="study-section-heading">
							<div>
								<div class="study-kicker">{{ __('Paso 1') }}</div>
								<h2>{{ __('Entiende el tema') }}</h2>
								<p>{{ __('Lee de arriba hacia abajo. Si seleccionas un texto, el tutor puede explicarlo.') }}</p>
							</div>
						</div>
						<img v-if="diagramUrl" :src="diagramUrl" class="mt-4 w-full rounded-lg border border-outline-gray-1" />
						<div v-if="lessonPack.lessonTitle || lessonPack.sections?.length" class="mt-5 grid gap-4">
							<div class="rounded-lg bg-surface-blue-1 p-4">
								<div class="text-xs font-semibold uppercase tracking-wide text-ink-blue-3">{{ __('Idea clave') }}</div>
								<div class="mt-2 text-base font-medium leading-7 text-ink-blue-4">{{ lessonPack.keyIdea || __('Esta lección ya está lista para estudiar.') }}</div>
							</div>
							<div v-if="lessonPack.conceptCards?.length" class="grid gap-3 md:grid-cols-2">
								<div v-for="card in lessonPack.conceptCards" :key="card.title" class="study-concept-card">
									<h3 class="text-base font-semibold">{{ card.title }}</h3>
									<p class="mt-2 text-sm leading-6 text-ink-gray-7">{{ card.body }}</p>
									<div v-if="card.formula" class="mt-3 rounded bg-surface-gray-1 px-3 py-2 font-mono text-sm">{{ card.formula }}</div>
								</div>
							</div>
							<div v-for="(section, index) in lessonPack.sections || []" :key="section.title" class="study-content-block">
								<div class="flex items-start gap-3">
									<span class="study-number">{{ index + 1 }}</span>
									<div>
										<h3 class="text-lg font-semibold">{{ section.title }}</h3>
										<p class="mt-2 text-sm leading-7 text-ink-gray-7">{{ section.summary }}</p>
									</div>
								</div>
								<ul class="mt-3 grid gap-2">
									<li v-for="point in section.keyPoints || []" :key="point" class="flex gap-2 text-sm leading-6 text-ink-gray-7">
										<span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-500" />
										<span>{{ point }}</span>
									</li>
								</ul>
							</div>
							<div v-if="lessonPack.workedExamples?.length" class="study-content-block">
								<h3 class="text-lg font-semibold">{{ __('Ejemplo resuelto paso a paso') }}</h3>
								<div v-for="example in lessonPack.workedExamples" :key="example.title || example.problem" class="mt-4 rounded-md bg-surface-gray-1 p-4">
									<div class="text-sm font-semibold">{{ example.title || example.problem }}</div>
									<p v-if="example.problem" class="mt-2 text-sm leading-6 text-ink-gray-7">{{ example.problem }}</p>
									<ol class="mt-3 grid gap-2">
										<li v-for="(step, index) in example.steps || []" :key="index" class="flex gap-3 text-sm leading-6">
											<span class="study-number">{{ index + 1 }}</span>
											<span>{{ step }}</span>
										</li>
									</ol>
									<div v-if="example.answer" class="mt-3 rounded bg-surface-green-1 px-3 py-2 text-sm text-ink-green-4">{{ example.answer }}</div>
								</div>
							</div>
							<div v-if="lessonPack.commonMistakes?.length" class="study-content-block">
								<h3 class="text-lg font-semibold">{{ __('Errores frecuentes') }}</h3>
								<div class="mt-3 grid gap-2">
									<div v-for="mistake in lessonPack.commonMistakes" :key="mistake.mistake" class="rounded-md bg-surface-red-1 p-3 text-sm leading-6">
										<strong>{{ mistake.mistake }}</strong>
										<div class="mt-1 text-ink-gray-7">{{ mistake.fix }}</div>
									</div>
								</div>
							</div>
						</div>
						<div v-else class="study-empty mt-4">
							<RotateCcw class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
							<h3 class="mt-2 text-base font-semibold">{{ __('Prepararemos esta lección automáticamente') }}</h3>
							<p class="mt-1 text-sm text-ink-gray-6">{{ __('Si tarda, usa “Regenerar” para pedir una nueva versión.') }}</p>
						</div>
					</div>

					<div class="grid gap-5 xl:grid-cols-2">
						<div class="study-panel p-4">
							<div class="study-section-heading">
								<div>
									<div class="study-kicker">{{ __('Paso 2') }}</div>
									<h2>{{ __('Practica') }}</h2>
									<p>{{ __('Responde y revisa la explicación de cada opción.') }}</p>
								</div>
								<Button :label="__('Generar')" :loading="loading === 'exercises'" @click="generateExercises" />
							</div>
							<ExerciseList :items="lessonPack.practice?.length ? lessonPack.practice : exercises" @answer="handleAnswer" />
						</div>
						<div class="study-panel p-4">
							<div class="study-section-heading">
								<div>
									<div class="study-kicker">{{ __('Paso 3') }}</div>
									<h2>{{ __('Quiz final') }}</h2>
									<p>{{ __('Comprueba si puedes pasar a la siguiente lección.') }}</p>
								</div>
								<Button :label="__('Generar')" :loading="loading === 'quiz'" @click="generateQuiz" />
							</div>
							<ExerciseList :items="lessonPack.quiz?.length ? lessonPack.quiz : quiz" @answer="handleQuizAnswer" />
							<div v-if="activeQuiz.length" class="mt-3 rounded-md bg-surface-blue-1 p-3 text-sm text-ink-blue-4">
								{{ __('Puntaje') }}: {{ quizScore }}%
							</div>
						</div>
					</div>
				</div>

				<aside class="flex flex-col gap-5">
					<div class="study-panel p-4">
						<h2 class="text-base font-semibold">{{ __('Checklist de dominio') }}</h2>
						<div v-if="lessonPack.masteryChecklist?.length" class="mt-3 grid gap-2">
							<label v-for="item in lessonPack.masteryChecklist" :key="item" class="flex items-start gap-2 rounded-md bg-surface-gray-1 p-3 text-sm leading-6">
								<input type="checkbox" class="mt-1 rounded border-outline-gray-3" @change="markProgress({ explanation_viewed: true })" />
								<span>{{ item }}</span>
							</label>
						</div>
						<div v-else class="study-mini-empty mt-3">{{ __('Termina la explicación para ver qué debes dominar.') }}</div>
					</div>
					<div class="study-panel p-4">
						<h2 class="text-base font-semibold">{{ __('Tutor contextual') }}</h2>
						<p class="mt-1 text-sm text-ink-gray-6">{{ __('Pregunta dudas o selecciona texto de la lección para pedir una explicación.') }}</p>
						<div ref="chatBox" class="mt-3 flex h-[360px] flex-col gap-3 overflow-y-auto rounded-md bg-surface-gray-1 p-3">
							<div
								v-for="message in chatMessages"
								:key="message.id || message.content"
								class="rounded-md px-3 py-2 text-sm leading-6"
								:class="message.role === 'user' ? 'self-end bg-surface-blue-2 text-ink-blue-4' : 'self-start bg-surface-white text-ink-gray-8'"
								v-html="renderMarkdown(message.content)"
							/>
						</div>
						<div class="mt-3 flex gap-2">
							<textarea v-model="chatInput" class="study-textarea min-h-11 flex-1" rows="2" :placeholder="__('Pregunta sobre este tema')" @keydown.enter.exact.prevent="sendChat" />
							<Button :disabled="!chatInput.trim()" :loading="loading === 'chat'" @click="sendChat">
								<template #icon><SendHorizontal class="h-4 w-4 stroke-1.5" /></template>
							</Button>
						</div>
					</div>

					<div class="study-panel p-4">
						<h2 class="text-base font-semibold">{{ __('Notas rápidas') }}</h2>
						<textarea v-model="whiteboardText" class="study-textarea mt-3" rows="8" :placeholder="__('Fórmulas, dudas, errores frecuentes...')" @input="saveWhiteboard" />
					</div>
				</aside>
			</section>

			<section v-else-if="isHistory" class="study-panel p-5">
				<div class="flex flex-wrap items-center justify-between gap-3">
					<div>
						<div class="study-kicker">{{ __('Biblioteca') }}</div>
						<h2 class="mt-1 text-xl font-semibold">{{ __('Todos tus cursos IA') }}</h2>
						<p class="mt-1 text-sm text-ink-gray-6">{{ __('Reanuda, revisa módulos o elimina cursos que ya no necesites.') }}</p>
					</div>
					<Button :label="__('Actualizar')" :loading="loading === 'dashboard'" @click="loadDashboard" />
				</div>
				<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
					<div v-for="session in sessions" :key="session.name" class="study-course-card">
						<div class="text-xs font-medium text-ink-blue-4">{{ flowLabel(session.flow_id || session.goal) }}</div>
						<h3 class="mt-1 text-base font-semibold">{{ session.title || session.name }}</h3>
						<p class="mt-1 text-sm text-ink-gray-6">{{ formatDate(session.modified) }}</p>
						<div class="mt-3 h-2 overflow-hidden rounded-full bg-surface-gray-2">
							<div class="h-full rounded-full bg-blue-500" :style="{ width: `${courseProgress(session)}%` }" />
						</div>
						<div class="mt-4 flex flex-wrap gap-2">
							<Button :label="__('Continuar')" variant="solid" @click="openRoom(session.name, nextLessonIndex(session))" />
							<Button :label="__('Módulos')" @click="openPlan(session.name)" />
							<Button :label="__('Borrar')" variant="subtle" @click="deleteSession(session.name)" />
						</div>
					</div>
					<div v-if="!sessions.length" class="study-empty md:col-span-2 xl:col-span-3">
						<History class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
						<h3 class="mt-2 text-base font-semibold">{{ __('Aún no hay historial') }}</h3>
						<p class="mt-1 text-sm text-ink-gray-6">{{ __('Tus cursos aparecerán aquí cuando crees el primero.') }}</p>
					</div>
				</div>
			</section>

			<section v-else-if="isStatistics" class="grid gap-4 md:grid-cols-3">
				<div v-for="metric in statisticsMetrics" :key="metric.label" class="study-panel p-5">
					<div class="text-sm text-ink-gray-6">{{ metric.label }}</div>
					<div class="mt-2 text-3xl font-semibold">{{ metric.value }}</div>
					<div class="mt-3 h-1.5 rounded-full bg-surface-gray-2">
						<div class="h-full w-1/2 rounded-full bg-blue-500" />
					</div>
				</div>
			</section>

			<section v-else-if="isExplanations" class="study-panel p-5">
				<div>
					<div class="study-kicker">{{ __('Favoritos') }}</div>
					<h2 class="mt-1 text-xl font-semibold">{{ __('Explicaciones guardadas') }}</h2>
					<p class="mt-1 text-sm text-ink-gray-6">{{ __('Aquí quedan las lecciones o fragmentos que quieras repasar después.') }}</p>
				</div>
				<div class="mt-4 grid gap-3">
					<div v-for="item in explanations" :key="item.name" class="rounded-lg border border-outline-gray-1 bg-surface-white p-4">
						<div class="flex items-start justify-between gap-3">
							<div>
								<h3 class="text-base font-semibold">{{ item.topic }}</h3>
								<p class="mt-1 text-sm text-ink-gray-6">{{ formatDate(item.creation) }}</p>
							</div>
							<Button :label="__('Borrar')" variant="subtle" @click="deleteExplanation(item.name)" />
						</div>
						<div class="study-markdown mt-3" v-html="renderMarkdown(item.content)" />
					</div>
					<div v-if="!explanations.length" class="study-empty">
						<LibraryBig class="mx-auto h-8 w-8 stroke-1.5 text-ink-gray-5" />
						<h3 class="mt-2 text-base font-semibold">{{ __('No guardaste explicaciones todavía') }}</h3>
						<p class="mt-1 text-sm text-ink-gray-6">{{ __('En una lección, usa “Guardar favorito” para traerla aquí.') }}</p>
					</div>
				</div>
			</section>

			<section v-else-if="isWhiteboard" class="grid gap-5 xl:grid-cols-[1fr_340px]">
				<div class="study-panel p-5">
					<div class="study-section-heading">
						<div>
							<div class="study-kicker">{{ __('Espacio libre') }}</div>
							<h2>{{ __('Pizarra') }}</h2>
							<p>{{ __('Escribe fórmulas, dudas, pasos de solución o un resumen rápido.') }}</p>
						</div>
					</div>
					<textarea v-model="whiteboardText" class="study-textarea mt-4 min-h-[520px]" :placeholder="__('Escribe aquí tu resolución, fórmulas o lluvia de ideas.')" @input="saveWhiteboard" />
				</div>
				<aside class="study-panel h-fit p-4">
					<h2 class="text-base font-semibold">{{ __('Acciones IA') }}</h2>
					<p class="mt-1 text-sm text-ink-gray-6">{{ __('Convierte tus notas sueltas en una guía clara o revisa posibles errores.') }}</p>
					<div class="mt-3 flex flex-col gap-2">
						<Button :label="__('Ordenar mis notas')" :loading="loading === 'whiteboard'" @click="askWhiteboard('organiza')" />
						<Button :label="__('Encontrar errores')" :loading="loading === 'whiteboard'" @click="askWhiteboard('errores')" />
					</div>
					<div class="study-markdown mt-4 rounded-md bg-surface-gray-1 p-3" v-html="renderMarkdown(whiteboardResponse)" />
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
	BarChart3,
	BookOpen,
	Brain,
	CalendarDays,
	ClipboardCheck,
	CheckCircle2,
	FileQuestion,
	FileText,
	GraduationCap,
	History,
	LibraryBig,
	NotebookPen,
	PanelTop,
	RotateCcw,
	SendHorizontal,
	Upload,
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
			if (item.selected === undefined) return 'border-outline-gray-1 bg-surface-white hover:bg-surface-gray-1'
			if (index === Number(item.correct || 0)) return 'border-green-500 bg-surface-green-1 text-ink-green-4'
			if (index === item.selected) return 'border-red-400 bg-surface-red-1 text-ink-red-4'
			return 'border-outline-gray-1 bg-surface-white text-ink-gray-6'
		}
		return () => h('div', { class: 'mt-3 flex flex-col gap-3' }, props.items.length
			? props.items.map((item, itemIndex) => h('div', { class: 'rounded-lg border border-outline-gray-1 p-3' }, [
				h('div', { class: 'text-sm font-semibold leading-6' }, `${itemIndex + 1}. ${item.question}`),
				h('div', { class: 'mt-3 grid gap-2' }, (item.options || []).map((option, index) =>
					h('button', {
						class: `rounded-md border px-3 py-2 text-left text-sm transition ${cls(item, index)}`,
						onClick: () => emit('answer', { item, index }),
					}, option)
				)),
				item.selected !== undefined ? h('div', { class: 'mt-3 rounded-md bg-surface-gray-1 p-3 text-sm leading-6 text-ink-gray-7' }, item.explanation || '') : null,
			]))
			: h('div', { class: 'rounded-md border border-dashed border-outline-gray-2 p-6 text-center text-sm text-ink-gray-6' }, __('Genera contenido para empezar.')))
	},
})
</script>

<style scoped>
.study-hero {
	background:
		linear-gradient(135deg, rgba(239, 246, 255, 0.9), rgba(255, 255, 255, 0.96) 42%),
		#ffffff;
}

.study-panel {
	border: 1px solid #e5e7eb;
	border-radius: 0.75rem;
	background: #ffffff;
	box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

.study-kicker {
	font-size: 0.75rem;
	font-weight: 650;
	letter-spacing: 0.04em;
	text-transform: uppercase;
	color: #2563eb;
}

.study-section-heading {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
}

.study-section-heading h2 {
	margin-top: 0.15rem;
	font-size: 1.125rem;
	font-weight: 650;
	color: #111827;
}

.study-section-heading p {
	margin-top: 0.25rem;
	max-width: 42rem;
	font-size: 0.875rem;
	line-height: 1.55;
	color: #4b5563;
}

.study-action-card,
.study-course-card,
.study-module-card,
.study-concept-card,
.study-content-block {
	border: 1px solid #e5e7eb;
	border-radius: 0.75rem;
	background: #ffffff;
}

.study-action-card {
	padding: 1rem;
	text-align: left;
	transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
}

.study-action-card:hover {
	border-color: #93c5fd;
	box-shadow: 0 10px 24px rgba(37, 99, 235, 0.08);
	transform: translateY(-1px);
}

.study-course-card,
.study-module-card,
.study-content-block {
	padding: 1rem;
}

.study-concept-card {
	padding: 1rem;
}

.study-icon {
	display: grid;
	width: 2.5rem;
	height: 2.5rem;
	flex-shrink: 0;
	place-items: center;
	border-radius: 0.625rem;
	background: #dbeafe;
	color: #1d4ed8;
}

.study-badge {
	display: inline-flex;
	align-items: center;
	border-radius: 999px;
	background: #eff6ff;
	padding: 0.25rem 0.625rem;
	font-size: 0.75rem;
	font-weight: 600;
	color: #1d4ed8;
}

.study-empty {
	border: 1px dashed #d1d5db;
	border-radius: 0.75rem;
	background: #f9fafb;
	padding: 2rem;
	text-align: center;
}

.study-mini-empty {
	border-radius: 0.5rem;
	background: #f9fafb;
	padding: 0.75rem;
	font-size: 0.875rem;
	line-height: 1.5;
	color: #6b7280;
}

.study-loader {
	border: 1px solid #bfdbfe;
	border-radius: 0.75rem;
	background: #eff6ff;
	padding: 1rem;
	font-size: 0.875rem;
	font-weight: 500;
	color: #1d4ed8;
}

.study-step,
.study-room-step {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
	border: 1px solid #e5e7eb;
	border-radius: 0.75rem;
	background: #ffffff;
	padding: 0.875rem;
	color: #6b7280;
}

.study-step span,
.study-room-step span,
.study-number {
	display: grid;
	width: 1.625rem;
	height: 1.625rem;
	flex-shrink: 0;
	place-items: center;
	border-radius: 999px;
	background: #f3f4f6;
	font-size: 0.75rem;
	font-weight: 700;
	color: #4b5563;
}

.study-step p,
.study-room-step p {
	margin-top: 0.15rem;
	font-size: 0.75rem;
	line-height: 1.35;
}

.study-step.is-active,
.study-room-step.is-active {
	border-color: #bfdbfe;
	background: #eff6ff;
	color: #1f2937;
}

.study-step.is-done {
	border-color: #bbf7d0;
	background: #f0fdf4;
	color: #166534;
}

.study-step.is-active span,
.study-room-step.is-active span {
	background: #2563eb;
	color: #ffffff;
}

.study-step.is-done span {
	background: #16a34a;
	color: #ffffff;
}

.study-lesson-row {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 0.75rem;
	border: 1px solid #e5e7eb;
	border-radius: 0.625rem;
	background: #ffffff;
	padding: 0.875rem;
	text-align: left;
	transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.study-lesson-row:hover {
	border-color: #93c5fd;
	box-shadow: 0 8px 18px rgba(15, 23, 42, 0.06);
}

.study-lesson-check {
	display: grid;
	width: 1.75rem;
	height: 1.75rem;
	flex-shrink: 0;
	place-items: center;
	border-radius: 999px;
	background: #f3f4f6;
	color: #9ca3af;
}

.study-lesson-check.is-done {
	background: #dcfce7;
	color: #16a34a;
}

.study-input {
	width: 100%;
	border-radius: 0.375rem;
	border: 1px solid #d1d5db;
	background: #ffffff;
	padding: 0.5rem 0.75rem;
	font-size: 0.875rem;
	outline: none;
}

.study-textarea {
	width: 100%;
	resize: vertical;
	border-radius: 0.375rem;
	border: 1px solid #d1d5db;
	background: #ffffff;
	padding: 0.5rem 0.75rem;
	font-size: 0.875rem;
	line-height: 1.55;
	outline: none;
}

.study-input:focus,
.study-textarea:focus {
	border-color: #3b82f6;
	box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
}

.study-markdown :deep(h1),
.study-markdown :deep(h2),
.study-markdown :deep(h3) {
	margin: 0.85rem 0 0.45rem;
	font-weight: 650;
	color: #111827;
}

.study-markdown :deep(p),
.study-markdown :deep(li) {
	font-size: 0.925rem;
	line-height: 1.7;
	color: #374151;
}

.study-markdown :deep(ul),
.study-markdown :deep(ol) {
	margin: 0.5rem 0 0.75rem 1.25rem;
}

@media (max-width: 768px) {
	.study-section-heading {
		flex-direction: column;
	}

	.study-lesson-row {
		flex-direction: column;
	}
}
</style>

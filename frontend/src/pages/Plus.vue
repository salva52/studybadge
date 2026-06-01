<template>
	<div class="plus-page min-h-screen pb-16">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b px-4 py-3 shadow-sm plus-header"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
		</header>

		<!-- Loading State -->
		<div v-if="billing.data === undefined" class="flex justify-center items-center py-24">
			<div class="flex flex-col items-center gap-4">
				<div class="relative">
					<div class="size-16 rounded-full plus-loading-ring animate-spin"></div>
					<Crown class="size-6 text-amber-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
				</div>
				<span class="text-sm font-medium plus-text-muted animate-pulse">{{ __('Cargando tu plan...') }}</span>
			</div>
		</div>

		<div v-else>

			<!-- ═══════════════════════════════════════════
			     ESTADO 2: PLAN ACTIVO
			     ═══════════════════════════════════════════ -->
			<div v-if="billing.data?.active">

				<!-- Hero Activo -->
				<div class="plus-hero-active relative overflow-hidden">
					<div class="plus-hero-glow-1"></div>
					<div class="plus-hero-glow-2"></div>
					<div class="plus-hero-grid"></div>
					<div class="mx-auto max-w-5xl relative z-10 px-6 py-14 sm:py-20">
						<div class="flex flex-col sm:flex-row items-center sm:items-start gap-8">
							<div class="plus-crown-badge shrink-0">
								<Crown class="size-10 sm:size-12 text-amber-400 drop-shadow-lg" />
							</div>
							<div class="text-center sm:text-left">
								<div class="inline-flex items-center gap-2 rounded-full bg-green-500/20 border border-green-400/30 px-4 py-1.5 text-xs font-bold text-green-300 uppercase tracking-wider mb-4 backdrop-blur-sm">
									<span class="relative flex h-2 w-2">
										<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
										<span class="relative inline-flex rounded-full h-2 w-2 bg-green-400"></span>
									</span>
									{{ __('Plan activo') }}
								</div>
								<h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
									{{ __('Tu membresía') }}
									<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-yellow-200 to-amber-400">Plus</span>
								</h1>
								<p class="mt-4 text-base sm:text-lg text-blue-100/80 max-w-xl font-medium">
									{{ __('Gestiona tu plan, revisa tus beneficios y descarga tus recibos.') }}
								</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Contenido Activo -->
				<div class="mx-auto max-w-5xl px-5 py-10">
					<div class="grid gap-8 lg:grid-cols-3 items-start">

						<!-- Main: Beneficios + Recibos -->
						<div class="lg:col-span-2 space-y-8">

							<!-- Beneficios Activos -->
							<div class="plus-card p-6 sm:p-8">
								<h2 class="text-xl font-bold plus-text-primary mb-6 flex items-center gap-3">
									<div class="plus-icon-badge bg-blue-500/10 text-blue-500">
										<Sparkles class="size-5" />
									</div>
									{{ __('Tus beneficios activos') }}
								</h2>
								<div class="grid gap-3 sm:grid-cols-2">
									<div
										v-for="benefit in benefits"
										:key="benefit.label"
										class="plus-benefit-item group"
									>
										<div class="plus-benefit-icon">
											<component :is="benefit.icon" class="size-5" />
										</div>
										<div class="min-w-0">
											<div class="font-bold text-sm plus-text-primary">{{ benefit.label }}</div>
											<div class="mt-0.5 text-xs plus-text-muted leading-relaxed">{{ benefit.description }}</div>
										</div>
										<CheckCircle2 class="size-4 text-green-500 shrink-0 ml-auto opacity-60" />
									</div>
								</div>
							</div>

							<!-- Historial de Pagos -->
							<div class="plus-card p-6 sm:p-8">
								<div class="flex items-center justify-between gap-4 border-b plus-border pb-5 mb-5">
									<h2 class="text-xl font-bold plus-text-primary flex items-center gap-3">
										<div class="plus-icon-badge bg-gray-500/10 text-gray-500">
											<Download class="size-5" />
										</div>
										{{ __('Historial de pagos') }}
									</h2>
									<button
										class="plus-btn-ghost text-xs"
										@click="billing.reload()"
									>
										<RefreshCcw class="size-3.5" :class="{'animate-spin': billing.loading}" />
										{{ __('Actualizar') }}
									</button>
								</div>

								<!-- Receipts List -->
								<div v-if="receipts.length" class="space-y-3">
									<div
										v-for="receipt in receipts"
										:key="receipt.name"
										class="plus-receipt-row"
									>
										<div class="min-w-0 flex-1">
											<div class="font-bold text-sm plus-text-primary truncate">
												{{ receipt.receipt_number || receipt.name }}
											</div>
											<div class="flex items-center gap-2 mt-1 text-xs plus-text-muted">
												<CalendarDays class="size-3.5 shrink-0" />
												{{ formatDate(receipt.paid_at || receipt.date_created) }}
												<span class="plus-status-pill" :class="receipt.status === 'paid' ? 'plus-status-paid' : 'plus-status-default'">
													{{ receipt.status }}
												</span>
											</div>
										</div>
										<div class="flex items-center gap-4 shrink-0">
											<span class="font-bold text-sm plus-text-primary">{{ formatMoney(receipt.amount, receipt.currency) }}</span>
											<button class="plus-btn-outline text-xs" @click="downloadReceipt(receipt)">
												<Download class="size-3.5" /> PDF
											</button>
										</div>
									</div>
								</div>

								<!-- Empty Receipts -->
								<div v-else class="plus-empty-state py-12">
									<div class="plus-empty-icon">
										<Download class="size-8" />
									</div>
									<h3 class="text-base font-bold plus-text-primary mt-4">{{ __('Todavía no hay recibos') }}</h3>
									<p class="text-sm plus-text-muted mt-1 max-w-xs">{{ __('Cuando Mercado Pago confirme un cobro, aparecerá aquí tu comprobante.') }}</p>
								</div>
							</div>
						</div>

						<!-- Sidebar -->
						<div class="space-y-6">

							<!-- Estado del Plan -->
							<div class="plus-card relative overflow-hidden">
								<div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 via-blue-400 to-cyan-400"></div>
								<div class="p-6">
									<div class="flex justify-between items-start mb-5">
										<div>
											<h3 class="font-bold text-lg plus-text-primary">StudyBadge Plus</h3>
											<div class="text-sm plus-text-muted mt-0.5">{{ formattedPrice }} / {{ __('mes') }}</div>
										</div>
										<Badge theme="green" class="font-bold text-xs">
											<CheckCircle2 class="size-3 mr-1" /> {{ __('Activo') }}
										</Badge>
									</div>

									<div class="space-y-3">
										<div class="plus-info-row">
											<CalendarDays class="size-4 plus-text-muted shrink-0" />
											<div class="min-w-0">
												<div class="text-[10px] plus-text-muted font-bold uppercase tracking-wider">{{ __('Próximo cobro') }}</div>
												<div class="text-sm font-semibold plus-text-primary mt-0.5">{{ formatDate(subscription.next_payment_date) }}</div>
											</div>
										</div>
										<div class="plus-info-row">
											<CreditCard class="size-4 plus-text-muted shrink-0" />
											<div class="min-w-0">
												<div class="text-[10px] plus-text-muted font-bold uppercase tracking-wider">{{ __('Método de pago') }}</div>
												<div class="text-sm font-semibold plus-text-primary mt-0.5 truncate">{{ paymentMethodLabel }}</div>
											</div>
										</div>
									</div>

									<!-- Cancellation Warning -->
									<div v-if="subscription.cancel_at_period_end" class="mt-5 rounded-xl bg-amber-500/10 border border-amber-500/20 p-4 text-sm">
										<span class="font-bold text-amber-600 dark:text-amber-400 block mb-1">{{ __('Cancelación programada') }}</span>
										<span class="text-amber-700 dark:text-amber-300 text-xs">
											{{ __('Tu suscripción se cancelará el {0}.', [formatDate(subscription.cancel_scheduled_for)]) }}
										</span>
									</div>

									<!-- Action Buttons -->
									<div class="mt-6 space-y-2.5">
										<button
											v-if="!subscription.cancel_at_period_end"
											class="plus-btn-primary w-full"
											@click="showPaymentMethodForm"
										>
											<CreditCard class="size-4" /> {{ __('Gestionar suscripción') }}
										</button>
										<button
											v-if="!subscription.cancel_at_period_end"
											class="plus-btn-danger-ghost w-full"
											:disabled="cancelResource.loading"
											@click="requestCancellation"
										>
											{{ __('Cancelar plan') }}
										</button>
										<button
											v-if="subscription.cancel_at_period_end"
											class="plus-btn-primary w-full"
											:disabled="reactivateResource.loading"
											@click="reactivateSubscription"
										>
											<RefreshCcw class="size-4" /> {{ __('Reactivar mi Plus') }}
										</button>
									</div>
								</div>
							</div>

							<!-- Soporte -->
							<div class="plus-card-support p-6 text-center">
								<LifeBuoy class="size-7 mx-auto mb-3 opacity-70" />
								<h3 class="font-bold text-sm plus-text-primary">{{ __('¿Necesitas ayuda?') }}</h3>
								<p class="mt-1.5 text-xs plus-text-muted mb-4 leading-relaxed">{{ __('Nuestro equipo está listo para ayudarte.') }}</p>
								<a
									class="plus-btn-ghost text-xs inline-flex"
									:href="`mailto:${billing.data?.support_email || 'soporte@studybadge.com'}`"
								>
									<Mail class="size-3.5" /> {{ __('Contactar Soporte') }}
								</a>
							</div>
						</div>
					</div>
				</div>

				<!-- Card Form Modal -->
				<Teleport to="body">
					<Transition name="plus-modal">
						<div v-if="cardFormVisible" class="fixed inset-0 z-[60] flex items-center justify-center p-4" @click.self="hidePaymentMethodForm">
							<div class="fixed inset-0 bg-black/60 backdrop-blur-sm"></div>
							<div class="plus-modal-content relative z-10 w-full max-w-md max-h-[90vh] flex flex-col">
								<div class="flex justify-between items-center px-6 py-4 border-b plus-border">
									<div class="flex items-center gap-3">
										<ShieldCheck class="size-5 text-green-500" />
										<span class="font-bold plus-text-primary">{{ __('Actualizar método de pago') }}</span>
									</div>
									<button @click="hidePaymentMethodForm" class="plus-text-muted hover:plus-text-primary transition-colors p-1 rounded-lg">
										<XCircle class="size-5" />
									</button>
								</div>
								<div class="p-6 overflow-y-auto">
									<div v-if="cardFormLoading" class="flex justify-center py-10 text-sm plus-text-muted animate-pulse">
										{{ __('Estableciendo conexión segura...') }}
									</div>
									<div id="studybadge-mp-card-form"></div>
								</div>
							</div>
						</div>
					</Transition>
				</Teleport>
			</div>

			<!-- ═══════════════════════════════════════════
			     ESTADO 1: SIN PLAN — PÁGINA DE VENTA
			     ═══════════════════════════════════════════ -->
			<div v-else class="bg-[#f5f7fb]">
				<!-- Hero de Venta -->
				<section class="relative bg-[#08204e] text-white pt-12 pb-20 overflow-hidden">
					<div class="absolute top-0 right-0 w-3/4 h-full bg-gradient-to-l from-blue-600/20 to-transparent pointer-events-none"></div>
					<div class="absolute -top-24 -left-24 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none"></div>
					<div class="absolute bottom-0 right-0 w-full h-24 bg-gradient-to-t from-[#f5f7fb] to-transparent pointer-events-none z-10"></div>
					
					<div class="max-w-7xl mx-auto px-6 relative z-20">
						<div class="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
							<!-- Columna Izquierda: Copy -->
							<div>
								<div class="inline-block px-3 py-1 mb-6 rounded-full bg-white/10 border border-white/20 text-amber-400 text-xs font-black uppercase tracking-widest backdrop-blur-sm">
									STUDYBADGE PLUS
								</div>
								<h1 class="text-4xl md:text-5xl lg:text-6xl font-black leading-tight mb-6">
									{{ __('Desbloquea todo el poder de StudyBadge') }}
								</h1>
								<p class="text-lg md:text-xl text-blue-100/90 leading-relaxed mb-8 max-w-xl">
									{{ __('Certificados ilimitados, Tutor IA sin límites, prompts premium, simulaciones y herramientas inteligentes para estudiar mejor, crear más rápido y avanzar todos los días.') }}
								</p>
								
								<div class="flex flex-col sm:flex-row gap-4 mb-8">
									<button @click="scrollToPricing" class="plus-btn-cta text-lg bg-amber-400 hover:bg-amber-300 text-[#08204e] border-none shadow-amber-500/30">
										{{ __('Desbloquear Plus ahora') }}
									</button>
									<button @click="scrollToBenefits" class="plus-btn-outline border-white/30 text-white hover:bg-white/10 hover:border-white/50 text-base">
										{{ __('Ver beneficios') }} <ArrowDown class="size-4" />
									</button>
								</div>
								
								<div class="flex flex-wrap items-center gap-4 text-sm text-blue-200 font-medium">
									<span class="flex items-center gap-1.5"><Sparkles class="size-4 text-amber-400"/> {{ __('Acceso inmediato') }}</span>
									<span class="flex items-center gap-1.5"><RefreshCcw class="size-4 text-amber-400"/> {{ __('Cancela cuando quieras') }}</span>
									<span class="flex items-center gap-1.5"><ShieldCheck class="size-4 text-green-400"/> {{ __('Pago seguro con Mercado Pago') }}</span>
								</div>
							</div>
							
							<!-- Columna Derecha: Pricing Card -->
							<div id="pricing-card" class="w-full max-w-md mx-auto lg:ml-auto mt-6 lg:mt-0">
								<div class="bg-white rounded-[2rem] overflow-hidden shadow-2xl border border-gray-100 text-gray-900 relative">
									<div class="absolute top-0 inset-x-0 h-1.5 bg-gradient-to-r from-amber-400 to-amber-500"></div>
									<div class="p-8 pb-6">
										<div class="text-center mb-6">
											<span class="inline-block px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-black uppercase tracking-widest mb-4">
												{{ __('Membresía Plus') }}
											</span>
											<div class="flex items-end justify-center gap-1 mb-2">
												<span class="text-5xl font-black tracking-tight">{{ formattedPrice }}</span>
												<span class="text-gray-500 font-medium pb-1">/ {{ __('mes') }}</span>
											</div>
											<p class="text-sm font-bold text-gray-500">{{ __('Menos de S/1 al día') }}</p>
										</div>
										
										<div class="space-y-4 mb-8 bg-blue-50/50 p-5 rounded-2xl border border-blue-100/50">
											<div class="flex items-start gap-3">
												<CheckCircle2 class="size-5 text-[#0b82e6] shrink-0" />
												<span class="text-sm font-semibold text-gray-700">{{ __('Certificados ilimitados') }}</span>
											</div>
											<div class="flex items-start gap-3">
												<CheckCircle2 class="size-5 text-[#0b82e6] shrink-0" />
												<span class="text-sm font-semibold text-gray-700">{{ __('Tutor IA ilimitado') }}</span>
											</div>
											<div class="flex items-start gap-3">
												<CheckCircle2 class="size-5 text-[#0b82e6] shrink-0" />
												<span class="text-sm font-semibold text-gray-700">{{ __('Prompts premium') }}</span>
											</div>
											<div class="flex items-start gap-3">
												<CheckCircle2 class="size-5 text-[#0b82e6] shrink-0" />
												<span class="text-sm font-semibold text-gray-700">{{ __('Calendario inteligente') }}</span>
											</div>
										</div>
										
										<button
											class="w-full py-4 rounded-xl font-bold text-white text-[17px] bg-[#1473e6] hover:bg-[#0f5ebd] transition-all shadow-lg shadow-blue-500/30 flex justify-center items-center gap-2 mb-4"
											:disabled="activating"
											@click="subscription?.init_point ? openExistingCheckout() : activatePlus()"
										>
											<span v-if="activating" class="animate-spin">⏳</span>
											<Crown v-else class="size-5" />
											{{ subscription?.init_point ? __('Continuar pago pendiente') : __('Desbloquear StudyBadge Plus') }}
										</button>
										
										<div class="flex items-center justify-center gap-2 text-xs font-semibold text-gray-500">
											<ShieldCheck class="size-4 text-green-500" />
											{{ __('Pago 100% seguro con Mercado Pago') }}
										</div>
									</div>
									<div class="bg-gray-50 p-4 text-center border-t border-gray-100">
										<p class="text-sm font-bold text-gray-600">{{ __('Próximamente: Plan anual con descuento especial') }}</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>
				
				<!-- Prueba Social -->
				<section class="border-y border-gray-200 bg-white py-6">
					<div class="max-w-7xl mx-auto px-6">
						<div class="flex flex-wrap justify-center md:justify-between items-center gap-6 text-center">
							<div class="flex items-center gap-2">
								<div class="p-2 bg-blue-50 rounded-lg"><Users class="size-5 text-blue-600" /></div>
								<span class="font-bold text-gray-700">+1,000 estudiantes</span>
							</div>
							<div class="flex items-center gap-2">
								<div class="p-2 bg-amber-50 rounded-lg"><FileText class="size-5 text-amber-600" /></div>
								<span class="font-bold text-gray-700">+100 prompts listos</span>
							</div>
							<div class="flex items-center gap-2">
								<div class="p-2 bg-emerald-50 rounded-lg"><PlayCircle class="size-5 text-emerald-600" /></div>
								<span class="font-bold text-gray-700">+30 cursos y recursos</span>
							</div>
							<div class="flex items-center gap-2">
								<div class="p-2 bg-indigo-50 rounded-lg"><Clock class="size-5 text-indigo-600" /></div>
								<span class="font-bold text-gray-700">Disponible 24/7</span>
							</div>
						</div>
					</div>
				</section>

				<!-- Beneficios (Cards) -->
				<section id="benefits-section" class="py-20 max-w-7xl mx-auto px-6">
					<div class="text-center mb-16">
						<h2 class="text-3xl md:text-4xl font-black text-[#08204e] mb-4">{{ __('Herramientas creadas para tu éxito') }}</h2>
						<p class="text-lg text-gray-600 max-w-2xl mx-auto">{{ __('Todo lo que necesitas para estudiar, crear y trabajar en un solo lugar.') }}</p>
					</div>
					
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
						<div v-for="benefit in benefits" :key="benefit.label" class="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
							<div class="w-14 h-14 rounded-xl bg-blue-50 text-[#0b82e6] flex items-center justify-center mb-6 transition-transform hover:scale-110">
								<component :is="benefit.icon" class="size-7" />
							</div>
							<h3 class="text-xl font-bold text-gray-900 mb-3">{{ benefit.label }}</h3>
							<p class="text-gray-600 leading-relaxed">{{ benefit.description }}</p>
						</div>
					</div>
				</section>

				<!-- Lo que desbloqueas hoy -->
				<section class="bg-white py-20 border-t border-gray-100">
					<div class="max-w-7xl mx-auto px-6">
						<div class="grid md:grid-cols-2 gap-12 lg:gap-20 items-center">
							<div>
								<h2 class="text-3xl md:text-4xl font-black text-[#08204e] mb-10">{{ __('Resultados desde el primer día') }}</h2>
								<div class="space-y-8">
									<div class="flex gap-4">
										<div class="mt-1"><div class="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600"><Zap class="size-5" /></div></div>
										<div>
											<h4 class="text-lg font-bold text-gray-900 mb-1">{{ __('Aprende más rápido') }}</h4>
											<p class="text-gray-600">{{ __('Convierte una clase larga en un resumen detallado y un quiz práctico en minutos.') }}</p>
										</div>
									</div>
									<div class="flex gap-4">
										<div class="mt-1"><div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600"><Briefcase class="size-5" /></div></div>
										<div>
											<h4 class="text-lg font-bold text-gray-900 mb-1">{{ __('Crea mejores trabajos') }}</h4>
											<p class="text-gray-600">{{ __('Prepara exposiciones, presentaciones y entrevistas con simulaciones realistas.') }}</p>
										</div>
									</div>
									<div class="flex gap-4">
										<div class="mt-1"><div class="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center text-amber-600"><Clock class="size-5" /></div></div>
										<div>
											<h4 class="text-lg font-bold text-gray-900 mb-1">{{ __('Ahorra horas con prompts') }}</h4>
											<p class="text-gray-600">{{ __('Genera contenido, planes de marketing y tareas sin empezar desde cero.') }}</p>
										</div>
									</div>
									<div class="flex gap-4">
										<div class="mt-1"><div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-600"><Bot class="size-5" /></div></div>
										<div>
											<h4 class="text-lg font-bold text-gray-900 mb-1">{{ __('Practica con IA sin límites') }}</h4>
											<p class="text-gray-600">{{ __('Recibe retroalimentación inmediata en tus respuestas y mejora tus habilidades.') }}</p>
										</div>
									</div>
								</div>
							</div>
							<div class="bg-gray-50 rounded-[2rem] p-6 lg:p-8 border border-gray-200 shadow-inner relative overflow-hidden">
								<div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNlNWU3ZWIiLz48L3N2Zz4=')] opacity-50"></div>
								<div class="relative z-10 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
									<div class="flex items-center gap-3 mb-5">
										<div class="w-10 h-10 bg-[#0b82e6] rounded-full flex items-center justify-center text-white"><Bot class="size-6" /></div>
										<div>
											<div class="font-bold text-sm text-gray-900">Tutor IA StudyBadge</div>
											<div class="text-xs text-green-500 font-semibold">En línea</div>
										</div>
									</div>
									<p class="text-sm text-gray-700 mb-4 bg-gray-50 p-4 rounded-xl rounded-tl-none border border-gray-100 leading-relaxed">
										¡Hola! He analizado tu documento sobre <b>Estrategias de Marketing</b>. Aquí tienes el resumen y las 5 preguntas clave para tu examen de mañana. ¿Empezamos el quiz interactivo?
									</p>
									<div class="text-right">
										<p class="inline-block text-sm text-white bg-[#0b82e6] p-4 rounded-xl rounded-tr-none shadow-sm shadow-blue-500/20">
											¡Sí, por favor! Empecemos con preguntas difíciles.
										</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>

				<!-- Gratis vs Plus -->
				<section class="py-20 max-w-5xl mx-auto px-6">
					<div class="text-center mb-12">
						<h2 class="text-3xl font-black text-[#08204e] mb-4">{{ __('Compara los planes') }}</h2>
					</div>
					
					<div class="bg-white rounded-3xl overflow-hidden shadow-xl border border-gray-200">
						<div class="grid grid-cols-2 bg-gray-50">
							<div class="p-6 text-center border-r border-gray-200">
								<h3 class="text-xl font-bold text-gray-500 mb-2">{{ __('Plan Gratis') }}</h3>
								<p class="text-sm text-gray-400">{{ __('Ideal para empezar') }}</p>
							</div>
							<div class="p-6 text-center bg-blue-50 border-b-2 border-[#0b82e6] relative">
								<div class="absolute -top-3 inset-x-0 flex justify-center"><span class="bg-amber-400 text-amber-900 text-[10px] font-black uppercase tracking-wider px-3 py-1 rounded-full shadow-sm">{{ __('Recomendado') }}</span></div>
								<h3 class="text-xl font-black text-[#08204e] mb-2">StudyBadge Plus</h3>
								<p class="text-sm text-[#0b82e6] font-medium">{{ __('Para lograr más') }}</p>
							</div>
						</div>
						
						<div class="divide-y divide-gray-100">
							<div class="grid grid-cols-2 hover:bg-gray-50 transition-colors">
								<div class="p-5 border-r border-gray-200 flex flex-col items-center justify-center text-center gap-2">
									<span class="text-sm text-gray-600">{{ __('Acceso limitado a cursos') }}</span>
								</div>
								<div class="p-5 flex flex-col items-center text-center gap-2 bg-blue-50/30">
									<CheckCircle2 class="size-5 text-[#0b82e6]" />
									<span class="text-sm font-bold text-gray-900">{{ __('Cursos y recursos premium') }}</span>
								</div>
							</div>
							<div class="grid grid-cols-2 hover:bg-gray-50 transition-colors">
								<div class="p-5 border-r border-gray-200 flex flex-col items-center justify-center text-center gap-2">
									<span class="text-sm text-gray-600">{{ __('Certificados limitados') }}</span>
								</div>
								<div class="p-5 flex flex-col items-center text-center gap-2 bg-blue-50/30">
									<CheckCircle2 class="size-5 text-[#0b82e6]" />
									<span class="text-sm font-bold text-gray-900">{{ __('Certificados ilimitados') }}</span>
								</div>
							</div>
							<div class="grid grid-cols-2 hover:bg-gray-50 transition-colors">
								<div class="p-5 border-r border-gray-200 flex flex-col items-center justify-center text-center gap-2">
									<span class="text-sm text-gray-600">{{ __('Prompts básicos') }}</span>
								</div>
								<div class="p-5 flex flex-col items-center text-center gap-2 bg-blue-50/30">
									<CheckCircle2 class="size-5 text-[#0b82e6]" />
									<span class="text-sm font-bold text-gray-900">{{ __('Prompts premium ilimitados') }}</span>
								</div>
							</div>
							<div class="grid grid-cols-2 hover:bg-gray-50 transition-colors">
								<div class="p-5 border-r border-gray-200 flex flex-col items-center justify-center text-center gap-2">
									<span class="text-sm text-gray-600">{{ __('Tutor IA limitado') }}</span>
								</div>
								<div class="p-5 flex flex-col items-center text-center gap-2 bg-blue-50/30">
									<CheckCircle2 class="size-5 text-[#0b82e6]" />
									<span class="text-sm font-bold text-gray-900">{{ __('Tutor IA ilimitado') }}</span>
								</div>
							</div>
							<div class="grid grid-cols-2 hover:bg-gray-50 transition-colors">
								<div class="p-5 border-r border-gray-200 flex flex-col items-center justify-center text-center gap-2">
									<X class="size-5 text-gray-300" />
									<span class="text-sm text-gray-500">{{ __('Sin simulaciones premium') }}</span>
								</div>
								<div class="p-5 flex flex-col items-center text-center gap-2 bg-blue-50/30">
									<CheckCircle2 class="size-5 text-[#0b82e6]" />
									<span class="text-sm font-bold text-gray-900">{{ __('Simulaciones con IA completas') }}</span>
								</div>
							</div>
							<div class="grid grid-cols-2 hover:bg-gray-50 transition-colors">
								<div class="p-5 border-r border-gray-200 flex flex-col items-center justify-center text-center gap-2">
									<X class="size-5 text-gray-300" />
									<span class="text-sm text-gray-500">{{ __('Sin calendario inteligente') }}</span>
								</div>
								<div class="p-5 flex flex-col items-center text-center gap-2 bg-blue-50/30">
									<CheckCircle2 class="size-5 text-[#0b82e6]" />
									<span class="text-sm font-bold text-gray-900">{{ __('Calendario y seguimiento total') }}</span>
								</div>
							</div>
						</div>
					</div>
				</section>

				<!-- FAQ -->
				<section class="py-20 bg-white border-t border-gray-100">
					<div class="max-w-4xl mx-auto px-6">
						<div class="text-center mb-12">
							<h2 class="text-3xl font-black text-[#08204e] mb-4">{{ __('Preguntas frecuentes') }}</h2>
						</div>
						
						<div class="grid gap-6 md:grid-cols-2">
							<div v-for="(faq, index) in faqs" :key="index" class="bg-gray-50 rounded-2xl p-6 border border-gray-100">
								<h3 class="text-base font-bold text-gray-900 mb-2">{{ faq.q }}</h3>
								<p class="text-sm text-gray-600 leading-relaxed">{{ faq.a }}</p>
							</div>
						</div>
					</div>
				</section>

				<!-- Final CTA -->
				<section class="py-24 bg-[#08204e] text-center px-6 relative overflow-hidden">
					<div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNmZmYiLz48L3N2Zz4=')] opacity-[0.03]"></div>
					<div class="relative z-10 max-w-2xl mx-auto">
						<h2 class="text-4xl font-black text-white mb-6">{{ __('Empieza hoy con StudyBadge Plus') }}</h2>
						<p class="text-xl text-blue-100 mb-10">{{ __('Desbloquea herramientas inteligentes para estudiar, crear y avanzar más rápido.') }}</p>
						
						<button
							class="plus-btn-cta text-lg bg-amber-400 hover:bg-amber-300 text-[#08204e] border-none shadow-amber-500/30 px-10 py-5 w-full sm:w-auto"
							:disabled="activating"
							@click="subscription?.init_point ? openExistingCheckout() : activatePlus()"
						>
							<span v-if="activating" class="animate-spin mr-2">⏳</span>
							{{ subscription?.init_point ? __('Continuar pago pendiente') : __('Desbloquear Plus por ') + formattedPrice }}
						</button>
						
						<div class="mt-6 flex flex-wrap justify-center gap-4 text-sm text-blue-200 font-medium">
							<span class="flex items-center gap-1.5"><Sparkles class="size-4" /> {{ __('Acceso inmediato') }}</span> 
							<span class="flex items-center gap-1.5"><RefreshCcw class="size-4" /> {{ __('Cancela cuando quieras') }}</span> 
							<span class="flex items-center gap-1.5"><ShieldCheck class="size-4" /> {{ __('Pago seguro') }}</span>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject, nextTick, onBeforeUnmount, ref } from 'vue'
import { Badge, Breadcrumbs, Button, createResource, toast, usePageMeta } from 'frappe-ui'
import {
	Award,
	Bot,
	CalendarDays,
	CheckCircle2,
	CreditCard,
	Crown,
	Download,
	FileText,
	LifeBuoy,
	RefreshCcw,
	Sparkles,
	XCircle,
	ShieldCheck,
	Mail,
	Info,
	Video,
	ArrowDown,
	Users,
	PlayCircle,
	Zap,
	Briefcase,
	X,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const activating = ref(false)
const cardFormVisible = ref(false)
const cardFormLoading = ref(false)
const cardController = ref(null)
const mercadoPagoLoader = ref(null)
const user = inject('$user')

const benefits = [
	{
		icon: Award,
		label: __('Certificados ilimitados'),
		description: __('Obtén certificados por cada curso completado y desbloquea todos los certificados premium.'),
	},
	{
		icon: Bot,
		label: __('Tutor IA ilimitado'),
		description: __('Haz preguntas, resuelve dudas, practica temas y recibe ayuda personalizada sin límites.'),
	},
	{
		icon: FileText,
		label: __('Biblioteca de prompts premium'),
		description: __('Usa prompts listos para marketing, estudio, negocios, productividad e imágenes IA.'),
	},
	{
		icon: Video,
		label: __('Simulaciones con IA'),
		description: __('Practica entrevistas, ventas, inglés, exposiciones y casos reales con retroalimentación.'),
	},
	{
		icon: CalendarDays,
		label: __('Calendario inteligente'),
		description: __('Organiza tus cursos, tareas y objetivos con seguimiento automático.'),
	},
	{
		icon: Zap,
		label: __('Herramientas de estudio IA'),
		description: __('Resume, practica, genera quizzes y convierte temas difíciles en ejercicios simples.'),
	},
]

const faqs = [
	{ q: __('¿Puedo cancelar cuando quiera?'), a: __('Sí, no hay contratos ni compromisos a largo plazo. Puedes cancelar tu suscripción en cualquier momento desde tu panel de configuración.') },
	{ q: __('¿Qué incluye StudyBadge Plus?'), a: __('Acceso a certificados ilimitados, herramientas de IA sin restricciones (tutor, simulaciones, herramientas de estudio), calendario inteligente y toda la biblioteca de prompts premium.') },
	{ q: __('¿Los certificados son verdaderamente ilimitados?'), a: __('Sí, una vez eres Plus puedes generar certificados de todos los cursos que hayas aprobado sin costos adicionales por emisión.') },
	{ q: __('¿El pago es seguro?'), a: __('Totalmente. Utilizamos Mercado Pago como pasarela, garantizando seguridad y protección en tu transacción.') },
	{ q: __('¿Puedo usarlo para estudiar y para negocios?'), a: __('¡Claro! Las herramientas de IA y los prompts están diseñados tanto para estudiantes como para emprendedores y profesionales.') },
	{ q: __('¿Qué pasa después de pagar?'), a: __('Tu cuenta se actualizará instantáneamente y tendrás acceso a todas las funciones premium y certificados de inmediato.') }
]

function scrollToPricing() {
	document.getElementById('pricing-card')?.scrollIntoView({ behavior: 'smooth' })
}

function scrollToBenefits() {
	document.getElementById('benefits-section')?.scrollIntoView({ behavior: 'smooth' })
}


const trustPoints = [
	{ icon: ShieldCheck, label: __('Pago seguro'), sub: __('Con Mercado Pago') },
	{ icon: RefreshCcw, label: __('Cancela cuando quieras'), sub: __('Sin contratos') },
	{ icon: Sparkles, label: __('Activación inmediata'), sub: __('Disfruta al instante') },
	{ icon: Download, label: __('Recibos en PDF'), sub: __('Comprobantes claros') },
]

const billing = createResource({
	url: 'lms.lms.subscriptions.get_plus_billing',
	auto: true,
	onSuccess(data) {
		if (data.active) {
			user.reload?.()
		}
	},
})

const checkout = createResource({
	url: 'lms.lms.subscriptions.create_plus_checkout',
})

const cancelResource = createResource({
	url: 'lms.lms.subscriptions.request_plus_cancellation',
})

const reactivateResource = createResource({
	url: 'lms.lms.subscriptions.reactivate_plus_subscription',
})

const paymentMethodResource = createResource({
	url: 'lms.lms.subscriptions.update_plus_payment_method',
})

const subscription = computed(() => billing.data?.subscription)
const receipts = computed(() => billing.data?.receipts || [])

const formattedPrice = computed(() => {
	const plan = billing.data?.plan
	if (!plan) return 'S/ 29.90'
	if (plan.currency === 'PEN') return `S/ ${Number(plan.amount).toFixed(2)}`
	return `${plan.currency} ${Number(plan.amount).toFixed(2)}`
})

const paymentMethodLabel = computed(() => {
	const method = subscription.value?.payment_method
	if (!method?.id && !method?.card_last_four) {
		return __('Mercado Pago')
	}
	if (method.card_last_four) {
		return `${method.card_brand || method.name || __('Tarjeta')} **** ${method.card_last_four}`
	}
	return method.name || method.id
})

function activatePlus() {
	activating.value = true
	checkout.submit(
		{},
		{
			onSuccess(url) {
				window.location.href = url
			},
			onError(err) {
				activating.value = false
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

function openExistingCheckout() {
	window.location.href = subscription.value.init_point
}

function requestCancellation() {
	if (!window.confirm(__('Tu Plus seguira activo hasta el final del periodo.'))) {
		return
	}
	cancelResource.submit(
		{},
		{
			onSuccess(data) {
				billing.data = data
				toast.success(__('Cancelacion programada.'))
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

function reactivateSubscription() {
	reactivateResource.submit(
		{},
		{
			onSuccess(data) {
				billing.data = data
				toast.success(__('Tu Plus sigue activo.'))
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

async function showPaymentMethodForm() {
	cardFormVisible.value = true
	await nextTick()
	initMercadoPagoCardForm()
}

function hidePaymentMethodForm() {
	cardFormVisible.value = false
	destroyCardForm()
}

function loadMercadoPago() {
	if (window.MercadoPago) {
		return Promise.resolve(window.MercadoPago)
	}
	if (mercadoPagoLoader.value) {
		return mercadoPagoLoader.value
	}
	mercadoPagoLoader.value = new Promise((resolve, reject) => {
		const script = document.createElement('script')
		script.src = 'https://sdk.mercadopago.com/js/v2'
		script.onload = () => resolve(window.MercadoPago)
		script.onerror = reject
		document.body.appendChild(script)
	})
	return mercadoPagoLoader.value
}

async function initMercadoPagoCardForm() {
	if (!billing.data?.public_key) {
		toast.error(__('Falta configurar la public key de Mercado Pago.'))
		return
	}
	cardFormLoading.value = true
	destroyCardForm()
	try {
		const MercadoPago = await loadMercadoPago()
		const mp = new MercadoPago(billing.data.public_key, { locale: 'es-PE' })
		const bricksBuilder = mp.bricks()
		cardController.value = await bricksBuilder.create(
			'cardPayment',
			'studybadge-mp-card-form',
			{
				initialization: {
					amount: Number(billing.data?.plan?.amount || 29),
				},
				customization: {
					paymentMethods: {
						maxInstallments: 1,
					},
				},
				callbacks: {
					onReady() {
						cardFormLoading.value = false
					},
					onError(error) {
						cardFormLoading.value = false
						toast.error(error?.message || __('Mercado Pago no pudo cargar.'))
					},
					onSubmit(cardFormData) {
						return new Promise((resolve, reject) => {
							const cardToken = cardFormData.token || cardFormData.card_token_id
							paymentMethodResource.submit(
								{ card_token_id: cardToken },
								{
									onSuccess(data) {
										billing.data = data
										hidePaymentMethodForm()
										toast.success(__('Metodo de pago actualizado.'))
										resolve()
									},
									onError(err) {
										toast.error(err.messages?.[0] || err)
										reject(err)
									},
								}
							)
						})
					},
				},
			}
		)
	} catch (error) {
		cardFormLoading.value = false
		toast.error(error?.message || __('No se pudo cargar Mercado Pago.'))
	}
}

function destroyCardForm() {
	if (cardController.value?.unmount) {
		cardController.value.unmount()
	}
	cardController.value = null
}

function downloadReceipt(receipt) {
	window.open(receipt.download_url, '_blank', 'noopener')
}

function formatDate(value) {
	if (!value) return __('Pendiente')
	return new Intl.DateTimeFormat('es-PE', {
		dateStyle: 'medium',
		timeStyle: 'short',
	}).format(new Date(value))
}

function formatMoney(amount, currency) {
	if (currency === 'PEN' || !currency) {
		return `S/ ${Number(amount || 0).toFixed(2)}`
	}
	return `${currency} ${Number(amount || 0).toFixed(2)}`
}

function formatSubscriptionStatus(status) {
	if (!status) return ''
	if (status === 'authorized' || status === 'active') return __('Activa')
	if (status === 'pending') return __('Pendiente de pago')
	if (status === 'cancelled') return __('Cancelada')
	return status.charAt(0).toUpperCase() + status.slice(1)
}

onBeforeUnmount(() => {
	destroyCardForm()
})

const breadcrumbs = computed(() => [
	{
		label: __('StudyBadge Plus'),
		route: { name: 'Plus' },
	},
])

usePageMeta(() => {
	return {
		title: __('StudyBadge Plus'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
/* ═══════════════════════════════════════
   PLUS PAGE — LIGHT & DARK TOKENS
   ═══════════════════════════════════════ */

.plus-page {
	background: var(--sb-bg);
	font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.plus-header {
	background: var(--sb-white);
	border-color: rgba(6, 27, 73, 0.06);
}

:root[data-theme="dark"] .plus-header {
	border-color: rgba(255, 255, 255, 0.06);
}

/* Text */
.plus-text-primary { color: #111827; }
.plus-text-muted { color: #6b7280; }
:root[data-theme="dark"] .plus-text-primary { color: #f3f4f6; }
:root[data-theme="dark"] .plus-text-muted { color: #9ca3af; }

/* Border */
.plus-border { border-color: rgba(0, 0, 0, 0.06); }
:root[data-theme="dark"] .plus-border { border-color: rgba(255, 255, 255, 0.08); }

/* ═══════════════════════════════════════
   HERO SECTIONS
   ═══════════════════════════════════════ */

.plus-hero-active,
.plus-hero-sell {
	background: linear-gradient(145deg, #061B49 0%, #0b2f73 40%, #0a2259 100%);
}

.plus-hero-glow-1 {
	position: absolute;
	top: -120px;
	right: -80px;
	width: 400px;
	height: 400px;
	background: radial-gradient(circle, rgba(59, 130, 246, 0.25), transparent 70%);
	border-radius: 50%;
	filter: blur(60px);
}

.plus-hero-glow-2 {
	position: absolute;
	bottom: -100px;
	left: -60px;
	width: 300px;
	height: 300px;
	background: radial-gradient(circle, rgba(245, 179, 1, 0.12), transparent 70%);
	border-radius: 50%;
	filter: blur(50px);
}

.plus-hero-grid {
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
		linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
	background-size: 48px 48px;
}

.plus-crown-badge {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 1.25rem;
	border-radius: 1.25rem;
	background: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.12);
	backdrop-filter: blur(12px);
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

/* ═══════════════════════════════════════
   CARDS
   ═══════════════════════════════════════ */

.plus-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.06);
	border-radius: 20px;
	box-shadow: 0 1px 3px rgba(6, 27, 73, 0.04), 0 4px 12px rgba(6, 27, 73, 0.03);
	transition: all 0.2s ease;
}

:root[data-theme="dark"] .plus-card {
	border-color: rgba(255, 255, 255, 0.06);
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.15);
}

.plus-card-support {
	background: rgba(59, 130, 246, 0.04);
	border: 1px solid rgba(59, 130, 246, 0.1);
	border-radius: 20px;
}

:root[data-theme="dark"] .plus-card-support {
	background: rgba(59, 130, 246, 0.08);
	border-color: rgba(59, 130, 246, 0.15);
}

/* ═══════════════════════════════════════
   PRICING CARD
   ═══════════════════════════════════════ */

.plus-pricing-card {
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.08);
	border-radius: 24px;
	box-shadow: 0 4px 6px rgba(6, 27, 73, 0.04), 0 20px 48px rgba(6, 27, 73, 0.08);
}

:root[data-theme="dark"] .plus-pricing-card {
	border-color: rgba(255, 255, 255, 0.08);
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2), 0 20px 48px rgba(0, 0, 0, 0.3);
}

/* ═══════════════════════════════════════
   BENEFIT ITEMS (Active state)
   ═══════════════════════════════════════ */

.plus-benefit-item {
	display: flex;
	align-items: center;
	gap: 12px;
	padding: 14px 16px;
	border-radius: 14px;
	background: rgba(59, 130, 246, 0.03);
	border: 1px solid rgba(59, 130, 246, 0.06);
	transition: all 0.2s ease;
}

.plus-benefit-item:hover {
	background: rgba(59, 130, 246, 0.06);
	border-color: rgba(59, 130, 246, 0.12);
}

:root[data-theme="dark"] .plus-benefit-item {
	background: rgba(59, 130, 246, 0.05);
	border-color: rgba(59, 130, 246, 0.1);
}

:root[data-theme="dark"] .plus-benefit-item:hover {
	background: rgba(59, 130, 246, 0.1);
	border-color: rgba(59, 130, 246, 0.18);
}

.plus-benefit-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
	background: rgba(59, 130, 246, 0.08);
	color: #3b82f6;
	flex-shrink: 0;
}

:root[data-theme="dark"] .plus-benefit-icon {
	background: rgba(59, 130, 246, 0.15);
	color: #60a5fa;
}

/* BENEFIT CARDS (Sale state) */
.plus-benefit-card {
	display: flex;
	align-items: flex-start;
	gap: 16px;
	padding: 20px;
	border-radius: 18px;
	background: var(--sb-white);
	border: 1px solid rgba(6, 27, 73, 0.06);
	box-shadow: 0 1px 4px rgba(6, 27, 73, 0.04);
	transition: all 0.25s ease;
}

.plus-benefit-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 24px rgba(6, 27, 73, 0.1);
	border-color: rgba(59, 130, 246, 0.15);
}

:root[data-theme="dark"] .plus-benefit-card {
	border-color: rgba(255, 255, 255, 0.06);
	box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

:root[data-theme="dark"] .plus-benefit-card:hover {
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
	border-color: rgba(59, 130, 246, 0.25);
}

.plus-benefit-card-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 48px;
	height: 48px;
	border-radius: 14px;
	background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.04));
	color: #3b82f6;
	flex-shrink: 0;
	transition: transform 0.2s ease;
}

:root[data-theme="dark"] .plus-benefit-card-icon {
	background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.08));
	color: #60a5fa;
}

/* ═══════════════════════════════════════
   ICON BADGES
   ═══════════════════════════════════════ */

.plus-icon-badge {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border-radius: 10px;
	flex-shrink: 0;
}

/* ═══════════════════════════════════════
   TRUST ICONS
   ═══════════════════════════════════════ */

.plus-trust-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 48px;
	height: 48px;
	border-radius: 14px;
	background: rgba(16, 185, 129, 0.06);
	color: #10b981;
	margin-bottom: 4px;
}

:root[data-theme="dark"] .plus-trust-icon {
	background: rgba(16, 185, 129, 0.1);
	color: #34d399;
}

/* ═══════════════════════════════════════
   INFO ROWS
   ═══════════════════════════════════════ */

.plus-info-row {
	display: flex;
	align-items: flex-start;
	gap: 12px;
	padding: 12px 14px;
	border-radius: 12px;
	background: rgba(0, 0, 0, 0.02);
}

:root[data-theme="dark"] .plus-info-row {
	background: rgba(255, 255, 255, 0.04);
}

/* ═══════════════════════════════════════
   RECEIPT ROWS
   ═══════════════════════════════════════ */

.plus-receipt-row {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;
	padding: 14px 16px;
	border-radius: 14px;
	background: rgba(0, 0, 0, 0.015);
	border: 1px solid transparent;
	transition: all 0.15s ease;
}

.plus-receipt-row:hover {
	background: rgba(59, 130, 246, 0.03);
	border-color: rgba(59, 130, 246, 0.08);
}

:root[data-theme="dark"] .plus-receipt-row {
	background: rgba(255, 255, 255, 0.03);
}

:root[data-theme="dark"] .plus-receipt-row:hover {
	background: rgba(59, 130, 246, 0.06);
	border-color: rgba(59, 130, 246, 0.12);
}

/* ═══════════════════════════════════════
   STATUS PILLS
   ═══════════════════════════════════════ */

.plus-status-pill {
	display: inline-flex;
	align-items: center;
	padding: 2px 8px;
	border-radius: 20px;
	font-size: 10px;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 0.04em;
}

.plus-status-paid {
	background: rgba(16, 185, 129, 0.1);
	color: #059669;
}

:root[data-theme="dark"] .plus-status-paid {
	background: rgba(16, 185, 129, 0.15);
	color: #34d399;
}

.plus-status-default {
	background: rgba(107, 114, 128, 0.1);
	color: #6b7280;
}

/* ═══════════════════════════════════════
   EMPTY STATE
   ═══════════════════════════════════════ */

.plus-empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	text-align: center;
}

.plus-empty-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 64px;
	height: 64px;
	border-radius: 20px;
	background: rgba(0, 0, 0, 0.03);
	color: #d1d5db;
}

:root[data-theme="dark"] .plus-empty-icon {
	background: rgba(255, 255, 255, 0.05);
	color: #4b5563;
}

/* ═══════════════════════════════════════
   LOADING RING
   ═══════════════════════════════════════ */

.plus-loading-ring {
	border: 3px solid rgba(0, 0, 0, 0.05);
	border-top-color: #3b82f6;
	border-radius: 50%;
}

:root[data-theme="dark"] .plus-loading-ring {
	border-color: rgba(255, 255, 255, 0.08);
	border-top-color: #60a5fa;
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */

.plus-btn-primary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 12px 20px;
	border-radius: 12px;
	font-size: 14px;
	font-weight: 700;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;
	box-shadow: 0 2px 8px rgba(13, 110, 253, 0.25);
}

.plus-btn-primary:hover {
	background: linear-gradient(135deg, #0b5ed7, #084298);
	transform: translateY(-1px);
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.35);
}

.plus-btn-primary:disabled {
	opacity: 0.6;
	pointer-events: none;
}

.plus-btn-cta {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 16px 24px;
	border-radius: 14px;
	font-size: 15px;
	font-weight: 800;
	color: #fff;
	background: linear-gradient(135deg, #0d6efd, #0b5ed7);
	border: none;
	cursor: pointer;
	transition: all 0.25s ease;
	box-shadow: 0 4px 16px rgba(13, 110, 253, 0.3);
}

.plus-btn-cta:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 32px rgba(13, 110, 253, 0.4);
}

.plus-btn-cta:disabled {
	opacity: 0.7;
	pointer-events: none;
}

.plus-btn-outline {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 8px 14px;
	border-radius: 10px;
	font-weight: 600;
	color: #374151;
	background: transparent;
	border: 1.5px solid rgba(0, 0, 0, 0.1);
	cursor: pointer;
	transition: all 0.15s ease;
}

.plus-btn-outline:hover {
	background: rgba(0, 0, 0, 0.03);
	border-color: rgba(0, 0, 0, 0.18);
}

:root[data-theme="dark"] .plus-btn-outline {
	color: #d1d5db;
	border-color: rgba(255, 255, 255, 0.12);
}

:root[data-theme="dark"] .plus-btn-outline:hover {
	background: rgba(255, 255, 255, 0.06);
	border-color: rgba(255, 255, 255, 0.2);
}

.plus-btn-ghost {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 8px 14px;
	border-radius: 10px;
	font-weight: 600;
	color: #6b7280;
	background: transparent;
	border: none;
	cursor: pointer;
	transition: all 0.15s ease;
}

.plus-btn-ghost:hover {
	background: rgba(0, 0, 0, 0.04);
	color: #374151;
}

:root[data-theme="dark"] .plus-btn-ghost:hover {
	background: rgba(255, 255, 255, 0.06);
	color: #e5e7eb;
}

.plus-btn-danger-ghost {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 6px;
	padding: 10px 16px;
	border-radius: 12px;
	font-size: 13px;
	font-weight: 600;
	color: #9ca3af;
	background: transparent;
	border: none;
	cursor: pointer;
	transition: all 0.15s ease;
}

.plus-btn-danger-ghost:hover {
	color: #ef4444;
	background: rgba(239, 68, 68, 0.06);
}

:root[data-theme="dark"] .plus-btn-danger-ghost:hover {
	background: rgba(239, 68, 68, 0.1);
}

/* ═══════════════════════════════════════
   MODAL
   ═══════════════════════════════════════ */

.plus-modal-content {
	background: var(--sb-white);
	border-radius: 20px;
	box-shadow: 0 24px 64px rgba(0, 0, 0, 0.3);
	overflow: hidden;
}

/* Modal Transition */
.plus-modal-enter-active,
.plus-modal-leave-active {
	transition: all 0.25s ease;
}

.plus-modal-enter-from,
.plus-modal-leave-to {
	opacity: 0;
}

.plus-modal-enter-from .plus-modal-content,
.plus-modal-leave-to .plus-modal-content {
	transform: scale(0.95) translateY(10px);
}

/* ═══════════════════════════════════════
   GRADIENT ANIMATION
   ═══════════════════════════════════════ */

@keyframes gradient-x {
	0%, 100% { background-position: 0% 50%; }
	50% { background-position: 100% 50%; }
}

.animate-gradient-x {
	background-size: 200% auto;
	animation: gradient-x 4s ease infinite;
}
</style>

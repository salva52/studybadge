<template>
	<div class="relative flex h-full flex-col">
		<div class="h-full flex-1">
			<div class="flex h-screen text-base bg-sb-bg">
				<div class="w-full overflow-auto" id="scrollContainer">
					<slot />
				</div>
			</div>
		</div>
	</div>
</template>

import frappeUIPreset from 'frappe-ui/tailwind'

export default {
	presets: [frappeUIPreset],
	content: [
		'./index.html',
		'./src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
	],
	theme: {
		extend: {
			colors: {
				'sb-dark': 'var(--sb-dark)',
				'sb-primary': 'var(--sb-primary)',
				'sb-medium': 'var(--sb-medium)',
				'sb-accent': 'var(--sb-accent)',
				'sb-bg': 'var(--sb-bg)',
				'sb-white': 'var(--sb-white)',
				'sb-accent-light': 'var(--sb-accent-light)',
			},
			fontFamily: {
				inter: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
			},
			strokeWidth: {
				1.5: '1.5',
			},
			screens: {
				'2xl': '1600px',
				'3xl': '1920px',
			},
			boxShadow: {
				'sb-card': '0 2px 12px rgba(6, 27, 73, 0.08)',
				'sb-card-hover': '0 8px 24px rgba(6, 27, 73, 0.12)',
				'sb-soft': '0 1px 4px rgba(6, 27, 73, 0.06)',
			},
			borderRadius: {
				'sb': '12px',
				'sb-lg': '16px',
			},
		},
	},
	plugins: [],
}

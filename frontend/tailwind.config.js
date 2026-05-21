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
				'sb-dark': '#061B49',
				'sb-primary': '#007BFF',
				'sb-medium': '#0A84FF',
				'sb-accent': '#F5B301',
				'sb-bg': '#F5F7FB',
				'sb-accent-light': '#FFF8E1',
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

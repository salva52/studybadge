<template>
	<div class="table-wrap">
		<table>
			<thead>
				<tr>
					<th v-for="col in columns" :key="col.key">{{ col.label }}</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(row, index) in rows" :key="row.name || index">
					<td v-for="col in columns" :key="col.key">
						{{ format(row[col.key]) }}
					</td>
				</tr>
				<tr v-if="!rows?.length">
					<td :colspan="columns.length" class="empty-cell">
						{{ __('Sin datos todavía.') }}
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
defineProps({
	columns: {
		type: Array,
		default: () => [],
	},
	rows: {
		type: Array,
		default: () => [],
	},
})

const format = (value) => {
	if (value === 1) return __('Sí')
	if (value === 0) return __('No')
	if (value === null || value === undefined || value === '') return '-'
	return value
}
</script>

<style scoped>
.table-wrap {
	overflow-x: auto;
}
table {
	width: 100%;
	border-collapse: collapse;
	font-size: 14px;
}
th,
td {
	text-align: left;
	border-bottom: 1px solid #eaecf0;
	padding: 10px 8px;
	vertical-align: top;
}
th {
	color: #667085;
	font-size: 12px;
	text-transform: uppercase;
	font-weight: 900;
}
.empty-cell {
	text-align: center;
	color: #667085;
	padding: 28px;
}
</style>

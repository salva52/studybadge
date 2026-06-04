const fs = require('fs');

const vueFile = 'frontend/src/pages/Study/Study.vue';
const txtFile = 'C:/Users/troll/Downloads/studyvue.txt';

let vueContent = fs.readFileSync(vueFile, 'utf8');
const txtContent = fs.readFileSync(txtFile, 'utf8');

// Find the first <style scoped> block
const startMatch = vueContent.match(/<style scoped>/);
if (!startMatch) {
    console.error('Could not find <style scoped> in Study.vue');
    process.exit(1);
}

const startIndex = startMatch.index;

// Find the end of the <style scoped> block.
// Since there are multiple </style> tags, we look for the first </style> after startIndex
const endIndex = vueContent.indexOf('</style>', startIndex);
if (endIndex === -1) {
    console.error('Could not find </style> in Study.vue');
    process.exit(1);
}

// Ensure the txtContent starts with <style scoped> and ends with </style>
let newStyle = txtContent.trim();
if (!newStyle.startsWith('<style scoped>')) {
    newStyle = '<style scoped>\n' + newStyle;
}
if (!newStyle.endsWith('</style>')) {
    newStyle = newStyle + '\n</style>';
}

const newVueContent = vueContent.substring(0, startIndex) + newStyle + vueContent.substring(endIndex + '</style>'.length);

fs.writeFileSync(vueFile, newVueContent, 'utf8');
console.log('Successfully replaced <style scoped> block.');

$vueFile = "C:\Users\troll\Documents\studybadge\lms\frontend\src\pages\AISessions.vue"
$txtFile = "C:\Users\troll\Downloads\aisessions.txt"

$vueContent = [System.IO.File]::ReadAllText($vueFile)
$txtContent = [System.IO.File]::ReadAllText($txtFile)

$startIndex = $vueContent.IndexOf("<style scoped>")
if ($startIndex -eq -1) {
    Write-Host "Could not find <style scoped> in AISessions.vue"
    exit 1
}

$endIndex = $vueContent.IndexOf("</style>", $startIndex)
if ($endIndex -eq -1) {
    Write-Host "Could not find </style> in AISessions.vue"
    exit 1
}

$newStyle = $txtContent.Trim()

if (-not $newStyle.StartsWith("<style scoped>")) {
    $newStyle = "<style scoped>`n" + $newStyle
}

if ($newStyle.EndsWith("</style>")) {
    $newStyle = $newStyle.Substring(0, $newStyle.Length - 8).TrimEnd()
}

$extraCss = @"
/* ═══════════════════════════════════════════════
   QUITAR DEGRADADOS — STUDYBADGE CLEAN STYLE
   Pega esto al final del <style scoped>
   ═══════════════════════════════════════════════ */

.chat-page {
	background: #f5f8fc !important;
}

.primary-btn {
	background: #0a2251 !important;
}

.primary-btn:hover:not(:disabled) {
	background: #12356e !important;
}

.send-btn {
	background: #0a2251 !important;
}

.send-btn:hover:not(:disabled) {
	background: #12356e !important;
}

.message-row.user .message-bubble {
	background: #0a2251 !important;
}

.tool-card::after {
	background: #0a2251 !important;
}

.new-form::before,
.new-chat-inner::before {
	display: none !important;
}

.composer-wrap {
	background: #f5f8fc !important;
}

.composer-wrap::before,
.composer-wrap::after {
	display: none !important;
}

/* MOBILE SIN DEGRADADO */
@media (max-width: 760px) {
	.chat-page {
		background: #f5f8fc !important;
	}

	.composer-wrap {
		background: #f5f8fc !important;
	}
}

/* DARK MODE SIN DEGRADADO */
:global(:root[data-theme='dark']) .chat-page,
:global(.dark) .chat-page {
	background: #07111f !important;
}

:global(:root[data-theme='dark']) .composer-wrap,
:global(.dark) .composer-wrap {
	background: #07111f !important;
}
</style>
"@

$newStyle = $newStyle + "`n`n" + $extraCss

$newVueContent = $vueContent.Substring(0, $startIndex) + $newStyle + $vueContent.Substring($endIndex + 8)

[System.IO.File]::WriteAllText($vueFile, $newVueContent)
Write-Host "Successfully replaced <style scoped> block in AISessions.vue."

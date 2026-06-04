$vueFile = "frontend\src\pages\Study\Study.vue"
$txtFile = "C:\Users\troll\Downloads\studyvue.txt"

$vueContent = [System.IO.File]::ReadAllText($vueFile)
$txtContent = [System.IO.File]::ReadAllText($txtFile)

$startIndex = $vueContent.IndexOf("<style scoped>")
if ($startIndex -eq -1) {
    Write-Host "Could not find <style scoped> in Study.vue"
    exit 1
}

$endIndex = $vueContent.IndexOf("</style>", $startIndex)
if ($endIndex -eq -1) {
    Write-Host "Could not find </style> in Study.vue"
    exit 1
}

$newStyle = $txtContent.Trim()
if (-not $newStyle.StartsWith("<style scoped>")) {
    $newStyle = "<style scoped>`n" + $newStyle
}
if (-not $newStyle.EndsWith("</style>")) {
    $newStyle = $newStyle + "`n</style>"
}

$newVueContent = $vueContent.Substring(0, $startIndex) + $newStyle + $vueContent.Substring($endIndex + 8)

[System.IO.File]::WriteAllText($vueFile, $newVueContent)
Write-Host "Successfully replaced <style scoped> block."

# Builds Tommy-itch.zip in the project root for an itch.io HTML game: index.html at the top level,
# plus the audio and image files it loads. Paths inside the zip use forward slashes, as itch.io expects.
$root = Split-Path $PSScriptRoot -Parent
& (Join-Path $PSScriptRoot "wrap.ps1")
$out = Join-Path $root "Tommy-itch.zip"
if (Test-Path $out) { Remove-Item $out }
Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::Open($out, 'Create')
$add = { param($file, $name) [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $file, $name, 'Optimal') }
& $add (Join-Path $PSScriptRoot "game.html") "index.html"
Get-ChildItem (Join-Path $root "audio") -Filter *.mp3 | ForEach-Object { & $add $_.FullName "audio/$($_.Name)" }
foreach ($a in "water.jpg","tree-sheet.jpg","tommy-toon-glb.txt","stephen-marsh-glb.txt") { & $add (Join-Path $root "assets\$a") "assets/$a" }
$zip.Dispose()
$z = [IO.Compression.ZipFile]::OpenRead($out); $z.Entries | Select-Object FullName, Length; $z.Dispose()
Get-Item $out | Select-Object Name, Length

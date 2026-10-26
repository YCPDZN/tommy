# Wraps the artifact page in a full HTML document (build\game.html) for the exe and local preview.
$root = Split-Path $PSScriptRoot -Parent
$src = Get-Content -Raw -Encoding UTF8 (Join-Path $root "tommy-night-run.html")
$marker = '<canvas id="scene"'
if (-not $src.Contains($marker)) { throw "marker not found" }
$head = "<!doctype html>`n<html lang=`"en`">`n<head>`n<meta charset=`"utf-8`">`n<meta name=`"viewport`" content=`"width=device-width, initial-scale=1, viewport-fit=cover`">`n<style>body{margin:0;font-size:14px}</style>`n"
$out = $head + $src.Replace($marker, "</head>`n<body>`n" + $marker) + "`n</body>`n</html>`n"
[IO.File]::WriteAllText((Join-Path $PSScriptRoot "game.html"), $out, (New-Object Text.UTF8Encoding $false))
# the voice clips sit next to the page
Copy-Item (Join-Path $root "audio") $PSScriptRoot -Recurse -Force
Copy-Item (Join-Path $root "assets") $PSScriptRoot -Recurse -Force

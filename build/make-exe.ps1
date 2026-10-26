# Builds Tommy.exe in the project root: the wrapped page, the audio and the images, embedded in a small
# launcher compiled with the C# compiler that ships with Windows (.NET Framework 4).
$root = Split-Path $PSScriptRoot -Parent
& (Join-Path $PSScriptRoot "wrap.ps1")
$launcher = Join-Path $PSScriptRoot "launcher"
$ico = Join-Path $launcher "tommy.ico"
if (-not (Test-Path $ico)) {
  Add-Type -AssemblyName System.Drawing
  $bmp = New-Object Drawing.Bitmap 64,64; $g = [Drawing.Graphics]::FromImage($bmp); $g.SmoothingMode = 'AntiAlias'
  $g.FillEllipse((New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(9,13,27))),0,0,63,63)
  $g.FillEllipse((New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(60,182,227))),4,4,55,55)
  $f = New-Object Drawing.Font("Arial Black",30,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $sf = New-Object Drawing.StringFormat; $sf.Alignment = 'Center'; $sf.LineAlignment = 'Center'
  $g.DrawString("T",$f,(New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(9,13,27))),(New-Object Drawing.RectangleF 0,2,64,64),$sf)
  $fs = [IO.File]::Create($ico); ([Drawing.Icon]::FromHandle($bmp.GetHicon())).Save($fs); $fs.Close()
}
$res = @("/resource:$(Join-Path $PSScriptRoot 'game.html'),index.html")
Get-ChildItem (Join-Path $root "audio") -Filter *.mp3 | ForEach-Object { $res += "/resource:$($_.FullName),audio/$($_.Name)" }
foreach ($a in "water.jpg","tree-sheet.jpg") { $res += "/resource:$(Join-Path $root "assets\$a"),assets/$a" }
$out = Join-Path $root "Tommy.exe"
& "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:winexe /optimize "/out:$out" "/win32icon:$ico" /r:System.Windows.Forms.dll @res (Join-Path $launcher "TommyLauncher.cs")
if ($LASTEXITCODE -ne 0) { throw "compile failed" }
Get-Item $out | Select-Object Name, Length

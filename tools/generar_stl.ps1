# Convierte soluciones/scad/*.scad en soluciones/stl/*.stl con OpenSCAD.
param([string]$OpenScad = "$env:LOCALAPPDATA\Programs\openscad-2021.01\openscad.com")
$root = Split-Path $PSScriptRoot -Parent
$in = Join-Path $root "soluciones\scad"; $out = Join-Path $root "soluciones\stl"
New-Item -ItemType Directory -Force $out | Out-Null
Get-ChildItem $in -Filter *.scad | ForEach-Object {
  $dst = Join-Path $out ($_.BaseName + ".stl")
  $t = Measure-Command { & $OpenScad -o $dst $_.FullName 2>&1 | Out-Null }
  if (Test-Path $dst) { "{0,-28} {1,7:N0} KB  {2,5:N1} s" -f $_.BaseName, ((Get-Item $dst).Length / 1KB), $t.TotalSeconds }
  else { "{0,-28} ERROR" -f $_.BaseName }
}

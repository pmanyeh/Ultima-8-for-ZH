# Build the Windows portable package (P14) into dist\Ultima8-zhTW-<Version>\ and a zip.
#
#   make_package.ps1 [-Version 0.9.0-beta] [-NoZip] [-Test]
#
# Needs: the Release build (tools\build\build_release.bat), Python, the font in
# private_test\extra. The catalog is compiled fresh from localization\zh_TW.
# -Test copies the package to private_test\package_test, adds the game from
# private_test\scummvm-dev.ini to its scummvm.ini (portable mode, nothing else
# on the command line), starts it once, closes it and prints the log.
# The game window is not touched.
param(
    [string]$Version = '0.9.0-beta',
    [switch]$NoZip,
    [switch]$Test
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$src = Join-Path $root 'scummvm-src'
$rel = Join-Path $src 'build-dev\Releasex64'
$crt = 'C:\Program Files\Microsoft Visual Studio\18\Community\VC\Redist\MSVC\14.51.36231\x64\Microsoft.VC145.CRT'
$font = Join-Path $root 'private_test\extra'
$name = "Ultima8-zhTW-$Version"
$dist = Join-Path $root 'dist'
$out = Join-Path $dist $name

if (-not (Test-Path (Join-Path $rel 'scummvm.exe'))) { throw "Release build missing; run tools\build\build_release.bat" }
if (-not (Test-Path $crt)) { throw "VC runtime not found: $crt" }
if (git -C $src status --porcelain --untracked-files=no) { Write-Warning 'scummvm-src has uncommitted changes' }
if (git -C $root status --porcelain --untracked-files=no -- localization) { Write-Warning 'localization has uncommitted changes' }
$engineCommit = (git -C $src rev-parse --short=10 HEAD).Trim()
$mainCommit = (git -C $root rev-parse --short=10 HEAD).Trim()

if (Test-Path $out) { Remove-Item -Recurse -Force $out }
New-Item -ItemType Directory -Force $out, "$out\extra" | Out-Null   # ScummVM creates "Saved games" itself

# engine, libraries, VC runtime
Copy-Item (Join-Path $rel 'scummvm.exe'), (Join-Path $rel '*.dll') $out
Copy-Item (Join-Path $crt '*.dll') $out

# translation catalog (fresh) and fonts (Cubic 11; jf open huninn for the
# high-res text layer; Wang Han-Tzong Wei Bei for engravings)
$env:PYTHONIOENCODING = 'utf-8'
python (Join-Path $root 'tools\catalog\po_compile.py') zh_TW (Join-Path $root 'localization\zh_TW') -o "$out\extra\u8_zh_TW.mo"
if ($LASTEXITCODE) { throw 'po_compile failed' }
Copy-Item (Join-Path $font 'Cubic_11.ttf'), (Join-Path $font 'Cubic_11-OFL.txt'),
          (Join-Path $font 'jf-openhuninn-2.1.ttf'), (Join-Path $font 'jf-openhuninn-OFL.txt'),
          (Join-Path $font 'WangHanZongWeiBeiTiFan-2.ttf'), (Join-Path $font 'WangHanZong-GPLv2.txt') "$out\extra"

# portable config: its presence next to scummvm.exe turns on portable mode.
# package\scummvm.ini has the settings with comments (UTF-8; ScummVM keeps
# "#" comment lines when it writes the file again)
Copy-Item (Join-Path $root 'package\scummvm.ini') "$out\scummvm.ini"

# launcher: the relative extrapath needs the package folder as working directory
"@echo off`r`ncd /d `"%~dp0`"`r`nstart `"`" scummvm.exe %*`r`n" |
    Set-Content -Encoding ascii -NoNewline (Join-Path $out ([char]0x555F + [char]0x52D5 + ' Ultima 8.bat'))

# documents and licenses
Copy-Item (Join-Path $root 'package\*.md') $out
(Get-Content -Raw -Encoding utf8 "$out\CHANGELOG.md").Replace('{ENGINE_COMMIT}', $engineCommit).Replace('{MAIN_COMMIT}', $mainCommit) |
    Set-Content -Encoding utf8 -NoNewline "$out\CHANGELOG.md"
Copy-Item (Join-Path $src 'COPYING') "$out\COPYING.txt"
Copy-Item (Join-Path $src 'COPYRIGHT') "$out\COPYRIGHT-ScummVM.txt"
Copy-Item (Join-Path $src 'AUTHORS') "$out\AUTHORS-ScummVM.txt"
Copy-Item -Recurse (Join-Path $src 'LICENSES') "$out\LICENSES"
Write-Output "package: $out (engine $engineCommit, main $mainCommit)"

if (-not $NoZip) {
    $zip = Join-Path $dist "$name.zip"
    if (Test-Path $zip) { Remove-Item $zip }
    Compress-Archive -Path $out -DestinationPath $zip
    Write-Output ("zip: $zip ({0:N1} MB)" -f ((Get-Item $zip).Length / 1MB))
}

if ($Test) {
    $t = Join-Path $root 'private_test\package_test'
    if (Test-Path $t) { Remove-Item -Recurse -Force $t }
    Copy-Item -Recurse $out $t
    # game domain from the dev config, without the settings the package should provide
    $skip = '^(font_cjk_\w+|localization\w*|extrapath|savepath|lastSave)='
    $game = $false
    $lines = foreach ($l in (Get-Content -Encoding utf8 (Join-Path $root 'private_test\scummvm-dev.ini'))) {
        if ($l -match '^\[') { $game = ($l -eq '[ultima8]') }
        if ($game -and $l -notmatch $skip) { $l }
    }
    Add-Content -Encoding ascii "$t\scummvm.ini" (@('') + $lines)
    $log = Join-Path $t 'test.log'
    $p = Start-Process -FilePath "$t\scummvm.exe" -WorkingDirectory $t -PassThru `
        -ArgumentList "`"--logfile=$log`"", '--debuglevel=1', '--debugflags=Localization', 'ultima8'
    $deadline = (Get-Date).AddSeconds(40)
    while ((Get-Date) -lt $deadline -and -not $p.HasExited) {
        Start-Sleep -Milliseconds 500
        if ((Test-Path $log) -and (Select-String -Path $log -Pattern 'Game Initialized' -Quiet)) { Start-Sleep -Seconds 2; break }
    }
    if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force; $p.WaitForExit() }
    Write-Output "== package test ($t)"
    if (Test-Path $log) { Select-String -Path $log -Pattern 'U8-L10N|TTF|CJK|WARNING|Game Initialized|portable' | ForEach-Object { $_.Line } }
    else { Write-Output '(no log)' }
}

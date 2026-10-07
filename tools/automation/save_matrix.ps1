# Save matrix (Phase 12): load a savegame in English and localized mode, let
# ScummVM autosave it (slot 0), close the game, then load each result in the
# other mode and autosave again. Only copies of the saves are used (work
# directory); the game windows are not touched, every run closes its own
# process.
#
#   save_matrix.ps1 [-Slot 1] [-Work private_test\save_matrix] [-Exe scummvm.exe] [-EnglishOnly]
#                   [-Source <savegame file instead of the slot in private_test\saves>]
#
# Timing: ScummVM tries an autosave before it loads the savegame; at that
# moment the new-game setup has the avatar in stasis, the attempt fails and
# ScummVM waits 5 minutes before the next one. So every run takes about
# 5 minutes; the runs of one stage run at the same time (about 11 minutes).
#
# Results in <Work>\results: source (the savegame), en1 / en2 (English, twice:
# timing baseline), zh1 (localized), zh_to_en (zh1 loaded in English),
# en_to_zh (en1 loaded localized). Compare with tools\validate\save_compare.py.
param(
    [int]$Slot = 1,
    [string]$Work = '',
    [string]$Exe = '',
    [switch]$EnglishOnly,
    [string]$Source = '',
    [int]$TimeoutSeconds = 420
)
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$exe = if ($Exe) { $Exe } else { Join-Path $root 'scummvm-src\build-dev\Debugx64\scummvm.exe' }
$priv = Join-Path $root 'private_test'
$extra = Join-Path $priv 'extra'
if (-not $Work) { $Work = Join-Path $priv 'save_matrix' }
if (Test-Path $Work) { Remove-Item -Recurse -Force $Work }
$results = Join-Path $Work 'results'
New-Item -ItemType Directory -Force $results | Out-Null

function Start-Run([string]$name, [string]$baseIni, [string]$source) {
    # one run: $source as slot $Slot of an empty save directory
    $dir = Join-Path $Work $name
    $saves = Join-Path $dir 'saves'
    New-Item -ItemType Directory -Force $saves | Out-Null
    Copy-Item $source (Join-Path $saves ("ultima8.{0:D3}" -f $Slot))
    $ini = Join-Path $dir 'scummvm.ini'
    $out = foreach ($l in (Get-Content -LiteralPath $baseIni)) {
        if ($l -match '^(savepath|lastSave|autosave_period)=') { continue }
        $l
        if ($l -eq '[ultima8]') { "savepath=$saves\"; 'autosave_period=10' }
    }
    $out | Set-Content -Encoding utf8 -LiteralPath $ini
    $log = Join-Path $dir 'run.log'
    $argList = @("--config=$ini", "--logfile=$log", "--extrapath=$extra", '--debuglevel=1',
                 '--debugflags=Localization', "--save-slot=$Slot", 'ultima8')
    $p = Start-Process -FilePath $exe -ArgumentList ($argList | ForEach-Object { "`"$_`"" }) -PassThru
    return @{ Name = $name; Process = $p; Auto = (Join-Path $saves 'ultima8.000'); Log = $log }
}

function Wait-Runs($runs) {
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $pending = @($runs | Where-Object { -not $_.Process.HasExited -and -not (Test-Path $_.Auto) })
        if ($pending.Count -eq 0) { break }
        Start-Sleep -Seconds 2
    }
    Start-Sleep -Seconds 3      # let the files be written completely
    foreach ($r in $runs) {
        if (-not $r.Process.HasExited) { Stop-Process -Id $r.Process.Id -Force; $r.Process.WaitForExit() }
        if (Test-Path $r.Auto) {
            Copy-Item $r.Auto (Join-Path $results "$($r.Name).sav")
            Write-Output "$($r.Name) : autosave OK"
        } else {
            Write-Output "$($r.Name) : NO AUTOSAVE (see $($r.Log))"
        }
    }
}

$source = if ($Source) { $Source } else { Join-Path $priv ("saves\ultima8.{0:D3}" -f $Slot) }
$zhIni = Join-Path $priv 'scummvm-dev.ini'
$enIni = Join-Path $priv 'scummvm-dev-en.ini'
Copy-Item $source (Join-Path $results 'source.sav')

$runs = @((Start-Run 'en1' $enIni $source), (Start-Run 'en2' $enIni $source))
if (-not $EnglishOnly) { $runs += Start-Run 'zh1' $zhIni $source }
Wait-Runs $runs

if (-not $EnglishOnly) {
    $runs = @()
    if (Test-Path (Join-Path $results 'zh1.sav')) { $runs += Start-Run 'zh_to_en' $enIni (Join-Path $results 'zh1.sav') }
    if (Test-Path (Join-Path $results 'en1.sav')) { $runs += Start-Run 'en_to_zh' $zhIni (Join-Path $results 'en1.sav') }
    if ($runs.Count) { Wait-Runs $runs }
}
Write-Output "results: $results"

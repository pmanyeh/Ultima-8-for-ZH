# Startup regression (Phase 12, recreates the Phase 4 scenarios): start the dev
# build with each configuration until "-- Game Initialized --", close it and
# print the localization log lines. The game window is not touched.
#
#   regression_startup.ps1 [-Work private_test\regression]
#
# Scenarios (all based on private_test\scummvm-dev.ini, new game):
#   A off            localization=off
#   B zh_TW          localization=zh_TW (normal)
#   C missing        localization_file=p12test_missing.mo
#   D broken         catalog truncated by 40 bytes
#   E language       catalog header says ja_JP
#   F no font        font_cjk_file=p12test_missing.ttf
#   G unset          no localization key
#   H no override    localization=zh_TW, font_override=false
#   I English ini    private_test\scummvm-dev-en.ini
# Test catalogs are written to private_test\extra\p12test_* and removed again.
param([string]$Work = '')
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$priv = Join-Path $root 'private_test'
$extra = Join-Path $priv 'extra'
if (-not $Work) { $Work = Join-Path $priv 'regression' }
if (Test-Path $Work) { Remove-Item -Recurse -Force $Work }
New-Item -ItemType Directory -Force $Work | Out-Null
$check = Join-Path $PSScriptRoot 'startup_check.ps1'

# test catalogs
$mo = [IO.File]::ReadAllBytes((Join-Path $extra 'u8_zh_TW.mo'))
[IO.File]::WriteAllBytes((Join-Path $extra 'p12test_broken.mo'), $mo[0..($mo.Length - 41)])
$text = [Text.Encoding]::GetEncoding(28591).GetString($mo)       # byte-preserving
$ja = [Text.Encoding]::GetEncoding(28591).GetBytes($text.Replace('Language: zh_TW', 'Language: ja_JP'))
[IO.File]::WriteAllBytes((Join-Path $extra 'p12test_ja.mo'), $ja)

function New-Config([string]$name, [string]$base, [hashtable]$set, [string[]]$remove = @()) {
    $keys = @($set.Keys) + $remove
    $out = foreach ($l in (Get-Content -LiteralPath $base)) {
        $k = ($l -split '=', 2)[0]
        if ($keys -contains $k -or $k -eq 'lastSave') { continue }
        $l
        if ($l -eq '[ultima8]') { foreach ($e in $set.GetEnumerator()) { "$($e.Key)=$($e.Value)" } }
    }
    $ini = Join-Path $Work "$name.ini"
    $out | Set-Content -Encoding utf8 -LiteralPath $ini
    return $ini
}

$zh = Join-Path $priv 'scummvm-dev.ini'
$scenarios = [ordered]@{
    'A-off'        = New-Config 'A-off' $zh @{ localization = 'off' }
    'B-zh_TW'      = New-Config 'B-zh_TW' $zh @{ localization = 'zh_TW' }
    'C-missing'    = New-Config 'C-missing' $zh @{ localization = 'zh_TW'; localization_file = 'p12test_missing.mo' }
    'D-broken'     = New-Config 'D-broken' $zh @{ localization = 'zh_TW'; localization_file = 'p12test_broken.mo' }
    'E-language'   = New-Config 'E-language' $zh @{ localization = 'zh_TW'; localization_file = 'p12test_ja.mo' }
    'F-nofont'     = New-Config 'F-nofont' $zh @{ localization = 'zh_TW'; font_cjk_file = 'p12test_missing.ttf' }
    'G-unset'      = New-Config 'G-unset' $zh @{} @('localization')
    'H-nooverride' = New-Config 'H-nooverride' $zh @{ localization = 'zh_TW'; font_override = 'false' }
    'I-english'    = New-Config 'I-english' (Join-Path $priv 'scummvm-dev-en.ini') @{}
}
foreach ($s in $scenarios.GetEnumerator()) {
    & $check -Config $s.Value -Seconds 40 -Pattern 'U8-L10N|TTF|CJK|WARNING|Game Initialized' `
        -Log (Join-Path $Work "$($s.Key).log")
}
Remove-Item (Join-Path $extra 'p12test_*')

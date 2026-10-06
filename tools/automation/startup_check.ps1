# Start the dev build with a given config, wait until the game has started
# (or a timeout), close it again and print the log lines matching -Pattern.
# Only the process started here is closed; the game window is not touched.
#
#   startup_check.ps1 -Config my.ini [-Seconds 20] [-Pattern 'U8-L10N|WARNING'] [-Log out.log]
param(
    [Parameter(Mandatory = $true)][string]$Config,
    [int]$Seconds = 20,
    [string]$Pattern = 'U8-L10N|WARNING',
    [string]$Log = '',
    [string]$Exe = ''
)
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not $Exe) { $Exe = Join-Path $root 'scummvm-src\build-dev\Debugx64\scummvm.exe' }
$extra = Join-Path $root 'private_test\extra'
if (-not $Log) { $Log = [IO.Path]::ChangeExtension($Config, '.log') }
if (Test-Path $Log) { Remove-Item $Log }

$argList = @("--config=$Config", "--logfile=$Log", "--extrapath=$extra",
          '--debuglevel=1', '--debugflags=Localization', 'ultima8')
$p = Start-Process -FilePath $Exe -ArgumentList ($argList | ForEach-Object { "`"$_`"" }) -PassThru

# "Game Started" is logged once the game data, fonts and settings are set up
$deadline = (Get-Date).AddSeconds($Seconds)
while ((Get-Date) -lt $deadline -and -not $p.HasExited) {
    Start-Sleep -Milliseconds 500
    if ((Test-Path $Log) -and (Select-String -Path $Log -Pattern '-- Game Started --|Game Initialized' -Quiet)) {
        Start-Sleep -Seconds 2
        break
    }
}
if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force; $p.WaitForExit() }

Write-Output "== $Config"
if (Test-Path $Log) {
    Select-String -Path $Log -Pattern $Pattern | ForEach-Object { $_.Line }
} else {
    Write-Output '(no log)'
}

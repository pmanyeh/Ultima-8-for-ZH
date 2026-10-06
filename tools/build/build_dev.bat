@echo off
rem Dev build (branch ultima8-zh-tw-dev)
call "C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64 >nul || exit /b 1
set SRC=D:\git\Ultima 8 for ZH\scummvm-src
if not exist "%SRC%\build-dev" mkdir "%SRC%\build-dev"
cd /d "%SRC%\build-dev" || exit /b 1
"%SRC%\devtools\create_project\cmake\Debug\create_project.exe" .. --msvc --vcpkg --disable-all-engines --enable-engine=ultima,ultima8 >nul || exit /b 1

msbuild scummvm.sln /m /p:Configuration=Debug /p:Platform=x64 /p:PreferredToolArchitecture=x64 /p:BuildInParallel=true ^
  /p:VcpkgRoot=D:\vcpkg\ /p:VcpkgEnableManifest=true /p:VcpkgManifestInstall=false ^
  /p:VcpkgInstalledDir=D:\vcpkg\installed_scummvm\ ^
  /p:ForceImportAfterCppTargets=D:\vcpkg\scripts\buildsystems\msbuild\vcpkg.targets ^
  /v:minimal /nologo

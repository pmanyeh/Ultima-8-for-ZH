@echo off
rem Phase 1: Debug build with DEBUG_USECODE defined via the CL env var (no source changes)
call "C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64 >nul || exit /b 1
set SRC=D:\git\Ultima 8 for ZH\scummvm-src
if not exist "%SRC%\build-trace" mkdir "%SRC%\build-trace"
cd /d "%SRC%\build-trace" || exit /b 1
"%SRC%\devtools\create_project\cmake\Debug\create_project.exe" .. --msvc --vcpkg --disable-all-engines --enable-engine=ultima,ultima8 >nul || exit /b 1
set CL=/DDEBUG_USECODE
msbuild scummvm.sln /m /p:Configuration=Debug /p:Platform=x64 /p:PreferredToolArchitecture=x64 /p:BuildInParallel=true ^
  /p:VcpkgRoot=D:\vcpkg\ /p:VcpkgEnableManifest=true /p:VcpkgManifestInstall=false ^
  /p:VcpkgInstalledDir=D:\vcpkg\installed_scummvm\ ^
  /p:ForceImportAfterCppTargets=D:\vcpkg\scripts\buildsystems\msbuild\vcpkg.targets ^
  /v:minimal /nologo

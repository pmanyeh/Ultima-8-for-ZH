@echo off
rem Phase 0: build unmodified ScummVM (ultima engine only). Usage: p0_build.bat Debug|Release
call "C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64 >nul || exit /b 1
cd /d "D:\git\Ultima 8 for ZH\scummvm-src\build-scummvm" || exit /b 1
msbuild scummvm.sln /m /p:Configuration=%1 /p:Platform=x64 /p:PreferredToolArchitecture=x64 /p:BuildInParallel=true ^
  /p:VcpkgRoot=D:\vcpkg\ /p:VcpkgEnableManifest=true /p:VcpkgManifestInstall=false ^
  /p:VcpkgInstalledDir=D:\vcpkg\installed_scummvm\ ^
  /p:ForceImportAfterCppTargets=D:\vcpkg\scripts\buildsystems\msbuild\vcpkg.targets ^
  /v:minimal /nologo

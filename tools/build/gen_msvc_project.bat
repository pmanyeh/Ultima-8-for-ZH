@echo off
rem Phase 0: build create_project and generate MSVC solution (ultima engine only)
call "C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64 >nul || exit /b 1
set SRC=D:\git\Ultima 8 for ZH\scummvm-src
cd /d "%SRC%\devtools\create_project\cmake" || exit /b 1
cmake . || exit /b 1
cmake --build . --config Debug -j 8 || exit /b 1
if not exist "%SRC%\build-scummvm" mkdir "%SRC%\build-scummvm"
cd /d "%SRC%\build-scummvm" || exit /b 1
"%SRC%\devtools\create_project\cmake\Debug\create_project.exe" .. --msvc --vcpkg --disable-all-engines --enable-engine=ultima,ultima8 || exit /b 1
dir /b

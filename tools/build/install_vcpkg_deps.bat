@echo off
rem Phase 0: install vcpkg manifest dependencies of unmodified ScummVM (x64-windows)
call "C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64 >nul || exit /b 1
set VCPKG_ROOT=D:\vcpkg
set VCPKG_DISABLE_METRICS=1
set VCPKG_OVERLAY_PORTS=D:\git\Ultima 8 for ZH\scummvm-src\.github\vcpkg-ports
cd /d "D:\git\Ultima 8 for ZH\scummvm-src" || exit /b 1
D:\vcpkg\vcpkg.exe install --triplet x64-windows --x-install-root=D:\vcpkg\installed_scummvm

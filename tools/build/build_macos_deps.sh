#!/bin/bash
# Build SDL2 and FreeType for the macOS package into a prefix, for the
# oldest macOS the package supports. Homebrew's libraries target the macOS
# of the machine that built them, and its sdl2 is sdl2-compat, which needs
# SDL3 as well.
#
#   tools/build/build_macos_deps.sh <prefix>
#
# Needs: cmake, curl, and MACOSX_DEPLOYMENT_TARGET set (11.0 for arm64,
# 13.0 for Intel in .github/workflows/macos.yml).
set -euo pipefail

PREFIX=$(mkdir -p "$1" && cd "$1" && pwd)
: "${MACOSX_DEPLOYMENT_TARGET:?set MACOSX_DEPLOYMENT_TARGET}"
WORK="$PREFIX/src"
mkdir -p "$WORK"
cd "$WORK"

SDL2=SDL2-2.32.10
SDL2_SHA256=5f5993c530f084535c65a6879e9b26ad441169b3e25d789d83287040a9ca5165
FREETYPE=freetype-2.13.3
FREETYPE_SHA256=0550350666d427c74daeb85d5ac7bb353acba5f76956395995311a9c6f063289

fetch() {
	curl -fsSL -o "$2" "$1"
	echo "$3  $2" | shasum -a 256 -c -
	tar xf "$2"
}
fetch "https://github.com/libsdl-org/SDL/releases/download/release-2.32.10/$SDL2.tar.gz" "$SDL2.tar.gz" $SDL2_SHA256
fetch "https://download.savannah.gnu.org/releases/freetype/$FREETYPE.tar.xz" "$FREETYPE.tar.xz" $FREETYPE_SHA256

# the libraries are loaded from the bundle's Contents/libs
COMMON=(-DCMAKE_OSX_ARCHITECTURES="$(uname -m)"
	-DCMAKE_OSX_DEPLOYMENT_TARGET="$MACOSX_DEPLOYMENT_TARGET"
	-DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
	-DCMAKE_INSTALL_NAME_DIR=@executable_path/../libs
	-DCMAKE_IGNORE_PREFIX_PATH="/opt/homebrew;/usr/local")
cmake -S $SDL2 -B sdl2-build "${COMMON[@]}" -DSDL_SHARED=ON -DSDL_STATIC=OFF -DSDL_TEST=OFF
cmake --build sdl2-build -j"$(sysctl -n hw.ncpu)"
cmake --install sdl2-build
# zlib from the system; the other optional libraries aren't needed
cmake -S $FREETYPE -B freetype-build "${COMMON[@]}" -DBUILD_SHARED_LIBS=ON \
	-DFT_DISABLE_BZIP2=ON -DFT_DISABLE_PNG=ON -DFT_DISABLE_HARFBUZZ=ON -DFT_DISABLE_BROTLI=ON
cmake --build freetype-build -j"$(sysctl -n hw.ncpu)"
cmake --install freetype-build

# freetype2.pc requires zlib, which the system has without a .pc file
cat > "$PREFIX/lib/pkgconfig/zlib.pc" << EOF
Name: zlib
Description: zlib from the system
Version: 1.2.12
Libs: -lz
Cflags:
EOF
# ScummVM's configure looks for pkg-config on the PATH
ln -sf "$(command -v pkg-config)" "$PREFIX/bin/pkg-config"

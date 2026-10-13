#!/bin/bash
# Build the macOS package: ScummVM.app with the translation and the fonts,
# SDL2 and FreeType inside, and the player documents, into
# dist/Ultima8-zhTW-<version>-macOS-<arch>/ and a zip.
#
#   tools/package/make_macos_bundle.sh <version> <arch> <deps prefix>
#
# Needs: the libraries built by tools/build/build_macos_deps.sh into the
# prefix, scummvm-src configured with them and built (make),
# MACOSX_DEPLOYMENT_TARGET as for both, python3.
# Run on macOS (the GitHub Actions workflow .github/workflows/macos.yml).
set -euo pipefail

VERSION=${1:-dev}
ARCH=${2:-$(uname -m)}
DEPS=$(cd "$3" && pwd)
: "${MACOSX_DEPLOYMENT_TARGET:?set MACOSX_DEPLOYMENT_TARGET}"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
SRC="$ROOT/scummvm-src"
NAME="Ultima8-zhTW-$VERSION-macOS-$ARCH"
OUT="$ROOT/dist/$NAME"

# ScummVM's own bundle rule packs scummvm-static; use the dynamic build
cd "$SRC"
cp scummvm scummvm-static
rm -rf ScummVM.app
# the dock tile plugin, built here: ScummVM's Intel rule targets macOS
# 10.6, which current Xcode no longer links
MINOS=$MACOSX_DEPLOYMENT_TARGET
rm -rf scummvm.docktileplugin
mkdir -p scummvm.docktileplugin/Contents/MacOS
cp dists/macosx/dockplugin/Info.plist scummvm.docktileplugin/Contents/
c++ -mmacosx-version-min=$MINOS -arch "$ARCH" -O2 -bundle -framework Foundation -framework AppKit -fobjc-link-runtime backends/taskbar/macosx/dockplugin/dockplugin.m -o scummvm.docktileplugin/Contents/MacOS/ScummVMDockTilePlugin
chmod 644 scummvm.docktileplugin/Contents/MacOS/ScummVMDockTilePlugin
make bundle-pack
APP="$SRC/ScummVM.app"

# the translation (compiled fresh) and the fonts: the bundle's Resources
# are searched like the extra path
python3 "$ROOT/tools/catalog/po_compile.py" zh_TW "$ROOT/localization/zh_TW" \
	-o "$APP/Contents/Resources/u8_zh_TW.mo"
cp "$ROOT"/package/fonts/*.ttf "$APP/Contents/Resources/"
mkdir -p "$APP/Contents/Resources/licenses"
cp "$ROOT"/package/fonts/*.txt "$APP/Contents/Resources/licenses/"

# SDL2 and FreeType inside the bundle (their install names point to
# Contents/libs), then sign it again (ad hoc); --deep doesn't re-sign
# dylibs in libs/, so sign them on their own
mkdir -p "$APP/Contents/libs"
cp "$DEPS/lib/libSDL2-2.0.0.dylib" "$APP/Contents/libs/"
cp "$DEPS/lib/libfreetype.6.dylib" "$APP/Contents/libs/"
codesign -s - --force "$APP"/Contents/libs/*.dylib
codesign -s - --deep --force "$APP"
# nothing else outside the system may be linked
if otool -L "$APP/Contents/MacOS/scummvm" "$APP"/Contents/libs/*.dylib \
	| grep -vE '^/|^[[:space:]]+(/System/|/usr/lib/|@executable_path/\.\./libs/)'; then
	echo "unexpected library" >&2
	exit 1
fi

# the package
rm -rf "$OUT"
mkdir -p "$OUT"
cp -R "$APP" "$OUT/"
cp "$ROOT"/package/README.zh-TW.md "$ROOT"/package/SETTINGS.zh-TW.md \
	"$ROOT"/package/CONSOLE.zh-TW.md \
	"$ROOT"/package/LICENSES.md "$ROOT"/package/TRANSLATION_CREDITS.md \
	"$ROOT"/package/INSTALL-macOS.zh-TW.md "$OUT/"
sed -e "s/{ENGINE_COMMIT}/$(git -C "$SRC" rev-parse --short=10 HEAD)/" \
	-e "s/{MAIN_COMMIT}/$(git -C "$ROOT" rev-parse --short=10 HEAD)/" \
	"$ROOT/package/CHANGELOG.md" > "$OUT/CHANGELOG.md"
cp "$ROOT/LICENSE" "$OUT/COPYING.txt"
cd "$ROOT/dist"
rm -f "$NAME.zip"
# ditto keeps the bundle's attributes and signature
ditto -c -k --keepParent "$NAME" "$NAME.zip"
echo "package: $OUT.zip"

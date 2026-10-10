#!/bin/bash
# Build the macOS package: ScummVM.app with the translation and the fonts,
# the Homebrew libraries inside, and the player documents, into
# dist/Ultima8-zhTW-<version>-macOS-<arch>/ and a zip.
#
#   tools/package/make_macos_bundle.sh <version> <arch>
#
# Needs: scummvm-src configured and built (make), dylibbundler, python3.
# Run on macOS (the GitHub Actions workflow .github/workflows/macos.yml).
set -euo pipefail

VERSION=${1:-dev}
ARCH=${2:-$(uname -m)}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
SRC="$ROOT/scummvm-src"
NAME="Ultima8-zhTW-$VERSION-macOS-$ARCH"
OUT="$ROOT/dist/$NAME"

# ScummVM's own bundle rule packs scummvm-static; use the dynamic build
cd "$SRC"
cp scummvm scummvm-static
rm -rf ScummVM.app
make scummvm.docktileplugin
make bundle-pack
APP="$SRC/ScummVM.app"

# the translation (compiled fresh) and the fonts: the bundle's Resources
# are searched like the extra path
python3 "$ROOT/tools/catalog/po_compile.py" zh_TW "$ROOT/localization/zh_TW" \
	-o "$APP/Contents/Resources/u8_zh_TW.mo"
cp "$ROOT"/package/fonts/*.ttf "$APP/Contents/Resources/"
mkdir -p "$APP/Contents/Resources/licenses"
cp "$ROOT"/package/fonts/*.txt "$APP/Contents/Resources/licenses/"

# the Homebrew libraries inside the bundle, then sign it again (ad hoc)
dylibbundler -od -b -x "$APP/Contents/MacOS/scummvm" \
	-d "$APP/Contents/libs" -p @executable_path/../libs
codesign -s - --deep --force "$APP"

# the package
rm -rf "$OUT"
mkdir -p "$OUT"
cp -R "$APP" "$OUT/"
cp "$ROOT"/package/README.zh-TW.md "$ROOT"/package/SETTINGS.zh-TW.md \
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

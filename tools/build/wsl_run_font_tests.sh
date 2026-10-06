#!/bin/bash
# Run each test of a suite separately with a timeout and memory limit.
cd ~/u8build || exit 1
SUITE=${1:-U8FontUTF8TestSuite}
for t in $(grep -o "void test_[a-z_0-9]*" ~/u8src/test/engines/ultima/ultima8/gfx/font_utf8.h | cut -c6-); do
	out=$( (ulimit -v 2000000; timeout 10 ./test/runner "$SUITE" "$t") 2>&1 | tail -3 | tr '\n' ' ')
	echo "[$?] $t :: $out"
done

#!/bin/bash
# Build and run ScummVM unit tests (null backend, ultima8 only) in WSL.
# - VER_REV skips "git describe", which is very slow on the Windows filesystem.
# - cxxtestgen is run through python3 here: the Windows checkout has CRLF line
#   endings and its shebang asks for "python", which WSL does not provide.
cd ~/u8build || exit 1
GEN=$(make -n VER_REV=wsltest test/runner.cpp 2>/dev/null | grep cxxtestgen)
if [ -n "$GEN" ]; then
	mkdir -p test
	python3 $GEN > ~/u8gen.log 2>&1 || { echo "cxxtestgen failed"; cat ~/u8gen.log; exit 1; }
fi
make -j16 VER_REV=wsltest -o test/runner.cpp test > ~/u8test.log 2>&1
echo "EXIT=$?"
grep -E "error:|Error |FAIL|Failed|OK!|Running|tests" ~/u8test.log | tail -40

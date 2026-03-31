#!/usr/bin/env bash
set -e

PASS_COUNT=0
FAIL_COUNT=0

fail() {
  echo "FAIL: $1"
  FAIL_COUNT=$((FAIL_COUNT+1))
}

pass() {
  echo "PASS: $1"
  PASS_COUNT=$((PASS_COUNT+1))
}

cleanup() {
  cd "$(dirname "$0")"
  rm -rf testrepo
}

# Build if needed
cd "$(dirname "$0")"

if [ -f Makefile ] || [ -f makefile ]; then
  make -s 2>/dev/null || true
fi
if [ -f build.sh ]; then
  bash build.sh 2>/dev/null || true
fi
chmod +x minibudget 2>/dev/null || true

######################################
# Setup
######################################

cleanup
mkdir testrepo
cd testrepo

######################################
# Test 1: init creates directory
######################################

if ../minibudget init && [ -d .minibudget ]; then
  pass "init creates .minibudget directory"
else
  fail "init creates .minibudget directory"
fi

######################################
# Test 2: init duplicate
######################################

if ../minibudget init 2>&1 | grep -q "Already initialized"; then
  pass "init duplicate prints message"
else
  fail "init duplicate prints message"
fi

######################################
# Test 3: add transaction
######################################

if ../minibudget add Yemek 100 Gida 2>&1 | grep -q "Added: Yemek"; then
  pass "add transaction success"
else
  fail "add transaction success"
fi

######################################
# Test 4: list shows transaction
######################################

OUTPUT=$(../minibudget list 2>&1)
if echo "$OUTPUT" | grep -q "Yemek"; then
  pass "list shows transaction"
else
  fail "list shows transaction"
fi

######################################
# Test 5: unknown command
######################################

if ../minibudget hello 2>&1 | grep -q "Unknown command: hello"; then
  pass "unknown command"
else
  fail "unknown command"
fi

######################################
# Test 6: not initialized
######################################

mkdir -p ../noinit && cd ../noinit
if ../minibudget list 2>&1 | grep -q "Error: Run 'init' first"; then
  pass "not initialized error"
else
  fail "not initialized error"
fi
cd ../testrepo
rm -rf ../noinit

######################################
# Cleanup & Summary
######################################

cd ..
rm -rf testrepo

echo ""
echo "========================"
echo "PASSED: $PASS_COUNT"
echo "FAILED: $FAIL_COUNT"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo "========================"

if [ "$FAIL_COUNT" -eq 0 ]; then
  echo "ALL TESTS PASSED"
  exit 0
else
  exit 1
fi

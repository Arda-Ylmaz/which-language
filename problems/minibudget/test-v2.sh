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

if ../minibudget add Kira 5000 Ev 2>&1 | grep -q "Added: Kira"; then
  pass "add transaction success"
else
  fail "add transaction success"
fi

######################################
# Test 4: add second transaction
######################################

if ../minibudget add Yemek 100 Gida 2>&1 | grep -q "Added: Yemek"; then
  pass "add second transaction success"
else
  fail "add second transaction success"
fi

######################################
# Test 5: list shows transactions
######################################

OUTPUT=$(../minibudget list 2>&1)
if echo "$OUTPUT" | grep -q "Kira" && echo "$OUTPUT" | grep -q "Yemek"; then
  pass "list shows all transactions"
else
  fail "list shows all transactions"
fi

######################################
# Test 6: summary count
######################################

if ../minibudget summary 2>&1 | grep -q "Total transactions: 2"; then
  pass "summary shows correct count"
else
  fail "summary shows correct count"
fi

######################################
# Test 7: delete transaction
######################################

if ../minibudget delete Kira 2>&1 | grep -q "Deleted: Kira"; then
  pass "delete transaction success"
else
  fail "delete transaction success"
fi

######################################
# Test 8: delete not found
######################################

if ../minibudget delete NonExistent 2>&1 | grep -q "Error: Record not found"; then
  pass "delete not found error"
else
  fail "delete not found error"
fi

######################################
# Test 9: summary after delete
######################################

if ../minibudget summary 2>&1 | grep -q "Total transactions: 1"; then
  pass "summary updated after delete"
else
  fail "summary updated after delete"
fi

######################################
# Test 10: unknown command
######################################

if ../minibudget hello 2>&1 | grep -q "Unknown command: hello"; then
  pass "unknown command"
else
  fail "unknown command"
fi

######################################
# Test 11: not initialized
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

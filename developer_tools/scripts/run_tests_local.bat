@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
::  TEST SUITE RUNNER - CHURN INSIGHT (LOCAL)
:: ============================================================================

set API_URL=http://localhost:9999
echo [INFO] Targeting Local Environment: !API_URL!

echo.
echo ============================================================================
echo   CHURN INSIGHT - AUTOMATED TEST SUITE (LOCAL)
echo ============================================================================
echo.

echo [INFO] Starting Test Suite Execution...

echo.
set PASSED=0
set FAILED=0

:: 2. Run Python Tests
call :RunTest "local_test_graphql.py" "1. Connectivity and Schema Check (Local)"
call :RunTest "test_api_e2e.py"     "2. End-to-End Flow Login Create Query"
:: call :RunTest "verify_model_logic.py" "3. Business Logic Verification"
call :RunTest "test_validation.py"  "4. Security Validation Negative Testing"
call :RunTest "test_optimized_batch.py" "5. Batch Processing"

echo.
echo ============================================================================
echo   SUMMARY
echo ============================================================================
echo   PASSED: %PASSED%
echo   FAILED: %FAILED%
echo.

if %FAILED% equ 0 (
    echo   [SUCCESS] ALL TESTS PASSED! ROCKET READY FOR LAUNCH! 
    exit /b 0
) else (
    echo   [WARNING] SOME TESTS FAILED. CHECK LOGS ABOVE.
    exit /b 1
)

:: function to run test
:RunTest
set SCRIPT=%~1
set NAME=%~2
echo.
echo ----------------------------------------------------------------------------
echo [TEST] %NAME% (%SCRIPT%)
echo ----------------------------------------------------------------------------
if exist %SCRIPT% (
    python %SCRIPT%
    if !errorlevel! equ 0 (
        echo   [PASS] !NAME! Passed.
        set /a PASSED+=1
    ) else (
        echo   [FAIL] !NAME! Failed.
        set /a FAILED+=1
    )
) else (
    echo   [SKIP] Script %SCRIPT% not found.
)
exit /b

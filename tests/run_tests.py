#!/usr/bin/env python3
"""
Test runner script for meteoplots library.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --unit       # Run only unit tests  
    python run_tests.py --integration # Run only integration tests
    python run_tests.py --coverage   # Run with coverage report
    python run_tests.py --fast       # Skip slow tests
"""

import sys
import subprocess
import argparse


def run_tests(test_type=None, coverage=False, fast=False, verbose=False):
    """Run pytest with specified options."""
    
    cmd = ["python", "-m", "pytest"]
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=meteoplots", "--cov-report=term-missing", "--cov-report=html"])
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Filter by test type
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif fast:
        cmd.extend(["-m", "not slow"])
    
    # Add test directory
    cmd.append("tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run the tests
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main function to parse arguments and run tests."""
    
    parser = argparse.ArgumentParser(description="Run meteoplots tests")
    parser.add_argument(
        "--unit", 
        action="store_true", 
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", 
        action="store_true", 
        help="Run only integration tests"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true", 
        help="Run with coverage report"
    )
    parser.add_argument(
        "--fast", 
        action="store_true", 
        help="Skip slow tests"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Determine test type
    test_type = None
    if args.unit:
        test_type = "unit"
    elif args.integration:
        test_type = "integration"
    
    # Run tests
    exit_code = run_tests(
        test_type=test_type,
        coverage=args.coverage,
        fast=args.fast,
        verbose=args.verbose
    )
    
    # Print summary
    if exit_code == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code {exit_code}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
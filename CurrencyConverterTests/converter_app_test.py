from functools import wraps
import subprocess
import sys
import os
from typing import List, Tuple

# Define paths based on known structure
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_PATH = os.path.join(BASE_DIR, "CurrencyConverter", "app.py")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

def step(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"STEP: {func.__name__} PASSED")
        return result
    return wrapper

class ConverterAppTest:
    """
    A class to test the currency converter application by running it as a subprocess.
    """
    
    @step
    def run_currency_converter_app(self, converter: str, amount: float, currency: str) -> str:

        file_name = f"test_output_{converter}_{amount}_rsd_to_{currency}"
        # Create the directory if it doesn't exist
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, file_name + ".txt")

        result = subprocess.run([sys.executable, APP_PATH, converter, currency, str(amount), output_file],
                            capture_output=True, text=True)   
    
        # Check for successful exit
        assert result.returncode == 0, f"Process failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        # Check for expected output in stdout
        assert "Conversion result" in result.stdout, f"Missing output: {result.stdout}"

        return output_file
    
    @step
    def check_output_file_exists(self, output_file: str) -> None:
        # Check the output file was created
        assert os.path.exists(output_file), f"Missing result file: {output_file}"
    
    @step
    def get_currency_amount_from_file(self, filepath: str) -> str:
        """Reads the currency amount from a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading from file: {e}")
            raise
        
    @step
    def assert_all_file_outputs(self, currency_amount_and_converter: List[Tuple[str, str]]) -> None:
        """
        Asserts that all string values in the list of (name, string) tuples are equal.
        If not, raises an AssertionError and prints mismatching entries and full details.
        """
        if not currency_amount_and_converter:
            return  # Empty list is valid

        reference_name, reference_value = currency_amount_and_converter[0]
        mismatches = [
            (name, value) for name, value in currency_amount_and_converter
            if value != reference_value
        ]

        if mismatches:
            mismatch_report = "\n".join(
                f"{name}: '{value}' != '{reference_value}'" for name, value in mismatches
            )
            all_values_report = "\n".join(
                f"{name}: '{value}'" for name, value in currency_amount_and_converter
            )
            raise AssertionError(
                f"String mismatch detected (expected: '{reference_value}'):\n"
                f"{mismatch_report}\n\nAll values:\n{all_values_report}"
            )
        
    def assert_all_file_outputs_by_amount(self, currency_amount_and_converter: List[Tuple[str, str]]) -> None:
        """
        Asserts that all currency values are in the same currency and have equal float amounts
        (rounded to 1 decimal place). Expects strings like '8.54 EUR'.

        Parameters:
            currency_amount_and_converter: List of (name, 'amount currency') tuples.

        Raises:
            AssertionError: If currencies differ or any rounded amount differs from the reference.
        """

        def parse_value(value: str) -> Tuple[float, str]:
            try:
                amount_str, currency = value.strip().split()
                return round(float(amount_str), 1), currency.upper()
            except (ValueError, IndexError):
                raise ValueError(f"Invalid currency string format: '{value}'")

        reference_name, reference_str = currency_amount_and_converter[0]
        reference_amount, reference_currency = parse_value(reference_str)

        mismatches = []
        for name, value in currency_amount_and_converter:
            amount, currency = parse_value(value)
            if currency != reference_currency or amount != reference_amount:
                mismatches.append((name, amount, currency, value))

        if mismatches:
            mismatch_report = "\n".join(
                f"{name}: {amount} {currency} != {reference_amount} {reference_currency} (from '{original}')"
                for name, amount, currency, original in mismatches
            )
            all_values_report = "\n".join(
                f"{name}: '{value}'" for name, value in currency_amount_and_converter
            )
            raise AssertionError(
                f"Currency amount mismatch detected (expected: {reference_amount} {reference_currency}):\n"
                f"{mismatch_report}\n\nAll values:\n{all_values_report}"
            )

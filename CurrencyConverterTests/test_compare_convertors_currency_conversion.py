
import pytest
import sys
from typing import List
from converter_app_test import ConverterAppTest

# Parameters for testing
web_converters_list  = [["web_xe", 'web_gb']]
amounts = [1000, 2000, 3000]

# Define the currencies to test 
currencies = ["euro", "usd"]

@pytest.mark.web
@pytest.mark.parametrize("converters", web_converters_list )
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_web_gb_and_web_xe(converters: List[str], amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter web_xe: uses 'https://www.xe.com/'  for real-time conversion.
    Converter web_gb: uses'https://wise.com/gb/currency-converter/ for real-time conversion.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency, True)

# -------------------------------------------------------------------------------------------

# Parameters for testing
calc_converters_list = [["calc", "calc2"]]

@pytest.mark.calc
@pytest.mark.parametrize("converters", calc_converters_list)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_calc_and_calc2(converters: List[str], amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter calculator app 1: uses Windows Calculator built in currency conversion app for conversion.
    Converter calculator app 2: uses Windows Calculator to calculate currency conversion based on exchange rate.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

# -------------------------------------------------------------------------------------------

# Parameters for testing
xe_calc_converters_list  = [["web_xe", "calc"]]

@pytest.mark.xe_calc
@pytest.mark.parametrize("converters", xe_calc_converters_list )
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_xe_and_calc(converters: List[str], amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter web_xe: uses 'https://www.xe.com/'  for real-time conversion.
    Converter calculator app: uses Windows Calculator built in currency conversion app for conversion.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

# -------------------------------------------------------------------------------------------

# Parameters for testing
xe_calc2_converters_list = [["web_xe", "calc2"]]

@pytest.mark.xe_calc2
@pytest.mark.parametrize("converters", xe_calc2_converters_list)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_xe_and_calc2(converters: List[str], amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter web_xe: uses 'https://www.xe.com/'  for real-time conversion.
    Converter calculator app 2: uses Windows Calculator to calculate currency conversion based on exchange rate.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

# -------------------------------------------------------------------------------------------

# Parameters for testing
all_converters = [["web_xe", "calc", "calc2", "web_gb"]]

@pytest.mark.all_converters
@pytest.mark.parametrize("converters", all_converters)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_all_converters(converters: List[str], amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

# -------------------------------------------------------------------------------------------

# Parameters for testing
all_converters = [["web_xe", "calc", "calc2", "web_gb"]]

@pytest.mark.all_converters_amount
@pytest.mark.parametrize("converters", all_converters)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_all_converters_amount(converters: List[str], amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results (rounded to 1 decimal place) from different converters.
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency, True)

# -------------------------------------------------------------------------------------------

def compare_convertors_currency_conversion(converters: str, amount: str, currency: str, by_amount: bool = False) -> None:

    currency_amount_and_converter = []
    for converter in converters:

        print(f"Starting converter: {converter} for amount: {amount} and currency: {currency}")
        converter_app_test = ConverterAppTest()
        output_file = converter_app_test.run_currency_converter_app(converter, amount, currency)
        converter_app_test.check_output_file_exists(output_file)
        output_file = converter_app_test.get_currency_amount_from_file(output_file)
        currency_amount_and_converter.append((converter, output_file))
    
    if len(converters) > 1:
        if by_amount:
            converter_app_test.assert_all_file_outputs_by_amount(currency_amount_and_converter)
        else:
             converter_app_test.assert_all_file_outputs(currency_amount_and_converter)

if __name__ == "__main__":
   pytest.main(["-s", "-v", "-m all_converters_amount", __file__])

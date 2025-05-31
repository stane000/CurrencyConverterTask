import argparse
import asyncio

from currency_converter_interface import ICurrencyConverter
from currency_converter_calculator import CurrencyConverterCalculator
from currency_converter_calculator_v2 import CurrencyConverterCalculatorV2
from currency_converter_gb import CurrencyConverterGB
from currency_converter_xe import CurrencyConverterXE

def positive_float(value):
    try:
        value = value.replace(',', '')  # Remove thousands separators
        f = float(value)
        if f <= 0:
            raise ValueError
        return f
    except ValueError:
        raise argparse.ArgumentTypeError(f"Amount must be a positive number, got '{value}'")
    
def txt_file_path(value):
    if not value.lower().endswith('.txt'):
        raise argparse.ArgumentTypeError(f"File path must end with '.txt', got '{value}'")
    return value

def main():
    
    parser = argparse.ArgumentParser(description="Currency Converter CLI")
    parser.add_argument('converter', type=str, choices=['web_xe', 'web_gb', 'calc', 'calc2'], help='Converter to use')
    parser.add_argument('currency', type=str, choices=['euro', 'usd'], help='Target currency')
    parser.add_argument('amount', type=positive_float, help='Amount in RSD to convert')
    parser.add_argument('file_path', type=txt_file_path, help='File path to result')

    args = parser.parse_args()
    converter: ICurrencyConverter = None

    if args.converter == "web_xe":
        converter = CurrencyConverterXE()
    elif args.converter == "web_gb":
        converter = CurrencyConverterGB()  
    elif args.converter == "calc":
        converter = CurrencyConverterCalculator()
    elif args.converter == "calc2":
        converter = CurrencyConverterCalculatorV2()   

    try:
        if args.currency == 'euro':
            if args.converter == 'web_gb':
                currency_amount = asyncio.run(converter.convert_rsd_to_euro(args.amount))
            else:
                currency_amount = converter.convert_rsd_to_euro(args.amount)
        else:
            if args.converter == 'web_gb':
                currency_amount = asyncio.run(converter.convert_rsd_to_usd(args.amount))
            else:
                currency_amount = converter.convert_rsd_to_usd(args.amount)

    except Exception as ex:
        print(f"Error: {ex}")
    else:
        converter.save_currency_amount_to_file(args.file_path, currency_amount)
        print(f"Conversion result for {args.amount} RSD is: {currency_amount}")
   

if __name__ == "__main__":
    main()



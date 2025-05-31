
import requests

from currency_converter_calculator_base import CurrencyConverterCalculatorBase
from currency_converter_interface import CurrencyAmount

class CurrencyConverterCalculatorV2(CurrencyConverterCalculatorBase):
    """
    A currency converter that uses the Windows Calculator to perform currency conversions
    from Serbian Dinar (RSD) to Euro (EUR) and US Dollar (USD).

    This class fetches the latest exchange rates from a reliable API and utilizes the
    Windows Calculator application to compute the converted amounts. It ensures that
    the Calculator is properly managed by opening it for each calculation and closing
    it afterward to prevent resource leaks.
    """

    def __init__(self) -> None:
        super().__init__()

    # Public methods
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount:
        return self._convert_currency(amount, 'EUR')

    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        return self._convert_currency(amount, 'USD')
    
    # Private methods
    def _convert_currency(self, amount_rsd, currency: str):
        """
        Opens the Windows Calculator in Standard mode, inputs the multiplication expression,
        and retrieves the result.
        """
        rate = self._get_exchange_rate(currency)
        try:
 
            self._start_calculator_and_prepare()

           # Switch to Standard mode using Alt+1
            self._press_keys('%1')

            # Clear any previous input
            self._press_keys('{ESC}')

            # Type the amount in RSD
            self._press_keys(f"{amount_rsd}")

            # Press multiplication operator
            self._press_keys('*', delay=0.1)

            # Type the exchange rate
            self._press_keys(f"{rate}")

            # Press Enter to calculate the result
            self._press_keys('{ENTER}', delay=1)

            # Retrieve the result from the Calculator's display
            result_element = self.calc.child_window(auto_id='CalculatorResults', control_type='Text')
            result_text = result_element.window_text().split(" ")[-1].replace(",", "")  
            return CurrencyAmount(float(result_text), currency.upper())
        
        except Exception as e:
            print(f"Error interacting with Calculator: {e}")
            return None
        finally:
            self._close_calculator()

    def _get_exchange_rate(self, currency: str = 'EUR') -> float:
        """
        Fetches the latest RSD to EUR exchange rate from a reliable API.
        """
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/RSD")
            data = response.json()
            rate = data['rates'][currency]
            return rate
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return None
    
if __name__ == "__main__":
    converter = CurrencyConverterCalculatorV2()
    
    # Example usage
    amount_rsd = 105000  # Amount in RSD
    #euro_result = converter.convert_rsd_to_euro(amount_rsd)
    usd_result = converter.convert_rsd_to_usd(amount_rsd)
    
    #print(f"{amount_rsd} RSD is equivalent to {euro_result} EUR")
    print(f"{amount_rsd} RSD is equivalent to {usd_result} USD")
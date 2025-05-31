import time

from currency_converter_calculator_base import CurrencyConverterCalculatorBase
from currency_converter_interface import CurrencyAmount

class CurrencyConverterCalculator(CurrencyConverterCalculatorBase):
    """
    A class to convert RSD to Euro or USD using the Windows Calculator built-in currency conversion
    Requires language settings to be set to English
    """
    
    def __init__(self) -> None:
        super().__init__()

    # Public methods
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount:
        self._start_calculator_and_prepare()
        return self._convert_currency(amount, "EUR")

    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        self._start_calculator_and_prepare()
        return self._convert_currency(amount, 'USD')

    # Private methods
    def _convert_currency(self, amount: float, target_currency: str) -> CurrencyAmount:
    
        try:
                
            # Switch to Currency mode
            self._press_keys('%H')
            self._press_keys('{DOWN 5}')
            self._press_keys('{ENTER}', delay=1)

            # Enter amount
            self._press_keys(str(int(amount)))

            # Set convert from
            self._press_keys('{TAB}')
            self._press_keys('{ENTER}')
            self._press_keys('ser')
            self._press_keys('{ENTER}', delay=1)

            # Set convert to
            self._press_keys('{TAB}')
            self._press_keys('{TAB}')
            self._press_keys('{ENTER}')

            if target_currency.upper() == "USD":
                result_elem = "" 
                timeout = 30
                start_time = time.time()
                while "United States Dollar" not in result_elem:
                    if time.time() - start_time > timeout:
                        raise TimeoutError("Timeout while waiting for 'United States Dollar' to appear.")
                    self._press_keys("united")
                    self._press_keys('{ENTER}')
                    result_elem = self.calc.child_window(auto_id='Value2', control_type='Text').window_text()
                    self._press_keys('{ENTER}')
            else:
                self._press_keys(target_currency)

            self._press_keys('{ENTER}')

            # Read result from Value2
            result_elem = self.calc.child_window(auto_id='Value2', control_type='Text')
            result_text = result_elem.window_text().split(" ")[2].replace(",", "")
            return CurrencyAmount(float(result_text), target_currency.upper())
        
        except Exception as e:
                print(f"Error interacting with Calculator: {e}")
                return None
        finally:
            self._close_calculator()

# Usage
if __name__ == "__main__":
    converter = CurrencyConverterCalculator()
    print("Converted to Euro:", converter.convert_rsd_to_euro(105000))
    print("Converted to USD:", converter.convert_rsd_to_usd(105000))

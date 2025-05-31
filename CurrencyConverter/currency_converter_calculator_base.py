import time
from typing import Optional
import psutil
from pywinauto import Application

from currency_converter_interface import CurrencyAmount, ICurrencyConverter

class CurrencyConverterCalculatorBase(ICurrencyConverter):
    """
    A base class for converting RSD to Euro or USD using the Windows Calculator app.
    """

    app: Optional[Application]
    calc: Optional[Application.window]

    def __init__(self) -> None:
        self.app = None
        self.calc = None
    
    # Public methods
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount: ...
    
    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount: ...

    # Private methods   
    def _press_keys(self, keys: str, delay: float = 0.5) -> None:
        """
        Presses the specified keys in the Calculator application and waits for a short delay.
        """
        self.calc.type_keys(keys)
        time.sleep(delay)

    def _kill_existing_calculator(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if "calculator" in str(proc.info['name']).lower():
                proc.kill()

    def _start_calculator_and_prepare(self):
        self._kill_existing_calculator()
        time.sleep(1)
        self.app = Application(backend="uia").start("calc.exe")
        time.sleep(2)
        self.app.connect(best_match='Calculator')
        self.calc = self.app.window(best_match='Calculator')
        self.calc.wait('visible', timeout=10)
        time.sleep(0.5)

    def _close_calculator(self):
        if self.app:
            try:
                self.app.kill()
                self.app = None
            except Exception as e:
                print(f"Error closing Calculator: {e}")
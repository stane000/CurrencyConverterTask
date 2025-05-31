
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class CurrencyAmount:
    amount: float
    currency: str

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

class ICurrencyConverter(ABC):
    
    @abstractmethod
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount: ...
    
    @abstractmethod
    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount: ...

    def save_currency_amount_to_file(self, filepath: str, currency_amount: CurrencyAmount) -> None:
        """Saves the currency amount to a file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(str(currency_amount))
        except Exception as e:
            print(f"Error saving to file: {e}")

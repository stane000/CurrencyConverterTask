
from time import sleep
from playwright.sync_api import sync_playwright
from currency_converter_interface import CurrencyAmount, ICurrencyConverter

class CurrencyConverterXE(ICurrencyConverter):
    """
    The CurrencyConverter class automates real-time currency conversion using exchange rates 
    fetched from 'https://www.xe.com/' via Playwright. 
    It is designed specifically to convert amounts from Serbian Dinar (RSD) to:

    Euro (EUR)

    US Dollar (USD)

    """

    def __init__(self) -> None:
        super().__init__()

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    # Public methods
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount:
        return self._convert_currency(amount, "EUR")

    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        return self._convert_currency(amount, "USD")
    
    # Private methods
    def _convert_currency(self, amount: str, to_currency: str) -> CurrencyAmount:
 
        # open page
        self.page.goto("https://www.xe.com/")

        # Accept cookies if shown
        try:
            self.page.click("text=Accept", timeout=3000)
        except:
            pass
        
        sleep(1)
        # Fill amount to convert
        self.page.press("#amount", "Control+A")
        self.page.press("#amount", "Backspace")
        self.page.fill("#amount", str(amount))

        # Select "From" currency
        input_selector = 'input[placeholder="Type to search..."]'
        self.page.click(input_selector)
        self.page.type(input_selector, "rsd")
        sleep(1)
        self.page.press(input_selector, "Enter")
    
        # Select "To" currency
        to_input = 'input[aria-describedby="midmarketToCurrency-current-selection"]'
        self.page.click(to_input)
        self.page.type(to_input, to_currency.lower())
        sleep(1)
        self.page.press(to_input, "Enter")
        
        # Convert
        sleep(1)
        self.page.click('button:has-text("Convert")')
        
        # Wait for results
        sleep(1)
        result_value = self.page.text_content('p.sc-708e65be-1.chuBHG')

        self.close()
        sleep(1)
        return CurrencyAmount(float(result_value.split(" ")[0].replace(",","")), to_currency)
    
    def close(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()

# Example usage
if __name__ == "__main__":
    converter = CurrencyConverterXE()
    eur_result = converter.convert_rsd_to_euro(1000)
    print(eur_result)

    usd_result = converter.convert_rsd_to_usd(1000)
    print(usd_result)

    converter.close()
    
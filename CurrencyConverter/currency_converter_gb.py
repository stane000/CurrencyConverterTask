
import asyncio
from time import sleep
from playwright.async_api import async_playwright

from currency_converter_interface import CurrencyAmount, ICurrencyConverter

class CurrencyConverterGB(ICurrencyConverter):
    """
    The CurrencyConverter class automates real-time currency conversion using exchange rates 
    fetched from 'https://wise.com/gb/currency-converter/' via Playwright. 
    It is designed specifically to convert amounts from Serbian Dinar (RSD) to:

    Euro (EUR)

    US Dollar (USD)

    """

    def __init__(self):
        super().__init__()

    # Public methods
    async def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount:
        return await self._convert_currency(amount, "EUR")

    async def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        return await self._convert_currency(amount, "USD")
    
    # Private methods
    async def _convert_currency(self, amount: float, to_currency: str) -> CurrencyAmount:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://wise.com/gb/currency-converter/")

            # Accept cookies
            try:
                await page.wait_for_selector('#twcc__accept-button', timeout=5000)
                await page.click('#twcc__accept-button')
            except:
                pass

            # Input amount
            await page.wait_for_selector('#source-input')
            await page.fill('#source-input', str(amount))

            # Select RSD
            await page.click('#source-inputSelectedCurrency')
            await page.wait_for_selector('#source-inputSelectedCurrencySearch')
            await page.fill('#source-inputSelectedCurrencySearch', 'RSD')
            sleep(0.2)
            await page.keyboard.press('Enter')

            sleep(0.2)
            # Select target currency (EUR or USD)
            await page.click('#target-inputSelectedCurrency')
            await page.wait_for_selector('#target-inputSelectedCurrencySearch')
            await page.fill('#target-inputSelectedCurrencySearch', to_currency)
            sleep(0.2)
            await page.keyboard.press('Enter')

            # Wait for result
            await page.wait_for_timeout(2000)

            # Extract result
            result_value = await page.get_attribute('#target-input', 'value')

            await browser.close()

            return CurrencyAmount(float(result_value.replace(",","")), to_currency)

if __name__ == "__main__":
    # Example usage
    async def main():
        converter = CurrencyConverterGB()
        result_eur = await converter.convert_rsd_to_euro(1000)
        result_usd = await converter.convert_rsd_to_usd(1000)
        print(result_eur)
        print(result_usd)

    asyncio.run(main())

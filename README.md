Project description
========================

This project aims to convert currency from RSD (Serbian dinar) to EUR and USD using four different converters. 
Two converters use Playwright to automate web-based conversion on external sites, 
while the other two simulate conversion using the OS calculator. 
Finally, tests are implemented to compare and validate the conversion results across all methods for consistency.

Structure:

    CurrencyConverter folder:

        currency_converter_interface.py -> interface for all converters
        currency_converter_xe.py -> converter uses Playwright/'https://www.xe.com/', synchronous methods
        currency_converter_gb.py -> converter use Playwright/'https://wise.com/gb/currency-converter/', asynchronous methods
        currency_converter_calculator_base -> base class dor calculator converters
        currency_converter_calculator.py -> converter uses windows os calculator built-in currency conversion but Requires language settings to be set to English
        currency_converter_calculator_v2.py -> converter uses windows os calculator to do the conversion using the exchange rate from reliable API 
       
        app.py -> app for running any convertor buy given arguments and stores result to outout file
                  converter: choices=['web_xe', 'web_gb', 'calc', 'calc2'],
                  currency, type=str, choices=['euro', 'usd']
                  amount: type=positive_float
                  file_path: type=txt_file_path

                  example: python path..\app.py web_xe euro 1000 path..\output.txt
                 
    CurrencyConverterTests folder:

        converter_app_test.py: A class to test the currency converter application by running it as a subprocess.
        pytest.ini: store pytest markers
        test_compare_convertors_currency_conversion.py: stores tests for testing app.py
            1. test_compere_currency_amounts_web_gb_and_web_xe:
                    marker: web,
                    compares results for web_xe and web_gb converter
            2. test_compere_currency_amounts_calc_and_calc2:
                    marker: calc,
                    compares results for calc and calc2 converter
            3. test_compere_currency_amounts_xe_and_calc:
                    marker: xe_calc,
                    compares results for web_xe and calc converter
            4. test_compere_currency_amounts_xe_and_calc2:
                    marker: xe_calc2,
                    compares results for web_xe and calc2 converter
            5. test_compere_currency_amounts_all_converters:
                    marker: all_converters,
                    compares results for web_xe, calc, calc2, web_gb


How to use!!!
installation --------------------------------------------------------------------------------

    For this project it is expected that python and pip are installed on your computer. If not first install it.

    Windows!
        Run script install_my_project.bat
        This script sets up the development environment from scratch.

        Runs:
            - env_create.bat       -> Creates a new virtual environment (.venv)
            - env_packages.bat     -> Installs all required Python packages (e.g., via pip install -r requirements.txt)
            - install_playwright.bat -> Installs Playwright browsers and dependencies

    .
    Linux!
        Give script setup_project.sh permission to run
        chmod +x setup_project.sh

        Run script
        This script sets up the development environment from scratch.
        ./setup_project.sh

    --------------------------
    Purpose:
        Ensures the project is fully set up and ready for development or testing

Tests scripts for Windows ---------------------------------------------------------------------------------------

    run_web_converter_tests.bat
    -------------------------------
    Description:
        Runs tests that are marked for web-based currency converters (e.g., XE, GB/Wise).

    Runs:
        - Activates the virtual environment (venv\Scripts\activate.bat)
        - Executes: `pytest -s -m web`

    Purpose:
        Runs tests that use Playwright 

    Note:
        Ensure that browsers are installed via Playwright and internet access is available.

    ---

    run_calc_converter_tests.bat 
    --------------------------------------------------------
    Description:
        Runs tests that use local Windows Calculator for conversion.
        calc: Requires windows language to be set to English
        calc2: Requires internet connection

    Runs:
        - Activates the virtual environment
        - Executes: `pytest -s -m calc`

    Purpose:
        Verifies currency conversions using built-in calculator logic or UI automation.

    ---

    run_webxe_calc_converter_tests
    --------------------------------------------------------
    Description:
        Runs tests that use local Windows Calculator for conversion.
        calc: Requires windows language to be set to English

    Runs:
        - Activates the virtual environment
        - Executes: `pytest -s -m calc`

    Purpose:
        Verifies currency conversions using Playwright and built-in calculator logic or UI automation.

    ---

    run_webxe_calc2_converter_tests
    --------------------------------------------------------
    Description:
        Runs tests that use local Windows Calculator for conversion.
        calc2: Requires internet connection

    Runs:
        - Activates the virtual environment
        - Executes: `pytest -s -m calc`

    Purpose:
        Verifies currency conversions using Playwright and built-in calculator logic or UI automation.

    ---

    run_all_converters.bat
    ---------------------------------------------
    Description:
        Runs test with all converters, to compare currency conversion results

    Runs:
        - Activates the virtual environment
        - Executes: `pytest -s`-m all_converters

    Purpose:
        For full regression or pre-release testing across all converters.

    ---

    
    run_all_converters_amount.bat
    ---------------------------------------------
    Description:
        Runs test with all converters, to compare currency conversion results (rounded to 1 decimal place)

    Runs:
        - Activates the virtual environment
        - Executes: `pytest -s`-m all_converters_amount

    Purpose:
        For full regression or pre-release testing across all converters.

---

Tests scripts for Linux ---------------------------------------------------------------------------------------
    Give script run_web_converter_tests.sh permission to run
        chmod +x run_web_converter_tests.sh

    Run script
    ./run_web_converter_tests.sh


Marker Summary
==============
- web      → tests using `web_xe`, `web_gb`
- calc     → tests using `calc`, `calc2`
- xe_calc  → comparison between `web_xe` and `calc`
- xe_calc2 → comparison between `web_xe` and `calc2`
- all_converters -> comparison between web_xe`, `web_gb`, `calc, `calc2`

How to Add New Marked Tests:
----------------------------
- Use `@pytest.mark.<marker_name>` above your test
- Register the marker in `pytest.ini` to avoid warnings


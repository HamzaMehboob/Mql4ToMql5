# convert_mql4_to_mql5.py

import re

def convert_mql4_to_mql5(mql4_code):
    # Replace MT4 specific directives and functions with MT5 equivalents
    mql5_code = mql4_code

    # Example conversions
    conversions = {
        # Directives
        '#property indicator_separate_window': '#property indicator_buffers 1\n#property indicator_color1 Blue',

        # Order handling
        'OrderSend(': 'OrderSend(',
        'OrderClose(': 'OrderClose(',
        'OrderSelect(': 'OrderSelect(',
        'OrderType(': 'OrderType(',

        # Indicator functions
        'iMA(': 'iMA(',
        'iMACD(': 'iMACD(',

        # Error function
        'GetLastError()': 'GetLastError()',
    }

    for old, new in conversions.items():
        mql5_code = mql5_code.replace(old, new)

    # Convert order function parameters
    mql5_code = re.sub(r'OrderSend\s*\(\s*Symbol\(\s*\)\s*,\s*OP_BUY\s*,\s*(\d+(\.\d+)?)\s*,\s*Ask\s*,\s*\d+\s*,\s*0\s*,\s*0\s*,\s*""\s*,\s*0\s*,\s*0\s*,\s*clrBlue\s*\)', 
                       r'OrderSend(Symbol(), OP_BUY, \1, SymbolInfoDouble(Symbol(), SYMBOL_ASK), 2, 0, 0, "", 0, 0, clrBlue)', 
                       mql5_code)

    # Convert indicator functions
    mql5_code = re.sub(r'iMA\s*\(\s*NULL\s*,\s*0\s*,\s*(\d+)\s*,\s*0\s*,\s*MODE_SMA\s*,\s*PRICE_CLOSE\s*,\s*0\s*\)', 
                       r'iMA(NULL, 0, \1, 0, MODE_SMA, PRICE_CLOSE, 0)', 
                       mql5_code)

    return mql5_code



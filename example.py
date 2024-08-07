import convert_mql4_to_mql5

def main():
    # Load MQL4 code from file
    with open('example.mq4', 'r') as file:
        mql4_code = file.read()

    # Convert to MQL5
    mql5_code = convert_mql4_to_mql5.convert_mql4_to_mql5(mql4_code)
    
    # Save MQL5 code to file
    with open('mql5_code.mq5', 'w') as file:
        file.write(mql5_code)

    print("Conversion completed successfully!")

if __name__ == '__main__':
    main()
# Braille to Speech Example
# This example demonstrates how to convert Braille Unicode characters to speech

import sys
import os

# Add the parent directory to the path so we can import the braille module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import braille

def convert_braille_example():
    # Example Braille Unicode string (spells "hello")
    braille_string = "⠓⠑⠇⠇⠕"
    
    print("Braille string:", braille_string)
    
    # Convert Braille to text
    text = braille.brailleToText(braille_string)
    print("Converted to text:", text)
    
    # Convert Braille to speech
    print("Converting to speech...")
    braille.brailleToSpeech(braille_string)

def convert_text_example(text_to_convert):
    print("\nConverting text to Braille and back to speech:")
    print("Original text:", text_to_convert)
    
    # Convert text to Braille
    braille_text = braille.textToBraille(text_to_convert)
    print("Converted to Braille:", braille_text)
    
    # Convert Braille back to speech
    print("Converting back to speech...")
    braille.brailleToSpeech(braille_text)
    
    return braille_text

def main():
    print("Braille to Speech Converter")
    print("==========================")
    print("1. Run example with predefined Braille string")
    print("2. Convert your text to Braille and speech")
    print("3. Convert Braille characters to text and speech")
    
    choice = input("Enter your choice (1, 2, or 3): ")
    
    if choice == "1":
        convert_braille_example()
    elif choice == "2":
        user_text = input("Enter the text you want to convert to Braille: ")
        convert_text_example(user_text)
    elif choice == "3":
        braille_input = input("Enter the Braille characters (e.g., ⠓⠑⠇⠇⠕): ")
        print("\nConverting Braille to text and speech:")
        print("Braille input:", braille_input)
        
        # Convert Braille to text
        text = braille.brailleToText(braille_input)
        print("Converted to text:", text)
        
        # Convert Braille to speech
        print("Converting to speech...")
        braille.brailleToSpeech(braille_input)
    else:
        print("Invalid choice. Please run the script again.")
        return

if __name__ == "__main__":
    main()
# Braille Photo to Speech Example
# This example demonstrates how to convert Braille images to speech

import sys
import os

# Add the parent directory to the path so we can import the braille module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import braille

def convert_braille_photo_to_speech(image_path):
    """
    Convert a photo containing braille to speech
    
    Args:
        image_path (str): Path to the image file containing braille
    """
    print(f"\nProcessing braille image: {image_path}")
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
    
    try:
        # Convert image to text
        print("Converting image to text...")
        text = braille.imageToText(image_path)
        
        if not text or text.isspace():
            print("No text could be extracted from the image.")
            return
            
        print(f"Extracted text: {text}")
        
        # Convert text to speech
        print("Converting text to speech...")
        braille.textToSpeech(text)
        
        # Optionally convert to braille
        print("\nConverting text to braille representation:")
        braille_text = braille.textToBraille(text)
        print(f"Braille representation: {braille_text}")
        
    except Exception as e:
        print(f"Error processing image: {e}")

def main():
    print("Braille Photo to Speech Converter")
    print("=================================")
    
    # Check if an image path was provided as a command-line argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"Using provided image: {image_path}")
    else:
        # Use the test image in the images folder by default
        image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "test.jpeg")
        print(f"Using sample image: {image_path}")
        print("\nTo use a custom image, run this script with the image path as an argument:")
        print("python braille_photo_to_speech.py /path/to/your/image.jpeg")
    
    convert_braille_photo_to_speech(image_path)

if __name__ == "__main__":
    main()
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# # Braille to Speech Web Application
# # Flask server to connect the web UI with the Python backend

# from flask import Flask, render_template, request, jsonify, send_from_directory
# import os
# import base64
# import tempfile
# import braille
# import io
# from PIL import Image
# import numpy as np
# from pytesseract import image_to_string

# app = Flask(__name__, 
#             static_folder='web/static',
#             template_folder='web/templates')

# # ...existing code...

# # ...existing code...

# # Add Braille to Text (no speech) endpoint after app is defined
# @app.route('/api/braille-to-text', methods=['POST'])
# def api_braille_to_text():
#     """Convert Braille text to normal text and return the result (no speech)"""
#     try:
#         data = request.json
#         braille_text = data.get('braille_text', '')
#         if not braille_text:
#             return jsonify({'error': 'No Braille text provided'}), 400
#         # Convert Braille to text
#         text = braille.brailleToText(braille_text)
#         return jsonify({'text': text})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Unicode Braille image to text/speech endpoint (after app is defined)
# @app.route('/api/image-to-braille', methods=['POST'])
# def api_image_to_braille():
#     """Extract Braille Unicode from uploaded image, convert to text, and return result"""
#     try:
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image uploaded'}), 400
#         image_file = request.files['image']
#         # Read image into PIL Image
#         img = Image.open(image_file.stream)
#         # Use pytesseract to extract Unicode Braille from image
#         braille_unicode = image_to_string(img, lang=None)
#         # Convert Braille Unicode to text
#         text = braille.brailleToText(braille_unicode)
#         # Optionally, generate speech as well (reuse espeak logic)
#         with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
#             temp_filename = temp_file.name
#         os.system(f'espeak -v en-us -s 150 -p 50 "{text}" -w {temp_filename}')
#         with open(temp_filename, 'rb') as audio_file:
#             audio_data = audio_file.read()
#             audio_base64 = base64.b64encode(audio_data).decode('utf-8')
#         os.unlink(temp_filename)
#         return jsonify({
#             'braille_unicode': braille_unicode,
#             'text': text,
#             'audio_base64': audio_base64
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# # Braille to Speech Web Application
# # Flask server to connect the web UI with the Python backend

# from flask import Flask, render_template, request, jsonify, send_from_directory
# import os
# import base64
# import tempfile
# import braille
# import io
# from PIL import Image
# import numpy as np

# app = Flask(__name__, 
#             static_folder='web/static',
#             template_folder='web/templates')

# @app.route('/')
# def index():
#     """Render the main page"""
#     return render_template('index.html')

# @app.route('/api/braille-to-speech', methods=['POST'])
# def api_braille_to_speech():
#     """Convert Braille text to speech and return the result"""
#     try:
#         data = request.json
#         braille_text = data.get('braille_text', '')
        
#         if not braille_text:
#             return jsonify({'error': 'No Braille text provided'}), 400
        
#         # Convert Braille to text
#         text = braille.brailleToText(braille_text)
        
#         # Create a temporary file to store the audio
#         with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
#             temp_filename = temp_file.name

#         # Use espeak to generate speech (with improved parameters for better quality)
#         os.system(f'espeak -v en-us -s 150 -p 50 "{text}" -w {temp_filename}')

#         # Read the audio file and convert to base64
#         with open(temp_filename, 'rb') as audio_file:
#             audio_data = audio_file.read()
#             audio_base64 = base64.b64encode(audio_data).decode('utf-8')

#         # Clean up the temporary file
#         os.unlink(temp_filename)

#         return jsonify({
#             'text': text,
#             'audio_base64': audio_base64
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Image-to-Braille endpoint removed as per requirements

# @app.route('/api/text-to-braille', methods=['POST'])
# def api_text_to_braille():
#     """Convert text to Braille and return the result"""
#     try:
#         data = request.json
#         text = data.get('text', '')
        
#         if not text:
#             return jsonify({'error': 'No text provided'}), 400
        
#         # Convert text to Braille
#         braille_text = braille.textToBraille(text)
        
#         return jsonify({
#             'braille_text': braille_text
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/braille-keyboard', methods=['POST'])
# def api_braille_keyboard():
#     """Convert Braille dot pattern to character"""
#     try:
#         data = request.json
#         dot_pattern = data.get('dot_pattern', [])
        
#         if not dot_pattern or len(dot_pattern) != 6:
#             return jsonify({'error': 'Invalid dot pattern'}), 400
        
#         # Convert the dot pattern to a 2D array format
#         braille_array = [
#             [dot_pattern[0], dot_pattern[1]],
#             [dot_pattern[2], dot_pattern[3]],
#             [dot_pattern[4], dot_pattern[5]]
#         ]
        
#         # Convert the array to a character
#         character = braille.brailleToTextArray([braille_array])
        
#         return jsonify({
#             'character': character
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Braille to Speech Web Application
# Flask server to connect the web UI with the Python backend

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Braille to Speech Web Application
# Flask server to connect the web UI with the Python backend

from flask import Flask, render_template, request, jsonify
import os
import base64
import tempfile
import braille
from PIL import Image
from pytesseract import image_to_string

app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/templates')

# ----------------------
# Routes
# ----------------------

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


# 1️⃣ Braille to Speech
@app.route('/api/braille-to-speech', methods=['POST'])
def api_braille_to_speech():
    try:
        data = request.json
        braille_text = data.get('braille_text', '')

        if not braille_text:
            return jsonify({'error': 'No Braille text provided'}), 400

        text = braille.brailleToText(braille_text)

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_filename = temp_file.name

        os.system(f'espeak -v en-us -s 150 -p 50 "{text}" -w {temp_filename}')


        with open(temp_filename, 'rb') as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        os.unlink(temp_filename)

        return jsonify({'text': text, 'audio_base64': audio_base64})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 2️⃣ Text to Braille
@app.route('/api/text-to-braille', methods=['POST'])
def api_text_to_braille():
    try:
        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        braille_text = braille.textToBraille(text)
        return jsonify({'braille_text': braille_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 3️⃣ Braille Keyboard (dot pattern)
@app.route('/api/braille-keyboard', methods=['POST'])
def api_braille_keyboard():
    try:
        data = request.json
        dot_pattern = data.get('dot_pattern', [])

        if not dot_pattern or len(dot_pattern) != 6:
            return jsonify({'error': 'Invalid dot pattern'}), 400

        braille_array = [
            [dot_pattern[0], dot_pattern[1]],
            [dot_pattern[2], dot_pattern[3]],
            [dot_pattern[4], dot_pattern[5]]
        ]

        character = braille.brailleToTextArray([braille_array])
        return jsonify({'character': character})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 4️⃣ Image → Braille Unicode only
@app.route('/api/image-to-braille', methods=['POST'])
def api_image_to_braille():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        img = Image.open(image_file.stream)

        # OCR → Raw Braille Unicode
        braille_unicode = image_to_string(img, lang=None)

        return jsonify({'braille_unicode': braille_unicode})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 5️⃣ Braille Unicode → Text
@app.route('/api/braille-to-text', methods=['POST'])
def api_braille_to_text():
    try:
        data = request.json
        braille_text = data.get('braille_text', '')

        if not braille_text:
            return jsonify({'error': 'No Braille text provided'}), 400

        text = braille.brailleToText(braille_text)
        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 6️⃣ Optional Combined: Image → Text directly
@app.route('/api/image-to-text', methods=['POST'])
def api_image_to_text():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        img = Image.open(image_file.stream)

        braille_unicode = image_to_string(img, lang=None)
        text = braille.brailleToText(braille_unicode)

        return jsonify({'braille_unicode': braille_unicode, 'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ----------------------
# Main entry point
# ----------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)

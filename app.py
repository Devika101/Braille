#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import os
import base64
import tempfile
from PIL import Image
import cv2
import numpy as np
from braille import brailleToText, textToBraille, textToSpeech
import pytesseract
from gtts import gTTS
from io import BytesIO
import base64

app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/templates')


@app.route('/')
def index():
    return render_template('index.html')


# -------------------------------
# Image to Braille Unicode + Text
# -------------------------------
@app.route('/api/image-to-braille', methods=['POST'])
def api_image_to_braille():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    try:
        file = request.files["image"]
        # Save image temporarily
        temp_path = "temp_braille.jpg"
        file.save(temp_path)

        # Load image with OpenCV
        img = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)
        # Preprocess: blur, threshold
        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

        # Detect circles (dots) using HoughCircles
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                                   param1=50, param2=15, minRadius=5, maxRadius=15)

        detected = []
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                detected.append((x, y, r))

        # Group dots into Braille cells (simple grid, assumes regular spacing)
        # This is a basic demo; for real use, you need clustering and calibration
        cell_size = 50  # adjust for your image
        rows = img.shape[0] // cell_size
        cols = img.shape[1] // cell_size
        braille_text = ""
        for row in range(rows):
            for col in range(cols):
                # Find dots in this cell
                cell_dots = [d for d in detected if
                             row * cell_size <= d[1] < (row + 1) * cell_size and
                             col * cell_size <= d[0] < (col + 1) * cell_size]
                # Map dot positions to Braille pattern (very basic)
                # You need to calibrate dot positions for your setup
                pattern = [0, 0, 0, 0, 0, 0]
                for (x, y, r) in cell_dots:
                    # Estimate dot position in cell (top-left is dot 1)
                    rel_x = x - col * cell_size
                    rel_y = y - row * cell_size
                    if rel_x < cell_size / 2 and rel_y < cell_size / 3:
                        pattern[0] = 1
                    elif rel_x < cell_size / 2 and rel_y < 2 * cell_size / 3:
                        pattern[1] = 1
                    elif rel_x < cell_size / 2:
                        pattern[2] = 1
                    elif rel_y < cell_size / 3:
                        pattern[3] = 1
                    elif rel_y < 2 * cell_size / 3:
                        pattern[4] = 1
                    else:
                        pattern[5] = 1
                # Map pattern to character
                braille_map = {
                    (1,0,0,0,0,0): 'a', (1,1,0,0,0,0): 'b', (1,0,0,1,0,0): 'c',
                    (1,0,0,1,1,0): 'd', (1,0,0,0,1,0): 'e', (1,1,0,1,0,0): 'f',
                    (1,1,0,1,1,0): 'g', (1,1,0,0,1,0): 'h', (0,1,0,1,0,0): 'i',
                    (0,1,0,1,1,0): 'j', (1,0,1,0,0,0): 'k', (1,1,1,0,0,0): 'l',
                    (1,0,1,1,0,0): 'm', (1,0,1,1,1,0): 'n', (1,0,1,0,1,0): 'o',
                    (1,1,1,1,0,0): 'p', (1,1,1,1,1,0): 'q', (1,1,1,0,1,0): 'r',
                    (0,1,1,1,0,0): 's', (0,1,1,1,1,0): 't', (1,0,1,0,0,1): 'u',
                    (1,1,1,0,0,1): 'v', (0,1,0,1,1,1): 'w', (1,0,1,1,0,1): 'x',
                    (1,0,1,1,1,1): 'y', (1,0,1,0,1,1): 'z', (0,0,0,0,0,0): ' '
                }
                char = braille_map.get(tuple(pattern), '?')
                braille_text += char
            braille_text += ' '
        os.remove(temp_path)

        if not braille_text.strip() or set(braille_text) == {'?',' '}:
            return jsonify({
                "braille_unicode": "",
                "text": "",
                "audio_base64": "",
                "error": "No Braille text detected in image."
            }), 400

        # Generate audio
        tts = gTTS(text=braille_text, lang="en")
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        audio_base64 = base64.b64encode(audio_io.read()).decode("utf-8")

        return jsonify({
            "braille_unicode": braille_text,
            "text": braille_text,
            "audio_base64": audio_base64
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

        return jsonify({
            'braille_unicode': braille_unicode,
            'text': text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -------------------------------
# Text to Braille
# -------------------------------
@app.route('/api/text-to-braille', methods=['POST'])
def api_text_to_braille():
    try:
        data = request.json
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        braille_text = textToBraille(text)
        return jsonify({'braille_text': braille_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -------------------------------
# Braille to Text
# -------------------------------
@app.route('/api/braille-to-text', methods=['POST'])
def api_braille_to_text():
    try:
        data = request.json
        braille_text = data.get('braille_text', '')
        if not braille_text:
            return jsonify({'error': 'No Braille text provided'}), 400

        text = brailleToText(braille_text)
        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -------------------------------
# Braille to Speech
# -------------------------------
@app.route('/api/braille-to-speech', methods=['POST'])
def api_braille_to_speech():
    try:
        data = request.json
        braille_text = data.get('braille_text', '')
        if not braille_text:
            return jsonify({'error': 'No Braille text provided'}), 400

        text = brailleToText(braille_text)
        textToSpeech(text)

        return jsonify({'text': text, 'message': 'Speech generated'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

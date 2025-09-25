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
        if img is None:
            return jsonify({'error': 'Could not load image'}), 400
            
        print(f"Image loaded: {img.shape}")
        
        # Improved preprocessing
        # Resize image if too large for better processing
        height, width = img.shape
        if width > 800:
            scale = 800 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height))
            print(f"Resized image to: {img.shape}")
        
        # Enhanced preprocessing
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        
        # Use adaptive thresholding for better dot detection
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morphological operations to clean up the image
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        print("Preprocessing completed")

        # Improved circle detection with multiple parameter sets
        detected = []
        
        # Try different parameter sets for different dot sizes
        param_sets = [
            {'dp': 1, 'minDist': 10, 'param1': 30, 'param2': 15, 'minRadius': 3, 'maxRadius': 20},
            {'dp': 1.2, 'minDist': 15, 'param1': 50, 'param2': 20, 'minRadius': 5, 'maxRadius': 25},
            {'dp': 1.5, 'minDist': 20, 'param1': 70, 'param2': 25, 'minRadius': 8, 'maxRadius': 30}
        ]
        
        for params in param_sets:
            circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, **params)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    # Avoid duplicate detections
                    is_duplicate = False
                    for existing in detected:
                        if abs(x - existing[0]) < 10 and abs(y - existing[1]) < 10:
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        detected.append((x, y, r))
        
        print(f"Detected {len(detected)} dots")
        
        if len(detected) == 0:
            # Try alternative detection using contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if 10 < area < 500:  # Filter by area
                    (x, y), radius = cv2.minEnclosingCircle(contour)
                    if 3 < radius < 20:  # Filter by radius
                        detected.append((int(x), int(y), int(radius)))
            print(f"After contour detection: {len(detected)} dots")

        # Adaptive cell size calculation
        if len(detected) > 0:
            # Calculate average distance between dots to estimate cell size
            distances = []
            for i, dot1 in enumerate(detected):
                for dot2 in detected[i+1:]:
                    dist = np.sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)
                    if 10 < dist < 100:  # Reasonable distance range
                        distances.append(dist)
            
            if distances:
                avg_distance = np.median(distances)
                cell_size = max(30, min(80, int(avg_distance * 1.5)))  # Adaptive cell size
            else:
                cell_size = 50  # Default fallback
        else:
            cell_size = 50
            
        print(f"Using cell size: {cell_size}")
        
        # Group dots into Braille cells
        rows = (img.shape[0] + cell_size - 1) // cell_size
        cols = (img.shape[1] + cell_size - 1) // cell_size
        braille_text = ""
        
        for row in range(rows):
            row_text = ""
            for col in range(cols):
                # Find dots in this cell
                cell_dots = []
                for (x, y, r) in detected:
                    if (row * cell_size <= y < (row + 1) * cell_size and 
                        col * cell_size <= x < (col + 1) * cell_size):
                        cell_dots.append((x, y, r))
                
                # Map dot positions to Braille pattern
                pattern = [0, 0, 0, 0, 0, 0]
                for (x, y, r) in cell_dots:
                    # Calculate relative position within cell
                    rel_x = (x - col * cell_size) / cell_size
                    rel_y = (y - row * cell_size) / cell_size
                    
                    # Improved dot position mapping
                    if rel_x < 0.5 and rel_y < 0.33:
                        pattern[0] = 1  # Top-left
                    elif rel_x < 0.5 and rel_y < 0.66:
                        pattern[1] = 1  # Middle-left
                    elif rel_x < 0.5:
                        pattern[2] = 1  # Bottom-left
                    elif rel_y < 0.33:
                        pattern[3] = 1  # Top-right
                    elif rel_y < 0.66:
                        pattern[4] = 1  # Middle-right
                    else:
                        pattern[5] = 1  # Bottom-right
                
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
                row_text += char
            braille_text += row_text + ' '
        
        print(f"Detected text: '{braille_text}'")
        
        # Clean up
        os.remove(temp_path)

        if not braille_text.strip() or set(braille_text.replace(' ', '')) == {'?'}:
            return jsonify({
                "braille_unicode": "",
                "text": "",
                "audio_base64": "",
                "error": f"No Braille text detected in image. Found {len(detected)} dots but couldn't map to text."
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
        print(f"Error in image processing: {str(e)}")
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
        
        # Generate audio using gTTS
        tts = gTTS(text=text, lang="en")
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        audio_base64 = base64.b64encode(audio_io.read()).decode("utf-8")

        return jsonify({
            'text': text, 
            'message': 'Speech generated',
            'audio_base64': audio_base64
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Braille to Speech Web Application
# Flask server to connect the web UI with the Python backend

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
import tempfile
import braille
import io
from PIL import Image
import numpy as np

app = Flask(__name__, 
            static_folder='web/static',
            template_folder='web/templates')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/braille-to-speech', methods=['POST'])
def api_braille_to_speech():
    """Convert Braille text to speech and return the result"""
    try:
        data = request.json
        braille_text = data.get('braille_text', '')
        
        if not braille_text:
            return jsonify({'error': 'No Braille text provided'}), 400
        
        # Convert Braille to text
        text = braille.brailleToText(braille_text)
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        # Use espeak to generate speech (with improved parameters for better quality)
        os.system(f"espeak -v en-us -s 150 -p 50 '{text}' -w {temp_filename}")
        
        # Read the audio file and convert to base64
        with open(temp_filename, 'rb') as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Clean up the temporary file
        os.unlink(temp_filename)
        
        return jsonify({
            'text': text,
            'audio_base64': audio_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Image-to-Braille endpoint removed as per requirements

@app.route('/api/text-to-braille', methods=['POST'])
def api_text_to_braille():
    """Convert text to Braille and return the result"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Convert text to Braille
        braille_text = braille.textToBraille(text)
        
        return jsonify({
            'braille_text': braille_text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/braille-keyboard', methods=['POST'])
def api_braille_keyboard():
    """Convert Braille dot pattern to character"""
    try:
        data = request.json
        dot_pattern = data.get('dot_pattern', [])
        
        if not dot_pattern or len(dot_pattern) != 6:
            return jsonify({'error': 'Invalid dot pattern'}), 400
        
        # Convert the dot pattern to a 2D array format
        braille_array = [
            [dot_pattern[0], dot_pattern[1]],
            [dot_pattern[2], dot_pattern[3]],
            [dot_pattern[4], dot_pattern[5]]
        ]
        
        # Convert the array to a character
        character = braille.brailleToTextArray([braille_array])
        
        return jsonify({
            'character': character
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
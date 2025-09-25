#!/usr/bin/env python3
# Test script for braille detection

import cv2
import numpy as np
import os

def test_braille_detection(image_path):
    """Test the improved braille detection on a sample image"""
    print(f"Testing image: {image_path}")
    
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Could not load image: {image_path}")
        return
    
    print(f"Image shape: {img.shape}")
    
    # Resize if too large
    height, width = img.shape
    if width > 800:
        scale = 800 / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height))
        print(f"Resized to: {img.shape}")
    
    # Enhanced preprocessing
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations
    kernel = np.ones((2,2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Save processed image for debugging
    processed_path = image_path.replace('.png', '_processed.png')
    cv2.imwrite(processed_path, thresh)
    print(f"Saved processed image: {processed_path}")
    
    # Circle detection
    detected = []
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
                is_duplicate = False
                for existing in detected:
                    if abs(x - existing[0]) < 10 and abs(y - existing[1]) < 10:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    detected.append((x, y, r))
    
    print(f"Detected {len(detected)} dots")
    
    # Contour detection as fallback
    if len(detected) == 0:
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if 10 < area < 500:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                if 3 < radius < 20:
                    detected.append((int(x), int(y), int(radius)))
        print(f"After contour detection: {len(detected)} dots")
    
    # Create visualization
    vis_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for (x, y, r) in detected:
        cv2.circle(vis_img, (x, y), r, (0, 255, 0), 2)
        cv2.circle(vis_img, (x, y), 2, (0, 0, 255), -1)
    
    # Save visualization
    vis_path = image_path.replace('.png', '_detected.png')
    cv2.imwrite(vis_path, vis_img)
    print(f"Saved detection visualization: {vis_path}")
    
    return len(detected)

if __name__ == "__main__":
    # Test with sample images
    test_images = [
        "images/a.png",
        "images/test.jpg", 
        "images/test.jpeg",
        "images/a_dots.png"
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            dots = test_braille_detection(img_path)
            print(f"Result: {dots} dots detected\n")
        else:
            print(f"Image not found: {img_path}\n")

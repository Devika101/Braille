// Braille to Speech Converter - JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initBrailleKeyboard();
    initWaveform();
    initEventListeners();
    
    // Add futuristic UI effects
    addUIEffects();
});

// Global variables
let currentBrailleDots = [0, 0, 0, 0, 0, 0]; // 6-dot pattern (0 = inactive, 1 = active)
let wavesurfer;
let audioBlob = null;

// Initialize Braille keyboard functionality
function initBrailleKeyboard() {
    const dots = document.querySelectorAll('.braille-dot');
    const addCharBtn = document.getElementById('add-character');
    const clearKeyboardBtn = document.getElementById('clear-keyboard');
    const currentCharDisplay = document.getElementById('current-char');
    
    // Add click event to each dot
    dots.forEach(dot => {
        dot.addEventListener('click', function() {
            // Toggle dot active state
            this.classList.toggle('active');
            
            // Update current Braille pattern
            const position = parseInt(this.getAttribute('data-position'));
            currentBrailleDots[position-1] = this.classList.contains('active') ? 1 : 0;
            
            // Update current character display
            updateCurrentCharacterDisplay();
        });
    });
    
    // Add character button
    addCharBtn.addEventListener('click', function() {
        const brailleInput = document.getElementById('braille-input');
        const character = getBrailleCharacter();
        
        if (character) {
            brailleInput.value += character;
            clearBrailleKeyboard();
            
            // Add futuristic effect
            addCharBtn.classList.add('button-pulse');
            setTimeout(() => {
                addCharBtn.classList.remove('button-pulse');
            }, 300);
        }
    });
    
    // Clear keyboard button
    clearKeyboardBtn.addEventListener('click', function() {
        clearBrailleKeyboard();
        
        // Add futuristic effect
        clearKeyboardBtn.classList.add('button-pulse');
        setTimeout(() => {
            clearKeyboardBtn.classList.remove('button-pulse');
        }, 300);
    });
}

// Update the current character display based on active dots
function updateCurrentCharacterDisplay() {
    const currentCharDisplay = document.getElementById('current-char');
    const character = getBrailleCharacter();
    
    if (character) {
        currentCharDisplay.textContent = character;
    } else {
        currentCharDisplay.textContent = 'None';
    }
}

// Get the Braille character based on active dots
function getBrailleCharacter() {
    // This is a simplified mapping of Braille patterns to characters
    // In a real application, this would be more comprehensive
    const brailleMap = {
        '100000': 'a',
        '110000': 'b',
        '100100': 'c',
        '100110': 'd',
        '100010': 'e',
        '110100': 'f',
        '110110': 'g',
        '110010': 'h',
        '010100': 'i',
        '010110': 'j',
        '101000': 'k',
        '111000': 'l',
        '101100': 'm',
        '101110': 'n',
        '101010': 'o',
        '111100': 'p',
        '111110': 'q',
        '111010': 'r',
        '011100': 's',
        '011110': 't',
        '101001': 'u',
        '111001': 'v',
        '010111': 'w',
        '101101': 'x',
        '101111': 'y',
        '101011': 'z',
        '000000': ' '
    };
    
    const pattern = currentBrailleDots.join('');
    return brailleMap[pattern] || null;
}

// Clear the Braille keyboard
function clearBrailleKeyboard() {
    const dots = document.querySelectorAll('.braille-dot');
    dots.forEach(dot => {
        dot.classList.remove('active');
    });
    
    currentBrailleDots = [0, 0, 0, 0, 0, 0];
    updateCurrentCharacterDisplay();
}

// Initialize waveform visualization
function initWaveform() {
    wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: 'rgba(230, 0, 255, 0.3)',
        progressColor: 'rgba(230, 0, 255, 0.8)',
        cursorColor: '#ffffff',
        barWidth: 2,
        barRadius: 3,
        cursorWidth: 1,
        height: 128,
        barGap: 3,
        responsive: true
    });
    
    // Add audio controls functionality
    document.getElementById('play-btn').addEventListener('click', function() {
        wavesurfer.play();
    });
    
    document.getElementById('pause-btn').addEventListener('click', function() {
        wavesurfer.pause();
    });
    
    document.getElementById('stop-btn').addEventListener('click', function() {
        wavesurfer.stop();
    });
    
    // Add waveform events
    wavesurfer.on('ready', function() {
        console.log('Waveform ready');
    });
    
    wavesurfer.on('finish', function() {
        console.log('Finished playing');
    });
}

// Initialize event listeners for main functionality
function initEventListeners() {
    const convertBtn = document.getElementById('convert-btn');
    const clearBtn = document.getElementById('clear-btn');
    
    // Convert button
    convertBtn.addEventListener('click', function() {
        const brailleInput = document.getElementById('braille-input').value.trim();
        
        if (brailleInput) {
            // Add button press effect
            convertBtn.classList.add('button-press');
            setTimeout(() => {
                convertBtn.classList.remove('button-press');
            }, 300);
            
            // Convert Braille to speech
            convertBrailleToSpeech(brailleInput);
        }
    });
    
    // Clear button
    clearBtn.addEventListener('click', function() {
        document.getElementById('braille-input').value = '';
        document.getElementById('text-output').textContent = '';
        wavesurfer.empty();
        audioBlob = null;
        
        // Add button press effect
        clearBtn.classList.add('button-press');
        setTimeout(() => {
            clearBtn.classList.remove('button-press');
        }, 300);
    });
}

// Convert Braille to speech using the backend API
async function convertBrailleToSpeech(brailleText) {
    try {
        // Show loading state
        showLoadingState(true);
        
        // Make API call to backend
        const response = await fetch('/api/braille-to-speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ braille_text: brailleText })
        });
        
        if (!response.ok) {
            throw new Error('Failed to convert Braille to speech');
        }
        
        const data = await response.json();
        
        // Update text output
        document.getElementById('text-output').textContent = data.text;
        
        // Load audio if available
        if (data.audio_base64) {
            loadAudioFromBase64(data.audio_base64);
        }
        
        // Add success effect
        addSuccessEffect();
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        // Hide loading state
        showLoadingState(false);
    }
}

// Image processing functionality removed as per requirements

// Load audio from base64 string
function loadAudioFromBase64(base64Data) {
    // Convert base64 to blob
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    audioBlob = new Blob([byteArray], { type: 'audio/wav' });
    
    // Load audio into waveform
    const audioUrl = URL.createObjectURL(audioBlob);
    wavesurfer.load(audioUrl);
    
    // Animate waveform
    animateWaveform();
}

// Show loading state
function showLoadingState(isLoading) {
    const convertBtn = document.getElementById('convert-btn');
    
    if (isLoading) {
        convertBtn.disabled = true;
        convertBtn.innerHTML = '<span class="btn-text">Processing...</span><i class="fas fa-spinner fa-spin"></i>';
    } else {
        convertBtn.disabled = false;
        convertBtn.innerHTML = '<span class="btn-text">Convert to Speech</span><i class="fas fa-volume-up"></i>';
    }
}

// Show error message
function showError(message) {
    // Create error notification
    const notification = document.createElement('div');
    notification.className = 'error-notification';
    notification.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 5000);
}

// Add success effect
function addSuccessEffect() {
    const outputSection = document.querySelector('.output-section');
    outputSection.classList.add('success-pulse');
    
    setTimeout(() => {
        outputSection.classList.remove('success-pulse');
    }, 1000);
}

// Animate waveform
function animateWaveform() {
    const waveformContainer = document.querySelector('.waveform-container');
    waveformContainer.classList.add('waveform-animate');
    
    setTimeout(() => {
        waveformContainer.classList.remove('waveform-animate');
    }, 1000);
}

// Add UI effects
function addUIEffects() {
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-3px)';
        });
        
        button.addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add parallax effect to decorative elements
    document.addEventListener('mousemove', function(e) {
        const shapes = document.querySelectorAll('.geometric-shape');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            const depth = (index + 1) * 10;
            const moveX = (mouseX - 0.5) * depth;
            const moveY = (mouseY - 0.5) * depth;
            
            shape.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });
    
    // Add glow effect to input on focus
    const brailleInput = document.getElementById('braille-input');
    brailleInput.addEventListener('focus', function() {
        this.parentElement.classList.add('input-focus');
    });
    
    brailleInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('input-focus');
    });
}

// Add CSS for dynamic effects
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .button-pulse {
            animation: buttonPulse 0.3s ease;
        }
        
        .button-press {
            transform: scale(0.95) !important;
            box-shadow: 0 0 5px rgba(230, 0, 255, 0.5) !important;
        }
        
        .input-focus {
            box-shadow: 0 0 20px rgba(230, 0, 255, 0.7), 0 0 40px rgba(230, 0, 255, 0.4) !important;
        }
        
        .success-pulse {
            animation: successPulse 1s ease;
        }
        
        .waveform-animate {
            animation: waveformAnimate 1s ease;
        }
        
        .error-notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: rgba(255, 0, 0, 0.8);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: fadeIn 0.5s ease;
        }
        
        .fade-out {
            animation: fadeOut 0.5s ease forwards;
        }
        
        @keyframes buttonPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        @keyframes successPulse {
            0% { box-shadow: 0 0 5px rgba(230, 0, 255, 0.5); }
            50% { box-shadow: 0 0 20px rgba(230, 0, 255, 0.8), 0 0 40px rgba(230, 0, 255, 0.4); }
            100% { box-shadow: 0 0 5px rgba(230, 0, 255, 0.5); }
        }
        
        @keyframes waveformAnimate {
            0% { background-color: rgba(10, 10, 15, 0.5); }
            50% { background-color: rgba(230, 0, 255, 0.2); }
            100% { background-color: rgba(10, 10, 15, 0.5); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(20px); }
        }
    `;
    
    document.head.appendChild(style);
}

// Call to add dynamic styles
addDynamicStyles();
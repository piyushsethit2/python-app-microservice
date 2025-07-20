#!/usr/bin/env python3
"""
Python App Microservice for Malicious URL Detection
Simple Flask service for local testing
"""

from flask import Flask, request, jsonify
import logging
import os
import re
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple patterns for URL analysis
SUSPICIOUS_PATTERNS = [
    r'(?i)(malware|virus|trojan|spyware|phishing|scam|fake|hack|crack|warez|keygen|nulled)',
    r'(?i)\.(exe|bat|cmd|com|pif|scr|vbs|js|jar|msi|dmg|app|deb|rpm|apk|ipa)$',
    r'(?i)(bit\.ly|goo\.gl|tinyurl|is\.gd|t\.co|fb\.me|ow\.ly|su\.pr|twurl|snipurl)',
    r'(?i)(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.|0\.|169\.254\.)'
]

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'python-app-microservice',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/detect', methods=['POST'])
def detect():
    """URL detection endpoint"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Simple detection logic
        confidence = 0.0
        issues = []
        
        # Check for suspicious patterns
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, url):
                issues.append(f"Matched pattern: {pattern}")
                confidence += 0.2
        
        # Check for suspicious keywords
        suspicious_keywords = ['malware', 'virus', 'trojan', 'spyware', 'phishing', 'scam', 'fake', 'hack']
        for keyword in suspicious_keywords:
            if keyword.lower() in url.lower():
                issues.append(f"Contains suspicious keyword: {keyword}")
                confidence += 0.1
        
        # Determine if malicious
        is_malicious = confidence > 0.3
        confidence = min(confidence, 1.0)
        
        result = {
            'url': url,
            'is_malicious': is_malicious,
            'confidence': confidence,
            'issues': issues,
            'method': 'Python App Microservice',
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Detection result for {url}: malicious={is_malicious}, confidence={confidence}")
        return jsonify(result)
            
    except Exception as e:
        logger.error(f"Error in detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Python App Microservice',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'detect': '/detect'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    logger.info(f"Starting Python App Microservice on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 
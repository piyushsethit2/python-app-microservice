#!/usr/bin/env python3
"""
Python App Microservice for Malicious URL Detection
Optimized lightweight Flask service for production
"""

from flask import Flask, request, jsonify
import logging
import sys
import os
import re
from datetime import datetime

# Enhanced logging configuration for Render visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)  # Also log to stderr for better visibility
    ],
    force=True  # Force reconfiguration
)

logger = logging.getLogger(__name__)

# Log startup information
logger.info("=== Python App Microservice Starting ===")
logger.info("Service: URL detection microservice")
logger.info("Version: 1.0.0")
logger.info("Environment: Production")
logger.info("Features: URL pattern analysis, lightweight detection")
logger.info("Logging: Enhanced for Render visibility")
logger.info("================================================")

app = Flask(__name__)

# Configure Flask logging
app.logger.setLevel(logging.INFO)
app.logger.handlers = logger.handlers

# Optimized patterns for URL analysis (reduced for faster processing)
SUSPICIOUS_PATTERNS = [
    r'(?i)(malware|virus|trojan|spyware|phishing|scam|fake|hack)',
    r'(?i)\.(exe|bat|cmd|com|pif|scr|vbs|js|jar|msi|dmg|app)$',
    r'(?i)(bit\.ly|goo\.gl|tinyurl|is\.gd|t\.co)',
    r'(?i)(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.)'
]

@app.route('/health', methods=['GET'])
def health_check():
    """Fast health check endpoint for monitoring"""
    logger.info("Health check endpoint called")
    try:
        health_status = {
            "status": "UP",
            "service": "Python App Microservice",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "/detect": "POST - URL detection endpoint",
                "/health": "GET - Health check endpoint"
            }
        }
        
        logger.info("Health check passed successfully")
        app.logger.info("Health check passed successfully")
        return jsonify(health_status), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        app.logger.error(f"Health check failed: {str(e)}")
        health_status = {
            "status": "DOWN",
            "service": "Python App Microservice",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        return jsonify(health_status), 503

@app.route('/detect', methods=['POST'])
def detect():
    """Optimized URL detection endpoint"""
    logger.info("Detection endpoint called")
    app.logger.info("Detection endpoint called")
    
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        logger.info(f"Processing URL: {url}")
        app.logger.info(f"Processing URL: {url}")
        
        if not url:
            logger.warning("Empty URL provided")
            app.logger.warning("Empty URL provided")
            return jsonify({'error': 'URL is required'}), 400
        
        # Fast detection logic
        confidence = 0.0
        issues = []
        
        logger.info("Starting pattern analysis")
        
        # Quick pattern check
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, url):
                issues.append(f"Matched pattern: {pattern}")
                confidence += 0.2
                logger.info(f"Pattern matched: {pattern}")
        
        # Quick keyword check
        suspicious_keywords = ['malware', 'virus', 'trojan', 'spyware', 'phishing', 'scam', 'fake', 'hack']
        for keyword in suspicious_keywords:
            if keyword.lower() in url.lower():
                issues.append(f"Contains suspicious keyword: {keyword}")
                confidence += 0.1
                logger.info(f"Keyword found: {keyword}")
        
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
        
        logger.info(f"Detection result for {url}: malicious={is_malicious}, confidence={confidence}, issues={len(issues)}")
        app.logger.info(f"Detection result for {url}: malicious={is_malicious}, confidence={confidence}, issues={len(issues)}")
        
        return jsonify(result)
            
    except Exception as e:
        logger.error(f"Error in detection: {str(e)}")
        app.logger.error(f"Error in detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    logger.info("Root endpoint called")
    app.logger.info("Root endpoint called")
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
    app.logger.info(f"Starting Python App Microservice on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True) 
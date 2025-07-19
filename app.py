"""
Flask Application for ML Microservice
Main application file for the URL classification service
"""
import logging
from flask import Flask, request, jsonify
from .config import Config
from .model_manager import ModelManager

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize model manager
model_manager = ModelManager()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ml-microservice",
        "model_loaded": model_manager.is_loaded()
    })

@app.route('/info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        "service": "ml-microservice",
        "model_info": model_manager.get_model_info(),
        "config": {
            "host": Config.HOST,
            "port": Config.PORT,
            "timeout": Config.TIMEOUT
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if URL is malicious"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "error": "Missing 'url' in request body"
            }), 400
        
        url = data['url']
        
        if not url or not isinstance(url, str):
            return jsonify({
                "error": "Invalid URL provided"
            }), 400
        
        # Get prediction
        label, confidence = model_manager.predict(url)
        
        logger.info(f"Prediction for {url}: {label} (confidence: {confidence:.3f})")
        
        return jsonify({
            "url": url,
            "prediction": label,
            "confidence": confidence,
            "model": model_manager.model_name
        })
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/reload', methods=['POST'])
def reload_model():
    """Reload the model with new configuration"""
    try:
        data = request.get_json() or {}
        model_name = data.get('model_name', Config.get_model_name())
        
        success = model_manager.load_model(model_name)
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Model reloaded: {model_name}",
                "model_info": model_manager.get_model_info()
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Failed to load model: {model_name}"
            }), 500
            
    except Exception as e:
        logger.error(f"Error reloading model: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

def create_app():
    """Application factory"""
    # Load model on startup
    if not model_manager.load_model():
        logger.error("Failed to load model on startup")
    
    return app

if __name__ == '__main__':
    # Load model
    if not model_manager.load_model():
        logger.error("Failed to load model")
        exit(1)
    
    # Get server config
    server_config = Config.get_server_config()
    
    logger.info(f"Starting ML microservice on {server_config['host']}:{server_config['port']}")
    logger.info(f"Model: {model_manager.model_name}")
    logger.info(f"Device: {model_manager.device}")
    
    # Run the app
    app.run(
        host=server_config['host'],
        port=server_config['port'],
        debug=server_config['debug']
    ) 
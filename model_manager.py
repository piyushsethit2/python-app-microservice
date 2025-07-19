"""
Model Manager for ML Microservice
Handles model loading, prediction, and model management
"""
import logging
from typing import Dict, Any, Tuple
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import Config

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages the ML model for URL classification"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self.model_name = None
        
    def load_model(self, model_name: str = None) -> bool:
        """
        Load the model and tokenizer
        
        Args:
            model_name: HuggingFace model name
            
        Returns:
            bool: True if model loaded successfully
        """
        try:
            if model_name is None:
                model_name = Config.get_model_name()
            
            self.device = Config.get_device()
            self.model_name = model_name
            
            logger.info(f"Loading model: {model_name} on device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Load model
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=2  # binary classification: safe/malicious
            )
            
            # Move to device
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded successfully: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            
            # Fallback to default model
            if model_name != 'distilbert-base-uncased':
                logger.info("Falling back to: distilbert-base-uncased")
                return self.load_model('distilbert-base-uncased')
            
            return False
    
    def predict(self, url: str) -> Tuple[str, float]:
        """
        Predict if URL is malicious or safe
        
        Args:
            url: URL to classify
            
        Returns:
            Tuple[str, float]: (label, confidence)
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded")
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                url,
                truncation=True,
                padding=True,
                max_length=Config.MAX_LENGTH,
                return_tensors="pt"
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
                
            # Get prediction and confidence
            prediction = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][prediction].item()
            
            # Map prediction to label
            label = "malicious" if prediction == 1 else "safe"
            
            return label, confidence
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "max_length": Config.MAX_LENGTH,
            "loaded": self.model is not None
        }
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.tokenizer is not None 
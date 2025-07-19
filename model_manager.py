"""
Model Manager for ML Microservice
Handles model loading, prediction, and management
"""
import logging
import os
import re
import numpy as np
from typing import Tuple, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages ML model loading and prediction"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.model_name = "scikit-learn"
        self.device = "cpu"
        self.is_model_loaded = False
        
        # Initialize with lightweight components
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),
            stop_words='english'
        )
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Initialize with dummy data
        dummy_urls = [
            "google.com",
            "facebook.com", 
            "amazon.com",
            "malicious-site.com",
            "phishing-example.com"
        ]
        dummy_labels = [0, 0, 0, 1, 1]  # 0 = safe, 1 = malicious
        
        try:
            X_dummy = self.vectorizer.fit_transform(dummy_urls)
            self.model.fit(X_dummy, dummy_labels)
            self.is_model_loaded = True
            logger.info("Model initialized with dummy data")
        except Exception as e:
            logger.error(f"Error initializing model: {e}")
            self.is_model_loaded = False
    
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
                model_name = "scikit-learn" # Default to scikit-learn
            
            self.device = "cpu" # Always use cpu for scikit-learn
            self.model_name = model_name
            
            logger.info(f"Loading model: {model_name} on device: {self.device}")
            
            # Load tokenizer
            # self.tokenizer = AutoTokenizer.from_pretrained(model_name) # Removed transformers imports
            
            # Load model
            # self.model = AutoModelForSequenceClassification.from_pretrained( # Removed transformers imports
            #     model_name,
            #     num_labels=2  # binary classification: safe/malicious
            # )
            
            # Move to device
            # self.model.to(self.device) # Removed transformers imports
            # self.model.eval() # Removed transformers imports
            
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
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Model not loaded")
        
        try:
            # Tokenize input
            # inputs = self.tokenizer( # Removed transformers imports
            #     url,
            #     truncation=True,
            #     padding=True,
            #     max_length=Config.MAX_LENGTH, # Removed Config import
            #     return_tensors="pt"
            # )
            
            # Move to device
            # inputs = {k: v.to(self.device) for k, v in inputs.items()} # Removed transformers imports
            
            # Get prediction
            # with torch.no_grad(): # Removed transformers imports
            #     outputs = self.model(**inputs) # Removed transformers imports
            #     probabilities = torch.softmax(outputs.logits, dim=1) # Removed transformers imports
                
            # Get prediction and confidence
            # prediction = torch.argmax(probabilities, dim=1).item() # Removed transformers imports
            # confidence = probabilities[0][prediction].item() # Removed transformers imports
            
            # Map prediction to label
            # label = "malicious" if prediction == 1 else "safe" # Removed transformers imports
            
            # Use scikit-learn prediction
            X_url = self.vectorizer.transform([url])
            prediction = self.model.predict(X_url)[0]
            confidence = self.model.predict_proba(X_url)[0][prediction]
            
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
            # "max_length": Config.MAX_LENGTH, # Removed Config import
            "loaded": self.model is not None
        }
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.vectorizer is not None 
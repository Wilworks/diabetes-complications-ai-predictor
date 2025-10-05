import joblib
import pandas as pd
import numpy as np
import os
from django.conf import settings

class DiabetesPredictor:
    """
    ML Prediction Engine for Diabetic Microvascular Complications
    """
    
    def __init__(self):
        self.scaler = None
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load the scaler and CatBoost models"""
        try:
            # Load scaler
            scaler_path = os.path.join(settings.ML_MODELS_DIR, 'scaler_original.joblib')
            self.scaler = joblib.load(scaler_path)
            print(f"✓ Loaded scaler from {scaler_path}")
            
            # Load CatBoost models
            target_variables = ['NEP', 'NEU', 'RET']
            for target in target_variables:
                model_path = os.path.join(settings.ML_MODELS_DIR, f'catboost_original_{target}.joblib')
                self.models[target] = joblib.load(model_path)
                print(f"✓ Loaded CatBoost model for {target} from {model_path}")
                
        except FileNotFoundError as e:
            print(f"❌ Error loading models: {e}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise
    
    def convert_dia_life(self, value):
        """Convert diabetes duration from months or years to years (float)"""
        if isinstance(value, str):
            value = value.lower().replace(' ', '')
            if 'm' in value or 'month' in value:
                try:
                    # Extract numeric part and convert months to years
                    numeric = value.replace('m', '').replace('month', '').replace('s', '')
                    return float(numeric) / 12
                except ValueError:
                    return np.nan
            else:
                try:
                    return float(value)
                except ValueError:
                    return np.nan
        try:
            return float(value)
        except (ValueError, TypeError):
            return np.nan
    
    def preprocess_input(self, input_dict):
        """
        Preprocess raw input data for model prediction
        
        Args:
            input_dict: Dictionary with patient data
            
        Returns:
            pd.DataFrame: Preprocessed data ready for prediction
        """
        # Define expected feature names in correct order
        feature_names = [
            'AGE', 'SEX', 'BMI', 'SP', 'BP', 'HbA1c', 'FPS', 'PPS', 
            'FAMILY H/O', 'ONSET AGE', 'DIA LIFE', 'SMOKING', 
            'PHY ACT', 'MED USE', 'MED ADH'
        ]
        
        # Create a copy of input
        processed = input_dict.copy()
        
        # Convert diabetes duration
        if 'DIA LIFE' in processed:
            processed['DIA LIFE'] = self.convert_dia_life(processed['DIA LIFE'])
        
        # Create DataFrame with correct column order
        try:
            input_df = pd.DataFrame([processed])[feature_names]
        except KeyError as e:
            raise ValueError(f"Missing required feature: {e}")
        
        # Scale numerical columns
        numerical_cols = ['AGE', 'BMI', 'SP', 'BP', 'HbA1c', 'FPS', 'PPS', 'ONSET AGE', 'DIA LIFE']
        
        try:
            input_df[numerical_cols] = self.scaler.transform(input_df[numerical_cols])
        except Exception as e:
            raise ValueError(f"Error during scaling: {e}")
        
        return input_df
    
    def predict(self, patient_data):
        """
        Make predictions for all three complications
        
        Args:
            patient_data: Dictionary with patient clinical data
            
        Returns:
            dict: Prediction probabilities for NEP, NEU, RET
        """
        # Preprocess the input
        processed_data = self.preprocess_input(patient_data)
        
        # Make predictions
        predictions = {}
        for target in ['NEP', 'NEU', 'RET']:
            model = self.models[target]
            # Get probability of positive class (class 1)
            probability = model.predict_proba(processed_data)[:, 1][0]
            predictions[target] = float(probability)
        
        return predictions

# Global instance
_predictor_instance = None

def get_predictor():
    """Get or create the global predictor instance"""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = DiabetesPredictor()
    return _predictor_instance
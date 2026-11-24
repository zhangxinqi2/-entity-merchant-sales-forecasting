"""TimesFM-2.5 model interface for time series forecasting.

Uses the official timesfm library from Google.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd
import torch
from loguru import logger

from .base import BaseForecaster
from ..configs.config import TimesFMConfig


class TimesFMForecaster(BaseForecaster):
    """Forecasting interface for TimesFM-2.5 using the official library."""
    
    def __init__(self, config: Optional[TimesFMConfig] = None):
        """
        Initialize TimesFM-2.5 forecaster.
        
        Args:
            config: Configuration for TimesFM model
        """
        self.config = config or TimesFMConfig()
        super().__init__(model_name="TimesFM-2.5", config=self.config)
    
    def load_model(self) -> None:
        """Load the TimesFM-2.5 model using the official library."""
        if self.is_loaded:
            logger.info("TimesFM-2.5 model already loaded")
            return
        
        logger.info(f"Loading TimesFM-2.5 model from {self.config.model_path}")
        
        try:
            # Import from timesfm library
            from timesfm import TimesFm
            
            # Check if model path is local directory or HuggingFace repo
            model_path = self.config.model_path
            if not Path(model_path).exists():
                # Try loading from HuggingFace
                logger.info(f"Model path not found locally, trying HuggingFace: {model_path}")
            
            # Load model using timesfm library
            self.model = TimesFm(
                context_len=self.config.context_length,
                horizon_len=self.config.horizon_length,
                input_patch_len=self.config.patch_length,
                output_patch_len=self.config.output_patch_length,
                num_layers=self.config.num_layers,
                model_dims=self.config.model_dims,
                backend=self.config.device
            )
            
            # Load checkpoint
            self.model.load_from_checkpoint(repo_id=model_path)
            
            self.is_loaded = True
            logger.info(f"TimesFM-2.5 model loaded successfully")
            
        except ImportError as e:
            logger.error(
                f"Failed to import timesfm package. Make sure it's installed.\n"
                f"Run: pip install timesfm\n"
                f"Original error: {e}"
            )
            raise
        except Exception as e:
            logger.error(f"Failed to load TimesFM-2.5 model: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def predict(
        self,
        context: Union[np.ndarray, pd.Series, pd.DataFrame],
        forecast_horizon: Optional[int] = None,
        quantiles: Optional[List[float]] = None
    ) -> Dict[str, np.ndarray]:
        """
        Make predictions using TimesFM-2.5.
        
        Args:
            context: Historical time series data
            forecast_horizon: Number of steps to predict ahead
            quantiles: Quantiles to compute (uses config default if None)
            
        Returns:
            Dictionary with 'mean', 'quantiles', 'lower_bound', 'upper_bound'
        """
        if not self.is_loaded:
            self.load_model()
        
        # Validate and prepare input
        context_values = self.validate_input(context)
        
        # Use config defaults if not provided
        if forecast_horizon is None:
            forecast_horizon = self.config.forecast_horizon
        if quantiles is None:
            quantiles = self.config.quantiles
        
        logger.info(
            f"Making prediction with context length={len(context_values)}, "
            f"horizon={forecast_horizon}"
        )
        
        try:
            # Prepare input for timesfm API
            # TimesFM expects input as numpy array
            input_array = np.array(context_values, dtype=np.float32)
            
            # Make prediction
            with torch.no_grad():
                predictions = self.model.forecast(
                    inputs=input_array,
                    forecast_horizon=forecast_horizon,
                    quantiles=quantiles
                )
            
            # Extract mean prediction
            if isinstance(predictions, dict):
                mean_pred = predictions.get('mean', predictions.get('point', predictions.get('forecast', input_array)))
            else:
                # Assume predictions is directly the forecast array
                mean_pred = predictions
            
            # Ensure it's a numpy array
            if isinstance(mean_pred, torch.Tensor):
                mean_pred = mean_pred.cpu().numpy()
            
            # Ensure correct shape
            mean_pred = np.asarray(mean_pred).flatten()[:forecast_horizon]
            
            # Process quantiles
            quantile_preds = {}
            if isinstance(predictions, dict) and 'quantiles' in predictions:
                q_values = predictions['quantiles']
                for i, q in enumerate(quantiles):
                    if isinstance(q_values, dict) and q in q_values:
                        quantile_preds[q] = np.asarray(q_values[q]).flatten()[:forecast_horizon]
                    elif isinstance(q_values, np.ndarray) and i < q_values.shape[-1]:
                        quantile_preds[q] = q_values.flatten()[i::len(quantiles)][:forecast_horizon]
                    else:
                        quantile_preds[q] = mean_pred.copy()
            else:
                # If no quantiles available, use mean as placeholder
                logger.warning("Quantiles not available, using mean as placeholder")
                for q in quantiles:
                    quantile_preds[q] = mean_pred.copy()
            
            # Get prediction intervals
            lower_bound, upper_bound = self.get_prediction_intervals(quantile_preds)
            
            result = {
                'mean': mean_pred,
                'quantiles': quantile_preds,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
            
            logger.info("Prediction completed successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def batch_predict(
        self,
        contexts: List[Union[np.ndarray, pd.Series, pd.DataFrame]],
        forecast_horizon: Optional[int] = None,
        quantiles: Optional[List[float]] = None
    ) -> List[Dict[str, np.ndarray]]:
        """
        Make predictions for multiple time series.
        
        Args:
            contexts: List of historical time series data
            forecast_horizon: Number of steps to predict ahead
            quantiles: Quantiles to compute
            
        Returns:
            List of prediction dictionaries
        """
        if not self.is_loaded:
            self.load_model()
        
        logger.info(f"Making batch predictions for {len(contexts)} time series")
        
        # Validate and prepare all inputs
        context_values = [self.validate_input(ctx) for ctx in contexts]
        
        # Use config defaults if not provided
        if forecast_horizon is None:
            forecast_horizon = self.config.forecast_horizon
        if quantiles is None:
            quantiles = self.config.quantiles
        
        try:
            # Process each time series individually
            predictions = []
            for ctx in context_values:
                pred = self.predict(ctx, forecast_horizon, quantiles)
                predictions.append(pred)
            
            logger.info("Batch prediction completed")
            
            return predictions
            
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            raise
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        if not self.is_loaded:
            return {"status": "not_loaded"}
        
        info = {
            "model_name": self.model_name,
            "model_path": self.config.model_path,
            "context_length": self.config.context_length,
            "horizon_length": self.config.horizon_length,
            "patch_length": self.config.patch_length,
            "device": self.config.device,
            "is_loaded": self.is_loaded,
            "description": "TimesFM-2.5: Time Series Foundation Model by Google"
        }
        
        return info

#!/usr/bin/env python3
"""
Model Comparison Script
Compares CNN model performance with YOLO model
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
import logging
from PIL import Image
import io
import base64

# Import models
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("YOLO not available - install ultralytics to compare")

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available - install tensorflow to compare")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelComparator:
    def __init__(self, data_dir, csv_path):
        self.data_dir = Path(data_dir)
        self.csv_path = csv_path
        self.class_names = ['mel', 'nv', 'bcc', 'akiec', 'bkl', 'df', 'vasc']
        
        # Load metadata
        self.metadata = self._load_metadata()
        
        # Initialize models
        self.yolo_model = None
        self.cnn_model = None
        
    def _load_metadata(self):
        """Load metadata from CSV"""
        df = pd.read_csv(self.csv_path)
        df = df[df['dx'].isin(self.class_names)]
        
        metadata_dict = {}
        for _, row in df.iterrows():
            image_id = row['image_id']
            diagnosis = row['dx']
            metadata_dict[image_id] = diagnosis
            
        return metadata_dict
    
    def load_models(self, yolo_path, cnn_path):
        """Load both models"""
        # Load YOLO model
        if YOLO_AVAILABLE and os.path.exists(yolo_path):
            try:
                self.yolo_model = YOLO(yolo_path)
                self.yolo_model.to("cpu")
                logger.info("YOLO model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load YOLO model: {e}")
        
        # Load CNN model
        if TF_AVAILABLE and os.path.exists(cnn_path):
            try:
                self.cnn_model = tf.keras.models.load_model(cnn_path)
                logger.info("CNN model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load CNN model: {e}")
    
    def predict_yolo(self, image_path):
        """Make prediction using YOLO model"""
        if self.yolo_model is None:
            return None
        
        try:
            image = Image.open(image_path).convert("RGB")
            results = self.yolo_model.predict(image, imgsz=640)[0]
            
            predictions = []
            for box in results.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = self.yolo_model.names[cls_id].lower()
                predictions.append({
                    'class': class_name,
                    'confidence': conf
                })
            
            # Return top prediction
            if predictions:
                top_pred = max(predictions, key=lambda x: x['confidence'])
                return {
                    'predicted_class': top_pred['class'],
                    'confidence': top_pred['confidence'],
                    'all_predictions': predictions
                }
            else:
                return {
                    'predicted_class': 'unknown',
                    'confidence': 0.0,
                    'all_predictions': []
                }
        except Exception as e:
            logger.error(f"YOLO prediction error: {e}")
            return None
    
    def predict_cnn(self, image_path):
        """Make prediction using CNN model"""
        if self.cnn_model is None:
            return None
        
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0
            image_batch = np.expand_dims(image_array, axis=0)
            
            # Make prediction
            prediction = self.cnn_model.predict(image_batch, verbose=0)
            
            # Get top prediction
            top_class_idx = np.argmax(prediction[0])
            top_class = self.class_names[top_class_idx]
            confidence = prediction[0][top_class_idx]
            
            # Get all predictions
            all_predictions = [
                {
                    'class': self.class_names[i],
                    'confidence': float(prediction[0][i])
                }
                for i in range(len(self.class_names))
            ]
            
            return {
                'predicted_class': top_class,
                'confidence': float(confidence),
                'all_predictions': all_predictions
            }
        except Exception as e:
            logger.error(f"CNN prediction error: {e}")
            return None
    
    def compare_on_dataset(self, split='val', num_samples=100):
        """Compare models on a subset of the dataset"""
        logger.info(f"Comparing models on {split} dataset...")
        
        images_dir = self.data_dir / 'images' / split
        image_paths = list(images_dir.glob('*.jpg'))[:num_samples]
        
        results = []
        
        for img_path in image_paths:
            image_id = img_path.stem
            if image_id not in self.metadata:
                continue
            
            true_label = self.metadata[image_id]
            
            # Get predictions
            yolo_pred = self.predict_yolo(img_path)
            cnn_pred = self.predict_cnn(img_path)
            
            result = {
                'image_id': image_id,
                'true_label': true_label,
                'yolo_prediction': yolo_pred,
                'cnn_prediction': cnn_pred
            }
            
            results.append(result)
        
        return results
    
    def calculate_metrics(self, results):
        """Calculate accuracy metrics for both models"""
        yolo_correct = 0
        cnn_correct = 0
        total_samples = len(results)
        
        yolo_confidences = []
        cnn_confidences = []
        
        for result in results:
            true_label = result['true_label']
            
            # YOLO metrics
            if result['yolo_prediction']:
                yolo_pred = result['yolo_prediction']['predicted_class']
                yolo_conf = result['yolo_prediction']['confidence']
                if yolo_pred == true_label:
                    yolo_correct += 1
                yolo_confidences.append(yolo_conf)
            
            # CNN metrics
            if result['cnn_prediction']:
                cnn_pred = result['cnn_prediction']['predicted_class']
                cnn_conf = result['cnn_prediction']['confidence']
                if cnn_pred == true_label:
                    cnn_correct += 1
                cnn_confidences.append(cnn_conf)
        
        metrics = {
            'yolo': {
                'accuracy': yolo_correct / total_samples if total_samples > 0 else 0,
                'avg_confidence': np.mean(yolo_confidences) if yolo_confidences else 0,
                'correct_predictions': yolo_correct,
                'total_samples': total_samples
            },
            'cnn': {
                'accuracy': cnn_correct / total_samples if total_samples > 0 else 0,
                'avg_confidence': np.mean(cnn_confidences) if cnn_confidences else 0,
                'correct_predictions': cnn_correct,
                'total_samples': total_samples
            }
        }
        
        return metrics
    
    def generate_comparison_report(self, results, metrics):
        """Generate a detailed comparison report"""
        report = {
            'summary': {
                'total_samples_tested': len(results),
                'models_compared': ['YOLO', 'CNN']
            },
            'performance_metrics': metrics,
            'model_characteristics': {
                'yolo': {
                    'type': 'Object Detection + Classification',
                    'input_size': '640x640',
                    'architecture': 'YOLOv10 Nano',
                    'use_case': 'Detects lesions and classifies them',
                    'output': 'Bounding boxes + class predictions'
                },
                'cnn': {
                    'type': 'Image Classification',
                    'input_size': '224x224',
                    'architecture': 'Custom CNN',
                    'use_case': 'Classifies entire image',
                    'output': 'Class probabilities'
                }
            },
            'detailed_results': results[:10]  # First 10 results for detailed view
        }
        
        return report
    
    def save_comparison_report(self, report, filename='model_comparison_report.json'):
        """Save comparison report to file"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Comparison report saved to {filename}")


def main():
    """Main comparison function"""
    # Paths
    data_dir = "/Users/bravozheng/Coding/Skin/PRS-PM-2025-AIS07PT-Group1_SkinAnalyzer-master/yolo_training_split_backup"
    csv_path = "/Users/bravozheng/Coding/Skin/PRS-PM-2025-AIS07PT-Group1_SkinAnalyzer-master/Kaggle Data/HAM10000_metadata.csv"
    
    # Model paths
    yolo_path = "/Users/bravozheng/Coding/Skin/PRS-PM-2025-AIS07PT-Group1_SkinAnalyzer-master/SystemCode/backend/yolov10nano_skin_detection_400runs.pt"
    cnn_path = "/Users/bravozheng/Coding/Skin/PRS-PM-2025-AIS07PT-Group1_SkinAnalyzer-master/SystemCode/backend/model_training_comparison/best_cnn_model.h5"
    
    # Initialize comparator
    comparator = ModelComparator(data_dir, csv_path)
    
    # Load models
    comparator.load_models(yolo_path, cnn_path)
    
    # Compare on validation set
    results = comparator.compare_on_dataset(split='val', num_samples=200)
    
    # Calculate metrics
    metrics = comparator.calculate_metrics(results)
    
    # Generate report
    report = comparator.generate_comparison_report(results, metrics)
    
    # Print summary
    print("\n" + "="*50)
    print("MODEL COMPARISON RESULTS")
    print("="*50)
    
    print(f"\nYOLO Model Performance:")
    print(f"  Accuracy: {metrics['yolo']['accuracy']:.4f}")
    print(f"  Average Confidence: {metrics['yolo']['avg_confidence']:.4f}")
    print(f"  Correct Predictions: {metrics['yolo']['correct_predictions']}/{metrics['yolo']['total_samples']}")
    
    print(f"\nCNN Model Performance:")
    print(f"  Accuracy: {metrics['cnn']['accuracy']:.4f}")
    print(f"  Average Confidence: {metrics['cnn']['avg_confidence']:.4f}")
    print(f"  Correct Predictions: {metrics['cnn']['correct_predictions']}/{metrics['cnn']['total_samples']}")
    
    print(f"\nWinner: {'YOLO' if metrics['yolo']['accuracy'] > metrics['cnn']['accuracy'] else 'CNN'}")
    
    # Save report
    comparator.save_comparison_report(report)
    
    return report


if __name__ == "__main__":
    main()

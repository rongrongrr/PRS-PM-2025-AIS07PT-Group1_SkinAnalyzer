#!/usr/bin/env python3
"""
CNN-based Skin Lesion Classification Model Training Script
Alternative to YOLO approach using CNN for image classification
"""

import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Try to import TensorFlow with error handling
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models, optimizers, callbacks
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    TF_AVAILABLE = True
except ImportError as e:
    print(f"TensorFlow not available: {e}")
    TF_AVAILABLE = False

try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    SKLEARN_AVAILABLE = True
except ImportError as e:
    print(f"Scikit-learn not available: {e}")
    SKLEARN_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError as e:
    print(f"Matplotlib not available: {e}")
    MATPLOTLIB_AVAILABLE = False

from PIL import Image
import json
import pickle
from pathlib import Path
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkinLesionCNN:
    def __init__(self, data_dir, csv_path, img_size=(224, 224)):
        """
        Initialize the CNN model for skin lesion classification
        
        Args:
            data_dir: Path to the training data directory
            csv_path: Path to the HAM10000 metadata CSV file
            img_size: Target image size for the model
        """
        self.data_dir = Path(data_dir)
        self.csv_path = csv_path
        self.img_size = img_size
        self.class_names = ['mel', 'nv', 'bcc', 'akiec', 'bkl', 'df', 'vasc']
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.class_names)}
        self.idx_to_class = {idx: cls for cls, idx in self.class_to_idx.items()}
        
        # Load metadata
        self.metadata = self._load_metadata()
        
        # Model will be initialized later
        self.model = None
        self.history = None
        
    def _load_metadata(self):
        """Load and process the HAM10000 metadata CSV"""
        logger.info("Loading metadata from CSV...")
        df = pd.read_csv(self.csv_path)
        
        # Filter only the classes we're interested in
        df = df[df['dx'].isin(self.class_names)]
        
        # Create image_id to diagnosis mapping
        metadata_dict = {}
        for _, row in df.iterrows():
            image_id = row['image_id']
            diagnosis = row['dx']
            metadata_dict[image_id] = diagnosis
            
        logger.info(f"Loaded metadata for {len(metadata_dict)} images")
        logger.info(f"Class distribution: {df['dx'].value_counts().to_dict()}")
        
        return metadata_dict
    
    def _create_dataset(self, split='train'):
        """Create dataset from images and labels"""
        logger.info(f"Creating {split} dataset...")
        
        images_dir = self.data_dir / 'images' / split
        image_paths = []
        labels = []
        
        for img_path in images_dir.glob('*.jpg'):
            image_id = img_path.stem
            if image_id in self.metadata:
                image_paths.append(str(img_path))
                labels.append(self.class_to_idx[self.metadata[image_id]])
        
        logger.info(f"Found {len(image_paths)} images in {split} set")
        return image_paths, labels
    
    def _load_and_preprocess_image(self, image_path):
        """Load and preprocess a single image"""
        try:
            image = Image.open(image_path).convert('RGB')
            image = image.resize(self.img_size)
            image_array = np.array(image) / 255.0  # Normalize to [0, 1]
            return image_array
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    
    def create_data_generators(self, batch_size=32, validation_split=0.2):
        """Create data generators for training and validation"""
        logger.info("Creating data generators...")
        
        # Get all image paths and labels
        train_paths, train_labels = self._create_dataset('train')
        val_paths, val_labels = self._create_dataset('val')
        
        # Combine train and val for proper splitting
        all_paths = train_paths + val_paths
        all_labels = train_labels + val_labels
        
        # Split into train and validation
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            all_paths, all_labels, test_size=validation_split, 
            random_state=42, stratify=all_labels
        )
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest'
        )
        
        # No augmentation for validation
        val_datagen = ImageDataGenerator()
        
        def data_generator(paths, labels, datagen, batch_size):
            """Custom data generator"""
            while True:
                indices = np.random.permutation(len(paths))
                for i in range(0, len(indices), batch_size):
                    batch_indices = indices[i:i + batch_size]
                    batch_paths = [paths[j] for j in batch_indices]
                    batch_labels = [labels[j] for j in batch_indices]
                    
                    batch_images = []
                    for path in batch_paths:
                        img = self._load_and_preprocess_image(path)
                        if img is not None:
                            batch_images.append(img)
                    
                    if batch_images:
                        batch_images = np.array(batch_images)
                        batch_labels = tf.keras.utils.to_categorical(
                            batch_labels, num_classes=len(self.class_names)
                        )
                        yield batch_images, batch_labels
        
        train_gen = data_generator(train_paths, train_labels, train_datagen, batch_size)
        val_gen = data_generator(val_paths, val_labels, val_datagen, batch_size)
        
        steps_per_epoch = len(train_paths) // batch_size
        validation_steps = len(val_paths) // batch_size
        
        return train_gen, val_gen, steps_per_epoch, validation_steps
    
    def build_model(self):
        """Build CNN model architecture"""
        logger.info("Building CNN model...")
        
        model = models.Sequential([
            # Input layer
            layers.Input(shape=(*self.img_size, 3)),
            
            # Convolutional layers
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Global Average Pooling instead of Flatten
            layers.GlobalAveragePooling2D(),
            
            # Dense layers
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            
            # Output layer
            layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        logger.info(f"Model built with {model.count_params()} parameters")
        return model
    
    def train(self, epochs=50, batch_size=32, validation_split=0.2):
        """Train the CNN model"""
        logger.info("Starting model training...")
        
        # Create data generators
        train_gen, val_gen, steps_per_epoch, validation_steps = self.create_data_generators(
            batch_size, validation_split
        )
        
        # Callbacks
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            callbacks.ModelCheckpoint(
                'best_cnn_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                save_weights_only=False
            )
        ]
        
        # Train model
        start_time = time.time()
        self.history = self.model.fit(
            train_gen,
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            validation_data=val_gen,
            validation_steps=validation_steps,
            callbacks=callbacks_list,
            verbose=1
        )
        end_time = time.time()
        self.training_time_seconds = end_time - start_time
        hours = int(self.training_time_seconds // 3600)
        minutes = int((self.training_time_seconds % 3600) // 60)
        seconds = int(self.training_time_seconds % 60)
        logger.info(f"Total training time: {hours}h {minutes}m {seconds}s ({self.training_time_seconds:.2f}s)")
        
        logger.info("Training completed!")
        return self.history
    
    def evaluate(self, test_data=None):
        """Evaluate the model"""
        logger.info("Evaluating model...")
        
        if test_data is None:
            # Use validation data for evaluation
            _, val_gen, _, validation_steps = self.create_data_generators()
            test_data = val_gen
        
        # Evaluate
        results = self.model.evaluate(test_data, steps=validation_steps, verbose=1)
        
        logger.info(f"Test Accuracy: {results[1]:.4f}")
        
        return results
    
    def predict(self, image_path):
        """Make prediction on a single image"""
        image = self._load_and_preprocess_image(image_path)
        if image is None:
            return None
        
        image_batch = np.expand_dims(image, axis=0)
        prediction = self.model.predict(image_batch, verbose=0)
        
        # Get top prediction
        top_class_idx = np.argmax(prediction[0])
        top_class = self.idx_to_class[top_class_idx]
        confidence = prediction[0][top_class_idx]
        
        # Get top 3 predictions
        top3_indices = np.argsort(prediction[0])[-3:][::-1]
        top3_predictions = [
            {
                'class': self.idx_to_class[idx],
                'confidence': float(prediction[0][idx])
            }
            for idx in top3_indices
        ]
        
        return {
            'predicted_class': top_class,
            'confidence': float(confidence),
            'top3_predictions': top3_predictions,
            'all_probabilities': {
                self.idx_to_class[i]: float(prediction[0][i]) 
                for i in range(len(self.class_names))
            }
        }
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            logger.error("No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_model(self, model_path='cnn_skin_lesion_model.h5'):
        """Save the trained model to file"""
        if self.model is None:
            logger.error("No model to save. Please train the model first.")
            return
        
        try:
            self.model.save(model_path)
            logger.info(f"Model saved successfully to {model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def save_model_info(self):
        """Save model information and class mappings"""
        model_info = {
            'class_names': self.class_names,
            'class_to_idx': self.class_to_idx,
            'idx_to_class': self.idx_to_class,
            'img_size': self.img_size,
            'model_architecture': 'CNN',
            'total_params': self.model.count_params() if self.model else 0
        }
        
        with open('cnn_model_info.json', 'w') as f:
            json.dump(model_info, f, indent=2)
        
        logger.info("Model information saved to cnn_model_info.json")


def compare_with_yolo():
    """Compare CNN model with YOLO model"""
    logger.info("Comparing CNN model with YOLO model...")
    
    # Load YOLO model for comparison
    try:
        from ultralytics import YOLO
        yolo_model = YOLO("yolov10nano_skin_detection_400runs.pt")
        logger.info("YOLO model loaded successfully")
    except Exception as e:
        logger.error(f"Could not load YOLO model: {e}")
        return
    
    # Load CNN model
    try:
        cnn_model = tf.keras.models.load_model('best_cnn_model.h5')
        logger.info("CNN model loaded successfully")
    except Exception as e:
        logger.error(f"Could not load CNN model: {e}")
        return
    
    # Comparison metrics
    comparison = {
        'model_type': ['YOLO', 'CNN'],
        'architecture': ['Object Detection', 'Image Classification'],
        'input_size': ['640x640', '224x224'],
        'output_type': ['Bounding boxes + Classification', 'Classification only'],
        'use_case': ['Detection + Classification', 'Classification only']
    }
    
    logger.info("Model Comparison:")
    for metric, values in comparison.items():
        logger.info(f"{metric}: {values[0]} vs {values[1]}")
    
    return comparison


def main():
    """Main training function"""
    # Check if required libraries are available
    if not TF_AVAILABLE:
        print("❌ TensorFlow is not available. Please install it with: pip install tensorflow")
        return
    
    if not SKLEARN_AVAILABLE:
        print("❌ Scikit-learn is not available. Please install it with: pip install scikit-learn")
        return
    
    print("✅ All required libraries are available!")
    
    # Paths
    data_dir = "/Users/bravozheng/Coding/Skin/PRS-PM-2025-AIS07PT-Group1_SkinAnalyzer-master/yolo_training_split_backup"
    csv_path = "/Users/bravozheng/Coding/Skin/PRS-PM-2025-AIS07PT-Group1_SkinAnalyzer-master/Kaggle Data/HAM10000_metadata.csv"
    
    # Initialize CNN model
    cnn_model = SkinLesionCNN(data_dir, csv_path, img_size=(224, 224))
    
    # Build model
    model = cnn_model.build_model()
    print(model.summary())
    
    # Train model
    history = cnn_model.train(epochs=30, batch_size=32)
    if hasattr(cnn_model, 'training_time_seconds'):
        hours = int(cnn_model.training_time_seconds // 3600)
        minutes = int((cnn_model.training_time_seconds % 3600) // 60)
        seconds = int(cnn_model.training_time_seconds % 60)
        logger.info(f"Training duration (reported by main): {hours}h {minutes}m {seconds}s ({cnn_model.training_time_seconds:.2f}s)")
    
    # Evaluate model
    results = cnn_model.evaluate()
    
    # Save the trained model
    cnn_model.save_model('cnn_skin_lesion_model.h5')
    
    # Plot training history
    cnn_model.plot_training_history()
    
    # Save model info
    cnn_model.save_model_info()
    
    # Compare with YOLO
    comparison = compare_with_yolo()
    
    logger.info("Training completed successfully!")
    logger.info(f"Final validation accuracy: {results[1]:.4f}")


if __name__ == "__main__":
    main()

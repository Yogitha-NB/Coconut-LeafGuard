import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class CoconutModelTrainer:
    def __init__(self):
        self.img_height = 224
        self.img_width = 224
        self.batch_size = 16
        self.epochs = 20
        self.num_classes = 5
        self.class_names = ['Yellowing', 'Drying of Leaflets', 'Caterpillars', 'Flaccidity', 'Healthy']

    def create_model(self):
        """ Create a MobileNetV2 Transfer Learning Model """
        base_model = keras.applications.MobileNetV2(
            input_shape=(self.img_height, self.img_width, 3),
            include_top=False,
            weights='imagenet'
        )

        base_model.trainable = False  # Freeze base

        model = keras.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.4),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def create_data_generator(self):
        """ Create training and validation augmentation """
        train_datagen = keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            rotation_range=25,
            width_shift_range=0.2,
            height_shift_range=0.2,
            zoom_range=0.2,
            shear_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            fill_mode='nearest',
            validation_split=0.2
        )
        return train_datagen

    def train_with_generator(self, data_dir):
        """ Train the model using ImageDataGenerator """
        datagen = self.create_data_generator()

        train_generator = datagen.flow_from_directory(
            data_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )

        val_generator = datagen.flow_from_directory(
            data_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )

        model = self.create_model()

        callbacks = [
            keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
            keras.callbacks.ModelCheckpoint('models/coconut_model_best.h5', save_best_only=True),
            keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3)
        ]

        history = model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=self.epochs,
            callbacks=callbacks
        )

        return model, history

    def plot_training_history(self, history):
        """ Plot accuracy and loss graphs """
        plt.figure(figsize=(12, 4))

        # Accuracy Plot
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.legend()

        # Loss Plot
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Model Loss')
        plt.legend()

        plt.savefig('training_history.png')
        plt.show()

def main():
    os.makedirs("models", exist_ok=True)

    trainer = CoconutModelTrainer()

    dataset_path = "dataset"

    if not os.path.exists(dataset_path):
        print("Dataset folder missing!")
        return

    model, history = trainer.train_with_generator(dataset_path)

    trainer.plot_training_history(history)

    model.save("models/coconut_model_final.h5")
    print("Training completed and model saved!")

if __name__ == "__main__":
    main()

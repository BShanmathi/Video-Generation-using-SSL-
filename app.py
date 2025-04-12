import tensorflow as tf
import tensorflow_addons as tfa
import tensorflow.keras.layers as layers
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import gc

gc.collect()

# --- 1️⃣ Load and Preprocess Dataset ---
batch_size = 8
img_height = 224
img_width = 224

data_dir = r"C:\Users\tssum\PycharmProjects\PythonProject\agriculture_dataset"

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.8, 1.2],
    zoom_range=0.2
)

train_data = datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical'  # Matches categorical_crossentropy loss
)

# --- 2️⃣ Build a CNN Encoder Model for SSL ---
base_model = tf.keras.applications.ResNet50(weights=None, include_top=False, input_shape=(img_height, img_width, 3))

x = layers.GlobalAveragePooling2D()(base_model.output)
x = layers.Dense(128, activation='relu')(x)  # SSL Projection Head
x = layers.Dense(4, activation='relu')(x)  # Additional Layer
ssl_encoder = tf.keras.models.Model(inputs=base_model.input, outputs=x)

# --- 3️⃣ Change Pretraining to Autoencoder-style Learning ---
ssl_encoder.compile(optimizer='adam', loss='mse')  # Use MSE for representation learning

ssl_encoder.fit(train_data, epochs=10)

# --- 4️⃣ Fine-Tune on Labeled Data ---
classifier_head = tf.keras.Sequential([
    layers.Dense(128, activation='relu'),
    layers.Dense(train_data.num_classes, activation='softmax')  # Ensure correct number of classes
])

# Attach the classifier to SSL encoder
final_model = tf.keras.models.Model(inputs=ssl_encoder.input, outputs=classifier_head(ssl_encoder.output))

# Compile with classification loss
final_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train on labeled data
final_model.fit(train_data, epochs=20)

# --- 5️⃣ Save Fine-Tuned Model ---
final_model.save("self_supervised_agriculture_model.h5")

print("✅ Self-Supervised Learning Model Trained and Saved!")


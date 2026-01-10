"""
Week 6 Lab: Neural Networks with TensorFlow/Keras
===================================================

This lab demonstrates:
1. Building a Multi-Layer Perceptron (MLP) for MNIST digit recognition
2. Understanding layers, activation functions, and training
3. Evaluating model performance
4. Visualizing predictions

To run:
    conda activate is_labs
    python src/week6/week6_lab.py
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

# ============================================
# WEEK 6 LAB: NEURAL NETWORKS
# ============================================

print("=" * 55)
print("   WEEK 6 LAB: Neural Networks (MNIST)")
print("=" * 55)
print(f"   TensorFlow Version: {tf.__version__}")

# ------------------------------------------
# 1. Load and Prepare Data
# ------------------------------------------
print("\n[1] Loading MNIST Dataset...")
(X_train, y_train), (X_test, y_test) = mnist.load_data()

print(f"    Training samples: {X_train.shape[0]}")
print(f"    Test samples: {X_test.shape[0]}")
print(f"    Image shape: {X_train.shape[1:]} (28x28 pixels)")
print(f"    Classes: 0-9 (digits)")

# Normalize pixel values to [0, 1]
X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0

# Flatten images for MLP (28x28 -> 784)
X_train_flat = X_train.reshape(-1, 784)
X_test_flat = X_test.reshape(-1, 784)
print(f"    Flattened input shape: {X_train_flat.shape[1]} features")

# ------------------------------------------
# 2. Build the Neural Network
# ------------------------------------------
print("\n[2] Building Neural Network...")

model = keras.Sequential([
    # Input layer (784 features)
    layers.Input(shape=(784,)),
    
    # Hidden Layer 1: 128 neurons with ReLU
    layers.Dense(128, activation='relu', name='hidden_1'),
    
    # Hidden Layer 2: 64 neurons with ReLU  
    layers.Dense(64, activation='relu', name='hidden_2'),
    
    # Output Layer: 10 neurons with Softmax (for 10 classes)
    layers.Dense(10, activation='softmax', name='output')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Display model architecture
print("\n    Model Architecture:")
model.summary()

# ------------------------------------------
# 3. Train the Model
# ------------------------------------------
print("\n[3] Training Neural Network...")
print("    Epochs: 10, Batch Size: 128")

history = model.fit(
    X_train_flat, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# ------------------------------------------
# 4. Evaluate the Model
# ------------------------------------------
print("\n[4] Evaluating Model...")
test_loss, test_accuracy = model.evaluate(X_test_flat, y_test, verbose=0)

print(f"\n    Test Results:")
print(f"    Loss:     {test_loss:.4f}")
print(f"    Accuracy: {test_accuracy*100:.2f}%")

# ------------------------------------------
# 5. Make Predictions
# ------------------------------------------
print("\n[5] Sample Predictions:")
predictions = model.predict(X_test_flat[:10], verbose=0)

print("    Image | True | Predicted | Confidence")
print("    " + "-" * 42)
for i in range(10):
    pred_class = np.argmax(predictions[i])
    confidence = predictions[i][pred_class] * 100
    correct = "✓" if pred_class == y_test[i] else "✗"
    print(f"      {i:2d}   |  {y_test[i]}   |     {pred_class}     |  {confidence:5.1f}%  {correct}")

# ------------------------------------------
# 6. Visualizations
# ------------------------------------------
print("\n[6] Creating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Training & Validation Accuracy
ax1 = axes[0, 0]
ax1.plot(history.history['accuracy'], label='Training', marker='o')
ax1.plot(history.history['val_accuracy'], label='Validation', marker='s')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.set_title('Model Accuracy over Epochs')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Training & Validation Loss
ax2 = axes[0, 1]
ax2.plot(history.history['loss'], label='Training', marker='o')
ax2.plot(history.history['val_loss'], label='Validation', marker='s')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.set_title('Model Loss over Epochs')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Sample Predictions
ax3 = axes[1, 0]
for i in range(5):
    ax3.subplot_mosaic = None  # placeholder
    
# Instead, show confusion-like accuracy per digit
from sklearn.metrics import confusion_matrix
y_pred = np.argmax(model.predict(X_test_flat, verbose=0), axis=1)
cm = confusion_matrix(y_test, y_pred)
per_class_acc = cm.diagonal() / cm.sum(axis=1) * 100

ax3.bar(range(10), per_class_acc, color='steelblue')
ax3.set_xlabel('Digit Class')
ax3.set_ylabel('Accuracy (%)')
ax3.set_title('Per-Class Accuracy')
ax3.set_xticks(range(10))
ax3.set_ylim([90, 100])
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: Sample digit images with predictions
ax4 = axes[1, 1]
ax4.axis('off')
ax4.set_title('Sample Predictions')

# Create mini grid of sample images
for i in range(8):
    ax_sub = fig.add_axes([0.55 + (i % 4) * 0.1, 0.1 + (1 - i // 4) * 0.15, 0.08, 0.12])
    ax_sub.imshow(X_test[i], cmap='gray')
    pred = np.argmax(predictions[i]) if i < 10 else "?"
    color = 'green' if pred == y_test[i] else 'red'
    ax_sub.set_title(f"pred:{pred}", fontsize=8, color=color)
    ax_sub.axis('off')

plt.tight_layout()
plt.savefig('src/week6/week6_neural_network_results.png', dpi=100)
print("    Saved: src/week6/week6_neural_network_results.png")

# ------------------------------------------
# Summary
# ------------------------------------------
print("\n" + "=" * 55)
print("   WEEK 6 LAB COMPLETE!")
print("=" * 55)
print("\n   Key Takeaways:")
print("   • Neural networks learn hierarchical representations")
print("   • ReLU activation enables training deep networks")
print("   • Softmax + CrossEntropy for multi-class classification")
print(f"   • Achieved {test_accuracy*100:.1f}% accuracy on digit recognition")
print("   • Training improved steadily over epochs")
print()

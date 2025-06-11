import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

print("TensorFlow version:", tf.__version__)
print("GPU Available:", tf.config.list_physical_devices('GPU'))
print()

# Load and preprocess CIFAR-10 dataset
print("Loading CIFAR-10 dataset...")
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Class names for CIFAR-10
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

print(f"Training data shape: {x_train.shape}")
print(f"Training labels shape: {y_train.shape}")
print(f"Test data shape: {x_test.shape}")
print(f"Test labels shape: {y_test.shape}")
print()

# Normalize pixel values to be between 0 and 1
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Convert labels to categorical one-hot encoding
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

# Display some sample images
plt.figure(figsize=(12, 8))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.imshow(x_train[i])
    plt.title(f'{class_names[np.argmax(y_train[i])]}')
    plt.axis('off')
plt.suptitle('Sample CIFAR-10 Images')
plt.tight_layout()
plt.show()

# Build the CNN model
def create_cnn_model():
    model = keras.Sequential([
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3), name='conv1'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', name='conv2'),
        layers.MaxPooling2D((2, 2), name='pool1'),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu', name='conv3'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', name='conv4'),
        layers.MaxPooling2D((2, 2), name='pool2'),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), activation='relu', name='conv5'),
        layers.BatchNormalization(),
        layers.Dropout(0.25),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu', name='dense1'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax', name='output')  # 10 classes for CIFAR-10
    ])
    
    return model

# Create and compile the model
print("Creating CNN model...")
model = create_cnn_model()

# Display model architecture
model.summary()

# Compile the model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Data augmentation for better generalization
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# Apply data augmentation to training data
x_train_augmented = data_augmentation(x_train)

# Define callbacks
callbacks = [
    keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-7)
]

# Train the model
print("\nStarting training...")
history = model.fit(
    x_train, y_train,
    batch_size=32,
    epochs=20,  # Reduced for demonstration
    validation_split=0.2,
    callbacks=callbacks,
    verbose=1
)

# Evaluate the model
print("\nEvaluating model on test data...")
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy:.4f}")
print(f"Test loss: {test_loss:.4f}")

# Plot training history
plt.figure(figsize=(15, 5))

# Plot training & validation accuracy
plt.subplot(1, 3, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot training & validation loss
plt.subplot(1, 3, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot learning rate (if available)
if 'lr' in history.history:
    plt.subplot(1, 3, 3)
    plt.plot(history.history['lr'])
    plt.title('Learning Rate')
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.yscale('log')
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Make predictions on test data
print("\nMaking predictions...")
predictions = model.predict(x_test[:100])  # Predict first 100 test images
predicted_classes = np.argmax(predictions, axis=1)
true_classes = np.argmax(y_test[:100], axis=1)

# Display prediction results
plt.figure(figsize=(15, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.imshow(x_test[i])
    predicted_class = class_names[predicted_classes[i]]
    true_class = class_names[true_classes[i]]
    confidence = predictions[i][predicted_classes[i]] * 100
    
    color = 'green' if predicted_classes[i] == true_classes[i] else 'red'
    plt.title(f'Pred: {predicted_class}\nTrue: {true_class}\nConf: {confidence:.1f}%', 
              color=color, fontsize=8)
    plt.axis('off')

plt.suptitle('CNN Predictions (Green=Correct, Red=Incorrect)')
plt.tight_layout()
plt.show()

# Analyze model performance per class
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Get predictions for all test data
all_predictions = model.predict(x_test)
all_predicted_classes = np.argmax(all_predictions, axis=1)
all_true_classes = np.argmax(y_test, axis=1)

# Classification report
print("\nClassification Report:")
print(classification_report(all_true_classes, all_predicted_classes, 
                          target_names=class_names))

# Confusion matrix
plt.figure(figsize=(10, 8))
cm = confusion_matrix(all_true_classes, all_predicted_classes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Feature visualization - show what the first conv layer learned
print("\nVisualizing learned filters...")
# Get the weights of the first convolutional layer
conv_weights = model.get_layer('conv1').get_weights()[0]
print(f"First conv layer weights shape: {conv_weights.shape}")

# Plot the filters
fig, axes = plt.subplots(4, 8, figsize=(15, 8))
for i, ax in enumerate(axes.flat):
    if i < conv_weights.shape[3]:  # Number of filters
        # Normalize the filter for better visualization
        filter_img = conv_weights[:, :, :, i]
        filter_img = (filter_img - filter_img.min()) / (filter_img.max() - filter_img.min())
        ax.imshow(filter_img)
        ax.set_title(f'Filter {i+1}')
        ax.axis('off')
    else:
        ax.axis('off')

plt.suptitle('Learned Filters in First Convolutional Layer')
plt.tight_layout()
plt.show()

print("\nCNN training and evaluation completed!")
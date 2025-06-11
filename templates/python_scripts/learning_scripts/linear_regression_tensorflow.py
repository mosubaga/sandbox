import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

# Create a small dataset (few data points)
# Let's say we're predicting house prices based on size
X_train = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float32)  # House size (in 1000 sq ft)
y_train = np.array([1.5, 3.2, 4.8, 6.1, 7.9], dtype=np.float32)  # House price (in $100k)

print("Training Data:")
print("House Size (1000 sq ft):", X_train)
print("House Price ($100k):", y_train)
print()

# Create the model
class LinearRegressionModel(tf.keras.Model):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        # Initialize weight and bias
        self.w = tf.Variable(tf.random.normal([1]), trainable=True, name='weight')
        self.b = tf.Variable(tf.random.normal([1]), trainable=True, name='bias')
    
    def call(self, x):
        return self.w * x + self.b

# Create model instance
model = LinearRegressionModel()

# Define loss function (Mean Squared Error)
def mse_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

# Define optimizer
optimizer = tf.optimizers.Adam(learning_rate=0.1)

# Training parameters
epochs = 1000
loss_history = []

print("Initial parameters:")
print(f"Weight: {model.w.numpy()[0]:.4f}")
print(f"Bias: {model.b.numpy()[0]:.4f}")
print()

# Training loop
for epoch in range(epochs):
    with tf.GradientTape() as tape:
        # Forward pass
        y_pred = model(X_train)
        loss = mse_loss(y_train, y_pred)
    
    # Compute gradients
    gradients = tape.gradient(loss, [model.w, model.b])
    
    # Update parameters
    optimizer.apply_gradients(zip(gradients, [model.w, model.b]))
    
    # Store loss for plotting
    loss_history.append(loss.numpy())
    
    # Print progress every 100 epochs
    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss.numpy():.6f}, Weight: {model.w.numpy()[0]:.4f}, Bias: {model.b.numpy()[0]:.4f}")

print()
print("Final parameters:")
print(f"Weight: {model.w.numpy()[0]:.4f}")
print(f"Bias: {model.b.numpy()[0]:.4f}")
print(f"Final Loss: {loss_history[-1]:.6f}")

# Make predictions
y_pred_final = model(X_train)
print()
print("Predictions vs Actual:")
for i, (actual, pred) in enumerate(zip(y_train, y_pred_final.numpy())):
    print(f"Size: {X_train[i]:.1f}, Actual: {actual:.2f}, Predicted: {pred:.2f}")

# Test with new data point
new_size = np.array([6.0], dtype=np.float32)
new_prediction = model(new_size)
print(f"\nPrediction for house size 6.0 (1000 sq ft): ${new_prediction.numpy()[0]*100:.1f}k")

# Plotting
plt.figure(figsize=(12, 4))

# Plot 1: Data and fitted line
plt.subplot(1, 2, 1)
plt.scatter(X_train, y_train, color='blue', label='Training Data', s=100)
plt.plot(X_train, y_pred_final.numpy(), color='red', label='Fitted Line', linewidth=2)
plt.xlabel('House Size (1000 sq ft)')
plt.ylabel('House Price ($100k)')
plt.title('Linear Regression Fit')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Loss during training
plt.subplot(1, 2, 2)
plt.plot(loss_history, color='green', linewidth=2)
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.title('Training Loss Over Time')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Calculate R-squared
ss_res = tf.reduce_sum(tf.square(y_train - y_pred_final))
ss_tot = tf.reduce_sum(tf.square(y_train - tf.reduce_mean(y_train)))
r_squared = 1 - (ss_res / ss_tot)
print(f"\nR-squared: {r_squared.numpy():.4f}")
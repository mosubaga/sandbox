import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_circles
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

print("Building Neural Network from Scratch")
print("=" * 50)

# =====================================================================
# STEP 1: ACTIVATION FUNCTIONS AND THEIR DERIVATIVES
# =====================================================================

class ActivationFunctions:
    """Collection of activation functions and their derivatives"""
    
    @staticmethod
    def sigmoid(x):
        """Sigmoid activation function"""
        # Clip x to prevent overflow
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))
    
    @staticmethod
    def sigmoid_derivative(x):
        """Derivative of sigmoid function"""
        s = ActivationFunctions.sigmoid(x)
        return s * (1 - s)
    
    @staticmethod
    def relu(x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    @staticmethod
    def relu_derivative(x):
        """Derivative of ReLU function"""
        return (x > 0).astype(float)
    
    @staticmethod
    def tanh(x):
        """Tanh activation function"""
        return np.tanh(x)
    
    @staticmethod
    def tanh_derivative(x):
        """Derivative of tanh function"""
        return 1 - np.tanh(x) ** 2

# =====================================================================
# STEP 2: NEURAL NETWORK CLASS
# =====================================================================

class NeuralNetwork:
    """A simple feedforward neural network built from scratch"""
    
    def __init__(self, layers, activation='sigmoid', learning_rate=0.01):
        """
        Initialize the neural network
        
        Args:
            layers: List of integers representing the number of neurons in each layer
            activation: Activation function to use ('sigmoid', 'relu', 'tanh')
            learning_rate: Learning rate for gradient descent
        """
        self.layers = layers
        self.learning_rate = learning_rate
        self.activation_name = activation
        
        # Set activation function
        if activation == 'sigmoid':
            self.activation = ActivationFunctions.sigmoid
            self.activation_derivative = ActivationFunctions.sigmoid_derivative
        elif activation == 'relu':
            self.activation = ActivationFunctions.relu
            self.activation_derivative = ActivationFunctions.relu_derivative
        elif activation == 'tanh':
            self.activation = ActivationFunctions.tanh
            self.activation_derivative = ActivationFunctions.tanh_derivative
        
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        
        # Xavier initialization for better training
        for i in range(len(layers) - 1):
            # Xavier initialization
            limit = np.sqrt(6 / (layers[i] + layers[i + 1]))
            w = np.random.uniform(-limit, limit, (layers[i], layers[i + 1]))
            b = np.zeros((1, layers[i + 1]))
            
            self.weights.append(w)
            self.biases.append(b)
        
        # Lists to store training history
        self.loss_history = []
        self.accuracy_history = []
    
    def forward_propagation(self, X):
        """
        Perform forward propagation through the network
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            activations: List of activations for each layer
            z_values: List of pre-activation values for each layer
        """
        activations = [X]
        z_values = []
        
        current_input = X
        
        for i in range(len(self.weights)):
            # Linear transformation: z = X * W + b
            z = np.dot(current_input, self.weights[i]) + self.biases[i]
            z_values.append(z)
            
            # Apply activation function (except for output layer in some cases)
            if i == len(self.weights) - 1:  # Output layer
                if self.layers[-1] == 1:  # Binary classification
                    a = ActivationFunctions.sigmoid(z)
                else:  # Multi-class classification (softmax)
                    a = self.softmax(z)
            else:  # Hidden layers
                a = self.activation(z)
            
            activations.append(a)
            current_input = a
        
        return activations, z_values
    
    def softmax(self, x):
        """Softmax activation for multi-class classification"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def backward_propagation(self, X, y, activations, z_values):
        """
        Perform backward propagation to compute gradients
        
        Args:
            X: Input data
            y: True labels
            activations: Activations from forward propagation
            z_values: Pre-activation values from forward propagation
            
        Returns:
            weight_gradients: Gradients for weights
            bias_gradients: Gradients for biases
        """
        m = X.shape[0]  # Number of samples
        
        weight_gradients = []
        bias_gradients = []
        
        # Calculate error for output layer
        if self.layers[-1] == 1:  # Binary classification
            delta = activations[-1] - y.reshape(-1, 1)
        else:  # Multi-class classification
            # Convert labels to one-hot encoding
            y_one_hot = np.eye(self.layers[-1])[y]
            delta = activations[-1] - y_one_hot
        
        # Backward pass through all layers
        for i in reversed(range(len(self.weights))):
            # Calculate gradients
            dW = np.dot(activations[i].T, delta) / m
            db = np.mean(delta, axis=0, keepdims=True)
            
            weight_gradients.insert(0, dW)
            bias_gradients.insert(0, db)
            
            # Calculate delta for previous layer (if not input layer)
            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * self.activation_derivative(z_values[i-1])
        
        return weight_gradients, bias_gradients
    
    def update_parameters(self, weight_gradients, bias_gradients):
        """Update weights and biases using gradients"""
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * weight_gradients[i]
            self.biases[i] -= self.learning_rate * bias_gradients[i]
    
    def compute_loss(self, y_true, y_pred):
        """Compute loss (cross-entropy)"""
        m = y_true.shape[0]
        
        if self.layers[-1] == 1:  # Binary classification
            # Binary cross-entropy
            y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)  # Avoid log(0)
            loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        else:  # Multi-class classification
            # Categorical cross-entropy
            y_true_one_hot = np.eye(self.layers[-1])[y_true]
            y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
            loss = -np.mean(np.sum(y_true_one_hot * np.log(y_pred), axis=1))
        
        return loss
    
    def predict(self, X):
        """Make predictions on new data"""
        activations, _ = self.forward_propagation(X)
        predictions = activations[-1]
        
        if self.layers[-1] == 1:  # Binary classification
            return (predictions > 0.5).astype(int).flatten()
        else:  # Multi-class classification
            return np.argmax(predictions, axis=1)
    
    def predict_proba(self, X):
        """Get prediction probabilities"""
        activations, _ = self.forward_propagation(X)
        return activations[-1]
    
    def fit(self, X, y, epochs=1000, verbose=True):
        """
        Train the neural network
        
        Args:
            X: Training data
            y: Training labels
            epochs: Number of training epochs
            verbose: Whether to print training progress
        """
        for epoch in range(epochs):
            # Forward propagation
            activations, z_values = self.forward_propagation(X)
            
            # Compute loss
            loss = self.compute_loss(y, activations[-1])
            self.loss_history.append(loss)
            
            # Compute accuracy
            predictions = self.predict(X)
            accuracy = np.mean(predictions == y)
            self.accuracy_history.append(accuracy)
            
            # Backward propagation
            weight_gradients, bias_gradients = self.backward_propagation(X, y, activations, z_values)
            
            # Update parameters
            self.update_parameters(weight_gradients, bias_gradients)
            
            # Print progress
            if verbose and (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss:.4f} - Accuracy: {accuracy:.4f}")

# =====================================================================
# STEP 3: DEMONSTRATION WITH DIFFERENT DATASETS
# =====================================================================

def demonstrate_binary_classification():
    """Demonstrate binary classification"""
    print("\n" + "=" * 50)
    print("BINARY CLASSIFICATION EXAMPLE")
    print("=" * 50)
    
    # Generate dataset
    X, y = make_classification(n_samples=1000, n_features=2, n_redundant=0, 
                             n_informative=2, n_clusters_per_class=1, random_state=42)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train network
    nn = NeuralNetwork(layers=[2, 10, 8, 1], activation='sigmoid', learning_rate=0.1)
    print(f"Network architecture: {nn.layers}")
    print(f"Activation function: {nn.activation_name}")
    
    nn.fit(X_train, y_train, epochs=1000, verbose=True)
    
    # Make predictions
    train_predictions = nn.predict(X_train)
    test_predictions = nn.predict(X_test)
    
    train_accuracy = np.mean(train_predictions == y_train)
    test_accuracy = np.mean(test_predictions == y_test)
    
    print(f"\nFinal Results:")
    print(f"Training Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    return nn, X_train, X_test, y_train, y_test

def demonstrate_multiclass_classification():
    """Demonstrate multi-class classification"""
    print("\n" + "=" * 50)
    print("MULTI-CLASS CLASSIFICATION EXAMPLE")
    print("=" * 50)
    
    # Generate dataset
    X, y = make_classification(n_samples=1000, n_features=2, n_redundant=0, 
                             n_informative=2, n_classes=3, n_clusters_per_class=1, random_state=42)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train network
    nn = NeuralNetwork(layers=[2, 15, 10, 3], activation='relu', learning_rate=0.01)
    print(f"Network architecture: {nn.layers}")
    print(f"Activation function: {nn.activation_name}")
    
    nn.fit(X_train, y_train, epochs=1500, verbose=True)
    
    # Make predictions
    train_predictions = nn.predict(X_train)
    test_predictions = nn.predict(X_test)
    
    train_accuracy = np.mean(train_predictions == y_train)
    test_accuracy = np.mean(test_predictions == y_test)
    
    print(f"\nFinal Results:")
    print(f"Training Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    return nn, X_train, X_test, y_train, y_test

def demonstrate_nonlinear_classification():
    """Demonstrate non-linear classification with circles dataset"""
    print("\n" + "=" * 50)
    print("NON-LINEAR CLASSIFICATION EXAMPLE (CIRCLES)")
    print("=" * 50)
    
    # Generate circles dataset
    X, y = make_circles(n_samples=1000, noise=0.1, factor=0.3, random_state=42)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train network with more hidden layers for non-linear patterns
    nn = NeuralNetwork(layers=[2, 20, 15, 10, 1], activation='tanh', learning_rate=0.1)
    print(f"Network architecture: {nn.layers}")
    print(f"Activation function: {nn.activation_name}")
    
    nn.fit(X_train, y_train, epochs=2000, verbose=True)
    
    # Make predictions
    train_predictions = nn.predict(X_train)
    test_predictions = nn.predict(X_test)
    
    train_accuracy = np.mean(train_predictions == y_train)
    test_accuracy = np.mean(test_predictions == y_test)
    
    print(f"\nFinal Results:")
    print(f"Training Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    return nn, X_train, X_test, y_train, y_test

# =====================================================================
# STEP 4: VISUALIZATION FUNCTIONS
# =====================================================================

def plot_decision_boundary(nn, X, y, title="Decision Boundary"):
    """Plot the decision boundary of the neural network"""
    plt.figure(figsize=(10, 8))
    
    # Create a mesh to plot the decision boundary
    h = 0.01
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # Make predictions on the mesh
    mesh_points = np.c_[xx.ravel(), yy.ravel()]
    if nn.layers[-1] == 1:  # Binary classification
        Z = nn.predict_proba(mesh_points)
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, levels=50, alpha=0.6, cmap='RdYlBu')
        plt.colorbar(label='Prediction Probability')
    else:  # Multi-class classification
        Z = nn.predict(mesh_points)
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, alpha=0.6, cmap='viridis')
        plt.colorbar(label='Predicted Class')
    
    # Plot the data points
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='black')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    
    if nn.layers[-1] > 1:
        plt.legend(*scatter.legend_elements(), title="Classes")

def plot_training_history(nn, title="Training History"):
    """Plot training loss and accuracy"""
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(nn.loss_history)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(nn.accuracy_history)
    plt.title('Training Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid(True, alpha=0.3)
    
    plt.suptitle(title)
    plt.tight_layout()

# =====================================================================
# STEP 5: RUN ALL DEMONSTRATIONS
# =====================================================================

def main():
    """Run all neural network demonstrations"""
    
    # Binary Classification
    nn1, X_train1, X_test1, y_train1, y_test1 = demonstrate_binary_classification()
    plot_decision_boundary(nn1, X_test1, y_test1, "Binary Classification - Decision Boundary")
    plt.show()
    plot_training_history(nn1, "Binary Classification - Training History")
    plt.show()
    
    # Multi-class Classification
    nn2, X_train2, X_test2, y_train2, y_test2 = demonstrate_multiclass_classification()
    plot_decision_boundary(nn2, X_test2, y_test2, "Multi-class Classification - Decision Boundary")
    plt.show()
    plot_training_history(nn2, "Multi-class Classification - Training History")
    plt.show()
    
    # Non-linear Classification
    nn3, X_train3, X_test3, y_train3, y_test3 = demonstrate_nonlinear_classification()
    plot_decision_boundary(nn3, X_test3, y_test3, "Non-linear Classification - Decision Boundary")
    plt.show()
    plot_training_history(nn3, "Non-linear Classification - Training History")
    plt.show()
    
    print("\n" + "=" * 60)
    print("NEURAL NETWORK FROM SCRATCH - COMPLETE!")
    print("=" * 60)
    print("\nKey Components Implemented:")
    print("1. Forward Propagation")
    print("2. Backward Propagation (Backpropagation)")
    print("3. Multiple Activation Functions (Sigmoid, ReLU, Tanh)")
    print("4. Xavier Weight Initialization")
    print("5. Cross-entropy Loss Functions")
    print("6. Gradient Descent Optimization")
    print("7. Support for Binary and Multi-class Classification")
    print("8. Decision Boundary Visualization")

if __name__ == "__main__":
    main()
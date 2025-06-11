import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def create_sample_data():
    """Create sample dataset for demonstration"""
    # Generate synthetic binary classification dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=2,
        n_redundant=0,
        n_informative=2,
        n_clusters_per_class=1,
        random_state=42
    )
    
    # Create DataFrame for easier handling
    df = pd.DataFrame(X, columns=['Feature_1', 'Feature_2'])
    df['Target'] = y
    
    return X, y, df

def plot_data(X, y):
    """Visualize the dataset"""
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter)
    plt.title('Original Dataset')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    
    return plt

def train_logistic_regression(X, y):
    """Train and evaluate logistic regression model"""
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale the features (recommended for logistic regression)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create and train the model
    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    return model, scaler, X_train_scaled, X_test_scaled, y_train, y_test, y_pred, y_pred_proba

def evaluate_model(y_test, y_pred, y_pred_proba):
    """Evaluate model performance"""
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.subplot(1, 2, 2)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    
    plt.tight_layout()
    plt.show()
    
    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()
    
    return accuracy, roc_auc

def plot_decision_boundary(model, scaler, X, y):
    """Plot decision boundary"""
    plt.figure(figsize=(10, 8))
    
    # Create a mesh
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # Make predictions on the mesh
    mesh_points = np.c_[xx.ravel(), yy.ravel()]
    mesh_points_scaled = scaler.transform(mesh_points)
    Z = model.predict_proba(mesh_points_scaled)[:, 1]
    Z = Z.reshape(xx.shape)
    
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, levels=50, alpha=0.8, cmap='RdYlBu')
    plt.colorbar(label='Probability of Class 1')
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap='RdYlBu', edgecolors='black')
    plt.title('Logistic Regression Decision Boundary')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

def model_interpretation(model, feature_names=None):
    """Interpret the model coefficients"""
    if feature_names is None:
        feature_names = [f'Feature_{i+1}' for i in range(len(model.coef_[0]))]
    
    print("\nModel Interpretation:")
    print(f"Intercept: {model.intercept_[0]:.4f}")
    print("\nFeature Coefficients:")
    for name, coef in zip(feature_names, model.coef_[0]):
        print(f"{name}: {coef:.4f}")
    
    # Plot feature importance
    plt.figure(figsize=(8, 6))
    coefficients = model.coef_[0]
    plt.barh(feature_names, coefficients)
    plt.xlabel('Coefficient Value')
    plt.title('Feature Coefficients in Logistic Regression')
    plt.grid(axis='x', alpha=0.3)
    plt.show()

def main():
    """Main function to run the logistic regression analysis"""
    print("Logistic Regression with Scikit-Learn")
    print("=" * 40)
    
    # Create sample data
    X, y, df = create_sample_data()
    print(f"Dataset shape: {X.shape}")
    print(f"Number of classes: {len(np.unique(y))}")
    print(f"Class distribution: {np.bincount(y)}")
    
    # Visualize data
    plot_data(X, y)
    
    # Train model
    model, scaler, X_train_scaled, X_test_scaled, y_train, y_test, y_pred, y_pred_proba = train_logistic_regression(X, y)
    
    # Evaluate model
    accuracy, roc_auc = evaluate_model(y_test, y_pred, y_pred_proba)
    
    # Plot decision boundary
    plot_decision_boundary(model, scaler, X, y)
    
    # Model interpretation
    model_interpretation(model)
    
    print(f"\nFinal Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC AUC: {roc_auc:.4f}")

if __name__ == "__main__":
    main()
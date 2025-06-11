import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def create_sample_data():
    """Create sample dataset for demonstration"""
    # Generate synthetic regression dataset
    X, y = make_regression(
        n_samples=1000,
        n_features=3,
        noise=10,
        random_state=42
    )
    
    # Create DataFrame for easier handling
    feature_names = ['Feature_1', 'Feature_2', 'Feature_3']
    df = pd.DataFrame(X, columns=feature_names)
    df['Target'] = y
    
    return X, y, df, feature_names

def explore_data(df):
    """Explore the dataset"""
    print("Dataset Overview:")
    print(f"Shape: {df.shape}")
    print(f"\nDataset Info:")
    print(df.info())
    print(f"\nDescriptive Statistics:")
    print(df.describe())
    
    # Correlation matrix
    plt.figure(figsize=(10, 8))
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.show()
    
    # Pairplot for feature relationships
    plt.figure(figsize=(12, 10))
    sns.pairplot(df, diag_kind='kde')
    plt.suptitle('Feature Relationships', y=1.02)
    plt.show()

def visualize_features(X, y, feature_names):
    """Visualize individual features vs target"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for i, (ax, feature) in enumerate(zip(axes, feature_names)):
        ax.scatter(X[:, i], y, alpha=0.6)
        ax.set_xlabel(feature)
        ax.set_ylabel('Target')
        ax.set_title(f'{feature} vs Target')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def train_linear_regression(X, y):
    """Train and evaluate linear regression model"""
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    return model, X_train, X_test, y_train, y_test, y_train_pred, y_test_pred

def evaluate_model(y_train, y_test, y_train_pred, y_test_pred):
    """Evaluate model performance"""
    
    # Calculate metrics for training set
    train_mse = mean_squared_error(y_train, y_train_pred)
    train_rmse = np.sqrt(train_mse)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    
    # Calculate metrics for test set
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    # Print results
    print("Model Performance:")
    print("=" * 50)
    print(f"{'Metric':<20} {'Training':<15} {'Test':<15}")
    print("-" * 50)
    print(f"{'MSE':<20} {train_mse:<15.4f} {test_mse:<15.4f}")
    print(f"{'RMSE':<20} {train_rmse:<15.4f} {test_rmse:<15.4f}")
    print(f"{'MAE':<20} {train_mae:<15.4f} {test_mae:<15.4f}")
    print(f"{'R²':<20} {train_r2:<15.4f} {test_r2:<15.4f}")
    
    return test_mse, test_rmse, test_mae, test_r2

def plot_predictions(y_train, y_test, y_train_pred, y_test_pred):
    """Plot actual vs predicted values"""
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Training set
    axes[0].scatter(y_train, y_train_pred, alpha=0.6, color='blue')
    axes[0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2)
    axes[0].set_xlabel('Actual Values')
    axes[0].set_ylabel('Predicted Values')
    axes[0].set_title('Training Set: Actual vs Predicted')
    axes[0].grid(True, alpha=0.3)
    
    # Test set
    axes[1].scatter(y_test, y_test_pred, alpha=0.6, color='green')
    axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[1].set_xlabel('Actual Values')
    axes[1].set_ylabel('Predicted Values')
    axes[1].set_title('Test Set: Actual vs Predicted')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_residuals(y_train, y_test, y_train_pred, y_test_pred):
    """Plot residuals for model diagnosis"""
    
    train_residuals = y_train - y_train_pred
    test_residuals = y_test - y_test_pred
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Residuals vs Predicted (Training)
    axes[0, 0].scatter(y_train_pred, train_residuals, alpha=0.6, color='blue')
    axes[0, 0].axhline(y=0, color='r', linestyle='--')
    axes[0, 0].set_xlabel('Predicted Values')
    axes[0, 0].set_ylabel('Residuals')
    axes[0, 0].set_title('Training: Residuals vs Predicted')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Residuals vs Predicted (Test)
    axes[0, 1].scatter(y_test_pred, test_residuals, alpha=0.6, color='green')
    axes[0, 1].axhline(y=0, color='r', linestyle='--')
    axes[0, 1].set_xlabel('Predicted Values')
    axes[0, 1].set_ylabel('Residuals')
    axes[0, 1].set_title('Test: Residuals vs Predicted')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Histogram of residuals (Training)
    axes[1, 0].hist(train_residuals, bins=30, alpha=0.7, color='blue', edgecolor='black')
    axes[1, 0].set_xlabel('Residuals')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Training: Distribution of Residuals')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Histogram of residuals (Test)
    axes[1, 1].hist(test_residuals, bins=30, alpha=0.7, color='green', edgecolor='black')
    axes[1, 1].set_xlabel('Residuals')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Test: Distribution of Residuals')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def model_interpretation(model, feature_names):
    """Interpret the model coefficients"""
    
    print("\nModel Interpretation:")
    print("=" * 30)
    print(f"Intercept: {model.intercept_:.4f}")
    print("\nFeature Coefficients:")
    for name, coef in zip(feature_names, model.coef_):
        print(f"{name}: {coef:.4f}")
    
    # Create regression equation
    equation = f"y = {model.intercept_:.4f}"
    for name, coef in zip(feature_names, model.coef_):
        sign = "+" if coef >= 0 else ""
        equation += f" {sign}{coef:.4f}*{name}"
    
    print(f"\nRegression Equation:")
    print(equation)
    
    # Plot feature importance (coefficients)
    plt.figure(figsize=(10, 6))
    coefficients = model.coef_
    plt.barh(feature_names, coefficients, color=['blue' if c >= 0 else 'red' for c in coefficients])
    plt.xlabel('Coefficient Value')
    plt.title('Feature Coefficients in Linear Regression')
    plt.grid(axis='x', alpha=0.3)
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    plt.show()

def feature_importance_analysis(X, y, model, feature_names):
    """Analyze feature importance through coefficient magnitude"""
    
    # Calculate absolute coefficients for importance ranking
    abs_coefficients = np.abs(model.coef_)
    feature_importance = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_,
        'Abs_Coefficient': abs_coefficients,
        'Importance_Rank': abs_coefficients.argsort()[::-1] + 1
    })
    
    feature_importance = feature_importance.sort_values('Abs_Coefficient', ascending=False)
    
    print("\nFeature Importance Analysis:")
    print("=" * 40)
    print(feature_importance)
    
    return feature_importance

def make_predictions(model, feature_names):
    """Make predictions on new data"""
    
    print("\nMaking Predictions on New Data:")
    print("=" * 35)
    
    # Create sample new data
    new_data = np.array([[1.5, -0.5, 2.0],
                        [0.0, 1.0, -1.0],
                        [-1.0, 0.5, 0.0]])
    
    predictions = model.predict(new_data)
    
    print(f"{'Sample':<10} {' '.join([f'{name:<12}' for name in feature_names])} {'Prediction':<12}")
    print("-" * 70)
    
    for i, (sample, pred) in enumerate(zip(new_data, predictions)):
        sample_str = ' '.join([f'{val:<12.2f}' for val in sample])
        print(f"Sample {i+1:<3} {sample_str} {pred:<12.2f}")

def main():
    """Main function to run the linear regression analysis"""
    print("Linear Regression with Scikit-Learn")
    print("=" * 40)
    
    # Create sample data
    X, y, df, feature_names = create_sample_data()
    
    # Explore data
    explore_data(df)
    
    # Visualize features
    visualize_features(X, y, feature_names)
    
    # Train model
    model, X_train, X_test, y_train, y_test, y_train_pred, y_test_pred = train_linear_regression(X, y)
    
    # Evaluate model
    test_mse, test_rmse, test_mae, test_r2 = evaluate_model(y_train, y_test, y_train_pred, y_test_pred)
    
    # Plot predictions
    plot_predictions(y_train, y_test, y_train_pred, y_test_pred)
    
    # Plot residuals
    plot_residuals(y_train, y_test, y_train_pred, y_test_pred)
    
    # Model interpretation
    model_interpretation(model, feature_names)
    
    # Feature importance analysis
    feature_importance = feature_importance_analysis(X, y, model, feature_names)
    
    # Make predictions on new data
    make_predictions(model, feature_names)
    
    print(f"\nFinal Model Summary:")
    print(f"Test R²: {test_r2:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")

if __name__ == "__main__":
    main()
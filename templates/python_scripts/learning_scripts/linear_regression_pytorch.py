import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
torch.manual_seed(42)
np.random.seed(42)

print("PyTorch Linear Regression Examples")
print("=" * 50)
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print()

# =====================================================================
# EXAMPLE 1: SIMPLE LINEAR REGRESSION (SINGLE FEATURE)
# =====================================================================

print("=" * 60)
print("EXAMPLE 1: SIMPLE LINEAR REGRESSION (SINGLE FEATURE)")
print("=" * 60)

# Generate simple dataset
np.random.seed(42)
X_simple = np.linspace(0, 10, 100).reshape(-1, 1)
y_simple = 2 * X_simple.flatten() + 1 + np.random.normal(0, 1, 100)

print(f"Dataset shape: X={X_simple.shape}, y={y_simple.shape}")

# Convert to PyTorch tensors
X_tensor = torch.FloatTensor(X_simple)
y_tensor = torch.FloatTensor(y_simple).view(-1, 1)

print(f"Tensor shapes: X={X_tensor.shape}, y={y_tensor.shape}")

# Method 1: Using nn.Linear
class SimpleLinearRegression(nn.Module):
    def __init__(self):
        super(SimpleLinearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)  # 1 input feature, 1 output
    
    def forward(self, x):
        return self.linear(x)

# Initialize model
model_simple = SimpleLinearRegression()
criterion = nn.MSELoss()
optimizer = optim.SGD(model_simple.parameters(), lr=0.01)

print("\nModel architecture:")
print(model_simple)
print(f"Initial parameters: Weight={model_simple.linear.weight.item():.4f}, Bias={model_simple.linear.bias.item():.4f}")

# Training loop
num_epochs = 1000
losses = []

for epoch in range(num_epochs):
    # Forward pass
    predictions = model_simple(X_tensor)
    loss = criterion(predictions, y_tensor)
    
    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    losses.append(loss.item())
    
    if (epoch + 1) % 200 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

print(f"\nFinal parameters: Weight={model_simple.linear.weight.item():.4f}, Bias={model_simple.linear.bias.item():.4f}")
print(f"True parameters: Weight=2.0000, Bias=1.0000")

# Make predictions
with torch.no_grad():
    y_pred_simple = model_simple(X_tensor).numpy()

# Calculate metrics
mse = mean_squared_error(y_simple, y_pred_simple.flatten())
r2 = r2_score(y_simple, y_pred_simple.flatten())
print(f"Mean Squared Error: {mse:.4f}")
print(f"R² Score: {r2:.4f}")

# =====================================================================
# EXAMPLE 2: MULTIPLE LINEAR REGRESSION
# =====================================================================

print("\n" + "=" * 60)
print("EXAMPLE 2: MULTIPLE LINEAR REGRESSION")
print("=" * 60)

# Generate multiple feature dataset
X_multi, y_multi = make_regression(n_samples=1000, n_features=5, noise=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_multi, y_multi, test_size=0.2, random_state=42)

print(f"Training set shape: X={X_train.shape}, y={y_train.shape}")
print(f"Test set shape: X={X_test.shape}, y={y_test.shape}")

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train_scaled)
y_train_tensor = torch.FloatTensor(y_train).view(-1, 1)
X_test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# Define model
class MultipleLinearRegression(nn.Module):
    def __init__(self, input_dim):
        super(MultipleLinearRegression, self).__init__()
        self.linear = nn.Linear(input_dim, 1)
        
    def forward(self, x):
        return self.linear(x)

# Initialize model
model_multi = MultipleLinearRegression(input_dim=5)
criterion = nn.MSELoss()
optimizer = optim.Adam(model_multi.parameters(), lr=0.01)

print("\nModel architecture:")
print(model_multi)

# Training loop
num_epochs = 1000
train_losses = []
val_losses = []

for epoch in range(num_epochs):
    # Training
    model_multi.train()
    train_pred = model_multi(X_train_tensor)
    train_loss = criterion(train_pred, y_train_tensor)
    
    optimizer.zero_grad()
    train_loss.backward()
    optimizer.step()
    
    # Validation
    model_multi.eval()
    with torch.no_grad():
        val_pred = model_multi(X_test_tensor)
        val_loss = criterion(val_pred, y_test_tensor)
    
    train_losses.append(train_loss.item())
    val_losses.append(val_loss.item())
    
    if (epoch + 1) % 200 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss.item():.4f}, Val Loss: {val_loss.item():.4f}')

# Final evaluation
model_multi.eval()
with torch.no_grad():
    y_train_pred = model_multi(X_train_tensor).numpy()
    y_test_pred = model_multi(X_test_tensor).numpy()

train_mse = mean_squared_error(y_train, y_train_pred.flatten())
test_mse = mean_squared_error(y_test, y_test_pred.flatten())
train_r2 = r2_score(y_train, y_train_pred.flatten())
test_r2 = r2_score(y_test, y_test_pred.flatten())

print(f"\nFinal Results:")
print(f"Training MSE: {train_mse:.4f}, R²: {train_r2:.4f}")
print(f"Test MSE: {test_mse:.4f}, R²: {test_r2:.4f}")

# =====================================================================
# EXAMPLE 3: POLYNOMIAL REGRESSION
# =====================================================================

print("\n" + "=" * 60)
print("EXAMPLE 3: POLYNOMIAL REGRESSION")
print("=" * 60)

# Generate non-linear dataset
np.random.seed(42)
X_poly = np.linspace(-2, 2, 200).reshape(-1, 1)
y_poly = 0.5 * X_poly.flatten()**3 + 0.3 * X_poly.flatten()**2 + 0.1 * X_poly.flatten() + np.random.normal(0, 0.1, 200)

print(f"Polynomial dataset shape: X={X_poly.shape}, y={y_poly.shape}")

# Create polynomial features
def create_polynomial_features(X, degree):
    """Create polynomial features up to given degree"""
    X_poly = np.ones((X.shape[0], 1))  # Bias term
    for i in range(1, degree + 1):
        X_poly = np.concatenate([X_poly, X**i], axis=1)
    return X_poly

degree = 3
X_poly_features = create_polynomial_features(X_poly, degree)
print(f"Polynomial features shape: {X_poly_features.shape}")

# Convert to tensors
X_poly_tensor = torch.FloatTensor(X_poly_features)
y_poly_tensor = torch.FloatTensor(y_poly).view(-1, 1)

# Define polynomial regression model
class PolynomialRegression(nn.Module):
    def __init__(self, input_dim):
        super(PolynomialRegression, self).__init__()
        self.linear = nn.Linear(input_dim, 1, bias=False)  # No bias since we have constant term
        
    def forward(self, x):
        return self.linear(x)

# Initialize and train model
model_poly = PolynomialRegression(input_dim=degree + 1)
criterion = nn.MSELoss()
optimizer = optim.Adam(model_poly.parameters(), lr=0.01)

print("\nTraining polynomial regression model...")
num_epochs = 2000
poly_losses = []

for epoch in range(num_epochs):
    predictions = model_poly(X_poly_tensor)
    loss = criterion(predictions, y_poly_tensor)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    poly_losses.append(loss.item())
    
    if (epoch + 1) % 400 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Make predictions
with torch.no_grad():
    y_poly_pred = model_poly(X_poly_tensor).numpy()

poly_mse = mean_squared_error(y_poly, y_poly_pred.flatten())
poly_r2 = r2_score(y_poly, y_poly_pred.flatten())
print(f"\nPolynomial Regression Results:")
print(f"MSE: {poly_mse:.4f}, R²: {poly_r2:.4f}")

# =====================================================================
# EXAMPLE 4: REGULARIZED LINEAR REGRESSION (RIDGE/LASSO)
# =====================================================================

print("\n" + "=" * 60)
print("EXAMPLE 4: REGULARIZED LINEAR REGRESSION")
print("=" * 60)

# Generate dataset with more features than samples (to show regularization benefit)
X_reg, y_reg = make_regression(n_samples=100, n_features=50, noise=10, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.3, random_state=42)

# Standardize
scaler_reg = StandardScaler()
X_train_reg_scaled = scaler_reg.fit_transform(X_train_reg)
X_test_reg_scaled = scaler_reg.transform(X_test_reg)

print(f"Regularization dataset: {X_train_reg.shape[0]} samples, {X_train_reg.shape[1]} features")

# Convert to tensors
X_train_reg_tensor = torch.FloatTensor(X_train_reg_scaled)
y_train_reg_tensor = torch.FloatTensor(y_train_reg).view(-1, 1)
X_test_reg_tensor = torch.FloatTensor(X_test_reg_scaled)
y_test_reg_tensor = torch.FloatTensor(y_test_reg).view(-1, 1)

# Define regularized regression model
class RegularizedLinearRegression(nn.Module):
    def __init__(self, input_dim):
        super(RegularizedLinearRegression, self).__init__()
        self.linear = nn.Linear(input_dim, 1)
        
    def forward(self, x):
        return self.linear(x)

# Train models with different regularization
def train_regularized_model(X_train, y_train, X_test, y_test, l1_lambda=0.0, l2_lambda=0.0, title=""):
    model = RegularizedLinearRegression(input_dim=X_train.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    losses = []
    
    for epoch in range(1000):
        predictions = model(X_train)
        loss = criterion(predictions, y_train)
        
        # Add regularization terms
        l1_reg = torch.tensor(0.0)
        l2_reg = torch.tensor(0.0)
        
        for param in model.parameters():
            l1_reg += torch.norm(param, p=1)
            l2_reg += torch.norm(param, p=2)
        
        total_loss = loss + l1_lambda * l1_reg + l2_lambda * l2_reg
        
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        
        losses.append(total_loss.item())
    
    # Evaluate
    model.eval()
    with torch.no_grad():
        train_pred = model(X_train).numpy()
        test_pred = model(X_test).numpy()
    
    train_mse = mean_squared_error(y_train.numpy(), train_pred.flatten())
    test_mse = mean_squared_error(y_test.numpy(), test_pred.flatten())
    
    print(f"{title}:")
    print(f"  Training MSE: {train_mse:.4f}")
    print(f"  Test MSE: {test_mse:.4f}")
    
    return model, losses, test_mse

# Train different models
print("\nTraining regularized models...")
model_normal, losses_normal, _ = train_regularized_model(
    X_train_reg_tensor, y_train_reg_tensor, X_test_reg_tensor, y_test_reg_tensor, 
    title="No Regularization"
)

model_ridge, losses_ridge, _ = train_regularized_model(
    X_train_reg_tensor, y_train_reg_tensor, X_test_reg_tensor, y_test_reg_tensor, 
    l2_lambda=0.1, title="Ridge Regression (L2)"
)

model_lasso, losses_lasso, _ = train_regularized_model(
    X_train_reg_tensor, y_train_reg_tensor, X_test_reg_tensor, y_test_reg_tensor, 
    l1_lambda=0.01, title="Lasso Regression (L1)"
)

# =====================================================================
# VISUALIZATION
# =====================================================================

print("\n" + "=" * 60)
print("CREATING VISUALIZATIONS")
print("=" * 60)

# Create comprehensive visualization
fig, axes = plt.subplots(3, 3, figsize=(18, 15))

# Simple Linear Regression
axes[0, 0].scatter(X_simple.flatten(), y_simple, alpha=0.6, label='Data')
axes[0, 0].plot(X_simple.flatten(), y_pred_simple.flatten(), 'r-', linewidth=2, label='Prediction')
axes[0, 0].set_title('Simple Linear Regression')
axes[0, 0].set_xlabel('X')
axes[0, 0].set_ylabel('y')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(losses)
axes[0, 1].set_title('Simple Regression - Training Loss')
axes[0, 1].set_xlabel('Epoch')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].grid(True, alpha=0.3)

# Multiple Linear Regression
axes[0, 2].plot(train_losses, label='Training Loss')
axes[0, 2].plot(val_losses, label='Validation Loss')
axes[0, 2].set_title('Multiple Regression - Training History')
axes[0, 2].set_xlabel('Epoch')
axes[0, 2].set_ylabel('Loss')
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

# Multiple Regression Predictions vs Actual
axes[1, 0].scatter(y_test, y_test_pred.flatten(), alpha=0.6)
axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
axes[1, 0].set_title('Multiple Regression: Predictions vs Actual')
axes[1, 0].set_xlabel('Actual')
axes[1, 0].set_ylabel('Predicted')
axes[1, 0].grid(True, alpha=0.3)

# Polynomial Regression
sort_idx = np.argsort(X_poly.flatten())
axes[1, 1].scatter(X_poly.flatten(), y_poly, alpha=0.6, label='Data')
axes[1, 1].plot(X_poly.flatten()[sort_idx], y_poly_pred.flatten()[sort_idx], 'r-', linewidth=2, label='Prediction')
axes[1, 1].set_title('Polynomial Regression')
axes[1, 1].set_xlabel('X')
axes[1, 1].set_ylabel('y')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].plot(poly_losses)
axes[1, 2].set_title('Polynomial Regression - Training Loss')
axes[1, 2].set_xlabel('Epoch')
axes[1, 2].set_ylabel('Loss')
axes[1, 2].grid(True, alpha=0.3)

# Regularization comparison
axes[2, 0].plot(losses_normal, label='No Regularization')
axes[2, 0].plot(losses_ridge, label='Ridge (L2)')
axes[2, 0].plot(losses_lasso, label='Lasso (L1)')
axes[2, 0].set_title('Regularization - Training Loss Comparison')
axes[2, 0].set_xlabel('Epoch')
axes[2, 0].set_ylabel('Loss')
axes[2, 0].legend()
axes[2, 0].grid(True, alpha=0.3)

# Feature importance comparison
def get_feature_importance(model):
    return torch.abs(model.linear.weight).detach().numpy().flatten()

importance_normal = get_feature_importance(model_normal)
importance_ridge = get_feature_importance(model_ridge)
importance_lasso = get_feature_importance(model_lasso)

x_pos = np.arange(len(importance_normal))
width = 0.25

axes[2, 1].bar(x_pos - width, importance_normal[:10], width, label='No Reg', alpha=0.7)
axes[2, 1].bar(x_pos, importance_ridge[:10], width, label='Ridge', alpha=0.7)
axes[2, 1].bar(x_pos + width, importance_lasso[:10], width, label='Lasso', alpha=0.7)
axes[2, 1].set_title('Feature Importance (First 10 Features)')
axes[2, 1].set_xlabel('Feature Index')
axes[2, 1].set_ylabel('Absolute Weight')
axes[2, 1].legend()
axes[2, 1].grid(True, alpha=0.3)

# Model comparison summary
models = ['Simple', 'Multiple', 'Polynomial', 'Ridge', 'Lasso']
test_errors = [mse, test_mse, poly_mse, 
               mean_squared_error(y_test_reg, model_ridge(X_test_reg_tensor).detach().numpy().flatten()),
               mean_squared_error(y_test_reg, model_lasso(X_test_reg_tensor).detach().numpy().flatten())]

axes[2, 2].bar(models, test_errors, color=['skyblue', 'lightgreen', 'lightcoral', 'gold', 'plum'], alpha=0.7)
axes[2, 2].set_title('Model Comparison - Test MSE')
axes[2, 2].set_ylabel('Mean Squared Error')
axes[2, 2].tick_params(axis='x', rotation=45)
axes[2, 2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("PYTORCH LINEAR REGRESSION EXAMPLES COMPLETED!")
print("=" * 60)
print("\nSummary of Examples:")
print("1. Simple Linear Regression: Single feature, basic PyTorch implementation")
print("2. Multiple Linear Regression: Multiple features with train/test split")
print("3. Polynomial Regression: Non-linear relationship modeling")
print("4. Regularized Regression: Ridge and Lasso for overfitting prevention")
print("\nKey PyTorch Concepts Demonstrated:")
print("- nn.Module and nn.Linear")
print("- Forward and backward passes")
print("- Different optimizers (SGD, Adam)")
print("- Loss functions (MSELoss)")
print("- Gradient computation and parameter updates")
print("- Model evaluation and prediction")
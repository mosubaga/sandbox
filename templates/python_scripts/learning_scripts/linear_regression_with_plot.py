import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Create sample data points
X = np.array([1, 2, 3, 4, 5, 6, 7]).reshape(-1, 1)  # Independent variable (reshaped for sklearn)
y = np.array([2.1, 3.9, 6.2, 8.1, 9.8, 12.2, 14.1])  # Dependent variable

# Create and fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Generate points for a smooth line
X_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_line = model.predict(X_line)

# Calculate R-squared score
r2 = r2_score(y, y_pred)

# Create the plot
plt.figure(figsize=(10, 6))

# Plot original data points
plt.scatter(X, y, color='red', s=100, alpha=0.7, label='Original Data Points')

# Plot regression line
plt.plot(X_line, y_line, color='blue', linewidth=2, label=f'Regression Line (R² = {r2:.3f})')

# Add labels and title
plt.xlabel('X (Independent Variable)')
plt.ylabel('Y (Dependent Variable)')
plt.title('Linear Regression Analysis')
plt.legend()
plt.grid(True, alpha=0.3)

# Display equation on the plot
equation = f'y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}'
plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
         fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()

# Print results
print(f"Linear Regression Results:")
print(f"Slope (coefficient): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"R-squared score: {r2:.4f}")
print(f"Equation: y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}")


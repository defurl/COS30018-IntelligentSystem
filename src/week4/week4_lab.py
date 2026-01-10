"""
Week 4 Lab: Linear Regression with scikit-learn
=================================================

This lab demonstrates:
1. Loading and exploring the California Housing dataset
2. Training a Linear Regression model
3. Evaluating model performance with MSE and R² score
4. Visualizing predictions vs actual values
5. Understanding feature coefficients

To run:
    conda activate is_labs
    python src/week4/week4_lab.py
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ============================================
# WEEK 4 LAB: LINEAR REGRESSION
# ============================================

print("=" * 50)
print("   WEEK 4 LAB: Linear Regression")
print("=" * 50)

# ------------------------------------------
# 1. Load the Dataset
# ------------------------------------------
print("\n[1] Loading California Housing Dataset...")
data = fetch_california_housing()
X = data.data
y = data.target
feature_names = data.feature_names

print(f"    Dataset shape: {X.shape}")
print(f"    Number of samples: {X.shape[0]}")
print(f"    Number of features: {X.shape[1]}")
print(f"    Features: {feature_names}")
print(f"    Target: Median house value (in $100k)")

# ------------------------------------------
# 2. Split into Training and Test Sets
# ------------------------------------------
print("\n[2] Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"    Training samples: {X_train.shape[0]}")
print(f"    Test samples: {X_test.shape[0]}")

# ------------------------------------------
# 3. Train the Model
# ------------------------------------------
print("\n[3] Training Linear Regression model...")
model = LinearRegression()
model.fit(X_train, y_train)
print("    Model trained successfully!")

# Display learned coefficients
print("\n    Learned Coefficients:")
for name, coef in zip(feature_names, model.coef_):
    print(f"      {name:12s}: {coef:+.4f}")
print(f"      {'Intercept':12s}: {model.intercept_:+.4f}")

# ------------------------------------------
# 4. Evaluate the Model
# ------------------------------------------
print("\n[4] Evaluating model performance...")

# Predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Metrics
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f"\n    Training Set:")
print(f"      MSE  = {train_mse:.4f}")
print(f"      RMSE = {np.sqrt(train_mse):.4f}")
print(f"      R²   = {train_r2:.4f}")

print(f"\n    Test Set:")
print(f"      MSE  = {test_mse:.4f}")
print(f"      RMSE = {np.sqrt(test_mse):.4f}")
print(f"      R²   = {test_r2:.4f}")

# ------------------------------------------
# 5. Visualize Results
# ------------------------------------------
print("\n[5] Creating visualizations...")

# Create a figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Predicted vs Actual
ax1.scatter(y_test, y_test_pred, alpha=0.3, s=10)
ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax1.set_xlabel('Actual Values ($100k)')
ax1.set_ylabel('Predicted Values ($100k)')
ax1.set_title('Predicted vs Actual House Values')
ax1.grid(True, alpha=0.3)

# Add R² annotation
ax1.text(0.05, 0.95, f'R² = {test_r2:.3f}\nRMSE = {np.sqrt(test_mse):.3f}',
         transform=ax1.transAxes, fontsize=12, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Subplot 2: Feature Importance (Coefficients)
sorted_idx = np.argsort(np.abs(model.coef_))
ax2.barh(range(len(sorted_idx)), model.coef_[sorted_idx], color='steelblue')
ax2.set_yticks(range(len(sorted_idx)))
ax2.set_yticklabels([feature_names[i] for i in sorted_idx])
ax2.set_xlabel('Coefficient Value')
ax2.set_title('Feature Coefficients (Importance)')
ax2.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('src/week4/week4_linear_regression_results.png', dpi=100)
print("    Saved: src/week4/week4_linear_regression_results.png")

# ------------------------------------------
# 6. Sample Predictions
# ------------------------------------------
print("\n[6] Sample Predictions:")
print("    Idx  |  Actual  | Predicted |  Error")
print("    " + "-" * 42)
for i in range(5):
    actual = y_test[i]
    predicted = y_test_pred[i]
    error = predicted - actual
    print(f"    {i:3d}  |  {actual:6.2f}  |   {predicted:6.2f}  |  {error:+.2f}")

# ------------------------------------------
# Summary
# ------------------------------------------
print("\n" + "=" * 50)
print("   WEEK 4 LAB COMPLETE!")
print("=" * 50)
print(f"\n   Key Takeaways:")
print(f"   • Linear regression models relationship: y = w·X + b")
print(f"   • MSE measures average squared prediction error")
print(f"   • R² indicates how much variance is explained (higher=better)")
print(f"   • This model explains {test_r2*100:.1f}% of house price variance")
print()

# Show the plot (optional - uncomment if you want to display)
# plt.show()

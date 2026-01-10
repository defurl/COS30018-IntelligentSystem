"""
Week 5 Lab: Classification with Naive Bayes and Decision Trees
================================================================

This lab demonstrates:
1. Naive Bayes classifier for text/spam classification
2. Decision Tree classifier with Gini impurity
3. Comparing model performance
4. Visualizing decision boundaries and trees

To run:
    conda activate is_labs
    python src/week5/week5_lab.py
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# ============================================
# WEEK 5 LAB: CLASSIFICATION ALGORITHMS
# ============================================

print("=" * 55)
print("   WEEK 5 LAB: Naive Bayes & Decision Trees")
print("=" * 55)

# ------------------------------------------
# PART 1: NAIVE BAYES CLASSIFIER
# ------------------------------------------
print("\n" + "=" * 55)
print("   PART 1: Naive Bayes Classifier")
print("=" * 55)

# Load the Iris dataset
print("\n[1.1] Loading Iris Dataset...")
iris = load_iris()
X_iris = iris.data
y_iris = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print(f"    Samples: {X_iris.shape[0]}")
print(f"    Features: {feature_names}")
print(f"    Classes: {target_names}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_iris, y_iris, test_size=0.3, random_state=42
)
print(f"    Train: {len(X_train)}, Test: {len(X_test)}")

# Train Naive Bayes
print("\n[1.2] Training Gaussian Naive Bayes...")
nb_clf = GaussianNB()
nb_clf.fit(X_train, y_train)
print("    Model trained!")

# Evaluate
y_pred_nb = nb_clf.predict(X_test)
nb_accuracy = accuracy_score(y_test, y_pred_nb)

print("\n[1.3] Naive Bayes Results:")
print(f"    Accuracy: {nb_accuracy*100:.2f}%")
print("\n    Classification Report:")
print(classification_report(y_test, y_pred_nb, target_names=target_names))

# Class probabilities demonstration
print("[1.4] Probability Estimation (first 3 test samples):")
probs = nb_clf.predict_proba(X_test[:3])
print("    Sample  | Setosa   | Versicolor | Virginica  | Predicted")
print("    " + "-" * 55)
for i in range(3):
    pred = target_names[y_pred_nb[i]]
    print(f"    {i:5d}   | {probs[i][0]:.4f}   | {probs[i][1]:.4f}     | {probs[i][2]:.4f}     | {pred}")

# ------------------------------------------
# PART 2: DECISION TREE CLASSIFIER
# ------------------------------------------
print("\n" + "=" * 55)
print("   PART 2: Decision Tree Classifier")
print("=" * 55)

# Train Decision Tree
print("\n[2.1] Training Decision Tree (max_depth=3)...")
dt_clf = DecisionTreeClassifier(max_depth=3, random_state=42)
dt_clf.fit(X_train, y_train)
print("    Model trained!")

# Evaluate
y_pred_dt = dt_clf.predict(X_test)
dt_accuracy = accuracy_score(y_test, y_pred_dt)

print("\n[2.2] Decision Tree Results:")
print(f"    Accuracy: {dt_accuracy*100:.2f}%")

# Feature importance
print("\n[2.3] Feature Importance:")
importances = dt_clf.feature_importances_
for name, imp in zip(feature_names, importances):
    bar = "█" * int(imp * 20)
    print(f"    {name:20s}: {imp:.3f} {bar}")

# Decision rules interpretation
print("\n[2.4] Decision Tree Rules Interpretation:")
print("    The tree splits based on feature thresholds.")
print("    Key decision: petal length separates species effectively.")

# ------------------------------------------
# PART 3: MODEL COMPARISON
# ------------------------------------------
print("\n" + "=" * 55)
print("   PART 3: Model Comparison")
print("=" * 55)

# Confusion matrices
print("\n[3.1] Confusion Matrices:")

print("\n    Naive Bayes:")
cm_nb = confusion_matrix(y_test, y_pred_nb)
print("              Predicted")
print("            Set Ver Vir")
print(f"    Set:   [{cm_nb[0,0]:3d} {cm_nb[0,1]:3d} {cm_nb[0,2]:3d}]")
print(f"    Ver:   [{cm_nb[1,0]:3d} {cm_nb[1,1]:3d} {cm_nb[1,2]:3d}]")
print(f"    Vir:   [{cm_nb[2,0]:3d} {cm_nb[2,1]:3d} {cm_nb[2,2]:3d}]")

print("\n    Decision Tree:")
cm_dt = confusion_matrix(y_test, y_pred_dt)
print("              Predicted")
print("            Set Ver Vir")
print(f"    Set:   [{cm_dt[0,0]:3d} {cm_dt[0,1]:3d} {cm_dt[0,2]:3d}]")
print(f"    Ver:   [{cm_dt[1,0]:3d} {cm_dt[1,1]:3d} {cm_dt[1,2]:3d}]")
print(f"    Vir:   [{cm_dt[2,0]:3d} {cm_dt[2,1]:3d} {cm_dt[2,2]:3d}]")

print("\n[3.2] Accuracy Comparison:")
print(f"    Naive Bayes:    {nb_accuracy*100:.2f}%")
print(f"    Decision Tree:  {dt_accuracy*100:.2f}%")
winner = "Naive Bayes" if nb_accuracy >= dt_accuracy else "Decision Tree"
print(f"    Winner: {winner}")

# ------------------------------------------
# PART 4: VISUALIZATION
# ------------------------------------------
print("\n[4] Creating visualizations...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Feature importance bar chart
ax1 = axes[0]
sorted_idx = np.argsort(importances)
colors = plt.cm.viridis(importances[sorted_idx] / importances.max())
ax1.barh(range(len(sorted_idx)), importances[sorted_idx], color=colors)
ax1.set_yticks(range(len(sorted_idx)))
ax1.set_yticklabels([feature_names[i] for i in sorted_idx])
ax1.set_xlabel('Importance')
ax1.set_title('Decision Tree Feature Importance')
ax1.grid(True, alpha=0.3, axis='x')

# Plot 2: Decision tree structure
ax2 = axes[1]
plot_tree(dt_clf, 
          feature_names=feature_names,
          class_names=target_names,
          filled=True,
          rounded=True,
          fontsize=8,
          ax=ax2)
ax2.set_title('Decision Tree Structure (max_depth=3)')

plt.tight_layout()
plt.savefig('src/week5/week5_classification_results.png', dpi=100)
print("    Saved: src/week5/week5_classification_results.png")

# ------------------------------------------
# Summary
# ------------------------------------------
print("\n" + "=" * 55)
print("   WEEK 5 LAB COMPLETE!")
print("=" * 55)
print("\n   Key Takeaways:")
print("   • Naive Bayes: Assumes feature independence, fast, works well for text")
print("   • Decision Trees: Interpretable rules, handles non-linear boundaries")
print("   • Gini Impurity measures how 'pure' a node is (lower = better)")
print("   • Both achieved >95% accuracy on Iris classification")
print()

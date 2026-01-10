# Week 5: Classification & Generative Models

## 📌 Core Concepts

This week covers classification algorithms: discriminative vs generative approaches.

---

## 🎯 Discriminative vs Generative

```
┌─────────────────────┬─────────────────────┐
│   DISCRIMINATIVE    │     GENERATIVE      │
├─────────────────────┼─────────────────────┤
│ Models P(y|x)       │ Models P(x|y)·P(y)  │
│ Learn decision      │ Learn class         │
│ boundary directly   │ distributions       │
├─────────────────────┼─────────────────────┤
│ Examples:           │ Examples:           │
│ - Logistic Reg      │ - Naive Bayes       │
│ - SVM               │ - GDA               │
│ - Neural Networks   │ - HMMs              │
└─────────────────────┴─────────────────────┘
```

---

## 📊 Logistic Regression

### Sigmoid Function

```
σ(z) = 1 / (1 + e⁻ᶻ)

where z = w·x + b
```

### Prediction

```
P(y=1|x) = σ(w·x + b)
```

### Loss Function (Binary Cross-Entropy)

```
L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```

---

## 🔔 Gaussian Discriminant Analysis (GDA)

### Assumptions

- P(x|y=0) ~ N(μ₀, Σ)
- P(x|y=1) ~ N(μ₁, Σ)

### Classification via Bayes Rule

```
P(y=1|x) = P(x|y=1)·P(y=1) / P(x)
```

---

## 🎲 Naïve Bayes

### Key Assumption

Features are conditionally independent given class:

```
P(x₁,x₂,...,xₙ|y) = ∏ P(xᵢ|y)
```

### Classification

```
ŷ = argmax P(y) · ∏ P(xᵢ|y)
         y
```

---

## 📧 Naïve Bayes for Text (Spam Detection)

```mermaid
graph LR
    E[Email] --> FV[Feature Vector]
    FV --> |"word ∈ email"| NB[Naïve Bayes]
    NB --> S[Spam?]
```

### Feature Vector Example

```
x = [1, 0, 0, 1, ...]
    │     │
    │     └── "aardvark" NOT present
    └── "a" IS present
```

---

## 📐 PCA (Principal Component Analysis)

### Purpose

Dimensionality reduction while preserving variance.

### Process

```
1. Standardize data
2. Compute covariance matrix
3. Find eigenvectors/eigenvalues
4. Project onto top k components
```

### Visualization

```
High-dim data → PCA → Low-dim representation
   (n features)         (k < n features)
```

---

## ⚖️ GDA vs Logistic Regression

| Aspect              | GDA                    | Logistic Regression |
| ------------------- | ---------------------- | ------------------- |
| **Assumptions**     | Gaussian distributions | None on P(x\|y)     |
| **Data efficiency** | Better with less data  | Needs more data     |
| **Robustness**      | Sensitive to outliers  | More robust         |
| **Flexibility**     | Less flexible          | More flexible       |

---

## 🎯 Project Relevance

- **Traffic Flow**: Classify traffic states
- **Pattern Recognition**: Identify congestion patterns

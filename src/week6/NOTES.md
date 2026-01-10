# Week 6: Artificial Neural Networks & Deep Learning

## 📌 Core Concept

Neural networks are computational models inspired by biological neurons.

---

## 🧠 Single Neuron (Perceptron)

```
        ┌─────────┐
x₁ ──w₁──►│         │
x₂ ──w₂──►│  Σ → f  │──► y
x₃ ──w₃──►│         │
        └─────────┘
           ↑
           b (bias)

y = f(Σ wᵢxᵢ + b)
```

---

## ⚡ Activation Functions

| Function    | Formula           | Use Case           |
| ----------- | ----------------- | ------------------ |
| **Sigmoid** | 1/(1+e⁻ᶻ)         | Binary output      |
| **Tanh**    | (eᶻ-e⁻ᶻ)/(eᶻ+e⁻ᶻ) | Hidden layers      |
| **ReLU**    | max(0, z)         | Most common        |
| **Softmax** | eᶻⁱ/Σeᶻʲ          | Multi-class output |

---

## 🏗️ Network Architecture

```
Input Layer    Hidden Layers    Output Layer
    ○              ○  ○              ○
    ○              ○  ○              ○
    ○      →       ○  ○      →       ○
    ○              ○  ○
    ○              ○  ○
  (n=400)       (layers)          (k=10)
```

---

## 📉 Training Process

### Forward Pass

```
Z[l] = W[l] · A[l-1] + b[l]
A[l] = g(Z[l])
```

### Cost Function (Cross-Entropy)

```
J(W) = -(1/m) Σ [y·log(ŷ) + (1-y)·log(1-ŷ)]
```

### Backpropagation

```
∂J/∂W[l] = (∂J/∂A[l]) · (∂A[l]/∂Z[l]) · (∂Z[l]/∂W[l])
```

---

## 🔄 Gradient Descent

```
Repeat until convergence:
    W := W - α · ∂J/∂W
    b := b - α · ∂J/∂b
```

---

## 📊 Multiclass Classification

### Softmax Output

```
ŷᵢ = eᶻⁱ / Σⱼ eᶻʲ

Σ ŷᵢ = 1 (probabilities sum to 1)
```

### Loss (Categorical Cross-Entropy)

```
L = -Σ yᵢ · log(ŷᵢ)
```

---

## 🚀 Why Deep Learning Now?

```
┌────────────────────────────────────┐
│ • Better algorithms & understanding │
│ • Computing power (GPUs, TPUs)     │
│ • Big data availability            │
│ • Open-source tools & models       │
└────────────────────────────────────┘
```

---

## 🛠️ Frameworks

| Framework        | Organization | Language |
| ---------------- | ------------ | -------- |
| **TensorFlow**   | Google       | Python   |
| **PyTorch**      | Meta         | Python   |
| **Keras**        | (TF wrapper) | Python   |
| **Scikit-learn** | Community    | Python   |

---

## ⚠️ Neural Network Challenges

| Issue                   | Solution                   |
| ----------------------- | -------------------------- |
| **Vanishing gradients** | ReLU, batch norm           |
| **Overfitting**         | Dropout, regularization    |
| **Black box**           | Explainable AI techniques  |
| **Computational cost**  | GPUs, distributed training |

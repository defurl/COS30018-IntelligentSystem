# COS30018 Lab Completion Overview

## Labs Completed ✅

| Week | Topic              | File Created                             | Result                      |
| ---- | ------------------ | ---------------------------------------- | --------------------------- |
| 1    | JADE Setup         | `Week1Lab.java`                          | AID, lifecycle demo         |
| 2    | Containers         | `Week2Lab.java`                          | ACLMessage, CyclicBehaviour |
| 3    | Book Trading       | `Week3Lab.java`, `Week3SellerAgent.java` | DF service, CNP             |
| 4    | Linear Regression  | `week4_lab.py`                           | R² = 0.576                  |
| 5    | Classification     | `week5_lab.py`                           | NB 97.78%, DT 100%          |
| 6    | Neural Networks    | `week6_lab.py`                           | 97.64% (MNIST)              |
| 7    | Face Recognition   | `week7_lab.py`                           | 83.5% (LFW)                 |
| 8    | Genetic Algorithms | `week8_lab.py`                           | 8-Queens solved             |

---

## Environment Setup

```bash
# Create conda environment
conda create -n is_labs python=3.10 -y
conda activate is_labs

# Install Python packages
pip install numpy pandas matplotlib scikit-learn tensorflow pygad
```

---

## Run Commands

### JADE Labs (Java)

```bash
# Compile all
javac -cp "lib/jade.jar" -d bin src/week1/Week1Lab.java
javac -cp "lib/jade.jar" -d bin src/week2/Week2Lab.java
javac -cp "lib/jade.jar" -d bin src/week3/*.java

# Week 1: JADE basics
java -cp "lib/jade.jar;bin" jade.Boot -gui -agents "agent:week1.Week1Lab"

# Week 2: Container communication
java -cp "lib/jade.jar;bin" jade.Boot -gui -agents "receiver:week2.Week2Lab"

# Week 3: Book trading
java -cp "lib/jade.jar;bin" jade.Boot -gui -agents "seller:week3.Week3SellerAgent"
```

### Python Labs

```bash
conda activate is_labs
python src/week4/week4_lab.py   # Linear Regression
python src/week5/week5_lab.py   # Naive Bayes + Decision Trees
python src/week6/week6_lab.py   # Neural Networks (MNIST)
python src/week7/week7_lab.py   # Face Recognition (LFW)
python src/week8/week8_lab.py   # Genetic Algorithms
```

---

## Visualizations

Each Python lab generates a results PNG:

- `src/week4/week4_linear_regression_results.png`
- `src/week5/week5_classification_results.png`
- `src/week6/week6_neural_network_results.png`
- `src/week7/week7_face_recognition_results.png`
- `src/week8/week8_genetic_algorithm_results.png`

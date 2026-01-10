# Week 7: Genetic Algorithms & Evolutionary Computing

## 📌 Core Concept

Evolutionary algorithms simulate natural selection to solve optimization problems.

---

## 🧬 EA Components

```
┌────────────────────────────────────────┐
│     EVOLUTIONARY ALGORITHM CYCLE       │
├────────────────────────────────────────┤
│  ┌──────────────┐                      │
│  │ Initial Pop  │                      │
│  └──────┬───────┘                      │
│         ▼                              │
│  ┌──────────────┐    ┌──────────────┐  │
│  │  Selection   │ ←─ │  Evaluation  │  │
│  └──────┬───────┘    └──────────────┘  │
│         ▼                    ↑         │
│  ┌──────────────┐            │         │
│  │ Recombination│ ───────────┘         │
│  └──────┬───────┘                      │
│         ▼                              │
│  ┌──────────────┐                      │
│  │   Mutation   │                      │
│  └──────────────┘                      │
└────────────────────────────────────────┘
```

---

## 🎯 Key Terminology

| Term           | Definition                     |
| -------------- | ------------------------------ |
| **Chromosome** | Encoded solution (genotype)    |
| **Gene**       | Single element in chromosome   |
| **Fitness**    | Quality measure of solution    |
| **Population** | Set of candidate solutions     |
| **Generation** | One iteration of the algorithm |

---

## 🔄 Genetic Operators

### Selection

```
Methods:
├── Tournament Selection (pick best of k random)
├── Roulette Wheel (probability ∝ fitness)
└── Rank Selection (probability ∝ rank)
```

### Crossover (Recombination)

```
Parent 1: [1 3 5 | 2 6 4 7 8]
Parent 2: [8 7 6 | 5 4 3 2 1]
                ↓
Child 1:  [1 3 5 | 4 2 8 7 6]  (ordered crossover)
```

### Mutation

```
Before: [1 3 5 2 6 4 7 8]
                ↑   ↑
               swap
After:  [1 3 7 2 6 4 5 8]
```

---

## 👸 8-Queens Example

### Representation

```
Chromosome: [2, 4, 6, 8, 3, 1, 7, 5]
             ↓
Position:    Row of queen in each column
```

### Fitness Function

```
f = (28 - conflicts)

where 28 = max non-attacking pairs
```

---

## 📊 Typical EA Behavior

```
Fitness
    │     ┌─────────────────────────
    │    /
    │   /  (rapid improvement)
    │  /
    │ /    (slowing progress)
    │/
    └─────────────────────────────→ Generations
      Early    Mid     Late
```

---

## ⚙️ Algorithm Parameters

| Parameter       | Description              | Typical Value |
| --------------- | ------------------------ | ------------- |
| Population Size | Number of individuals    | 50-200        |
| Crossover Rate  | Probability of crossover | 0.7-0.9       |
| Mutation Rate   | Probability of mutation  | 0.001-0.1     |
| Generations     | Number of iterations     | 100-10000     |

---

## 🎯 Project Relevance (VRP)

### Chromosome for VRP

```
[D1→C2→C5→D1, D2→C1→C3→C4→D2]
     Route 1        Route 2
```

### Fitness for VRP

```
f(route) = -total_distance (minimize)
         + items_delivered (maximize)
```

---

## 🌍 Applications

- Route optimization (VRP, TSP)
- Scheduling problems
- Machine learning (neuroevolution)
- Image generation (evolving Mona Lisa)

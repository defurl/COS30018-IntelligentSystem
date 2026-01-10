"""
Week 8 Lab: Genetic Algorithms with PyGAD
==========================================

This lab demonstrates:
1. Basic Genetic Algorithm for function optimization
2. GA operators: selection, crossover, mutation
3. Solving the 8-Queens puzzle
4. Parameter tuning effects

To run:
    conda activate is_labs
    python src/week8/week8_lab.py
"""

import numpy as np
import pygad
import matplotlib.pyplot as plt

# ============================================
# WEEK 8 LAB: GENETIC ALGORITHMS
# ============================================

print("=" * 55)
print("   WEEK 8 LAB: Genetic Algorithms (PyGAD)")
print("=" * 55)

# ------------------------------------------
# PART 1: Function Optimization
# ------------------------------------------
print("\n" + "=" * 55)
print("   PART 1: Linear Function Optimization")
print("=" * 55)

# Target: Find weights w such that y = w1*x1 + w2*x2 + ... = 44
# Given inputs: [4, -2, 3.5, 5, -11, -4.7]
# Find optimal weights

function_inputs = [4, -2, 3.5, 5, -11, -4.7]
desired_output = 44

def fitness_function_p1(ga_instance, solution, solution_idx):
    """Fitness = inverse of absolute error from target"""
    output = np.sum(solution * function_inputs)
    fitness = 1.0 / (np.abs(output - desired_output) + 0.0001)
    return fitness

print("\n[1.1] Problem: Find weights w where Σ(w*x) = 44")
print(f"    Inputs: {function_inputs}")
print(f"    Target output: {desired_output}")

# GA Parameters
num_generations = 100
num_parents_mating = 4
sol_per_pop = 20
num_genes = len(function_inputs)

print("\n[1.2] GA Parameters:")
print(f"    Population size: {sol_per_pop}")
print(f"    Generations: {num_generations}")
print(f"    Parents mating: {num_parents_mating}")
print(f"    Number of genes: {num_genes}")

# Create GA instance
ga_instance = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    fitness_func=fitness_function_p1,
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    init_range_low=-10,
    init_range_high=10,
    parent_selection_type="sss",
    crossover_type="single_point",
    mutation_type="random",
    mutation_percent_genes=15,
    suppress_warnings=True
)

# Run GA
print("\n[1.3] Running Genetic Algorithm...")
ga_instance.run()

# Get best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()
predicted_output = np.sum(solution * function_inputs)

print("\n[1.4] Results:")
print(f"    Best Solution (weights):")
for i, (inp, sol) in enumerate(zip(function_inputs, solution)):
    print(f"      w{i+1} = {sol:+.4f}  (input = {inp})")
print(f"\n    Predicted Output: {predicted_output:.4f}")
print(f"    Target Output: {desired_output}")
print(f"    Error: {abs(predicted_output - desired_output):.6f}")
print(f"    Generations to best: {ga_instance.best_solution_generation}")

# Store fitness history for plotting
fitness_history_p1 = ga_instance.best_solutions_fitness.copy()

# ------------------------------------------
# PART 2: 8-Queens Problem
# ------------------------------------------
print("\n" + "=" * 55)
print("   PART 2: 8-Queens Puzzle")
print("=" * 55)

print("\n[2.1] Problem: Place 8 queens on 8x8 board with no attacks")
print("    Solution: One queen per column, find row positions")

def count_attacks(solution):
    """Count number of attacking pairs"""
    attacks = 0
    n = len(solution)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Same row
            if solution[i] == solution[j]:
                attacks += 1
            # Same diagonal
            if abs(solution[i] - solution[j]) == abs(i - j):
                attacks += 1
    return attacks

def fitness_function_queens(ga_instance, solution, solution_idx):
    """Fitness = inverse of attacks (more attacks = lower fitness)"""
    attacks = count_attacks(solution)
    if attacks == 0:
        return float('inf')  # Perfect solution
    return 1.0 / attacks

# GA for 8-Queens
ga_queens = pygad.GA(
    num_generations=500,
    num_parents_mating=10,
    fitness_func=fitness_function_queens,
    sol_per_pop=50,
    num_genes=8,
    gene_type=int,
    gene_space=range(8),  # Constrain genes to 0-7
    keep_parents=2,
    parent_selection_type="tournament",
    crossover_type="two_points",
    mutation_type="random",
    mutation_percent_genes=20,
    suppress_warnings=True
)

print("\n[2.2] Running GA for 8-Queens...")
ga_queens.run()

# Get solution
queens_solution, queens_fitness, _ = ga_queens.best_solution()
queens_solution = [int(x) for x in queens_solution]
attacks = count_attacks(queens_solution)

print("\n[2.3] Results:")
print(f"    Solution (row for each column): {queens_solution}")
print(f"    Number of attacks: {attacks}")
print(f"    Status: {'✓ SOLVED!' if attacks == 0 else '✗ Not optimal'}")

# Display board
print("\n[2.4] Board Visualization:")
print("    " + "+" + "---+" * 8)
for row in range(8):
    line = "    |"
    for col in range(8):
        if queens_solution[col] == row:
            line += " Q |"
        else:
            line += "   |"
    print(line)
    print("    " + "+" + "---+" * 8)

# ------------------------------------------
# PART 3: Visualization
# ------------------------------------------
print("\n[3] Creating visualizations...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Fitness over generations (Part 1)
ax1 = axes[0]
ax1.plot(fitness_history_p1, 'b-', linewidth=2)
ax1.set_xlabel('Generation')
ax1.set_ylabel('Fitness (1/error)')
ax1.set_title('Part 1: Function Optimization Convergence')
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')

# Plot 2: 8-Queens board
ax2 = axes[1]
board = np.zeros((8, 8))
for col, row in enumerate(queens_solution):
    board[row, col] = 1

# Checkerboard pattern
for i in range(8):
    for j in range(8):
        color = 'wheat' if (i + j) % 2 == 0 else 'tan'
        ax2.add_patch(plt.Rectangle((j, 7-i), 1, 1, facecolor=color))

# Queens
for col, row in enumerate(queens_solution):
    ax2.plot(col + 0.5, 7 - row + 0.5, 'ko', markersize=25)
    ax2.plot(col + 0.5, 7 - row + 0.5, 'wo', markersize=15)

ax2.set_xlim(0, 8)
ax2.set_ylim(0, 8)
ax2.set_aspect('equal')
ax2.set_title(f'Part 2: 8-Queens Solution (Attacks: {attacks})')
ax2.set_xticks(np.arange(0.5, 8, 1))
ax2.set_xticklabels(range(1, 9))
ax2.set_yticks(np.arange(0.5, 8, 1))
ax2.set_yticklabels(range(8, 0, -1))

plt.tight_layout()
plt.savefig('src/week8/week8_genetic_algorithm_results.png', dpi=100)
print("    Saved: src/week8/week8_genetic_algorithm_results.png")

# ------------------------------------------
# Summary
# ------------------------------------------
print("\n" + "=" * 55)
print("   WEEK 8 LAB COMPLETE!")
print("=" * 55)
print("\n   Key Takeaways:")
print("   • GA mimics natural selection: fitness, crossover, mutation")
print("   • Population-based search explores solution space")
print("   • Fitness function guides evolution toward optimal solutions")
print("   • Useful for optimization problems without gradient")
print(f"   • Part 1: Optimized to error = {abs(predicted_output - desired_output):.6f}")
print(f"   • Part 2: 8-Queens with {attacks} attacks")
print()

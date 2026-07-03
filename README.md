# Evolutionary AI for Lunar Lander

An autonomous Lunar Lander controller developed as part of the **Artificial Intelligence** course in the B.Sc. in Informatics Engineering at the **University of Coimbra**.

The objective of the project was to design an autonomous agent capable of safely landing a spacecraft by applying evolutionary computation techniques to optimise control parameters within a physics-based simulation.

Rather than relying on manually designed behaviours, the controller evolves increasingly effective solutions by evaluating candidate parameter sets over multiple simulation runs.

---

# Project Overview

The agent operates within the Gymnasium implementation of the Lunar Lander environment, where every candidate solution is evaluated according to its ability to perform a controlled landing.

The optimisation process considers several aspects of the landing, including:

- Landing success
- Vertical velocity
- Horizontal velocity
- Spacecraft orientation
- Fuel-efficient thruster usage
- Collision avoidance
- Stability during descent

The resulting fitness score guides the evolutionary algorithm towards increasingly successful landing strategies.

---

# Controller Design

Rather than directly controlling every action through manually defined rules, the agent computes thruster commands based on the current state of the spacecraft, including:

- Position
- Linear velocity
- Orientation
- Angular velocity
- Contact with the landing surface

The controller uses a set of parameters that determine how these variables influence the activation of the main and side thrusters. These parameters are optimised using an evolutionary algorithm, allowing the controller to progressively discover landing strategies that satisfy the imposed landing constraints while maintaining stable trajectories.

---

# Features

- Autonomous spacecraft control
- Evolutionary optimisation
- Physics-based simulation
- Fitness function design
- Thruster control
- Collision detection
- Landing constraint evaluation
- Parameter optimisation

---

# Technologies

- Python
- Gymnasium
- NumPy
- Matplotlib

---

# Project Structure

```text
.
├── agent.py
├── evolution.py
├── fitness.py
├── simulation.py
├── main.py
└── ...
```

*(Update this tree to reflect the repository structure.)*

---

# Running

Install the required dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** Depending on the operating system and Python version, some dependencies may need to be installed individually. If `pip install -r requirements.txt` fails, install the listed packages one by one.

Run one of the available controllers:

```bash
python tp1-alunos.py
```

or

```bash
python trigo.py
```

---

# Learning Outcomes

This project provided practical experience with:

- Evolutionary computation
- Artificial intelligence
- Autonomous agent design
- Fitness function engineering
- Physics-based simulation
- Controller optimisation
- Scientific computing using Python

---

# Future Improvements

Potential future developments include:

- Comparison with reinforcement learning approaches
- Neural-network-based controllers
- Multi-objective optimisation
- Adaptive mutation and crossover strategies
- Visualisation of the optimisation process
- Automated parameter sensitivity analysis

---

# Acknowledgements

Developed collaboratively as part of the **Artificial Intelligence** course in the B.Sc. in Informatics Engineering at the **University of Coimbra**.

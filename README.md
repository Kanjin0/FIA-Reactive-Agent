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

```
.
├── agent.py
├── evolution.py
├── fitness.py
├── simulation.py
├── main.py
└── ...
```

*(Update this tree to reflect the repository.)*

---

# Running

Install the required dependencies (WARNING: There may be trouble in doing it this way. Speaking from personal experience, as one of the contributors of this project, you may need to install the parts listed in the requirements one by one)

```bash
pip install -r requirements.txt
```

Run the simulation

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
- Fitness function design
- Physics-based simulation
- Autonomous agents
- Parameter optimisation
- Scientific computing using Python

---

# Future Improvements

Potential future developments include:

- Alternative evolutionary algorithms
- Reinforcement learning comparison
- Neural-network-based controllers
- Multi-objective optimisation
- Adaptive mutation strategies
- Visualisation of the optimisation process

---

# Acknowledgements

Developed collaboratively as part of the Artificial Intelligence course in the B.Sc. in Informatics Engineering at the University of Coimbra.

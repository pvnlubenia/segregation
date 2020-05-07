# Agent-based models of segregation using Python

The 2 models presented are based on the Schelling segregation model. The system is composed of different groups of agents interacting with each other. Each agent scans his neighborhood to check the number of agents belonging to the same group as him. He stays put if the number satisfies him. Otherwise, he moves to a different location. As Thomas Schelling originally showed, even a low satisfaction threshold leads to a highly segregated community.

The models use basic Python libraries, and the codes can be run on their own.

## Model 1

Model 1 is based on Moujahid. It uses a discrete grid system, and a neighborhood is composed of the 8 agents surrounding an agent.

## Model 2

Model 2 is based on Sayama. It does NOT use a discrete grid system: the spatial distribution of the agents is more realistic. A neighborhood is an area of a certain radius from an agent.

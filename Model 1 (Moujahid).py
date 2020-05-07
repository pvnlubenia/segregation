#
# An agent-based model of segregation
# Largely based on Moujahid
# https://www.binpress.com/simulating-segregation-with-python/
# See pdf "Agent-based models of segregation using Python" for more details
#



### Needed libraries ###

import itertools
import random as rd
import matplotlib.pyplot as plt
import os



### Agent-based model ###

class Schelling:
	def __init__(self, width, height, empty_ratio, happiness_threshold, groups, n_iterations):
		
        # Width of community grid
        self.width = width
        
        # Height of community grid
		self.height = height
        
        # Percentage of empty houses
		self.empty_ratio = empty_ratio
        
        # Minimum similarity ratio, to be considered happy
		self.happiness_threshold = happiness_threshold
        
        # Number of groups of residents
		self.groups = groups
        
        # Maximum iterations
		self.n_iterations = n_iterations
        
        # List of empty houses
		self.empty_houses = []
        
        # Dictionary of residents
		self.agents = {}


    ## Place residents on the community

	def populate(self):
        
        # Create address (coordinates) of residents
		all_houses = list(itertools.product(range(self.width), range(self.height)))
		
        # Shuffle the order of houses
        rd.shuffle(all_houses)
        
        # Determine number of empty houses
		n_empty = int(self.empty_ratio*len(all_houses))
        
        # Assign first few houses as empty
		self.empty_houses = all_houses[ : n_empty]
        
        # Assign the rest to be occupied
		remaining_houses = all_houses[n_empty : ]
        
        # Assign houses to residents
		houses_by_group = [remaining_houses[i::self.groups] for i in range(self.groups)]
		
        # Create dictionary of residents
        # Each resident is defined by his address and group number
        for i in range(self.groups):
			agent = dict(zip(houses_by_group[i], [i+1]*len(houses_by_group[i])))
			self.agents.update(agent)

    ## Checker if resident is unhappy

	def is_unhappy(self, x, y):
        
        # Get group number of resident
		group = self.agents[(x, y)]
        
        # Initialize variables
		count_similar = 0
		count_different = 0
        
        # Check similarity with bottom left neighbor
		if x > 0 and y > 0 and (x-1, y-1) not in self.empty_houses:
			if self.agents[(x-1, y-1)] == group:
				count_similar += 1
			else:
				count_different += 1
		
        # Check similarity with bottom neighbor
        if y > 0 and (x, y-1) not in self.empty_houses:
			if self.agents[(x, y-1)] == group:
				count_similar += 1
			else:
				count_different += 1
		
        # Check similarity with bottom right neighbor
        if x < (self.width-1) and y > 0 and (x+1, y-1) not in self.empty_houses:
			if self.agents[(x+1, y-1)] == group:
				count_similar += 1
			else:
				count_different += 1
		
        # Check similarity with left neighbor
        if x > 0 and (x-1, y) not in self.empty_houses:
			if self.agents[(x-1,y)] == group:
				count_similar += 1
			else:
				count_different += 1
		
        # Check similarity with right neighbor
        if x < (self.width-1) and (x+1, y) not in self.empty_houses:
			if self.agents[(x+1,y)] == group:
				count_similar += 1
			else:
				count_different += 1
		
        # Check similarity with upper left neighbor
        if x > 0 and y < (self.height-1) and (x-1, y+1) not in self.empty_houses:
			if self.agents[(x-1,y+1)] == group:
				count_similar += 1
			else:
				count_different += 1        
		
        # Check similarity with upper neighbor
        if x > 0 and y < (self.height-1) and (x, y+1) not in self.empty_houses:
			if self.agents[(x,y+1)] == group:
				count_similar += 1
			else:
				count_different += 1        
		
        # Check similarity with upper right neighbor
        if x < (self.width-1) and y < (self.height-1) and (x+1, y+1) not in self.empty_houses:
			if self.agents[(x+1,y+1)] == group:
				count_similar += 1
			else:
				count_different += 1
		
        # Resident is NOT unhappy, i.e., happy if he has no neighbors
        if (count_similar + count_different) == 0:
			return False
		
        # Check if similarity ratio is below happiness threshold
        else:
			return float(count_similar/(count_similar + count_different)) < self.happiness_threshold

    ## Resident moves if he is unhappy

	def move(self):
        
        # Maximum iterations allowed
		for i in range(self.n_iterations):
            
            # Initialize count
			n_changes = 0
            
            # Check each resident
			for agent in self.agents:
                
                # Activated if resident is unhappy
				if self.is_unhappy(agent[0], agent[1]):
                    
                    # Get a random empty house
					empty_house = rd.choice(self.empty_houses)
                    
                    # Get group number of the resident
					agent_group = self.agents[agent]
                    
                    # Assign the empty house to the resident
					self.agents[empty_house] = agent_group
                    
                    # Remove the original residence from the dictionary
					del self.agents[agent]
                    
                    # Remove the now-occupied house from the list of empty houses
					self.empty_houses.remove(empty_house)
                    
                    # Add the house the resident just left to the list of empty houses
					self.empty_houses.append(agent)
                    
                    # Count as a move
					n_changes += 1
            
            # Iteration stops if everyone is already happy
			if n_changes == 0:
				break

    ## Compute similarity ratio

	def similarity(self):
        
        # Initialize list
		similarity = []
        
        # Do for each resident
		for agent in self.agents:
            
            # Initialize variables
			count_similar = 0
			count_different = 0
            
            # Get address and group number of the resident
			x = agent[0]
			y = agent[1]
			group = self.agents[(x,y)]
            
            # Check similarity with bottom left neighbor
			if x > 0 and y > 0 and (x-1, y-1) not in self.empty_houses:
				if self.agents[(x-1, y-1)] == group:
					count_similar += 1
				else:
					count_different += 1
            
            # Check similarity with bottom neighbor
			if y > 0 and (x, y-1) not in self.empty_houses:
				if self.agents[(x, y-1)] == group:
					count_similar += 1
				else:
					count_different += 1
			
            # Check similarity with bottom right neighbor
            if x < (self.width-1) and y > 0 and (x+1, y-1) not in self.empty_houses:
				if self.agents[(x+1, y-1)] == group:
					count_similar += 1
				else:
					count_different += 1
			
            # Check similarity with left neighbor
            if x > 0 and (x-1, y) not in self.empty_houses:
				if self.agents[(x-1, y)] == group:
					count_similar += 1
				else:
					count_different += 1        
			
            # Check similarity with right neighbor
            if x < (self.width-1) and (x+1, y) not in self.empty_houses:
				if self.agents[(x+1, y)] == group:
					count_similar += 1
				else:
					count_different += 1
			
            # Check similarity with upper left neighbor
            if x > 0 and y < (self.height-1) and (x-1, y+1) not in self.empty_houses:
				if self.agents[(x-1, y+1)] == group:
					count_similar += 1
				else:
					count_different += 1        
			
            # Check similarity with upper neighbor
            if x > 0 and y < (self.height-1) and (x, y+1) not in self.empty_houses:
				if self.agents[(x, y+1)] == group:
					count_similar += 1
				else:
					count_different += 1        
			
            # Check similarity with upper right neighbor
            if x < (self.width-1) and y < (self.height-1) and (x+1, y+1) not in self.empty_houses:
				if self.agents[(x+1,y+1)] == group:
					count_similar += 1
				else:
					count_different += 1
			
            # Place similarity ratio in the list
            try:
				similarity.append(float(count_similar/(count_similar + count_different)))
			
            # If there are no neighbors, similarity ratio is 1
            except:
				similarity.append(1)
        
        # Compute average similarity ratio over all residents
		return sum(similarity)/len(similarity)

    ## Visualize the state

	def plot(self, state):
        
        # Initialize subplots
		fig, ax = plt.subplots()
        
        # Assign color to each group (define more as needed)
		agent_colors = {1:'b', 2:'r', 3:'g', 4:'c', 5:'m', 6:'y', 7:'k'}
        
        # Create a scatterplot for each resident, colored based on his group
		for agent in self.agents:
			ax.scatter(agent[0]+0.5, agent[1]+0.5, color = agent_colors[self.agents[agent]],
									edgecolors = 'white')
		
        # Title
        ax.set_title('Schelling Model: ' + state + ' State' + '\n' + 'Similarity: '
									+ str("{:.1f}".format(schelling.similarity()*100)) + '%')
		
        # Horizontal axis label
        ax.set_xlabel(str(self.empty_ratio*100) + '% Empty Houses' + '\n'
									+ str(self.happiness_threshold*100) + '% Happiness Threshold' + '\n'
									+ str(self.groups) + ' groups')
		
        # Ensure all residents are visible
        ax.set_xlim([0, self.width])
		ax.set_ylim([0, self.height])
        
        # Remove extra tick marks on the axes
		ax.set_xticks([])
		ax.set_yticks([])
        
        # Prepare format of file name
		filename = 'Model1_' + state
        
        # Starting filename count
		i = 1
        
        # Check if filename already exists; add 1 if it does
		while os.path.exists('{}{:d}.png'.format(filename, i)):
			i += 1
        
        # Save figure
		plt.savefig('{}{:d}.png'.format(filename, i), bbox_inches = 'tight', dpi = 300)



### Simulation ###

# Initialize parameters
schelling = Schelling(width = 25, height = 25, empty_ratio = 0.25, happiness_threshold = 0.30,
											groups = 2, n_iterations = 500)

# Place residents on the community
schelling.populate()

# Visualize initial state
schelling.plot('Initial')

# Allow unhappy residents to move
schelling.move()

# Visualize final state
schelling.plot('Final')







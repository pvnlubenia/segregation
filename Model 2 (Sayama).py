#
# An agent-based model of segregation
# Largely based on Sayama
# https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_Introduction_to_the_Modeling_and_Analysis_of_Complex_Systems_(Sayama)/19%3A_Agent-Based_Models
# See pdf "Agent-based models of segregation using Python" for more details
#



### Needed libraries ###

# For assigning a random location to agents
import random as rd

# For visualizing the distribution of agents using plot
import matplotlib.pyplot as plt

# For checking if a filename already exists, to avoid overwriting files
import os



### Initialize class to create residents ###

class agent:
    pass



### Create residents ###

def create_agents():
    
    # Allow list of residents to be accessed outside the function
	global agents_list
    
    # Initialize list
	agents_list = []
    
    # Create specified number of residents
	for each_agent in range(n_agents):
        
        # Create an agent
		agent_ = agent()
        
        # Assign to a random address
		agent_.x = rd.random()
		agent_.y = rd.random()
        
        # Assign to a random group
		agent_.group = rd.randint(0, groups-1)
        
        # Place resident on the list
		agents_list.append(agent_)



### Group residents according to group number ###

def group_by_number():
    
    # Allow list of groups to be accessed outside the function
	global group
    
    # Initialize list
	group = []
    
    # Group according to group number
	for group_number in range(groups):
        
        # A resident is grouped with other residents with the same group number
		group.append([agent_ for agent_ in agents_list if agent_.group == group_number])



### Let resident move if he is not satisfied with his neighbors ###

def move():
    
    # Allow number of iterations done to be accessed outside the function
	global iteration
    
    # Maximum iterations allowed
	for iteration in range(n_iterations):
        
        # Initialize count
		n_changes = 0
        
        # Check each resident
		for agent_ in agents_list:
            
            # Create list of neighbors within the radius specified
			neighbors = [neighbor for neighbor in agents_list if (agent_.x - neighbor.x)**2 + (agent_.y - neighbor.y)**2 < radius**2]

            # Remove resident himself from list of neighbors
			neighbors.remove(agent_)
			
            # Check if there are neighbors within the radius
			if len(neighbors) > 0:
                
                # Compute similarity ratio
				satisfaction = len([neighbor for neighbor in neighbors if neighbor.group == agent_.group])/len(neighbors)
				
                # Move resident to a random location if similarity ratio is below threshold
				if satisfaction < threshold:
					agent_.x, agent_.y = rd.random(), rd.random()
                    
                    # Count as a move
					n_changes += 1

        # Iteration stops if everyone is already happy
		if n_changes == 0:
			break



### Compute similarity ratio ###
            
def similarity_ratio():
    
    # Allow overall similarity ratio to be accessed outside the function
	global overall_similarity_ratio
    
    # Initialize list
	similarity_ratios = []
    
    # Check each resident
	for agent_ in agents_list:
        
        # Create list of neighbors within the radius specified
		neighbors = [neighbor for neighbor in agents_list if (agent_.x - neighbor.x)**2 + (agent_.y - neighbor.y)**2 < radius**2]

        # Remove resident himself from list of neighbors
		neighbors.remove(agent_)

		# Check if there are neighbors within the radius
		if len(neighbors) > 0:
			
            # Place similarity ratio in the list
			try:
				similarity_ratios.append(len([neighbor for neighbor in neighbors if neighbor.group == agent_.group])/len(neighbors))
			
            # If there are no neighbors, similarity ratio is 1
			except:
				similarity_ratios.append(1)
	
    # Compute average similarity ratio over all residents
	overall_similarity_ratio = sum(similarity_ratios)/len(similarity_ratios)
	
    # Outputs overall similarity ratio
	return overall_similarity_ratio



### Visualize the state ###

def visualize(state):
    
    # Initialize subplots
	fig, ax = plt.subplots()
    
    # Create a scatterplot by group, plotting each resident
	for Group in range(groups):
		ax.plot([agent_.x for agent_ in group[Group]], [agent_.y for agent_ in group[Group]], 'o')
	
    # Title
	ax.set_title(state + ' State' + ' || ' + 'Segregation: ' + str("{:.1f}".format(similarity_ratio()*100)) + '%')
	
    # Horizontal axis label
	ax.set_xlabel(str(n_agents) + ' Residents' + ' || ' + str(groups) + ' Groups' + ' || ' + str(radius*100) + '% Neighborhood || ' + str(threshold*100) + '% Threshold' + '\n' + 'moves: ' + str(iteration))
	
    # Remove extra tick marks on the axes
	ax.set_xticks([])
	ax.set_yticks([])
	
    # Prepare format of file name
	filename = 'Model2_' + state
	
    # Starting filename count
	i = 1
    
    # Check if filename already exists; add 1 if it does
	while os.path.exists('{}{:d}.png'.format(filename, i)):
		i += 1
	
    # Save figure
	plt.savefig('{}{:d}.png'.format(filename, i), bbox_inches = 'tight', dpi = 300)



### Simulation ###

# Number of residents
n_agents = 1000

# Number of groups
groups = 2

# Maximum iterations
n_iterations = 100

# Neighborhood radius
radius = 0.1

# Satisfaction threshold
threshold = 0.31

# Create residents
create_agents()

# Group residents according to group number
group_by_number()

# Needed for label of initial state
iteration = 0

# Visualize initial state
visualize('Initial')

# Allow unsatisfied residents to move
move()

# Visualize initial state
visualize('Final')

####### End of Code #######







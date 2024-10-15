import numpy as np
import matplotlib.pyplot as plt

class ChaosGame:
    
    def __init__(self , num_corners , scale):
        if not isinstance(num_corners , int):
            raise ValueError("Number of corners must be an integer!")
        if scale > 1.0:
            raise ValueError("Scale must be <= 1!")
        
        self.num_corners = num_corners
        self.scale = scale
        
        plt.figure(figsize=(10,10)) #Change accordingly
        plt.axis('off') #Change accordingly
        
    def GenerateBoard(self , ans):
        '''Generates an n-gon based on number of corners'''
        
        if ans == True:
            angles = np.linspace(0 , 2 * np.pi, self.num_corners)[:-1]
            plt.title(f"{num_corners} cornered chaos game, scale factor = {self.scale:.2f}")
            
        elif ans == False:
            angles = np.linspace(0 , 2 * np.pi, self.num_corners + 1)[:-1]
            plt.title(f"{num_corners} cornered chaos game with corner {num_corners} at center, scale factor = {self.scale:.2f}")
            
        else:
            print("Enter y or n only!")
        
        x = np.zeros(self.num_corners+1)
        y = np.zeros(self.num_corners+1)
        
        x[:angles.shape[0]] = np.cos(angles)
        y[:angles.shape[0]] = np.sin(angles)

        return np.column_stack((x,y))

    def GenerateIFS(self, probability_array, num_points):
        '''
        This function is used to generate a random IFS array based on the supplied 
        probability of the corners. num_points refers to the number of points you
        want to use to generate the fractal image.
        '''
        if len(probability_array) == 0:
            probability_array = np.full((self.num_corners, ) , 1.0/self.num_corners)
        else:      
            if len(probability_array) < self.num_corners - 1:
                raise ValueError("Cannot proceed, probability information for two or more corners is missing.")
            
            if len(probability_array) == self.num_corners - 1:
                probability_array = np.append(probability_array, 1 - np.sum(probability_array))
            
            if self.num_corners < len(probability_array):
                raise IndexError("Number of points considered in probability_array is more than the number of corners in the game!")
            
            if np.sum(probability_array) != 1:
                raise ValueError("The entered probabilities do not(or cannot) sum up to 1!")
        
        corner_index = [i+1 for i in range(probability_array.shape[0])]
        point_frequency = (num_points * probability_array).astype(int)
        
        IFS_array = []
        for i in range(point_frequency.shape[0]):
            subarray = np.full((point_frequency[i] , ) , corner_index[i])
            IFS_array.append(subarray)
        
        IFS_array = np.concatenate(IFS_array)
        np.random.shuffle(IFS_array)

        return IFS_array

    def GenerateFractal(self , probability_array , num_points , starting_pos , corner_at_origin):
        '''
        1.) IFS stands for Iterated Function System. It contains the information of 
            the corners that appear in our game.
        2.) Probability array contains the information of how frequently a corner is
            (or is allowed to) occur in the IFS array. The elements must sum to 1 (ensured by the code). 
        3.) The scale is the fraction of distance we move towards every corner that
            pops up in IFS.
        '''
        
        IFS = self.GenerateIFS(probability_array , num_points)

        pos = np.zeros((len(IFS) , 2))
        pos[0] = starting_pos
        
        corners = self.GenerateBoard(corner_at_origin)

        for i in range(1 , len(IFS)):
            j = (IFS[i]).astype(int)
            update = corners[j-1]
            pos[i] = self.scale * pos[i-1] + (1 - self.scale) * update
        
        plt.scatter(pos[:,0] , pos[:,1] , s = 0.5 , color='green' , label='Fractal points') #Change accordingly
        plt.scatter(corners[:,0] , corners[:,1] , s = 4 , color='red' , label='Corners') #Change accordingly
        plt.legend()
        plt.show()
        
        return pos , corners

num_corners = 5
sl = 1.0/3.0 #scale

num_points = 20000 #number of points that will make up the fractal
probability_array = [] #Leave blank for equal probability. **Automatically computes the probability of final corner if not entered.
fractal = ChaosGame(num_corners , sl)

fractal.GenerateFractal(probability_array , num_points , [0 , 0] , True)
fractal.GenerateFractal(probability_array , num_points , [0 , 0] , False)


'''
Some combinations of scale and corners that i found cool are listed below:
    corners = 6 (6th corner at center) scale = 1/3, probability_array = np.array([]) (equal probability for all points)
    corners = 5 (5th corner at center) scale = 1/3, probability_array = np.array([]) (equal probability for all points)
    corners = 4 (4th corner at center) scale = 1/3, np.array([1/10,1/10,1/10]) or np.array([1/10,1/10,1/10,7/10]) both will work since the function calculates the probability for the missing corner.
    corners = 4  scale = 1/2, probability_array = np.array([]) (equal probability for all points)
    corners = 3 scale = 1/2,  probability_array = np.array([]) (equal probability for all points)
I have also included the images of these generated fractals in the Images folder of this repo.
'''

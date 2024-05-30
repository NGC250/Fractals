import numpy as np
import matplotlib.pyplot as plt
import librosa as aud
from PIL import Image

class ChaosGame:
    
    def __init__(self, num_corners):
        if not isinstance(num_corners, int):
            raise ValueError("Number of corners must be an integer!")
        self.num_corners = num_corners
        
    def GenerateBoard(self):
        '''Generates an n-gon based on number of corners'''
        
        ans = input(f"Do you want the corner number {self.num_corners} to be at the center?(y/n): ")
        if ans == 'y':
            angles = np.linspace(0, 2*np.pi, self.num_corners)[:-1]
            x = np.cos(angles)
            y = np.sin(angles)
            x = np.append(x,0)
            y = np.append(y,0)
            z = 1
        elif ans == 'n':
            angles = np.linspace(0, 2*np.pi, self.num_corners+1)[:-1]
            x = np.cos(angles)
            y = np.sin(angles)
            z = 0
        else:
            print("Enter y or n only!")
        return np.column_stack((x,y)) , z

    def GenerateIFS(self, probability_array, num_points):
        '''
        This function is used to generate a random IFS array based on the supplied 
        probability of the corners. num_points refers to the number of points you
        want to use to generate the fractal image.
        '''
        if probability_array.size == 0:
            probability_array = np.full((self.num_corners,),1/self.num_corners)
        else:      
            if probability_array.shape[0] < self.num_corners - 1:
                raise ValueError("Cannot proceed, probability information for one or more corners is missing. Add alteast one more value to the array.")
            
            if probability_array.shape[0] == self.num_corners - 1:
                probability_array = np.append(probability_array, 1 - np.sum(probability_array))
            
            if self.num_corners < probability_array.shape[0]:
                raise IndexError("Number of points considered in probability_array is more than the number of corners in the game!")
            
            if np.sum(probability_array) != 1:
                raise ValueError("One or more values exceed 1! OR The entered probabilities do not sum to 1.")
        
        corner_index = np.zeros((self.num_corners,))
        for i in range(probability_array.shape[0]):
            corner_index[i] = i+1
        
        point_frequency = (num_points*probability_array).astype(int)
        IFS_array = np.array([])
        for i in range(point_frequency.shape[0]):
            subarray = np.full((point_frequency[i],),corner_index[i])
            IFS_array = np.append(IFS_array,subarray)

        np.random.shuffle(IFS_array)
        return IFS_array

    def GenerateFractal(self, IFS, scale, starting_pos):
        '''
        1.) IFS stands for Iterated Function System. It contains the information of 
            the corners that appear in our game.
        2.) Probability array contains the information of how frequently a corner is
            (or is allowed to) occur in the IFS array. The elements must sum to 1 (ensured by the code). 
        3.) The scale is the fraction of distance we move towards every corner that
            pops up in IFS.
        '''
        pos = np.zeros((IFS.shape[0],2))
        pos[0] = starting_pos
        
        corners, z = self.GenerateBoard()
        
        for i in range(1,IFS.shape[0]):
            j = (IFS[i]).astype(int)
            update = corners[j-1]
            pos[i] = scale*pos[i-1] + (1-scale)*update
            
            print("currently evaluating:",i+1)
            
        plt.figure(figsize=(10,10)) #Change accordingly
        plt.scatter(pos[:,0],pos[:,1], s = 1, color='green', label='Fractal points') #Change accordingly
        plt.scatter(corners[:,0],corners[:,1],s = 4, color='red', label='Corners') #Change accordingly
        plt.axis('off') #Change accordingly
        if z == 0:
            plt.title(f"{num_corners} cornered chaos game, scale factor = {scale:.2f}")
        elif z == 1:
            plt.title(f"{num_corners} cornered chaos game with corner {num_corners} at center, scale factor = {scale:.2f}")
        plt.legend() 
        
        return pos, corners

num_corners = 4
num_points = 10000 #number of points that will make up the fractal
probability_array = np.array([]) #Leave blank for equal probability. **Automatically computes the probability of final corner if not entered.
fractal1 = ChaosGame(num_corners)

IFS = fractal1.GenerateIFS(probability_array,num_points)
points, corners = fractal1.GenerateFractal(IFS,1/3,np.array([0,0]))

'''
Some combinations of scale and corners that i found cool are listed below:
Fractal1: corners = 6 (6th corner at center) scale = 1/3, probability_array = np.array([]) (equal probability for all points)
Fractal2: corners = 5 (5th corner at center) scale = 1/3, probability_array = np.array([]) (equal probability for all points)
Fractal3: corners = 4 (4th corner at center) scale = 1/3, np.array([1/10,1/10,1/10]) or np.array([1/10,1/10,1/10,7/10]) both will work since the function calculates the probability for the missing corner.
Fractal4: corners = 4  scale = 1/3, probability_array = np.array([]) (equal probability for all points)
Fractal5: corners = 3 scale = 1/2,  probability_array = np.array([]) (equal probability for all points)
I have also included the images of these generated fractals in the Images folder of this repo.
'''

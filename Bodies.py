import numpy as np
import math

class Bodies:
    def __init__(
        self,
        position = np.array([0, 0, 0], dtype = float),
        velocity = np.array([0, 0, 0], dtype = float),
        acceleration=np.array([0, 0, 0], dtype = float),
        name = None,
        mass = 1.0
    ):
        self.position = np.copy(np.asfarray(position))
        self.velocity = np.copy(np.asfarray(velocity))
        self.acceleration = np.copy(np.asfarray(acceleration))
        self.name = name
        self.SetMass(mass)
        self.G = 6.67408E-11
        
    def SetMass(self, mass):
        if mass < 0:
            raise ValueError("mass cannot be a negative value")
        self.mass = mass
        
    def update(self, deltaT):
        '''updates the veloacity and position vectors given the new acceleration'''
        
        i = self.position + self.velocity*deltaT
        j = self.velocity + self.acceleration*deltaT
        
        #update vel and pos arrays
        self.positon = i 
        self.velocity = j
        
    def gravacc(self, body):
        '''calculates new acceralation between object and body due to gravity'''
        
        r = self.position-body.position #vector between the bodies
        mag_r = np.linalg.norm(r) #magnitude of vector between bodies
        
        mag_Acc = -(self.G*body.mass)/(mag_r**2)
        self.Acc = mag_Acc*((r)/(mag_r))
        
        
           
            
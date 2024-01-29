import numpy as np
import math


class Particle:
    def __init__(
        self,
        position=np.array([0, 0, 0], dtype=float),
        velocity=np.array([0, 0, 0], dtype=float),
        acceleration=np.array([0, -10, 0], dtype=float),
        name = "Ball",
        mass = 1.0
    ):
        self.position = np.copy(np.asfarray(position))
        self.velocity = np.copy(np.asfarray(velocity))
        self.acceleration = np.copy(np.asfarray(acceleration))
        self.name = name
        self.SetMass(mass)
        self.G = 6.67408E-11
        
    
        
    
    def SetMass(self, mass):
        '''helps with debugging as it creates f strings'''
        if mass < 0:
            raise ValueError("mass cannot be a negative value")
        self.mass = mass

    def update(self, deltaT=5, acc=0, method='E', acc0 = 0):
        '''
        updates the velocity and position vectors given the acceleration over the course of time deltatT
        '''
        if method == 'E':
            #initalise variables for position and velocity after deltaT
            i = self.position + self.velocity*deltaT
            j = self.velocity + acc*deltaT
        
            #update arrays
            self.position = i
            self.velocity = j
        elif method == 'EC':
            j=  self.velocity+acc*deltaT
            i = self.position +j*deltaT
            
            self.position = i
            self.velocity = j
        elif method =='V':
            i = self.position +self.velocity*deltaT +0.5*self.acceleration*(deltaT**2)
            j = self.velocity+0.5*(acc + acc0)*deltaT
            
            self.position = i
            self.velocity = j
            
        
    def updateGravitationalAcceleration(self, body):
        '''calculates acceleration of the object due to another body'''
        
        r = self.position-body.position
        mag_r = np.linalg.norm(r)
        if mag_r == 0:
            Acc = 0
        else:
            mag_Acc = -(self.G*body.mass)/(mag_r**2)
            Acc = mag_Acc*((r)/(mag_r))

        self.acceleration = Acc
        
    def kineticEnergy(self):
        '''calculates the kinetic energy between of object'''
        KE = 0.5*self.mass*((np.linalg.norm(self.velocity))**2)
        return KE
        

        
        
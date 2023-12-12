import numpy as np


class Bodies:
    def __init__(
        self,
        position = np.array([0, 0, 0], dtype=float),
        velocity = np.array([0, 0, 0], dtype=float),
        acceleration=np.array([0, 0, 0], dtype = float),
        name = None,
        mass = 1.0
    ):
        self.position =  np.copy(np.asfarray(position))
        self.velocity =  np.copy(np.asfarray(velocity))
        self.acceleration = np.copy(np.asfarray(acceleration))
        self.name = name
        self.SetMass(mass)
        self.G = 6.67408E-11
        
        
    def __str__(self):
        return "Particle: {0}, Mass: {1:.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}".format(self.name, self.mass, self.position, self.velocity, self.acceleration
        )
        
    def SetMass(self, mass):
        if mass < 0:
            raise ValueError("mass cannot be a negative value")
        self.mass = mass
        
    def update(self, deltaT, accelerate=0):
        '''updates the veloacity and position vectors given the new acceleration'''
        #using Verlet algorithm
        i = self.position + self.velocity*deltaT
        j = self.velocity + accelerate*deltaT
        
        #update arrays
        self.position = i
        self.velocity = j
        
        #print("hopefully updated the velocity and position of: ", self.name, "now is: ", self.velocity, self.position)
        
    def gravacc(self, body, sp = False):
        '''calculates new acceralation between object and body due to gravity'''
        
        r = self.position-body.position #vector between the bodies
        mag_r = np.linalg.norm(r) #magnitude of vector between bodies
        if mag_r == 0:
            Acc = 0
        else:
            mag_Acc = -(self.G*body.mass)/(mag_r**2)
            Acc = mag_Acc*((r)/(mag_r))
        if sp == False:
            return Acc
        elif sp == True:
            self.acceleration = self.acceleration + Acc
        #print("updated the acceleration of: ", self.name)
        
        
           
            
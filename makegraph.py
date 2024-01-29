import matplotlib.pyplot as plt

# create data 
x = [10, 20, 50, 100, 200, 300, 400, 600, 800, 900, 1200, 1600, 2400, 2700, 3200, 3600, 4800, 10800, 28800, 43200, 86400]
 

with open('averages.txt', 'r') as f:
    yE = [float(line.rstrip()) for line in f]
print(yE)
with open('averagesEC.txt', 'r') as f1:
    yEC = [float(line.rstrip()) for line in f1]
print(yEC)
with open('averagesER.txt', 'r') as f2:
    yER = [float(line.rstrip()) for line in f2]
print(yER)
with open('averagesV.txt', 'r') as f3:
    yV = [float(line.rstrip()) for line in f3]
print(yV)


  
# plot lines 
plt.plot(x, yE, label = "E") 
#plt.plot(x, yEC, label = "EC") 
plt.plot(x, yER, label = "ER") 
plt.plot(x, yV, label = "V") 
plt.legend() 
plt.show()
pos = []
vec = []
fname = "test/Mars.txt"
with open("test/Mars.txt") as file:
    for line in file:
        if line[:4] == " X =":
            pos.append(float(line[4:26]))
            pos.append(float(line[30:52]))
            pos.append(float(line[56:78]))
        if line[:4] == " VX=":
            vec.append(float(line[4:26]))
            vec.append(float(line[30:52]))
            vec.append(float(line[56:78]))
            break
    name = fname[5:-4]
print("position ", pos, "\nvelocity ", vec, "\nname ", name)
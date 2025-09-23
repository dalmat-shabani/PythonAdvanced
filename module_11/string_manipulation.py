with open("example.txt", "r") as file:
    for line in file:
        cleared_line = line.strip()
        print(cleared_line)


with open("example.txt", "r") as file:
    for line in file:
        words = line.strip().split()
        print(words)


name = "Alice"
age = 28

with open("output.txt", "w") as file:
    file.write("Name: " + name + '\n')
    file.write("Age " + str(age) + "\n")

with open("example.txt", "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        cleared_line = line.strip()
        modified_line = cleared_line.replace("Line 1", "Line x")
        outfile.write(modified_line + '\n')
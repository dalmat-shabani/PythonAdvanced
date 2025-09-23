#open a file in 'read' mode
#file_path = "example.txt"
#file = open(file_path, "r")

#content = file.read()
#print(content)

#close the file
#file.close()

import os

file_path = "example.txt"
with open(file_path, "r") as file:
    content = file.read()
    print(content)


#File modes
# 'r' : read
# 'w' : write
# 'a' : append
# 'b' : binary mode
# 'x' : Exclusive creation

#reading from files
file_path = "example.txt"
with open(file_path, "r") as file:
    content = file.read()
    line = file.readline()
    lines = file.readlines() # read all lines into a list


print(content)
print(line)
print(lines)


#writing to files
with open('example.txt', 'w') as file:
    file.write('Welcome to Digital School')

lines = ['Hello, world\n ', 'Welcome to python\n']
with open('example.txt', 'w') as file:
    file.writelines(lines)

with open("example.txt", "r") as file:
    file.seek(0)
    data = file.read()
    print(data)

if os.path.exists("example.txt"):
    print("File exists!")

with open("example.txt", "a") as file:
    file.write("New data appended")

# Reading/Writing binary files
data = b'This is some binary data'
with open("example.bin", "wb") as file:
    file.write(data)

with open("example.bin", "rb") as binary_file:
    data= binary_file.read()
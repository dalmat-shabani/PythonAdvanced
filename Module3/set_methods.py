from Tools.demo.mcast import MYTTL

my_set = {1,2,3}

#add elements
my_set.add(7)
print(my_set)

#remove
my_set.remove(3)
print(my_set)



#discard
my_set.discard(3)
print(my_set)

#CLEAR
my_set.clear()
print(my_set)


#len
set_length = len(my_set)
print(set_length)



#examples on how we can use sets
my_list = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5]
unique_set = set(my_list)

unique_list = list(unique_set)
print(unique_list)

user1_interests = {"music", "movies", "travel"}
user2_interests = {"movies", "reading", "cooking"}

common_interests = user1_interests.intersection(user2_interests)
print(common_interests)


#in operator
colors = {"red", "green", "blue"}
color = "green"
print(color in colors)
print(color not in colors)
from environment import Environment
x,y=int(input("Enter initial x: ")),int(input("Enter initial y: "))
my_list = []
num_sets = int(input("How many tables do you wanna deliver? "))
for i in range(num_sets):
    elements_str = input("Enter the x and y separated by commas: ".format(i+1))
    elements = [int(x.strip()) for x in elements_str.split(',')]

    my_list.append(list(elements))
print("List of sets:", my_list)
goal = my_list
Environment(6, 6, x,y, goal)


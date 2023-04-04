import numpy as np
#import pin lists from CSV files in the current folder. Change file name if necessary
import random
import string
import math 


print("Starting program...")
pin_length = int(input("How long should each pin be?"))
total_pins = int(input("How many pins do you need?"))
job_number = input("What is the job number?")
nu_pins = math.ceil(math.sqrt(total_pins))

#create array to hold combinations
list_1 = []
list_2 = []
list_3 = []

#create string to pull characters from 
letters = string.ascii_uppercase + string.digits
letters = letters.replace("I","")
letters = letters.replace("0","")
letters = letters.replace("O","")
print("Creating List 1")
for x in range(0, nu_pins):
    set = ''.join(random.choice(letters) for i in range(pin_length))
    list_1 = np.append(list_1, set)
print("Creating List 2")
for x in range(0, nu_pins):
    set = ''.join(random.choice(letters) for i in range(pin_length))
    list_2 = np.append(list_2, set)

print("Combining Lists...")
#create array to hold combinations
list_3 = []

for x in list_1:
    for y in list_2:
        list_3 = np.append(list_3,x+y)

np.savetxt(job_number + "_list_1.csv", list_1, fmt='%6s', delimiter=",")
np.savetxt(job_number + "_list_2.csv", list_2, fmt='%6s', delimiter=",")
np.savetxt(job_number + "_pin_list.csv", list_3, fmt='%6s', delimiter=",")

print("Done!")
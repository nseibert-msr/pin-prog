import numpy as np
import random
import string
import math 

#This program automates the creation of pins to be used for validating someones credentials when we send them a mailing. 
# As all the pins need to be uploaded to formidable forms for the validation, it is quicker to upload 2 shorter lists, and then use all the combinations of the two list to get a much larger list.
# i.e. 2 lists, of 10 pins, is only 20 pins to be uploaded, but creates 100 combinations.
#

print("Starting program...")
#Collect starting variables: Length of Pin, total number of pins, and the job number.
pin_length = int(input("How long should each pin be?"))
total_pins = int(input("How many pins do you need?"))
job_number = input("What is the job number?")

#Takes the square root of the total number of pins and rounds up to the nearest integer.
nu_pins = math.ceil(math.sqrt(total_pins))

#initialize arrays to hold lists
list_1 = []
list_2 = []
list_3 = []

#create string to pull characters from and removes I, 0, O as those characters are often confused. 
#This version only uses uppercase and digits 1-9
letters = string.ascii_uppercase + string.digits
letters = letters.replace("I","")
letters = letters.replace("0","")
letters = letters.replace("O","")

#generates list 1
print("Creating List 1")
for x in range(0, nu_pins):
    set = ''.join(random.choice(letters) for i in range(pin_length))
    list_1 = np.append(list_1, set)

#generates list 2
print("Creating List 2")
for x in range(0, nu_pins):
    set = ''.join(random.choice(letters) for i in range(pin_length))
    list_2 = np.append(list_2, set)

print("Combining Lists...")

#iterates over the two lists to create all combinations and append them to the final list
for x in list_1:
    for y in list_2:
        list_3 = np.append(list_3,x+y)

#saves all three lists as csv files and appends the job number to the file name.
np.savetxt(job_number + "_list_1.csv", list_1, fmt='%6s', delimiter=",")
np.savetxt(job_number + "_list_2.csv", list_2, fmt='%6s', delimiter=",")
np.savetxt(job_number + "_pin_list.csv", list_3, fmt='%6s', delimiter=",")

print("Done!")

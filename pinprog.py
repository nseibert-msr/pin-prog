import numpy as np
import random
import string
import math
import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askdirectory()

print(file_path)

# Define a custom exception class
class RestartProgramException(Exception):
    pass

#create string to pull characters from and removes I, 0, O as those characters are often confused. 
#This version only uses uppercase and digits 1-9
letters = string.ascii_uppercase + string.digits
letters_list = []
pins_1 = []

for x in range(0, len(letters)):
    letters_list.append(letters[x])

del letters_list[letters_list.index("I")]
del letters_list[letters_list.index("0")]
del letters_list[letters_list.index("O")]

#This program automates the creation of pins to be used for validating someones credentials when we send them a mailing. 
# As all the pins need to be uploaded to formidable forms for the validation, it is quicker to upload 2 shorter lists, and then use all the combinations of the two list to get a much larger list.
# i.e. 2 lists, of 10 pins, is only 20 pins to be uploaded, but creates 100 combinations.
#

print("Starting program...")
#Collect starting variables: Pin List type, Length of Pin segments, total number of pins, and the job number.
def menu():
    pin_type = int(input("What type of pin list do you want to generate? \n '1' - Single List \n '2' - Duple List \n '9' - quit:  \n"))

    if pin_type==1:
        pin_length = int(input("How many characters should each pin be?   \n"))
    elif pin_type==2:
        pin_length = int(input("How many characters each pin segment be?   \n"))
    elif pin_type==9:
        quit()
    else:
        print("Not a valid entry.")
        menu()

    total_pins = int(input("How many pins do you need?  \n"))
    job_number = input("Enter the five digit job number:  \n")
    
    site_id = int(input("Is this for a mailing or focus on boston distribution? \n'1' - MAIL \n'2' - Focus on Boston \n "))

    if site_id==1:
        site = "MAIL"
    elif site_id==2:
        site = "FOB"
    else:
        print("Not a valid selection")
        menu()

    if pin_type==1:
        pins_single(total_pins,job_number,pin_length)
    elif pin_type==2:
        pins_duple(total_pins,job_number,pin_length,site)
    else:
        menu()

#funtion for creating one list of pins
def pins_single(total_pins,job_number,pin_length):
    print("Creating List 1")
    #initialize arrays to hold lists
    pins_1 = []
    out_name_1 = file_path + "/" + job_number + "_pins.csv"
    for x in range(0, total_pins):
        pin_set = ''.join(random.choice(letters_list) for i in range(pin_length))
        pins_1 = np.append(pins_1, pin_set)
    np.savetxt(out_name_1, pins_1, fmt='%6s', delimiter=",") 
    print("Done!")
    quit()

#function for creating two list of pins that when all combinations of the two lists are combined, generates a list of length of list1 * length of list2
def pins_duple(total_pins,job_number,pin_length, site):
    #Takes the square root of the total number of pins and rounds up to the nearest integer. Add five to each list as a buffer for duplicates.
    nu_pins = math.ceil(math.sqrt(total_pins))+10
    
    #initialize arrays to hold lists
    pins_1 = []
    pins_2 = []
    pins_3 = []
    combined_data = []

    #generates list 1
    print("Creating List 1")
    for x in range(0, nu_pins):
        pin_set = ''.join(random.choice(letters_list) for i in range(pin_length))
        pins_1.append(pin_set)

    #generates list 2
    print("Creating List 2")
    for x in range(0, nu_pins):
        pin_set = ''.join(random.choice(letters_list) for i in range(pin_length))
        pins_2.append(pin_set)
        
    #remove duplicates from lists and then removes any duplicates found in the 2nd pin list compared to the 1st pin list
    pins_1 = list(set(pins_1))
    pins_2 = list(set(pins_2))
    pins_2 = [item for item in pins_2 if item not in pins_1]
    
    #removes any pins from the longer list so that they are the same length
    if len(pins_1) > len(pins_2):
        n = len(pins_1) - len(pins_2)
        del pins_1[-n:]
    elif len(pins_1) < len(pins_2):
        n = len(pins_2) - len(pins_1)
        del pins_2[-n:]
    else: 
        None

    #checks to make sure there will be enough pins after the duplicates have been removed
    if len(pins_1) * len(pins_2) < total_pins:
        raise RestartProgramException()
    else:
        None

    #creates the data table for the formidable forms upload
    combined_data.append(("MSR_ID","PIN_1","PIN_2"))
    for i in range(len(pins_1)):
        combined_data.append((i+1,pins_1[i],pins_2[i]))

    print("Combining Lists...")

    #iterates over the two lists to create all combinations and append them to the final list
    url = "https://marketstreetresearch.com/survey-" + job_number + "/?SITE=" + site
    for x in pins_1:
        for y in pins_2:
            pins_3.append((random.uniform(0,1),x+y,x,y))

    pins_3.sort(key=lambda x: x[0], reverse=False)
    counter=1
    numbered_pins = [('MSR_ID','PIN','PIN-1','PIN-2','URL')]
    for item in pins_3:
        numbered_pins.append((counter,item[1],item[2],item[3],url + "&PIN1=" + item[2] + "&PIN2=" + item[3]))
        counter += 1

    #creates the export name including the file path from the folder prompt
    out_name_1 = file_path + "/" + job_number + "_pins.csv"
    out_name_2 = file_path + "/" + job_number + "_ff_upload.csv"
    
    #exports the final tables as csv files to the folder previously chosen
    np.savetxt(out_name_1, numbered_pins, fmt='%6s', delimiter=",") #File will all combinations of pins to be sent to external vendor
    np.savetxt(out_name_2, combined_data, fmt='%6s', delimiter=",") #File with only each individal pin in two columns for upload to formidable forms
    
    print("Done!")
    quit()

while True:
    try:
        menu()
    except RestartProgramException:
        print("There were too many duplicates generated - Restarting the program...")
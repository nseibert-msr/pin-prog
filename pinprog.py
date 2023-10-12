print("Import numpy")
import numpy as np
print("Import random")
import random
print("Import String")
import string
print("Import Math")
import math
import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askdirectory()

print(file_path)

#create string to pull characters from and removes I, 0, O as those characters are often confused. 
#This version only uses uppercase and digits 1-9
letters = string.ascii_uppercase + string.digits
letters = letters.replace("I","")
letters = letters.replace("0","")
letters = letters.replace("O","")

#This program automates the creation of pins to be used for validating someones credentials when we send them a mailing. 
# As all the pins need to be uploaded to formidable forms for the validation, it is quicker to upload 2 shorter lists, and then use all the combinations of the two list to get a much larger list.
# i.e. 2 lists, of 10 pins, is only 20 pins to be uploaded, but creates 100 combinations.
#

print("Starting program...")
#Collect starting variables: Pin List type,Length of Pin, total number of pins, and the job number.
def menu():
    pin_type = int(input("What type of pin list do you want to generate? Enter '1' for Single List and '2' for Duple List and 99 to quit:  "))

    if pin_type==1:
        pin_length = int(input("How long should each pin be?   "))
    elif pin_type==2:
        pin_length = int(input("How long should each pin segment be?   "))
    elif pin_type==99:
        quit()
    else:
        print("Not a valid pin list.")
        menu()

    total_pins = int(input("How many pins do you need?  "))
    job_number = input("Enter the five digit job number:  ")

    if pin_type==1:
        pin_list_single(total_pins,job_number,pin_length)
    elif pin_type==2:
        pin_list_duple(total_pins,job_number,pin_length)
    else:
        menu()

#funtion for creating one list of pins
def pin_list_single(total_pins,job_number,pin_length):
    print("Creating List 1")
    #initialize arrays to hold lists
    list_1 = []
    for x in range(0, total_pins):
        set = ''.join(random.choice(letters) for i in range(pin_length))
        list_1 = np.append(list_1, set)
    np.savetxt(job_number + "_pin_list.csv", list_1, fmt='%6s', delimiter=",")
    print("Done!")
    quit()

#function for creating two list of pins that when all combinations of the two lists are combined, generates a list of length of list1 * length of list2
def pin_list_duple(total_pins,job_number,pin_length):
    #Takes the square root of the total number of pins and rounds up to the nearest integer. Add two to each list as a buffer for duplicates.
    nu_pins = math.ceil(math.sqrt(total_pins))+2

    #initialize arrays to hold lists
    list_1 = []
    list_2 = []
    list_3 = []
    list_1a = []
    list_2a = []
    combined_data = []

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
        
    #remove duplicates from lists
    list_1a = np.unique(list_1)
    list_2a = np.setdiff1d(np.unique(list_2), list_1a)
    

    combined_data.append(("MSR_ID", "PIN_1", "PIN_2"))
    for i in range(len(list_1a)):
        combined_data.append((i+1,list_1a[i], list_2a[i]))
        


    print("Combining Lists...")

    #iterates over the two lists to create all combinations and append them to the final list
    for x in list_1a:
        for y in list_2a:
            list_3.append((random.uniform(0,1),x+y,x,y))

    out_name_1 = file_path + "/" + job_number + "_pin_list.csv"
    out_name_2 = file_path + "/" + job_number + "_ff_upload.csv"
    
    #saves csv files and appends the job number to the file name.
    np.savetxt(out_name_1, list_3, fmt='%6s', delimiter=",") #File will all combinations of pins to be sent to external vendor
    np.savetxt(out_name_2, combined_data, fmt='%6s', delimiter=",") #File with only each individal pin in two columns for upload to formidable forms
    

    print("Done!")
    quit()

menu()
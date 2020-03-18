#!/usr/bin/env python
# coding: utf-8


"""Premier exemple avec Tkinter.

On crée une fenêtre simple qui souhaite la bienvenue à l'utilisateur.

"""
import gtk
from itertools import groupby
import tkFileDialog
from Tkinter import Menu
import Tkinter as tk
from tkFileDialog import askopenfilename
import colored
from colored import stylize
import pandas as pd
import os.path
import sys
import math 
from time import *
import pyscreenshot
import numpy as np



###Step 1: Create The App Frame
class AppFrame(tk.Frame):


    def __init__(self, parent, *args, **kwargs):
        ###call the parent constructor
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent




        lbl = tk.Label(self, text="Acess Point Flow analyser Cayrol Martin V1.1\n\n Nowadays the access point configuration must be in WPA-AES-CCM")
        lbl.pack()

        ###Create button
        btn = tk.Button(self, text='Choose a CSV file to analyze',command=self.askopenfilename)
        btn.pack(pady=5)

    
   
    def askopenfilename(self):
        ###ask filepath




        filepath = askopenfilename()

        ###if you selected a file path
        if filepath:
            ###add it to the filepath list
            self.parent.filepaths.append(filepath)

            ###put it on the screen
            lbl = tk.Label(self, text=filepath)
            lbl.pack()

            df_paris = pd.read_csv(filepath, sep=','  , engine='python')

            lbl = tk.Label(self, text="--------------------------------------------------------------------------------------------------------------------------")
            lbl.pack()

            lbl = tk.Label(self, text="Number of packets scanned")
            lbl.pack()

            count_row = df_paris.shape[0]

            lbl = tk.Label(self, text=count_row, fg="blue")
            lbl.pack()

            lbl = tk.Label(self, text="Number of packets in authentication mode and management of AES keys")
            lbl.pack()

            AKM = df_paris.GroupCipherSuitetype.str.count("AES").sum()

            lbl = tk.Label(self, text=AKM, fg="blue")
            lbl.pack()

            lbl = tk.Label(self, text="Number of Packets in WPA/WPA2 Cryptographic Suite")
            lbl.pack()

            GCS = df_paris.AuthKeyManagementtype.str.count("WPA").sum()

            lbl = tk.Label(self, text=GCS, fg="blue")
            lbl.pack()

            count_row = float(count_row)
            AKM = float(AKM)
            GCS = float(GCS)
            SUM = count_row * 2 - GCS - AKM

            lbl = tk.Label(self, text="Number of packages with a different configuration")
            lbl.pack()
            lbl = tk.Label(self, text=SUM, fg="blue")
            lbl.pack()

            dbm_max = df_paris['dBm'].max()
            dbm_min = df_paris['dBm'].min()

            df_paris['dBm'] = df_paris['dBm'].str.extract('(\d+)')
            moyenne = df_paris['dBm'].mean()
            
            #lbl = tk.Label(self, text=moyenne)
            #lbl.pack()

            
            #dbm_min = [int(''.join(i)) for is_digit, i in groupby(dbm_min, str.isdigit) if is_digit]
            #dbm_max = [int(''.join(i)) for is_digit, i in groupby(dbm_max, str.isdigit) if is_digit]


            
            #dbm_min = [int(i) for i in dbm_min]
            #dbm_max = [int(i) for i in dbm_max]

            #dbm_min = ','.join([str(i) for i in value_list])
            #dbm_min = ','.join([str(i) for i in value_list])


            lbl = tk.Label(self, text="--------------------------------------------------------------------------------------------------------------------------", fg="black")
            lbl.pack()

            lbl = tk.Label(self, text="Location of the AP")
            lbl.pack()
            lbl = tk.Label(self, text="")
            lbl.pack()
       
            lbl = tk.Label(self, text="the lowest value is : " + dbm_min, fg="brown")
            lbl.pack()
            lbl = tk.Label(self, text="The highest value is : " + dbm_max + " dBm", fg="brown")
            lbl.pack()
            lbl = tk.Label(self, text="")
            lbl.pack()

            count1 = df_paris['Time'].max()
            count1 = math.trunc(count1)
            count1 = strftime('%H %M %S', gmtime(count1))
          

            

            
            
            lbl = tk.Label(self, text="Duration of passive analysis (in h:m:s) : " + count1, fg="brown")
            lbl.pack()

            #lbl = tk.Label(self, text=count1, fg="brown")
            #lbl.pack()
            count2 = df_paris['Time'].diff().max()
            count2 = math.trunc(count2)
            

            if count2 > 20:
                count2 = str(count2)
                lbl = tk.Label(self, text="Caution, the ap flow has been cut off during : " + count2 + " second", fg="red")
                lbl.pack()
           
            


            lbl = tk.Label(self, text="--------------------------------------------------------------------------------------------------------------------------")
            lbl.pack()

            if SUM == 0.0:
            	lbl = tk.Label(self, text="The configuration of the access point has remained the same, the test is deemed valid.", fg="green")
            	lbl.pack()
            else:
            	lbl = tk.Label(self, text="Packages underwent a configuration change during the analysis", fg="black")
            	lbl.pack()
            	lbl = tk.Label(self, text="the test is therefore INVALID", fg="red")
            	lbl.pack()

            	lbl = tk.Label(self, text="The configuration has changed for the following lines: ", fg="black")
            	lbl.pack()

			
            for n,line in enumerate(open(filepath)):
    		    if "WEP" in line: lbl = tk.Label(self, text=n+1, fg="green")
    		    lbl.pack()



        


###Step 2: Creating The App
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        ###call the parent constructor
        tk.Tk.__init__(self, *args, **kwargs)

        ###create filepath list
        self.filepaths = []

        ###show app frame
        self.appFrame = AppFrame(self)
        self.appFrame.pack(side="top",fill="both",expand=True)

        

    


###Step 3: Bootstrap the app
def main():
    app = App()
    app.mainloop()
          

if __name__ == '__main__':
    main()
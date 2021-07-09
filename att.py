from datetime import date
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os





def open_file():
    global src_file_dir
    global dest_file_dir
    
    
    init_dir=os.getcwd()
    filename=filedialog.askopenfile(initialdir=init_dir,title='choose file',filetypes=(('xlsx file','*.xlsx'),('csv files','*.csv'),('all files','*.*')))
    src_file_dir=filename.name
    src_file_dir
    
root = tk.Tk()
root.title('Attendnce Marker')

open_src_file_label = tk.Label(root,text='source file directory :').pack()
input_box_src=tk.Text(root,height = 3,width = 25).pack()
open_source_file_button = tk.Button(root,text='Open source file',command=open_file).pack()

print(src_file_dir)


root.mainloop()




# data = pd.read_csv(r"D:\downloads\meetingAttendanceList (2).csv",encoding='utf-16',delimiter='\t')

# # data.drop('User Action',inplace=True, axis=1)
# print(data)
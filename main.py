# -*- coding: utf-8 -*-
from generator import *

import tkinter as tk
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import Workbook
'''
09/20/2023
Create-Elevator-Lobby function inputs are re-organized to SEVEN items. Right now the lstBase input is the one to be tackled.
The main function is not callable for now, its inputs need to be re-aligned with the functions in GENERATOR file.
10/10/2023
The main generating funciton is working, the user interface is roughly there, but the user input still needs to processed properly.
10/11/2023
PyInstall Compile successfully
Populate Button just got started, the overall workflow is working but rn it's not really reading the dir and file name from the user input'
'''


#-----------------------------------------------------------
#Preparation
#Dispatcher
dispatcher = {'CEL':createElevatorLobby,
              'CGE':createGuestElevByClosest,
              'CFA':createFromAccessible,             
              
              }
#-----------------------------------------------------------
#User Interface
line_names = ['Row','Column','Episode']
for i in range(20):
    line_names.append('Module ' + str(i))

line_examples = ['6','7','100',
                 ['CEL',None,6,'L_1',1],
                 ['CGE','L_1',6,'GE_1',None],
                 ['CEL',None,3,'L_2',1],
                 ['CGE','L_2',5,'GE_2',None],
                 ['CEL',None,3,'L_3',1],
                 ['CGE','L_3',4,'GE_3',None],
                 ['CFA',None,2,'V_1',None],
                 ['CFA','V_1',2,'S_1',None],
                 ['CFA','V_1',1,'FE',None],
                 ['CFA','V_1',1,'FE',None],
                 ['CFA',None,1,'V_2',None],
                 ['CFA','V_2',2,'S_2',None],
                 ['CFA',None,1,'ADA',None],
                 ['CFA',None,1,'MEP',None],
                 ['CFA',None,1,'MEP',None],
                 ['CFA',None,1,'MEP',None],
                 ['CFA',None,1,'SHAFT',None],
                 ['CFA',None,1,'SHAFT',None]]

root = tk.Tk()
root.title("Text Editor")
top_instruction_label = tk.Label(root, text='Enter your action inputs below, \n'
                                 + 'you can also copy the example code from the right side')
top_instruction_label.pack(pady=5)

#-----------------------------------------------------------
#Button Functions
def readInput():
    text_raw = text_widget.get('1.0',"end-1c").splitlines()
    #Grab first three parameters
    text_list = []
    for line_raw in text_raw:
        line_raw = line_raw.replace(" ", "")#PBCAK - EXTRA SPACE
        line_list = line_raw.split(',')
        text_list.append(line_list)
    try:
        maxRow = eval(text_list[0][0])
        maxCol = eval(text_list[1][0])
        episode = eval(text_list[2][0])
    except:#PBACK ALERT
        print ('PLEASE CHECK YOUR FIRST THREE INPUTS')
        return None
    #Convert strings to python variables
    converted_list = []
    for i,list_raw in enumerate(text_list):
        if i<=2:#PBCAK ALERT
            if len(list_raw)>1:
                print ('PLEASE CHECK YOUR FIRST THREE INPUTS')
                return None
        else:
            sub_list = []
            for stuff in list_raw:
                try:
                    sub_list.append(eval(stuff))
                except:
                    sub_list.append(stuff)
            converted_list.append(sub_list)
    #Dispatching
    for stuff in converted_list:
        try:
            stuff[0] = dispatcher[stuff[0]]
        except:
            print ('PLEASE CHECK YOUR FUNCTION ABBREVIATIONS')
           
    return maxRow, maxCol, episode, converted_list

def plot(lstCell,mapCore, dictProgram, programDict,maxRow, maxCol):
    #Create a different window to display heatmap
    heatmap_window = Toplevel(root)
    heatmap_window.title("Heatmap")
        
    plt.cla()
    plt.figure(figsize=(maxCol, maxRow))
    map_function = np.vectorize(lambda x: dictProgram.get(x, x))
    mapCoreProgram = map_function(mapCore)
    ax = sns.heatmap(mapCore, cmap="inferno_r", annot=mapCoreProgram, 
                     linewidths = 1,cbar = False,
                     annot_kws={'fontsize': 10},fmt='',vmin=0, 
                     vmax=len(dictProgram))    
    
    canvas = FigureCanvasTkAgg(plt.gcf(), master=heatmap_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()    
    
def populate():
    book = Workbook()
    sheet = book.active
    maxRow, maxCol, episode, lstFuncs = readInput()
    counter = 0
    for i in tqdm(range(episode)):
        lstCell,mapCore,dictProgram,programDict = generate(maxRow,maxCol,lstFuncs)
        if not (0 in mapCore):
            lstText = [dictProgram[stuff] for stuff in mapCore.flatten().tolist()]
            for j,stuff in enumerate(lstText):
                sheet.cell(row = counter + 1, column = j + 1).value = str(lstText[j])
            counter += 1
    book.save('test.xlsx')
    print (counter)
    
def createOne():
    maxRow, maxCol, episode, lstFuncs = readInput()
    for i in range(episode):
        lstCell,mapCore,dictProgram,programDict = generate(maxRow,maxCol,lstFuncs)
        if not (0 in mapCore):
            print ('got one layout after ' + str(i) + ' tries')  
            plot(lstCell,mapCore, dictProgram,programDict,maxRow,maxCol)
            print (mapCore)
            return mapCore
        elif i == episode - 1:
            print ('got nothing after ' + str(episode) + ' episodes')

def extraInput():
    input_window = tk.Tk()
    input_window.title('Core Layout Saving')
    
    input_label = tk.Label(input_window, text = "Enter your file name below")
    input_label.pack()
    
    input_entry = tk.Entry(input_window)
    input_entry.pack()    
    
    input_label_b = tk.Label(input_window, text = "Enter the path to your folder")
    input_label_b.pack()
    
    input_entry_b = tk.Entry(input_window)
    input_entry_b.pack()  
        
    def go_populate():
        name_save = input_entry.get()
        dir_save = input_entry_b.get()
        print (name_save)
        populate()
        input_window.destroy()
            
    submit_button = tk.Button(input_window, text = 'Start Populating', command = go_populate)
    submit_button.pack()
    
    input_window.mainloop()
    
        
#-----------------------------------------------------------
printButton = tk.Button(root, 
                        text = "Create One",  
                        command = createOne) 
printButton.pack(pady= 5)
#-----------------------------------------------------------
populateButton = tk.Button(root, 
                        text = "Populate",  
                        command = extraInput) 
populateButton.pack(pady= 5)

# Create a frame to hold the line names labels
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=(5, 0), pady = (0,0),fill=tk.Y)

# Create labels for each line name and pack them in the frame
for name in line_names:
    label = tk.Label(left_frame, text=name, anchor="e", padx=5, pady = 0)
    label.pack(fill=tk.X,pady = 0,ipady = 0)

# Text Box
text_widget = tk.Text(root, wrap=tk.WORD,width = 30, spacing1=1, spacing3=5)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH,expand=True)

# Create example labels
right_instruction_text = tk.Text(root, wrap=tk.WORD,height = len(line_names), 
                                 width = 50,spacing1=1, spacing3=5, bg = 'beige')
right_instruction_text.pack(pady=0,padx=5, anchor = 'n',side=tk.RIGHT)

# Right instruction labels
for example in line_examples:
    if  isinstance(example, list):
        single_example = ''
        for stuff in example:
            single_example = single_example + str(stuff) + ','
        single_example = single_example[:-1]
    else:
        single_example = example
    right_instruction_text.insert(tk.END, str(single_example) + "\n")
right_instruction_text.configure(state="disabled")

root.mainloop()
#-----------------------------------------------------------











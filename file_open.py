#DEPRECIATED, OLD METHOD OF LOADING FILES / FILE INTERFACE

from PySimpleGUI.PySimpleGUI import MenubarCustom, Titlebar
import PySimpleGUI as sg
import os


def fileopen():
    file_type_list = [
        ("", "*"),
        ("Ada",".ada"),
        ("Bash", ".bash"),
        ("Batch", ".bat"),
        ("Brainfuck", ".bf"),
        ("C",".c"),
        ("C++",".cpp"),
        ("C-Make",".cmake"),
        ("CoffeeScript",".coffee"),
        ("CSS",".css"),
        ("C#",".cs"),
        ("Dart",".dart"),
        ("DockerFile",".dockerfile"),
        ("Go Script",".go"),
        ("Groovy",".groovy"),
        ("Haskell",".hs"),
        ("HTML",".html"),
        ("Java",".java"),
        ("JavaScript",".js"),
        ("JSON",".json"),
        ("TXT",".txt"),
        ("Kotlin",".kt"),
        ("Lisp",".lisp"),
        ("Lua",".lua"),
        ("MakerFile",".mak"),
        ("MatLab",".mat"),
        ("NASM",".nasm"),
        ("Objective-C",".m"),
        ("Perl",".p6"),
        ("PHP",".php"),
        ("SQL",".sql"),
        ("Swift",".swift"),
        ("Python",".py"),
        ("R",".r"),
        ("Ruby",".rb"),
        ("TCL",".tcl"),
        ("VIM",".vim"),
        ("YAML", ".yaml")
        
    ]
    sg.theme('Reddit')
    icon_path = os.path.join(os.path.dirname(__file__), 'tiny_icon.png')   
    layout = [[Titlebar(title = "SimpIDE", icon = icon_path, background_color = "black")],
            [sg.FileSaveAs(target = "-CREATE-", key = "-CREATE-", button_text = "Create", size = ("20",None), file_types = file_type_list, default_extension = ".txt", enable_events=True), sg.FileBrowse(target = "-OPEN-", button_text = "Open", key = "-OPEN-", size = ("20",None), enable_events=True)]]
            # [sg.Button(button_text = "Let's Go", key = "-SUBMIT-", focus = True)]]
    
    
    window = sg.Window('SimpIDE', layout, button_color = "purple")
    #event loop for input, makes the window persistent
    while True:
        event, values = window.read()
        path = "" 
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            return 0  
        elif values["-OPEN-"] != "":
            path = values["-OPEN-"]
            window.close()
            return path,"open"
        elif values["-CREATE-"] != "":
            path = values["-CREATE-"]
            window.close()
            return path,"create"
        else:
            print("No value, passing...")
            pass
    #closes window when breaking out of event loop
    

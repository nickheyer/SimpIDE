
from contextlib import suppress
import tkinter
from tkcode import CodeEditor
from file_open import fileopen
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import *
import threading
import io
import os
import keyboard
from time import sleep
import sys
from ttkthemes import ThemedTk
from tkinter import filedialog
import ctypes.wintypes
from ctypes import windll
import time
import pyautogui
from PIL import ImageTk, Image
import webbrowser

#Constant variables, out of loop
file_list = {}
target_file = None
prev_tab = None
prev_geom = None
is_fs = False
map_state_count = 0
GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080
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
#File Class
class Files():
    def __init__(self, file_path):    
        self.file_path = file_path
        if "/" in self.file_path:
            self.file_name = file_path.split("/")[-1]
        else:
            self.file_name = file_path.split("\\")[-1]
        self.file_ext = self.file_name.strip().split(".")[1].lower()
        self.indent_stop = False
        
    def __repr__(self):
        return self.file_path
    
    def get_lang(self):
        if self.file_ext == "ada":
            self.file_lang = "ADA"
        elif self.file_ext  == "bash":
            self.file_lang = "Bash"
        elif self.file_ext == "bat":
            self.file_lang = "Batch"
        elif self.file_ext  in ["brainfuck", "bf"]:
            self.file_lang = "Brainfuck"
        elif self.file_ext  == "c":
            self.file_lang = "C"
        elif self.file_ext  == "cmake":
            self.file_lang = "Cmake"
        elif self.file_ext  in ["coffeescript", "coffee"]:
            self.file_lang = "CoffeeScript"
        elif self.file_ext  == "css":
            self.file_lang = "CSS"
        elif self.file_ext  in ["c sharp", "cs", "c#"]:
            self.file_lang = "C#"
        elif self.file_ext  in ["c plus plus", "cpp", "c++"]:
            self.file_lang = "C++"
        elif self.file_ext  == "dart":
            self.file_lang = "Dart"
        elif self.file_ext  == "delphi":
            self.file_lang = "Delphi"
        elif self.file_ext  in ["dockerfile", "docker"]:
            self.file_lang = "Dockerfile"
        elif self.file_ext  == "fortran":
            self.file_lang = "Fortran"
        elif self.file_ext  in ["go", "goself.file_ext "]:
            self.file_lang = "Go"
        elif self.file_ext  == "groovy":
            self.file_lang = "Groovy"
        elif self.file_ext  == "haskell":
            self.file_lang = "Haskell"
        elif self.file_ext  == "html":
            self.file_lang = "HTML"
        elif self.file_ext  == "java":
            self.file_lang = "Java"
        elif self.file_ext  in ["javascript", "js"]:
            self.file_lang = "JavaScript"
        elif self.file_ext  == "json":
            self.file_lang = "JSON"
        elif self.file_ext  == "txt" or self.file_ext  == "md" or self.file_ext  == "spec":
            self.file_lang = "TXT"
        elif self.file_ext  == "kotlin":
            self.file_lang = "Kotlin"
        elif self.file_ext  == "lisp":
            self.file_lang = "Lisp"
        elif self.file_ext  == "lua":
            self.file_lang == "Lua"
        elif self.file_ext  == "makefile":
            self.file_lang = "Makefile"
        elif self.file_ext  == "matlab":
            self.file_lang = "MatLab"
        elif self.file_ext  == "nasm":
            self.file_lang = "Nasm"
        elif self.file_ext  in ["objective-c", "objectivec"]:
            self.file_lang = "Objective-C"
        elif self.file_ext  == "perl":
            self.file_lang = "Perl"
        elif self.file_ext  == "php":
            self.file_lang = "PHP"
        elif self.file_ext  == "powershell":
            self.file_lang = "PowerShell"
        elif self.file_ext  in ["python", "py"]:
            self.file_lang = "Python"
        elif self.file_ext  in ["r", "erself.file_ext "]:
            self.file_lang = "R"
        elif self.file_ext  == "ruby":
            self.file_lang = "Ruby"
        elif self.file_ext  == "swift":
            self.file_lang = "Swift"
        elif self.file_ext  == "sql":
            self.file_lang = "SQL"
        elif self.file_ext  == "tcl":
            self.file_lang = "Tcl"
        elif self.file_ext  in ["typescript", "ts"]:
            self.file_lang = "TypeScript"
        elif self.file_ext  == "vim":
            self.file_lang = "Vim"
        elif self.file_ext  == "yaml":
            self.file_lang = "YAML"
        return self.file_lang

    def add_tab(self, tab):
        self.tab = tab
    def add_editor(self, editor):
        self.editor = editor
        self.editor_content = editor.content

#Instantiating the simp_pad
CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value
buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
starter_f = os.path.join(buf.value, 'simp_pad.txt')
starter_tmp = ""
for x in starter_f:
    if x == "\ ".strip():
        starter_tmp += "/"
    else:
        starter_tmp += x
starter_f = starter_tmp
file_list[starter_f] = Files(starter_f)

#Instantiating (Potentially) the 'open with' File = sys arg 1
#Path var for 'open with SimpIDE' Attempting to init
try:
    file_list[f'{sys.argv[1]}'] = Files(sys.argv[1])
except:
    pass

def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())


#Main 
def main():

    
    #CONFIGURING ROOT/MAIN WINDOW
    root = ThemedTk(theme="black")
    
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    icon_png_path = os.path.join(os.path.dirname(__file__), 'icon.png')
    tiny_icon_png_path = os.path.join(os.path.dirname(__file__), 'tiny_icon.png') 
    root.iconbitmap(icon_path)
    root.title("SimpIDE")
    root.option_add("*tearOff", 0)
    root.after(10, lambda: set_appwindow(root))
    root.configure(bg="black")
    root.configure(borderwidth = 2, relief = "ridge")
    #Fullscreen func for root window
    root.overrideredirect(1)
    def fullscreen_func(modifier):
        global prev_geom, is_fs, map_state_count
        map_state_count = True
        if modifier == "FS":
            if is_fs == True:
                return
            if is_fs == False:
                prev_geom = root.geometry()
            is_fs = True
            root.overrideredirect(0)
            root.attributes("-fullscreen", True)
        elif modifier == "MS":
            if is_fs == False:
                return
            is_fs = False
            root.overrideredirect(1)
            root.attributes("-fullscreen", False)
            root.geometry(f"+{int(pyautogui.position()[0]/4)}+{int(pyautogui.position()[1]/4)}") 
    root.bind("<Shift-Escape>", lambda a :fullscreen_func("MS"))
    root.bind("<F1>", lambda b: fullscreen_func("FS"))
    
    def fullscreen_toggle():
        global prev_geom, is_fs, map_state_count
        map_state_count = True
        if is_fs == False:
            prev_geom = root.geometry()
            is_fs = True
            root.overrideredirect(0)
            root.attributes("-fullscreen", True)    
        else:
            is_fs = False
            root.overrideredirect(1)
            root.attributes("-fullscreen", False)
            root.geometry(f"+{int(pyautogui.position()[0]/4)}+{int(pyautogui.position()[1]/4)}") 

    def roundPolygon(x, y, sharpness, **kwargs): #Depreciated, but saving for future ref
        #For rounded corners
        if sharpness < 2:
            sharpness = 2
        ratioMultiplier = sharpness - 1
        ratioDividend = sharpness
        points = []
        # Iterate over the x points
        for i in range(len(x)):
            # Set vertex
            points.append(x[i])
            points.append(y[i])
            # If it's not the last point
            if i != (len(x) - 1):
                # Insert submultiples points. The more the sharpness, the more these points will be
                # closer to the vertex. 
                points.append((ratioMultiplier*x[i] + x[i + 1])/ratioDividend)
                points.append((ratioMultiplier*y[i] + y[i + 1])/ratioDividend)
                points.append((ratioMultiplier*x[i + 1] + x[i])/ratioDividend)
                points.append((ratioMultiplier*y[i + 1] + y[i])/ratioDividend)
            else:
                # Insert submultiples points.
                points.append((ratioMultiplier*x[i] + x[0])/ratioDividend)
                points.append((ratioMultiplier*y[i] + y[0])/ratioDividend)
                points.append((ratioMultiplier*x[0] + x[i])/ratioDividend)
                points.append((ratioMultiplier*y[0] + y[i])/ratioDividend)
                # Close the polygon
                points.append(x[0])
                points.append(y[0])
        return root.create_polygon(points, **kwargs, smooth=TRUE)
    
    #Custom Option Window
    def custom_option_tab():
        for x in notebook.tabs():
            notebook.tab(x, state = "disabled")
        option_tab = ttk.Frame(notebook)
        notebook.insert(0, option_tab, text = "Confirm")
        option_editor = CodeEditor(
            option_tab,
            width = 30,
            height = 30,
            language = "TXT",
            background = "black",
            font="Consolas",
            autofocus=True,
            blockcursor=True,
            insertofftime=0,
            startline = 0,
            padx=10,
            pady=10,
        )
        option_editor.pack(fill="both", expand=True)
        prompt = "Quitting SimpIDE...\n\nWould you like to save all your tabs?\n\nY ~ Yes, i'd like to save.\n\nN ~ Nope, no saves for me.\n\nC ~ Cancel, back to Simp'in.\n\n\nPlease enter below (y, n, or c) or press escape.\n------------------------------------------------\n "
        option_editor.content = prompt
        root.bind("y", lambda event:option_y())
        root.bind("n", lambda event:option_n())
        root.bind("c", lambda event:option_c())
        root.bind("<Control-s>")
        root.unbind("<Control-o>")
        root.unbind("<Control-n>")
        root.unbind("<Escape>")
        exit_button.unbind("<ButtonRelease-1>")
        root.bind("<Escape>", lambda event:option_y())
        exit_button.bind("<ButtonRelease-1>", lambda event:option_y())
        root.protocol("WM_DELETE_WINDOW", lambda: option_y())
        if option_editor.content != prompt:
            option_answer = option_editor.content[-1]
            if option_answer.lower() not in ("y","n","c"):
                option_editor.content = prompt
                pass
            def option_y():
                save_all()
                root.quit()
                root.destroy()
            def option_n():
                root.quit()
                root.destroy()
            def option_c():
                root.unbind("<Escape>")
                root.unbind("y")
                root.unbind("n")
                root.unbind("c")
                exit_button.unbind("<ButtonRelease-1>")
                exit_button.bind("<ButtonRelease-1>", lambda event:on_quit())
                root.bind("<Control-s>", lambda event:on_saving())
                root.bind("<Control-o>", lambda event:open_file())
                root.bind("<Control-n>", lambda event:create_file())
                root.bind("<Escape>", lambda event:on_quit())
                root.protocol("WM_DELETE_WINDOW", on_quit)               
                notebook.forget(0)
                for x in notebook.tabs():
                    notebook.tab(x, state = "normal")
                notebook.select(prev_tab)
                return  
    def save_all():
        for x in file_list.values():
            with io.open(x.file_path, "w", encoding="utf-8", errors="ignore") as file_to_save:
                file_to_save.write(x.editor.content[:-1])    
    def get_info_from_tab():
        menu_tabs = [
            "Create - Ctrl+N", 
            "Open - Ctrl+O", 
            "Save - Ctrl+S", 
            "Save+Run (.py/.cpp) - Ctrl+R", 
            "Close - Esc", 
            "Running Code",  
            "Confirm"
            ]
        if notebook.tab(notebook.select(), "text") in menu_tabs:
            return
        for x in file_list.values():
            if x.file_name == notebook.tab(notebook.select(), 'text'):
                if x == None:
                    return file_list[starter_f]
                else:
                    return x
    def on_saving():
            with io.open(get_info_from_tab().file_path, "w", encoding="utf-8", errors="ignore") as file_to_save:
                file_to_save.write(get_info_from_tab().editor.content[:-1])  
    def on_quit():
        custom_option_tab()
    def get_parent_folder(path):
        split_path = path.split("/")
        parent = "/".join(split_path[:-1])
        return parent  

    def on_run():
        on_saving()
        for xxx in notebook.tabs():
            notebook.tab(xxx, state = "disabled")
        option_tab = ttk.Frame(notebook)
        notebook.insert(0, option_tab, text = "Running Code")
        option_editor = CodeEditor(
            option_tab,
            width = 30,
            height = 30,
            language = "TXT",
            background = "black",
            font="Consolas",
            autofocus=True,
            blockcursor=True,
            insertofftime=0,
            padx=10,
            pady=10,
            startline = 0,
        )
        option_editor.pack(fill="both", expand=True)
        option_editor.content += "Please choose which tab to run >>\n\n"
        dict_of_tabs = {}
        for xx in notebook.tabs():
            for yy,zz in enumerate(file_list.values()):
                if str(zz.tab) == str(xx):
                    option_editor.content += f"{yy + 1}. {zz.file_name}"
                    dict_of_tabs[yy+1] = zz
        option_editor.content += "\nEnter your selection below.\n---------------------------\n"
        def wait_for_input(key):
            for xz,yz in dict_of_tabs.items():
                if key.char == str(xz):
                    with io.open(os.path.join(buf.value, 'code_to_run.txt'), "w", encoding = "utf-8", errors="ignore") as clear_doc:
                        clear_doc.write("")
                    input_bool = False
                    if dict_of_tabs[xz].file_ext == "py":
                        option_editor.content = ""
                        if "input(" in dict_of_tabs[xz].editor.content:
                            option_editor.content += f"CMD input required for {dict_of_tabs[xz].file_name}, please run file manually.\nSpawning CMD terminal. \nSince you are already in the correct dir,\nsimply type 'python {dict_of_tabs[xz].file_name}'"
                            input_bool = True
                            os.system(f'start cmd.exe cmd /K "cd {get_parent_folder(dict_of_tabs[xz].file_path)}"')
                        else:
                            os.system(f'cd "{get_parent_folder(dict_of_tabs[xz].file_path)}" & python "{dict_of_tabs[xz].file_name}" > {os.path.join(buf.value, "code_to_run.txt")}')
                    elif dict_of_tabs[xz].file_ext == "cpp":
                        option_editor.content = ""
                        if "cin" not in dict_of_tabs[xz].editor.content:
                            os.system(f'cd "{get_parent_folder(dict_of_tabs[xz].file_path)}" && g++ "{dict_of_tabs[xz].file_name}" -o output && .\\output.exe > {os.path.join(buf.value, "code_to_run.txt")}"' )
                        else:
                            option_editor.content += f"CMD input required for {dict_of_tabs[xz].file_name}, please run file manually.\nSpawning CMD terminal.\nSince your program has already been compiled and you are in the correct dir,\nsimply type '.\\output.exe'"
                            input_bool = True
                            os.system(f'start cmd.exe cmd /K "cd {get_parent_folder(dict_of_tabs[xz].file_path)} && g++ "{dict_of_tabs[xz].file_name}" -o output"')
                    with io.open(os.path.join(buf.value, 'code_to_run.txt'), "r", encoding = "utf-8", errors="ignore") as input_output:
                        if input_bool != True:
                            try:
                                output_read = input_output.read().splitlines()
                                extra_dash = len(os.path.join(buf.value, 'code_to_run.txt')) * "-"
                                output_read.insert(0, f"""See below for your code's output.\nA text-file containing this output can be found at {os.path.join(buf.value, 'code_to_run.txt')}
---------------------------------------------------{extra_dash}""")
                                output_readout = "\n".join(output_read)
                            except:
                                output_readout = "Code run, no output provided."
                            option_editor.content += output_readout
        root.bind("<Key>", wait_for_input)
        for xxx in notebook.tabs()[5:]:
            notebook.tab(xxx, state = "normal")
        def unlock_tabs_and_delete_running():
            notebook.forget(option_tab)
            for xxx in notebook.tabs():
                notebook.tab(xxx, state = "normal")   
            root.unbind("<<NotebookTabChanged>>")
            root.unbind("<Key>")
        root.bind("<<NotebookTabChanged>>", lambda event:unlock_tabs_and_delete_running())
        
    def open_file(): 
        file = filedialog.askopenfile(mode ='r', filetypes = file_type_list) 
        if file is not None:    
            file_list[file.name] = Files(file.name)
            tab = ttk.Frame(notebook)
            file_list[file.name].add_tab(tab)
            notebook.insert("end", tab, text = file.name.split("/")[-1])
            code_editor = CodeEditor(
                            file_list[file.name].tab,
                            width=99,
                            height=30,
                            language=file_list[file.name].get_lang(),
                            background="black",
                            highlighter="dracula",
                            font="Consolas",
                            autofocus=True,
                            blockcursor=False,
                            insertofftime=0,
                            padx=10,
                            pady=10,
                            startline = 0
                            )
            code_editor.content = file.read()
            file_list[file.name].add_editor(code_editor)
            code_editor.pack(fill="both", expand=True)
            notebook.select(tab) 
    def create_file():
        file = filedialog.asksaveasfile(mode = 'w', filetypes = file_type_list)  
        if file is not None:
            file_list[file.name] = Files(file.name)
            tab = ttk.Frame(notebook)
            file_list[file.name].add_tab(tab)
            notebook.insert("end", tab, text = file.name.split("/")[-1])
            code_editor = CodeEditor(
                            file_list[file.name].tab,
                            width=99,
                            height=30,
                            language=file_list[file.name].get_lang(),
                            background="black",
                            highlighter="dracula",
                            font="Consolas",
                            autofocus=True,
                            blockcursor=False,
                            insertofftime=0,
                            padx=10,
                            pady=10,
                            startline = 0,
                            undo = True
                            )

            code_editor.pack(fill="both", expand=True)
            file_list[file.name].add_editor(code_editor)
            with io.open(file.name, "w", encoding="utf-8", errors="ignore") as file_to_save:
                file_to_save.write(file_list[file.name].editor_content) 
            notebook.select(tab) 
    notebook = ttk.Notebook(root)

    def minimize_window():
        global map_state_count
        root.withdraw()
        root.overrideredirect(False)
        root.iconify()  
        map_state_count = True
    
    def check_map(event): # apply override on deiconify.
        global map_state_count
        if str(event) == "<Map event>": #Deiconified
            if map_state_count == True and root.state() == "normal":
                root.overrideredirect(1)
                root.after(10, lambda: set_appwindow(root))
                map_state_count = False            
        else: #Iconified, minimized          
            pass
    
    # #Defining style for buttons
    s = ttk.Style()
    s.configure('Test.TLabel', anchor=tk.N)
   
#Window movement / "grips" / RIGHT SIDE MENU BUTTONS
     #Top
    icon_img = ImageTk.PhotoImage(Image.open(icon_png_path))
    tiny_icon_img = ImageTk.PhotoImage(Image.open(tiny_icon_png_path))
    grip_label = ttk.Label(width = 20, borderwidth = 2, relief = "raised") #Right
    grip_label_2 = ttk.Label(borderwidth = 2, relief = "raised", image = tiny_icon_img, anchor = tk.CENTER)
    title_button = ttk.Button(grip_label, text = " SimpIDE V0.6", takefocus=0, compound=tk.CENTER, command=lambda :webbrowser.open_new("https://github.com/nickheyer/SimpIDE"), cursor = "coffee_mug")
    icon_title = ttk.Label(grip_label, image = icon_img, borderwidth = 2, relief = "raised", compound=tk.CENTER)
    web_button = ttk.Button(grip_label, text = " www.heyer.app", takefocus=0, compound=tk.CENTER, command=lambda :webbrowser.open_new("https://www.heyer.app"), cursor = "coffee_mug")

#MENU FUCKING BUTTONS FUCK THIS SHIT
    exit_button = ttk.Button(grip_label_2, text = u"\u29BB", compound=tk.CENTER, width = 2.75, takefocus=0)
    max_button = ttk.Button(grip_label_2, text = u"\u25F3", compound=tk.CENTER, width = 2.75, takefocus=0)
    min_button = ttk.Button(grip_label_2, text = u"\u2509", compound=tk.CENTER, width = 2.75, takefocus=0)
    resize_button = ttk.Button(grip_label, text = u" \u2928", width = 2.75, takefocus=0, compound=tk.CENTER, cursor = "bottom_right_corner")
    exit_button.pack(side = "right", fill = "x", padx = (7,25))
    max_button.pack(side = "right", fill = "x", padx = 7)
    min_button.pack(side = "right", fill = "x", padx = 7)
    resize_button.pack(side = "bottom", anchor = tk.SE, ipadx = 2.75)
    icon_title.pack(side = "top", fill = "x", expand= False, ipadx = 5, ipady = 5, pady=5, padx = 5, anchor = tk.CENTER)
    grip_label_2.pack(side = "top", fill = "both", expand = False, ipady = 10)
    grip_label.pack(side = "right", fill = "both", expand = False)
    title_button.pack(side = "top", fill = "x", expand= False, pady=5, padx = 5)
    web_button.pack(side = "top", fill = "x", expand= False, pady=5, padx = 5)
    exit_button.bind("<ButtonRelease-1>", lambda event: on_quit())
    max_button.bind("<ButtonRelease-1>", lambda event: fullscreen_toggle())
    min_button.bind("<ButtonRelease-1>", lambda event: minimize_window())

    #Creating line numbers, depcreciated till I can find a 'less-hacky' way. 
    # line_style = ttk.Style()
    # line_style.configure('Line.TLabel')
    # def line_labeler(event):
    #     for x in line_num_label.winfo_children()[1:]:
    #         x.destroy()
    #     for x in range(len(get_info_from_tab().editor.content.splitlines())):
    #         if x == 0:
    #             line_label = ttk.Label(line_num_label, text = x + 1, width = 3, borderwidth = 3, relief = "raised", style = 'Line.TLabel')
    #             line_label.pack(side = "top", fill = "x", expand = False, ipady = 9)
    #         else:
    #             line_label = ttk.Label(line_num_label, text = x + 1, width = 3, borderwidth = 3, relief = "raised", style = 'Line.TLabel')
    #             line_label.pack(side = "top", fill = "x", expand = False, ipady = 3.5) 
    # root.after(100, line_labeler)
    # root.after(100, line_labeler)
    
    x, y = 0, 0
    def mouse_motion(event):
        global x, y
        # Positive offset represent the mouse is moving to the lower right corner, negative moving to the upper left corner
        offset_x, offset_y = event.x - x, event.y - y  
        new_x = root.winfo_x() + offset_x
        new_y = root.winfo_y() + offset_y
        new_geometry = f"+{new_x}+{new_y}"
        root.geometry(new_geometry)

    def OnMotion(event):
        x1 = root.winfo_pointerx()
        y1 = root.winfo_pointery()
        x0 = root.winfo_rootx()
        y0 = root.winfo_rooty()
        root.geometry("%sx%s" % ((x1-x0),(y1-y0)))
        return
    
    def mouse_press(event):
        global x, y
        count = time.time()
        x, y = event.x, event.y
    def mouse_release(event):
        x, y = pyautogui.position()
        if x < 50 or y < 25 or x > (pyautogui.size()[0] - 50) or y > (pyautogui.size()[1] - 50):
            fullscreen_func("FS")
    def mouse_doubleclick(event):
        global is_fs, prev_geom
        if is_fs:
            fullscreen_func("MS")
        else:
            fullscreen_func("FS")   
        
    grip_label.bind("<B1-Motion>", mouse_motion)  # Right Bar
    grip_label.bind("<Button-1>", mouse_press)  
    grip_label_2.bind("<B1-Motion>", mouse_motion) #Top Bar
    grip_label_2.bind("<Button-1>", mouse_press) 
    grip_label.bind("<ButtonRelease-1>", mouse_release)
    grip_label.bind("<Double-Button-1>", mouse_doubleclick)
    grip_label_2.bind("<ButtonRelease-1>", mouse_release)
    grip_label_2.bind("<Double-Button-1>", mouse_doubleclick)
    icon_title.bind("<B1-Motion>", mouse_motion)
    icon_title.bind("<Button-1>", mouse_press) 
    resize_button.bind("<B1-Motion>", OnMotion)
    
    def ini_tab_log(event): #Depreciated, but keeping for ref
        global prev_tab
        prev_tab = file_list[starter_f].tab
        root.unbind("<Visibility>")
    
    def tabs_log(event):
        global prev_tab
        menu_tabs = [
            "Create - Ctrl+N",
            "Open - Ctrl+O", 
            "Save - Ctrl+S", 
            "Save+Run (.py/.cpp) - Ctrl+R", 
            "Close - Esc", 
            "Running Code",  
            "Confirm"
            ]
        if notebook.tab(notebook.select(), "text") in menu_tabs:
            return
        elif notebook.tab(notebook.select(), "text") == None:
            return
        else:
            prev_tab = get_info_from_tab().tab
    #Menu Tabs
    def fTabSwitched(event):
        global prev_tab
        l_tabText = notebook.tab(notebook.select(), "text")
        if (l_tabText == "Create - Ctrl+N"):
            notebook.select(prev_tab)
            create_file()
        elif (l_tabText == "Open - Ctrl+O"):
            notebook.select(prev_tab)
            open_file()
        elif (l_tabText == "Save - Ctrl+S"):
            notebook.select(prev_tab)
            on_saving()
        elif (l_tabText == "Save+Run (.py/.cpp) - Ctrl+R"):
            notebook.select(prev_tab)
            threading.Thread(target=on_run, args=(), daemon=True).start()
        elif (l_tabText == "Close - Esc"):
            on_quit() 

    menu_0 = ttk.Frame(notebook)
    notebook.add(menu_0, text = "Create - Ctrl+N")
    menu_1 = ttk.Frame(notebook)
    notebook.add(menu_1, text = "Open - Ctrl+O")
    menu_2 = ttk.Frame(notebook)
    notebook.add(menu_2, text = "Save - Ctrl+S")
    menu_3 = ttk.Frame(notebook)
    notebook.add(menu_3, text = "Save+Run (.py/.cpp) - Ctrl+R")
    menu_4 = ttk.Frame(notebook)
    notebook.add(menu_4, text = "Close - Esc")
    tab_1 = ttk.Frame(notebook)
    notebook.add(tab_1, text = (file_list[starter_f].file_name))
    file_list[starter_f].add_tab(tab_1)
    root.bind("<Button-1>", tabs_log)
    root.bind("<ButtonRelease-1>",fTabSwitched)
    notebook.tab(file_list[starter_f].tab, padding = [5,5])
    notebook.select(file_list[starter_f].tab)
    
    

    notebook.bind("<B1-Motion>", mouse_motion)
    notebook.bind("<Button-1>", mouse_press)
    notebook.bind("<ButtonRelease-1>", mouse_release)   
    notebook.bind("<Double-Button-1>", mouse_doubleclick)
    #Creating default txt file 'simp_pad.txt'
    try:
        with io.open(starter_f, "r", encoding = "utf-8", errors="ignore") as simp_pad:
            simp_pad_content = simp_pad.read()
    except:
        with io.open(starter_f, "w", encoding = "utf-8", errors="ignore") as simp_pad:
            simp_pad_content = f"""
Welcome to SimpIDE
This tab is your 'Simp Pad'!
Consider it a persistent, single-page, notebook.
The file 'simp_pad.txt' can be found in ({starter_f}).
To create a new file (of nearly any type), press Cntrl-N, 
or Cntrl-O to open a new one!
"""

            simp_pad_content += r"""
In order to test out Simp's capabilities, why don't you say hello to the world!

In python:

print('Hello, World!')

In C++:

#include <iostream>
using namespace std;
int main(){
cout<<"Hello, World!";
}

Make sure you use the proper extension when creating your file!
(helloworld.cpp for C++, helloworld.py for Python)
Enjoy!
"""
    code_editor = CodeEditor(
        file_list[starter_f].tab,
        width=99,
        height=30,
        language="TXT",
        background="black",
        highlighter="dracula",
        font="Consolas",
        autofocus=True,
        blockcursor=False,
        insertofftime=0,
        padx=10,
        pady=10,
        startline = 0
    )
    
    # number_line = CodeEditor(
    #     # file_list[starter_f].tab,
    #     code_editor,
    #     width=10,
    #     height=30,
    #     language="TXT",
    #     background="black",
    #     highlighter="dracula",
    #     font="Consolas",
    #     autofocus=True,
    #     blockcursor=False,
    #     insertofftime=0,
    #     padx=10,
    #     pady=10,
    # )
    #Adding simp_pad for first time use
    file_list[starter_f].add_editor(code_editor)
    file_list[starter_f].editor.content = simp_pad_content
    code_editor.pack(fill="both", expand=True)
    #Tab creation for Sys.Arg (Open With attempt)
    try:
        sys_file = file_list[f'{sys.argv[1]}']    
        tab = ttk.Frame(notebook)
        sys_file.add_tab(tab)
        notebook.insert("end", tab, text = sys_file.file_name)
        sys_code_editor = CodeEditor(
                        tab,
                        width=99,
                        height=30,
                        language=sys_file.get_lang(),
                        background="black",
                        highlighter="dracula",
                        font="Consolas",
                        autofocus=True,
                        blockcursor=False,
                        insertofftime=0,
                        padx=10,
                        pady=10,
                        startline = 0
                        )
        with io.open(sys_file.file_path, "r", encoding = "utf-8", errors="ignore") as sys_file_r:
            sys_code_editor.content = sys_file_r.read()
        sys_file.add_editor(sys_code_editor)
        sys_code_editor.pack(fill="both", expand=True)
        notebook.select(tab) 
    except:
        pass
    
    #Logic for auto-indent
    def auto_indent():
        global stop_indent
        if len(get_info_from_tab().editor.content.strip().splitlines()) == 0 or get_info_from_tab().get_lang() != "Python":
            return
        code_list = [x for x in get_info_from_tab().editor.content.splitlines() if x != ""]
        if code_list[-1][-1] == ":" and get_info_from_tab().indent_stop == False:
            get_info_from_tab().indent_stop = False
            indents = get_info_from_tab().editor.content.strip().splitlines()[-1].count("\t")
            indents += 1
            tabs = "\t" * (indents)
            keyboard.write(tabs)
        elif get_info_from_tab().indent_stop == False:
            indents = get_info_from_tab().editor.content.strip().splitlines()[-1].count("\t")
            tabs = "\t" * (indents)
            keyboard.write(tabs)
    root.bind("<Return>", lambda event:auto_indent())
    def indent_stop():
        if get_info_from_tab().get_lang() != "Python":
            return
        get_info_from_tab().indent_stop = True
    def indent_start():
        if get_info_from_tab().get_lang() != "Python":
            return
        get_info_from_tab().indent_stop = False        
    root.bind("<BackSpace>", lambda event:indent_stop())
    root.bind(":", lambda event:indent_start())
    def force_newline():
        root.unbind("<Shift-Return>")
        keyboard.write("#")
        sleep(.01)
        root.bind("<Shift-Return>", lambda event:threading.Thread(target=force_newline, args=(), daemon=True).start())
    root.bind("<Shift-Return>", lambda event:threading.Thread(target=force_newline, args=(), daemon=True).start())
    code_editor.pack(fill="both", expand=True)
    
    #Defining Keyboard Shortcuts                    
    root.bind("<Control-r>", lambda event:threading.Thread(target=on_run, args=(), daemon=True).start())
    root.bind("<Control-s>", lambda event:on_saving())
    root.bind("<Control-o>", lambda event:open_file())
    root.bind("<Control-n>", lambda event:create_file())
    root.bind("<Escape>", lambda event:on_quit())
    root.bind('<Map>', check_map) # added bindings to pass windows status to function
    root.bind('<Unmap>', check_map)
    notebook.pack(fill="both", expand=True)
    root.minsize(root.winfo_width(), root.winfo_height())
    root.protocol("WM_DELETE_WINDOW", on_quit)
    root.mainloop()

    return
if __name__ == "__main__":
    main()

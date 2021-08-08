#DEPRECIATED, AT ONE POINT SIMP_IDE WAS TITLED MAIN.PY ~ Do Not Use

from tkcode import CodeEditor
from file_open import fileopen
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import *
from tkinter import messagebox
import threading
import io
import os


def main():
    file_open = fileopen()
    if file_open == 0:
        return
    file_path, file_state = file_open
    file_name = file_path.split("/")[-1]
    file_ext = file_name.strip().split(".")[1].lower()
    file_name = file_name.strip().split(".")[0] + "."
    file_lang = None
    root = tk.Tk()
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')  
    root.iconbitmap(icon_path)
    root.title("SimpIDE")
    root.option_add("*tearOff", 0)

    if file_ext == "ada":
        file_lang = "ADA"
    elif file_ext == "bash":
        file_lang = "Bash"
    elif file_ext == "bat":
        file_lang = "Batch"
    elif file_ext in ["brainfuck", "bf"]:
        file_lang = "Brainfuck"
    elif file_ext == "c":
        file_lang = "C"
    elif file_ext == "cmake":
        file_lang = "Cmake"
    elif file_ext in ["coffeescript", "coffee"]:
        file_lang = "CoffeeScript"
    elif file_ext == "css":
        file_lang = "CSS"
    elif file_ext in ["c sharp", "cs", "c#"]:
        file_lang = "C#"
    elif file_ext in ["c plus plus", "cpp", "c++"]:
        file_lang = "C++"
    elif file_ext == "dart":
        file_lang = "Dart"
    elif file_ext == "delphi":
        file_lang = "Delphi"
    elif file_ext in ["dockerfile", "docker"]:
        file_lang = "Dockerfile"
    elif file_ext == "fortran":
        file_lang = "Fortran"
    elif file_ext in ["go", "gofile_ext"]:
        file_lang = "Go"
    elif file_ext == "groovy":
        file_lang = "Groovy"
    elif file_ext == "haskell":
        file_lang = "Haskell"
    elif file_ext == "html":
        file_lang = "HTML"
    elif file_ext == "java":
        file_lang = "Java"
    elif file_ext in ["javascript", "js"]:
        file_lang = "JavaScript"
    elif file_ext == "json":
        file_lang = "JSON"
    elif file_ext == "txt":
        file_lang = "Txt"
    elif file_ext == "kotlin":
        file_lang = "Kotlin"
    elif file_ext == "lisp":
        file_lang = "Lisp"
    elif file_ext == "lua":
        file_lang == "Lua"
    elif file_ext == "makefile":
        file_lang = "Makefile"
    elif file_ext == "matlab":
        file_lang = "MatLab"
    elif file_ext == "nasm":
        file_lang = "Nasm"
    elif file_ext in ["objective-c", "objectivec"]:
        file_lang = "Objective-C"
    elif file_ext == "perl":
        file_lang = "Perl"
    elif file_ext == "php":
        file_lang = "PHP"
    elif file_ext == "powershell":
        file_lang = "PowerShell"
    elif file_ext in ["python", "py"]:
        file_lang = "Python"
    elif file_ext in ["r", "erfile_ext"]:
        file_lang = "R"
    elif file_ext == "ruby":
        file_lang = "Ruby"
    elif file_ext == "swift":
        file_lang = "Swift"
    elif file_ext == "sql":
        file_lang = "SQL"
    elif file_ext == "tcl":
        file_lang = "Tcl"
    elif file_ext in ["typescript", "ts"]:
        file_lang = "TypeScript"
    elif file_ext == "vim":
        file_lang = "Vim"
    elif file_ext == "yaml":
        file_lang = "YAML"
    notebook = ttk.Notebook(root)
    tab_1 = ttk.Frame(notebook)
    notebook.add(tab_1, text = file_name + file_ext)
    notebook.pack(fill="both", expand=True)

    code_editor = CodeEditor(
        tab_1,
        width=99,
        height=30,
        language=file_lang,
        background="black",
        highlighter="dracula",
        font="Consolas",
        autofocus=True,
        blockcursor=True,
        insertofftime=0,
        padx=10,
        pady=10,
        
    )
    
    code_editor.pack(fill="both", expand=True)
    if file_state == "open":
        with io.open(file_path, "r", encoding="utf-8") as file_to_open:
            code_editor.content = file_to_open.read()
    def on_closing():
        if messagebox.askyesno("Saving...", "Would you like to save your work?"):
            with io.open(file_path, "w", encoding="utf-8") as file_to_save:
                file_to_save.write(code_editor.content)
        root.quit()
        root.destroy()
    def on_saving():
        with io.open(file_path, "w", encoding="utf-8") as file_to_save:
            file_to_save.write(code_editor.content)
    def get_parent_folder(path):
        split_path = path.split("/")
        parent = "\\".join(split_path[:-1])
        return parent
    def on_run():
        try:
            if file_ext == "py":
                os.system(f'cd "{get_parent_folder(file_path)}" && python "{file_name + file_ext}"')
                messagebox.showwarning("Executing", "Running code -> See Console")
            elif file_ext == "cpp":
                os.system(f'cd "{get_parent_folder(file_path)}"" && g++ "{file_name + file_ext}" -o output && .\\output.exe')          
        except:
            print("-------------Code Finished-------------")
                           
    #Defining the menu
    menubar = Menu(root, background='#A9A9A9', foreground='black', activebackground='white', activeforeground='black')  
    file = Menu(menubar, tearoff=1, background='#A9A9A9', foreground='black')  
    file.add_command(label="Create/Open", command = lambda: main())  
    file.add_command(label="Save", command = lambda: on_saving())
    file.add_command(label="Run (.py/.cpp)", command = lambda: threading.Thread(target=on_run, args=(), daemon=True).start())
    file.add_command(label="Exit", command= lambda: on_closing())  
    menubar.add_cascade(label="File", menu=file)  

    root.config(menu=menubar)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    return
if __name__ == "__main__":
    main()

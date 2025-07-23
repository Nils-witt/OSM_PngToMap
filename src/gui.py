import os
from tkinter import *

DATA_DIR = "/Users/nilswitt/git/pngToMap/data/"

selected_project = None

def open_project_view(parent):
    root = Toplevel(master=parent)
    lb = Listbox(root)

    projects = os.listdir(DATA_DIR)
    for p in projects:
        if os.path.isdir(os.path.join(DATA_DIR, p)):
            lb.insert(END, p)
    lb.grid()

    def clicked():
        values = [lb.get(idx) for idx in lb.curselection()]
        global selected_project
        if len(values) == 0:
            print("No project selected")
            return
        selected_project.set(values[0])
        root.destroy()

    btn = Button(root, text="Auswählen", command=clicked)
    btn.grid(column=1, row=0)

    root.transient(parent)
    root.grab_set()
    parent.wait_window(root)


def main():

    root = Tk()
    root.title("PDF to OSM")

    root.geometry('1000x1100')
    global selected_project
    selected_project = StringVar()

    Label(root, textvariable=selected_project).grid(column=1, row=0)

    def open_project_view_btn():
        open_project_view(root)

    btn = Button(root, text="Auswählen", command=open_project_view_btn)
    btn.grid(column=0, row=0)

    root.mainloop()


if __name__ == "__main__":
    main()

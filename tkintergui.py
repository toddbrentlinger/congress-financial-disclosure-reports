import tkinter as tk

def createWindow():
    return tk.Tk()

def main():
    window = createWindow()

    greeting = tk.Label(text="Hello, Tkinter")
    greeting.pack()

    window.mainloop()

if __name__ == '__main__':
    main()
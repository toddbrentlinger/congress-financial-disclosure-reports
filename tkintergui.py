import tkinter as tk

def createWindow():
    return tk.Tk()

def createCustomWindow():
    window = createWindow()

    # Top Bar

    # Left Side Bar

    # Main

    # Right Side Bar

    # Footer

    window.mainloop()

def main():
    window = createWindow()

    # TODO: Keep all widgets in list and pack them all in single line: widget.pack() for widget in widgetList

    greeting = tk.Label(text="U.S. Congress Financial Disclosure Reports")
    greeting.pack()

    button = tk.Button(
        text='Check New Report Listings',
        width=25,
        height=5,
        bg='blue',
        fg='white',
    )
    button.pack()

    entry = tk.Entry(width=50)
    entry.pack()
    
    window.mainloop()

if __name__ == '__main__':
    main()
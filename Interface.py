import tkinter as tk
from PIL import Image, ImageTk

def start_puzzle_interface(input_callback):
    global root, canvas, imgtk
    root = tk.Tk()
    root.title("Puzzle Webcam App")

    # Create a canvas to display the webcam feed
    canvas = tk.Canvas(root, width=640, height=480)
    canvas.pack()

    # Button to start the puzzle
    start_button = tk.Button(root, text="Start Puzzle", command=lambda: print("Puzzle started"))
    start_button.pack()

    # Button to reset the puzzle
    reset_button = tk.Button(root, text="Reset Puzzle", command=lambda: print("Puzzle reset"))
    reset_button.pack()

    # Input fields for indices
    index1_label = tk.Label(root, text="Index 1:")
    index1_label.pack()
    index1_entry = tk.Entry(root)
    index1_entry.pack()

    index2_label = tk.Label(root, text="Index 2:")
    index2_label.pack()
    index2_entry = tk.Entry(root)
    index2_entry.pack()

    # Swap button
    swap_button = tk.Button(root, text="Swap!", command=lambda: input_callback(index1_entry.get(), index2_entry.get()))
    swap_button.pack()

    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the Tkinter main loop
    root.mainloop()

def update_image(frame):
    global canvas, imgtk
    # Convert frame to ImageTk format
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)

    # Update the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
    canvas.imgtk = imgtk  # Keep a reference to avoid garbage collection

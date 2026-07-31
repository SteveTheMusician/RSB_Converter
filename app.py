from customtkinter import *
from tkinter import filedialog

app = CTk()
app.title("RS Converter")
app.geometry("640x360")
app.resizable(False, False)

app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=0)

mainFrame = CTkFrame(master=app, corner_radius=6, fg_color="transparent")
mainFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
mainFrame.grid_columnconfigure(0, weight=1)
mainFrame.grid_columnconfigure(1, weight=1)
mainFrame.grid_rowconfigure(0, weight=1)

# Content Frame Left
contentFrameLeft = CTkFrame(master=mainFrame, fg_color="transparent")
contentFrameLeft.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

fileDropFrame = CTkFrame(master=contentFrameLeft, border_color="#343434",fg_color="transparent",
                         border_width=1, corner_radius=6, height=140)
fileDropFrame.pack(fill="x", padx=10, pady=10)
fileDropFrame.pack_propagate(False)

fileDropLabel = CTkLabel(fileDropFrame, text="📁\nDatei auswählen",
                         justify="center", text_color="#888888", font=("Arial", 16))
fileDropLabel.pack(expand=True)

# select file function
def select_file(event=None):
    filepath = filedialog.askopenfilename(
        filetypes=[("Alle Dateien", "*.*")]
    )
    if filepath:
        fileDropLabel.configure(text=f"\n{filepath}", text_color="#17bdaf")

fileDropFrame.bind("<Button-1>", select_file)
fileDropLabel.bind("<Button-1>", select_file)
fileDropFrame.configure(cursor="hand2")
fileDropLabel.configure(cursor="hand2")

# Content Frame Right
contentFrameRight = CTkFrame(master=mainFrame, fg_color="transparent")
contentFrameRight.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

# Footer Frame
footerFrame = CTkFrame(master=app, width=640, height=80, corner_radius=0)
footerFrame.grid(row=1, column=0, sticky="we", padx=0, pady=(5, 0))

progressBar = CTkProgressBar(footerFrame, orientation="horizontal",
                             width=240, height=20, border_width=1, border_color="#343434",
                             fg_color="#222222", progress_color="#17bdaf")
progressBar.place(relx=0, rely=0.5, anchor="w", x=20)

btnStart = CTkButton(master=footerFrame, text="Start", corner_radius=6,
                     fg_color="transparent", hover_color="#17bdaf",
                     border_color="#17bdaf", border_width=2, cursor="hand2")
btnStart.place(relx=1, rely=0.5, anchor="e", x=-20)

app.mainloop()
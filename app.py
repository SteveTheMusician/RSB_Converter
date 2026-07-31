from customtkinter import *

app = CTk()
app.title("RSB Converter")
app.geometry("640x360")
app.resizable(False, False)

# Beide Spalten/Zeilen konfigurieren
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)  # MainFrame nimmt verfügbaren Platz
app.grid_rowconfigure(1, weight=0)  # Footer bleibt fix

mainFrame = CTkFrame(master=app, corner_radius=6, fg_color="#c87373")
mainFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

# Footer Frame unten kleben
footerFrame = CTkFrame(master=app, width=640, height=80, corner_radius=0)
footerFrame.grid(row=1, column=0, sticky="we", padx=0, pady=(5, 0))

btnStart = CTkButton(master=footerFrame, text="Start", corner_radius=6, 
                       fg_color="transparent", hover_color="#17bdaf", 
                       border_color="#17bdaf", border_width=2)
btnStart.place(relx=1, rely=0.5, anchor="e", x=-20)

app.mainloop()
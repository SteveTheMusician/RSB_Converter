from customtkinter import *

app = CTk()
app.title("RSB Converter")
app.geometry("640x360")
app.resizable(False, False)

# set_appearance_mode('dark')

# Footer Frame
footerFrame = CTkFrame(master=app, width=640, height=100, corner_radius=0)
footerFrame.pack(expand=True)
footerFrame.place(relx=0.5, rely=0.86, anchor="center")

btnExtract = CTkButton(master=footerFrame, text="Extract",corner_radius=6, fg_color="transparent",hover_color="#17bdaf",border_color="#17bdaf", border_width=2)
btnExtract.place(relx=0.55, rely=0.5, anchor="center")

btnCompile = CTkButton(master=footerFrame, text="Compile",corner_radius=6, fg_color="transparent",hover_color="#b717bd",border_color="#b717bd", border_width=2)
btnCompile.place(relx=0.8, rely=0.5, anchor="center")

app.mainloop()
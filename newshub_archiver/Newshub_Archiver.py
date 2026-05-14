import customtkinter
import pdfkit
import openpyxl
import os 
from pathlib import Path

root = customtkinter.CTk()
root.geometry("550x330")
root.title("Newshub Archiver")

frame = customtkinter.CTkFrame(master = root)
frame.pack(pady=20, padx = 20, fill="both", expand=True)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

progress_bar = customtkinter.CTkProgressBar(master = frame, width = 450, progress_color='red')
progress_bar.place(x=25, y=265)
progress_bar.set(0)

#relative paths
script_dir = os.path.dirname(os.path.abspath(__file__))

wkhtmltopdf_path = os.path.join(script_dir, 'resources/wkhtmltopdf.exe')
database_path = os.path.join(script_dir, 'resources/newshub-database_ext.xlsx')

#direct to the wkhtmltopdf file
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path) 

def newWindow(counter):
    newWindow = customtkinter.CTkToplevel(frame)
    newWindow.title = "Newshub Archiver Success"
    newWindow.geometry("200x100")

    newWindowLabel = customtkinter.CTkLabel(master = newWindow, text=f"Archive success!\n\n{counter} articles extracted")
    newWindowLabel.pack(pady = 12, padx=12)
    # Make the new window float on top of all
    newWindow.lift()
    newWindow.attributes('-topmost', True)

# Function matching the provided author name to the article links & urls
def authorMatch(databasePath, authorName):
    wb = openpyxl.load_workbook(databasePath)
    ws = wb.active

    #outputPath = os.path.join(script_dir, Path(f"{authorName} archive"))
    #outputPath.mkdir(parents=True,exist_ok=True)

    counter = 0
    totalCounter = 0

    for row in ws.iter_rows(min_row=1, values_only=True):  # Data starts from second row (excluding header)
        url, title, author = row
        totalCounter += 1
        
        if author is not None:
            if ',' in author:
                authors = [name.strip() for name in author.split(",")]
            else:
                authors = [author.strip()]

            if any(authorName in name for name in authors):
                #pdfkit.from_url(url, f'{title}.pdf', options={'disable-javascript': None})
                #pdfkit.from_url(url, f'{outputPath}/{title}.pdf', options={'disable-javascript': None})
                pdfkit.from_url(url, f'{title}.pdf', options={'disable-javascript': None}, configuration=config)

                counter += 1
        progress = (totalCounter / 58601)        
        progress_bar.set(progress)
        root.update_idletasks()


    print(f"Total articles: {counter} out of {totalCounter}")
    newWindow(counter)
    button.configure(text="Export Archive",fg_color="#3a7ebf")

def convertAll():
    database = database_path
    author = nameInput.get()
    button.configure(text="Export In Progress...",fg_color="#325882")
    progress_bar.set(0)
    authorMatch(database, author)


#GUI information
intructionLabel1 = customtkinter.CTkLabel(master = frame, text="1. Type in your name exactly as it appears on the Newshub.co.nz website")
intructionLabel1.pack(pady = 12, padx = 10)
intructionLabel2 = customtkinter.CTkLabel(master = frame, text="2. Click 'Export Archive'")
intructionLabel2.pack(pady = 12, padx = 10)
intructionLabel3 = customtkinter.CTkLabel(master = frame, text="3. Leave program running in the background until you see a success pop-up")
intructionLabel3.pack(pady = 12, padx = 10)

nameInput = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text="Author Name")
nameInput.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master = frame, text="Export Archive",command=convertAll,fg_color="#3a7ebf")
button.pack(pady=12, padx=10)

#Run program
root.mainloop()
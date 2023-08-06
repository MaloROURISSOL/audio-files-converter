import os
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pydub import AudioSegment
from ttkthemes import ThemedStyle

class App:
    def __init__(self, root):
        self.root = root
        self.files_to_convert = []

        # Widgets
        self.select_button = ttk.Button(self.root, text="Sélectionner des fichiers audio", command=self.select_files)
        self.select_button.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        self.listbox = Listbox(self.root)
        self.listbox.grid(row=1, column=0, sticky='nsew', padx=10)

        self.delete_button = ttk.Button(self.root, text="Retirer le fichier sélectionné", command=self.delete_file)
        self.delete_button.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

        self.label = Label(self.root, text="Convertir les fichiers en :")
        self.label.grid(row=3, column=0, sticky='w', padx=10)

        self.format_combobox = ttk.Combobox(self.root, values=["mp3", "wav", "aiff", "flac", "ogg"], state="readonly")
        self.format_combobox.grid(row=3, column=0, sticky='e', padx=10)
        self.format_combobox.set("mp3")  # Set default value

        self.convert_button = ttk.Button(self.root, text="Convertir", command=self.start_conversion)
        self.convert_button.grid(row=4, column=0, sticky='ew', padx=10, pady=10)

        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress.grid(row=5, column=0, sticky='ew', padx=10, pady=10)

        # Configure the grid to expand properly
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def select_files(self):
        files = filedialog.askopenfilenames(initialdir = "/", title = "Sélectionnez des fichiers audio", filetypes = (("audio files", "*.*"), ("all files", "*.*")))
        self.files_to_convert = list(files)  # Convert the tuple to a list

        self.listbox.delete(0, END)
        for file in self.files_to_convert:
            self.listbox.insert(END, os.path.basename(file))

    def delete_file(self):
        selected = self.listbox.curselection()
        if selected:
            del self.files_to_convert[selected[0]]
            self.listbox.delete(selected)

    def start_conversion(self):
        self.convert_button.config(state=DISABLED)

        self.progress['value'] = 0
        self.progress['maximum'] = len(self.files_to_convert)

        threading.Thread(target=self.convert_files, daemon=True).start()

    def convert_files(self):
        if not self.files_to_convert:
            messagebox.showerror("Erreur", "Veuillez sélectionner des fichiers à convertir")
            return

        # Get the selected output format
        output_format = self.format_combobox.get()

        output_dir = filedialog.askdirectory()

        for file in self.files_to_convert:
            self.convert_to_audio(file, output_dir, output_format)

            self.progress['value'] += 1
            self.root.update_idletasks()

        self.convert_button.config(state=NORMAL)

    def convert_to_audio(self, file_path, output_dir, output_format):
        audio = AudioSegment.from_file(file_path)

        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + "." + output_format)

        audio.export(output_file, format=output_format)

root = Tk()
style = ThemedStyle(root)
style.set_theme("arc")
root.geometry("350x400")  # Set the window size
root.minsize(350, 400)
root.title("Convertisseur de fichier audio")
app = App(root)
root.mainloop()

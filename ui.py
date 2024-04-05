import subprocess
import tkinter as tk
from someVariables import *
from cyclicUL import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from datetime import datetime


class UI:
    def __init__(self, master):
        self.master = master
        master.title("Project Manager System")
        master.geometry("700x300")
        master.resizable(width=False, height=False)

        self.teamList = CyclicTeamList()

        self.statusLabel = tk.Label(master, text="Running", bg="Green", anchor="center", width=80)
        self.statusLabel.place(x=0, y=0)

        self.creationButton = tk.Button(master, text="Sukurti projektą", command=self.createProject)
        self.creationButton.place(x=20, y=50)

        self.employeeEntry = tk.Entry(master, width=30)
        self.employeeEntry.insert(0, "Darbuotojo vardas, pareigos")
        self.employeeEntry.bind("<FocusIn>", self.on_entry_focus_in)
        self.employeeEntry.bind("<FocusOut>", self.on_entry_focus_out)
        self.employeeEntry.place(x=250, y=50)

        self.entryButton = tk.Button(master, text="Pridėti narį", command=self.addEmployee)
        self.entryButton.place(x=530, y=50)

        self.comboLabel = tk.Label(master, text="Užduotys pridedamos šiam nariui:")
        self.comboLabel.place(x=20, y=100)

        self.employeeCombo = Combobox(master, width=20)
        self.employeeCombo.place(x=250, y=100)

        self.titleLabel = tk.Label(master, text="Užduoties pavadinimas ir prioritetas:")
        self.titleLabel.place(x=20, y=150)

        self.titleEntry = tk.Entry(master, width=30)
        self.titleEntry.place(x=250, y=150)

        self.combobox = Combobox(master, width=15)
        self.combobox['values'] = ("Vidutinis", "Aukštas")
        self.combobox.current(0)
        self.combobox.place(x=530, y=150)

        self.descriptionLabel = tk.Label(master, text="Užduoties aprašymas:")
        self.descriptionLabel.place(x=20, y=200)

        self.descriptionEntry = tk.Entry(master, width=30)
        self.descriptionEntry.place(x=250, y=200)

        self.taskButton = tk.Button(master, text="Pridėti užduotį", command=self.addJob)
        self.taskButton.place(x=530, y=200)

        self.seeTaskButton = tk.Button(master, text="Peržiūrėti pasirinkto nario užduotis", command=self.displayFile)
        self.seeTaskButton.place(x=20, y=250)

        self.finishButton = tk.Button(master, text="Baigti Projektą", command=self.endProject)
        self.finishButton.place(x=530, y=250)

    def createProject(self):
        file_path = os.path.join(desktop_path, "Projektas.txt")
        if second_file_path:
            try:
                with open(second_file_path, 'a') as secondFile:
                    secondFile.write(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} sukurtas projektas\n")
            except Exception as e:
                self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

        if file_path:
            try:
                with open(file_path, 'a') as file:
                    file.write("Projekto pavadinimas: ADS antrasis namų darbas. \n")
                    file.write(f"Projekto pradžia: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    messagebox.showinfo("Atliktas veiksmas", "Sėkmingai sukurtas projektas")
            except Exception as e:
                self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

    def endProject(self):
        file_path = os.path.join(desktop_path, "Projektas.txt")
        if second_file_path:
            try:
                with open(second_file_path, 'a') as secondFile:
                    secondFile.write(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} Projektas baigtas\n")
            except Exception as e:
                self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

        try:
            with open(file_path, 'a') as file:
                file.write(f"Projekto pabaiga: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("Statusas: Sėkmingai užbaigtas laiku")
                subprocess.run(["open", file_path])
        except Exception as e:
            self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

    def displayFile(self):
        member_text = self.employeeCombo.get()
        name, profession = member_text.split(', ')
        file_path = os.path.join(desktop_path, f"{profession}.txt")

        if second_file_path:
            try:
                with open(second_file_path, 'a') as secondFile:
                    secondFile.write(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} Žiūrimos nario vardu {name}"
                                     f" užduotys\n")
            except Exception as e:
                self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

        if file_path:
            subprocess.run(["open", file_path])

    def addJob(self):
        member_text = self.employeeCombo.get()
        task_title_text = self.titleEntry.get()
        combo_value = self.combobox.get()

        if second_file_path:
            try:
                with open(second_file_path, 'a') as secondFile:
                    secondFile.write(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} {member_text} gavo užduotį "
                                     f"{task_title_text}\n")
            except Exception as e:
                self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

        if member_text or task_title_text:
            name, profession = member_text.split(', ')
            found_member = self.teamList.findMember(name)
            file_path = os.path.join(desktop_path, f"{profession}.txt")

            if found_member:
                found_member.addTask(task_title_text, self.descriptionEntry.get(), combo_value)
                messagebox.showinfo("Atliktas veiksmas", f"{name} gavo užduotis į savo deką")
            else:
                messagebox.showerror("Error", "Nėra tokio nario")

            try:
                with open(file_path, 'a') as file:
                    file.write(f"\nUžduotis: {task_title_text} | Statusas: Atliekama\n")
                    file.write(f"Prioritetas: {combo_value}\n")
            except Exception as e:
                self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

            self.titleEntry.delete(0, "end")
            self.descriptionEntry.delete(0, "end")
        else:
            messagebox.showerror("Error", "Empty input")

    def addEmployee(self):
        entry_text = self.employeeEntry.get()

        if second_file_path:
            try:
                with open(second_file_path, 'a') as secondFile:
                    secondFile.write(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} Į komandą prisidėjo "
                                     f"{entry_text}\n")
            except Exception as e:
                self.statusLabel.config(text=f"Error: {str(e)}", bg="Red")

        if entry_text:
            name, profession = entry_text.split(', ')

            self.teamList.addMember(name, profession)
            self.employeeCombo["values"] = (*self.employeeCombo["values"], entry_text)

            messagebox.showinfo("Atliktas veiksmas", f"Pridėtas komandos narys vardu: {name}")
            self.employeeEntry.delete(0, "end")

        else:
            messagebox.showerror("Error", "Empty input")
            self.employeeEntry.config(bg="Red")

    def on_entry_focus_in(self, event):
        if self.employeeEntry.get() == "Darbuotojo vardas, pareigos":
            self.employeeEntry.delete(0, tk.END)
            self.employeeEntry.configure(show="")
            self.employeeEntry.configure(fg="White")

    def on_entry_focus_out(self, event):
        if self.employeeEntry.get() == "":
            self.employeeEntry.insert(0, "Darbuotojo vardas, pareigos")
            self.employeeEntry.configure(show="")
            self.employeeEntry.configure(fg="White")

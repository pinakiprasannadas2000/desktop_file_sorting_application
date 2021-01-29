from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import shutil

# all files present in the selected folder
all_files = []

# total number of files in the selected folder
count = 0


# ------------------------------------------all functions------------------------------------------
def rename_existing_folder(selected_folder):
    all_folders = os.listdir(selected_folder)

    for folder in all_folders:
        if os.path.isdir(os.path.join(selected_folder, folder)):
            os.rename(os.path.join(selected_folder, folder), os.path.join(selected_folder, folder.lower()))


def move_the_file(extension_of_the_file, file_name, selected_folder):
    find = False
    for folder_name in folders:
        if "." + extension_of_the_file in folders[folder_name]:
            if folder_name not in os.listdir(selected_folder):
                os.mkdir(os.path.join(selected_folder, folder_name))
            shutil.move(os.path.join(selected_folder, file_name), os.path.join(selected_folder, folder_name))
            find = True
            break

    if not find:
        others_folder_name = "others"
        if others_folder_name not in os.listdir(selected_folder):
            os.mkdir(os.path.join(selected_folder, others_folder_name))
        shutil.move(os.path.join(selected_folder, file_name), os.path.join(selected_folder, others_folder_name))


def clear():
    start_button.config(state=DISABLED)

    entry_select.config(state=NORMAL)
    entry_select.delete(0, END)
    entry_select.config(state=DISABLED)

    lbl_total.config(text="Total: ")
    lbl_moved.config(text="Moved: ")
    lbl_left.config(text="Left: ")

    total_files_label.config(text="Total Files: ")
    image_label.config(text="Total Images: \n")
    audio_label.config(text="Total Audios: \n")
    video_label.config(text="Total Videos: \n")
    document_label.config(text="Total Documents: \n")
    other_label.config(text="Others: \n")


def start_function():
    selected_folder = entry_select.get()

    rename_existing_folder(selected_folder)

    if selected_folder != "":
        clear_button.config(state=DISABLED)
        moved_file = 0
        for file in all_files:
            if os.path.isfile(os.path.join(selected_folder, file)):
                move_the_file(file.split(".")[-1], file, selected_folder)
                moved_file += 1
                lbl_moved.config(text=f"Moved: {moved_file}")
                lbl_left.config(text=f"Left: {count - moved_file}")

                lbl_moved.update()
                lbl_left.update()

        messagebox.showinfo(title="Move Information", message=f"{moved_file}/{count} files have moved successfully.")
        start_button.config(state=DISABLED)
        clear_button.config(state=NORMAL)
    else:
        messagebox.showerror(title="Error", message="Please select a directory.")


def total_count(selected_folder):
    global all_files, count

    images = 0
    audios = 0
    videos = 0
    documents = 0

    for file in all_files:
        if os.path.isfile(os.path.join(selected_folder, file)):
            count += 1
            extension_of_the_file = "." + file.split(".")[-1]
            for folder_name in folders.items():
                if extension_of_the_file.lower() in folder_name[1] and folder_name[0] == "images":
                    images += 1
                if extension_of_the_file.lower() in folder_name[1] and folder_name[0] == "audios":
                    audios += 1
                if extension_of_the_file.lower() in folder_name[1] and folder_name[0] == "videos":
                    videos += 1
                if extension_of_the_file.lower() in folder_name[1] and folder_name[0] == "documents":
                    documents += 1

    others = count - (images + audios + videos + documents)

    total_files_label.config(text=f"Total Files: {count}")
    image_label.config(text=f"Total Images: \n{images}")
    audio_label.config(text=f"Total Audios: \n{audios}")
    video_label.config(text=f"Total Videos: \n{videos}")
    document_label.config(text=f"Total Documents: \n{documents}")
    other_label.config(text=f"Others: \n{others}")

    lbl_total.config(text=f"Total: {count}")


def browse_folder():
    global all_files

    entry_select.config(state=NORMAL)
    entry_select.delete(0, END)
    entry_select.config(state=DISABLED)

    selected_folder = filedialog.askdirectory(initialdir="/", title="Select folder for sorting")
    
    if selected_folder == "":
        messagebox.showerror(title="Error", message="Please select a directory.")

    if selected_folder is not None:
        entry_select.config(state=NORMAL)
        entry_select.insert(0, str(selected_folder))
        entry_select.config(state=DISABLED)

        # it will list out all files present in that folder
        all_files = os.listdir(selected_folder)
        total_count(selected_folder)

        if count > 0:
            start_button.config(state=NORMAL)
        else:
            start_button.config(state=DISABLED)
    else:
        messagebox.showerror(title="Error", message="Please select a directory.")


# ------------------------------------------setting the window------------------------------------------
root = Tk()
root.title("FILES SORTING APPLICATION by PPD")
root.geometry("1500x750+0+0")
root.resizable(False, False)
root.config(bg="white")

# ------------------------------------------title------------------------------------------
lbl_title = Label(root, text=" FILES SORTING APPLICATION by PPD", font=("times new roman", 40, "bold"), bg="orange",
                  fg="white", anchor="w")
lbl_title.pack(side=TOP, fill=X)

# ------------------------------------------folder select------------------------------------------
lbl_select = Label(root, text="Select Folder", font=("times new roman", 20, "bold"), bg="white", fg="black")
lbl_select.place(x=20, y=100)

entry_select = Entry(root, font=("times new roman", 15, "bold"), bg="light yellow", bd=2, relief=SOLID, state=DISABLED)
entry_select.place(x=200, y=100, width=1000, height=40)

lbl_hr_line = Label(root, bg="light grey")
lbl_hr_line.place(x=20, y=160, width=1460, height=2)

# ------------------------------------------supported extensions------------------------------------------
lbl_extension = Label(root, text="Various Extension Supports", font=("times new roman", 35, "bold"), bg="white",
                      fg="black")
lbl_extension.place(x=20, y=180)

# allowed extensions
image_extensions = ["Image Extensions", ".png", ".jpg"]
audio_extensions = ["Audio Extensions", ".amr", ".mp3"]
video_extensions = ["Video Extensions", ".mp4", ".avi", ".mpeg4", ".3gp"]
document_extensions = ["Document Extensions", ".doc", ".xlsx", ".ppt", ".pptx", "xls", ".pdf", ".zip", ".rar", ".csv",
                       ".docx", ".txt"]

# folder dictionary (these are the folders that this application is going to make while sorting)
folders = {
    "videos": video_extensions,
    "audios": audio_extensions,
    "images": image_extensions,
    "documents": document_extensions
}

# extension combobox
image_combobox = ttk.Combobox(root, values=image_extensions, font=("times new roman", 15, "bold"),
                              state="readonly", justify=CENTER)
image_combobox.place(x=45, y=260, width=330)
image_combobox.current(0)

audio_combobox = ttk.Combobox(root, values=audio_extensions, font=("times new roman", 15, "bold"),
                              state="readonly", justify=CENTER)
audio_combobox.place(x=405, y=260, width=330)
audio_combobox.current(0)

video_combobox = ttk.Combobox(root, values=video_extensions, font=("times new roman", 15, "bold"),
                              state="readonly", justify=CENTER)
video_combobox.place(x=765, y=260, width=330)
video_combobox.current(0)

document_combobox = ttk.Combobox(root, values=document_extensions, font=("times new roman", 15, "bold"),
                                 state="readonly", justify=CENTER)
document_combobox.place(x=1125, y=260, width=330)
document_combobox.current(0)

# ------------------------------------------file showing frame------------------------------------------
files_frame = Frame(root, bd=1, relief=SOLID, bg="light blue")
files_frame.place(x=20, y=350, width=1460, height=240)

total_files_label = Label(files_frame, text="Total Files: ", font=("times new roman", 30, "bold"), bg="light blue",
                          fg="black")
total_files_label.place(x=10, y=10)

image_label = Label(files_frame, text="Total Images: \n", font=("times new roman", 20, "bold"), bg="orange",
                    fg="black", justify=CENTER)
image_label.place(x=10, y=130, width=280, height=100)

audio_label = Label(files_frame, text="Total Audios: \n", font=("times new roman", 20, "bold"), bg="orange",
                    fg="black", justify=CENTER)
audio_label.place(x=300, y=130, width=280, height=100)

video_label = Label(files_frame, text="Total Videos: \n", font=("times new roman", 20, "bold"), bg="orange",
                    fg="black", justify=CENTER)
video_label.place(x=590, y=130, width=280, height=100)

document_label = Label(files_frame, text="Total Documents: \n", font=("times new roman", 20, "bold"), bg="orange",
                       fg="black", justify=CENTER)
document_label.place(x=880, y=130, width=280, height=100)

other_label = Label(files_frame, text="Others: \n", font=("times new roman", 20, "bold"), bg="orange",
                    fg="black", justify=CENTER)
other_label.place(x=1170, y=130, width=277, height=100)

lbl_hr_line2 = Label(root, bg="light grey")
lbl_hr_line2.place(x=20, y=630, width=1460, height=2)

# ------------------------------------------buttons------------------------------------------
browse_button = Button(root, text="Browse Folder", font=("times new roman", 15, "bold"), bg="purple", fg="white",
                       activebackground="purple", activeforeground="white", command=browse_folder)
browse_button.place(x=1250, y=100, height=40)

clear_button = Button(root, text="CLEAR", font=("times new roman", 15, "bold"), bg="black", fg="white",
                      activebackground="black", activeforeground="white", command=clear)
clear_button.place(x=1150, y=670, height=40, width=150)

start_button = Button(root, text="START", font=("times new roman", 15, "bold"), bg="green", fg="white",
                      activebackground="green", activeforeground="white", state=DISABLED, command=start_function)
start_button.place(x=1330, y=670, height=40, width=150)

# ------------------------------------------status------------------------------------------
lbl_total = Label(root, text="Total: ", font=("times new roman", 25, "bold"), bg="white",  fg="black")
lbl_total.place(x=20, y=670)

lbl_moved = Label(root, text="Moved: ", font=("times new roman", 25, "bold"), bg="white",  fg="green")
lbl_moved.place(x=300, y=670)

lbl_left = Label(root, text="Left: ", font=("times new roman", 25, "bold"), bg="white",  fg="red")
lbl_left.place(x=580, y=670)

root.mainloop()

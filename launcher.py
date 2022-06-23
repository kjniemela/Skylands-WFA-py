import tkinter as tk
import urllib.request
import subprocess
import os

try:
    f = open("Skylands/version.txt")
    cur_version = f.read()
    f.close()
except FileNotFoundError:
    cur_version = None

## Callbacks
def check():
    global update_window

    version_file_link = "https://raw.githubusercontent.com/kjniemela/Skylands-WFA/master/version.txt"
    f = urllib.request.urlopen(version_file_link)
    new_version = f.read().decode()
    f.close()
    print("Current Version:", cur_version)
    print("Latest Version:", new_version)

    update_window = tk.Toplevel()
    update_window.title("Check for updates")
    update_window.minsize(width=400, height=100)

    if new_version == cur_version:
        message = "You are running the latest version of Skylands WFA (%s)." % (cur_version)
    elif cur_version == None:
        message = "Skylands WFA is currently not installed on your device. Do you want to download and install the latest version (%s)?" % (new_version)
    else:
        message = "You are running Skylands WFA (%s). A new version (%s) is available. Do you want to download and install it?" % (cur_version, new_version)

    msg = tk.Message(update_window, text=message, font=("Helvetica", 11))
    msg.pack(padx=12, pady=12)

    if new_version == cur_version:
        button = tk.Button(update_window, text="Ok", command=update_window.destroy)
        button.pack()
    else:
        button_install = tk.Button(update_window, text="Install", command=install_latest)
        button_install.pack()

        button_cancel = tk.Button(update_window, text="Cancel", command=update_window.destroy)
        button_cancel.pack()

def install_latest():
    global update_window
    global button_install
    global button_cancel
    global cur_version

    button_install.config(state=tk.DISABLED)
    button_cancel.config(state=tk.DISABLED)

    filepaths_link = "https://raw.githubusercontent.com/kjniemela/Skylands-WFA/master/filepaths"
    f = urllib.request.urlopen(filepaths_link)
    filepaths = f.read().decode().split("\n")
    f.close()

    if not os.path.exists("Skylands"):
        os.mkdir("Skylands")

    i = 0
    for filepath in filepaths:
        link = "https://raw.githubusercontent.com/kjniemela/Skylands-WFA/master/" + filepath
        link = link.replace(" ", "%20")
        f = urllib.request.urlopen(link)
        data = f.read()
        f.close()

        dir_name = "/".join(filepath.split("/")[:-1])
        print("Downloading", filepath)
        if not dir_name == "" and not os.path.exists("Skylands/" + dir_name):
            os.makedirs("Skylands/" + dir_name)

        f = open("Skylands/" + filepath, "wb")
        f.write(data)
        f.close()


        update_window.title("Installing... %d" % (round((i / len(filepaths)) * 100)) + "%")
        master.update()
        i += 1

    f = open("Skylands/version.txt")
    cur_version = f.read()
    f.close()

    launch_btn.config(state=tk.NORMAL)
    launch_btn.config(text="Launch Skylands WFA v%s" % (cur_version))

    top = tk.Toplevel(update_window)
    top.title("Install successful")
    top.resizable(False, False)
    
    msg = tk.Message(top, text="Skylands WFA version %s installed successfully!" % (cur_version), font=("Helvetica", 11))
    msg.pack(padx=12, pady=12)

    button = tk.Button(top, text="Ok", command=update_window.destroy)
    button.pack()

def launch():
    print("Launching Skylands WFA version", cur_version)
    python_dir = "/".join(os.__file__.replace("\\", "/").split("/")[:-2])
    subprocess.Popen(python_dir + "/pythonw main.py", cwd="Skylands")
    exit() ## TODO maybe use sys.exit? - or have the launcher continue in the background

def settings():
    print("SETTINGS")

master = tk.Tk()
master.title('Skylands Launcher')

update_window = None
button_install = None
button_cancel = None

greeting = tk.Label(master, text="Skylands WFA - Launcher", font=("Helvetica", 24))
greeting.pack(padx=48, pady=48)

btn_frame = tk.Frame(master)
btn_frame.pack()

check_btn = tk.Button(btn_frame, text="Check for Updates", command=check)
check_btn.pack(side=tk.LEFT)
launch_btn = tk.Button(
    btn_frame,
    text="Launch Skylands WFA" + (" v%s" % (cur_version) if cur_version != None else ""),
    command=launch,
    state=tk.NORMAL if cur_version != None else tk.DISABLED
)
launch_btn.pack(side=tk.LEFT)
settings_btn = tk.Button(btn_frame, text="Settings", command=settings)
settings_btn.pack(side=tk.LEFT)

master.mainloop()
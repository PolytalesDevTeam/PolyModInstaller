import os
import io
import sys
import zipfile
import requests
import threading
import customtkinter

BEPINEX = "692/BepInEx-Unity.IL2CPP-win-x64-6.0.0-be.692%2B851521c"
POLYMOD = "https://github.com/PolytalesDevTeam/PolyMod/releases/latest/download/PolyMod.dll"


def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)


def to_zip(request: requests.Response):
    return zipfile.ZipFile(io.BytesIO(request.content))


def browse():
    global path_entry
    path_entry.delete(0, customtkinter.END)
    path_entry.insert(0, customtkinter.filedialog.askdirectory())


def install():
    global progress_bar
    path_entry.configure(state=customtkinter.DISABLED)
    browse_button.configure(state=customtkinter.DISABLED)
    install_button.configure(state=customtkinter.DISABLED)
    progress_bar = customtkinter.CTkProgressBar(app, determinate_speed=50 / 2)
    progress_bar.grid(column=0, row=2, columnspan=2, padx=5, pady=5)
    progress_bar.set(0)
    threading.Thread(target=_install, daemon=True).start()


def _install():
    path = path_entry.get()

    if not os.path.exists(path):
        os.makedirs(path)

    to_zip(
        requests.get(f"https://builds.bepinex.dev/projects/bepinex_be/{BEPINEX}.zip")
    ).extractall(path)
    progress_bar.step()

    open(path + "/BepInEx/plugins/PolyMod.dll", "wb").write(
        requests.get(POLYMOD).content
    )
    progress_bar.step()

    customtkinter.CTkButton(app, text="Launch", command=launch).grid(
        column=0, row=3, columnspan=2, padx=5, pady=5
    )


def launch():
    os.system("start steam://rungameid/874390")
    app.destroy()
    sys.exit()


app = customtkinter.CTk()
app.title("PolyMod")
app.iconbitmap(default=resource_path("icon.ico"))
app.resizable(False, False)

path_entry = customtkinter.CTkEntry(app, placeholder_text="Game path", width=228)
browse_button = customtkinter.CTkButton(app, text="Browse", command=browse, width=1)
install_button = customtkinter.CTkButton(app, text="Install", command=install)

path_entry.grid(column=0, row=0, padx=5, pady=5)
browse_button.grid(column=1, row=0, padx=(0, 5), pady=5)
install_button.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

app.mainloop()

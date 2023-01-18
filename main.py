from pygame import mixer
import tkinter
from tkinter.filedialog import askdirectory
import os

p = False

root = tkinter.Tk()
root.title("Music Player")
root.geometry("270x325")

var = tkinter.StringVar()
var.set("Select the song to play")

os.chdir(askdirectory())
songlist = os.listdir()

playing = tkinter.Listbox(root, font="Roboto,12", width=28, bg="black", fg="white", selectmode=tkinter.SINGLE)

for song in songlist:
    playing.insert(0, song)


mixer.init()


def play():
    mixer.music.load(playing.get(tkinter.ACTIVE))
    name = playing.get(tkinter.ACTIVE)
    var.set(f"{name[:20]}..." if len(name) > 22 else name)
    mixer.music.play()


def pause():
    global p
    if not p:
        mixer.music.pause()
        p = True
        pause_button.config(text="Resume")
    else:
        mixer.music.unpause()
        p = False
        pause_button.config(text="Pause")


def change_volume(v):
    mixer.music.set_volume(int(v)/100)


text = tkinter.Label(root, font="Roboto,12", textvariable=var)
text.grid(row=0, columnspan=3)
playing.grid(columnspan=3)
play = tkinter.Button(root, width=7, height=1,font="Roboto", text="Play", command=play)
play.grid(row=2, column=0)
pause_button = tkinter.Button(root, width=7, height=1, font="Roboto", text="Pause", command=pause, fg="black")
pause_button.grid(row=2, column=2)
sound_label = tkinter.Label(root, font="Roboto,12", text="Volume:")
sound_label.grid(row=3, column=0)
volume = tkinter.Scale(root, from_=0, to=100, orient="horizontal", command=change_volume)
volume.set(100)
volume.grid(row=3, column=1)

root.mainloop()

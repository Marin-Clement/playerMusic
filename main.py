from pygame import mixer
import tkinter
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os

p = False
current_pos = 0


root = tkinter.Tk()
#root.resizable(False, False)
root.title("Music Player")
root.geometry("256x325")

var = tkinter.StringVar()
var.set("Select the song to play")

os.chdir(askdirectory())
songlist = os.listdir()

playing = tkinter.Listbox(root, font="Roboto,12", width=28, bg="black", fg="white", selectmode=tkinter.SINGLE)

for song in songlist:
    playing.insert(0, song)


mixer.init()


def play():
    print(mixer.Sound(playing.get(tkinter.ACTIVE)).get_length())
    global p
    reset_progressbar()
    update_progressbar()
    mixer.music.load(playing.get(tkinter.ACTIVE))
    name = playing.get(tkinter.ACTIVE)
    var.set(f"{name[:20]}..." if len(name) > 22 else name)
    mixer.music.play()
    p = False
    pause_button.config(text="Pause")


def pause():
    global p
    if not p:
        mixer.music.pause()
        p = True
        pause_button.config(text="Resume")
    else:
        mixer.music.unpause()
        p = False
        update_progressbar()
        pause_button.config(text="Pause")


def change_volume(v):
    mixer.music.set_volume(int(v)/100)


def previous_song():
    current_song = playing.curselection()
    if not current_song:
        previous_song = 0
    else:
        previous_song = current_song[0] - 1
    if previous_song < 0:
        previous_song = len(songlist) - 1
    playing.activate(previous_song)
    playing.selection_clear(0, len(songlist) - 1)
    playing.activate(previous_song)
    playing.selection_set(previous_song, last=previous_song)
    play()


def next_song():
    current_song = playing.curselection()
    if not current_song:
        next_song = 0
    else:
        next_song = current_song[0] + 1
    if next_song >= len(songlist):
        next_song = 0
    playing.activate(next_song)
    playing.selection_clear(0, len(songlist) - 1)
    playing.activate(next_song)
    playing.selection_set(next_song, last=next_song)
    play()


def update_progressbar():
    global current_pos
    progressbar.config(value=current_pos)
    current_pos += 1
    print(current_pos)
    if mixer.music.get_busy() and not p:
        root.after(1000, update_progressbar)


def on_progressbar_click(event):
    global current_pos
    new_pos = int(event.x * progressbar['maximum'] / progressbar.winfo_width())
    current_pos = new_pos
    mixer.music.rewind()
    mixer.music.set_pos(new_pos)


def reset_progressbar():
    global current_pos
    current_pos = 0
    progressbar.config(value=current_pos)


text = tkinter.Label(root, font="Roboto,12", textvariable=var)
text.grid(row=0, columnspan=3)

playing.grid(columnspan=3)

play_button = tkinter.Button(root, width=7, height=1,font="Roboto", text="Play", command=play)
play_button.grid(row=3, column=1)

pause_button = tkinter.Button(root, width=7, height=1, font="Roboto", text="Pause", command=pause, fg="black")
pause_button.grid(row=4, column=1)

sound_label = tkinter.Label(root, font="Roboto,12", text="Volume:")
sound_label.grid(row=5, column=0)

volume = tkinter.Scale(root, from_=0, to=100, orient="horizontal", command=change_volume)
volume.set(100)
volume.grid(row=5, column=1)

next_button = tkinter.Button(root, width=7, height=1, font="Roboto", text="Next", command=next_song)
next_button.grid(row=4, column=2)

previous_button = tkinter.Button(root, width=7, height=1, font="Roboto", text="Previous", command=previous_song)
previous_button.grid(row=4, column=0)

progressbar = ttk.Progressbar(root, maximum=mixer.Sound(playing.get(tkinter.ACTIVE)).get_length(), length=250)
progressbar.grid(row=2, columnspan=3)
progressbar.bind("<Button-1>", on_progressbar_click)

if mixer.music.get_busy() and not p:
    update_progressbar()
root.mainloop()

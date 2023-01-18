from pygame import mixer
import tkinter
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os
import random

p = False
current_pos = 0

repeat_status = False
random_status = False

name_scrolling_task = str()
current_max = int()

root = tkinter.Tk()
root.resizable(False, False)
root.title("Ipod")
root.iconbitmap("myIcon.ico")
root.geometry("266x420")

var = tkinter.StringVar()
var.set("Select the song to play")


current_time_max_ui = tkinter.StringVar()
current_time_ui = tkinter.StringVar()

os.chdir(askdirectory())
songlist = os.listdir()

playing = tkinter.Listbox(root, font="Roboto,12", width=28, bg="black", fg="white", selectmode=tkinter.SINGLE)

for song in songlist:
    playing.insert(0, song)

mixer.init()


def play():
    global p, name_scrolling_task, current_max
    current_max = mixer.Sound(playing.get(tkinter.ACTIVE)).get_length()
    reset_progressbar()
    mixer.music.load(playing.get(tkinter.ACTIVE))
    name = playing.get(tkinter.ACTIVE)
    name = name.rstrip(".mp3 ") + " " * 4
    if name_scrolling_task:
        root.after_cancel(name_scrolling_task)
    name_scrolling_task = root.after(0, name_scrolling, name)
    mixer.music.play()
    p = False
    pause_button.config(text="Pause")
    current_time_max_ui.set(str(convert(current_max)))
    progressbar.config(maximum=current_max)


def on_song_end():
    if repeat_status:
        play()
    elif random_status:
        choose_random_song()
    else:
        next_song()


def stop():
    global p, name_scrolling_task
    mixer.music.stop()
    p = False
    pause_button.config(text="Pause")
    if name_scrolling_task:
        root.after_cancel(name_scrolling_task)
    var.set("Select the song to play")
    current_time_max_ui.set("")
    current_time_ui.set("")
    reset_progressbar()


def name_scrolling(name):
    global name_scrolling_task
    var.set(name[:20])
    name_scrolling_task = root.after(250, name_scrolling, name[1:]+name[0])


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


def update():
    if not p and mixer.music.get_busy():
        global current_pos, current_max
        progressbar.config(value=current_pos)
        current_pos += 1
        current_time_ui.set(str(convert(current_pos)))
        root.after(1000, update)
        if current_pos >= int(current_max) - 1:
            on_song_end()
    else:
        root.after(1000, update)


def on_progressbar_click(event):
    global current_pos, p
    new_pos = int(event.x * progressbar['maximum'] / progressbar.winfo_width())
    current_pos = new_pos
    mixer.music.rewind()
    mixer.music.set_pos(new_pos)
    if p:
        mixer.music.unpause()
        p = False
        pause_button.config(text="Pause")


def reset_progressbar():
    global current_pos
    current_pos = 0
    progressbar.config(value=current_pos)


def repeat():
    global repeat_status
    if not repeat_status:
        repeat_button.config(bg="green")
        repeat_status = True
    else:
        repeat_button.config(bg="white")
        repeat_status = False


def random_button():
    global random_status
    if not random_status:
        random_song_button.config(bg="green")
        random_status = True
    else:
        random_song_button.config(bg="white")
        random_status = False


def choose_random_song():
    random_song = random.choice(songlist)
    playing.activate(songlist.index(random_song))
    playing.selection_clear(0, len(songlist) - 1)
    playing.activate(songlist.index(random_song))
    playing.selection_set(songlist.index(random_song), last=songlist.index(random_song))
    play()


def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%02d:%02d" % (minutes, seconds)


playing.grid(columnspan=3, row=0, padx=5,pady=5)

current_t = tkinter.Label(root, font="Roboto,12", textvariable=current_time_ui)
current_t.grid(row=2, column=0)

max_t = tkinter.Label(root, font="Roboto,12", textvariable=current_time_max_ui)
max_t.grid(row=2, column=2)

text = tkinter.Label(root, font="Roboto,12", textvariable=var, pady=10)
text.grid(row=3, columnspan=3)

play_button = tkinter.Button(root, width=7, height=1, font="Roboto,12", text="Play", command=play)
play_button.grid(row=4, column=0)

stop_button = tkinter.Button(root,width=7, height=1, font="Roboto,12", text="Stop", command=stop)
stop_button.grid(row=4, column=2)

pause_button = tkinter.Button(root, width=7, height=1, font="Roboto,12", text="Pause", command=pause, fg="black")
pause_button.grid(row=5, column=1)

volume = tkinter.Scale(root, from_=0, to=100, orient="horizontal", font="Roboto,12", command=change_volume)
volume.set(100)
volume.grid(row=6, column=1)

next_button = tkinter.Button(root, width=7, height=1, font="Roboto,12", text="Next", command=next_song)
next_button.grid(row=5, column=2)

previous_button = tkinter.Button(root, width=7, height=1, font="Roboto,12", text="Previous", command=previous_song)
previous_button.grid(row=5, column=0)

repeat_button = tkinter.Button(root, width=7, height=1, font="Roboto,12", text="Repeat", command=repeat, bg="white")
repeat_button.grid(row=6, column=2)

random_song_button = tkinter.Button(root, width=7, height=1, font="Roboto,12", text="Random", command=random_button, bg="white")
random_song_button.grid(row=6, column=0)

progressbar = ttk.Progressbar(root, length=250)
progressbar.grid(row=1, columnspan=3, pady=10)
progressbar.bind("<Button-1>", on_progressbar_click)

update()
root.mainloop()

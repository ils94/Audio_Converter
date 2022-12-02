from pydub import AudioSegment
from tkinter import filedialog, Tk, Button, Frame, X, Entry, END, Label, LEFT, RIGHT, messagebox, OptionMenu, \
    StringVar, ttk
import os
import threading

audio_list = []

STOP = True

AudioSegment.converter = r"ffmpeg.exe"


def disable_widgets():
    entry_in["state"] = "disabled"
    entry_out["state"] = "disabled"
    sample_rate_option["state"] = "disabled"
    bit_rate_option["state"] = "disabled"
    extension_option["state"] = "disabled"
    channel_option["state"] = "disabled"
    button_start["state"] = "disabled"


def enable_widgets():
    entry_in["state"] = "normal"
    entry_out["state"] = "normal"
    sample_rate_option["state"] = "normal"
    bit_rate_option["state"] = "normal"
    extension_option["state"] = "normal"
    channel_option["state"] = "normal"
    button_start["state"] = "normal"


def stop():
    global STOP

    if not STOP:
        STOP = True

        button_stop["state"] = "disabled"
        button_stop["text"] = "Stopping..."


def multithreading(function):
    t = threading.Thread(target=function)
    t.setDaemon(True)
    t.start()


def convert():
    try:
        global audio_list, STOP

        counter = 0

        pb["value"] = 0

        if os.path.isdir(entry_in.get()) and os.path.isdir(entry_out.get()):
            for file in os.listdir(entry_in.get()):
                if file.endswith(".mp3") or file.endswith(".mp4") or file.endswith(".wav") or file.endswith(".ogg"):
                    audio_list.append(file)

        if audio_list:

            STOP = False

            disable_widgets()

            for audio in audio_list:
                if not STOP:
                    counter += 1

                    audio_name["text"] = 'Converting "' + audio

                    sound = AudioSegment.from_file(entry_in.get() + "/" + audio)
                    sound.set_frame_rate(int(var_sample_rate.get().replace(" Khz", "")))
                    sound.set_channels(int(var_channel.get().replace("Ch ", "")))
                    no_ex = audio.split(".")
                    sound.export(entry_out.get() + "/" + no_ex[0] + "." + var_extension.get(),
                                 format=var_extension.get(),
                                 bitrate=var_bit_rate.get().replace(" kbps", "") + "k")

                    pb["value"] = counter / len(audio_list) * 100
                else:
                    pb["value"] = 0
                    button_stop["state"] = "normal"
                    button_stop["text"] = "Stop"
                    STOP = True
                    audio_list.clear()
                    break

            audio_name["text"] = "All done!"
            STOP = True
            audio_list.clear()
            enable_widgets()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        enable_widgets()


def file_dialog(entry):
    file = filedialog.askdirectory()

    if file != "":
        entry.delete(0, END)
        entry.insert(0, file)


root = Tk()

window_width = 350
window_height = 160

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

var_sample_rate = StringVar(root)
var_sample_rate.set("44100 Khz")
var_bit_rate = StringVar(root)
var_bit_rate.set("128 kbps")
var_extension = StringVar(root)
var_extension.set("mp3")
var_channel = StringVar(root)
var_channel.set("Ch 2")

root.geometry("350x155+" + str(int(x)) + "+" + str(int(y)))
root.title("Audio Converter")
root.resizable(False, False)
if os.path.isfile("icon/icon.ico"):
    root.iconbitmap("icon/icon.ico")

frame1 = Frame(root)
frame1.pack(fill=X)

entry_in = Entry()
entry_in.pack(fill=X, padx=5, pady=1)
entry_in.insert(0, "Folder with audio files to convert")
entry_in.bind("<Double-Button-1>", lambda x: file_dialog(entry_in))

entry_out = Entry()
entry_out.pack(fill=X, padx=5, pady=1)
entry_out.insert(0, "Folder where the converted audios will be saved")
entry_out.bind("<Double-Button-1>", lambda x: file_dialog(entry_out))

frame2 = Frame(root)
frame2.pack(fill=X)

sample_rate_option = OptionMenu(frame2, var_sample_rate, "32000 Khz", "44100 Khz", "48000 Khz")
sample_rate_option.config(width=8)
sample_rate_option.pack(side=LEFT, padx=2, pady=1)

bit_rate_option = OptionMenu(frame2, var_bit_rate, "64 kbps", "128 kbps", "192 kbps", "320 kbps")
bit_rate_option.config(width=7)
bit_rate_option.pack(side=LEFT, padx=2, pady=1)

extension_option = OptionMenu(frame2, var_extension, "mp3", "wav", "ogg")
extension_option.config(width=3)
extension_option.pack(side=LEFT, padx=2, pady=1)

channel_option = OptionMenu(frame2, var_channel, "Ch 1", "Ch 2")
channel_option.config(width=3)
channel_option.pack(side=LEFT, padx=2, pady=1)

frame3 = Frame(root)
frame3.pack(fill=X)

pb = ttk.Progressbar(frame3, orient="horizontal", mode="determinate", length=100)
pb.pack(fill=X, padx=5, pady=1)

audio_name = Label(frame3)
audio_name.pack(padx=5, pady=1)

frame4 = Frame(root)
frame4.pack(fill=X)

button_start = Button(frame4, text="Start", width=10, height=1, command=lambda: multithreading(convert))
button_start.pack(side=LEFT, padx=5, pady=1)

button_stop = Button(frame4, text="Stop", width=10, height=1, command=stop)
button_stop.pack(side=RIGHT, padx=5, pady=1)

root.mainloop()

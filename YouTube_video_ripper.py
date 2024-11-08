import threading
import os
import re
import moviepy
from tkinter import *
from tkinter.ttk import Progressbar
from pytube import *
from pytube import Playlist
from threading import Thread
from moviepy.editor import *
 
invalidchar = re.compile('[?|:\/]')
validlink = 'https://www.youtube.com/'

disposablePath = '/Volumes/320G/disposable'
outputPath = '/Volumes/320G/YouTubeRip'

window = Tk()
linklabel = Label(window, text='Paste link here', fg='purple', bg='#282828', font=("Comic Sans MS", 20)).pack(side=TOP)

link = StringVar()
linkfield1 = Entry(window, width= 50, textvariable=link).pack(side=TOP)

DownloadPlaylist = IntVar()
Downloadmode = IntVar()
Playlistmode = Checkbutton(window,text='Playlist',bg='#282828',fg='purple',activebackground='#282828',font=("Comic Sans MS", 10), variable=DownloadPlaylist).pack(side=TOP)
Audio = Radiobutton(window,text='Audio',bg='#282828',fg='purple',activebackground='#282828',font=("Comic Sans MS", 10), variable=Downloadmode, value=1).pack(side=TOP)
Video = Radiobutton(window,text='Video',bg='#282828',fg='purple',activebackground='#282828',font=("Comic Sans MS", 10), variable=Downloadmode, value=2).pack(side=TOP)

def run_progress(): #yay a progress bar
    if validlink in link.get():
        progress.start(5)    

def video_downloader(): #video function
    DownloadPlaylistmode = DownloadPlaylist.get()
    Download_label = Label(window, text='Downloading', fg='purple', bg='#282828', font=("Comic Sans MS", 15))
    Download_label.pack(side='top')
    if DownloadPlaylistmode == 1 :
        playlist = Playlist(str(link.get()))
        num_of_video = playlist.length
        Episode_num = 0 #for ripping series playlist
        for url in playlist.video_urls[:num_of_video]:
            Episode_num += 1 #for ripping series playlist
            video = YouTube(url, use_oauth=True, allow_oauth_cache=True)
            video_title = video.title
            if invalidchar.search(video_title): #invalid character filter
                new_video_title = video_title.replace("|", "").replace("?", "").replace(":", "").replace("/", "")
            else:
                new_video_title = video_title                
            print(new_video_title+".mp4 is downloading")     
            video.streams.filter(adaptive=True).first().download(output_path= disposablePath, filename= new_video_title+'.mp4', max_retries = 100)
            print('done downloading .mp4')
        Download_label.destroy()
    else:
        video = YouTube(str(link.get()), use_oauth=True, allow_oauth_cache=True)
        video_title = video.title
        if invalidchar.search(video_title): #invalid character filter
            new_video_title = video_title.replace("|", "").replace("?", "").replace(":", "").replace("/", "")
        else:
            new_video_title = video_title                
        print(new_video_title+".mp4 is downloading")  
        video.streams.filter(adaptive=True).first().download(output_path= disposablePath, filename= new_video_title+'.mp4', max_retries = 100)
        print('done downloading .mp4')
        Download_label.destroy()              
    video_audio_merger()    
    Finishlabel = Label(window, text='Done', fg='purple', bg='#282828', font=("Comic Sans MS", 15))
    Finishlabel.pack(side='top')
    Finishlabel.after(5000, Finishlabel.destroy)
    progress.stop()    
    

def audio_downloader(): #audio function
    DownloadPlaylistmode = DownloadPlaylist.get()
    selection = Downloadmode.get()
    if selection == 1:
        Download_label = Label(window, text='Downloading', fg='purple', bg='#282828', font=("Comic Sans MS", 15))
        Download_label.pack(side='top')
        output_folder = outputPath
        extension = ".mp3"
    else:
        output_folder = disposablePath
        extension = ".aac"
    if DownloadPlaylistmode == 1 :
        playlist = Playlist(str(link.get()))
        num_of_audio = playlist.length
        Episode_num = 0 #for ripping series playlist
        for url in playlist.video_urls[:num_of_audio]:
            Episode_num += 1 #for ripping series playlist
            audio = YouTube(url, use_oauth=True, allow_oauth_cache=True)
            audio_title = audio.title
            if invalidchar.search(audio_title): #invalid character filter
                    new_audio_title = audio_title.replace("|", "").replace("?", "").replace(":", "").replace("/", "")
            else:
                    new_audio_title = audio_title                
            print(new_audio_title+extension+" is downloading") 
            audio.streams.get_audio_only().download(output_path= output_folder, max_retries= 100, filename= new_audio_title+extension)
            print("done downloading "+extension)
    else:
        audio = YouTube(str(link.get()), use_oauth=True, allow_oauth_cache=True)
        audio_title = audio.title
        if invalidchar.search(audio_title): #invalid character filter
            new_audio_title = audio_title.replace("|", "").replace("?", "").replace(":", "").replace("/", "")
        else:
            new_audio_title = audio_title                
        print(new_audio_title+extension+" is downloading")
        audio.streams.get_audio_only().download(output_path= output_folder, max_retries= 100, filename= new_audio_title+extension)
        print("done downloading "+extension)
    if selection == 1:    
        Download_label.destroy()    
        Finishlabel = Label(window, text='Done', fg='purple', bg='#282828', font=("Comic Sans MS", 15))
        Finishlabel.pack(side='top')
        Finishlabel.after(5000, Finishlabel.destroy)
        progress.stop()        

def video_audio_merger(): #need to figure out a way to run this automatically
    DownloadPlaylistmode = DownloadPlaylist.get()
    Finalizing_label = Label(window, text='Finalizing', fg='purple', bg='#282828', font=("Comic Sans MS", 15))
    Finalizing_label.pack(side='top')
    Episode_num = 0 #for ripping series playlist
    if DownloadPlaylistmode == 1 :
        playlist = Playlist(str(link.get()))
        num_of_video = playlist.length
        for url in playlist.video_urls[:num_of_video]:
            Episode_num += 1 #for ripping series playlist      
            video = YouTube(url, use_oauth=True, allow_oauth_cache=True)
            video_title = video.title
            if invalidchar.search(video_title): #invalid character filter
                new_video_title = video_title.replace("|", "").replace("?", "").replace(":", "").replace("/", "")
            else:
                new_video_title = video_title                
            print("Finalizing "+new_video_title)
            temp_video_path = os.path.join(disposablePath, new_video_title+'.mp4') #put string into file path
            temp_audio_path = os.path.join(disposablePath, new_video_title+'.aac') #put string into file path
            output_folder = os.path.join(outputPath, new_video_title+'.mp4') #put string into file path
            moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio(temp_video_path, temp_audio_path, output_folder, vcodec='copy', acodec='copy', ffmpeg_output=False, logger='bar')
        Finalizing_label.destroy()
    else:
        video = YouTube(str(link.get()), use_oauth=True, allow_oauth_cache=True)
        video_title = video.title
        if invalidchar.search(video_title): #invalid character filter
            new_video_title = video_title.replace("|", "").replace("?", "").replace(":", "").replace("/", "")
        else:
            new_video_title = video_title                
        print("Finalizing "+new_video_title)
        temp_video_path = os.path.join(disposablePath, new_video_title+'.mp4') #put string into file path
        temp_audio_path = os.path.join(disposablePath, new_video_title+'.aac') #put string into file path
        output_folder = os.path.join(outputPath, new_video_title+'.mp4') #put string into file path
        moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio(temp_video_path, temp_audio_path, output_folder, vcodec='copy', acodec='copy', ffmpeg_output=False, logger='bar')
        Finalizing_label.destroy()  

def main(): #running 3 func at the same time using threading
    selection = Downloadmode.get()
    if validlink in link.get():
        if selection == 1:
            threading.Thread(target=audio_downloader).start()
            threading.Thread(target=run_progress).start()
        if selection == 2:
            threading.Thread(target=audio_downloader).start()
            threading.Thread(target=run_progress).start()
            threading.Thread(target=video_downloader).start()                           
    else:
        Errorlabel = Label(window, text='Invaild link', fg='purple', bg='#282828', font=("Comic Sans MS", 15))
        Errorlabel.pack(side='top')
        Errorlabel.after(5000, Errorlabel.destroy)           

progress = Progressbar(window, mode='indeterminate', length=200)
progress.place (x=480/2, y=210, anchor=CENTER)

button1 = Button(window,text='RIP', bg='black', activebackground='black', command = main).place (x=480/2, y=260, anchor=CENTER)
button2 = Button(window,text='Finalize Video', bg='black', activebackground='black', command = video_audio_merger).place (x=480/2, y=300, anchor=CENTER)

window.title('Youtube Ripper')
window.geometry("480x350")
window.resizable(0,0) #prevent resizing
window.configure(bg='#282828')
window.mainloop()

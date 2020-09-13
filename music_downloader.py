#goals 
# 300 + lines 
# video file_quality  
# audio download ✓ 
# add in download location 
# GUI format
# alternative: music bot on discord
#Library

import os as OS 
import cv2
import sys
import time
import json
import shutil
import subprocess
import ffmpeg
from mhmovie.code import *
from moviepy.editor import *
from pytube import YouTube
from youtubesearchpython import SearchVideos
import PySimpleGUI as sg  #add in GUI functionality

#Conditions

OS.system('cls')
runtime = 0
prefix_link = 'https://www.youtube.com'
download_location = (OS.getcwd()+'\\tmp\\') # puts the download in a temporary folder in the same working dir
aud_loc = (OS.getcwd()+'\\downloads\\'+'\\audio\\')
av_loc = (OS.getcwd()+'\\downloads\\' + '\\av\\')
yt_link = ''
title = ''
sg.theme('DarkAmber')
layout = [
    [sg.Text('Search for video: '), sg.Input()],
    [sg.Text('Audio Only?: ') ,sg.Checkbox(text = ' ', size=(1,1), default=False)],
    [sg.Text('Advanced Video options: (Just press download if not sure.)')],
    [sg.Radio(text='adaptive', group_id=1),sg.Radio(text='progressive', group_id=1), sg.Button('Search')],
    [sg.Text('Save location: '), sg.Input(), sg.FileBrowse()],
    [sg.Button('Download'), sg.Button('Exit')],
]

window = sg.Window("YT Downloader", layout)
        
#Back End-----------------------

def combine(vidname, audname, outname, fps=30):
    query = f'ffmpeg -i "{vidname}" -i "{audname}" -c:v copy -c:a aac "{outname}"'
    print(query)
    OS.system(query)
    

def quote(string):
    return '"{}"' .format(string)

def search(strng): #Fetch link
    OS.system('cls')
    global yt_link
    #search_query = (input("Search for a video :  ")) -> depreciated
    search_result = json.loads(SearchVideos(str(strng), offset = 1, mode = "json", max_results = 1).result())
    yt_link = search_result.get("search_result")[0].get("link")

def download(bol=False, obj = None, typ = None, aud = None): #Fetch video
    global title 
    if obj:
        if typ == 'prog':
            title = obj.title
            obj.download(av_loc)
        if typ == 'raw':
            title = obj.title
            aud.download()
            convert_to_mp3(OS.getcwd())
            obj.download()
            vidc = cv2.VideoCapture(title+'.mp4')
            vidfps = vidc.get(cv2.CAP_PROP_FPS)
            #videoclip = VideoFileClip(f'{(title)}.mp4')
            #audioclip = AudioFileClip(f"{str(title)}.mp3")
            #new_audioclip = CompositeAudioClip([audioclip])
            #videoclip.audio = new_audioclip
            #videoclip.write_videofile(f"{str(title)}[out].mp4")
            time.sleep(2)
            #OS.rename(f'{title}.mp4', 'output.mp4')
            #OS.rename(f'{title}.mp3', 'output.mp3')
            combine(f'output.mp4', f"output.mp3", f"{str(title)}.mp4")
            time.sleep(2)
            OS.remove(f'output.mp4')
            OS.remove(f'output.mp3')
            shutil.move(f"{str(title)}.mp4", av_loc)
            #m = movie(f"{OS.getcwd()}\\{title}.mp4")
            #mu = music(f'{OS.getcwd()}\\{title}.mp3')
            #mu.Aconvert()#convert wav to mp3
            #final = m+mu
            #final.save(f"{download_location}\\{title}\\")
            
        elif typ == 'audio':
            title = obj.title
            obj.download(aud_loc)
    else:
        try:
            yt = YouTube(yt_link, on_progress_callback = progress_Check)
        except KeyError:
            print("RIP There's a cifer")
            return
        title = yt.title
        if bol:
            yt_video = yt.streams.filter(only_audio = True, adaptive= True).first()
            yt_video.download(aud_loc)
            convert_to_mp3()
        elif not bol:
            yt_video = yt.streams.filter(progressive=True, file_extension='mp4').first()
            yt_video.download(av_loc)
        else:
            print("Something effed up")

def progress_Check(chunk, file_handle, remaining): #check download progress
    sys.stdout.write(f'Downloading now: {title}\n')
    sys.stdout.write(f'Megabytes remaining: {round(remaining / 1000000, 2)} MB')
    OS.system('cls')
    
    
def convert_to_mp3(loc = aud_loc): #convert from mp4 to mp3 for groove/etc
    print("-> Download complete. Compiling into mp3...")
    print("Finding file...")
    OS.chdir(loc) #permanently change dir to aud folder
    for files in OS.walk(loc):
            for filedir in files:
                for mp4 in filedir:
                    if mp4.endswith('.mp4'): #verify file is actually of .mp4 extension
                        mp4file = mp4
                        print(f"Found {mp4file}.")
                        audioclip = AudioFileClip(mp4file) #select audio file 
                        audioclip.write_audiofile(f"{mp4file[0:-4]}.mp3") 
                        audioclip.close() #write audio file as mp3 with the same name, and remove the '.mp4' section
                        print("\nDeleting the old file..")
                        OS.remove(mp4file) #Remove old .mp4 file
                        print("\nAll done! Exiting program if no more mp4 files found.")
                        return

def save(direct):
    shutil.move(download_location, direct)
#Front End-----------------------

#while runtime == 0: #Need to add a proper PyQT5 or (preferably) an actual GUI
#    choice = input('''
#======================
#Music downloader...
#    
#Press 1 to download.
#    
#Press 2 to exit.
#    
#Enter your choice - ''')
#    if choice == '1':
#        
#       #search()
#       #download()
#       #convert_to_mp3()
#    
#    elif choice == '2':
#        runtime = 1

def audioonlyadv(values, yt):
    print("hye from audio only!")
    opts = yt.streams.filter(only_audio=True).all()
    optx = []
    for stream in opts:
        txt = str(stream)
        optx.append(stream)
    print(optx)
    wind = [
        *[[sg.Radio(text=text, group_id=1),] for text in optx],
        [sg.Button('Download!'), sg.Button('Exit')],
    ]

    wind = sg.Window("Audio Only" , wind , keep_on_top=True)
    while True:
        fevent, fvalues = wind.read()
        if fevent == sg.WIN_CLOSED:
            break
        elif fevent == 'Exit':
            break
        elif fevent == 'Download!':
            choice = list(fvalues.values()).index(True)
            obj = opts[choice]
            download(False, obj, 'audio')

def adaptiveadv(values, yt):
    print("hye from progressive!")
    opts = yt.streams.filter(adaptive=True, only_audio = True, file_extension = 'mp4').all()
    optv = yt.streams.filter(adaptive=True, only_video = True, file_extension = 'mp4').all()
    optx = []
    opty = []
    for stream in opts:
        txt = str(stream)
        optx.append(stream)
    for stream in optv:
        txt = str(stream)
        opty.append(stream)
    print(optx)
    wind = [
        [sg.Text('Video Stream: ')],
        *[[sg.Radio(text=text, group_id=1),] for text in opty],
        [sg.Text('Audio Stream: ')],
        *[[sg.Radio(text=text, group_id=2),] for text in optx],
        [sg.Button('Download!'), sg.Button('Exit')],
    ]

    wind = sg.Window("Adaptive[DASH]" , wind , keep_on_top=True)
    while True:
        fevent, fvalues = wind.read()
        if fevent == sg.WIN_CLOSED:
            break
        elif fevent == 'Exit':
            break
        elif fevent == 'Download!':
            choices = []
            for key, value in fvalues.items():
                if value == True:
                    choices.append(key)
                else:
                    continue
            download(False, opty[choices[0]], 'raw', optx[(len(fvalues)-1) - choices[1]])


def progressive(values, yt):
    print("hye from progressive!")
    opts = yt.streams.filter(adaptive=True).all()
    optx = []
    for stream in opts:
        txt = str(stream)
        optx.append(stream)
    print(optx)
    wind = [
        *[[sg.Radio(text=text, group_id=1),] for text in optx],
        [sg.Button('Download!'), sg.Button('Exit')],
    ]

    wind = sg.Window("Progressive[Low Quality]" , wind , keep_on_top=True)
    while True:
        fevent, fvalues = wind.read()
        if fevent == sg.WIN_CLOSED:
            break
        elif fevent == 'Exit':
            break
        elif fevent == 'Download!':
            choice = list(fvalues.values()).index(True)
            obj = opts[choice]
            download(False, obj, 'prog')

def errwin():
    errwind = [
        [sg.Text("Oof! You should've picked a radio button or chosen audio only or searched for something! Please exit and choose an option!")],
        [sg.Button('Exit')],
    ]

    err = sg.Window("Oof" , errwind , keep_on_top=True)
    while True:
        fevent, fvalues = err.read()
        if fevent == sg.WIN_CLOSED:
            break
        elif fevent == 'Exit':
            break

def adv_search(values):
    search(values[0])
    yt = YouTube(yt_link, on_progress_callback = progress_Check)
    if values[1]:
        print(1)
        audioonlyadv(values, yt)
    elif values[2]:
        print(2)
        adaptiveadv(values, yt)
    elif values[3]:
        print(3)
        progressive(values, yt)
    else:
        print(4)
        errwin()



while True:
    event, values = window.read()
    print(values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Download':
        if values[0] != '':
            search(values[0])
            download(values[1])
            if values[2]:
                save(values[2])
        else:
            errwin()
    elif event == 'Search':
        if values[0] != '':
            print('here!')
            adv_search(values)
            if values[2]:
                save(values[2])
        else:
            errwin()
window.close()
    


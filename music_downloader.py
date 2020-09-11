#goals 
# 300 + lines 
# video file_quality  
# audio download ✓ 
# add in download location 
# GUI format
# alternative: music bot on discord
#Library

import os as OS 
import sys
import time
import moviepy.editor as movpy 
from pytube import YouTube
from youtube_search import YoutubeSearch
import PySimpleGUI as sg  #add in GUI functionality

#Conditions

OS.system('cls')
runtime = 0
prefix_link = 'https://www.youtube.com'
download_location = (OS.getcwd()+'/tmp/') # puts the download in a temporary folder in the same working dir
sg.theme('DarkAmber')
layout = [
    [sg.Text('Search for video:'), sg.Input()],
    [sg.Button('Download'), sg.Button('Exit')],
]

window = sg.Window("Music downloader", layout)
        
#Back End-----------------------

def search(strng): #Fetch link
    OS.system('cls')
    global yt_link
    #search_query = (input("Search for a video :  ")) -> depreciated
    search_result = YoutubeSearch(str(strng), max_results = 1).to_dict()
    for results in search_result:
        for k,v in results.items():
            if k == 'url_suffix':
                yt_link = (prefix_link+v)


def download(): #Fetch video
    yt = YouTube(yt_link, on_progress_callback = progress_Check)
    global title 
    title = yt.title
    yt_video = yt.streams.filter(only_audio = True, adaptive= True).first()
    yt_video.download(download_location)
    print("-> Download complete. Compiling into mp3...")

def progress_Check(chunk, file_handle, remaining): #check download progress
    sys.stdout.write(f'Downloading now: {title}\n')
    sys.stdout.write(f'Megabytes remaining: {round(remaining / 1000000, 2)} MB')
    OS.system('cls')
    
    
def convert_to_mp3(): #convert from mp4 to mp3 for groove/etc
    print("Finding file...")
    OS.chdir(download_location) #permanently change dir to temp folder
    for files in OS.walk(download_location):
            for filedir in files:
                for mp4 in filedir:
                    if mp4.endswith('.mp4'): #verify file is actually of .mp4 extension
                        mp4file = mp4
                        print(f"Found {mp4file}.")
                        audioclip = movpy.AudioFileClip(mp4file) #select audio file 
                        audioclip.write_audiofile(f"{mp4file[0:-4]}.mp3") 
                        audioclip.close() #write audio file as mp3 with the same name, and remove the '.mp4' section
                        print("\nDeleting the old file..")
                        OS.remove(mp4file) #Remove old .mp4 file
                        print("\nAll done! Exiting program if no more mp4 files found.")
                        time.sleep(1)

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


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Download':
        search(values[0])
        download()
        convert_to_mp3()

window.close()
    


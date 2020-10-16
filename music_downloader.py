#goals 
# 300 + lines 
# video file_quality  
# audio download ✓ 
# add in download location ✓
# GUI format ✓
#Library

import os
import sys
import time
import moviepy.editor as movpy 
from pytube import YouTube
from youtube_search import YoutubeSearch
import PySimpleGUI as sg  #add in GUI functionality

#Conditions

work_dir = 0
os.system('cls')
runtime = 0
prefix_link = 'https://www.youtube.com'

dl_tp = '''Use this button for downloading any video/music file you would like, from youtube. The resolution settings work 
only when the video quality is selected, the audio quality defaults to the maximum.'''

cv_tp = '''Use this to conver any .mp4 extension files into .mp3 extension files. The function will
check for .mp4 extension files in the directory that the file was downloaded in. Use this for audio files.'''

precaution = '''Please make sure to fill the search box, as well select a directory to download. Unless 
those two conditions are met, the downloader will not download to prevent any 
inconviniences. By default, the app will start in the current working directory. Make sure to 
shift focus elsewhere, if needed.'''


#Py Simple Gui

sg.theme('DarkAmber')
layout = [
    [sg.Text('Search for video: '),sg.Input(key="Input"), sg.Button('Search')],
    [sg.Text('Browse directory:'), sg.Input(key="dir"), sg.FolderBrowse(initial_folder=os.getcwd(),change_submits=True, key="folder")],
    [sg.Text(f'{precaution}')],
    [sg.Radio(group_id=1,  text='Audio'), sg.Radio(group_id=1, text='Video')],
    [sg.Radio(group_id=2, text='240p'), sg.Radio(group_id=2, text='360p'), sg.Radio(group_id=2, text='480p'), sg.Radio(group_id=2, text='720p')],
    [sg.Button('Download', tooltip=dl_tp), sg.Button('Convert', tooltip=cv_tp), sg.Text('Ready: X', key="status")],
]

window = sg.Window("Music downloader", layout)
        
#Back End-----------------------

def search(strng): #Fetch link
    os.system('cls')
    global title 
    global yt_link
    #search_query = (input("Search for a video :  ")) -> depreciated
    try:
        search_result = YoutubeSearch(str(strng), max_results = 1).to_dict()
        for results in search_result:
            for k,v in results.items():
                if k == 'url_suffix':
                    yt_link = (prefix_link+v)
                if k == 'title':
                    title = v
        window['status'].update("Ready: ✓")
    except:
        print ("put something in the search field!")


def download(media_format, dirc): #Fetch video
    try:
        yt = YouTube(yt_link, on_progress_callback = progress_Check)
        yt_video = yt.streams.filter(only_audio=media_format, adaptive= True).first()
        yt_video.download(dirc)
        print("-> Download complete. Compiling into mp3...")
    except:
        pass

def progress_Check(chunk, file_handle, remaining): #check download progress
    sys.stdout.write(f'Downloading now: {title}\n')
    sys.stdout.write(f'Megabytes remaining: {round(remaining / 1000000, 2)} MB')
    os.system('cls')
    

def convert_to_mp3(dirc): #convert from mp4 to mp3 for groove/etc
    print("Finding file...")
    try:
        os.chdir(dirc) #permanently change dir to temp folder
        for files in os.walk(dirc):
                for filedir in files:
                    for mp4 in filedir:
                        if mp4.endswith('.mp4'): #verify file is actually of .mp4 extension
                            mp4file = mp4
                            print(f"\n--\nFound {mp4file}.")
                            audioclip = movpy.AudioFileClip(mp4file) #select audio file 
                            audioclip.write_audiofile(f"{mp4file[0:-4]}.mp3") 
                            audioclip.close() #write audio file as mp3 with the same name, and remove the '.mp4' section
                            print("\nDeleting the old file..")
                            os.remove(mp4file) #Remove old .mp4 file
                            print("\n--\nAll done! Exiting program if no more mp4 files found.")
                            time.sleep(1)
    except:
        print('no .mp4 file found.  ')
        pass

#Front End-----------------------

while True:
    event, values = window.read()
    backup_location = (os.getcwd()+'/tmp/')
    work_dir = values['folder']
    
    # defines tmp dir
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    #Search logic and debugging
    elif event == 'Search':
        try:
            search(values['Input'])
            print(title)
            print(work_dir)
            print(values['folder'])

        except:
            pass


    #Download logic -> needs to be completed to allow video/audio downlink
    elif event == 'Download':
        
        if work_dir == 0:
            window['status'].update('Set download location!')
        else:
            window['status'].update('Downloading...')

        #checks if dl location is :///. if positive then put it to :///tmp/
        
        download(True, work_dir)

    #Coversion logic -> should put this into audio.get() section

    elif event == 'Convert':
        convert_to_mp3(work_dir)
    

window.close()
    


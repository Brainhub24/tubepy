from pytube import YouTube
from ffmpeg import FFmpeg, Progress, ffmpeg
from lang import read_config_file, progressive_vtags, clean_filename, error_message
import time
import subprocess
import os

# try to read from config.json file where to store the downloaded video
video_res = progressive_vtags.get("720p")
audio_fq:int = 140
current_time = time.time()

location = read_config_file()
preferred_location = location["download_location"]

def quick_download(youtube_url):
    youtube_file = YouTube(youtube_url) 
    youtube_file.streams.get_highest_resolution().download(preferred_location)

def data_save_download(youtube_url):
    youtube_file = YouTube(youtube_url)
    youtube_file.streams.get_lowest_resolution().download(preferred_location)

def download(youtube_url):
    youtube_file = YouTube(youtube_url)
    
    # downloading progressive videos ( allowing users to choose theie desird resolutions)yo
    progressive_res = youtube_file.streams.get_by_itag(video_res)
    progressive_res.download(preferred_location) 
    
#? download audio files from youtube
def audio_download(youtube_url):
    '''
        added exception handler for convessionall purposes
    '''
    try:
        youtube_file = YouTube(youtube_url)
    except VideoUnavailable:
        print(error_message.get("VideoUnavailable"))
    else:
        audio_file = youtube_file.streams.get_by_itag(audio_fq)
        audio_file.download(preferred_location)
        

#? download Dynamic Adaptive Streaming over HTTP (DASH) and merge them with ffmpeg from youtube
def DASH_download(youtube_url):
    youtube_file = YouTube(youtube_url)
    
    try:        
        youtube_file.streams.filter(res='1080p', progressive= False).first().download(preferred_location, filename="video.mp4")
        youtube_file.streams.filter(abr='160kbps', progressive= False).first().download(preferred_location, filename="audio.mp3")
    except:
        youtube_file.streams.filter(res='720p', progressive= False).first().download(preferred_location, filename="video.mp4")
        youtube_file.streams.filter(abr='128kbps', progressive= False).first().download(preferred_location, filename="audio.mp3")
        
    # audio = FFmpeg().option("y").input(audio_url, 'audio.mp3')
    # video = FFmpeg().option("y").input(audio_url, 'video.mp4')
    # video = FFmpeg.input(video_url, 'video.mp4')
    # 
    # FFmpeg.output(audio, video, filename).run(overwrite_output=True)
    # # tracking the time
    # print('Time taken:'.format(time.time() - current_time))
    
    #? TRYING TO SELECT VIDEO AND AUDIO FILES FROM PREFERRED DIRECTORY
    #? KEPT GETTING FILE NOT FOUND ERROR WHEN TRYING TO MERGE THE VIDEO AND AUDIO FILES USING FFMP
    video = "video.mp4"
    audio = "audio.mp3"
    output_file = preferred_location + "\\\output.mp4"
    
    folder = []    
    for files in os.scandir(preferred_location):
        if files.name == video or files.name == audio:
            folder.append(files.path)
            print(files.path)
    print(folder)
    print(output_file)

    # subprocess.run(['ffmpeg', '-i', folder[1], '-i', folder[0], '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file])
       
#? download video files from youtube with other formats
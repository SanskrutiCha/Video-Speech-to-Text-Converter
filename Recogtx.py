import os
import speech_recognition as sr 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

video_files = [f for f in os.listdir() if f.endswith(".mp4")]

print("Select a video file:")
for i, video in enumerate(video_files, 1):
    print(f"{i}. {video}")

selected_video_index = int(input("Enter the number of the video file to process: ")) - 1

if 0 <= selected_video_index < len(video_files):
    selected_video = video_files[selected_video_index]

    num_seconds_video = 5*60

    l = list(range(0, num_seconds_video + 1,300 ))
    diz = {}

    for i in range(len(l)-1):
        ffmpeg_extract_subclip(selected_video, l[i] - 2 * (l[i] != 0), l[i+1], targetname=f"./cut/cut{i+1}.mp4")
        clip = mp.VideoFileClip(r"cut/cut{}.mp4".format(i+1))
        clip.audio.write_audiofile(r"converted/converted{}.wav".format(i+1))
        r = sr.Recognizer()
        audio = sr.AudioFile(f"./converted/converted{i+1}.wav")
        with audio as source:
            r.adjust_for_ambient_noise(source)  
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        diz[f'chunk{i+1}'] = result

    l_chunks = [diz[f'chunk{i+1}'] for i in range(len(diz))]
    text = '\n'.join(l_chunks)

    with open('recognized.txt', mode='w') as file:
        file.write("Recognized Speech:\n")
        file.write(text)
        print("Text has been Recognized....")

else:
    print("Invalid selection. Please choose a valid number.")
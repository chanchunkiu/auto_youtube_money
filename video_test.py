import whisper
import random
import pyttsx3
import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, TextClip
from script import generate_script
import datetime
import time

def generate_video(script_text):
    # Directory of reference videos
    normalized_script_text = script_text.strip().lower()
    if 'charismatic leader' in normalized_script_text:
        video_directory = "legend_video"
    else:
        video_directory = "video"
    # List of all reference videos
    print(f"Selected video directory: {video_directory}")
    video_files = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith('.mp4')]

    # Randomly select a video
    selected_video = random.choice(video_files)

    # Convert script into voiceover
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 160)
    engine.save_to_file(script_text, "voiceover.wav")
    engine.runAndWait()

    # Load the selected video
    video = VideoFileClip(selected_video)

    # Load voiceover
    voiceover = AudioFileClip("voiceover.wav")

    # Trim the video to the duration of the voiceover
    final_video = video.subclip(0, voiceover.duration)

    # Combine voiceover and original audio
    mixed_audio = CompositeAudioClip([final_video.audio, voiceover.set_start(0)])
    final_video = final_video.set_audio(mixed_audio)

    # Transcribe the audio and generate subtitles using Whisper
    model = whisper.load_model("base")
    result = model.transcribe("voiceover.wav")

    # Extract the transcript and create subtitles
    if 'segments' in result and result['segments']:
        subtitles = [(seg['start'], seg['end'], seg['text']) for seg in result['segments']]
    else:
        raise ValueError("Whisper transcription failed or returned unexpected result.")

        # Function to create visually appealing word-by-word subtitles
    def make_textclip(txt):
        return TextClip(
            txt,
            fontsize=100, 
            color='white', 
            stroke_color='black', 
            stroke_width=3, 
            font='Impact',  
            method='caption',  
            size=final_video.size 
        ).set_position(('center', 'bottom')) 
        
    def create_word_clips(text, start, end):
        words = text.split()
        duration = (end - start) / len(words) # Duration for each word
        speedfactor = 0.9
        word_duration = duration * speedfactor
        word_clips = []
        
        for i, word in enumerate(words):
            # Calculate the start and end time for each word
            word_start = start + (i * word_duration)
            word_end = word_start + word_duration
            
            # Create the TextClip for the word
            word_clip = make_textclip(word)
            word_clip = word_clip.set_start(word_start).set_end(word_end)
            word_clips.append(word_clip)
        
        return word_clips
    


    #create words clips
    subtitle_clips = []
    for (start, end, text) in subtitles:
        subtitle_clips.extend(create_word_clips(text, start, end))

    if not subtitle_clips:
        raise ValueError("No subtitles were created. Check the transcript.")
    #output directory
    output_directory = "output_videos"
    os.makedirs(output_directory, exist_ok=True)


    # combine the video with the subtitles
    final_video_with_subtitles = CompositeVideoClip([final_video] + subtitle_clips, size=final_video.size)
    
    
    #create file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"finalvideo{timestamp}.mp4"

    #finalise and render the video
    final_video_with_subtitles.write_videofile(
        os.path.join(output_directory, output_file_name),  # save to output
        codec="libx264", audio_codec="aac", fps=final_video.fps
    )

def main():
    max_videos = 2  # Set the maximum number of videos to generate
    video_count = 0  # Initialize a counter for the number of videos generated

    while video_count < max_videos:
        try:
            script_text = generate_script()  
            generate_video(script_text)  
            video_count += 1 
            print(f"Generated video {video_count}/{max_videos}") 
            time.sleep(60)  
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    print("Video generation of 10 complete.")



if __name__ == "__main__":
    main()
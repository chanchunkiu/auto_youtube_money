# Automate the generation of YouTube Shorts

Description of project:
It automates the process of generating videos by using AI and Python. It can shorten the time to create a video by just running the code.
The code can automatically generate 10 videos at a time.

tools used: moviepy, ppyt,s pyttsx3 whisper, Google generative AI

## How does it work?
1. Clone the files
2. Build a virtual environment
3. Install libraries used in requirements.txt  #pip install -r requirements.txt
4. Prepare short videos you would like to use and save them in the video file
5. Run video_final.py
6. Check the output folder for the generated video


## System Design
1. Prompt → AI generates video script
2.  AI voice synthesises narration from the script
3.  Subtitles are generated from the script
4.  Assests(voice, subtitles, video) are merged in a single viedo 


![image](https://github.com/user-attachments/assets/4945e742-ab68-4c6e-9f8d-acd001f65919)
You can see that the script and video are generated.


Upload the files to YouTube
![image](https://github.com/user-attachments/assets/e9b5a2da-8244-4b60-a60b-1599e176b84d)

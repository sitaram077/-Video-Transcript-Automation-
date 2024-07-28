import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from apscheduler.schedulers.blocking import BlockingScheduler


# Function to convert video to audio
def video_to_audio(video_path, audio_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
        video_clip.close()
        audio_clip.close()
        print("Audio extraction complete.")
    except Exception as e:
        print(f"Error in video to audio conversion: {e}")


# Function to convert audio to text
def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_file(audio_path)
        audio.export("temp.wav", format="wav")

        audio_file = sr.AudioFile("temp.wav")
        with audio_file as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        os.remove("temp.wav")
        return text
    except Exception as e:
        print(f"Error in audio to text conversion: {e}")
        return ""


# Main function to generate transcript
def generate_transcript(video_path, transcript_path):
    audio_path = "temp_audio.wav"
    video_to_audio(video_path, audio_path)
    transcript = audio_to_text(audio_path)

    if transcript:
        try:
            with open(transcript_path, 'w') as file:
                file.write(transcript)
            print(f"Transcript saved to {transcript_path}")
        except Exception as e:
            print(f"Error in saving transcript: {e}")

    try:
        os.remove(audio_path)
    except Exception as e:
        print(f"Error in removing temporary audio file: {e}")


# Scheduler function to automate the process
def scheduled_task(video_path, transcript_path):
    print("Starting scheduled task...")
    generate_transcript(video_path, transcript_path)
    print("Scheduled task completed.")


# Example usage
video_path = "videoplayback (2).mp4"
transcript_path = "transcript.txt"

# Schedule the task to run every day at a specific time
scheduler = BlockingScheduler()
scheduler.add_job(scheduled_task, 'interval', args=[video_path, transcript_path], hours=24)  # Runs every 24 hours
scheduler.start()

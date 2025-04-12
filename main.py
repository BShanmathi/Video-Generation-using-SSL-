import os
import requests
import google.generativeai as genai
from serpapi import GoogleSearch
from gtts import gTTS
from moviepy import *
import random

# ==== 🔑 API KEYS ====
GEMINI_API_KEY = "AIzaSyAR7QyO1zIYOWqoFnmXdhXhpWul5SoI4gM"
SERP_API_KEY = "b1deef23d2c0a75a0acb88c9b7e31e1dc3ea1ba2eaa3a96e0ebf7b2f1aefba64"  # From you

# ==== 🎯 INIT GEMINI ====
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# ==== 📜 GEMINI: GET ANSWER ====
def generate_answer(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None

# ==== 🖼️ SERPAPI: SSL Images ====
def fetch_ssl_images(query, max_images=5):
    print("🖼️ Fetching SSL images with fallback and retries...")
    try:
        search = GoogleSearch({
            "q": query,
            "tbm": "isch",
            "ijn": "0",
            "api_key": SERP_API_KEY
        })
        results = search.get_dict()
        image_results = results.get("images_results", [])

        image_urls = [
            img["original"] for img in image_results if img["original"].startswith("https://")
        ]

        if not image_urls:
            print("⚠️ No HTTPS images found. Falling back to HTTP images...")
            image_urls = [
                img["original"] for img in image_results if img["original"].startswith("http")
            ]

        image_paths = []
        for i, url in enumerate(image_urls[:max_images]):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    filename = f"image_{i}.jpg"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    image_paths.append(filename)
            except Exception:
                continue

        # ✅ Backup logic
        if not image_paths:
            print("❌ No clean images saved. Using backup stock images...")
            backup_urls = [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Mussolini_bundled.jpg/640px-Mussolini_bundled.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/4/4a/Mussolini_with_flag.jpg"
            ]
            for i, url in enumerate(backup_urls):
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        filename = f"backup_{i}.jpg"
                        with open(filename, "wb") as f:
                            f.write(response.content)
                        image_paths.append(filename)
                except Exception:
                    continue

        if not image_paths:
            print("🛑 Total failure. Using a local fallback image...")
            local = "local_fallback.jpg"
            with open(local, "wb") as f:
                f.write(requests.get("https://placekitten.com/800/600").content)
            image_paths = [local]

        return image_paths

    except Exception as e:
        print(f"⚠️ Error in image fetching: {e}")
        return []

# ==== 🔊 AUDIO GENERATION ====
def generate_audio(text, filename="output_audio.mp3"):
    tts = gTTS(text=text)
    tts.save(filename)
    return filename

# ==== 🎥 VIDEO CREATION ====
def create_video(images, audio, output="final_video.mp4"):
    clips = [ImageClip(img).set_duration(3).resize(height=720) for img in images]
    video = concatenate_videoclips(clips, method="compose")

    # Load and adjust audio
    audio_clip = AudioFileClip(audio)
    if video.duration > audio_clip.duration:
        audio_clip = audio_clip.audio_loop(duration=video.duration)
    else:
        video = video.subclip(0, audio_clip.duration)

    video = video.set_audio(audio_clip)

    # Subtitle overlay
    txt_clip = TextClip("Powered by Gemini + SerpAPI", fontsize=30, color='white')
    txt_clip = txt_clip.set_pos('bottom').set_duration(video.duration)

    final = CompositeVideoClip([video, txt_clip])
    final.write_videofile(output, fps=24)

# ==== 🚀 MAIN ====
def main():
    prompt = input("❓ Ask a question: ")
    answer = generate_answer(prompt)
    if not answer:
        print("🧠 Answer: Sorry, I couldn't generate an answer.")
        return

    print("🧠 Answer:", answer)

    print("🖼️ Fetching SSL images with fallback and retries...")
    images = fetch_ssl_images(prompt)
    if not images:
        print("❌ Image fetch failed. Exiting...")
        return

    audio_path = generate_audio(answer)
    create_video(images, audio_path)
    print("✅ Final video created!")

if __name__ == "__main__":
    main()

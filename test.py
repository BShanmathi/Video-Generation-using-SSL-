import os
print(os.path.exists("C:/Users/tssum/PycharmProjects/PythonProject/agriculture_dataset/crop_images"))
print(os.listdir("C:/Users/tssum/PycharmProjects/PythonProject/agriculture_dataset/crop_images"))

import cv2
import os


def generate_video(image_folder, output_video_path, fps=2):
    images = sorted([img for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))])

    if not images:
        print(f"❌ No images found in {image_folder}. Exiting...")
        return

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        if frame is not None:
            video.write(frame)
        else:
            print(f"⚠️ Warning: Unable to read {img_path}")

    video.release()
    print(f"✅ Video saved: {output_video_path}")


# Run it
generate_video(r"C:/Users/tssum/PycharmProjects/PythonProject/agriculture_dataset/crop_images", "video.mp4")


image_folder = r"C:/Users/tssum/PycharmProjects/PythonProject/agriculture_dataset/crop_images"

if os.path.exists(image_folder):
    files = os.listdir(image_folder)
    print("All files in folder:", files)

    # Get file extensions
    extensions = set(os.path.splitext(f)[1] for f in files)
    print("File extensions found:", extensions)
else:
    print("❌ Folder not found!")


image_folder = r"C:/Users/tssum/PycharmProjects/PythonProject/agriculture_dataset/crop_images/jute"
valid_extensions = {".jpg", ".jpeg", ".png"}  # Ensure correct extensions

files = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in valid_extensions]

print("✅ Images found:", files)  # Debugging output

image_folder = "C:/Users/tssum/PycharmProjects/PythonProject/agriculture_dataset/crop_images"
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))])
print("Found Images:", image_files)

print(os.path.exists("narration.mp3"))  # Should print True
import os
print(os.path.exists("video.mp4"))  # Should print True
print(os.path.exists("narration.mp3"))  # Should print True



audio_path = "narration.mp3"

if os.path.exists(audio_path):
    print("✅ narration.mp3 exists.")
else:
    print("❌ narration.mp3 is missing!")
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyCbbIILmbkjRvZQzg6Fm5V6Eqhcvc96f8I")




models = genai.list_models()
for m in models:
    print(m.name)

# Load the correct model
model = genai.GenerativeModel("gemini-pro")  # Ensure this is correct!

def get_ai_answer(question):
    """Generate an AI-based answer using Gemini API."""
    response = model.generate_content(question)
    return response.text.strip() if response else "No response."

# Example usage
user_question = "What is AI?"
answer = get_ai_answer(user_question)
print("💡 AI Answer:", answer)

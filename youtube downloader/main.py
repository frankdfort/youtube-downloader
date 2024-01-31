from pytube import YouTube
import os

# Function to convert bytes to Megabytes
def bytes_to_mb(bytes):
  return bytes / 1024 ** 2

# Get video ID from user
video_id = input("Enter YouTube video ID: ")

# Create YouTube object
try:
  youtube_obj = YouTube(f"https://www.youtube.com/watch?v={video_id}")
except Exception as e:
  print(f"Error: {e}")
  exit()

# Define available resolutions list
available_resolutions = {
  "240p": {
    "itag": None,
    "size_mb": 0,
  },
  "360p": {
    "itag": None,
    "size_mb": 0,
  },
  "480p": {
    "itag": None,
    "size_mb": 0,
  },
  "720p": {
    "itag": None,
    "size_mb": 0,
  },
  "1080p": {
    "itag": None,
    "size_mb": 0,
  },
}

# Fill available resolutions dictionary with actual data
for stream in youtube_obj.streams:
  resolution = stream.resolution
  size_mb = bytes_to_mb(stream.filesize)
  if resolution in available_resolutions:
    available_resolutions[resolution]["itag"] = stream.itag
    available_resolutions[resolution]["size_mb"] = size_mb

# Show resolutions and sizes as a menu
print("Available Resolutions:")
for resolution, data in available_resolutions.items():
  if data["itag"]:
    print(f"{resolution} ({data['size_mb']:.2f} MB)")

# Get user choice for resolution
user_resolution_choice = input("Choose your desired resolution: ")

# Check if chosen resolution is valid
if user_resolution_choice not in available_resolutions:
  print(f"Invalid resolution choice: '{user_resolution_choice}'")
  exit()

# Download video based on chosen resolution
chosen_itag = available_resolutions[user_resolution_choice]["itag"]
try:
  stream = youtube_obj.streams.get_by_itag(chosen_itag)
  filename = f"{youtube_obj.title}.mp4"
  stream.download(filename=filename)
  print(f"Downloaded video '{filename}' successfully!")
except Exception as e:
  print(f"Error: {e}")

# Show downloaded file size
downloaded_file = open(filename, "rb")
file_size_mb = bytes_to_mb(os.path.getsize(filename))
downloaded_file.close()
print(f"Downloaded file size: {file_size_mb:.2f} MB")


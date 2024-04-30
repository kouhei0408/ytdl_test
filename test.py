from flask import Flask, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/download', methods=['GET'])
def download():
    youtube_url = request.args.get('youtubeUrl')
    download_location = request.args.get('downloadLocation')
    audio_only = request.args.get('audioOnly', type=bool)

    try:
        youtube = YouTube(youtube_url)
        if audio_only:
            stream = youtube.streams.filter(only_audio=True, subtype='mp4').first()
        else:
            stream = youtube.streams.filter(subtype='mp4').first()

        if stream:
            if not os.path.exists(download_location):
                os.makedirs(download_location)
            file_path = os.path.join(download_location, stream.default_filename)
            stream.download(output_path=download_location)
            return send_file(file_path, as_attachment=True)
        else:
            return "Error: No suitable stream found for download."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)

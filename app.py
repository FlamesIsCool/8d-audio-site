from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import os, math

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['audio']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    audio = AudioSegment.from_file(filepath)
    interval = 50
    total_chunks = math.floor(len(audio) / interval)

    new_audio = AudioSegment.silent(duration=0)
    for i in range(total_chunks):
        chunk = audio[i * interval:(i + 1) * interval]
        pan = math.sin(i * 0.1)
        new_audio += chunk.pan(pan)

    output_path = os.path.join(OUTPUT_FOLDER, f"8d_{filename}")
    try:
        new_audio.export(output_path, format="mp3")
    except Exception as e:
        return f"Export failed. Make sure ffmpeg is available. Error: {e}"

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

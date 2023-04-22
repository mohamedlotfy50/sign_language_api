import os
import tensorflow as tf
import speech_recognition as sr
from flask import Flask,request,jsonify

app = Flask(__name__)

# Load the TensorFlow model
model = tf.keras.models.load_model('ar_translator')

@app.route("/speech_to_sign",methods=['POST'])

def speech_to_sign():

    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})
    
    # Get the file from the request
    file = request.files['file']

    if file.filename.split('.')[-1] != 'wav':
        return jsonify({'error': 'File must be a WAV file'})
    
    file.save(file.filename)

    r = sr.Recognizer()

    with sr.AudioFile(file) as source:
        audio_data = r.record(source)
    
    try:

        text = r.recognize_google(audio_data)

        return {'text': text}
    
    except sr.UnknownValueError:

        return {'error': 'Unable to recognize speech'}

if __name__ == "__main__":
  app.run()
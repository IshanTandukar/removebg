from flask import Flask, render_template, request, send_file, send_from_directory
from rembg import remove
from PIL import Image
import os

app=Flask(__name__)

upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    file = request.files["image"]

    input_path = os.path.join(upload_folder, file.filename)

    output_filename = f"output_{os.path.splitext(file.filename)[0]}.png"
    output_path = os.path.join(upload_folder, output_filename )
    
    file.save(input_path)

    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)

    # return send_file(output_path, as_attachment=True)
    return render_template(
        'result.html', 
        original=file.filename, 
        processed=output_filename
        )

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(upload_folder, filename)
    return send_file(path, as_attachment=True)

@app.route('/uploads/<filename>')
def static_uploads(filename):
    return send_from_directory(upload_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
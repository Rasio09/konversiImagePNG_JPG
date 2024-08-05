from flask import Flask, request, send_file, render_template
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_image():
    file = request.files['imageFile']
    format = request.form['format']
    quality = int(request.form.get('quality', 85))  # Default quality 85
    resolution = int(request.form.get('resolution', 100))  # Default resolution percentage
    
    image = Image.open(file.stream)
    
    # Konversi mode gambar untuk format JPEG
    if format == 'jpg':
        if image.mode == 'RGBA':
            image = image.convert('RGB')  # Konversi RGBA ke RGB
        format = 'JPEG'
    
    # Sesuaikan ukuran gambar sesuai resolusi
    if resolution != 100:
        width, height = image.size
        new_width = int(width * resolution / 100)
        new_height = int(height * resolution / 100)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format.upper(), quality=quality)
    img_byte_arr.seek(0)
    
    return send_file(
        img_byte_arr, 
        mimetype='image/' + format.lower(), 
        as_attachment=True, 
        download_name='converted_image.' + format.lower()
    )

if __name__ == '__main__':
    app.run(debug=True)

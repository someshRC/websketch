from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def cartoonize_image(image_path):
     img = cv2.imread(image_path)
     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     gray = cv2.medianBlur(gray, 5)
     edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
cv2.THRESH_BINARY, 9, 9)
     color = cv2.bilateralFilter(img, 9, 250, 250)
     cartoon = cv2.bitwise_and(color, color, mask=edges)
     output_path = os.path.join(PROCESSED_FOLDER, 'cartoon_' +
os.path.basename(image_path))
     cv2.imwrite(output_path, cartoon)
     return output_path

def sketch_image(image_path):
     img = cv2.imread(image_path)
     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     inverted = cv2.bitwise_not(gray)
     blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
     inverted_blurred = cv2.bitwise_not(blurred)
     sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
     output_path = os.path.join(PROCESSED_FOLDER, 'sketch_' +
os.path.basename(image_path))
     cv2.imwrite(output_path, sketch)
     return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
     if request.method == 'POST':
         file = request.files['file']
         action = request.form['action']
         if file:
             file_path = os.path.join(UPLOAD_FOLDER, file.filename)
             file.save(file_path)
             if action == 'Cartoonize':
                 processed_path = cartoonize_image(file_path)
             elif action == 'Sketch':
                 processed_path = sketch_image(file_path)
             return send_file(processed_path, mimetype='image/png',
as_attachment=True)
     return '''
     <!doctype html>
     <html>
     <head><title>Cartoonize or Sketch Image</title></head>
     <body>
         <h1>Upload an image to Cartoonize or Sketch</h1>
         <form method="post" enctype="multipart/form-data">
             <input type="file" name="file" required>
             <br><br>
             <button type="submit" name="action"
value="Cartoonize">Cartoonize</button>
             <button type="submit" name="action"
value="Sketch">Sketch</button>
         </form>
     </body>
     </html>
     '''

if __name__ == '__main__':
     app.run(debug=True)
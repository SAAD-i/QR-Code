from flask import Flask, render_template, request, send_from_directory, url_for
import qrcode
import os

app = Flask(__name__)

# Ensure the qrcodes directory exists
os.makedirs(os.path.join(app.static_folder, 'qrcodes'), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    url = request.form.get('url')
    if url:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        filename = f"{url.replace('/', '_')}.png"
        filepath = os.path.join(app.static_folder, 'qrcodes', filename)
        img.save(filepath)

        return render_template('index.html', qr_code=filename)
    return render_template('index.html')

@app.route('/qrcodes/<filename>')
def send_qr(filename):
    return send_from_directory(os.path.join(app.static_folder, 'qrcodes'), filename)

if __name__ == '__main__':
    app.run(debug=True)

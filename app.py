import logging
from flask import Flask, request, render_template_string, render_template, send_file, make_response
import qrcode, os, datetime
from uuid import uuid4
from PIL import Image, ImageDraw
from utils.api import make_api_request, upload_file_to_s3

app = Flask(__name__)

# request_url = 'https://voyager-q.onrender.com/'
s3_bucket='yminer-bk'
object_path='rss'

# Generate a QR code linking to the form
@app.route('/')
def home():
    os.makedirs("static", exist_ok=True)
    # # You could generate QR code on demand
    link = request.url_root + 'ask'
    # qr = qrcode.make(link)
    # # Save QR to serve as image
    # qr.save("static/qr.png")
    return render_template("start.html", link=link)

# Input form
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        data = request.form['feedback']
        res, err = make_api_request(data)
        if err:
            logging.error(f"Ask chat bot failed with error {err}")
            response = make_response("<h2>出了点问题，请稍后再试。如果问题持续，请联系管理员</h2>", 500)
            response.headers["X-Error-Message"] = str(err)
            return response
        # upload file to s3
        filename = f"rs-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}-{uuid4().hex[:8]}.txt"
        success = upload_file_to_s3(res, s3_bucket, f"{object_path}/{filename}")
        if success:
            logging.info("Upload successful!")
        else:
            logging.info("Upload failed.")
        return "<h2>正在制作中， 感谢参与!</h2>"
    
    return make_response(render_template("ask.html"), 200)


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = f'/yminer/{filename}'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return make_response("File not found", 404)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True, use_reloader=False)

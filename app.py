import logging
from flask import Flask, request, render_template_string, send_file
import qrcode, os, httpx, datetime
import openai
from PIL import Image, ImageDraw
from utils.api import make_api_request, upload_file_to_s3

app = Flask(__name__)
client = openai.OpenAI(
    timeout=60.0,
    base_url=os.getenv("OPENAI_API_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(verify=False)
)

s3_bucket='yminer-bk'
object_path='rss'

# Generate a QR code linking to the form
@app.route('/')
def home():
    os.makedirs("static", exist_ok=True)
    link = request.url_root + 'submit'
    qr = qrcode.make(link)
    qr.save("static/qr.png")  # Save QR to serve as image
    return f"""
    <h2>Scan the QR Code to Submit Feedback</h2>
    <img src="/static/qr.png">
    <p>Or open: <a href="{link}">{link}</a></p>
    """

# Input form
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    os.makedirs("/yminer", exist_ok=True)

    if request.method == 'POST':
        data = request.form['feedback']
        # TODO ask bot
        res = make_api_request(client, data)
        # You can upload file to a object storage as well
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"rs-{timestamp}.txt"
        success = upload_file_to_s3(res, s3_bucket, f"{object_path}/{filename}")
        if success:
            logging.info("Upload successful!")
        else:
            logging.info("Upload failed.")
        # with open(f"/yminer/{filename}", "a") as f:
        #     f.write(res + "\n")
        return "<h3>Thanks for your feedback!</h3>"
    
    return render_template_string("""
        <h2>Submit Feedback</h2>
        <form method="post">
            <textarea name="feedback" rows="4" cols="50" required></textarea><br>
            <input type="submit" value="Submit">
        </form>
    """)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = f'/yminer/{filename}'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

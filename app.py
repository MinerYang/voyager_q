from flask import Flask, request, render_template_string, redirect, url_for
import qrcode, os
from PIL import Image, ImageDraw

app = Flask(__name__)

# Generate a QR code linking to the form
@app.route('/')
def home():
    os.makedirs("static", exist_ok=True)
    use_reloader=False
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
    if request.method == 'POST':
        data = request.form['feedback']
        # You can save this to a file/database
        with open("submissions.txt", "a") as f:
            f.write(data + "\n")
        return "<h3>Thanks for your feedback!</h3>"
    
    return render_template_string("""
        <h2>Submit Feedback</h2>
        <form method="post">
            <textarea name="feedback" rows="4" cols="50" required></textarea><br>
            <input type="submit" value="Submit">
        </form>
    """)

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return "no image was sent"
    return "image was sent"


if __name__ == '__main__':
    app.run(debug=True)
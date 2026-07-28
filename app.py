from flask import Flask, render_template

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def home():
    return render_template('index.html')
def analyze():
    return "Route is working!"


if __name__ == '__main__':
    app.run(debug=True)
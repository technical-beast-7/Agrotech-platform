from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
import crops

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'nareshrko10'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commodity')
def commodity():
    return render_template('commodity.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/trends')
def trends():
    return render_template('trends.html')

@app.route('/crop/<name>')
def crop_info(name):
    try:
        crop_data = crops.crop(name.lower())
        return render_template('cindex.html', name=name, image=crop_data[0], 
                              states=crop_data[1], season=crop_data[2], export=crop_data[3])
    except Exception as e:
        print(f"Error in crop_info: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
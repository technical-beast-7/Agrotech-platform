from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib
from email.mime.text import MIMEText
from flask import jsonify
from waitress import serve
import json
from pymongo import MongoClient
from flask_pymongo import PyMongo
from datetime import datetime
import os
import json
from bson.objectid import ObjectId
from dotenv import load_dotenv
import crops
import folium
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client['FarmEz']

app = Flask(__name__)
app.secret_key = 'nareshrko10'
app.config["MONGO_URI"] = "mongodb://localhost:27017/farm_ez"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commodity')
def commodity():
    return render_template('commodity.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Email sending logic
        sender_email = "your_email@example.com"  # Replace with your email
        sender_password = "your_password"  # Replace with your email password
        receiver_email = "kirtanshah001@gmail.com"

        msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        msg['Subject'] = "New Contact Form Submission"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            flash('Your message has been sent to the developer!', 'success')
        except Exception as e:
            flash(f'Failed to send message. Error: {e}', 'danger')

    return redirect(url_for('contact'))

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

@app.route('/farmer')
def farmer():
    return render_template('findex.html')

@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        landsize = request.form.get('landsize')
        address = request.form.get('address')
        land_survey_no = request.form.get('Land_Survey_No')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        other_info = request.form.get('other-info')
        full_name = request.form.get('full-name')
        phone = request.form.get('phone')
        district = request.form.get('district')
        taluka = request.form.get('taluka')
        taluka = request.form.get('taluka')

        # Handle file upload
        land_photo = request.files.get('land_photo')
        if land_photo:
            # Save the file to a designated folder or upload to a cloud storage
            # For simplicity, let's save it to a 'uploads' folder
            upload_folder = os.path.join(app.root_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(land_photo.filename)
            file_path = os.path.join(upload_folder, filename)
            land_photo.save(file_path)
        else:
            filename = None

        # Insert data into MongoDB
        try:
            user_data = {
                'full-name': full_name,
                'email': email,
                'phone': phone,
                'landsize': landsize,
                'address': address,
                'Land_Survey_No': land_survey_no,
                'latitude': float(latitude) if latitude else None,
                'longitude': float(longitude) if longitude else None,
                'other-info': other_info,
                'district': district,
                'taluka': taluka,
                'land_photo': filename  # Store the filename in the database
            }
            mongo.db.users.insert_one(user_data)
            return redirect(url_for('farmer')) # Redirect to farmer page or a success page
        except Exception as e:
            print(f"Error inserting data: {e}")
            return "Error registering land", 500
    return redirect(url_for('farmer'))

@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        district = request.form.get('district')
        # Query the MongoDB database for the user information
        # Fetch locations from the database based on the selected district
        query = {'district': district, 'latitude': {'$exists': True}, 'longitude': {'$exists': True}}
        if taluka:
            query['taluka'] = taluka
        locations = list(mongo.db.users.find(query))

        if not locations:
            return render_template('mindex.html', district=district, map_html="<p>No farmers found in this district.</p>")

        # Create a Folium map centered on the first location in the list
        map = folium.Map(location=[locations[0]['latitude'], locations[0]['longitude']], zoom_start=10)

        tile_layer = folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            overlay=False,
            control=True
        ).add_to(map)

        # Add markers for all the locations in the list
        for location in locations:
            # Query the MongoDB database for the user information
            user_info = mongo.db.users.find_one({'district': district, 'taluka': taluka, 'latitude': location['latitude'], 'longitude': location['longitude']})

            # Create the URL for the farmer's profile using the farmer's ID
            profile_url = url_for('farmer_profile', farmer_id = str(user_info['_id']))

            # Modify the popup HTML to include the "More Info" link leading to the farmer's profile
            popup_html = f"""
            <div style="width: 300px;">
                <h3 style="margin: 0; padding: 10px; background-color: #00704A; color: #FFF; text-align: center; font-size: 20px;">
                    {user_info['full-name']}
                </h3>
                <div style="padding: 10px;">
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Phone: {user_info['phone']}</p>
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Land Size: {user_info['landsize']} acres</p>
                    <p style="margin: 0; margin-bottom: 5px; font-size: 16px;">Land Survey Number: {user_info['Land_Survey_No']}</p>
                    <div style="text-align: center;">
                        <a href='{profile_url}' target='_blank' style="color: #002F6C; text-decoration: none; font-size: 13px; display: inline-block;">More Info</a>
                    </div>
                </div>
            </div>
            """  # Add a marker with the pop-up to the map
            folium.Marker(location=[location['latitude'], location['longitude']], popup=popup_html).add_to(map)

        # Convert the map to HTML and pass it to the template
        map_html = map._repr_html_()
        return render_template('mindex.html', district=district, taluka=taluka, map_html=map_html)
    return render_template('mindex.html')

@app.route('/farmer_profile/<farmer_id>')
def farmer_profile(farmer_id):
    # This is a placeholder. In a real application, you would fetch farmer details
    # from the database using the farmer_id and render a dedicated profile page.
    return f"<h1>Farmer Profile for ID: {farmer_id}</h1><p>Details coming soon!</p>"

@app.route('/crop')
def crop():
    return render_template('cindex.html')

# Buy and Sell routes
@app.route('/buy', methods=['GET', 'POST'])
def buy():
    crops_collection = db['trades']
    try:
        all_crops = list(crops_collection.find({}))
        # Adjust prices to be per kg and within the 20-100 range
        # Realistic price ranges for different types of crops (per kg)
        crop_prices = {
            'vegetables': [250, 300, 350, 400, 450, 500],
            'fruits': [400, 500, 550, 600],
            'grains': [200, 250, 300, 350],
            'pulses': [300, 350, 400, 450],
            'spices': [500, 550, 600]
        }
        
        if 'crop_prices_session' not in session:
            session['crop_prices_session'] = {}

        for crop in all_crops:
            if 'price_per_10kg' in crop:
                crop_name = crop.get('name')
                if crop_name not in session['crop_prices_session']:
                    # Assign specific fixed prices to crops
                    fixed_prices = {
                        'Turnip': 25,
                        'Lady finger': 30,
                        'Brocolli': 50,
                        'Tomatoes': 40,
                        'Cabbage': 35,
                        'Spinach': 25
                    }
                    if crop_name in fixed_prices:
                        session['crop_prices_session'][crop_name] = fixed_prices[crop_name] * 10
                    else:
                        # Fallback to the first price in the crop_prices list if crop not in fixed_prices
                        session['crop_prices_session'][crop_name] = crop_prices.get(crop.get('type', 'grains'), [200])[0]
                crop['price_per_10kg'] = session['crop_prices_session'][crop_name]
            else:
                print(f"Warning: 'price_per_10kg' key not found for crop {crop.get('name', 'Unknown')}")
        print(f"All crops data: {all_crops}") # Temporary print for debugging
        return render_template('buy.html', crops=all_crops)
    except Exception as e:
        print(f"Error in buy route: {e}")
        import traceback
        traceback.print_exc()
        return "An error occurred while loading crops.", 500

@app.route('/buy_crops', methods=['POST'])
def buy_crops():
    # Process search form
    return redirect(url_for('buy'))

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        # Process the form data here
        return redirect(url_for('index'))
    return render_template('sell.html')

# Chatbot route
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Shopping and product routes
@app.route('/shopping_list', methods=['GET', 'POST'])
def shopping_list():
    if 'cart' not in session:
        session['cart'] = []
    
    if request.method == 'POST':
        try:
            product_id = request.form.get('product_id')
            product_name = request.form.get('product_name', 'Product')
            price_str = request.form.get('price', '0')
            try:
                price = float(price_str)
            except ValueError:
                # Handle the case where price_str is not a valid float (e.g., empty string)
                price = 0.0  # Default to 0.0 or handle as an error

            quantity = int(request.form.get('quantity', 1))
            print(f"Incoming data: {request.form}")
            print(f"Incoming data: ID={product_id}, Name={product_name}, Price={price}, Quantity={quantity})")
            print(f"Cart before modification: {session['cart']}")
            
            # Check if product already in cart
            found = False
            for item in session['cart']:
                if item['id'] == product_id:
                    print(f"Found existing item {item['id']}. Updating quantity from {item['quantity']} to {item['quantity'] + quantity}")
                    item['quantity'] += quantity
                    found = True
                    break
                    
            if not found:
                session['cart'].append({
                    'id': product_id,
                    'name': product_name,
                    'price': price,
                    'quantity': quantity,
                    'crop_image': request.form.get('crop_image', 'img.jpg') # Get image from form, default to img.jpg
                })
                print(f"Added new item: {product_name} (ID: {product_id}, Quantity: {quantity})")
            
            try:
                session.modified = True
            except OSError as e:
                print(f"OSError during session modification: {e}")
            print(f"Cart after modification: {session['cart']}")
            return jsonify({'success': True, 'message': 'Item added to cart!'})
        except Exception as e:
            print(f"Error in shopping_list: {e}")
            return jsonify({'success': False, 'message': str(e)})
    
    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in session['cart'])
    
    return render_template('shopping_list.html', cart_items=session['cart'], total_price=total_price)

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    session.modified = True
    return redirect(url_for('shopping_list'))

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    product_id = request.form.get('product_id')
    change = int(request.form.get('change', 0))
    
    if 'cart' in session:
        for item in session['cart']:
            if item['id'] == product_id:
                item['quantity'] = max(1, item['quantity'] + change)  # Ensure quantity is at least 1
                break
        
        session.modified = True
    
    return {'success': True}

@app.route('/product_profile')
def product_profile():
    return render_template('product_profile.html')

@app.route('/productdetail')
def productdetail():
    product_id = request.args.get('id')
    try:
        product = db.trades.find_one({'_id': ObjectId(product_id)}) # Fetch product from db
    except Exception as e:
        print(f"Error converting product_id to ObjectId: {e}")
        return "Invalid Product ID", 400
    if product:
        return render_template('productdetail.html', product=product, product_id=product_id)
    else:
        return "Product not found", 404

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/crop/<name>')
def crop_info(name):
    try:
        crop_data = crops.crop(name.lower())
        return render_template('cindex.html', name=name, image=crop_data[0], 
                              states=crop_data[1], season=crop_data[2], export=crop_data[3])
    except Exception as e:
        print(f"Error in crop_info: {e}")
        return redirect(url_for('index'))
        
# Language routes
@app.route('/hi')
def index_hi():
    return render_template('index_hi.html')

@app.route('/ma')
def index_ma():
    return render_template('index_ma.html')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)

# Additional language-specific routes
@app.route('/hiabout')
def about_hi():
    return render_template('aboutus_hi.html')

@app.route('/maabout')
def about_ma():
    return render_template('aboutus_ma.html')

@app.route('/hicontact')
def contact_hi():
    return render_template('contact_hi.html')

@app.route('/macontact')
def contact_ma():
    return render_template('contact_ma.html')

@app.route('/hisignin')
def signin_hi():
    return render_template('signin_hi.html')

@app.route('/masignin')
def signin_ma():
    return render_template('signin_ma.html')

@app.route('/hisignup')
def signup_hi():
    return render_template('signup_hi.html')

@app.route('/masignup')
def signup_ma():
    return render_template('signup_ma.html')

from waitress import serve

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
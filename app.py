from flask import Flask, render_template, request

app = Flask(__name__)

# Sample Data for Booking Options
TRANSPORT_OPTIONS = {
    'train': ['Express Express - $50', 'Superfast Express - $80', 'Bullet Train - $120'],
    'flight': ['Economy Flight - $200', 'Business Flight - $500', 'First Class Flight - $900'],
    'bus': ['AC Sleeper Bus - $30', 'Volvo Seater Bus - $25', 'Express Bus - $15']
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book/<category>', methods=['GET', 'POST'])
def book_ticket(category):
    category_name = category.capitalize()
    options = TRANSPORT_OPTIONS.get(category.lower(), [])
    booking_success = None
    
    if request.method == 'POST':
        passenger_name = request.form.get('passenger_name')
        selected_option = request.form.get('selected_option')
        booking_date = request.form.get('booking_date')
        
        booking_success = {
            'name': passenger_name,
            'category': category_name,
            'option': selected_option,
            'date': booking_date
        }

    return render_template('booking.html', category=category_name, options=options, success=booking_success)

if __name__ == '__main__':
    app.run(debug=True)
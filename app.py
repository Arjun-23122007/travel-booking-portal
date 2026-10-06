from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
# Secret key is required for session management and flash messages
app.secret_key = 'super_secret_travel_key_123'

# Temporary in-memory storage for registered users (username: password)
users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('register'))

        if username in users:
            flash('Username already exists! Please choose another.', 'danger')
            return redirect(url_for('register'))
            
        users[username] = password
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username] == password:
            session['user'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user' not in session:
        flash('Please log in to book a ticket.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        passenger_name = request.form.get('name')
        travel_mode = request.form.get('mode')
        from_loc = request.form.get('from')
        to_loc = request.form.get('to')
        date = request.form.get('date')
        
        # Validating input
        if not all([passenger_name, travel_mode, from_loc, to_loc, date]):
            flash('Please fill in all fields before submitting.', 'danger')
            return redirect(url_for('book'))

        booking = {
            'name': passenger_name,
            'mode': travel_mode,
            'from': from_loc,
            'to': to_loc,
            'date': date,
            'status': 'Confirmed'
        }
        
        if 'bookings' not in session:
            session['bookings'] = []
            
        # Updating session list properly
        bookings = session['bookings']
        bookings.append(booking)
        session['bookings'] = bookings
        
        flash('Ticket booked successfully!', 'success')
        return redirect(url_for('my_bookings'))

    return render_template('booking.html')

@app.route('/my-bookings')
def my_bookings():
    if 'user' not in session:
        flash('Please log in to view your bookings.', 'warning')
        return redirect(url_for('login'))
        
    user_bookings = session.get('bookings', [])
    return render_template('my_bookings.html', bookings=user_bookings)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'utsav1234'

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'utsav'
app.config['MYSQL_DB'] = 'movie_booking'
mysql = MySQL(app)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, name, email FROM user WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        user = User()
        user.id, user.name, user.email = row
        return user
    return None

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        pw = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, password FROM user WHERE email=%s", (email,))
        row = cur.fetchone()
        cur.close()
        if row and check_password_hash(row[1], pw):
            user = User()
            user.id = row[0]
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=16)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (name,email,password) VALUES (%s,%s,%s)", (name,email,pw))
        mysql.connection.commit()
        cur.close()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Home page: only 5 movies
@app.route('/')
@login_required
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT movie_id, title FROM movie LIMIT 5")
    movies = cur.fetchall()
    cur.close()
    return render_template('index.html', movies=movies)

# All movies page
@app.route('/movies')
@login_required
def all_movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT movie_id, title FROM movie")
    movies = cur.fetchall()
    cur.close()
    return render_template('all_movies.html', movies=movies)

@app.route('/search', methods=['POST'])
@login_required
def search():
    q = request.form['query']
    cur = mysql.connection.cursor()
    cur.execute("SELECT movie_id, title FROM movie WHERE title LIKE %s OR genre LIKE %s", 
                (f"%{q}%", f"%{q}%"))
    movies = cur.fetchall()
    cur.close()
    flash(f"Found {len(movies)} result(s) for '{q}'", 'success')
    return render_template('index.html', movies=movies)

@app.route('/book/<int:movie_id>', methods=['GET','POST'])
@login_required
def booking(movie_id):
    cur = mysql.connection.cursor()
    if request.method=='POST':
        show_id = request.form['show_id']
        seat_id = request.form['seat_id']
        cur.execute("INSERT INTO booking (user_id, show_id, seat_id) VALUES (%s,%s,%s)",
                    (current_user.id, show_id, seat_id))
        mysql.connection.commit()
        booking_id = cur.lastrowid
        cur.execute("UPDATE seat SET is_booked=TRUE WHERE seat_id=%s", (seat_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('payment', booking_id=booking_id))
    # GET
    cur.execute("SELECT show_id, show_date, start_time, end_time FROM showtime WHERE movie_id=%s", (movie_id,))
    showtimes = cur.fetchall()
    cur.execute("SELECT seat_id, seat_number FROM seat WHERE is_booked=FALSE")
    seats = cur.fetchall()
    cur.close()
    return render_template('booking.html', showtimes=showtimes, seats=seats)

@app.route('/payment/<int:booking_id>', methods=['GET','POST'])
@login_required
def payment(booking_id):
    if request.method == 'POST':
        amount = request.form['amount']
        method = request.form['payment_method']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO payment (booking_id, amount, payment_method, payment_status) "
                "VALUES (%s, %s, %s, 'Success')",
                (booking_id, amount, method)
            )
            mysql.connection.commit()
            cur.close()
            flash('Payment successful! 🎉', 'success')
        except Exception as e:
            flash('Payment failed, please try again.', 'error')
            app.logger.error(f"Payment error: {e}")
        return redirect(url_for('index'))

    # GET = show the payment form only
    return render_template('payment.html', booking_id=booking_id)

@app.route('/confirmation')
@login_required
def confirmation():
    # not used directly
    return redirect(url_for('index'))

@app.route('/payment_history')
@login_required
def payment_history():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT
            p.payment_id,
            m.title,
            p.amount,
            p.payment_status,
            p.payment_date
        FROM payment p
        JOIN booking b ON p.booking_id = b.booking_id
        JOIN showtime s ON b.show_id = s.show_id
        JOIN movie m    ON s.movie_id = m.movie_id
        WHERE b.user_id = %s
        ORDER BY p.payment_date DESC
    """, (current_user.id,))
    payments = cur.fetchall()
    cur.close()
    return render_template('payment_history.html', payments=payments)

@app.route('/cancel_booking', methods=['POST'])
@login_required
def cancel_booking():
    bid = request.form['booking_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT seat_id FROM booking WHERE booking_id=%s", (bid,))
    seat = cur.fetchone()[0]
    cur.execute("DELETE FROM booking WHERE booking_id=%s", (bid,))
    mysql.connection.commit()
    cur.execute("UPDATE seat SET is_booked=FALSE WHERE seat_id=%s", (seat,))
    mysql.connection.commit()
    cur.close()
    flash('Booking cancelled.', 'success')
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)

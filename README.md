

# Movie Ticket Booking System

A full-stack Flask application for browsing movies, booking tickets, and managing payments.

## 📂 Project Structure

```
movie_booking_app/
│
├── app.py
├── run_app.py
├── schema.sql
├── seed.sql
├── requirements.txt
├── config_sample.ini
├── .gitignore
│
├── static/
│ ├── style.css
│ └── images/
│ └── background.png
│
└── templates/
├── base.html
├── index.html
├── login.html
├── signup.html
├── booking.html
├── payment.html
├── confirmation.html
└── payment_history.html
```


---

## 🔧 Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/movie-ticket-booking.git
   cd movie-ticket-booking
    ```

2. **Create & activate a virtual environment**
```
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```
3. **Install dependencies**
```
pip install -r requirements.txt
```
4. **Initialize the database**
```
mysql -u root -p < schema.sql
mysql -u root -p movie_booking < seed.sql
```
5. **Configure environment variables**
    Copy config_sample.ini → config.ini and fill in your MySQL credentials.

6. **Run the application**
```
python app.py
```
Open http://127.0.0.1:5000 in your browser.

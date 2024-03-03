from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, timedelta
import os
from sexEd import chat_demo
from flask import redirect


app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Custom 404 page
@app.route('/404')
def not_found():
    return render_template('404.html')

# Phase tracker page
@app.route('/phase-tracker')
def phase_tracker():
    return render_template('phase-tracker-page.html')

# Sex education page
@app.route('/sex-ed')
def sex_ed():
    return render_template('sex-ed-page.html')

# Period tracker page
@app.route('/period-tracker-page.html')
def period_tracker_page():
    return render_template('period-tracker-page.html')

# Function to add days to a given date
def add_days(start_date, days):
    return start_date + timedelta(days=days)

# Function to calculate the difference in days from the start date
def get_current_day(start_date):
    today = datetime.today()
    return (today - start_date).days

# Function to determine the next period start date
def get_next_period(start_date, cycle_length):
    return add_days(start_date, cycle_length)

# Function to determine ovulation status
def get_ovulation_status(start_date, cycle_length):
    current_day = get_current_day(start_date)
    ovulation_day = cycle_length - 14
    if current_day < ovulation_day:
        return f"Ovulation in {ovulation_day - current_day} days"
    elif current_day == ovulation_day:
        return "Ovulation today"
    elif current_day > ovulation_day and current_day <= ovulation_day + 2:
        return "Ovulation just passed"
    else:
        return "Ovulation finished"

# Function to estimate pregnancy chance
def get_pregnancy_chance(start_date, cycle_length):
    current_day = get_current_day(start_date)
    ovulation_day = cycle_length - 14
    if ovulation_day - 2 <= current_day <= ovulation_day + 2:
        return "High chance of pregnancy"
    return "Low chance of pregnancy"

# Function to estimate days before the next period
def get_days_before_period(start_date, cycle_length):
    current_day = get_current_day(start_date)
    days_before_period = cycle_length - current_day
    if days_before_period > 0:
        return f"Period in {days_before_period} days"
    if days_before_period == 0:
        return "Period is today"
    return f"Period is late by {abs(days_before_period)} days"

# Function to determine the current menstrual phase
def get_phase(start_date, cycle_length, period_length=5):
    current_day = get_current_day(start_date)
    if current_day <= period_length:
        return "Menstrual phase"
    if cycle_length - 14 <= current_day <= cycle_length - 12:
        return "Ovulation phase"
    if current_day > period_length and current_day < cycle_length - 14:
        return "Follicular phase"
    return "Luteal phase"

# Endpoint for tracking the menstrual cycle
@app.route('/track', methods=['POST'])
def track():
    start_date_str = request.form.get('start_date')
    cycle_length_str = request.form.get('cycle_length', type=int, default=28)

    if not start_date_str:
        return redirect(url_for('home'))

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    next_period = get_next_period(start_date, cycle_length_str)
    ovulation_status = get_ovulation_status(start_date, cycle_length_str)
    pregnancy_chance = get_pregnancy_chance(start_date, cycle_length_str)
    days_before_period = get_days_before_period(start_date, cycle_length_str)
    phase = get_phase(start_date, cycle_length_str)

    return render_template('results.html', next_period=next_period.strftime('%Y-%m-%d'),
                           ovulation_status=ovulation_status, pregnancy_chance=pregnancy_chance,
                           days_before_period=days_before_period, phase=phase)



@app.route('/trigger_gradio', methods=['GET', 'POST'])
def trigger_gradio():
    # Call the function to launch the Gradio chatbot
    os.environ["GRADIO_SERVER_PORT"] = "7862"
    chat_demo.launch(share=False)
    # Redirect the user to the provided share link
    return redirect(url_for('index', _external=True, _scheme='http', _port=7862))
    


if __name__ == '__main__':
    app.run(debug=True, port=5004)

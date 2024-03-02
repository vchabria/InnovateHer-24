from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
app = Flask(__name__)

from datetime import datetime, timedelta

def add_days(start_date, days):
    return start_date + timedelta(days=days)

def get_current_day(start_date):
    today = datetime.today()
    delta = today - start_date
    return delta.days

def get_next_period(start_date, cycle_length):
    return add_days(start_date, cycle_length)

def get_ovulation_status(start_date, cycle_length):
    current_day = get_current_day(start_date)
    ovulation_day = cycle_length - 14
    if current_day < ovulation_day:
        return f"Ovulation in {ovulation_day - current_day} Days"
    elif current_day == ovulation_day:
        return "Ovulation today"
    elif ovulation_day < current_day <= ovulation_day + 2:
        return "Ovulation possible"
    else:
        return "Ovulation finished"

def get_pregnancy_chance(start_date, cycle_length):
    current_day = get_current_day(start_date)
    ovulation_day = cycle_length - 14
    if ovulation_day - 2 <= current_day <= ovulation_day + 2:
        return "High"
    else:
        return "Low"

def get_days_before_period(start_date, cycle_length):
    current_day = get_current_day(start_date)
    days_before_period = cycle_length - current_day
    if days_before_period > 0:
        return f"Period in {days_before_period} Days"
    elif days_before_period == 0:
        return "Period is today"
    else:
        return f"Delay in {abs(days_before_period)} Days"

def get_phase(start_date, cycle_length, period_length):
    current_day = get_current_day(start_date)
    ovulation_day = cycle_length - 14

    if current_day <= period_length:
        return "Menstrual phase"
    elif ovulation_day - 1 <= current_day <= ovulation_day + 1:
        return "Ovulation phase"
    elif current_day > ovulation_day:
        return "Luteal phase"
    else:
        return "Follicular phase"


@app.route('/')
def index():
    return render_template('index.html')

# Assuming an average cycle length of 28 days
AVERAGE_CYCLE_LENGTH = 28

@app.route('/track', methods=['POST'])
def track():
    start_date_str = request.form['start_date']
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    cycle_length = int(request.form['cycle_length'])  # Ensure this input is validated for reasonable values.

    next_period = get_next_period(start_date, cycle_length)
    ovulation_status = get_ovulation_status(start_date, cycle_length)
    pregnancy_chance = get_pregnancy_chance(start_date, cycle_length)
    days_before_period = get_days_before_period(start_date, cycle_length)
    phase = get_phase(start_date, cycle_length, 28)  # Consider allowing user input or a more dynamic calculation for period length.

    return render_template('results.html', next_period=next_period, ovulation_status=ovulation_status,
                           pregnancy_chance=pregnancy_chance, days_before_period=days_before_period, phase=phase)

if __name__ == "__main__":
    app.run(debug=True)



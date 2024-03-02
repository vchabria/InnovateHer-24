
import openai
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Your OpenAI API key
openai.api_key = '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'

def fetch_information_from_chatgpt(day):
    """
    Fetches information from ChatGPT based on the day of the menstrual cycle.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose the engine you prefer
            prompt=f"Explain what happens during day {day} of a menstrual cycle, including phases like luteal, follicular, menstrual, and ovulation.",
            temperature=0.5,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error fetching information from ChatGPT: {e}")
        return "Error fetching information."

@app.route('/fetch', methods=['GET'])
def fetch():
    """
    Endpoint to fetch and display information for each day of the menstrual cycle.
    """
    day = request.args.get('day', 1, type=int)
    information = fetch_information_from_chatgpt(day)
    return render_template('information.html', day=day, information=information)

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


@app.route('/', methods=['GET', 'POST'])
def index():
    events = []
    if request.method == 'POST':
        start_date_str = request.form['start_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        # Menstruation Phase (Day 1-5)
        for i in range(5):
            events.append({
                'title': 'Menstruation',
                'start': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                'color': '#ff0000'  # Example: Red for menstruation
            })

        # Follicular Phase (Day 1-13, but already covered Day 1-5 with menstruation)
        for i in range(5, 13):
            events.append({
                'title': 'Follicular Phase',
                'start': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                'color': '#00ff00'  # Example: Green for follicular phase
            })


        # Ovulation (Day 14)
        events.append({
            'title': 'Ovulation',
            'start': (start_date + timedelta(days=14)).strftime('%Y-%m-%d'),
            'color': '#0000ff'  # Example: Blue for ovulation
        })

        # Luteal Phase (Day 15-28)
        for i in range(15, 28):
            events.append({
                'title': 'Luteal Phase',
                'start': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                'color': '#ffff00'  # Example: Yellow for luteal phase
            })

    return render_template('index.html', events=events)

# Assuming an average cycle length of 28 days
AVERAGE_CYCLE_LENGTH = 28

@app.route('/track', methods=['POST'])
def track():
    start_date_str = request.form.get('start_date')
    cycle_length_str = request.form.get('cycle_length')

    if not (start_date_str and cycle_length_str):
        # Redirect to the home page if required values are missing
        return redirect(url_for('index'))

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    cycle_length = int(cycle_length_str)

    next_period = get_next_period(start_date, cycle_length)
    ovulation_status = get_ovulation_status(start_date, cycle_length)
    pregnancy_chance = get_pregnancy_chance(start_date, cycle_length)
    days_before_period = get_days_before_period(start_date, cycle_length)
    phase = get_phase(start_date, cycle_length, 28)  # Here, period length is hardcoded as 28 which might need adjustment

    return render_template('results.html', next_period=next_period, ovulation_status=ovulation_status,
                           pregnancy_chance=pregnancy_chance, days_before_period=days_before_period, phase=phase)

if __name__ == "__main__":
    app.run(debug=True, port=5001)



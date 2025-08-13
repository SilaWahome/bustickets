from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'change-me-to-a-secret-key'

routes = [
    {'id': 1, 'from': 'Nairobi', 'to': 'Mombasa', 'duration': '6h', 'price': 2000},
    {'id': 2, 'from': 'Nakuru', 'to': 'Eldoret', 'duration': '4h', 'price': 1500},
    {'id': 3, 'from': 'Kisumu', 'to': 'Kakamega', 'duration': '2.5h', 'price': 900}
]

schedules = [
    {'id': 1, 'route_id': 1, 'departure': '2025-09-01 08:00', 'seats_left': 10},
    {'id': 2, 'route_id': 1, 'departure': '2025-09-01 14:00', 'seats_left': 20},
    {'id': 3, 'route_id': 2, 'departure': '2025-09-02 09:00', 'seats_left': 12}
]

fleet = [
    {'id': 1, 'name': 'Bus A', 'capacity': 40, 'status': 'Active'},
    {'id': 2, 'name': 'Bus B', 'capacity': 30, 'status': 'Maintenance'}
]

bookings = []

def get_route(rid):
    for r in routes:
        if r['id'] == rid:
            return r
    return None

@app.route('/')
def index():
    return render_template('index.html', routes=routes, schedules=schedules, fleet=fleet)

@app.route('/features')
def features():
    features_list = [
        'Route Management', 'Schedule Management', 'Fleet Management', 'Seat Management',
        'Booking & Reservation', 'Pricing & Discounts', 'Online Payment Integration',
        'CRM', 'Refund & Cancellation', 'SMS & Email Notifications'
    ]
    return render_template('features.html', features=features_list)

@app.route('/book/<int:schedule_id>', methods=['GET', 'POST'])
def book(schedule_id):
    schedule = next((s for s in schedules if s['id'] == schedule_id), None)
    if not schedule:
        flash('Schedule not found', 'error')
        return redirect(url_for('index'))
    route = get_route(schedule['route_id'])
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        seat = request.form.get('seat')
        if not name or not phone or not seat:
            flash('Please complete all fields', 'error')
            return redirect(request.url)
        booking = {
            'id': len(bookings)+1,
            'schedule_id': schedule_id,
            'route': route,
            'name': name,
            'phone': phone,
            'seat': seat,
            'price': route['price'],
            'created_at': datetime.utcnow().isoformat()
        }
        bookings.append(booking)
        schedule['seats_left'] = max(0, schedule['seats_left'] - 1)
        flash('Booking confirmed! Your e-ticket has been generated.', 'success')
        return redirect(url_for('ticket', booking_id=booking['id']))
    capacity = next((f['capacity'] for f in fleet if f['id']==1), 20)
    occupied = [b['seat'] for b in bookings if b['schedule_id']==schedule_id]
    return render_template('book.html', schedule=schedule, route=route, capacity=capacity, occupied=occupied)

@app.route('/ticket/<int:booking_id>')
def ticket(booking_id):
    booking = next((b for b in bookings if b['id'] == booking_id), None)
    if not booking:
        flash('Ticket not found', 'error')
        return redirect(url_for('index'))
    return render_template('ticket.html', b=booking)

@app.route('/routes')
def routes_page():
    return render_template('routes.html', routes=routes, schedules=schedules)

@app.route('/fleet')
def fleet_page():
    return render_template('fleet.html', fleet=fleet)

@app.route('/bookings')
def bookings_page():
    return render_template('bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8787, debug=True)

from flask import Flask, render_template, request, redirect, url_for
from models import db, Company, Vehicle, ServiceHistory
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mechanic_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    companies_count = Company.query.count()
    vehicles_count = Vehicle.query.count()
    return render_template('index.html', companies_count=companies_count, vehicles_count=vehicles_count)

@app.route('/companies', methods=['GET', 'POST'])
def companies():
    if request.method == 'POST':
        name = request.form['name']
        tax_id = request.form['tax_id']
        contact_info = request.form['contact_info']
        new_company = Company(name=name, tax_id=tax_id, contact_info=contact_info)
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('companies'))
    
    all_companies = Company.query.all()
    return render_template('companies.html', companies=all_companies)

@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    if request.method == 'POST':
        plate = request.form['plate']
        make = request.form['make']
        model = request.form['model']
        year = request.form.get('year', type=int)
        company_id = request.form.get('company_id', type=int)
        
        new_vehicle = Vehicle(plate=plate, make=make, model=model, year=year, company_id=company_id)
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for('vehicles'))

    all_vehicles = Vehicle.query.all()
    all_companies = Company.query.all()
    return render_template('vehicles.html', vehicles=all_vehicles, companies=all_companies)

@app.route('/vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
def vehicle_detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        description = request.form['description']
        cost = request.form.get('cost', type=float)
        
        new_service = ServiceHistory(vehicle_id=vehicle.id, date=date, description=description, cost=cost)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('vehicle_detail', vehicle_id=vehicle.id))
        
    return render_template('vehicle_detail.html', vehicle=vehicle)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

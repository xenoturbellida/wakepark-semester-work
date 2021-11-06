from flask import Blueprint, render_template, request, jsonify

from wakepark.cashier.equipment_manager import EquipmentManager

cashier = Blueprint('cashier', __name__, template_folder='templates', static_folder='static')

# TODO synchronize with the template
units_number = 10
equipment_manager = EquipmentManager(units_number)


@cashier.route('/equipment')
def display_equipment():
    global equipment_manager
    equipment_manager.update_statuses_and_countdowns()
    return render_template('cashier/equipment.html',
                           units_number=units_number,
                           statuses=equipment_manager.units_statuses)


@cashier.route('/update_timers')
def update_timers_on_equipment():
    global equipment_manager
    equipment_manager.update_statuses_and_countdowns()
    return jsonify(statuses=equipment_manager.units_statuses,
                   countdowns=equipment_manager.countdowns)


@cashier.route('/init_timer', methods=['GET', 'POST'])
def init_timer_on_equipment():
    # d = request.json['data']
    serial_number = int(request.args.get('serial_number'))
    time_interval = int(request.args.get('time_interval'))
    global equipment_manager
    equipment_manager.init_timer(serial_number, time_interval)
    return 'ajaxxxx'


@cashier.route('/reset_timer')
def reset_timer():
    serial_number = int(request.args.get('serial_number'))
    global equipment_manager
    equipment_manager.reset_unit_status(serial_number)
    return 'resp'


@cashier.route('/tes')
def tes():
    return render_template('cashier/tes.html')

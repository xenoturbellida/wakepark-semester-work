from flask import Blueprint, render_template, request

from wakepark.cashier.equipment_manager import EquipmentManager

cashier = Blueprint('cashier', __name__, template_folder='templates', static_folder='static')

# TODO synchronize with the template
units_number = 10
equipment_manager = EquipmentManager(units_number)
print(equipment_manager.units)


@cashier.route('/equipment')
def display_equipment():
    return render_template('cashier/equipment.html')


@cashier.route('/update_timers')
def update_timers_on_equipment():
    global equipment_manager
    equipment_manager.update_statuses_and_countdowns()
    return 'updated'


@cashier.route('/init_timer', methods=['GET', 'POST'])
def init_timer_on_equipment():
    # d = request.json['data']
    serial_number = int(request.args.get('serial_number'))
    time_interval = int(request.args.get('time_interval'))
    global equipment_manager
    equipment_manager.init_timer(serial_number, time_interval)
    return 'ajaxxxx'


@cashier.route('/tes')
def tes():
    return render_template('cashier/tes.html')



'''
db = None
@cashier.before_request
def before_request():
    global db
    db = g.get('link_db')


@cashier.teardown_request
def teardown_request(request):
    global db
    db = None
    return request
'''



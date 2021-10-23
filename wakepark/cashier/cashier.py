from flask import Blueprint, render_template, request

cashier = Blueprint('cashier', __name__, template_folder='templates', static_folder='static')


@cashier.route('/equipment')
def display_equipment():
    return render_template('cashier/equipment.html')


@cashier.route('/ajax', methods=['GET', 'POST'])
def set_timer_on_equipment():
    return 'ajaxxxx'

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



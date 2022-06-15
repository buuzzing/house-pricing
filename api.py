from flask import Blueprint, request, jsonify, session

from db import HouseDB

api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)


@api_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    res = HouseDB.query_res(f'SELECT * FROM user WHERE username = \'{username}\' AND password = \'{password}\';')
    res = res.fetchall()

    if len(res) == 0:
        return jsonify({'code': -1})
    else:
        session['user'] = username
        return jsonify({'code': 0})


@api_blueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({})


@api_blueprint.route('/getHouseList', methods=['GET'])
def get_house_list():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))

    res = HouseDB.query_res(f'SELECT * FROM houseinfo ORDER BY id LIMIT {limit} OFFSET {(page - 1) * limit};')

    data = []
    for row in res:
        house = {
            'id': row[0],
            'house_name': row[1],
            'location': row[2],
            'house_type': row[3],
            'unit_price': row[4],
            'tot_price': row[5],
            'floor': row[6],
            'area': row[7],
            'build_time': row[8],
            'lift_type': row[9],
        }
        data.append(house)

    res = {
        'code': 0,
        'count': 1505,
        'data': data,
    }

    return jsonify(res)

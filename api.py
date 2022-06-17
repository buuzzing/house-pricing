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


@api_blueprint.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    res = HouseDB.insert(f'INSERT INTO user VALUES (\'{username}\', \'{password}\');')

    return jsonify({'code': res})


@api_blueprint.route('/getHouseList', methods=['GET'])
def get_house_list():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))

    pre_price = request.args.get('pre_price')
    area = request.args.get('area')
    stime = request.args.get('stime')
    etime = request.args.get('etime')
    district = request.args.get('district')
    floor = request.args.get('floor')

    where_sql = ''
    if stime is not None and stime != '':
        where_sql = f'WHERE build_year BETWEEN {stime} AND {etime} '

    if pre_price is not None and pre_price != '':
        where_sql += f'AND unit_price BETWEEN {int(pre_price) - 2000} AND {int(pre_price) + 2000} '
    if area is not None and area != '':
        where_sql += f'AND area BETWEEN {float(area) - 20} AND {float(area) + 20} '
    if district is not None and district != '':
        where_sql += f'AND location like \'{district}%\' '
    if floor is not None and floor != '':
        where_sql += f'AND floor like \'{floor}%\' '

    print(where_sql)
    res = HouseDB.query_res(f'SELECT COUNT(*) FROM houseinfo {where_sql}')

    tot = 0
    for row in res:
        tot = int(row[0])

    res = HouseDB.query_res(
        f'SELECT * FROM houseinfo {where_sql} ORDER BY id LIMIT {limit} OFFSET {(page - 1) * limit};')

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
        'count': tot,
        'data': data,
    }

    return jsonify(res)

import json

from flask import Flask, render_template

from api import api_blueprint
from db import HouseDB

app = Flask(__name__)
app.secret_key = '0x7f'
app.register_blueprint(api_blueprint)


def get_prices():
    res = HouseDB.query_res('SELECT location, unit_price FROM houseinfo;')

    prices = {}

    for row in res:
        dis_name = row[0].strip().split()[0]
        if dis_name not in prices:
            prices[dis_name] = []
        prices[dis_name].append(row[1])

    return prices


@app.route('/')
def show_index():
    res = HouseDB.query_res('SELECT unit_price, lng, lat FROM houseinfo;')
    heatmap_data = []
    for row in res:
        single_data = {
            'lng': float(row[1]),
            'lat': float(row[2]),
            'count': row[0]
        }
        heatmap_data.append(single_data)
    return render_template('index.html',
                           heatmap_data=heatmap_data)


@app.route('/list')
def show_list():
    return render_template('list.html')


@app.route('/pic1')
def show_pic1():
    with open('static/database/avg_price.json', 'r') as f:
        avg_price = f.read()
    with open('static/database/sales_volume.json', 'r') as f:
        sales_volume = f.read()
    date = [i for i in range(2002, 2021)]
    avg_price_label = ['商品房', '住宅商品房', '别墅', '办公楼', '商业营业用房', '其他']
    avg_price = json.loads(avg_price)
    sales_volume = json.loads(sales_volume)
    return render_template('pic1.html',
                           date=date,
                           avg_price_label=avg_price_label,
                           avg_price=avg_price,
                           sales_volume=sales_volume)


@app.route('/pic2')
def show_pic2():
    prices = get_prices()
    with open('static/database/history.json', 'r') as f:
        history_price = f.read()
    history_price = json.loads(history_price)
    return render_template('pic2.html',
                           prices=prices,
                           history_price=history_price)


@app.route('/surrounding')
def show_surrounding():
    return render_template('surrounding.html')


@app.route('/login_page')
def login_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()

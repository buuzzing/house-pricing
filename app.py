import json

from flask import Flask, render_template, request, session, redirect
from pyecharts import options as opts
from pyecharts.charts import Bar, Map
from pyecharts.globals import ThemeType

from api import api_blueprint
from db import HouseDB

app = Flask(__name__)
app.secret_key = '0x7f'
app.register_blueprint(api_blueprint)


def get_dis_val():
    res = HouseDB.query_res('SELECT location, unit_price FROM houseinfo;')

    nums = {}
    prices = {}
    for row in res:
        if row[0].split()[0] not in nums:
            nums[row[0].split()[0]] = 1
            prices[row[0].split()[0]] = 0.
        else:
            nums[row[0].split()[0]] += 1
        prices[row[0].split()[0]] += float(row[1])

    dis = list(nums.keys())
    val = [round(prices[dis_name] / nums[dis_name], 2) for dis_name in dis]

    return dis, val


@app.route('/')
def show_index():
    return render_template('index.html')


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
    dis, val = get_dis_val()

    house_map = (
        Map(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width='1200px', height='700px'))
        .add(
            series_name="每平米房价",
            data_pair=list(zip(dis, val)),
            maptype='郑州',
            is_map_symbol_show=False,
            zoom=0.9,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='郑州市各区每平米平均房价',
                subtitle='数据来源：链家网郑州',
                pos_right='center',
                pos_top='5%',
                pos_bottom='10%',
            ),
            visualmap_opts=opts.VisualMapOpts(
                max_=14_000,
                min_=4_000,
            ),
        )
        .render_embed()
    )

    return render_template('pic2.html', house_map=house_map)


@app.route('/surrounding')
def show_surrounding():
    return render_template('surrounding.html')


@app.route('/login_page')
def login_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()

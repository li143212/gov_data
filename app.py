from flask import *
from flask import jsonify, json
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, query_user
import sqlite3
import time
from collections import Counter
from datetime import datetime
from datetime import timedelta

def date_add(date_str, days_count):
    date_list = time.strptime(date_str, "%Y-%m-%d")
    y, m, d = date_list[:3]
    delta = timedelta(days=days_count)
    date_result = datetime(y, m, d) + delta
    date_result = date_result.strftime("%Y-%m-%d")
    return date_result


today_min = '2018-10-30 00:00:00'
today_max = '2018-10-30 24:00:00'
app = Flask(__name__)
app.secret_key = '1234567'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)


def get_db():
    db = sqlite3.connect('datatest.db')
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv


def warning():
    warning_res = []
    cnt = []
    name =[]
    warning_cnt = []
    warning_min_time = '2018-10-30 00:00:00'
    warning_max_time = '2018-10-30 24:00:00'
    warning_datas = query_db("SELECT  SUB_TYPE_NAME, CREATE_TIME,INTIME_TO_ARCHIVE_NUM FROM data")
    for warning_data in warning_datas:
        if warning_data[2] == '1' or warning_min_time <= warning_data[1] <=warning_max_time:        #
            warning_res.append(warning_data)
    for a in warning_res:
        cnt.append(a[0])
    dic_temp = Counter(cnt)
    d = sorted(dic_temp.items(), key=lambda x: x[1], reverse=True)
    for b in d:
        name.append(b[0])
        warning_cnt.append(b[1])
    dic_warning = {'name':name,'value':warning_cnt}
    return dic_warning


def _pie(min_time,max_time):
    data = query_db("SELECT EVENT_PROPERTY_NAME, CREATE_TIME FROM data")
    cnt_t = 0
    cnt_z = 0
    cnt_j = 0
    cnt_g = 0
    cnt_q = 0
    cnt_o = 0
    res = []
    dic = {}
    for x in data:
        if x[1] <= max_time and x[1] >= min_time:
            res.append(x[0])

    for y in res:
        if '投诉' in y:
            cnt_t += 1
        elif '咨询' in y:
            cnt_z += 1
        elif '建议' in y:
            cnt_j += 1
        elif '感谢' in y:
            cnt_g += 1
        elif '求决' in y:
            cnt_q += 1
        elif '其他' in y:
            cnt_o += 1

    dic = {'name': ['投诉', '咨询', '建议', '感谢','求决','其他'], 'value': [cnt_t, cnt_z, cnt_j, cnt_g, cnt_q, cnt_o]}
    return dic


def _bar(min_time,max_time):
    res = []
    cnt_0 = []
    cnt_1 = []
    cnt_2 = []
    cnt_3 = []
    cnt_4 = []
    cnt_5 = []
    dic = {}
    list_r =[]
    list_name = []
    datas = query_db("SELECT STREET_NAME, SUB_TYPE_NAME, CREATE_TIME FROM data")
    for data in datas:
        if min_time <= data[2] <= max_time:
            res.append(data)

    for x in res:
        if x[0] == '碧岭街道':
            cnt_0.append(x[1])
        elif x[0] == '龙田街道':
            cnt_1.append(x[1])
        elif x[0] == '马峦街道':
            cnt_2.append(x[1])
        elif x[0] == '石井街道':
            cnt_3.append(x[1])
        elif x[0] == '坪山街道':
            cnt_4.append(x[1])
        elif x[0] == '坑梓街道':
            cnt_5.append(x[1])

    res_0 = Counter(cnt_0)
    res_1 = Counter(cnt_1)
    res_2 = Counter(cnt_2)
    res_3 = Counter(cnt_3)
    res_4 = Counter(cnt_4)
    res_5 = Counter(cnt_5)

    c = dict(res_0, **res_1)
    c.update(res_2)
    c.update(res_3)
    c.update(res_4)
    c.update(res_5)

    for y in c.keys():
        if y not in res_0:
            res_0[y] = 0
        if y not in res_0:
            res_1[y] = 0
        if y not in res_0:
            res_2[y] = 0
        if y not in res_0:
            res_3[y] = 0
        if y not in res_0:
            res_4[y] = 0
        if y not in res_0:
            res_5[y] = 0

    list_r = []
    for j in range(len(c.keys())):
        list_i = []
        for z in c.keys():
            list_i.append(res_0[z])
            list_i.append(res_1[z])
            list_i.append(res_2[z])
            list_i.append(res_3[z])
            list_i.append(res_4[z])
            list_i.append(res_5[z])
            list_r.append(list_i)
            list_i = []

    list_name = list(c.keys())


    dic = {'district': ['碧岭街道', '龙田街道', '马峦街道', '石井街道', '坪山街道', '坑梓街道'],
       'name': list_name,
       'value': list_r}
    return dic


def _map(min_time,max_time):
    cnt=[0 for x in range(23)]
    res = []
    dic = {}
    data = query_db("SELECT COMMUNITY_ID, CREATE_TIME FROM data")
    for y in data:
        if y[1] <= max_time and y[1] >= min_time:
            res.append(y[0])

    for z in res:
        if '10000' in z:
            cnt[0] += 1
        elif '10001' in z:
            cnt[1] += 1
        elif '10002' in z:
            cnt[2] += 1
        elif '10003' in z:
            cnt[3] += 1
        elif '10004' in z:
            cnt[4] += 1
        elif '10005' in z:
            cnt[5] += 1
        elif '10006' in z:
            cnt[6] += 1
        elif '10007' in z:
            cnt[7] += 1
        elif '10008' in z:
            cnt[8] += 1
        elif '10009' in z:
            cnt[9] += 1
        elif '10010' in z:
            cnt[10] += 1
        elif '10011' in z:
            cnt[11] += 1
        elif '10012' in z:
            cnt[12] += 1
        elif '10013' in z:
            cnt[13] += 1
        elif '10014' in z:
            cnt[14] += 1
        elif '10015' in z:
            cnt[15] += 1
        elif '10016' in z:
            cnt[16] += 1
        elif '10017' in z:
            cnt[17] += 1
        elif '10018' in z:
            cnt[18] += 1
        elif '10019' in z:
            cnt[19] += 1
        elif '10020' in z:
            cnt[20] += 1
        elif '10021' in z:
            cnt[21] += 1
        elif '10022' in z:
            cnt[22] += 1

    dic = {'name': ['马峦社区', '金龟社区', '汤坑社区', '江岭社区', '坪环社区', '坪山社区', '沙坣社区', '六联社区', \
                '田头社区', '碧岭社区', '沙湖社区', '田心社区', '六和社区', '竹坑社区', '老坑社区', '坑梓社区', \
                '和平社区', '石井社区', '南布社区', '金沙社区', '龙田社区', '沙田社区', '秀新社区'], \
            'value': [cnt[0], cnt[1], cnt[2], cnt[3], cnt[4], cnt[5], cnt[6], cnt[7], cnt[8], cnt[9], cnt[10], cnt[11], \
                 cnt[12], cnt[13], cnt[14], cnt[15], cnt[16], cnt[17], cnt[18], cnt[19], cnt[20], cnt[21], cnt[22]]}
    return dic


def _nest(min_time,max_time):
    res_overtime = []    #超期结办
    res_intime_to = []   #处置中
    res_intime = []      #按期结办
    dic = {}
    over = [0 for x in range(18)]
    intime_to = [0 for x in range(18)]
    intime = [0 for x in range(18)]
    data = query_db(
        "SELECT OVERTIME_ARCHIVE_NUM, INTIME_TO_ARCHIVE_NUM, INTIME_ARCHIVE_NUM, EVENT_TYPE_NAME, CREATE_TIME FROM data")
    for x in data:
        if x[4] <= max_time and x[4] >= min_time:
            if x[0] == '1':
                res_overtime.append(x[3])
            if x[1] == '1':
                res_intime_to.append(x[3])
            if x[2] == '1':
                res_intime.append(x[3])
    over[0] = res_overtime.count('安全隐患')
    over[1] = res_overtime.count('治安维稳')
    over[2] = res_overtime.count('环保水务')
    over[3] = res_overtime.count('规土城建')
    over[4] = res_overtime.count('市容环卫')
    over[5] = res_overtime.count('市政设施')
    over[6] = res_overtime.count('交通运输')
    over[7] = res_overtime.count('劳动社保')
    over[8] = res_overtime.count('食药市监')
    over[9] = res_overtime.count('文体旅游')
    over[10] = res_overtime.count('教育卫生')
    over[11] = res_overtime.count('组织人事')
    over[12] = res_overtime.count('党建群团')
    over[13] = res_overtime.count('党纪政纪')
    over[14] = res_overtime.count('民政服务')
    over[15] = res_overtime.count('统一战线')
    over[16] = res_overtime.count('社区管理')
    over[17] = res_overtime.count('专业事件采集')
    intime_to[0] = res_intime_to.count('安全隐患')
    intime_to[1] = res_intime_to.count('治安维稳')
    intime_to[2] = res_intime_to.count('环保水务')
    intime_to[3] = res_intime_to.count('规土城建')
    intime_to[4] = res_intime_to.count('市容环卫')
    intime_to[5] = res_intime_to.count('市政设施')
    intime_to[6] = res_intime_to.count('交通运输')
    intime_to[7] = res_intime_to.count('劳动社保')
    intime_to[8] = res_intime_to.count('食药市监')
    intime_to[9] = res_intime_to.count('文体旅游')
    intime_to[10] = res_intime_to.count('教育卫生')
    intime_to[11] = res_intime_to.count('组织人事')
    intime_to[12] = res_intime_to.count('党建群团')
    intime_to[13] = res_intime_to.count('党纪政纪')
    intime_to[14] = res_intime_to.count('民政服务')
    intime_to[15] = res_intime_to.count('统一战线')
    intime_to[16] = res_intime_to.count('社区管理')
    intime_to[17] = res_intime_to.count('专业事件采集')
    intime[0] = res_intime.count('安全隐患')
    intime[1] = res_intime.count('治安维稳')
    intime[2] = res_intime.count('环保水务')
    intime[3] = res_intime.count('规土城建')
    intime[4] = res_intime.count('市容环卫')
    intime[5] = res_intime.count('市政设施')
    intime[6] = res_intime.count('交通运输')
    intime[7] = res_intime.count('劳动社保')
    intime[8] = res_intime.count('食药市监')
    intime[9] = res_intime.count('文体旅游')
    intime[10] = res_intime.count('教育卫生')
    intime[11] = res_intime.count('组织人事')
    intime[12] = res_intime.count('党建群团')
    intime[13] = res_intime.count('党纪政纪')
    intime[14] = res_intime.count('民政服务')
    intime[15] = res_intime.count('统一战线')
    intime[16] = res_intime.count('社区管理')
    intime[17] = res_intime.count('专业事件采集')
    dic = {'name1': ['超期结办', '处置中', '按期结办'],
           'value1': [len(res_overtime), len(res_intime_to), len(res_intime)],
           'name2': ['安全隐患(超期结办)', '治安维稳(超期结办)', '环保水务(超期结办)', '规土城建(超期结办)', '市容环卫(超期结办)' \
               , '市政设施(超期结办)', '交通运输(超期结办)', '劳动社保(超期结办)', '食药市监(超期结办)', '文体旅游(超期结办)', '教育卫生(超期结办)' \
               , '组织人事(超期结办)', '党建群团(超期结办)', '党纪政纪(超期结办)', '民政服务(超期结办)', '统一战线(超期结办)', '社区管理(超期结办)' \
               , '专业事件采集(超期结办)', '安全隐患(处置中)', '治安维稳(处置中)', '环保水务(处置中)', '规土城建(处置中)', '市容环卫(处置中)' \
               , '市政设施(处置中)', '交通运输(处置中)', '劳动社保(处置中)', '食药市监(处置中)', '文体旅游(处置中)', '教育卫生(处置中)' \
               , '组织人事(处置中)', '党建群团(处置中)', '党纪政纪(处置中)', '民政服务(处置中)', '统一战线(处置中)', '社区管理(处置中)',
                     '专业事件采集(处置中)', '安全隐患(按期结办)', '治安维稳(按期结办)', '环保水务(按期结办)', '规土城建(按期结办)', '市容环卫(按期结办)' \
               , '市政设施(按期结办)', '交通运输(按期结办)', '劳动社保(按期结办)', '食药市监(按期结办)', '文体旅游(按期结办)', '教育卫生(按期结办)' \
               , '组织人事(按期结办)', '党建群团(按期结办)', '党纪政纪(按期结办)', '民政服务(按期结办)', '统一战线(按期结办)', '社区管理(按期结办)',
                     '专业事件采集(按期结办)'],
           'value2': [over[0], over[1], over[2], over[3], over[4], over[5], over[6], over[7], over[8], over[9],
                      over[10], over[11], over[12], over[13], over[14], over[15], over[16], over[17], \
                      intime_to[0], intime_to[1], intime_to[2], intime_to[3], intime_to[4], intime_to[5], intime_to[6],
                      intime_to[7], intime_to[8], intime_to[9], intime_to[10], intime_to[11], \
                      intime_to[12], intime_to[13], intime_to[14], intime_to[15], intime_to[16], intime_to[17], \
                      intime[0], intime[1], intime[2], intime[3], intime[4], intime[5], intime[6], intime[7], intime[8],
                      intime[9], intime[10], intime[11], intime[12], intime[13], intime[14], \
                      intime[15], intime[16], intime[17]]}
    return dic


def adddata_pie(min_time,max_time):

    data = query_db("SELECT EVENT_PROPERTY_NAME, CREATE_TIME FROM data ")
    cnt_t = 0
    cnt_z = 0
    cnt_j = 0
    cnt_g = 0
    cnt_q = 0
    cnt_o = 0
    res = []
    dic = {}
    for x in data:
        if x[1] <= max_time and x[1] >= min_time:
            res.append(x[0])

    for y in res:
        if '投诉' in y:
            cnt_t += 1
        elif '咨询' in y:
            cnt_z += 1
        elif '建议' in y:
            cnt_j += 1
        elif '感谢' in y:
            cnt_g += 1
        elif '求决' in y:
            cnt_q += 1
        elif '其他' in y:
            cnt_o += 1

    dic = {'name': ['投诉', '咨询', '建议', '感谢','求决','其他'], 'value': [cnt_t, cnt_z, cnt_j, cnt_g, cnt_q, cnt_o]}
    return dic





@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id

        return curr_user


@app.route('/')
@login_required
def main():
    max_time = '2018-10-30 24:00:00'
    min_time = '2018-10-30 00:00:00'
    dic_warning = warning()
    dic_1 = _pie(today_min,today_max)
    #chart2
    dic_2 = _bar(today_min,today_max)
    #chart3
    dic_3 = _map(today_min,today_max)
    #chart4
    dic_4 = _nest(today_min,today_max)
    return render_template('main.html',data_1 = dic_1, data_2 = dic_2, data_3 = dic_3, data_4 = dic_4,data_warning = dic_warning)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userid')
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:
            curr_user = User()
            curr_user.id = user_id

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)

            return redirect(url_for('main'))

        # flash('Wrong username or password!')
        return render_template('login.html', error=1)

    # GET 请求
    return render_template('login.html',error=0)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were logged out!")
    return render_template('login.html')


@app.route('/piedata', methods=['POST'])
@login_required
def piedata():

    min = '2018-10-30'
    max = '2018-10-30'
    data = json.loads(request.form.get('data'))
    min = data['start']
    max = data['end']
    i = data['i']
    if min > max:
        return jsonify({})
    if max == '2018-10-30':
        max = date_add(max, int(i))
        if max >= '2018-11-30':
            max = '2018-11-30'
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _pie(min_time, max_time)
        return jsonify(dic)
    else:
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _pie(min_time, max_time)
        return jsonify(dic)


@app.route('/pie', methods=['GET', 'POST'])
@login_required
def pie():
    error = 0
    dic_warning = warning()
    # dic = _pie(today_min,today_max)
    min = '2018-10-30'
    max = '2018-10-30'
    if request.method == 'POST':
        min = request.form.get('start')
        max = request.form.get('end')
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        if min_time > max_time:
            # flash('错误的输入格式！请重新输入')
            error = 1

    return render_template('pie.html',data_warning=dic_warning,start=min,end=max,error=error)


@app.route('/bardata', methods=['POST'])
@login_required
def bardata():

    min = '2018-10-30'
    max = '2018-10-30'
    data = json.loads(request.form.get('data'))
    min = data['start']
    max = data['end']
    i = data['i']
    if min > max:
        return jsonify({})
    if max == '2018-10-30':
        max = date_add(max, int(i))
        if max >= '2018-11-30':
            max = '2018-11-30'
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _bar(min_time, max_time)
        return jsonify(dic)
    else:
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _bar(min_time, max_time)
        return jsonify(dic)


@app.route('/bar', methods=['GET', 'POST'])
@login_required
def bar():
    error = 0
    dic_warning = warning()
    dic = _bar(today_min,today_max)
    min = '2018-10-30'
    max = '2018-10-30'
    if request.method == 'POST':
        min = request.form.get('start')
        max = request.form.get('end')
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        if min_time > max_time:
            # flash('错误的输入格式！请重新输入')
            error = 1
    return render_template('bar.html', data_warning=dic_warning,start=min,end=max,error=error)


@app.route('/mapdata', methods=['POST'])
@login_required
def mapdata():

    min = '2018-10-30'
    max = '2018-10-30'
    data = json.loads(request.form.get('data'))
    min = data['start']
    max = data['end']
    i = data['i']
    if min > max:
        return jsonify({})
    if max == '2018-10-30':

        max = date_add(max, int(i))
        if max >= '2018-11-30':
            max = '2018-11-30'
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _map(min_time, max_time)
        return jsonify(dic)
    else:
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _map(min_time, max_time)
        return jsonify(dic)


@app.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    error = 0
    dic_warning = warning()
    dic = _map(today_min, today_max)
    min = '2018-10-30'
    max = '2018-10-30'
    if request.method == 'POST':
        min = request.form.get('start')
        max = request.form.get('end')
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        if min_time > max_time:
            # flash('错误的输入格式！')
            error = 1
    return render_template('map.html', data_warning=dic_warning,start=min,end=max,error=error)


@app.route('/nestdata', methods=['POST'])
@login_required
def nestdata():

    min = '2018-10-30'
    max = '2018-10-30'
    data = json.loads(request.form.get('data'))
    min = data['start']
    max = data['end']
    i = data['i']
    if min > max:
        return jsonify({})
    if max == '2018-10-30':

        max = date_add(max, int(i))
        if max >= '2018-11-30':
            max = '2018-11-30'
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _nest(min_time, max_time)
        return jsonify(dic)

    else :
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        dic = _nest(min_time, max_time)
        return jsonify(dic)


@app.route('/nest', methods=['GET', 'POST'])
@login_required
def nest():
    error = 0
    dic_warning = warning()
    dic=_nest(today_min, today_max)
    min = '2018-10-30'
    max = '2018-10-30'
    if request.method == 'POST':
        min = request.form.get('start')
        max = request.form.get('end')
        min_time = min + ' ' + '00:00:00'
        max_time = max + ' ' + '24:00:00'
        if min_time > max_time:
            # flash('错误的输入格式！请重新输入')
            error = 1
    return render_template('nest.html', data_warning=dic_warning,start=min,end=max,error=error)


@app.route('/unsolved', methods=['GET'])
def unsolved():
    res = []
    create_time = []
    street_name = []
    community_name = []
    event_src_name = []
    sub_type_name = []
    event_pro_name = []
    dispose_nuit_name = []
    datas = query_db("SELECT STREET_NAME, COMMUNITY_NAME, EVENT_SRC_NAME, SUB_TYPE_NAME,EVENT_PROPERTY_NAME, \
    DISPOSE_UNIT_NAME, CREATE_TIME, INTIME_TO_ARCHIVE_NUM FROM data ORDER BY CREATE_TIME")
    max_time = '2018-10-30 24:00:00'
    min_time = '2018-10-30 00:00:00'
    for data in datas:
        if data[7] == '1' or min_time <= data[6] <=max_time:        #
            res.append(data)

    for x in res:
        create_time.append(x[6])
        street_name.append(x[0])
        community_name.append(x[1])
        event_src_name.append(x[2])
        sub_type_name.append(x[3])
        event_pro_name.append(x[4])
        dispose_nuit_name.append(x[5])

    list_r = []
    list_r = [create_time,street_name,community_name,event_src_name,sub_type_name,event_pro_name,dispose_nuit_name]
    # print(type(create_time[0]))
    return render_template('unsolved.html', data = list_r)


if __name__ == '__main__':
    app.run()
    app.debug = True

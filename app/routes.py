# -*- coding: utf-8 -*-
import time

import pytz
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, BotSettingForm, ResetPasswordRequestForm, ResetPasswordForm, RegistrationForm, FavBetDataForm, UserDataForm, ImitateCasinoGame, ChangePassword, AdminPanelAllUsers
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
import datetime as dt
from datetime import datetime
import browser as favbet
import user_params as params
import config as cnfg
from datetime import timedelta
from app.email import send_password_reset_email
from user_forms import Forms

#game_state = False
#bot_state_flag = False
#final_time = ''
#bet_adress = ''
#message_count = -1
#info_state = ''
bot_list = dict()
params_list = dict()
forms_dict = dict()

#@user_logged_in.connect_via(app)
#def on_user_logged_in(sender, user):
#    cnfg.online_users.append(user.username) # or whatever.

@app.route('/')
@app.route('/index')
@login_required
def index():
    if cnfg.scheduler.get_job('verify') == None:
        cnfg.scheduler.add_job(cnfg.generate_verification_code,
                               'interval',
                               hours=12,
                               id='verify')
    return render_template('index.html',
                           user_text='Пользовательский текст',
                           username=current_user.username,
                           id=current_user.id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    #Если пользователь уше вошел
    if current_user.is_authenticated:
        #Перекинуть на домашнюю страницу
        return redirect(url_for('index'))
    #Присваивание переменной класса формы Входа
    form = LoginForm()
    #При отправке браузером GET запроса возвращает False
    #При отправке POST запроса возвращает True
    if form.validate_on_submit():
        #Поиск юзера по никнейму в бд
        user = User.query.filter_by(username=form.username.data).first()
        #Если нет юзера или пароль неверный
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин или пароль!', 'error')
            return redirect(url_for('login'))
        #Метод для запоминания вошедшего пользователя
        login_user(user, remember=form.remember_me.data)
        #Отлавливание в браузере приставки next в строке браузера для перехода на следующую страницу
        next_page = request.args.get('next')
        #Если страницы нет и еще что-то
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form = form)

@app.route('/change_password/<username>', methods = ['GET', 'POST'])
@login_required
def change_password(username):
    form = ChangePassword()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(form.old_password.data):
            flash('Пароль не совпадает со старым паролем!', 'error')
            return redirect(url_for('change_password', username=current_user.username))
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Изменения сохранены успешно', 'success')
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    #Если пользователь вошел
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Запись в БД введенных данных
        user = User(username=form.username.data,
                    email=form.email.data,
                    favbet_login=form.favbet_login.data,
                    favbet_password=form.favbet_password.data)
        user.set_password(form.password.data)
        #Добавление данных в сессию
        db.session.add(user)
        #Подтверждение записи в БД
        db.session.commit()
        flash('Поздравляем с регистрацией!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',
                           form=form)


@app.route('/edit_favbet_data/<username>', methods=['GET', 'POST'])
@login_required
def edit_favbet_data(username):
    form = FavBetDataForm()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        current_user.favbet_login = form.username.data
        current_user.favbet_password = form.password.data
        db.session.commit()
        flash('Изменения сохранены', 'info')
        return redirect(url_for('index'))
    if request.method == 'GET':
        form.username.data = current_user.favbet_login
        form.password.data = current_user.favbet_password
    return render_template('edit_favbet_data.html',
                           form=form,
                           user=user)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/change_user_data/<username>', methods=['GET', 'POST'])
@login_required
def change_user_data(username):
    param = add_user_parameters(current_user.username)
    form = UserDataForm(current_user.username)
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Изменения сохранены успешно', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_user_data.html',
                           form=form,
                           user=user)


@app.route('/stop_game/', methods=['POST'])
@login_required
def stop_game():
    global params_list, bot_list
    stop = ''
    print(bot_list[current_user.username].no_balance_bet)
    if bot_list[current_user.username].no_balance_bet == "На балансе недостаточно средств для ставки":
        stop = True
        flash("Бот остановлен. Недостаточно средств для совершения ставки", 'error')
    param = add_user_parameters(current_user.username)
    if current_user.username in cnfg.online_users:
        cnfg.online_users.remove(current_user.username)
    if len(cnfg.online_users) == 0:
        cnfg.online_users.append("Нет пользователей онлайн")
    #index = request.form['index']
    #if index == '1':
    #driver = cnfg.add_webdriver(current_user.username)
    if cnfg.scheduler.get_job(str(current_user.username) + "_stop"):
        cnfg.scheduler.remove_job(str(current_user.username) + "_stop")
    if params_list[current_user.username].strategy == '2 раза на цвет' or params_list[current_user.username].strategy == 'Антимартингейл-цвет' or params_list[current_user.username].strategy == 'Средняя0' or params_list[current_user.username].strategy == 'СреднийБлок0':
        while bot_list[current_user.username].is_last_bet_win == False:
            #print('Ждем выигрыш')
            i = 0
    if cnfg.scheduler.get_job(str(current_user.username) + "_run"):
        cnfg.scheduler.remove_job(str(current_user.username) + "_run")
    #driver.get("https://www.favbet.com")
    params_list[current_user.username].game_state = not params_list[current_user.username].game_state
    params_list[current_user.username].bot_state_flag = False
    bot_list[current_user.username].reset_all()
    delete_user_bot(current_user.username)
    params_list[current_user.username].reset_parameters()
    print(cnfg.bet_information_dict[current_user.username])
    user_info = cnfg.user_bot_last_state[current_user.username]
    #print(user_info[1])
    cnfg.delete_webdriver(current_user.username)
    print('Driver close')
    if stop == True:
        return render_template('no_balance.html',
                               str = "Недостаточно средств для совершения ставки")
    else:
        if user_info[1] == 'one_bet':
            cnfg.bet_information_dict[current_user.username].clear()
            return render_template('index.html',
                                   username=current_user.username)
        else:
            session_info = cnfg.bet_information_dict[current_user.username].reverse()
            cnfg.bet_information_dict[current_user.username].clear()
            return render_template('bet_session_results.html',
                                   bet_scheme=user_info[0],
                                   info_list=session_info)

@app.route('/instant_stop_game/', methods=['POST'])
@login_required
def stop_game_instant():
    global params_list, bot_list
    stop = ''
    print(bot_list[current_user.username].no_balance_bet)
    if bot_list[current_user.username].no_balance_bet == "На балансе недостаточно средств для ставки":
        stop = True
        flash("Бот остановлен. Недостаточно средств для совершения ставки", 'error')
    param = add_user_parameters(current_user.username)
    if current_user.username in cnfg.online_users:
        cnfg.online_users.remove(current_user.username)
    if len(cnfg.online_users) == 0:
        cnfg.online_users.append("Нет пользователей онлайн")
    #index = request.form['index']
    #if index == '1':
    #driver = cnfg.add_webdriver(current_user.username)
    if cnfg.scheduler.get_job(str(current_user.username) + "_stop"):
        cnfg.scheduler.remove_job(str(current_user.username) + "_stop")
    if cnfg.scheduler.get_job(str(current_user.username) + "_run"):
        cnfg.scheduler.remove_job(str(current_user.username) + "_run")
    #driver.get("https://www.favbet.com")
    params_list[current_user.username].game_state = not params_list[current_user.username].game_state
    params_list[current_user.username].bot_state_flag = False
    bot_list[current_user.username].reset_all()
    delete_user_bot(current_user.username)
    params_list[current_user.username].reset_parameters()
    print(cnfg.bet_information_dict[current_user.username])
    user_info = cnfg.user_bot_last_state[current_user.username]
    #print(user_info[1])
    cnfg.delete_webdriver(current_user.username)
    print('Driver close')
    if stop == True:
        return render_template('no_balance.html',
                               str = "Недостаточно средств для совершения ставки")
    else:
        if user_info[1] == 'one_bet':
            cnfg.bet_information_dict[current_user.username].clear()
            return render_template('index.html',
                                   username=current_user.username)
        else:
            session_info = cnfg.bet_information_dict[current_user.username].reverse()
            cnfg.bet_information_dict[current_user.username].clear()
            return render_template('bet_session_results.html',
                                   bet_scheme=user_info[0],
                                   info_list=session_info)

def stop_game_in_code(username):
    global params_list, bot_list
    stop = ''
    print(bot_list[username].no_balance_bet)
    if bot_list[username].no_balance_bet == "На балансе недостаточно средств для ставки":
        stop = True
    param = add_user_parameters(username)
    if username in cnfg.online_users:
        cnfg.online_users.remove(username)
    if len(cnfg.online_users) == 0:
        cnfg.online_users.append("Нет пользователей онлайн")
    #index = request.form['index']
    #if index == '1':
    #driver = cnfg.add_webdriver(current_user.username)
    if cnfg.scheduler.get_job(str(username) + "_stop"):
        cnfg.scheduler.remove_job(str(username) + "_stop")
    if params_list[username].strategy == '2 раза на цвет' or params_list[username].strategy == 'Антимартингейл-цвет' or params_list[username].strategy == 'Средняя0' or params_list[username].strategy == 'СреднийБлок0':
        while bot_list[username].is_last_bet_win == False:
            #print('Ждем выигрыш')
            i = 0
    if cnfg.scheduler.get_job(str(username) + "_run"):
        cnfg.scheduler.remove_job(str(username) + "_run")
    #driver.get("https://www.favbet.com")
    time.sleep(2)
    params_list[username].game_state = not params_list[username].game_state
    params_list[username].bot_state_flag = False
    bot_list[username].reset_all()
    delete_user_bot(username)
    params_list[username].reset_parameters()
    print(cnfg.bet_information_dict[username])
    user_info = cnfg.user_bot_last_state[username]
    #print(user_info[1])
    cnfg.delete_webdriver(username)
    print('Driver close')
    cnfg.bet_information_dict[username].clear()


@app.route('/bot_settings', methods=['GET', 'POST'])
@login_required
def bot_settings():
    global bot_list, params_list, forms_dict
    param = add_user_parameters(current_user.username)
    #params_list[current_user.username].reset_parameters()
    timeobj = dt.time(2,0,0)
    add_user_forms(current_user.username)
    if params_list[current_user.username].game_state == True:
        params_list[current_user.username].game_active = 'disabled'
        params_list[current_user.username].game_disabled = 'active'
    else:
        params_list[current_user.username].game_active = 'active'
        params_list[current_user.username].game_disabled = 'disabled'
    #form = BotSettingForm()
    forms_dict[current_user.username].bot = BotSettingForm()
    if forms_dict[current_user.username].bot.validate_on_submit():
        #forms_dict[current_user.username].bot.bet = form.min_bet.data
        params_list[current_user.username].info_state = forms_dict[current_user.username].bot.bet_info.data
        params_list[current_user.username].middle0_line = forms_dict[current_user.username].bot.middle0_line.data
        params_list[current_user.username].middle0_block = forms_dict[current_user.username].bot.middle0_block.data
        #forms_dict[current_user.username].bot.time = forms_dict[current_user.username].bot.play_time.data
        user = add_user_bot(current_user.username, current_user.favbet_login, current_user.favbet_password)
        if forms_dict[current_user.username].bot.min_bet.data == '4':
            params_list[current_user.username].bet_adress = cnfg.bet_4_bt
            bot_list[current_user.username].min_bet_int = 4
        elif forms_dict[current_user.username].bot.min_bet.data == '10':
            params_list[current_user.username].bet_adress = cnfg.bet_10_bt
            bot_list[current_user.username].min_bet_int = 10
        elif forms_dict[current_user.username].bot.min_bet.data == '20':
            params_list[current_user.username].bet_adress = cnfg.bet_20_bt
            bot_list[current_user.username].min_bet_int = 20
        elif forms_dict[current_user.username].bot.min_bet.data == '100':
            params_list[current_user.username].bet_adress = cnfg.bet_100_bt
            bot_list[current_user.username].min_bet_int = 100
        elif forms_dict[current_user.username].bot.min_bet.data == '500':
            params_list[current_user.username].bet_adress = cnfg.bet_500_bt
            bot_list[current_user.username].min_bet_int = 500
        elif forms_dict[current_user.username].bot.min_bet.data == '2000':
            params_list[current_user.username].bet_adress = cnfg.bet_2000_bt
            bot_list[current_user.username].min_bet_int = 2000
        if forms_dict[current_user.username].bot.play_schema.data == '1':
            params_list[current_user.username].strategy = '2 раза на цвет'
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username)
        elif forms_dict[current_user.username].bot.play_schema.data == '2':
            params_list[current_user.username].strategy = 'Линии'
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username)
        elif forms_dict[current_user.username].bot.play_schema.data == '3':
            params_list[current_user.username].strategy = 'Линии3'
            bot_list[current_user.username].lines_2_or_3 = 3
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username)
        elif forms_dict[current_user.username].bot.play_schema.data == '4':
            params_list[current_user.username].strategy = 'Линии2'
            bot_list[current_user.username].lines_2_or_3 = 2
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username)
        elif forms_dict[current_user.username].bot.play_schema.data == '5':
            params_list[current_user.username].strategy = 'Антимартингейл-цвет'
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username)
        elif forms_dict[current_user.username].bot.play_schema.data == '6':
            params_list[current_user.username].strategy = 'Средняя0'
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username,
                params_list[current_user.username].middle0_line)
        elif forms_dict[current_user.username].bot.play_schema.data == '7':
            params_list[current_user.username].strategy = 'СреднийБлок0'
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username,
                params_list[current_user.username].middle0_block)
        elif forms_dict[current_user.username].bot.play_schema.data == '8':
            params_list[current_user.username].strategy = 'СредняяЛинияБлок'
            params_list[current_user.username].login_state = start_game(
                forms_dict[current_user.username].bot.play_schema.data,
                params_list[current_user.username].bet_adress,
                forms_dict[current_user.username].bot.min_bet.data,
                current_user.username,
                params_list[current_user.username].middle0_line,
                params_list[current_user.username].middle0_block)
        else:
            params_list[current_user.username].strategy = 'Неопределенный вариант'
        #id = str(current_user.username) + "_stop"
        params_list[current_user.username].final_time = datetime.now(pytz.timezone("Europe/Kiev"))+timedelta(hours=forms_dict[current_user.username].bot.play_time.data.hour,
                                                                                 minutes=forms_dict[current_user.username].bot.play_time.data.minute)
        bot_list[current_user.username].id_stop_aps = f"{current_user.username}_stop"
        #cnfg.scheduler.add_job(stop_game, 'date', run_date=params_list[current_user.username].final_time.strftime("%Y-%m-%d %H:%M:%S"), id=bot_list[current_user.username].id_stop_aps)
        cnfg.scheduler.add_job(stop_game_in_code,
                               'interval',
                               hours=forms_dict[current_user.username].bot.play_time.data.hour,
                               minutes=forms_dict[current_user.username].bot.play_time.data.minute,
                               args=(current_user.username,),
                               id=bot_list[current_user.username].id_stop_aps)
        cnfg.scheduler.print_jobs()
        params_list[current_user.username].game_state = not params_list[current_user.username].game_state
        params_list[current_user.username].bot_state_flag = True
        cnfg.user_bot_last_state[current_user.username] = []
        cnfg.user_bot_last_state[current_user.username].append(params_list[current_user.username].strategy)
        cnfg.user_bot_last_state[current_user.username].append(forms_dict[current_user.username].bot.bet_info.data)
        #return render_template('index.html', info_state=info_state)
        if bot_list[current_user.username].no_balance_bet == 'На балансе недостаточно средств для ставки':
            return render_template('once_bet_result.html',
                                   no_balance = bot_list[current_user.username].no_balance_bet,
                                   user_text = params_list[current_user.username].login_state,
                                   game_state=params_list[current_user.username].game_state,
                                   info_state=params_list[current_user.username].info_state,
                                   load_data=True,
                                   strings=cnfg.bet_information_dict[current_user.username])
        else:
            return render_template('once_bet_result.html',
                                   user_text=params_list[current_user.username].login_state,
                                   game_state=params_list[current_user.username].game_state,
                                   info_state=params_list[current_user.username].info_state,
                                   load_data=True,
                                   strings=cnfg.bet_information_dict[current_user.username])
    elif request.method == 'GET':
        forms_dict[current_user.username].bot.play_time.data = timeobj
        if params_list[current_user.username].game_active == 'active':
            flash('Загрузка бота может занимать продолжительное время. Оставайтесь на данной странице, по окончанию загрузки вас перенаправит на главную страницу', 'info')
        if params_list[current_user.username].game_active == 'disabled':
            flash('При нажатии на кнопку "Остановить", бот прекратит игру, после последней выиграшной ставки. Ожидайте окончания игры и оставайтесь на данной странице', 'error')
        if params_list[current_user.username].no_balance_bet == "На балансе недостаточно средств для ставки":
            flash("Бот остановлен. Недостаточно средств для совершения ставки", 'error')
    return render_template('control_panel.html',
                           form=forms_dict[current_user.username].bot,
                           game_start=params_list[current_user.username].game_active,
                           game_stop=params_list[current_user.username].game_disabled)


def check_bot_state(username):
    global params_list, bot_list
    param = add_user_parameters(username)
    if params_list[username].bot_state_flag == True:
        if params_list[username].no_balance_bet == 'Ставка':
            if username in cnfg.drivers_dict:
                #str = f"Бот запущен. Баланс: {bot_list[username].check_balance(cnfg.drivers_dict[username])} грн. Игра закроется в {params_list[username].final_time.hour}:{params_list[username].final_time.minute}"
                str = f"Бот запущен, Игра закроется в {params_list[username].final_time.strftime('%H:%M')}"
            else:
                str = "Бот остановлен"
            return str
        #else:
            #stop_game()
            #return "Бот остановлен. Недостаточно средств для совершения ставки"
    else:
        return "Бот остановлен"


def start_game(mode, bet_adress, user_bet, username, middle_line = 'middle', middle_block = 'middle'):
    global start_mode, bot_list
    if "Нет пользователей онлайн" in cnfg.online_users:
        cnfg.online_users.remove("Нет пользователей онлайн")
    if username not in cnfg.online_users:
        cnfg.online_users.append(username)
    driver = cnfg.add_webdriver(current_user.username)
    '''if mode == '1':
        if start_mode == 0:
            favbet.bet_login(cnfg.driver, current_user.favbet_login, current_user.favbet_password)
            start_mode = 1
        favbet.change_camera(cnfg.driver)'''
    state = bot_list[username].prepare_to_game(driver,
                                               current_user.favbet_login,
                                               current_user.favbet_password,
                                               web_username=username,
                                               user_bet=user_bet)
    if state == True:
        bot_list[username].set_start_parameters(driver, bet_adress)
            #    bet_status(driver)
        print(mode)
        print(user_bet)
        print(username)
        bot_list[username].id_run = f"{username}_run"
        cnfg.scheduler.add_job(call_game,
                               'interval',
                               seconds=1,
                               args=(driver,mode,user_bet,username,params_list[username],bot_list[username],middle_line,middle_block,),
                               id = bot_list[username].id_run)
        return "Вход выполнен успешно!"
    else:
        stop_game()
        return "Вход не выполнен"


def call_game(web, mode, user_bet, username, param: params.UserParameters, user: favbet.BotClass, middle_line, middle_block):
    global bot_list, params_list
    if bot_list[username].no_balance_bet == "Ставка":
        user.check_status(web,mode, user_bet, username, param, middle_line, middle_block)
    params_list[username].no_balance_bet = bot_list[username].no_balance_bet
    '''else:
        stop_games(username)'''
    #print(user.bet_info_field)
'''    with app.test_request_context('/index'):
        if cnfg.no_balance_bet != '':
            flash(cnfg.no_balance_bet, 'error')'''


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user.username)
        if user:
            send_password_reset_email(user)
        flash('Перейдите по ссылке и придерживайтесь инструкций', 'info')
        return redirect(url_for('login'))
    return render_template('password_reset_email.html',
                           title='Восстановление пароля',
                           form = form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль успешно изменен', 'success')
        return redirect(url_for('login'))
    return render_template('password_reset_password.html', form=form)

'''@app.route('/update', methods = ['GET', 'POST'])
def update():
    global params_list, bot_list
    if current_user.username in cnfg.user_bot_last_state:
        # user_info = cnfg.user_bot_last_state[current_user.username]
        params_list[current_user.username].one_bet_info = cnfg.bet_information_dict[current_user.username]
        if len(params_list[current_user.username].one_bet_info) == 0 and params_list[current_user.username].message_count == -1:
            params_list[current_user.username].message_count = 0
            if params_list[current_user.username].strategy == '2 раза на цвет' or params_list[current_user.username].strategy == 'Антимартингейл-цвет':
                return jsonify({'data': render_template('message_template.html',
                                                        str="Бот запущен, информация отобразится после первой ставки")})
            else:
                return jsonify({'data': render_template('mass_message_template.html',
                                                        elements=["Бот запущен, информация отобразится после первой ставки"])})
        elif len(params_list[current_user.username].one_bet_info) != 0 and params_list[current_user.username].message_count != -1:
            if params_list[current_user.username].message_count == 0:
                params_list[current_user.username].message_count = 1
                if params_list[current_user.username].strategy == '2 раза на цвет' or params_list[current_user.username].strategy == 'Антимартингейл-цвет':
                    params_list[current_user.username].last_res = params_list[current_user.username].one_bet_info[-1]
                    return jsonify({'data': render_template('message_template.html',
                                                            str=params_list[current_user.username].one_bet_info[-1])})
                else:
                    params_list[current_user.username].last_res = params_list[current_user.username].one_bet_info[-1]
                    return jsonify({'data': render_template('mass_message_template.html',
                                                            elements=params_list[current_user.username].one_bet_info[
                                                                -1])})
            else:
                if params_list[current_user.username].one_bet_info[-1] != params_list[current_user.username].last_res:
                    if params_list[current_user.username].strategy == '2 раза на цвет' or params_list[current_user.username].strategy == 'Антимартингейл-цвет':
                        params_list[current_user.username].last_res = params_list[current_user.username].one_bet_info[-1]
                        return jsonify({'data': render_template('message_template.html',
                                                                str=params_list[current_user.username].one_bet_info[-1])})
                    else:
                        params_list[current_user.username].last_res = params_list[current_user.username].one_bet_info[-1]
                        return jsonify({'data': render_template('mass_message_template.html',
                                                                elements=params_list[current_user.username].one_bet_info[-1])})
                else:
                    return ""
        else:
            return ""
    else:
        return ""'''

@app.route('/update', methods=['POST'])
def update():
    global params_list, bot_list
    if current_user.username in cnfg.user_bot_last_state:
        #user_info = cnfg.user_bot_last_state[current_user.username]
        params_list[current_user.username].one_bet_info = cnfg.bet_information_dict[current_user.username]
        if len(params_list[current_user.username].one_bet_info) == 0 and params_list[current_user.username].message_count == -1:
            params_list[current_user.username].message_count += 1
            if params_list[current_user.username].strategy == '2 раза на цвет' or params_list[current_user.username].strategy == 'Антимартингейл-цвет':
                return jsonify({'data': render_template('message_template.html',
                                                        str="Бот запущен, информация отобразится после первой ставки")})
            #elif params_list[current_user.username].strategy == 'Линии' or params_list[current_user.username].strategy == 'Линии3' or params_list[current_user.username].strategy == 'Линии2' or params_list[current_user.username].strategy == 'Средняя0' or params_list[current_user.username].strategy == 'СреднийБлок0':
            else:
                params_list[current_user.username].mass = ["Бот запущен, информация отобразится после первой ставки"]
                return jsonify({'data': render_template('mass_message_template.html',
                                                        elements = params_list[current_user.username].mass)})
        elif params_list[current_user.username].message_count == len(params_list[current_user.username].one_bet_info) - 1:
            params_list[current_user.username].message_count += 1
            # bet_info.append('Бот запущен, информация отобразится после первой ставки')
            if params_list[current_user.username].strategy == '2 раза на цвет' or params_list[current_user.username].strategy == 'Антимартингейл-цвет':
                return jsonify({'data': render_template('message_template.html',
                                                        str=params_list[current_user.username].one_bet_info[0])})
            #elif params_list[current_user.username].strategy == 'Линии' or params_list[current_user.username].strategy == 'Линии3' or params_list[current_user.username].strategy == 'Линии2' or params_list[current_user.username].strategy == 'Средняя0':
            else:
                return jsonify({'data': render_template('mass_message_template.html',
                                                        elements = params_list[current_user.username].one_bet_info[0])})
        else:
            return ""
    else:
        return ""


@app.route('/update_state', methods=['POST'])
def update_state():
    global params_list, bot_list
    if current_user.is_authenticated:
        if current_user.username in params_list:
            if params_list[current_user.username].no_balance_bet == "Ставка":
                return jsonify({
                    'value': check_bot_state(current_user.username)
                })
            else:
                text = "Ошибка. Бот остановлен. Недостаточно средств для совершения ставки"
                #flash(text, 'error')
                if len(cnfg.bet_information_dict[current_user.username]) == 0:
                    cnfg.bet_information_dict[current_user.username].append(['Ошибка. Бот остановлен. Недостаточно средств для совершения ставки'])
                else:
                    if cnfg.bet_information_dict[current_user.username][-1][0] != 'Ошибка. Бот остановлен. Недостаточно средств для совершения ставки':
                        cnfg.bet_information_dict[current_user.username].insert(0, ['Ошибка. Бот остановлен. Недостаточно средств для совершения ставки'])
                bot_list[current_user.username].is_last_bet_win = True
                params_list[current_user.username].game_state = False
                params_list[current_user.username].no_balance_bet = "Ставка"
                stop_game_in_code(current_user.username)
                #return render_template('no_balance.html', str = 'На балансе недостаточно средств для ставки')
                #params_list[current_user.username].login_state = "Вход выполнен успешно!. Не хвататет средств на ставку"
                #return render_template('bet_session_results.html', bet_scheme="Ошибка. Бот остановлен. Недостаточно средств для совершения ставки")
                return jsonify({
                    'value': "Бот остановлен. Недостаточно средств для совершения ставки"
                })
        else:
            return jsonify({
                'value': "Бот остановлен."
            })
    else:
        return jsonify({
            'value': "Бот остановлен."
        })


@app.route('/bet_session_result', methods=['GET', 'POST'])
@login_required
def bet_session_result():
    return render_template('bet_session_results.html')


@app.route('/once_bet_result', methods=['GET', 'POST'])
@login_required
def once_bet_result():
    global params_list, bot_list
    if current_user.username in cnfg.bet_information_dict:
        #params_list[current_user.username].bet_info.clear()
        #params_list[current_user.username].bet_info = cnfg.bet_information_dict[current_user.username]
        #params_list[current_user.username].bet_info.reverse()
        '''return render_template('once_bet_result.html',
                               mode=params_list[current_user.username].strategy,
                               game_state=params_list[current_user.username].game_state,
                               info_state=params_list[current_user.username].info_state,
                               load_data=False,
                               strings=params_list[current_user.username].bet_info)'''
    else:
        params_list[current_user.username].game_state = False
        '''return render_template('once_bet_result.html',
                               game_state=False,
                               load_data=False)'''
    return render_template('once_bet_result.html',
                           mode=params_list[current_user.username].strategy,
                           game_state=params_list[current_user.username].game_state,
                           info_state=params_list[current_user.username].info_state,
                           load_data=False,
                           strings=cnfg.bet_information_dict[current_user.username])


@app.route('/game_simulation_panel', methods=['GET','POST'])
@login_required
def game_simulation_panel():
    global forms_dict
    #form = ImitateCasinoGame()
    add_user_forms(current_user.username)
    forms_dict[current_user.username].retro = ImitateCasinoGame()
    strategy_sim = ''
    result_list = list()

    if forms_dict[current_user.username].retro.validate_on_submit():
        '''schema = forms_dict[current_user.username].retro.play_schema.data
        game_count = forms_dict[current_user.username].retro.game_count.data
        min_bet = forms_dict[current_user.username].retro.min_bet.data
        mode = forms_dict[current_user.username].retro.mode.data'''
        retro = cnfg.add_retro(current_user.username, current_user.favbet_login, current_user.favbet_password)
        if forms_dict[current_user.username].retro.play_schema.data == '1':
            cnfg.retro_dict[current_user.username].strategy = "2 раза на цвет"
        elif forms_dict[current_user.username].retro.play_schema.data == '2':
            cnfg.retro_dict[current_user.username].strategy = "Линии"
        elif forms_dict[current_user.username].retro.play_schema.data == '3':
            cnfg.retro_dict[current_user.username].strategy = "Линии3"
        elif forms_dict[current_user.username].retro.play_schema.data == '4':
            cnfg.retro_dict[current_user.username].strategy = "Линии2"
        elif forms_dict[current_user.username].retro.play_schema.data == '5':
            cnfg.retro_dict[current_user.username].strategy = "Антимартингейл-цвет"
        elif forms_dict[current_user.username].retro.play_schema.data == '6':
            cnfg.retro_dict[current_user.username].strategy = "Средняя линия почти 0"
        elif forms_dict[current_user.username].retro.play_schema.data == '7':
            cnfg.retro_dict[current_user.username].strategy = "Средний блок почти 0"
        elif forms_dict[current_user.username].retro.play_schema.data == '8':
            cnfg.retro_dict[current_user.username].strategy = "Средняя линия и блок"
        if forms_dict[current_user.username].retro.mode.data == 'retro':
            cnfg.retro_dict[current_user.username].result_list = cnfg.retro_dict[current_user.username].retropersp(cnfg.retro_dict[current_user.username].strategy,
                                                                                                                   int(forms_dict[current_user.username].retro.min_bet.data),
                                                                                                                   int(forms_dict[current_user.username].retro.game_count.data),
                                                                                                                   current_user.username,
                                                                                                                   current_user.favbet_login,
                                                                                                                   current_user.favbet_password,
                                                                                                                   forms_dict[current_user.username].retro.middle0_line.data)
        elif forms_dict[current_user.username].retro.mode.data == 'forecasting':
            cnfg.retro_dict[current_user.username].result_list = cnfg.retro_dict[current_user.username].forecasting(cnfg.retro_dict[current_user.username].strategy,
                                                                                                                    int(forms_dict[current_user.username].retro.min_bet.data),
                                                                                                                    int(forms_dict[current_user.username].retro.game_count.data),
                                                                                                                    forms_dict[current_user.username].retro.middle0_line.data)
        cnfg.retro_dict[current_user.username].result_list.reverse()
        print(cnfg.retro_dict[current_user.username].result_list)
        cnfg.delete_webdriver(current_user.username)
        return render_template('simulation_result.html',
                               scheme=cnfg.retro_dict[current_user.username].strategy,
                               elements=cnfg.retro_dict[current_user.username].result_list)
    elif request.method == 'GET':
        cnfg.delete_retro(current_user.username)
        forms_dict[current_user.username].retro.game_count.data = 100
    return render_template('game_simulation_panel.html', form=forms_dict[current_user.username].retro)


@app.route('/administrator_panel', methods=['GET','POST'])
@login_required
def admin_panels():
    print(current_user.id)
    print(cnfg.online_users)
    #cnfg.generate_verification_code()
    return render_template('admin_panel.html',
                           verification_code=cnfg.verification_code,
                           users=cnfg.online_users)


@app.route('/all_users_panel', methods = ['GET','POST'])
@login_required
def all_users_panel():
    users = User.query.filter(User.username != current_user.username).all()
    return render_template('all_users_panel.html', users=users)

@app.route('/change_user_data_admin/<username>', methods = ['GET', 'POST'])
def change_user_data_admin(username):
    form = AdminPanelAllUsers()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        user.is_admin = int(form.is_admin.data)
        user.is_active = int(form.is_active.data)
        db.session.commit()
        flash('Права пользователя изменены успешно', 'success')
        return redirect(url_for('all_users_panel'))
    elif request.method == 'GET':
        form.is_active.data = str(user.is_active)
        form.is_admin.data = str(user.is_admin)
    return render_template('change_user_data_admin.html', username=username, form = form)



@app.route('/no_balance', methods=['GET', 'POST'])
def no_balance():
    return render_template('no_balance.html',
                           str = "Недостаточно средств для совершения ставки")


def add_user_bot(username,favbet_username,favbet_password):
    global bot_list
    if username in bot_list:
        return bot_list[username]
    else:
        user = favbet.BotClass(username,favbet_username,favbet_password)
        bot_list[username] = user
        return user


def delete_user_bot(username):
    global bot_list
    if username in bot_list:
        bot_list.pop(username)


def add_user_parameters(username):
    global params_list
    if username in params_list:
        return params_list[username]
    else:
        param = params.UserParameters(username)
        params_list[username] = param
        return param


def delete_user_parameters(username):
    global params_list
    if username in params_list:
        params_list.pop(username)


def add_user_forms(username):
    global forms_dict
    if username in forms_dict:
        return forms_dict[username]
    else:
        forms = Forms()
        forms_dict[username] = forms
        return forms

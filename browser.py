import datetime
import random
import time

import pytz
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import config as cnfg
from selenium.webdriver.common.action_chains import ActionChains
import user_params as params

class BotClass:
    username = ''
    favbet_username = ''
    favbet_password = ''
    check_bet_status = 0
    red = ''
    black = ''
    min_bet = ''
    min_bet_int = 0
    double = ''
    cnt_red = 0
    cnt_black = 0
    black_red_circle = 0
    win_bet = ''
    last_bet = ''
    top2to1 = ''
    middle2to1 = ''
    bottom2to1 = ''
    first12 = ''
    second12 = ''
    third12 = ''
    min_line = ''
    middle_line = ''
    max_line = ''
    line_names_dict = dict()
    lines_bets_state = list()
    lines3_down_state = list()
    lines3_middle_state = list()
    lines3_top_state = list()
    lines3_count = list()
    lines3_win_line = ''
    lines_2_or_3 = 0
    id_stop_aps = ''
    id_run = ''
    is_last_bet_win = True
    no_balance_bet = 'Ставка'
    line_bet = {'min': 0, 'middle': 0, 'max': 0}
    anti_color_tuple = ('КРАСНОЕ', 'ЧЕРНОЕ')
    svl = 0
    snl = 0
    ssl = 0
    count_SL = 0
    svl_block = 0
    snl_block = 0
    ssl_block = 0
    count_SL_block = 0
    middle0_win_line = ''
    middle0_win_block = ''
    middle0_middle_line = ''
    middle0_bottom = ''
    middle0_middle = ''
    middle0_top = ''
    middle0_bottom_block = ''
    middle0_middle_block = ''
    middle0_top_block = ''
    middle0_lines_dict = {'НИЖНЯЯ ЛИНИЯ':'МИНИМУМ', 'СРЕДНЯЯ ЛИНИЯ':'СРЕДНЕ', 'ВЕРХНЯЯ ЛИНИЯ':'МАКСИМУМ'}
    middle0_lines_bet_dict = {'МИНИМУМ': 0, 'СРЕДНЕ': 0, 'МАКСИМУМ': 0}
    middle0_block_dict = {'ПЕРВЫЕ 12': 'МИНИМУМ', 'ВТОРЫЕ 12': 'СРЕДНЕ', 'ТРЕТЬИ 12': 'МАКСИМУМ'}
    middle0_block_bet_dict = {'МИНИМУМ': 0, 'СРЕДНЕ': 0, 'МАКСИМУМ': 0}
    current_sum_bet = 0
    bet = {'4': 0, '10': 0, '20': 0, '100': 0, '500': 0, '2000': 0}
    bets_int = (2000, 500, 100, 20, 10, 4)
    bet_4 = ''
    bet_10 = ''
    bet_20 = ''
    bet_100 = ''
    bet_500 = ''
    bet_2000 = ''
    lines3_count_min = 0
    lines3_count_middle = 0
    lines3_count_max = 0
    lines_last_bet_state = ''

    def __init__(self,username, favbet_username, favbet_password):
        self.username = username
        self.favbet_username = favbet_username
        self.favbet_password = favbet_password
        self.id_stop_aps = str(username) + "_stop"
        self.id_run = str(username) + "_run"

    def reset_all(self):
        self.black_red_circle = 0
        self.cnt_red = 0
        self.cnt_black = 0
        self.check_bet_status = 0
        self.reset_lines_params()
        self.reset_lines3()
        self.middle0_reset()
        self.middle0_block_reset()

    def divide_bet_to_small_numbers(self, numb, sum):
        self.bet[str(numb)] = sum // numb
        sum %= numb
        return sum

    def place_bet_from_small_numbers(self, sum):
        for elem in self.bets_int:
            sum = self.divide_bet_to_small_numbers(elem, sum)

    def check_status(self, web, mode, user_bet, username, user: params.UserParameters, middle_line, middle_block):
        if mode == '1':
            self.do_bet_2_colors(web, user_bet, username, user, 'color')
        elif mode == '2':
            self.do_bet_lines(web, user_bet, username, user)
        elif mode == '3':
            self.do_bet_lines3(web, user_bet, username, user)
        elif mode == '4':
            self.do_bet_lines3(web, user_bet, username, user)
        elif mode == '5':
            self.do_bet_2_colors(web, user_bet, username, user, 'anti')
        elif mode == '6':
            self.do_middle0_bet(web, user_bet, username, user, middle_line)
        elif mode == '7':
            self.do_middle0_block_bet(web, user_bet, username, user, middle_line)
        elif mode == '8':
            self.do_bet_blocks_and_lines(web,user_bet, username, user, middle_line, middle_block)

    def prepare_to_game(self, web, username, password, web_username, user_bet):
        web.get("https://www.favbet.com/ru/login/")
        time.sleep(2)
        if web.current_url == "https://www.favbet.com/ru/login/":
            self.bet_login(web, username, password)
        cnfg.bet_information_dict[web_username] = []
        state = self.change_camera(web)
        balance = self.check_balance(web)
        if balance < int(user_bet):
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        return state

    def bet_login(self, web, username, password):
        print("Start Login")
        web.get("https://www.favbet.com/ru/login/")
        #time.sleep(5)
        '''try:
            #elm = wait.until(lambda x: x.find_element(by=By.XPATH, value=cnfg.email_field))
            el = web.find_element(by=By.XPATH, value=cnfg.email_field)
        except:
            return 0'''
        wait = WebDriverWait(web, 90)
        elm = wait.until(lambda x: x.find_element(by=By.XPATH, value=cnfg.email_field))
        #login_field = web.find_element(by=By.XPATH, value=cnfg.email_field)
        login_field = elm
        login_field.send_keys(username)
        password_field = web.find_element(by=By.XPATH, value=cnfg.password_field)
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        print("End Login")

    def check_balance(self, web):
        balance = web.find_element(by=By.XPATH, value=cnfg.balance_field).text
        print(balance)
        string = balance.replace(" ", "")
        str1 = ''
        if ',' in string:
            str1 = string.replace(',', '.')
        else:
            str1 = string
        int_num = float(str1)
        return int_num

    def set_start_parameters(self, web, bet_adress):
        colors = web.find_elements(by=By.CLASS_NAME, value='outsides_color ')
        for i in colors:
            buff = i.get_attribute('data-bet-spot-id')
            if buff == 'red':
                self.red = i
            elif buff == 'black':
                self.black = i
            elif buff == 'top2to1':
                print(i)
                self.top2to1 = i
            elif buff == 'middle2to1':
                print(i)
                self.middle2to1 = i
            elif buff == 'bottom2to1':
                print(i)
                self.bottom2to1 = i
            elif buff == '1st12':
                print(i)
                self.first12 = i
            elif buff == '2nd12':
                print(i)
                self.second12 = i
            elif buff == '3rd12':
                print(i)
                self.third12 = i
        self.bet_4 = web.find_element(by=By.XPATH, value=cnfg.bet_4_bt)
        self.bet_10 = web.find_element(by=By.XPATH, value=cnfg.bet_10_bt)
        self.bet_20 = web.find_element(by=By.XPATH, value=cnfg.bet_20_bt)
        self.bet_100 = web.find_element(by=By.XPATH, value=cnfg.bet_100_bt)
        self.bet_500 = web.find_element(by=By.XPATH, value=cnfg.bet_500_bt)
        self.bet_2000 = web.find_element(by=By.XPATH, value=cnfg.bet_2000_bt)
        self.min_bet = web.find_element(by=By.XPATH, value=bet_adress)
        self.set_lines()

    def change_camera(self, web):
        print("Start Change camera")
        web.get("https://www.favbet.com/ru/live-casino/show-game/evolution/lightning-roulette/?playMode=real")
        if web.current_url != "https://www.favbet.com/ru/live-casino/show-game/evolution/lightning-roulette/?playMode=real":
            return False
        else:
            #time.sleep(15)
            wait = WebDriverWait(web, 90)
            elm = wait.until(lambda x: x.find_element(by=By.XPATH, value=cnfg.game_iframe))
            web.switch_to.frame(elm)
            #web.switch_to.frame(web.find_element(by=By.XPATH, value=cnfg.game_iframe))
            camera_bt = wait.until(lambda x: x.find_element(by=By.XPATH, value=cnfg.video_mode_bt))
            camera_bt.click()
            print("End Change camera")
            return True

#Lines 3 2

    def lines3_up_bet_for_line(self, min, middle, max):
        if min == True:
            self.lines3_down_state.append(self.min_bet_int)
        if middle == True:
            self.lines3_middle_state.append(self.min_bet_int)
        if max == True:
            self.lines3_top_state.append(self.min_bet_int)

    def lines3_check_win(self, list):
        sum_down = sum(list)
        list.clear()
        if sum_down > 3 * self.min_bet_int:
            stavka = sum_down - self.lines_2_or_3 * self.min_bet_int
            print(stavka)
            for i in range(stavka // self.min_bet_int):
                list.append(self.min_bet_int)
        else:
            list.append(self.min_bet_int)

    def lines3_click_lines(self, web, count_min, count_middle, count_max):
        for elem in range(count_min):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.bottom2to1, 5, 5).click().perform()
        for elem in range(count_middle):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle2to1, 5, 5).click().perform()
        for elem in range(count_max):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.top2to1, 5, 5).click().perform()

    def lines3_logic(self, web):
        balance = self.check_balance(web)
        if self.lines3_win_line == "НИЖНЯЯ":
            self.lines3_check_win(self.lines3_down_state)
        elif self.lines3_win_line == "СРЕДНЯЯ":
            self.lines3_check_win(self.lines3_middle_state)
        elif self.lines3_win_line == "ВЕРХНЯЯ":
            self.lines3_check_win(self.lines3_top_state)
        sum_bet = sum(self.lines3_down_state) + sum(self.lines3_middle_state) + sum(self.lines3_top_state)
        if sum_bet > balance:
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            '''for elem in range(len(self.lines3_down_state)):
                actions = ActionChains(web)
                actions.move_to_element_with_offset(self.bottom2to1, 5, 5).click().perform()
            for elem in range(len(self.lines3_middle_state)):
                actions = ActionChains(web)
                actions.move_to_element_with_offset(self.middle2to1, 5, 5).click().perform()
            for elem in range(len(self.lines3_top_state)):
                actions = ActionChains(web)
                actions.move_to_element_with_offset(self.top2to1, 5, 5).click().perform()'''
            count_min = len(self.lines3_down_state)
            count_middle = len(self.lines3_middle_state)
            count_max = len(self.lines3_top_state)
            if count_min >= self.lines3_count_min and count_middle >= self.lines3_count_middle and count_max >= self.lines3_count_max:
                repeat = web.find_element(by=By.XPATH, value=cnfg.double_bt)
                temp_min = count_min - self.lines3_count_min
                temp_middle = count_middle - self.lines3_count_middle
                temp_max = count_max - self.lines3_count_max
                repeat.click()
                self.lines3_click_lines(web, temp_min, temp_middle, temp_max)
            else:
                self.lines3_click_lines(web, count_min, count_middle, count_max)
            self.lines3_count_min = count_min
            self.lines3_count_middle = count_middle
            self.lines3_count_max = count_max

    def do_bet_lines3(self, web, user_bet, username, user: params.UserParameters):
        balance = self.check_balance(web)
        count_wins = 0
        status_info = ''
        if balance < int(user_bet):
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            user.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            user.no_balance_bet = 'Ставка'
            text = web.find_element(by=By.XPATH, value=cnfg.info_text_field).text
            print(text)
            first_txt = text[: text.find(' ')]
            last_txt = text[text.find(' ') + 1:]
            if first_txt == 'ДЕЛАЙТЕ' and self.check_bet_status == 0:
                if len(self.lines3_down_state)==0 and len(self.lines3_middle_state)==0 and len(self.lines3_top_state)==0:
                    self.lines3_up_bet_for_line(True, True, True)
                self.min_bet.click()
                self.lines3_logic(web)
                self.check_bet_status = 1
            elif (last_txt == 'ЗЕЛЕНОЕ' or last_txt == 'ЧЕРНОЕ' or last_txt == 'КРАСНОЕ') and self.check_bet_status == 1:
                user.bet_info_field = ''
                status_bet = ''
                # status_info = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ". " + "Выпало: " + text
                print(text)
                bal = self.check_balance(web)
                mass = list()
                for num in cnfg.min_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal, True, "НИЖНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", sum(self.lines3_down_state), text))
                        mass.append(self.print_lines_result(bal, False, "СРЕДНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", sum(self.lines3_middle_state), text))
                        mass.append(self.print_lines_result(bal, False, "ВЕРХНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", sum(self.lines3_top_state), text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.lines3_win_line = "НИЖНЯЯ"
                        self.lines3_up_bet_for_line(False, True, True)
                        # status_info = status_info + ', Победа по нижней линии. Ставка: ' + str(self.line_bet['min']) + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        # self.reset_lines_params()
                        count_wins = 1
                for num in cnfg.middle_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        # status_info = status_info + ', Победа по средней линии' + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        mass.append("---")
                        mass.append(self.print_lines_result(bal, False, "НИЖНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", sum(self.lines3_down_state), text))
                        mass.append(self.print_lines_result(bal, True, "СРЕДНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", sum(self.lines3_middle_state), text))
                        mass.append(self.print_lines_result(bal, False, "ВЕРХНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", sum(self.lines3_top_state), text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.lines3_win_line = "СРЕДНЯЯ"
                        self.lines3_up_bet_for_line(True, False, True)
                for num in cnfg.max_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        # status_info = status_info + ', Победа по верхней линии' + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        mass.append("---")
                        mass.append(self.print_lines_result(bal, False, "НИЖНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", sum(self.lines3_down_state), text))
                        mass.append(self.print_lines_result(bal, False, "СРЕДНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", sum(self.lines3_middle_state), text))
                        mass.append(self.print_lines_result(bal, True, "ВЕРХНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", sum(self.lines3_top_state), text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.lines3_win_line = "ВЕРХНЯЯ"
                        self.lines3_up_bet_for_line(True, True, False)
                if first_txt == '0':
                    # status_info = status_info + ', Проигрыш'
                    mass.append("---")
                    mass.append(self.print_lines_result(bal, False, "НИЖНЯЯ ЛИНИЯ", " ", sum(self.lines3_down_state), text))
                    mass.append(self.print_lines_result(bal, False, "СРЕДНЯЯ ЛИНИЯ", " ", sum(self.lines3_middle_state), text))
                    mass.append(self.print_lines_result(bal, False, "ВЕРХНЯЯ ЛИНИЯ", " ", sum(self.lines3_top_state), text))
                    mass.append("---")
                    #cnfg.bet_information_dict[username].append(mass)
                    self.lines3_win_line = "0"
                    self.lines3_up_bet_for_line(True, True, True)
                user.bet_info_field = status_info
                cnfg.bet_information_dict[username].insert(0, mass)
                # cnfg.bet_information_dict[username].append(status_info)
                self.check_bet_status = 0

    def reset_lines3(self):
        self.lines3_win_line = ''
        self.lines3_down_state.clear()
        self.lines3_top_state.clear()
        self.lines3_middle_state.clear()
        self.lines_2_or_3 = 0
        self.lines3_count_min = 0
        self.lines3_count_middle = 0
        self.lines3_count_max = 0


# Middle line 0

    def bet_on_one_line(self, web, line_adr, bet_adr, one_bet):
        if self.bet[str(one_bet)] != 0:
            bet_adr.click()
            for i in range(self.bet[str(one_bet)]):
                actions = ActionChains(web)
                actions.move_to_element_with_offset(line_adr, 5, 5).click().perform()

    def bet_on_lines_middle0(self, web, line_adr):
        self.bet_on_one_line(web, line_adr, self.bet_2000, 2000)
        self.bet_on_one_line(web, line_adr, self.bet_500, 500)
        self.bet_on_one_line(web, line_adr, self.bet_100, 100)
        self.bet_on_one_line(web, line_adr, self.bet_20, 20)
        self.bet_on_one_line(web, line_adr, self.bet_10, 10)
        self.bet_on_one_line(web, line_adr, self.bet_4, 4)

    def not_use_middle0_bets_in_line(self, web, c_snl, c_ssl, c_svl):
        self.place_bet_from_small_numbers(c_snl * self.min_bet_int)
        self.bet_on_lines_middle0(web,self.middle0_bottom)
        self.place_bet_from_small_numbers(c_ssl * self.min_bet_int)
        self.bet_on_lines_middle0(web, self.middle0_middle)
        self.place_bet_from_small_numbers(c_svl * self.min_bet_int)
        self.bet_on_lines_middle0(web, self.middle0_top)
        self.snl = c_snl
        self.ssl = c_ssl
        self.svl = c_svl
        self.middle0_lines_bet_dict['МИНИМУМ'] = self.snl
        self.middle0_lines_bet_dict['СРЕДНЕ'] = self.ssl
        self.middle0_lines_bet_dict['МАКСИМУМ'] = self.svl

    def middle0_click_to_lines(self, web, count_snl, count_ssl, count_svl):
        for i in range(count_snl):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle0_bottom, 5, 5).click().perform()
        for i in range(count_ssl):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle0_middle, 5, 5).click().perform()
        for i in range(count_svl):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle0_top, 5, 5).click().perform()

    def middle0_bets_in_line(self, web, c_snl, c_ssl, c_svl):
        balance = self.check_balance(web)
        sum_bet = (c_snl*self.min_bet_int) + (c_ssl*self.min_bet_int) + (c_svl*self.min_bet_int)
        if sum_bet > balance:
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            if self.snl == 0 and self.ssl == 0 and self.svl == 0:
                self.middle0_click_to_lines(web, c_snl, c_ssl, c_svl)
            elif c_snl == 2*self.snl and c_ssl == 2*self.ssl and c_svl == 2*self.svl:
                repeat_and_double = web.find_element(by=By.XPATH, value=cnfg.double_bt)
                repeat_and_double.click()
                repeat_and_double.click()
            elif c_snl >= self.snl and c_ssl >= self.ssl and c_svl >= self.svl:
                repeat = web.find_element(by=By.XPATH, value=cnfg.double_bt)
                temp_snl = c_snl - self.snl
                temp_ssl = c_ssl - self.ssl
                temp_svl = c_svl - self.svl
                repeat.click()
                self.middle0_click_to_lines(web, temp_snl, temp_ssl, temp_svl)
            else:
                self.middle0_click_to_lines(web, c_snl, c_ssl, c_svl)
            self.snl = c_snl
            self.ssl = c_ssl
            self.svl = c_svl
            self.middle0_lines_bet_dict['МИНИМУМ'] = self.snl
            self.middle0_lines_bet_dict['СРЕДНЕ'] = self.ssl
            self.middle0_lines_bet_dict['МАКСИМУМ'] = self.svl

    def middle0_logic(self,web,win_line):
        if win_line == 'МАКСИМУМ':
            self.count_SL = 0
            self.middle0_bets_in_line(web,
                                      c_snl=2,
                                      c_ssl=0,
                                      c_svl=3)
        elif win_line == 'МИНИМУМ':
            self.count_SL = 0
            if self.snl == 0:
                self.middle0_bets_in_line(web,
                                          c_snl=2*self.ssl,
                                          c_ssl=0,
                                          c_svl=2*self.svl)
            else:
                self.middle0_bets_in_line(web,
                                          c_snl=self.snl,
                                          c_ssl=self.ssl,
                                          c_svl=self.svl)
        elif win_line == 'СРЕДНЕ':
            if self.count_SL == 0:
                self.count_SL += 1
                self.middle0_bets_in_line(web,
                                          c_snl=2*self.snl,
                                          c_ssl=0,
                                          c_svl=2*self.svl)
            elif self.count_SL == 1:
                self.count_SL += 1
                self.middle0_bets_in_line(web,
                                          c_snl=0,
                                          c_ssl=2*self.snl,
                                          c_svl=2*self.svl)
            elif self.count_SL == 2:
                self.count_SL = 0
                self.middle0_bets_in_line(web,
                                          c_snl=self.ssl,
                                          c_ssl=0,
                                          c_svl=self.svl)
        elif win_line == 'НОЛЬ':
            self.count_SL = 0
            if self.ssl == 0:
                self.middle0_bets_in_line(web,
                                          c_snl=2*self.snl,
                                          c_ssl=self.ssl,
                                          c_svl=2*self.svl)
            else:
                self.middle0_bets_in_line(web,
                                          c_snl=2*self.ssl,
                                          c_ssl=0,
                                          c_svl=2*self.svl)

    def do_middle0_bet(self,web, user_bet, username,user: params.UserParameters, middle_line):
        balance = self.check_balance(web)
        count_wins = 0
        status_info = ''
        if balance < 0:
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            user.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            user.no_balance_bet = 'Ставка'
            text = web.find_element(by=By.XPATH, value=cnfg.info_text_field).text
            print(text)
            first_txt = text[: text.find(' ')]
            last_txt = text[text.find(' ') + 1:]
            if self.middle0_bottom == '' and self.middle0_middle == '' and self.middle0_top == '':
                self.set_middle0_middle_line(middle_line)
            if first_txt == 'ДЕЛАЙТЕ' and self.check_bet_status == 0:
                self.min_bet.click()
                self.is_last_bet_win = False
                if self.snl==0 and self.ssl==0 and self.svl==0:
                    self.middle0_bets_in_line(web,
                                              c_snl=2,
                                              c_ssl=0,
                                              c_svl=3)
                else:
                    self.middle0_logic(web,self.middle0_win_line)
                self.check_bet_status = 1
            elif (last_txt == 'ЗЕЛЕНОЕ' or last_txt == 'ЧЕРНОЕ' or last_txt == 'КРАСНОЕ') and self.check_bet_status == 1:
                user.bet_info_field = ''
                print(text)
                down = self.middle0_lines_bet_dict[self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ']]
                mid = self.middle0_lines_bet_dict[self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ']]
                top = self.middle0_lines_bet_dict[self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ']]
                bal = self.check_balance(web)
                mass = list()
                for num in cnfg.min_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                           "НИЖНЯЯ ЛИНИЯ",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                           "НИЖНЯЯ ЛИНИЯ",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                           "НИЖНЯЯ ЛИНИЯ",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_line = self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ']
                        count_wins = 1
                for num in cnfg.middle_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                           "СРЕДНЯЯ ЛИНИЯ",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                           "СРЕДНЯЯ ЛИНИЯ",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                           "СРЕДНЯЯ ЛИНИЯ",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_line = self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ']
                for num in cnfg.max_line:
                    if int(first_txt) == num:
                        print('Выигрыш')

                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                           "ВЕРХНЯЯ ЛИНИЯ",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                           "ВЕРХНЯЯ ЛИНИЯ",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                           "ВЕРХНЯЯ ЛИНИЯ",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_line = self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ']
                if first_txt == '0':
                    mass.append("---")
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                       " ",
                                                        down * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                       " ",
                                                        mid * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                       " ",
                                                        top * self.min_bet_int,
                                                        text))
                    mass.append("---")
                    #cnfg.bet_information_dict[username].append(mass)
                    self.middle0_win_line = "НОЛЬ"
                if self.middle0_win_line == 'МАКСИМУМ':
                    self.is_last_bet_win = True
                user.bet_info_field = status_info
                cnfg.bet_information_dict[username].insert(0, mass)
                # cnfg.bet_information_dict[username].append(status_info)
                self.check_bet_status = 0

    def set_middle0_lines(self, min, mid, max, min_name, middle_name, max_name):
        self.middle0_bottom = min
        self.middle0_middle = mid
        self.middle0_top = max
        self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'] = min_name
        self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'] = middle_name
        self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'] = max_name

    def set_middle0_middle_line(self, middle_line):
        if middle_line == 'min':
            self.set_middle0_lines(self.middle2to1,self.bottom2to1,self.top2to1, 'СРЕДНЕ', 'МИНИМУМ', 'МАКСИМУМ')
        elif middle_line == 'middle':
            self.set_middle0_lines(self.bottom2to1,self.middle2to1,self.top2to1, 'МИНИМУМ', 'СРЕДНЕ', 'МАКСИМУМ')
        elif middle_line == 'max':
            self.set_middle0_lines(self.bottom2to1,self.top2to1,self.middle2to1, 'МИНИМУМ', 'МАКСИМУМ', 'СРЕДНЕ')

    def middle0_reset(self):
        self.snl = 0
        self.ssl = 0
        self.svl = 0
        self.count_SL = 0
        self.middle0_bottom = ''
        self.middle0_middle = ''
        self.middle0_top = ''
        self.middle0_lines_dict = {'НИЖНЯЯ ЛИНИЯ':'МИНИМУМ', 'СРЕДНЯЯ ЛИНИЯ':'СРЕДНЕ', 'ВЕРХНЯЯ ЛИНИЯ':'МАКСИМУМ'}
        self.middle0_lines_bet_dict = {'МИНИМУМ': 0, 'СРЕДНЕ': 0, 'МАКСИМУМ': 0}


#Middle block 0

    def middle0_block_click_to_lines(self, web, count_snl, count_ssl, count_svl):
        for i in range(count_snl):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle0_bottom_block, 10, 10).click().perform()
        for i in range(count_ssl):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle0_middle_block, 10, 10).click().perform()
        for i in range(count_svl):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle0_top_block, 10, 10).click().perform()

    def middle0_block_bets_in_line(self, web, c_snl, c_ssl, c_svl):
        balance = self.check_balance(web)
        sum_bet = (c_snl * self.min_bet_int) + (c_ssl * self.min_bet_int) + (c_svl * self.min_bet_int)
        if sum_bet > balance:
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            if self.snl_block == 0 and self.ssl_block == 0 and self.svl_block == 0:
                self.middle0_block_click_to_lines(web, c_snl, c_ssl, c_svl)
            elif c_snl == 2*self.snl_block and c_ssl == 2*self.ssl_block and c_svl == 2*self.svl_block:
                repeat_and_double = web.find_element(by=By.XPATH, value=cnfg.double_bt)
                repeat_and_double.click()
                repeat_and_double.click()
            elif c_snl >= self.snl_block and c_ssl >= self.ssl_block and c_svl >= self.svl_block:
                repeat = web.find_element(by=By.XPATH, value=cnfg.double_bt)
                temp_snl = c_snl - self.snl_block
                temp_ssl = c_ssl - self.ssl_block
                temp_svl = c_svl - self.svl_block
                repeat.click()
                self.middle0_block_click_to_lines(web, temp_snl, temp_ssl, temp_svl)
            else:
                self.middle0_block_click_to_lines(web, c_snl, c_ssl, c_svl)
            self.snl_block = c_snl
            self.ssl_block = c_ssl
            self.svl_block = c_svl
            self.middle0_block_bet_dict['МИНИМУМ'] = self.snl_block
            self.middle0_block_bet_dict['СРЕДНЕ'] = self.ssl_block
            self.middle0_block_bet_dict['МАКСИМУМ'] = self.svl_block

    def middle0_block_logic(self, web, win_line):
        if win_line == 'МАКСИМУМ':
            self.count_SL_block = 0
            self.middle0_block_bets_in_line(web,
                                      c_snl=2,
                                      c_ssl=0,
                                      c_svl=3)
        elif win_line == 'МИНИМУМ':
            self.count_SL_block = 0
            if self.snl == 0:
                self.middle0_block_bets_in_line(web,
                                          c_snl=2 * self.ssl,
                                          c_ssl=0,
                                          c_svl=2 * self.svl)
            else:
                self.middle0_block_bets_in_line(web,
                                          c_snl=self.snl,
                                          c_ssl=self.ssl,
                                          c_svl=self.svl)
        elif win_line == 'СРЕДНЕ':
            if self.count_SL_block == 0:
                self.count_SL_block += 1
                self.middle0_block_bets_in_line(web,
                                          c_snl=2 * self.snl,
                                          c_ssl=0,
                                          c_svl=2 * self.svl)
            elif self.count_SL_block == 1:
                self.count_SL_block += 1
                self.middle0_block_bets_in_line(web,
                                          c_snl=0,
                                          c_ssl=2 * self.snl,
                                          c_svl=2 * self.svl)
            elif self.count_SL_block == 2:
                self.count_SL_block = 0
                self.middle0_block_bets_in_line(web,
                                          c_snl=self.ssl,
                                          c_ssl=0,
                                          c_svl=self.svl)
        elif win_line == 'НОЛЬ':
            self.count_SL_block = 0
            if self.ssl_block == 0:
                self.middle0_block_bets_in_line(web,
                                          c_snl=2 * self.snl,
                                          c_ssl=self.ssl,
                                          c_svl=2 * self.svl)
            else:
                self.middle0_block_bets_in_line(web,
                                          c_snl=2 * self.ssl,
                                          c_ssl=0,
                                          c_svl=2 * self.svl)

    def do_middle0_block_bet(self,web, user_bet, username,user: params.UserParameters, middle_line):
        balance = self.check_balance(web)
        count_wins = 0
        status_info = ''
        if self.middle0_bottom_block == '' and self.middle0_middle_block == '' and self.middle0_top_block == '':
            self.set_middle0_middle_block(middle_line)
        if balance < 0:
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            user.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            user.no_balance_bet = 'Ставка'
            text = web.find_element(by=By.XPATH, value=cnfg.info_text_field).text
            print(text)
            first_txt = text[: text.find(' ')]
            last_txt = text[text.find(' ') + 1:]
            if first_txt == 'ДЕЛАЙТЕ' and self.check_bet_status == 0:
                self.min_bet.click()
                self.is_last_bet_win = False
                if self.snl_block==0 and self.ssl_block==0 and self.svl_block==0:
                    self.middle0_block_bets_in_line(web,
                                                    c_snl=2,
                                                    c_ssl=0,
                                                    c_svl=3)
                else:
                    self.middle0_block_logic(web,self.middle0_win_block)
                self.check_bet_status = 1
            elif (last_txt == 'ЗЕЛЕНОЕ' or last_txt == 'ЧЕРНОЕ' or last_txt == 'КРАСНОЕ') and self.check_bet_status == 1:
                user.bet_info_field = ''
                status_bet = ''
                # status_info = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ". " + "Выпало: " + text
                print(text)
                down = self.middle0_block_bet_dict[self.middle0_block_dict['ПЕРВЫЕ 12']]
                mid = self.middle0_block_bet_dict[self.middle0_block_dict['ВТОРЫЕ 12']]
                top = self.middle0_block_bet_dict[self.middle0_block_dict['ТРЕТЬИ 12']]
                bal = self.check_balance(web)
                mass = list()
                for num in cnfg.first12:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                           "ПЕРВЫЕ 12",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ВТОРЫЕ 12'],
                                                           "ПЕРВЫЕ 12",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ТРЕТЬИ 12'],
                                                           "ПЕРВЫЕ 12",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_block = self.middle0_block_dict['ПЕРВЫЕ 12']
                        count_wins = 1
                for num in cnfg.second12:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                           "ВТОРЫЕ 12",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_block_dict['ВТОРЫЕ 12'],
                                                           "ВТОРЫЕ 12",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ТРЕТЬИ 12'],
                                                           "ВТОРЫЕ 12",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_block = self.middle0_block_dict['ВТОРЫЕ 12']
                for num in cnfg.third12:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        self.is_last_bet_win = True
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                           "ТРЕТЬИ 12",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ВТОРЫЕ 12'],
                                                           "ТРЕТЬИ 12",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_block_dict['ТРЕТЬИ 12'],
                                                           "ТРЕТЬИ 12",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_block = self.middle0_block_dict['ТРЕТЬИ 12']
                if first_txt == '0':
                    mass.append("---")
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                       " ",
                                                        down * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_block_dict['ВТОРЫЕ 12'],
                                                       " ",
                                                        mid * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_block_dict['ТРЕТЬИ 12'],
                                                       " ",
                                                        top * self.min_bet_int,
                                                        text))
                    mass.append("---")
                    #cnfg.bet_information_dict[username].append(mass)
                    self.middle0_win_block = "НОЛЬ"
                if self.middle0_win_block == 'МАКСИМУМ':
                    self.is_last_bet_win = True
                cnfg.bet_information_dict[username].insert(0, mass)
                user.bet_info_field = status_info
                # cnfg.bet_information_dict[username].append(status_info)
                self.check_bet_status = 0

    def set_middle0_blocks(self, min, mid, max, min_name, middle_name, max_name):
        self.middle0_bottom_block = min
        self.middle0_middle_block = mid
        self.middle0_top_block = max
        self.middle0_block_dict['ПЕРВЫЕ 12'] = min_name
        self.middle0_block_dict['ВТОРЫЕ 12'] = middle_name
        self.middle0_block_dict['ТРЕТЬИ 12'] = max_name

    def set_middle0_middle_block(self, middle_line):
        if middle_line == 'min':
            self.set_middle0_blocks(self.second12,self.first12,self.third12, 'СРЕДНЕ', 'МИНИМУМ', 'МАКСИМУМ')
        elif middle_line == 'middle':
            self.set_middle0_blocks(self.first12,self.second12,self.third12, 'МИНИМУМ', 'СРЕДНЕ', 'МАКСИМУМ')
        elif middle_line == 'max':
            self.set_middle0_blocks(self.first12,self.third12,self.second12, 'МИНИМУМ', 'МАКСИМУМ', 'СРЕДНЕ')

    def middle0_block_reset(self):
        self.snl_block = 0
        self.ssl_block = 0
        self.svl_block = 0
        self.count_SL_block = 0
        self.middle0_bottom_block = ''
        self.middle0_middle_block = ''
        self.middle0_top_block = ''
        self.middle0_block_dict = {'ПЕРВЫЕ 12': 'МИНИМУМ', 'ВТОРЫЕ 12': 'СРЕДНЕ', 'ТРЕТЬИ 12': 'МАКСИМУМ'}
        self.middle0_block_bet_dict = {'МИНИМУМ': 0, 'СРЕДНЕ': 0, 'МАКСИМУМ': 0}

#Lines

    def set_lines(self):
        list = [self.bottom2to1, self.middle2to1, self.top2to1]
        #names = ['min', 'middle', 'max']
        rand_min = random.randrange(0, 3)
        self.min_line = list.pop(rand_min)
        #self.line_names_dict['НИЖНЯЯ'] = names.pop(rand_min)
        rand_mid = random.randrange(0, 2)
        self.middle_line = list.pop(rand_mid)
        #self.line_names_dict['СРЕДНЯЯ'] = names.pop(rand_mid)
        self.max_line = list[0]
        #self.line_names_dict['ВЕРХНЯЯ'] = names[0]
        self.check_lines_names('НИЖНЯЯ',self.bottom2to1)
        self.check_lines_names('СРЕДНЯЯ', self.middle2to1)
        self.check_lines_names('ВЕРХНЯЯ', self.top2to1)
        #print(f'Min: {min}, Mid: {middle}, Max: {max}')

    def check_lines_names(self, key, value):
        if value == self.min_line:
            self.line_names_dict[key] = 'min'
        elif value == self.middle_line:
            self.line_names_dict[key] = 'middle'
        elif value == self.max_line:
            self.line_names_dict[key] = 'max'

    def start_lines_bet(self,web):
        actions1 = ActionChains(web)
        actions1.move_to_element_with_offset(self.min_line, 5, 5).click().perform()
        print("Min bet")
        for i in range(0, 2):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.middle_line, 5, 5).click().perform()
            print("Middle bet")
        for i in range(0, 3):
            actions = ActionChains(web)
            actions.move_to_element_with_offset(self.max_line, 5, 5).click().perform()
            print("Max bet")

    def not_using_lines_bet(self, web):
        if len(self.lines_bets_state) == 0:
            self.start_lines_bet(web)
        self.double = web.find_element(by=By.XPATH, value=cnfg.double_bt)
        for elem in self.lines_bets_state:
            if elem == '+':
                actions = ActionChains(web)
                actions.move_to_element_with_offset(self.min_line, 5, 5).click().perform()
                self.line_bet['min'] += self.min_bet_int
                #bottom2to1.click()
                print('++++++')
            if elem == 'x2':
                self.double.click()
                self.line_bet['min'] *= 2
                self.line_bet['middle'] *= 2
                self.line_bet['max'] *= 2
                print('x2')

    def lines_bet(self, web):
        self.line_bet['min'] = self.min_bet_int
        self.line_bet['middle'] = self.min_bet_int * 2
        self.line_bet['max'] = self.min_bet_int * 3
        if len(self.lines_bets_state) == 0:
            self.start_lines_bet(web)
        else:
            double_and_repeat = web.find_element(by=By.XPATH, value=cnfg.double_bt)
            double_and_repeat.click()
            if self.lines_last_bet_state == '+':
                actions = ActionChains(web)
                actions.move_to_element_with_offset(self.min_line, 5, 5).click().perform()
            elif self.lines_last_bet_state == '*':
                double_and_repeat.click()
            for elem in self.lines_bets_state:
                if elem == '+':
                    self.line_bet['min'] += self.min_bet_int
                    print('++++++')
                if elem == 'x2':
                    self.line_bet['min'] *= 2
                    self.line_bet['middle'] *= 2
                    self.line_bet['max'] *= 2
                    print('x2')

    def check_bet_sum(self):
        bets = list()
        bets.append(self.min_bet_int)
        bets.append(self.min_bet_int*2)
        bets.append(self.min_bet_int*3)
        '''bets[0] = self.min_bet_int
        bets[1] = self.min_bet_int*2
        bets[2] = self.min_bet_int*3'''
        for elem in self.lines_bets_state:
            if elem == '+':
                bets[0] += self.min_bet_int
            if elem == '*':
                bets[0] *= 2
                bets[1] *= 2
                bets[2] *= 2
        sum = bets[0] + bets[1] + bets[2]
        return sum

    def print_lines_result(self, balance, state, name, win_line, sum_bet, win_number=''):
        if state == True:
            return f'{str(datetime.datetime.now(pytz.timezone("Europe/Kiev")).strftime("%Y-%m-%d %H:%M"))} Выпало {win_number} {win_line}. Победа по ставке на {name}, сумма ставки: {str(sum_bet)}, текущий баланс: {balance}'
        else:
            return f'{str(datetime.datetime.now(pytz.timezone("Europe/Kiev")).strftime("%Y-%m-%d %H:%M"))} Выпало {win_number} {win_line}. Проигрыш по ставке на {name}, сумма ставки: {str(sum_bet)}, текущий баланс: {balance}'

    def do_bet_lines(self, web, user_bet, username, user: params.UserParameters):
        balance = self.check_balance(web)
        count_wins = 0
        status_info = ''
        if balance < 0:
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            user.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            user.no_balance_bet = 'Ставка'
            text = web.find_element(by=By.XPATH, value=cnfg.info_text_field).text
            print(text)
            first_txt = text[: text.find(' ')]
            last_txt = text[text.find(' ') + 1:]
            if first_txt == 'ДЕЛАЙТЕ' and self.check_bet_status == 0:
                if self.check_bet_sum() > balance:
                    self.no_balance_bet = 'На балансе недостаточно средств для ставки'
                    self.is_last_bet_win = True
                else:
                    self.min_bet.click()
                    self.lines_bet(web)
                    self.check_bet_status = 1
            elif (last_txt == 'ЗЕЛЕНОЕ' or last_txt == 'ЧЕРНОЕ' or last_txt == 'КРАСНОЕ') and self.check_bet_status == 1:
                user.bet_info_field = ''
                status_bet = ''
                #status_info = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ". " + "Выпало: " + text
                print(text)
                bal = self.check_balance(web)
                mass = list()
                for num in cnfg.min_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal, True, "НИЖНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['НИЖНЯЯ']], text))
                        mass.append(self.print_lines_result(bal, False, "СРЕДНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['СРЕДНЯЯ']], text))
                        mass.append(self.print_lines_result(bal, False, "ВЕРХНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['ВЕРХНЯЯ']], text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        #status_info = status_info + ', Победа по нижней линии. Ставка: ' + str(self.line_bet['min']) + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        #self.reset_lines_params()
                        if self.line_names_dict['НИЖНЯЯ'] == 'min':
                            self.lines_last_bet_state = 'ВЫИГРЫШ'
                            count_wins = 1
                for num in cnfg.middle_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        #status_info = status_info + ', Победа по средней линии' + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        mass.append("---")
                        mass.append(self.print_lines_result(bal, False, "НИЖНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['НИЖНЯЯ']], text))
                        mass.append(self.print_lines_result(bal, True, "СРЕДНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['СРЕДНЯЯ']], text))
                        mass.append(self.print_lines_result(bal, False, "ВЕРХНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['ВЕРХНЯЯ']], text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        if self.line_names_dict['СРЕДНЯЯ'] == 'min':
                            self.lines_last_bet_state = 'ВЫИГРЫШ'
                            count_wins = 1
                for num in cnfg.max_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        #status_info = status_info + ', Победа по верхней линии' + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        mass.append("---")
                        mass.append(self.print_lines_result(bal, False, "НИЖНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['НИЖНЯЯ']], text))
                        mass.append(self.print_lines_result(bal, False, "СРЕДНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['СРЕДНЯЯ']], text))
                        mass.append(self.print_lines_result(bal, True, "ВЕРХНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", self.line_bet[self.line_names_dict['ВЕРХНЯЯ']], text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        if self.line_names_dict['ВЕРХНЯЯ'] == 'min':
                            self.lines_last_bet_state = 'ВЫИГРЫШ'
                            count_wins = 1
                if count_wins == 0 and first_txt != '0':
                    #status_info = status_info + ', Проигрыш'
                    self.lines_bets_state.append('+')
                    self.lines_last_bet_state = '+'
                    count_wins = 0
                if first_txt == '0' and count_wins == 0:
                    #status_info = status_info + ', Проигрыш'
                    self.lines_bets_state.append('x2')
                    self.lines_last_bet_state = '*'
                    mass.append("---")
                    mass.append(self.print_lines_result(bal, False, "НИЖНЯЯ ЛИНИЯ", " ", self.line_bet[self.line_names_dict['НИЖНЯЯ']], text))
                    mass.append(self.print_lines_result(bal, False, "СРЕДНЯЯ ЛИНИЯ", " ", self.line_bet[self.line_names_dict['СРЕДНЯЯ']], text))
                    mass.append(self.print_lines_result(bal, False, "ВЕРХНЯЯ ЛИНИЯ", " ", self.line_bet[self.line_names_dict['ВЕРХНЯЯ']], text))
                    mass.append("---")
                    #cnfg.bet_information_dict[username].append(mass)
                cnfg.bet_information_dict[username].insert(0, mass)
                user.bet_info_field = status_info
                #cnfg.bet_information_dict[username].append(status_info)
                self.line_bet['min'] = 0
                self.line_bet['middle'] = 0
                self.line_bet['max'] = 0
                self.check_bet_status = 0

    def reset_lines_params(self):
        self.lines_bets_state.clear()
        self.line_bet['min'] = 0
        self.line_bet['middle'] = 0
        self.line_bet['max'] = 0
        self.check_bet_status = 0
        self.lines_last_bet_state = ''

#2 Colours and antimartingale

    def set_random_color(self):
        color_num = random.randrange(0, 2)
        return self.anti_color_tuple[color_num]

    def bet_on_red(self, web, win_colour):
        print(win_colour)
        balance = self.check_balance(web)
        self.cnt_red += 1
        if win_colour == self.last_bet:
            print("Ставка выиграла. Начинаем сначала")
            self.black_red_circle = 0
            sum_bet = self.min_bet_int
            self.current_sum_bet = self.min_bet_int
            if sum_bet > balance:
                self.no_balance_bet = 'На балансе недостаточно средств для ставки'
                self.is_last_bet_win = True
            else:
                self.min_bet.click()
                time.sleep(2)
                self.red.click()
        else:
            pow = 2**self.black_red_circle
            sum_bet = self.min_bet_int*pow
            self.current_sum_bet = self.min_bet_int
            if sum_bet > balance:
                self.no_balance_bet = 'На балансе недостаточно средств для ставки'
                self.is_last_bet_win = True
            else:
                self.min_bet.click()
                time.sleep(2)
                self.red.click()
                self.double = web.find_element(by=By.XPATH, value=cnfg.double_bt)
                for i in range(self.black_red_circle):
                    print("Ставка проиграла, удваиваем ставку")
                    #time.sleep(1)
                    self.double.click()
                    self.current_sum_bet *= 2
        self.last_bet = "КРАСНОЕ"

    def bet_on_black(self, web, win_colour):
        print(win_colour)
        self.cnt_black += 1
        balance = self.check_balance(web)
        if win_colour == self.last_bet:
            print("Ставка выиграла. Начинаем сначала")
            self.black_red_circle = 0
            sum_bet = self.min_bet_int
            self.current_sum_bet = self.min_bet_int
            if sum_bet > balance:
                self.no_balance_bet = 'На балансе недостаточно средств для ставки'
                self.is_last_bet_win = True
            else:
                self.min_bet.click()
                time.sleep(2)
                self.black.click()
        else:
            pow = 2 ** self.black_red_circle
            sum_bet = self.min_bet_int * pow
            self.current_sum_bet = self.min_bet_int
            if sum_bet > balance:
                self.no_balance_bet = 'На балансе недостаточно средств для ставки'
                self.is_last_bet_win = True
            else:
                self.min_bet.click()
                time.sleep(2)
                self.black.click()
                self.double = web.find_element(by=By.XPATH, value=cnfg.double_bt)
                for i in range(self.black_red_circle):
                    print("Ставка проиграла, удваиваем ставку")
                    #time.sleep(1)
                    self.double.click()
                    self.current_sum_bet *= 2
        self.last_bet = "ЧЕРНОЕ"

    def zeroing(self, web, win_colour):
        print(win_colour)
        self.cnt_black = 0
        self.cnt_red = 0
        print("Цикл ставок окончен")
        self.bet_on_black(web, win_colour)

    def red_black_strategy(self, web, win_colour):
        if self.cnt_red == 0 and self.cnt_black == 0:
            self.bet_on_black(web, win_colour)
        elif self.cnt_black < 2:
            self.bet_on_black(web,win_colour)
        elif self.cnt_red < 2:
            self.bet_on_red(web,win_colour)
        else:
            self.zeroing(web,win_colour)

    def do_bet_2_colors(self, web, user_bet, username, user: params.UserParameters, mode):
        print("Start bet")
        status_bet = ''
        my_bet = ''
        balance = self.check_balance(web)
        if balance < 0:
            print(f'Баланс {balance}, Ставка {int(user_bet)}')
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            user.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            user.no_balance_bet = 'Ставка'
            text = web.find_element(by=By.XPATH, value=cnfg.info_text_field).text
            print(text)
            first_txt = text[ : text.find(' ')]
            last_txt = text[text.find(' ') + 1 : ]
            if first_txt == 'ДЕЛАЙТЕ' and self.check_bet_status == 0:
                my_bet = 'КРАСНОЕ'
                if mode == 'anti':
                    color = self.set_random_color()
                    self.is_last_bet_win = False
                    if color == 'КРАСНОЕ':
                        self.bet_on_red(web, self.win_bet)
                    elif color == 'ЧЕРНОЕ':
                        self.bet_on_black(web, self.win_bet)
                elif mode == 'color':
                    self.is_last_bet_win = False
                    self.red_black_strategy(web, self.win_bet)
                #min_bet.click()
                #time.sleep(2)
                #red.click()
                #time.sleep(2)
                #double.click()
                #print(f"Ставка сделана на {my_bet}")
                self.check_bet_status = 1
            elif (last_txt == 'ЗЕЛЕНОЕ' or last_txt == 'ЧЕРНОЕ' or last_txt == 'КРАСНОЕ') and self.check_bet_status == 1:
                user.bet_info_field = ''
                status_info = ''
                status_info = str(datetime.datetime.now(pytz.timezone("Europe/Kiev")).strftime("%Y-%m-%d %H:%M")) + ". " + "Выпало: " + text
                if last_txt == self.last_bet:
                    status_info = status_info + ', Победа по ' + self.last_bet + f". Ставка: {self.current_sum_bet}. Баланс: {self.check_balance(web)} грн."
                    self.is_last_bet_win = True
                    #print(f'Вы выиграли!!!!! Сыграло {last_txt}')
                    print("-----------------------------------------------")
                else:
                    status_info = status_info + ', Проигрыш по ' + self.last_bet + f". Ставка: {self.current_sum_bet}. Баланс: {self.check_balance(web)} грн."
                    self.is_last_bet_win = False
                    #print(f'Вы проиграли. Сыграло {last_txt}')
                    print("--------------------------------------------------")
                user.bet_info_field = status_info
                cnfg.bet_information_dict[username].insert(0, status_info)
                self.win_bet = last_txt
                self.check_bet_status = 0
                self.black_red_circle += 1
        print('End Bet')


#Blocks and lines

    def do_bet_blocks_and_lines(self,web, user_bet, username,user: params.UserParameters, middle_line, middle_block):
        balance = self.check_balance(web)
        count_wins = 0
        status_info = ''
        if balance < 0:
            self.no_balance_bet = 'На балансе недостаточно средств для ставки'
            user.no_balance_bet = 'На балансе недостаточно средств для ставки'
            self.is_last_bet_win = True
        else:
            user.no_balance_bet = 'Ставка'
            text = web.find_element(by=By.XPATH, value=cnfg.info_text_field).text
            print(text)
            first_txt = text[: text.find(' ')]
            last_txt = text[text.find(' ') + 1:]
            if self.middle0_bottom == '' and self.middle0_middle == '' and self.middle0_top == '':
                self.set_middle0_middle_line(middle_line)
            if self.middle0_bottom_block == '' and self.middle0_middle_block == '' and self.middle0_top_block == '':
                self.set_middle0_middle_block(middle_block)
            if first_txt == 'ДЕЛАЙТЕ' and self.check_bet_status == 0:
                self.min_bet.click()
                if self.snl==0 and self.ssl==0 and self.svl==0:
                    self.middle0_bets_in_line(web,
                                              c_snl=2,
                                              c_ssl=0,
                                              c_svl=3)
                else:
                    self.middle0_logic(web,self.middle0_win_line)
                self.check_bet_status = 1

                self.is_last_bet_win = False
                if self.snl_block == 0 and self.ssl_block == 0 and self.svl_block == 0:
                    self.middle0_block_bets_in_line(web,
                                                    c_snl=2,
                                                    c_ssl=0,
                                                    c_svl=3)
                else:
                    self.middle0_block_logic(web, self.middle0_win_block)
                self.check_bet_status = 1
            elif (last_txt == 'ЗЕЛЕНОЕ' or last_txt == 'ЧЕРНОЕ' or last_txt == 'КРАСНОЕ') and self.check_bet_status == 1:
                user.bet_info_field = ''
                print(text)
                down = self.middle0_lines_bet_dict[self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ']]
                mid = self.middle0_lines_bet_dict[self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ']]
                top = self.middle0_lines_bet_dict[self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ']]
                bal = self.check_balance(web)
                mass = list()
                for num in cnfg.min_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                           "НИЖНЯЯ ЛИНИЯ",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                           "НИЖНЯЯ ЛИНИЯ",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                           "НИЖНЯЯ ЛИНИЯ",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_line = self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ']
                        count_wins = 1
                for num in cnfg.middle_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                           "СРЕДНЯЯ ЛИНИЯ",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                           "СРЕДНЯЯ ЛИНИЯ",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                           "СРЕДНЯЯ ЛИНИЯ",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_line = self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ']
                for num in cnfg.max_line:
                    if int(first_txt) == num:
                        print('Выигрыш')

                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                           "ВЕРХНЯЯ ЛИНИЯ",
                                                            down * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                           "ВЕРХНЯЯ ЛИНИЯ",
                                                            mid * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                           "ВЕРХНЯЯ ЛИНИЯ",
                                                            top * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        #cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_line = self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ']
                if first_txt == '0':
                    mass.append("---")
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_lines_dict['НИЖНЯЯ ЛИНИЯ'],
                                                       " ",
                                                        down * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_lines_dict['СРЕДНЯЯ ЛИНИЯ'],
                                                       " ",
                                                        mid * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_lines_dict['ВЕРХНЯЯ ЛИНИЯ'],
                                                       " ",
                                                        top * self.min_bet_int,
                                                        text))
                    mass.append("---")
                    #cnfg.bet_information_dict[username].append(mass)
                    self.middle0_win_line = "НОЛЬ"
                if self.middle0_win_line == 'МАКСИМУМ':
                    self.is_last_bet_win = True
                user.bet_info_field = status_info
                # cnfg.bet_information_dict[username].append(status_info)
                down_bl = self.middle0_block_bet_dict[self.middle0_block_dict['ПЕРВЫЕ 12']]
                mid_bl = self.middle0_block_bet_dict[self.middle0_block_dict['ВТОРЫЕ 12']]
                top_bl = self.middle0_block_bet_dict[self.middle0_block_dict['ТРЕТЬИ 12']]
                bal = self.check_balance(web)
                for num in cnfg.first12:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                            "ПЕРВЫЕ 12",
                                                            down_bl * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ВТОРЫЕ 12'],
                                                            "ПЕРВЫЕ 12",
                                                            mid_bl * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ТРЕТЬИ 12'],
                                                            "ПЕРВЫЕ 12",
                                                            top_bl * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        # cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_block = self.middle0_block_dict['ПЕРВЫЕ 12']
                        count_wins = 1
                for num in cnfg.second12:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                            "ВТОРЫЕ 12",
                                                            down_bl * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_block_dict['ВТОРЫЕ 12'],
                                                            "ВТОРЫЕ 12",
                                                            mid_bl * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ТРЕТЬИ 12'],
                                                            "ВТОРЫЕ 12",
                                                            top_bl * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        # cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_block = self.middle0_block_dict['ВТОРЫЕ 12']
                for num in cnfg.third12:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        self.is_last_bet_win = True
                        mass.append("---")
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                            "ТРЕТЬИ 12",
                                                            down_bl * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            False,
                                                            self.middle0_block_dict['ВТОРЫЕ 12'],
                                                            "ТРЕТЬИ 12",
                                                            mid_bl * self.min_bet_int,
                                                            text))
                        mass.append(self.print_lines_result(bal,
                                                            True,
                                                            self.middle0_block_dict['ТРЕТЬИ 12'],
                                                            "ТРЕТЬИ 12",
                                                            top_bl * self.min_bet_int,
                                                            text))
                        mass.append("---")
                        # cnfg.bet_information_dict[username].append(mass)
                        self.middle0_win_block = self.middle0_block_dict['ТРЕТЬИ 12']
                if first_txt == '0':
                    mass.append("---")
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_block_dict['ПЕРВЫЕ 12'],
                                                        " ",
                                                        down_bl * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_block_dict['ВТОРЫЕ 12'],
                                                        " ",
                                                        mid_bl * self.min_bet_int,
                                                        text))
                    mass.append(self.print_lines_result(bal,
                                                        False,
                                                        self.middle0_block_dict['ТРЕТЬИ 12'],
                                                        " ",
                                                        top_bl * self.min_bet_int,
                                                        text))
                    mass.append("---")
                    # cnfg.bet_information_dict[username].append(mass)
                    self.middle0_win_block = "НОЛЬ"
                if self.middle0_win_block == 'МАКСИМУМ':
                    self.is_last_bet_win = True
                cnfg.bet_information_dict[username].insert(0, mass)
                user.bet_info_field = status_info
                # cnfg.bet_information_dict[username].append(status_info)
                self.check_bet_status = 0

    def reset_lines_block(self):
        self.middle0_block_reset()
        self.middle0_reset()
'''if __name__ == "__main__":
    bet_login(cnfg.driver, cnfg.username, cnfg.password)
    cnfg.scheduler.add_job(check_status, 'interval', seconds=1, args=(cnfg.driver,))
    cnfg.scheduler.start()
    while True:
        time.sleep(0.5)'''

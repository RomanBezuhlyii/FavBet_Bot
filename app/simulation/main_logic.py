import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import app.simulation.colors as colors
import app.simulation.lines as lines
import app.simulation.lines3 as lines3
import app.simulation.middle0_line as middle0
import app.simulation.middle0_block as middle0_block
import app.retroperspective.retro as retro
import config as cnfg
import browser as browser

balance = 10000
game_list = list()
win_list = list()

class RetroperspectiveClass:
    strategy_sim = ''
    username = ''
    fav_username = ''
    fav_password = ''
    balance = 10000
    game_list = list()
    win_list = list()
    result_list = list()

    def __init__(self, username, fav_username, fav_password):
        self.username = username
        self.fav_username = fav_username
        self.fav_password = fav_password

    def reset_parameters(self):
        self.balance = 10000
        self.game_list.clear()
        self.win_list.clear()


    def bet_login(self, web):
        web.get("https://www.favbet.com/ru/login/")
        wait = WebDriverWait(web, 60)
        elm = wait.until(lambda x: x.find_element(by=By.XPATH, value=cnfg.email_field))
        login_field = elm
        login_field.send_keys(self.fav_username)
        password_field = web.find_element(by=By.XPATH, value=cnfg.password_field)
        password_field.send_keys(self.fav_password)
        password_field.send_keys(Keys.ENTER)

    def change_camera(self, web):
        web.get("https://www.favbet.com/ru/live-casino/show-game/evolution/lightning-roulette/?playMode=real")
        wait = WebDriverWait(web, 60)
        elm = wait.until(lambda x: x.find_element(by=By.XPATH, value=cnfg.game_iframe))
        web.switch_to.frame(elm)
        camera_bt = wait.until(lambda x: x.find_element(by=By.XPATH, value=cnfg.video_mode_bt))
        camera_bt.click()

    def retropersp(self, scheme, bet, count, username, fav_username, fav_password, middle_line):
        win_color = ''
        win_line = ''
        win_line_lines = ''
        win_line_blocks = ''
        temp_list = list()
        self.game_list.clear()
        color = colors.Colors()
        line = lines.Lines()
        line3 = lines3.Lines3()
        line3.min_bet_int = int(bet)
        middle0_lines = middle0.Middle0Line()
        middle0_lines.min_bet_int = int(bet)
        middle0_blocks = middle0_block.Middle0Block()
        middle0_blocks.min_bet_int = int(bet)
        driver = cnfg.add_webdriver(username)
        if driver.current_url != "https://www.favbet.com/ru/live-casino/show-game/evolution/lightning-roulette/?playMode=real":
            self.bet_login(driver)
            self.change_camera(driver)
        self.win_list = retro.retro_data(driver)
        temp_list = self.win_list[:count]
        temp_list.reverse()
        counter = 0
        if scheme == "Линии":
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = line.lines(self.balance, bet, win_line)
                sum = data['min'] + data['middle'] + data['max']
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win_retro(data, temp_list[i])
            line.reset_parameters()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == 'Линии3':
            line3.lines_2_or_3 = 3
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = line3.lines3(self.balance,win_line)
                sum = data['min'] + data['middle'] + data['max']
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win_retro(data, temp_list[i])
            line3.reset_lines3()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == 'Линии2':
            line3.lines_2_or_3 = 2
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = line3.lines3(self.balance,win_line)
                sum = data['min'] + data['middle'] + data['max']
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win_retro(data, temp_list[i])
            line3.reset_lines3()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "Средняя линия почти 0":
            middle0_lines.middle_line = middle_line
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = middle0_lines.do_middle0_bet(self.balance, win_line)
                sum = (data['min'] + data['middle'] + data['max'])*int(bet)
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win_middle0_lines_retro(data, bet,temp_list[i])
            middle0_lines.middle0_reset()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "Средний блок почти 0":
            middle0_blocks.middle_line = middle_line
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = middle0_blocks.do_middle0_bet(self.balance, win_line)
                sum = (data['min'] + data['middle'] + data['max'])*int(bet)
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win_middle0_block_retro(data, bet,temp_list[i])
            middle0_blocks.middle0_reset()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "Средняя линия и блок":
            middle0_lines.middle_line = middle_line
            middle0_blocks.middle_line = middle_line
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                self.game_list.append("---")
                data_lines = middle0_lines.do_middle0_bet(self.balance, win_line_lines)
                data_blocks = middle0_blocks.do_middle0_bet(self.balance, win_line_blocks)
                sum_blocks = (data_blocks['min'] + data_blocks['middle'] + data_blocks['max']) * int(bet)
                sum_lines = (data_lines['min'] + data_lines['middle'] + data_lines['max']) * int(bet)
                if self.change_balance(False, sum_lines) == False:
                    break
                elif self.change_balance(False, sum_blocks) == False:
                    break
                win_line_lines = self.check_lines_win_middle0_lines_retro(data_lines, bet, temp_list[i])
                win_line_blocks = self.check_lines_win_middle0_block_retro(data_blocks, bet, temp_list[i])
                self.game_list.append("---")
            middle0_lines.middle0_reset()
            middle0_blocks.middle0_reset()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "2 раза на цвет":
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(count):
                # Ставка от бота
                data = color.do_bet(win_color, bet, self.balance, 'color')
                if self.change_balance(False, data['bet_sum']) == False:
                    break
                # Проверка ставки на стороне казино
                win_color = self.check_color_win_retro(data['bet_color'], data['bet_sum'],temp_list[i])
                counter += 1
            color.reset_parameters()
            self.game_list.append(f'Окончательный баланс: {self.balance}')
            print(counter)
        elif scheme == "Антимартингейл-цвет":
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(count):
                # Ставка от бота
                data = color.do_bet(win_color, bet, self.balance, 'anti')
                if self.change_balance(False, data['bet_sum']) == False:
                    break
                # Проверка ставки на стороне казино
                win_color = self.check_color_win_retro(data['bet_color'], data['bet_sum'],temp_list[i])
                counter += 1
            color.reset_parameters()
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        self.win_list.clear()
        self.balance = 10000
        #self.game_list.reverse()
        return self.game_list

    def forecasting(self, scheme, bet, count, middle_line = 'middle'):
        win_color = ''
        win_line = ''
        win_line_lines = ''
        win_line_blocks = ''
        temp_list = list()
        self.game_list.clear()
        color = colors.Colors()
        line = lines.Lines()
        line3 = lines3.Lines3()
        line3.min_bet_int = int(bet)
        middle0_lines = middle0.Middle0Line()
        middle0_lines.min_bet_int = int(bet)
        middle0_blocks = middle0_block.Middle0Block()
        middle0_blocks.min_bet_int = int(bet)
        if scheme == "Линии":
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = line.lines(self.balance, bet, win_line)
                sum = data['min'] + data['middle'] + data['max']
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win(data)
            line.reset_parameters()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == 'Линии3':
            line3.lines_2_or_3 = 3
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = line3.lines3(self.balance, win_line)
                sum = data['min'] + data['middle'] + data['max']
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win(data)
            line3.reset_lines3()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == 'Линии2':
            line3.lines_2_or_3 = 2
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = line3.lines3(self.balance, win_line)
                sum = data['min'] + data['middle'] + data['max']
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win(data)
            line3.reset_lines3()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "Средняя линия почти 0":
            middle0_lines.middle_line = middle_line
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = middle0_lines.do_middle0_bet(self.balance, win_line)
                sum = (data['min'] + data['middle'] + data['max'])*int(bet)
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win_middle0_lines(data, bet)
            middle0_lines.middle0_reset()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "Средний блок почти 0":
            middle0_blocks.middle_line = middle_line
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                data = middle0_blocks.do_middle0_bet(self.balance, win_line)
                sum = (data['min'] + data['middle'] + data['max'])*int(bet)
                if self.change_balance(False, sum) == False:
                    break
                win_line = self.check_lines_win_middle0_block(data, bet)
            middle0_blocks.middle0_reset()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "Средняя линия и блок":
            middle0_lines.middle_line = middle_line
            middle0_blocks.middle_line = middle_line
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(int(count)):
                self.game_list.append("---")
                data_lines = middle0_lines.do_middle0_bet(self.balance, win_line_lines)
                data_blocks = middle0_blocks.do_middle0_bet(self.balance, win_line_blocks)
                sum_blocks = (data_blocks['min'] + data_blocks['middle'] + data_blocks['max']) * int(bet)
                sum_lines = (data_lines['min'] + data_lines['middle'] + data_lines['max']) * int(bet)
                if self.change_balance(False, sum_lines) == False:
                    break
                elif self.change_balance(False, sum_blocks) == False:
                    break
                win_line_lines = self.check_lines_win_middle0_lines(data_lines, bet)
                win_line_blocks = self.check_lines_win_middle0_block(data_blocks, bet)
                self.game_list.append("---")
            middle0_lines.middle0_reset()
            self.game_list.append("---")
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "2 раза на цвет":
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(count):
                #Ставка от бота
                data = color.do_bet(win_color,bet, self.balance,'color')
                if self.change_balance(False,data['bet_sum']) == False:
                    break
                #Проверка ставки на стороне казино
                win_color = self.check_color_win(data['bet_color'],data['bet_sum'])
            color.reset_parameters()
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        elif scheme == "Антимартингейл-цвет":
            self.game_list.append(f'Начальный баланс: {self.balance}')
            for i in range(count):
                # Ставка от бота
                data = color.do_bet(win_color, bet, self.balance, 'anti')
                if self.change_balance(False, data['bet_sum']) == False:
                    break
                # Проверка ставки на стороне казино
                win_color = self.check_color_win(data['bet_color'], data['bet_sum'])
            color.reset_parameters()
            self.game_list.append(f'Окончательный баланс: {self.balance}')
        self.balance = 10000
        return self.game_list

    def change_balance(self, state, bet_sum):
        if state == True:
            self.balance += bet_sum
            return True
        if state == False:
            if self.balance-bet_sum <= 0:
                self.game_list.append("---")
                self.game_list.append('Не хвататет средств для ставки')
                return False
            else:
                self.balance -= bet_sum
                return True

    def random_colour(self):
        pers = random.randrange(1,100)
        if pers > 0 and pers < 52:
            return "КРАСНОЕ"
        elif pers > 51 and pers < 99:
            return "ЧЕРНОЕ"
        elif pers > 98 and pers < 101:
            return "ЗЕЛЕНОЕ"
        else:
            return "Неопределено"

    def random_line(self):
        pers = random.randrange(1,100)
        if pers > 0 and pers < 32:
            #print("Нижняя линия")
            return "Нижняя линия"
        if pers > 31 and pers < 66:
            #print("Средняя линия")
            return "Средняя линия"
        if pers > 65 and pers < 99:
            #print("Верхняя линия")
            return "Верхняя линия"
        if pers > 98 and pers < 100:
            #print("Выпал 0")
            return "Выпал 0"


    def random_block(self):
        pers = random.randrange(1,100)
        if pers > 0 and pers < 32:
            #print("Нижняя линия")
            return "Первые 12"
        if pers > 31 and pers < 66:
            #print("Средняя линия")
            return "Вторые 12"
        if pers > 65 and pers < 99:
            #print("Верхняя линия")
            return "Третьи 12"
        if pers > 98 and pers < 100:
            #print("Выпал 0")
            return "Выпал 0"

    def check_lines_win_middle0_block(self, current_sum_bet, bet):
        self.game_list.append("---")
        win_line = self.random_block()
        check_win = False
        bet_int = int(bet)
        if win_line == "Первые 12":
            win_sum = current_sum_bet['min'] * 3 * bet_int
            self.change_balance(True, win_sum)
            self.game_list.append(
                self.print_result_line(True, "ПЕРВЫЕ 12", "ПЕРВЫЕ 12", current_sum_bet['min'] * bet_int))
            self.game_list.append(
                self.print_result_line(False, "ВТОРЫЕ 12", "ПЕРВЫЕ 12", current_sum_bet['middle'] * bet_int))
            self.game_list.append(
                self.print_result_line(False, "ТРЕТЬИ 12", "ПЕРВЫЕ 12", current_sum_bet['max'] * bet_int))
            win_line = "Первые 12"
        elif win_line == "Вторые 12":
            win_sum = current_sum_bet['middle'] * 3 * bet_int
            self.change_balance(True, win_sum)
            self.game_list.append(
                self.print_result_line(False, "ПЕРВЫЕ 12", "ВТОРЫЕ 12", current_sum_bet['min'] * bet_int))
            self.game_list.append(
                self.print_result_line(True, "ВТОРЫЕ 12", "ВТОРЫЕ 12", current_sum_bet['middle'] * bet_int))
            self.game_list.append(
                self.print_result_line(False, "ТРЕТЬИ 12", "ВТОРЫЕ 12", current_sum_bet['max'] * bet_int))
            win_line = "Вторые 12"
        elif win_line == "Третьи 12":
            win_sum = current_sum_bet['max'] * 3 * bet_int
            self.change_balance(True, win_sum)
            self.game_list.append(
                self.print_result_line(False, "ПЕРВЫЕ 12", "ТРЕТИЕ 12", current_sum_bet['min'] * bet_int))
            self.game_list.append(
                self.print_result_line(False, "ВТОРЫЕ 12", "ТРЕТИЕ 12", current_sum_bet['middle'] * bet_int))
            self.game_list.append(
                self.print_result_line(True, "ТРЕТЬИ 12", "ТРЕТИЕ 12", current_sum_bet['max'] * bet_int))
            win_line = "Третьи 12"
        else:
            self.game_list.append(
                self.print_result_line(False, "ПЕРВЫЕ 12", "Выпало 0", current_sum_bet['min'] * bet_int))
            self.game_list.append(
                self.print_result_line(False, "ВТОРЫЕ 12", "Выпало 0", current_sum_bet['middle'] * bet_int))
            self.game_list.append(
                self.print_result_line(False, "ТРЕТЬИ 12", "Выпало 0", current_sum_bet['max'] * bet_int))
            win_line = "Выпал 0"
        return win_line

    def check_lines_win_middle0_lines(self, current_sum_bet, bet):
        self.game_list.append("---")
        win_line = self.random_line()
        check_win = False
        bet_int = int(bet)
        if win_line == "Нижняя линия":
            win_sum = current_sum_bet['min'] * 3 * bet_int
            self.change_balance(True, win_sum)
            self.game_list.append(self.print_result_line(True, "НИЖНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['min']*bet_int))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['middle']*bet_int))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['max']*bet_int))
            win_line = "Нижняя линия"
        elif win_line == "Средняя линия":
            win_sum = current_sum_bet['middle'] * 3 * bet_int
            self.change_balance(True, win_sum)
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['min']*bet_int))
            self.game_list.append(self.print_result_line(True, "СРЕДНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['middle']*bet_int))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['max']*bet_int))
            win_line = "Средняя линия"
        elif win_line == "Верхняя линия":
            win_sum = current_sum_bet['max'] * 3 * bet_int
            self.change_balance(True, win_sum)
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['min']*bet_int))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['middle']*bet_int))
            self.game_list.append(self.print_result_line(True, "ВЕРХНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['max']*bet_int))
            win_line = "Верхняя линия"
        else:
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['min']*bet_int))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['middle']*bet_int))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['max']*bet_int))
            win_line = "Выпал 0"
        return win_line

    def check_lines_win_middle0_block_retro(self, current_sum_bet, bet, win_number):
        self.game_list.append("---")
        win_line = ''
        bet_int = int(bet)
        if win_number != 0:
            for elem in cnfg.first12:
                if elem == win_number:
                    win_sum = current_sum_bet['min'] * 3 * bet_int
                    self.change_balance(True, win_sum)
                    self.game_list.append(
                        self.print_result_line(True, "ПЕРВЫЕ 12", "ПЕРВЫЕ 12", current_sum_bet['min'] * bet_int,win_number))
                    self.game_list.append(
                        self.print_result_line(False, "ВТОРЫЕ 12", "ПЕРВЫЕ 12", current_sum_bet['middle'] * bet_int,win_number))
                    self.game_list.append(
                        self.print_result_line(False, "ТРЕТЬИ 12", "ПЕРВЫЕ 12", current_sum_bet['max'] * bet_int,win_number))
                    win_line = "Первые 12"
            for elem in cnfg.second12:
                if elem == win_number:
                    win_sum = current_sum_bet['middle'] * 3 * bet_int
                    self.change_balance(True, win_sum)
                    self.game_list.append(
                        self.print_result_line(False, "ПЕРВЫЕ 12", "ВТОРЫЕ 12", current_sum_bet['min'] * bet_int,win_number))
                    self.game_list.append(
                        self.print_result_line(True, "ВТОРЫЕ 12", "ВТОРЫЕ 12", current_sum_bet['middle'] * bet_int,win_number))
                    self.game_list.append(
                        self.print_result_line(False, "ТРЕТЬИ 12", "ВТОРЫЕ 12", current_sum_bet['max'] * bet_int,win_number))
                    win_line = "Вторые 12"
            for elem in cnfg.third12:
                if elem == win_number:
                    win_sum = current_sum_bet['max'] * 3 * bet_int
                    self.change_balance(True, win_sum)
                    self.game_list.append(
                        self.print_result_line(False, "ПЕРВЫЕ 12", "ТРЕТЬИ 12", current_sum_bet['min'] * bet_int,win_number))
                    self.game_list.append(
                        self.print_result_line(False, "ВТОРЫЕ 12", "ТРЕТЬИ 12", current_sum_bet['middle'] * bet_int,win_number))
                    self.game_list.append(
                        self.print_result_line(True, "ТРЕТЬИ 12", "ТРЕТЬИ 12", current_sum_bet['max'] * bet_int,win_number))
                    win_line = "Третьи 12"
        else:
            self.game_list.append(
                self.print_result_line(False, "ПЕРВЫЕ 12", "Выпало 0", current_sum_bet['min'] * bet_int,win_number))
            self.game_list.append(
                self.print_result_line(False, "ВТОРЫЕ 12", "Выпало 0", current_sum_bet['middle'] * bet_int,win_number))
            self.game_list.append(
                self.print_result_line(False, "ТРЕТЬИ 12", "Выпало 0", current_sum_bet['max'] * bet_int,win_number))
            win_line = "Выпал 0"
        return win_line

    def check_lines_win_middle0_lines_retro(self, current_sum_bet, bet, win_number):
        self.game_list.append("---")
        win_line = ''
        bet_int = int(bet)
        if win_number != 0:
            for elem in cnfg.min_line:
                if elem == win_number:
                    win_sum = current_sum_bet['min'] * 3 * bet_int
                    self.change_balance(True, win_sum)
                    self.game_list.append(self.print_result_line(True, "НИЖНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['min']*bet_int,win_number))
                    self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['middle']*bet_int,win_number))
                    self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['max']*bet_int,win_number))
                    win_line = "Нижняя линия"
            for elem in cnfg.middle_line:
                if elem == win_number:
                    win_sum = current_sum_bet['middle'] * 3 * bet_int
                    self.change_balance(True, win_sum)
                    self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['min']*bet_int,win_number))
                    self.game_list.append(self.print_result_line(True, "СРЕДНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['middle']*bet_int,win_number))
                    self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['max']*bet_int,win_number))
                    win_line = "Средняя линия"
            for elem in cnfg.max_line:
                if elem == win_number:
                    win_sum = current_sum_bet['max'] * 3 * bet_int
                    self.change_balance(True, win_sum)
                    self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['min']*bet_int,win_number))
                    self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['middle']*bet_int,win_number))
                    self.game_list.append(self.print_result_line(True, "ВЕРХНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['max']*bet_int,win_number))
                    win_line = "Верхняя линия"
        else:
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['min']*bet_int,win_number))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['middle']*bet_int,win_number))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['max']*bet_int,win_number))
            win_line = "Выпал 0"
        return win_line

    def check_lines_win_retro(self, current_sum_bet, win_number):
        self.game_list.append("---")
        win_line = ''
        if win_number != 0:
            for elem in cnfg.min_line:
                if elem == win_number:
                    win_sum = current_sum_bet['min'] * 3
                    self.change_balance(True, win_sum)
                    self.game_list.append(self.print_result_line(True, "НИЖНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['min'],win_number))
                    self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['middle'],win_number))
                    self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ", current_sum_bet['max'],win_number))
                    win_line = "Нижняя линия"
            for elem in cnfg.middle_line:
                if elem == win_number:
                    win_sum = current_sum_bet['middle'] * 3
                    self.change_balance(True, win_sum)
                    self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['min'],win_number))
                    self.game_list.append(self.print_result_line(True, "СРЕДНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['middle'],win_number))
                    self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ", current_sum_bet['max'],win_number))
                    win_line = "Средняя линия"
            for elem in cnfg.max_line:
                if elem == win_number:
                    win_sum = current_sum_bet['max'] * 3
                    self.change_balance(True, win_sum)
                    self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['min'],win_number))
                    self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['middle'],win_number))
                    self.game_list.append(self.print_result_line(True, "ВЕРХНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ", current_sum_bet['max'],win_number))
                    win_line = "Верхняя линия"
        else:
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['min'],win_number))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['middle'],win_number))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", "Выпало 0", current_sum_bet['max'],win_number))
            win_line = "Выпал 0"
        return win_line

    def check_lines_win(self, current_sum_bet):
        win_line = self.random_line()
        self.game_list.append("---")
        if win_line == "Нижняя линия":
            win_sum = current_sum_bet['min'] * 3
            self.change_balance(True,win_sum)
            self.game_list.append(self.print_result_line(True, "НИЖНЯЯ ЛИНИЯ", win_line, current_sum_bet['min']))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", win_line, current_sum_bet['middle']))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", win_line, current_sum_bet['max']))
        elif win_line == "Средняя линия":
            win_sum = current_sum_bet['middle'] * 3
            self.change_balance(True, win_sum)
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", win_line, current_sum_bet['min']))
            self.game_list.append(self.print_result_line(True, "СРЕДНЯЯ ЛИНИЯ", win_line, current_sum_bet['middle']))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", win_line, current_sum_bet['max']))
        elif win_line == "Верхняя линия":
            win_sum = current_sum_bet['max'] * 3
            self.change_balance(True, win_sum)
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", win_line, current_sum_bet['min']))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", win_line, current_sum_bet['middle']))
            self.game_list.append(self.print_result_line(True, "ВЕРХНЯЯ ЛИНИЯ", win_line, current_sum_bet['max']))
        else:
            self.game_list.append(self.print_result_line(False, "НИЖНЯЯ ЛИНИЯ", win_line, current_sum_bet['min']))
            self.game_list.append(self.print_result_line(False, "СРЕДНЯЯ ЛИНИЯ", win_line, current_sum_bet['middle']))
            self.game_list.append(self.print_result_line(False, "ВЕРХНЯЯ ЛИНИЯ", win_line, current_sum_bet['max']))
        return win_line

    def print_result_line(self, state, name, win_line, sum_bet,win_number=''):
        if state == True:
            return f'Выпало {str(win_number)} {win_line}. Победа по ставке на {name}, сумма ставки: {sum_bet}, текущий баланс: {self.balance}'
        else:
            return f'Выпало {str(win_number)} {win_line}. Проигрыш по ставке на {name}, сумма ставки: {sum_bet}, текущий баланс: {self.balance}'

    def check_color_win_retro(self, last_bet, current_bet, win_number):
        win_color = ''
        if win_number != 0:
            for elem in cnfg.black:
                if elem == win_number:
                    win_color = 'ЧЕРНОЕ'
            for elem in cnfg.red:
                if elem == win_number:
                    win_color = 'КРАСНОЕ'
        else:
            win_color = 'ЗЕЛЕНОЕ'
        if last_bet == win_color:
            win_sum = current_bet * 2
            self.change_balance(True,win_sum)
            self.game_list.append(f'Выпало {win_number} {win_color}.Победа по ставке на {last_bet}, сумма ставки: {current_bet}, текущий баланс: {self.balance}')
        else:
            #return f'Победа по ставке на {win_color}, текущий баланс: {current_balance + current_bet}'
            self.game_list.append(f'Выпало {win_number} {win_color}. Проигрыш по ставке на {last_bet}, сумма ставки: {current_bet}, текущий баланс: {self.balance}')
        return win_color

    def check_color_win(self, last_bet, current_bet):
        win_color = self.random_colour()
        if last_bet == win_color:
            win_sum = current_bet * 2
            self.change_balance(True,win_sum)
            self.game_list.append(f'Выпало {win_color}.Победа по ставке на {last_bet}, сумма ставки: {current_bet}, текущий баланс: {self.balance}')
        else:
            #return f'Победа по ставке на {win_color}, текущий баланс: {current_balance + current_bet}'
            self.game_list.append(f'Выпало {win_color}. Проигрыш по ставке на {last_bet}, сумма ставки: {current_bet}, текущий баланс: {self.balance}')
        return win_color
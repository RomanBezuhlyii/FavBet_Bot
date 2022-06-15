import datetime


class Lines3:
    dict = {'min': 0, 'middle': 0, 'max': 0}
    lines3_down_state = list()
    lines3_middle_state = list()
    lines3_top_state = list()
    min_bet_int = 0
    lines_2_or_3 = 0


    def print_result_line(self, balance, state, name, win_line, sum_bet,win_number=''):
        if state == True:
            return f'{str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))} Выпало {win_number} {win_line}. Победа по ставке на {name}, сумма ставки: {str(sum_bet)}, текущий баланс: {balance}'
        else:
            return f'{str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))} Выпало {win_number} {win_line}. Проигрыш по ставке на {name}, сумма ставки: {str(sum_bet)}, текущий баланс: {balance}'

    def lines3_up(self, min, middle, max):
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

    def lines3_bet(self, win_line):
        if win_line == "Нижняя линия":
            self.lines3_check_win(self.lines3_down_state)
        elif win_line == "Средняя линия":
            self.lines3_check_win(self.lines3_middle_state)
        elif win_line == "Верхняя линия":
            self.lines3_check_win(self.lines3_top_state)
        self.reset_dict()
        for elem in self.lines3_down_state:
            self.dict['min'] += elem
        for elem in self.lines3_middle_state:
            self.dict['middle'] += elem
        for elem in self.lines3_top_state:
            self.dict['max'] += elem

    def lines3(self, balance, last_win_line):
        if balance < self.min_bet_int:
            return 'На балансе недостаточно средств для ставки'
        else:
            #self.lines3_win_line = last_win_line
            if len(self.lines3_down_state) == 0 and len(self.lines3_middle_state) == 0 and len(self.lines3_top_state) == 0:
                self.lines3_up(True,True,True)
            else:
                if last_win_line == "Нижняя линия":
                    self.lines3_up(False,True,True)
                elif last_win_line == "Средняя линия":
                    self.lines3_up(True, False, True)
                elif last_win_line == "Верхняя линия":
                    self.lines3_up(True,True,False)
                else:
                    self.lines3_up(True,True,True)
            self.lines3_bet(last_win_line)
        return self.dict

    '''def do_lines3_bet(self,web, user_bet, username,user: params.UserParameters):
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
                self.min_bet.click()
                if len(self.lines3_down_state)==0 and len(self.lines3_middle_state)==0 and len(self.lines3_top_state)==0:
                    self.lines3_up()
                self.lines3_bet(web)
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
                        mass.append(self.print_result_line(bal, True, "НИЖНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ",sum(self.lines3_down_state), text))
                        mass.append(self.print_result_line(bal, False, "СРЕДНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ",sum(self.lines3_middle_state), text))
                        mass.append(self.print_result_line(bal, False, "ВЕРХНЯЯ ЛИНИЯ", "НИЖНЯЯ ЛИНИЯ",sum(self.lines3_top_state), text))
                        mass.append("---")
                        cnfg.bet_information_dict[username].append(mass)
                        self.lines3_win_line = "НИЖНЯЯ"
                        self.lines3_up()
                        # status_info = status_info + ', Победа по нижней линии. Ставка: ' + str(self.line_bet['min']) + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        # self.reset_lines_params()
                        count_wins = 1
                for num in cnfg.middle_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        # status_info = status_info + ', Победа по средней линии' + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        mass.append("---")
                        mass.append(self.print_result_line(bal, False, "НИЖНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ",sum(self.lines3_down_state), text))
                        mass.append(self.print_result_line(bal, True, "СРЕДНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ",sum(self.lines3_middle_state), text))
                        mass.append(self.print_result_line(bal, False, "ВЕРХНЯЯ ЛИНИЯ", "СРЕДНЯЯ ЛИНИЯ",sum(self.lines3_top_state), text))
                        mass.append("---")
                        cnfg.bet_information_dict[username].append(mass)
                        self.lines3_win_line = "СРЕДНЯЯ"
                        self.lines3_up()
                for num in cnfg.max_line:
                    if int(first_txt) == num:
                        print('Выигрыш')
                        # status_info = status_info + ', Победа по верхней линии' + ". Баланс: " + str(self.check_balance(web)) + " грн."
                        mass.append("---")
                        mass.append(self.print_result_line(bal, False, "НИЖНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ",sum(self.lines3_down_state), text))
                        mass.append(self.print_result_line(bal, False, "СРЕДНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ",sum(self.lines3_middle_state), text))
                        mass.append(self.print_result_line(bal, True, "ВЕРХНЯЯ ЛИНИЯ", "ВЕРХНЯЯ ЛИНИЯ",sum(self.lines3_top_state), text))
                        mass.append("---")
                        cnfg.bet_information_dict[username].append(mass)
                        self.lines3_win_line = "ВЕРХНЯЯ"
                        self.lines3_up()
                if first_txt == '0':
                    # status_info = status_info + ', Проигрыш'
                    mass.append("---")
                    mass.append(self.print_result_line(bal, False, "НИЖНЯЯ ЛИНИЯ", " ",sum(self.lines3_down_state), text))
                    mass.append(self.print_result_line(bal, False, "СРЕДНЯЯ ЛИНИЯ", " ",sum(self.lines3_middle_state), text))
                    mass.append(self.print_result_line(bal, False, "ВЕРХНЯЯ ЛИНИЯ", " ",sum(self.lines3_top_state), text))
                    mass.append("---")
                    cnfg.bet_information_dict[username].append(mass)
                    self.lines3_win_line = "0"
                    self.lines3_up()
                user.bet_info_field = status_info
                # cnfg.bet_information_dict[username].append(status_info)
                self.check_bet_status = 0'''

    def reset_dict(self):
        self.dict['min'] = 0
        self.dict['middle'] = 0
        self.dict['max'] = 0

    def reset_lines3(self):
        self.reset_dict()
        self.lines3_win_line = ''
        self.lines3_down_state.clear()
        self.lines3_top_state.clear()
        self.lines3_middle_state.clear()
        self.lines_2_or_3 = 0
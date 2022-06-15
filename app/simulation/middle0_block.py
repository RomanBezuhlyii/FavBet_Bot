class Middle0Block:
    snl = 0
    ssl = 0
    svl = 0
    middle0_lines_dict = {'Первые 12': 'МИНИМУМ', 'Вторые 12': 'СРЕДНЕ', 'Третьи 12': 'МАКСИМУМ', 'Выпал 0': 'НОЛЬ'}
    middle0_lines_bet_dict = {'МИНИМУМ': 0, 'СРЕДНЕ': 0, 'МАКСИМУМ': 0}
    min_bet_int = 0
    start_game = False
    dict = {'min': 0, 'middle': 0, 'max': 0}
    count_SL = 0
    middle_line = ''

    def middle0_bets_in_line(self, c_snl, c_ssl, c_svl):
        self.snl = c_snl
        self.ssl = c_ssl
        self.svl = c_svl
        self.middle0_lines_bet_dict['МИНИМУМ'] = self.snl
        self.middle0_lines_bet_dict['СРЕДНЕ'] = self.ssl
        self.middle0_lines_bet_dict['МАКСИМУМ'] = self.svl
        self.dict['min'] = self.middle0_lines_bet_dict[self.middle0_lines_dict['Первые 12']]
        self.dict['middle'] = self.middle0_lines_bet_dict[self.middle0_lines_dict['Вторые 12']]
        self.dict['max'] = self.middle0_lines_bet_dict[self.middle0_lines_dict['Третьи 12']]

    def middle0_logic(self,win_line):
        if win_line == 'МАКСИМУМ':
            self.count_SL = 0
            self.middle0_bets_in_line(c_snl=2,
                                      c_ssl=0,
                                      c_svl=3)
        elif win_line == 'МИНИМУМ':
            self.count_SL = 0
            if self.snl == 0:
                self.middle0_bets_in_line(c_snl=2*self.ssl,
                                          c_ssl=0,
                                          c_svl=2*self.svl)
            else:
                self.middle0_bets_in_line(c_snl=self.snl,
                                          c_ssl=self.ssl,
                                          c_svl=self.svl)
        elif win_line == 'СРЕДНЕ':
            if self.count_SL == 0:
                self.count_SL += 1
                self.middle0_bets_in_line(c_snl=2*self.snl,
                                          c_ssl=0,
                                          c_svl=2*self.svl)
            elif self.count_SL == 1:
                self.count_SL += 1
                self.middle0_bets_in_line(c_snl=0,
                                          c_ssl=2*self.snl,
                                          c_svl=2*self.svl)
            elif self.count_SL == 2:
                self.count_SL = 0
                self.middle0_bets_in_line(c_snl=self.ssl,
                                          c_ssl=0,
                                          c_svl=self.svl)
        elif win_line == 'НОЛЬ':
            self.count_SL = 0
            if self.ssl == 0:
                self.middle0_bets_in_line(c_snl=2*self.snl,
                                          c_ssl=self.ssl,
                                          c_svl=2*self.svl)
            else:
                self.middle0_bets_in_line(c_snl=2*self.ssl,
                                          c_ssl=0,
                                          c_svl=2*self.svl)


    def do_middle0_bet(self,balance, last_win_line):
        count_wins = 0
        status_info = ''
        if balance < self.min_bet_int:
            return 'На балансе недостаточно средств для ставки'
        else:
            if self.start_game == False:
                self.set_middle0_middle_line(self.middle_line)
                self.start_game = True
            if self.snl==0 and self.ssl==0 and self.svl==0:
                self.middle0_bets_in_line(c_snl=2,
                                            c_ssl=0,
                                            c_svl=3)
            else:
                self.middle0_logic(self.middle0_lines_dict[last_win_line])
        return self.dict


    def set_middle0_lines(self, min_name, middle_name, max_name):
        self.middle0_lines_dict['Первые 12'] = min_name
        self.middle0_lines_dict['Вторые 12'] = middle_name
        self.middle0_lines_dict['Третьи 12'] = max_name
        self.middle0_lines_dict['Выпал 0'] = 'НОЛЬ'

    def set_middle0_middle_line(self, middle_line):
        if middle_line == 'min':
            self.set_middle0_lines('СРЕДНЕ', 'МИНИМУМ', 'МАКСИМУМ')
        elif middle_line == 'middle':
            self.set_middle0_lines('МИНИМУМ', 'СРЕДНЕ', 'МАКСИМУМ')
        elif middle_line == 'max':
            self.set_middle0_lines('МИНИМУМ', 'МАКСИМУМ', 'СРЕДНЕ')

    def middle0_reset(self):
        self.snl = 0
        self.ssl = 0
        self.svl = 0
        self.middle0_lines_dict = {'Первые 12': 'МИНИМУМ', 'Вторые 12': 'СРЕДНЕ', 'Третьи 12': 'МАКСИМУМ', 'Выпал 0': 'НОЛЬ'}
        self.middle0_lines_bet_dict = {'МИНИМУМ': 0, 'СРЕДНЕ': 0, 'МАКСИМУМ': 0}
        self.min_bet_int = 0
        self.start_game = False
        self.dict = {'min': 0, 'middle': 0, 'max': 0}
        self.count_SL = 0
        self.middle_line = ''
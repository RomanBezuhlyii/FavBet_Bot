min_line = [1,4,7,10,13,16,19,22,25,28,31,34]
middle_line = [2,5,8,11,14,17,20,23,26,29,32,35]
max_line = [3,6,9,12,15,18,21,24,27,30,33,36]

class Lines:
    lines_bets_state = list()

    def start_lines_bet(self, min_bet):
        bets = dict()
        bets['min'] = min_bet
        bets['middle'] = min_bet * 2
        bets['max'] = min_bet * 3
        return bets

    def lines_bet(self, min_bet):
        dict = self.start_lines_bet(min_bet)
        for elem in self.lines_bets_state:
            if elem == '+':
                dict['min'] += min_bet
            if elem == 'x2':
                dict['min'] *= 2
                dict['middle'] *= 2
                dict['max'] *= 2
        return dict

    def lines(self, balance, min_bet, last_win_line):
        count_wins = 0
        if balance < int(min_bet):
            return 'На балансе недостаточно средств для ставки'
        else:
            if last_win_line == "Нижняя линия":
                #lines_bets_state.clear()
                pass
            elif last_win_line == "Средняя линия" or last_win_line == "Верхняя линия":
                self.lines_bets_state.append('+')
            elif last_win_line == "Выпал 0":
                self.lines_bets_state.append('x2')
            dict = self.lines_bet(min_bet)
            return dict

    def reset_parameters(self):
        self.lines_bets_state.clear()

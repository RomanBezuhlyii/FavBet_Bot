import datetime
import random

cnt_red = 0
cnt_black = 0
black_red_circle = 0
win_bet = ''
last_color_bet = ''
lines_bets_state = list()
balance = 0
current_sum_bet = 0

class Colors:
    cnt_red = 0
    cnt_black = 0
    black_red_circle = 0
    win_bet = ''
    last_color_bet = ''
    lines_bets_state = list()
    balance = 0
    current_sum_bet = 0
    anti_color_tuple = ('КРАСНОЕ', 'ЧЕРНОЕ')

    def reset_all_params(self):
        self.cnt_red = 0
        self.cnt_black = 0
        self.black_red_circle = 0
        self.win_bet = ''
        self.last_color_bet = ''
        self.lines_bets_state.clear()
        self.balance = 0
        self.current_sum_bet = 0

    def bet_on_red(self, win_colour, default_sum_bet):
        self.cnt_red += 1
        if win_colour == self.last_color_bet:
            #print("Ставка выиграла. Начинаем сначала")
            self.black_red_circle = 0
            self.current_sum_bet = default_sum_bet
            self.last_color_bet = "КРАСНОЕ"
        else:
            #print("Ставка проиграла, удваиваем ставку")
            self.current_sum_bet = default_sum_bet
            for i in range(self.black_red_circle):
                self.current_sum_bet = self.current_sum_bet * 2
            self.last_color_bet = "КРАСНОЕ"

    def bet_on_black(self, win_colour, default_sum_bet):
        self.cnt_black += 1
        if win_colour == self.last_color_bet:
            #print("Ставка выиграла. Начинаем сначала")
            self.black_red_circle = 0
            self.current_sum_bet = default_sum_bet
            self.last_color_bet = "ЧЕРНОЕ"
        else:
            #print("Ставка проиграла, удваиваем ставку")
            self.current_sum_bet = default_sum_bet
            for i in range(self.black_red_circle):
                self.current_sum_bet = self.current_sum_bet * 2
            self.last_color_bet = "ЧЕРНОЕ"

    def zeroing(self, win_colour, default_bet):
        self.cnt_black = 0
        self.cnt_red = 0
        #current_sum_bet = default_bet
        #print("Цикл ставок окончен")
        self.bet_on_black(win_colour, default_bet)

    def red_black(self, win_colour, default_bet):
        if self.cnt_red == 0 and self.cnt_black == 0:
            self.bet_on_black(win_colour, default_bet)
        elif self.cnt_black < 2:
            self.bet_on_black(win_colour, default_bet)
        elif self.cnt_red < 2:
            self.bet_on_red(win_colour, default_bet)
        else:
            self.zeroing(win_colour, default_bet)

    def set_current_colour(self):
        color_num = random.randrange(0, 2)
        return self.anti_color_tuple[color_num]

    def do_bet(self, win_color, default_bet, balance, mode):
        status_bet = ''
        my_bet = ''
        if balance < int(default_bet):
            return 'На балансе недостаточно средств для ставки'
        else:
            if mode == 'anti':
                color = self.set_current_colour()
                if color == 'КРАСНОЕ':
                    self.bet_on_red(win_color, default_bet)
                elif color == 'ЧЕРНОЕ':
                    self.bet_on_black(win_color, default_bet)
            elif mode == 'color':
                self.red_black(win_color, default_bet)
            self.black_red_circle += 1
            data = dict()
            data['bet_color'] = self.last_color_bet
            data['bet_sum'] = self.current_sum_bet
            return data

    def reset_parameters(self):
        self.balance = 0
        self.current_sum_bet = 0
        self.cnt_red = 0
        self.cnt_black = 0
        self.black_red_circle = 0
        self.win_bet = ''
        self.last_color_bet = ''
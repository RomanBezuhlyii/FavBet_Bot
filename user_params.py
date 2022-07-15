class UserParameters:
    username = ''
    game_state = False
    bot_state_flag = False
    final_time = ''
    bet_adress = ''
    message_count = -1
    last_res = ''
    info_state = ''
    strategy = ''
    game_active = 'active'
    game_disabled = 'disabled'
    no_balance_bet = 'Ставка'
    bet_info_field = ''
    login_state = ''
    bet_info = list()
    one_bet_info = list()
    mass = ["Бот запущен, информация отобразится после первой ставки"]
    middle0_line = ''
    middle0_block = ''

    def __init__(self, username):
        self.username = username

    def reset_parameters(self):
        self.username = ''
        self.game_state = False
        self.bot_state_flag = False
        self.final_time = ''
        self.bet_adress = ''
        self.message_count = -1
        self.info_state = ''
        self.strategy = ''
        self.game_active = ''
        self.game_disabled = ''
        self.no_balance_bet = 'Ставка'
        self.bet_info_field = ''
        self.middle0_line = ''
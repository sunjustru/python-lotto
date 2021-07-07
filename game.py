import random
import numpy as np

# Карточка лотто
class Card:
    __nums = [itm for itm in range(1, 90)]
    def __init__(self):
        self.cols = 9
        self.rows = 3

    # Создаём карточку
    @property
    def set_card(self):
        matrix = np.array(random.sample(self.__nums, self.cols * self.rows)).reshape(self.rows, self.cols)
        matrix = np.array(([sorted(itm) for itm in matrix]), int)
        for itm in matrix:
            i = 0
            while i < 4:
                k = random.randint(0, 8)
                if itm[k] != 0:
                    itm[k] = 0
                    i += 1
        return matrix

# Игроки
class Player(Card):

    def __init__(self, name, bot='n'):
        Card.__init__(self)
        self.name = name

        # Определяем бот или не бот
        if bot == 'y':
            self.player_type = 1
        else:
            self.player_type = 0

        # Получаем карточку игрока
        self.card = self.get_card

    @property
    def get_card(self):
        return self.set_card

# Сама игра
class Lotto:
    __nums = [itm for itm in range(1, 90)]

    def __init__(self):
        self.players = []
        self.players_answer = []

    def __add__(self, other):
        self.players.append(other)

    # Возвращаем случайное число (бочёнок)
    @property
    def get_num(self):
        # Кол-во ходов
        self.count_steps = len(self.__nums)
        # случайное число
        self.num = random.choice(self.__nums)
        # удаляем число из списка
        self.__nums.remove(self.num)

    def check_card(self):
        self.players_count = len(self.players)
        self.win = []

        for key, player in enumerate(self.players):
            # если БОТ
            if player.player_type == 0:
                if self.num in player.card:
                    result = np.where(player.card == self.num)
                    player.card[result] = -1

                    # Проверяем победитель или нет
                    if player.card.sum() == -15:
                        # Если сумма -15 значений в матрице, то добавляем игрока в победители
                        self.win.append(player.name)

            # если НЕ БОТ
            else:
                if self.num in player.card:
                    # Делаем поиск в матрице есть возвращаем ключ x,y
                    result = np.where(player.card == self.num)
                    if self.players_answer[key] == 'y':
                        player.card[result] = -1

                        # Проверяем победитель или нет
                        if player.card.sum() == -15:
                            # Если сумма -15 значений в матрице, то добавляем игрока в победители
                            self.win.append(player.name)

                    else:
                        if self.players_count > 1:
                            mes = f'Игрок: {key} с имянем {player.name} — проиграл и выбывает из игры!'
                            print(mes)
                            # Удаляем объект пользователя
                            self.players.pop(key)
                        break
                else:
                    if self.players_answer[key] == 'y':
                        if self.players_count >= 2:
                            mes = f'Игрок: {key} с имянем {player.name} — проиграл и выбывает из игры!'
                            print(mes)
                            # Удаляем объект пользователя
                            self.players.pop(key)
                        else:
                            mes = f'Игрок: {key} с имянем {player.name} — проиграл!'
                            print(mes)
                            self.players.pop(key)


        # Очищаем список
        self.players_answer.clear()

        if self.players_count == 0:
            print('Игроков для игры нет')
            return False

    @property
    def __render_card(self):
        text = ''
        for i in self.players:
            if i.player_type == 0:
                text = text + f'------ Компьютер {i.name}------\n'
            else:
                text = text + f'------ Игрок {i.name}------\n'

            for x in i.card:
                for itm in x:
                    if itm == 0:
                        text = text + (' ' * 2)
                    elif itm == -1:
                        text = text + ' —— '
                    else:
                        if len(str(itm)) == 2:
                            text = text + ' ' + str(itm) + ' '
                        else:
                            text = text + '  ' + str(itm) + ' '

                text = text + '\n'
            text = text + '######\n'
        print(text)

    @property
    def play_game(self):
        self.get_num # получаем случайное число self.num и удаляем его из списка self.__nums

        # Выводим карточки игроков с применением декорирования
        self.__render_card

        print(f'Кол-во ходов: {self.count_steps}')

        # Обходим список игроков и уточняем у не бота есть число или нет
        for key, player in enumerate(self.players):

            # Если не компьютер
            if player.player_type == 1:
                temp = input(f'Игрок ({player.name}) — Число ({self.num}) есть у вас? (y/n):\n')
                # Создаём список где ключ игрок; его имя и ответ (вставил ключ как ID) так как имя может быть не уникальным
                self.players_answer.insert(key, temp)
            else:
                self.players_answer.insert(key, 'no')

        # Делаем проверку ошибся/сь игрок/и или нет
        if self.check_card() == False:
            return False

        if len(self.win) > 0:
            for itm in self.win:
                print(f'Победил: {itm}')
                return False

cls = Lotto()

while True:
    count_players = int(input('Сколько игроков? (Укажите целое число кол-во, проверку на число я не вставлял)\n'))
    i = 1
    while i <= count_players:
        player_name = input(f'Укажите Имя игрока — {i}: ')
        player_type = input(f'{player_name} — Реальный игрок или компьютер? (y/n): ')

        # создаём игрока
        player = Player(player_name, player_type)
        cls + player
        i = i + 1
    break

while True:
    if cls.play_game == False:
        break

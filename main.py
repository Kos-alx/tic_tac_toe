import random


# Функция, которая выводит текущее состояние поля
def print_field():
    print('    A   B   C')
    for row in range(len(FIELD)):
        print(str(row + 1) + ' ', *FIELD[row])
    print()


# Функция, которая переводит координаты кортежа (0,0)-(3,3) в координаты формата A1-C3
def coo_to_coo(turn):
    for k, v in c_d.items():
        if turn == v:
            return k


# Функция, которая проверяет правильность вводимых данных игроком
def check_turn(turn):
    if turn not in ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']:
        print(
            'Нужно ввести координаты в формате A1, B3. Английские буквы (A, B, C) и цифры (1, 2, 3).'
            ' Попробуйте еще раз.'
        )
        print()
        return False
    elif FIELD[c_d[turn][0]][c_d[turn][1]] != '[ ]':
        print('Данное поле занято, попробуйте еще раз')
        print()
        return False
    return True


# Функция, которая выставляет на поле FIELD крестик или нолик
def turn_player(trn, sign):
    FIELD[c_d[trn][0]][c_d[trn][1]] = sign


# Функция, которая проверяет, победный ли ход у игрока
def player_win(sign):
    binary_matrix = []
    for i in range(3):
        tmp = []
        for j in range(3):
            if FIELD[i][j] == sign:
                tmp.append(1)
            else:
                tmp.append(0)
        binary_matrix.append(tmp)

    for row in w_f_coord:
        count = 0
        for item in row:
            count += binary_matrix[item[0]][item[1]]
        if count == 3:
            return True


# Функция, которая определяет, кто будет ходить первым
def first_player():
    while True:
        coin = input('О/Р: ').upper()
        if coin not in ['О', 'Р', 'O', 'P']:
            print('Нужно выбрать О и Р')
        else:
            break
    if coin in random.choice([['O', 'О'], ['P', 'Р']]):
        return '[X]', '[O]'
    else:
        return '[O]', '[X]'


# Функция, которая проверяет, можно ли текущим ходом завершить игру или отвратить поражение.
def check_win_fail(sign):
    # проверка каким знаком идет игра
    if sign == '[X]':
        vs_sign = '[O]'
    else:
        vs_sign = '[X]'

    # создаем матрицу на базе FIELDS: 1 - наша метка, 0 - пустое поле, -1 метка противника
    binary_matrix = []
    for i in range(3):
        tmp = []
        for j in range(3):
            if FIELD[i][j] == sign:
                tmp.append(1)
            elif FIELD[i][j] == vs_sign:
                tmp.append(-1)
            else:
                tmp.append(0)
        binary_matrix.append(tmp)

    # Проверяем есть ли возможность поставит выигрышный ход. Функция выдаст ход
    for row in w_f_coord:
        count = 0
        for item in row:
            if binary_matrix[item[0]][item[1]] == 0:
                empty_sign = item
            count += binary_matrix[item[0]][item[1]]
        if count == 2:
            return empty_sign, 'win'

    for row in w_f_coord:
        count = 0
        for item in row:
            if binary_matrix[item[0]][item[1]] == 0:
                empty_sign = item
            count += binary_matrix[item[0]][item[1]]
        if count == -2:
            return empty_sign, None
            # противнику.


# Функция, которая описывает логику хода компьютера
def turn_comp(sign):
    check = check_win_fail(sign)

    if dif_level == '1':
        if check:
            return coo_to_coo(check[0]), check[1]
        else:
            return random.choice(cells), 0

    if not check:
        if FIELD[1][1] == '[ ]':
            return 'B2', 0
    else:
        return coo_to_coo(check[0]), check[1]

    ma_x = 0
    turn = ''
    for i in ['A1', 'A3', 'C1', 'C3']:
        if i in cells:
            if ma_x < abs(ord(i[0]) - ord(last_turn[0])) + abs(int(i[1]) - int(last_turn[1])):
                ma_x = abs(ord(i[0]) - ord(last_turn[0])) + abs(int(i[1]) - int(last_turn[1]))
                turn = i
    if turn:
        return turn, 0
    else:
        return random.choice(cells), 0


# Генерируем пустое поле
FIELD = [['[ ]' for i in '123'] for i in '123']
# Словарь с координатами
c_d = {
    'A1': (0, 0), 'A2': (1, 0), 'A3': (2, 0),
    'B1': (0, 1), 'B2': (1, 1), 'B3': (2, 1),
    'C1': (0, 2), 'C2': (1, 2), 'C3': (2, 2)
}

ttt_dct = {'[X]': 'крестик', '[O]': 'нолик'}

w_f_coord = [
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
]

print('Приветствую игрок. Сейчас мы будем играть в крестики-нолики.')
print('Для начала выберем уровень сложности 1 - легкий, 2 - сложный')
# На уровне сложности 2 - компьютер не может проиграть
# На уровне сложности 1 - компьютер пытается выиграть текущим ходом, или не допустить поражения на следующем ходу
# Первые ходы на уровне сложности 1 у компьютера случайные.
while True:
    dif_level = input()
    if dif_level in ['1', '2']:
        break
    else:
        print('Нужно верно указать уровень сложности. 1 или 2')
print('Сейчас определим, кто будет ходить первым. Кинем виртуальную монету.')
print('Выбери: Орел (буква О) или решка (буква Р)')

# пока отключаем выбор первого игрока.
signs = first_player()
sign, computer_sign = signs[0], signs[1]
player_turn = False

if sign == '[X]':
    print('Вам достаются крестики, Вы ходите первый')
    player_turn = True
    print_field()
else:
    print('У Вас нолики, первым будет ходить компьютер')


cells = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

while cells:
    if player_turn:
        while True:
            print('Введите координаты, где Вы поставите', ttt_dct[sign])
            trn = input().upper()
            if not check_turn(trn):
                continue
            turn_player(trn, sign)
            last_turn = trn
            cells.remove(trn)
            player_turn = not player_turn
            print_field()
            break
        if player_win(sign):
            print('Ура, Вы победили!!!')
            trn = 'player', 'win'
            break
    else:
        trn = turn_comp(computer_sign)
        turn_player(trn[0], computer_sign)
        last_turn = trn[0]
        cells.remove(trn[0])
        player_turn = not player_turn
        print_field()
        if trn[1] == 'win':
            print('Игра окончена, победу одержал компьютер')
            break
if trn[1] != 'win':
    print('Ничья')

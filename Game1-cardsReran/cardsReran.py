import random

# Список участников
with open('Participant.txt', encoding='utf-8') as f:
    participants = sorted([name.strip() for name in f])

# Создание колоды
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']
suits = ['♠', '♣', '♥', '♦']
cards = [f'{rank} {suit}' for suit in suits for rank in ranks] + ['Джокер', 'Джокер']

random.shuffle(cards)

# Словарь хранения закреплённых карт
assigned_cards = {}

# Раздача карт
for i, participant in enumerate(participants):
    num = i + 1
    if cards:
        card = cards.pop()
        assigned_cards[participant] = card
        print(f'{num}. {participant}: {card}')
    else:
        print('Колода закончилась')
        break

# Процесс перевыбора карт
print('Участники, которым не нравится их карта, могут её перевыбрать.')
while True:
    need_to_change = input('Введите номера участников, которые хотят сменить карту (через запятую) или нажмите Enter, чтобы продолжить: ')
    if not need_to_change:
        break
    need_to_change = [int(x.strip()) for x in need_to_change.split(',')]
    for num in need_to_change:
        if num <= len(participants):
            participant = participants[num-1]
            if participant in assigned_cards:
                current_card = assigned_cards[participant]
                cards.append(current_card)
                random.shuffle(cards)
                while True:
                    new_card = cards.pop()
                    if new_card not in assigned_cards.values():
                        break
                assigned_cards[participant] = new_card
                print(f'Новая карта для {participant}: {new_card}')
            else:
                print(f'Участник {num} не получил карту')
        else:
            print(f'Неверный номер участника: {num}')

# Вывод всех участников и закрепленных за ними карт
if input('Введите "0", чтобы увидеть всех участников и их карты, или любой другой символ, чтобы продолжить: ') == '0':
    suits_dict = {suit: [] for suit in suits}
    for participant, card in assigned_cards.items():
        if card == 'Джокер':
            continue
        rank, suit = card.split()
        suits_dict[suit].append(f'{participant}: {card}')
    for suit in suits:
        print(f'{suit}:')
        for card in suits_dict[suit]:
            print(f'\t{card}')
else:
    print('Вы выбрали продолжить игру')

# Вывод оставшихся карт
if cards:
    print('Оставшиеся карты в колоде:')
    for card in cards:
        print(card)
else:
    print('Колода закончилась')

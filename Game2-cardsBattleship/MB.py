import random
from tabulate import tabulate

def create_deck():
    suits = ["♥", "♦", "♣", "♠"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [rank + suit for suit in suits for rank in ranks]
    deck.extend(["JR", "JB"])  # Добавляем джокеров
    random.shuffle(deck)
    return deck

def distribute_cards(fields):
    deck = create_deck()
    min_cards_per_field = len(deck) // len(fields)  # Минимум 13 карт на каждое поле
    for field in fields:
        cards_to_distribute = min(len(deck), min_cards_per_field)
        for _ in range(cards_to_distribute):
            row = random.randint(0, 4)
            col = random.randint(0, 5)
            while field[row][col] != "-":
                row = random.randint(0, 4)
                col = random.randint(0, 5)
            field[row][col] = deck.pop()

def print_field(field):
    headers = ["", "A", "B", "C", "D", "E", "F"]
    table = []

    for i, row in enumerate(field):
        table.append([i + 1] + row)

    print(tabulate(table, headers, tablefmt="fancy_grid"))

def take_card(player, fields, current_field):
    while True:
        print_field(fields[current_field])
        coords = input(f"{player['name']}, введите координаты (например, A1): ").upper()
        
        if coords.lower() in ["выход", "0"]:
            return "exit"

        if len(coords) != 2 or coords[0] not in "ABCDEF" or not coords[1].isdigit():
            print("Некорректные координаты. Попробуйте ещё раз.")
            continue

        row = int(coords[1]) - 1
        col = ord(coords[0]) - ord("A")

        while True:
            if fields[current_field][row][col] == "-":
                print("Пустая клетка!")
                return "no_card"
            else:
                print("Вы нашли карту:", fields[current_field][row][col])
                choice = input("Вы хотите взять её? (Y/N): ").lower()
                if choice == "y":
                    card = fields[current_field][row][col]
                    fields[current_field][row][col] = "-"
                    return card
                elif choice == "n":
                    return "no_card"
                else:
                    print("Некорректный выбор. Попробуйте ещё раз.")

def main():
    field_symbols = ["♥", "♦", "♣", "♠"]
    num_fields = len(field_symbols)
    fields = [[["-" for _ in range(6)] for _ in range(5)] for _ in range(num_fields)]
    
    distribute_cards(fields)  # Распределить карты по всем полям

    total_max_players = 54  # Общее количество участников
    max_players_per_field = [15, 15, 15, 15]  # Максимальное количество участников на каждом поле
    
    with open("Participant.txt", "r", encoding='utf-8') as file:
        players = [{"name": line.strip()} for line in file]

    if len(players) > total_max_players:
        print(f"Слишком много участников. Сократите список на {len(players) - total_max_players} игроков.")
        return

    for i, player in enumerate(players):
        while True:
            print(f"Выберите поле для игрока {player['name']} (осталось {len(players) - i} игроков):")
            for j, symbol in enumerate(field_symbols):
                num_players_on_field = sum(1 for p in players if p.get("field") == j)
                num_cards_on_field = sum(1 for f in fields[j] for cell in f if cell != "-")
                num_jokers_on_field = sum(1 for f in fields[j] for cell in f if cell == "JR" or cell == "JB")
                print(f"{j + 1}: {symbol} (игроков: {num_players_on_field}/{num_cards_on_field + num_jokers_on_field}, карт: {num_cards_on_field}, джокеров: {num_jokers_on_field})")
            
            field_choice = input("Введите номер поля: ")
            chosen_field = int(field_choice) - 1
            
            if field_choice.isdigit() and 1 <= int(field_choice) <= num_fields and max_players_per_field[chosen_field] > 0:
                num_players_on_chosen_field = sum(1 for p in players if p.get("field") == chosen_field)
                num_cards_on_chosen_field = sum(1 for f in fields[chosen_field] for cell in f if cell != "-")
                num_jokers_on_chosen_field = sum(1 for f in fields[chosen_field] for cell in f if cell == "JR" or cell == "JB")
                
                if num_players_on_chosen_field >= num_cards_on_chosen_field + num_jokers_on_chosen_field:
                    print("На этом поле уже достаточно участников. Выберите другое поле.")
                    continue
                
                player["field"] = chosen_field
                max_players_per_field[chosen_field] -= 1
                break
            else:
                print("Некорректный выбор поля. Попробуйте ещё раз.")
    
    while True:
        all_players_have_cards = all("cards" in player for player in players)
        no_remaining_cards = all(all(cell == '-' for cell in row) for field in fields for row in field)
        
        if all_players_have_cards or no_remaining_cards:
            print("\nВсе игроки имеют карту/колода кончилась!")
            break

        for player in players:
            if "cards" not in player:
                print(f"\nХодит игрок {player['name']} на поле {field_symbols[player['field']]}")
                result = take_card(player, fields, player['field'])
                
                if result == "exit":
                    print("Игра завершена!")
                    break
                elif result == "no_card":
                    continue
                else:
                    player["cards"] = [result]

    print("\nРезультаты игры:")
    players.sort(key=lambda p: p['name'])
    for player in players:
        card = player.get('cards', ['нет карты'])[0]
        print(f"{player['name']} - {card}")

if __name__ == "__main__":
    main()

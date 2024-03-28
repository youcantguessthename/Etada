import random
import pickle

class Character:
    def __init__(self, name, hp, damage):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.damage = damage

    def attack(self, target):
        damage_dealt = random.randint(0, self.damage)
        target.take_damage(damage_dealt)
        print(f"{self.name} atakuje {target.name} i zadaje {damage_dealt} obrażeń.")

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(f"{self.name} został pokonany!")
        else:
            print(f"{self.name} ma teraz {self.hp} punktów życia.")

class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 20)
        self.gold = 0
        self.inventory = []

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} odnowił {amount} punktów życia i ma teraz {self.hp} punktów życia.")

class Enemy(Character):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp, damage)

class Area:
    def __init__(self, name, enemies):
        self.name = name
        self.enemies = enemies

class Shop:
    def __init__(self):
        self.stock = [
            Potion("Mikstura Małego Leczenia", 20, 0.5),
            Potion("Mikstura Średniego Leczenia", 40, 0.4),
            Potion("Mikstura Dużego Leczenia", 60, 0.25),
            Item("Podstawowy Miecz", 10, 0),
            Item("Kamienny Miecz", 15, 0.1),
            Item("Żelazny Miecz", 40, 0.05),
            Item("Szmaragdowy Miecz", 100, 0.025),
            Item("Kamienna Zbroja", 20, 0),
            Item("Żelazna Zbroja", 40, 0.1),
            Item("Szmaragdowa Zbroja", 100, 0.2)
        ]

class Item:
    def __init__(self, name, price, defense):
        self.name = name
        self.price = price
        self.defense = defense

class Potion(Item):
    def __init__(self, name, price, healing_amount):
        super().__init__(name, price, 0)
        self.healing_amount = healing_amount

def save_game(player, current_area):
    with open("savegame.pkl", "wb") as file:
        pickle.dump(player, file)
        pickle.dump(current_area, file)
    print("Gra została zapisana.")

def load_game():
    try:
        with open("savegame.pkl", "rb") as file:
            player = pickle.load(file)
            current_area = pickle.load(file)
        print("Gra została wczytana.")
        return player, current_area
    except FileNotFoundError:
        print("Brak zapisanej gry.")
        return None, None

def respawn(player):
    player.hp = player.max_hp
    print(f"{player.name} odrodził się w wiosce z pełnym zdrowiem.")

def main():
    print("Witaj w Etadzie!")
    choice = input("Wybierz opcję: 1. Nowa gra, 2. Wczytaj grę, 3. Wyjdź z gry: ")

    if choice == "1":
        player_name = input("Podaj imię swojej postaci: ")
        player = Player(player_name)
        current_area = Area("Niebieska Kraina", [Enemy("Szkielet", 70, 10)])
    elif choice == "2":
        player, current_area = load_game()
        if player is None or current_area is None:
            return
    elif choice == "3":
        print("Do widzenia!")
        return
    else:
        print("Nieprawidłowy wybór.")
        return

    while True:
        print(f"Znajdujesz się w: {current_area.name}")

        action = input("Co chcesz zrobić? [z]walcz, [s]klep, [p]okaż postać, [q] wyjdź: ")

        if action == "z":
            if not current_area.enemies:
                print("Nie ma wrogów w tej krainie.")
                continue

            enemy = random.choice(current_area.enemies)
            while enemy.hp > 0 and player.hp > 0:
                player.attack(enemy)
                if enemy.hp > 0:
                    enemy.attack(player)
            if player.hp > 0:
                print("Pokonałeś wroga!")
                player.gold += 10
                print(f"{player.name} zdobywa 10 złota.")
            else:
                print("Zostałeś pokonany!")
                respawn(player)
                break
        elif action == "s":
            print("Witaj w sklepie!")
            # Dział sklepu
        elif action == "p":
            print(f"Imię: {player.name}, HP: {player.hp}/{player.max_hp}, Złoto: {player.gold}")
            # Wyświetlanie inwentarza
        elif action == "q":
            save_game(player, current_area)
            print("Do widzenia!")
            break
        else:
            print("Nieprawidłowy wybór.")

if __name__ == "__main__":
    main()

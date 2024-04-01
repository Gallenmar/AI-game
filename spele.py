import random
import MiniMaksa
import alphaBeta

def evaluate_turn(current_number, human_points, computer_points, bank_points):
    total_points = human_points + computer_points
    points_gain = 1

    if current_number % 2 == 0:
        points_gain *= -1

    if current_number % 10 == 0 or current_number % 10 == 5:
        points_gain += 1

    total_points_gain = points_gain + bank_points

    remaining_distance = 5000 - current_number

    if remaining_distance < 1000:
        return total_points_gain * 2
    else:
        return bank_points

def main():
    print("Sveiki! Laimes spēle sākas!")
    human_number = int(input("Lūdzu, izvēlieties skaitli no 25 līdz 40: "))

    while human_number < 25 or human_number > 40:
        human_number = int(input("Nederīga ievade. Lūdzu, izvēlieties skaitli no 25 līdz 40: "))

    human_points = 0
    computer_points = 0
    bank_points = 0
    current_number = human_number

    while current_number < 5000:
        print("\nPašreizējais skaitlis:", current_number)
        multiplier = int(input("Izvēlieties, ar ko reizināt (2, 3 vai 4): "))
        while multiplier not in [2, 3, 4]:
            multiplier = int(input("Nederīga ievade. Izvēlieties, ar ko reizināt (2, 3 vai 4): "))

        current_number *= multiplier

        if current_number % 2 == 0:
            human_points -= 1
        else:
            human_points += 1

        if current_number % 10 == 0 or current_number % 10 == 5:
            bank_points += 1

        print("Cilvēka punkti:", human_points)
        print("Datora punkti:", computer_points)
        print("Bankas punkti:", bank_points)

        evaluation_result = evaluate_turn(current_number, human_points, computer_points, bank_points)
        if evaluation_result == -1:
            print("Gājiens bija slikts.")
        elif evaluation_result == 0:
            print("Gājiens bija viduvējs.")
        else:
            print("Gājiens bija labs.")

        if current_number >= 5000:
            human_points += bank_points
            break

        print("\nDatora gājiens:")
        #MiniMaksa AND alphaBeta
        dzilums = 7

        # UNCOMMENT THIS LINE TO PICK MINIMAX
        #computer_multiplier = MiniMaksa.MiniMaxIzvele(current_number, human_points, computer_points, bank_points, dzilums)
        computer_multiplier = alphaBeta.AlphaBetaIzvele(current_number, human_points, computer_points, bank_points, dzilums)
        #computer_multiplier = random.choice([2, 3, 4])

        print("Dators izvēlējās reizināt ar", computer_multiplier)
        current_number *= computer_multiplier

        if current_number % 2 == 0:
            computer_points -= 1
        else:
            computer_points += 1

        if current_number % 10 == 0 or current_number % 10 == 5:
            bank_points += 1

        print("Cilvēka punkti:", human_points)
        print("Datora punkti:", computer_points)
        print("Bankas punkti:", bank_points)

        evaluation_result = evaluate_turn(current_number, human_points, computer_points, bank_points)
        if evaluation_result == -1:
            print("Datora gājiens bija slikts.")
        elif evaluation_result == 0:
            print("Datora gājiens bija viduvējs.")
        else:
            print("Datora gājiens bija labs.")

        if current_number >= 5000:
            computer_points += bank_points

    print("\nBeigas!")
    print("Cilvēka punkti:", human_points)
    print("Datora punkti:", computer_points)

    if human_points > computer_points:
        print("Cilvēks uzvar!")
    elif human_points < computer_points:
        print("Dators uzvar!")
    else:
        print("Neizšķirts rezultāts!")

if __name__ == "__main__":
    main()

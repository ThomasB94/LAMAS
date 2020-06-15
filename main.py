from game import Game

def main():
    won_counter = 0
    number_of_games = 1
    for _ in range(number_of_games):
        game = Game(2, 20, 'range')
        if game.won:
            won_counter = won_counter + 1
    print("+++++++++++++++++++++++++++++++++++++++")
    print("Eventually won", won_counter/number_of_games, "of matches")
    print(won_counter)

main()
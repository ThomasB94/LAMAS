from game import Game

def main():
    won_counter = 0
    removed = 0
    number_of_games = 1
    for _ in range(number_of_games):
        game = Game(2, 10, 'range')
        if game.won:
            won_counter = won_counter + 1
        removed = removed + game.removedWorlds
    print("+++++++++++++++++++++++++++++++++++++++")
    print("Eventually won", won_counter/number_of_games, "of matches")
    print(won_counter)
    print("On average ", removed/number_of_games, " worlds removed")

main()

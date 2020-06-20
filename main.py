from game import Game

def main():
    won_counter = 0
    removed = 0
    for _ in range(10):
        game = Game(2, 10, 'absolute')
        if game.won:
            won_counter = won_counter + 1
        removed = removed + game.removedWorlds
    print("+++++++++++++++++++++++++++++++++++++++")
    print("Eventually won", won_counter/10, "of matches")
    print(won_counter)
    print("On average ", removed/10, " worlds removed")

main()

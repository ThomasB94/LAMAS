from game import Game

def main():
    won_counter = 0
    for i in range(1000):
        game = Game(2, 20, 'range')
        if game.won:
            won_counter = won_counter + 1
    print("+++++++++++++++++++++++++++++++++++++++")
    print("Eventually won", won_counter/1000, "of matches")
    print(won_counter)

main()
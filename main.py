import time
from game import Game


def main():
    won_counter = 0
    removed = 0
    announcements = 0
    t = time.time()
    for _ in range(3):
        game = Game(2, 10, 'range')
        if game.won:
            won_counter = won_counter + 1
        removed = removed + game.removed_worlds
        announcements = announcements + game.announcements_made
    print("+++++++++++++++++++++++++++++++++++++++")
    print("Eventually won", won_counter/3, "of matches")
    print(won_counter)
    if announcements == 0:
        print("No announcements were done")
    else:
        print("On average ", (removed / announcements) / 3, " worlds removed per announcement")
    elapsed = time.time() - t
    print("This took", elapsed, "seconds")

main()

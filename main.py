import time
from game import Game
from multiprocessing import Pool

def run_parallel(_):
    for _ in range(2):
        game = Game(2, 10, 'absolute')
    return game.won

def main():
    won_counter = 0
    removed = 0
    announcements = 0
    num_of_games = 1000
    t = time.time()
    
    with Pool() as p:
        print(p.map(run_parallel, range(3)))
    




    # for _ in range(num_of_games):
    #     game = Game(2, 10, 'absolute')
    #     if game.won:
    #         won_counter = won_counter + 1
    #     removed = removed + game.removed_worlds
    #     announcements = announcements + game.announcements_made
    # print("+++++++++++++++++++++++++++++++++++++++")
    # print("Eventually won", won_counter/num_of_games, "of matches")
    # print(won_counter)
    # if announcements == 0:
    #     print("No announcements were done")
    # else:
    #     print("On average ", (removed / announcements) / num_of_games, " worlds removed per announcement")
    # elapsed = time.time() - t
    # print("This took", elapsed, "seconds")

if __name__ == "__main__":
    main()

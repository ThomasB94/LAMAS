import time
import sys
from game import Game

def main():
    # handles the command line input from the user
    if len(sys.argv) != 3:
        sys.exit("Please specify an announcement type and the number of announcements for example: python main.py absolute 2") 
    announcement_type = sys.argv[1]
    if announcement_type != 'absolute' and announcement_type != 'range' and announcement_type != 'none':
        sys.exit("Please specify a correct communication type: none, absolute or range")
    num_announcements = sys.argv[2]
    if announcement_type == 'absolute' or announcement_type == 'range':
        if num_announcements not in ['1','2','3']:
            sys.exit("Please specify a correct number of announcements: 1, 2 or 3")
        else:
            num_announcements = int(num_announcements)
    if announcement_type == 'none' and num_announcements != 0:
        num_announcements = 0
        print("The none announcement can only be run with 0 announcement. The simulation will run with 0 announcements")
    
    won_counter = 0
    removed = 0
    announcements = 0
    num_of_games = 1000
    t = time.time()
    for _ in range(num_of_games):
        game = Game(2, 10, announcement_type, num_announcements)
        if game.won:
            won_counter = won_counter + 1
        removed = removed + game.removed_worlds
        announcements = announcements + game.announcements_made
    print("+++++++++++++++++++++++++++++++++++++++")
    print("Eventually won", won_counter/num_of_games, "of matches")
    print(won_counter)
    if announcements == 0:
        print("No announcements were done")
    else:
        print("On average ", (removed / announcements), " worlds removed per announcement")
    elapsed = time.time() - t
    print("This took", elapsed, "seconds")

if __name__ == "__main__":
    main()
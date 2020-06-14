# do announcements stuff here, such as reducing the kripke model

    # Number of announcements per turn}: 
    # For this variation we will look at the effects of multiple rounds of announcements. 
    # Every announcement will provide more information. 
    # Percentage range of the announcement}: 
    # For this strategy we will experiment with the percentiles (the default is 50). 
    # We will look at the 10th and 25th percentiles, which represent the range where a card is considered 'good'.
    # Absolute range of the announcement}: 
    # In this case we take the good statement not to mean having a card in a certain percentile, but having a card in the top $k$ cards. 
    # Announcement about stack preference}: 
    # Here, we will experiment with announcements that only say something about which stack the agent prefers. 
    # This preference is based on which stack the agent has better cards for. 



def make_range_announcement(agent, game, kripke):
    pass
def make_relative_announcement(agent, game, kripke):
    pass
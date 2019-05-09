def latest(scores):
    print("Your last score was:")
    n=len(scores)-1
    print(scores[n])


def best(scores):
    print("Your High Score is:")
    print(max(scores))


def top3(scores):
    scores.sort()
    scores.reverse()
    print("Your top scores are:")
    print(scores[0:3])

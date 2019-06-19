def latest(scores):
    n=len(scores)-1
    retun(scores[n])


def best(scores):
    return(max(scores))


def top3(scores):
    scores.sort()
    scores.reverse()
    return(scores[0:3])

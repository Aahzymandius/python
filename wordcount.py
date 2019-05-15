##Count the number of times each word in a text is used

def remover(n,list)
  for x in list:
    if x == n:
	list.remove(x)

def wordcount(text):
  stats = {}
  with open(text) as t:
    words=t.read().split()
    for i in words:
      count=words.count(i)
      print(i + " appears " + str(count) + " times")
      stats[i] = count
      remover(i,words)
  return stats
		
text=input("Enter path text: ",)
wordcount(text)

##Count the number of times each word in a text is used

def remover(n,list)
  i=0
  length=len(list)
  while x < length:
    if list[x]==n:
	  list.remove(list[i])
	  length-=1
	  continue
	x+=1

def wordcount(text):
  with open(text) as t:
    words=t.read().split()
    for i in words:
      count=words.count(i)
      print(str(i) + " appears " + str(count) + " times")
      remover(i,words)
	  
text=input("Enter path text: ",)
wordcount(text)

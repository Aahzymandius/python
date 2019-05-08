def is_pangram(sentence):
  count=0
  for l in "abcdefghijklmnopqrstuvwxyz"
    if l in sentence:
      count+=1
    else:
      print("Not a pangram")
  if count >= 26:
    print("This is a pangram")
    
sentence=input(Which sentence would you like to test?,)
is_pangram(sentence)

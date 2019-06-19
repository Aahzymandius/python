def is_pangram(sentence):
  for l in "abcdefghijklmnopqrstuvwxyz":
    if l not in sentence:
      return("This is not a pangram")
  return("This is a pangram")
    
sentence=input("Which sentence would you like to test?",)
is_pangram(sentence)

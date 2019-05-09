import random

dice=input("How many sided dice?",)
amount=input("How many dice are you rolling",)

print("Rolling " + amount + "d" + dice)

total=0
for i in range(int(amount)):
  rolled = random.choice(range(1,int(dice)+1))
  print(rolled)
  total+=int(rolled)

print("Total rolled is " + str(total))

def armstrong(number):
  total=0
  x=len(number)
  for d in number:
    dd = int(d)**int(x)
    total+=dd
  if int(total) == int(number):
    print("You found an armstrong number!")
  else:
    print("This is not an armstrong number")

number=input("Enter a number you think may be an armostrong number:")
armstrong(number)

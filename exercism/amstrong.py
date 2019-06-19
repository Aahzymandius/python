def armstrong(number):
  total=0
  x=len(number)
  for d in number:
    dd = int(d)**int(x)
    total+=dd
  if int(total) == int(number):
    return("You found an armstrong number!")
  return("This is not an armstrong number")

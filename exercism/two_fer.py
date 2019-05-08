def two_fer(name):
    if name == "":
      print("One for you and one for me")
    else:
      print("One for " + name + ", one for me")

name=input("What is your name?",)
two_fer(name)

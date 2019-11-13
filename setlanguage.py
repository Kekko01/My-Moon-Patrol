print("Select your language:")
print("1. English")
print("2. Italiano")
choice=int(input("Insert (1-2) "))

with open("assets/lang/choice", "w") as target:
    if choice==1:
        print("eng", file=target)
        print("Set English language")
    elif choice==2:
        print("ita", file=target)
        print("Lingua Italiana impostata")
    else:
        print("Number not allow!")

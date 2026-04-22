word = input("Enter your word: ")

for i in word:
    if (i=="A" or i=="a"):
        print("A is found")
        break
    else:
        print("A is not found")
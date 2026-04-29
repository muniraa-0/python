import random
playing = True
number = str(random.rndint(0,9))

print("I will genrate a numbe rbetween 0 and 9. YOU have to guess the number one digit at a time")
print("The game ends when you get 1!")

while playing:
    guess = input("Guess the number: ")
    if number == guess:
        print("you win the game!")
        print("The number was",number)
        break
    else:
        print("Your guess is wrong try again!")
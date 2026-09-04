import random #tells it to import random for this project

secret_number = random.randint(1,20)
Attempt = 0
Attempt = int(Attempt)
print("Guess the Number")
print("It is bewteen 1 and 20")
while True:
    guess = int(input("Your Guess: "))
    if guess < secret_number:
        print("To Low")
        Attempt = Attempt + 1
    elif guess > secret_number:
        print("To High")
        Attempt = Attempt + 1
    else:
        print(f"Congradulation you got it in {Attempt} Attempt ")
        break

    if Attempt == 5:
        print("You have ran out of lives")
        print(f"The number was {secret_number}")
    




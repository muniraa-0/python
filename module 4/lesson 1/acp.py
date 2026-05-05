
start = int(input("Enter start of range: "))
end = int(input("Enter end of range: "))


squares = [i**2 for i in range(start, end + 1)]


even_squares = [x for x in squares if x % 2 == 0]
odd_squares = [x for x in squares if x % 2 != 0]


print("All square values:", squares)
print("Even square values:", even_squares)
print("Odd square values:", odd_squares)
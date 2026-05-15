

test_dict = {
    "apple": 5,
    "banana": 3,
    "orange": 5,
    "grape": 2,
    "mango": 5
}

value = int(input("Enter the value to check frequency: "))

frequency = list(test_dict.values()).count(value)

print("Frequency of", value, "is:", frequency)
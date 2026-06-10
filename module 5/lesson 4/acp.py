class StringReverser:
    def reverse_words(self, text):
        words = text.split()
        return " ".join(words[::-1])


reverser = StringReverser()

input_string = "Python is a powerful language"
result = reverser.reverse_words(input_string)

print(result)
class IOString:
    def __init__(self):
        self.str1 = ""
    def get_string(self):
            self.str1 = input("Enter your string:")
    def print_string(self):
         print("Result:",self.str1.upper()) 

string = IOString()

string.get_string()
string.print_string()
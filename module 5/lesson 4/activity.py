class myclass:

    __x = 24

    def __mymethod(self):
        print("This is private")

    def myfunc(self):
        print(myclass.__x)

obj = myclass()
obj.myfunc()
obj.__mymethod()
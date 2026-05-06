def palindrome(t):
    reverse = len(t)-1
    front = 0

    while (front<reverse):
        if (t[front] != t[reverse]):
            return False
        front = front+1
        reverse = reverse - 1
    return True

t = (1,2,3,3,2,1)

if (palindrome(t)):
    print("The tuple is a flip=flop")
marks=[85,72.90,66,58]
total=0
marks.sort()
print(marks)
highest = marks[-1]
for m in marks:
    total=total+m
average=total / len(marks)
print("average:",average)
print("highest mark:", highest)
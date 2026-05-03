def match_words(words):
    ctr - 0
    lst = [1]

    for word in words:
        if len(word)> 1 and words[0]==word[-1]:
            ctr = ctr + 1
            lst.append(word)

    return ctr
count = match_words(['abc','cfc','xyz','aba','1221'])
print("Number of words having the first and last character same:",count)
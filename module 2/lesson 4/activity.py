word=input('give me a word: ').lower()
char=input('give me a character: ').lower()
i=0
c=0
while (i<len(word)):
    if (word[i]==char):
        c=c+1
        i=i+1
print('your word has ',c,' ',char,'s')

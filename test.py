def QuestionsMarks(s):
    indices     = [i for i, ltr in enumerate(s) if ltr.isdigit()]
    for i in range(len(indices)):
        stride                 = i+1 if i+1 < len(indices) else len(indices)-1
        startIndice, endIndice = indices[i], indices[stride]
        if (s[startIndice:endIndice].count('?') == 3 and (int(s[startIndice]) + int(s[endIndice])) == 10) or endIndice == startIndice:
            continue
        if (s[startIndice:endIndice].count('?') != 3 and (int(s[startIndice]) + int(s[endIndice])) == 10):
            return False
    return True

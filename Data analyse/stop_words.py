from pandas.core.algorithms import rank

f = open("./stop_words.txt", "w")
for i in range(0, 20000):
    f.write(str(i)+" ")
    if i < 101:
        f.write("0"+str(i)+" ")
        f.write(str(i)+"% ")
f.write("##")


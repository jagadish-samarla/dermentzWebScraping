ls = [i for i in range(1, 10)]
#n = int(input(('Please enter the number:\n')))


def mystery(n):
    if n > 1:
        v = 0
        for i in range(1, n+1):
            k = str(i)*i
            v = v + int(k)
        return v
    else:
        return 1


for n in ls:
    print(mystery(n))
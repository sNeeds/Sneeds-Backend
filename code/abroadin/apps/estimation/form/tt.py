# t = [True, [1, 2]]


class ss(list):
    def __init__(self):
        super().__init__()

    def __bool__(self):
        return self[0]


t = ss()

t.append(True)
t.append([1, 2])

if t:
    print('yes')
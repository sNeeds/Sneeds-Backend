from pprint import pprint

a = {
    # 'GREAT_UNIVERSITY_RANK': 100,
    #  'GOOD_UNIVERSITY_RANK': 600,
    #  'AVERAGE_UNIVERSITY_RANK': 1200,
    #  'BAD_UNIVERSITY_RANK': 3000,
}

with open('admission_chance_test_data/test_data.py', 'r') as f:
    s = f.read()
    # for key, value in a.items():
    #     s.replace(key, str(value))
    x = eval(s)

    idd = 0
    for xx in x:
        # xx['id'] = idd
        # c = xx['Chances']
        # del(xx['Chances'])
        # pprint(xx)
        # pprint(c)
        print('{\n"id": ' + '{},'.format(idd))
        for key, value in xx.items():
            if isinstance(value, str):
                print("'{}': '{}',\n".format(key, value))
            else:
                print("'{}': {},\n".format(key, value))
        print('}\n\n')

        idd += 5
    # pprint(x)

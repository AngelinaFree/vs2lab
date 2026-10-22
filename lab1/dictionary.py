dictonary = dict([('jan', '123456789'), ('jason', '80085'), ('angelina', '426967'), ('christof', '31415926535897932348')])
dictonary.update(dict([(f'name{i:03d}', str(i)) for i in range(1,501)]))

def to_string():
    answer = ''
    for name, number in dictonary.items():
        answer += f'{name}: {number}\n'
    return answer
PATH = 'C:\Python\PythonProjects\payout_task\data\data1.csv'


def group(data: list) -> dict:
    #  группируем сотрудников по отделам
    headers = data[0].split(',')
    departments = {}

    for line in data[1:]:
        if len(line) > 1:
            values = line.split(',')
            employees = dict(zip(headers, values))

            department_name = employees['department']
            if department_name not in departments:
                departments[department_name] = []
            departments[department_name].append(employees)

    return departments

def get_keys(data: list) -> str:
    #  обрабатываем варианты ключа rate
    headers = {'id': '', 'email': '', 'name': '', 'department': '', 'hours_worked': '', 'rate': ''}

    for i in data[0].split(','):
        if i in headers:
            headers[i] = i
        else:
            headers['rate'] = i
    return headers['rate']

def printing(departments: dict, key: str):
    print('name'.rjust(19), 'hours'.rjust(18), 'rate'.rjust(10), 'payout'.rjust(13))

    for dep, info in departments.items():
        total_cash = []
        total_hours = []
        print(dep)

        for i in info:
            cash = int(i['hours_worked']) * int(i[key])

            print(''.rjust(14, '-'),
                  i['name'].ljust(18),
                  i['hours_worked'].ljust(12),
                  i[key].ljust(10),
                  '$' + str(cash).ljust(5)
                  )
            total_cash.append(cash),
            total_hours.append(int(i['hours_worked']))

        print(
            (str(sum(total_hours)).rjust(37)),
            (str(sum(total_cash)).rjust(25))
            )


if __name__ == '__main__':
    with open(PATH, 'r') as file:
        data = file.read().split('\n')

        key = get_keys(data)
        employees = group(data)
        printing(employees, key)


def group(data: list) -> dict:
    #  группируем сотрудников по отделам
    headers = data[0]
    departments = {}

    for employee in data[1:]:
        if len(employee) > 1:
            employees = dict(zip(headers, employee))

            department = employees['department']
            if department not in departments:
                departments[department] = []
            departments[department].append(employees)

    return departments

def get_keys(data: list) -> dict:
    #  обрабатываем варианты разных названий колонки rate
    headers = {'id': '', 'email': '', 'name': '', 'department': '', 'hours_worked': '', 'rate': ''}

    for i in data:
        if i in headers:
            headers[i] = i
        else:
            headers['rate'] = i

    return headers

def payout_report(departments: dict, key: str):
    print(f"{'name':>19} {'hours':>18} {'rate':>10} {'payout':>13}")

    for dep, info in departments.items():
        total_cash = []
        total_hours = []
        print(dep)

        for employee in info:
            cash = int(employee['hours_worked']) * int(employee[key])

            print(f"{' ':->14}"
                  f"{employee['name']:<18}",
                  f"{employee['hours_worked']:<12}",
                  f"{employee[key]:<10}",
                  f"${str(cash):<10}"
                  )
            total_cash.append(cash),
            total_hours.append(int(employee['hours_worked']))

        print(f"{str(sum(total_hours)):>36}",
              f"{'$' + str(sum(total_cash)):>25}"
              )
    print(f"{'':->65}")

from dataclasses import dataclass


@dataclass
class Employer:
    id: int
    email: str
    name: str
    department: str
    hours_worked: int
    rate: int


class ReportModule:
    type: str
    name: str

    def print_report(self, files: list[Employer]):
        ...


class PayoutReportModule(ReportModule):
    type: str = "payout"
    name: str = "Отчет по зарплате"

    def print_report(self, files: list[Employer]):
        print(f"{'name':>20} {'hours':>20} {'rate':>13} {'payout':>18}")
        departments = []
        total_cash = 0
        total_hours = 0

        for employee in files:
            if employee.department not in departments:
                departments.append(employee.department)
                print(employee.department)

            cash = int(employee.rate) * int(employee.hours_worked)
            print(f"{' ':->14}",
                  f"{employee.name:<20}",
                  f"{employee.hours_worked:<15}",
                  f"{employee.rate:<15}",
                  f"${cash:<10}"
                  )

            total_cash += cash
            total_hours+= int(employee.hours_worked)

        print(f"{total_hours:>39}{'$':>30}{total_cash:<7}")
        print(f"{'':_>75}")
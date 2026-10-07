class Worker:
    def __init__(self, name, surname, position, wage, bonus):
        self.name = name
        self.surname = surname
        self.position = position
        self._income = {"wage": wage, "bonus": bonus}


class Position(Worker):
    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def get_total_income(self):
        return self._income["wage"] + self._income["bonus"]


workers = [
    Position("Иван", "Петров", "инженер-программист", 3200, 800),
    Position("Анна", "Смирнова", "аналитик данных", 2900, 650),
    Position("Сергей", "Ковалев", "инженер по тестированию", 2100, 350),
]

for w in workers:
    print("Имя:", w.name)
    print("Фамилия:", w.surname)
    print("Должность:", w.position)
    print("Доход (атрибут _income):", w._income)
    print("Полное имя:", w.get_full_name())
    print("Доход с учетом премии:", w.get_total_income(), "руб.")
    print("-" * 45)

best = max(workers, key=lambda x: x.get_total_income())
print("Самый высокий доход у сотрудника:", best.get_full_name(),
      "-", best.get_total_income(), "руб.")

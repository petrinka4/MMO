class Student:
    count = 0
    min_grade = 1
    max_grade = 10

    def __init__(self, name, group, grades=None):
        self.name = name
        self.group = group
        self.grades = []
        if grades:
            for g in grades:
                self.add_grade(g)
        Student.count += 1

    def add_grade(self, grade):
        if not Student.is_valid_grade(grade):
            raise ValueError(f"оценка {grade} должна быть от "
                             f"{Student.min_grade} до {Student.max_grade}")
        self.grades.append(grade)

    def average(self):
        if not self.grades:
            return 0
        return round(sum(self.grades) / len(self.grades), 2)

    def info(self):
        avg = self.average()
        return (f"{self.name}, гр. {self.group}, оценки: {self.grades}, "
                f"средний балл: {avg} ({Student.grade_to_text(avg)})")

    @staticmethod
    def is_valid_grade(grade):
        if not isinstance(grade, int):
            return False
        return Student.min_grade <= grade <= Student.max_grade

    @staticmethod
    def grade_to_text(grade):
        if grade >= 9:
            return "отлично"
        if grade >= 7:
            return "хорошо"
        if grade >= 4:
            return "удовлетворительно"
        return "неудовлетворительно"

    @classmethod
    def from_string(cls, line):
        name, group, grades = line.split(";")
        marks = [int(x) for x in grades.split()]
        return cls(name.strip(), group.strip(), marks)

    @classmethod
    def get_count(cls):
        return cls.count


s1 = Student("Козлов Андрей", "351002", [8, 9, 7, 10])
s2 = Student.from_string("Морозова Ольга; 351002; 6 7 5 8")
s3 = Student("Новиков Павел", "351003")
s3.add_grade(9)
s3.add_grade(10)

print("Методы экземпляра:")
for s in [s1, s2, s3]:
    print(s.info())

print()
print("Статические методы:")
print("Оценка 7 допустима:", Student.is_valid_grade(7))
print("Оценка 12 допустима:", Student.is_valid_grade(12))
print("Оценка 9.3 словами:", Student.grade_to_text(9.3))

print()
print("Методы класса:")
print("Создано студентов:", Student.get_count())

print()
try:
    s1.add_grade(15)
except ValueError as e:
    print("Ошибка:", e)

best = max([s1, s2, s3], key=lambda s: s.average())
print("Лучший средний балл:", best.name, "-", best.average())

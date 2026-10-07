def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def process(value):
    if isinstance(value, list):
        total = 0
        for item in value:
            if is_number(item):
                total += item
        return total
    if isinstance(value, dict):
        try:
            values = sorted(value.values(), reverse=True)
        except TypeError:
            raise TypeError("значения словаря нельзя сравнить между собой")
        return values[:3]
    if is_number(value):
        return sum(int(d) for d in str(value) if d.isdigit())
    if isinstance(value, str):
        return len(value.split())
    raise TypeError(f"тип {type(value).__name__} не поддерживается")


def describe(value):
    if isinstance(value, list):
        return "Список, сумма чисел"
    if isinstance(value, dict):
        return "Словарь, три наибольших значения"
    if is_number(value):
        return "Число, сумма цифр"
    if isinstance(value, str):
        return "Строка, количество слов"
    return "Неизвестный тип"


tests = [
    [4, 15, "abc", 2.5, 10, True, "7"],
    {"январь": 120, "февраль": 95, "март": 140, "апрель": 87, "май": 160},
    {"a": 3, "b": 1},
    98765,
    -4071,
    "Python простой и удобный язык программирования",
    "",
    {"x": 10, "y": "двадцать"},
    (1, 2, 3),
    None,
]

for t in tests:
    print("Аргумент:", repr(t))
    try:
        result = process(t)
        print(describe(t) + ":", result)
    except TypeError as e:
        print("Ошибка:", e)
    finally:
        print("-" * 50)

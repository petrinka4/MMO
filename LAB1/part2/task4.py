class NegativeValueError(Exception):
    pass


def divide(a, b):
    return a / b


def square_root(x):
    if x < 0:
        raise NegativeValueError(
            "нельзя извлечь корень из отрицательного числа")
    return x ** 0.5


def read_file(filename):
    f = None
    try:
        f = open(filename, "r", encoding="utf-8")
        text = f.read()
        print("Содержимое файла:", text)
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден")
    finally:
        if f is not None:
            f.close()
            print("Файл закрыт")
        print("finally: работа с файлом завершена")


def get_element(items, index):
    try:
        return items[index]
    except IndexError:
        print(f"Ошибка: индекса {index} нет в списке")
        return None
    finally:
        print(f"finally: обращение к элементу с индексом {index}")


print("1. Деление двух чисел")
while True:
    a_str = input("Введите делимое (q - выход): ").strip()
    if a_str.lower() == "q":
        break
    b_str = input("Введите делитель: ").strip()
    try:
        a = float(a_str)
        b = float(b_str)
        result = divide(a, b)
    except ValueError:
        print("Ошибка: введено не число")
    except ZeroDivisionError:
        print("Ошибка: деление на ноль")
    else:
        print("Результат деления:", result)
    finally:
        print("finally: операция деления завершена")
    print()

print()
print("2. Собственное исключение")
for x in [16, -9]:
    try:
        print(f"Корень из {x} =", square_root(x))
    except NegativeValueError as e:
        print("Ошибка:", e)
    finally:
        print("finally: проверка числа", x, "завершена")

print()
print("3. Обращение к элементу списка")
data = [10, 20, 30]
print("Элемент:", get_element(data, 1))
print("Элемент:", get_element(data, 5))

print()
print("4. Чтение файла")
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("Привет, Python!")
read_file("test.txt")
read_file("missing.txt")

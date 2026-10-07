import random


def read_int(text):
    value = input(text)
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"'{value}' не является целым числом")


def create_random_matrix(rows, cols):
    matrix = []
    for _ in range(rows):
        matrix.append([random.randint(-5, 20) for _ in range(cols)])
    return matrix


def input_matrix(rows, cols):
    matrix = []
    for i in range(rows):
        line = input(f"Строка {i + 1}: ").split()
        if len(line) != cols:
            raise ValueError(f"в строке должно быть {cols} элементов")
        try:
            matrix.append([int(x) for x in line])
        except ValueError:
            raise ValueError("элементы матрицы должны быть целыми числами")
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print("".join(f"{x:5}" for x in row))


def find_positive_row(matrix):
    for i, row in enumerate(matrix):
        if all(x > 0 for x in row):
            return i, sum(row)
    return None


def main():
    try:
        rows = read_int("Введите количество строк: ")
        cols = read_int("Введите количество столбцов: ")
        if rows <= 0 or cols <= 0:
            raise ValueError("размеры матрицы должны быть больше нуля")
        print("1 - ввести матрицу вручную, 2 - заполнить случайно")
        mode = input("Ваш выбор: ").strip()
        if mode == "1":
            matrix = input_matrix(rows, cols)
        elif mode == "2":
            matrix = create_random_matrix(rows, cols)
        else:
            raise ValueError("нужно выбрать 1 или 2")
        print("Матрица:")
        print_matrix(matrix)
        result = find_positive_row(matrix)
        if result is None:
            print("В матрице нет строки, все элементы которой положительны")
        else:
            index, total = result
            print(f"Первая строка с положительными элементами: {index + 1}")
            print("Элементы строки:", matrix[index])
            print("Сумма элементов:", total)
    except ValueError as e:
        print("Ошибка:", e)
    finally:
        print("Работа программы завершена")


main()

shop = {
    "тормозные колодки": [
        "керамические накладки, стальное основание, комплект на одну ось",
        85.0, 20],
    "масляный фильтр": [
        "металлический корпус, фильтрующая бумага, резиновое уплотнение",
        18.5, 40],
    "свеча зажигания": [
        "керамический изолятор, иридиевый электрод",
        25.0, 60],
    "аккумулятор": [
        "свинцово-кислотный, 12 В, 60 Ач, пусковой ток 540 А",
        260.0, 8],
    "амортизатор": [
        "стальной корпус, газомасляный, передний",
        140.0, 12],
    "щетка стеклоочистителя": [
        "резиновая лента, металлический каркас, длина 600 мм",
        32.0, 25],
}


def show_menu():
    print()
    print("===== Магазин автозапчастей =====")
    print("1. Просмотр описания")
    print("2. Просмотр цены")
    print("3. Просмотр количества")
    print("4. Вся информация")
    print("5. Покупка")
    print("6. До свидания")


def show_description():
    for name, info in shop.items():
        print(f"{name} - {info[0]}")


def show_price():
    for name, info in shop.items():
        print(f"{name} - {info[1]:.2f} руб.")


def show_count():
    for name, info in shop.items():
        print(f"{name} - {info[2]} шт.")


def show_all():
    for name, info in shop.items():
        print(f"{name}: состав - {info[0]}; цена - {info[1]:.2f} руб.; "
              f"количество - {info[2]} шт.")


def buy():
    total = 0
    cart = {}
    while True:
        name = input("Введите название товара (n - выход): ").strip().lower()
        if name == "n":
            break
        if name not in shop:
            print("Такого товара нет в магазине")
            continue
        count_str = input("Введите количество: ").strip()
        if not count_str.isdigit() or int(count_str) == 0:
            print("Количество должно быть целым положительным числом")
            continue
        count = int(count_str)
        if count > shop[name][2]:
            print(f"В наличии только {shop[name][2]} шт.")
            continue
        shop[name][2] -= count
        cost = count * shop[name][1]
        total += cost
        cart[name] = cart.get(name, 0) + count
        print(f"Добавлено в корзину: {name} x {count} = {cost:.2f} руб.")

    if cart:
        print()
        print("Ваша покупка:")
        for name, count in cart.items():
            print(f"{name} - {count} шт.")
        print(f"Итого к оплате: {total:.2f} руб.")
        print()
        print("Осталось в магазине:")
        show_count()
    else:
        print("Покупка не совершена")


while True:
    show_menu()
    choice = input("Выберите пункт меню: ").strip()
    if choice == "1":
        show_description()
    elif choice == "2":
        show_price()
    elif choice == "3":
        show_count()
    elif choice == "4":
        show_all()
    elif choice == "5":
        buy()
    elif choice == "6":
        print("До свидания!")
        break
    else:
        print("Такого пункта нет, попробуйте еще раз")

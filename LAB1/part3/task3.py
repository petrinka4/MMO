def format_time(hours):
    total_minutes = round(hours * 60)
    return f"{total_minutes // 60} ч {total_minutes % 60} мин"


class Vehicle:
    def __init__(self, name, speed, extra_time=0):
        self.name = name
        self.speed = speed
        self.extra_time = extra_time

    def move(self):
        return "способ передвижения не задан"

    def get_time(self, distance):
        return distance / self.speed + self.extra_time

    def get_cost(self, distance):
        return 0

    def get_info(self, city_from, city_to, distance):
        time = format_time(self.get_time(distance))
        cost = self.get_cost(distance)
        return (f"{self.name} ({self.move()}): {city_from} - {city_to}, "
                f"{distance} км, время {time}, стоимость {cost:.2f} руб.")

    def write_to_file(self, filename, city_from, city_to, distance):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(self.get_info(city_from, city_to, distance) + "\n")


class Airplane(Vehicle):
    def __init__(self):
        super().__init__("Самолет", 750, 2.5)
        self.base_price = 60
        self.price_per_km = 0.2

    def move(self):
        return "летит по воздуху"

    def get_cost(self, distance):
        return self.base_price + distance * self.price_per_km


class Train(Vehicle):
    def __init__(self):
        super().__init__("Поезд", 90, 0.3)
        self.price_per_km = 0.07

    def move(self):
        return "едет по железной дороге"

    def get_cost(self, distance):
        return distance * self.price_per_km


class Car(Vehicle):
    def __init__(self):
        super().__init__("Автомобиль", 80)
        self.fuel_consumption = 7.5
        self.fuel_price = 2.6

    def move(self):
        return "едет по автомобильной дороге"

    def get_cost(self, distance):
        return distance / 100 * self.fuel_consumption * self.fuel_price


def compare(vehicles, city_from, city_to, distance, filename):
    print(f"Маршрут: {city_from} - {city_to} ({distance} км)")
    for v in vehicles:
        print("  " + v.get_info(city_from, city_to, distance))
        v.write_to_file(filename, city_from, city_to, distance)

    fastest = min(vehicles, key=lambda v: v.get_time(distance))
    cheapest = min(vehicles, key=lambda v: v.get_cost(distance))
    best_time = format_time(fastest.get_time(distance))
    best_cost = cheapest.get_cost(distance)
    line1 = f"Самая быстрая поездка: {fastest.name}, {best_time}"
    line2 = (f"Самая экономичная поездка: {cheapest.name}, "
             f"{best_cost:.2f} руб.")
    print("  " + line1)
    print("  " + line2)
    print()
    with open(filename, "a", encoding="utf-8") as f:
        f.write(line1 + "\n")
        f.write(line2 + "\n\n")


filename = "trips.txt"
open(filename, "w", encoding="utf-8").close()

vehicles = [Airplane(), Train(), Car()]
routes = [
    ("Минск", "Брест", 350),
    ("Минск", "Москва", 715),
    ("Минск", "Вильнюс", 185),
]

for city_from, city_to, distance in routes:
    compare(vehicles, city_from, city_to, distance, filename)

print("Добавьте свой маршрут")
city_from = input("Город отправления: ").strip()
city_to = input("Город прибытия: ").strip()
distance_str = input("Расстояние, км: ").strip()
if city_from and city_to and distance_str.isdigit() and int(distance_str):
    print()
    compare(vehicles, city_from, city_to, int(distance_str), filename)
else:
    print("Маршрут введен неверно")

print(f"Информация о поездках записана в файл {filename}")

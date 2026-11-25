from abc import ABC, abstractmethod


# Интерфейс для атакующих объектов
class Attacker(ABC):
    @abstractmethod
    def attack(self, unit: 'Unit') -> None:
        pass


# Интерфейс для движущихся объектов
class Moveable(ABC):
    @abstractmethod
    def move_to(self, x: int, y: int) -> None:
        pass

    @property
    @abstractmethod
    def move_range(self) -> int:
        pass


# Базовый абстрактный класс всех игровых объектов
class GameObject(ABC):
    def __init__(self, id: int, name: str, x: int, y: int):
        self._id = id
        self._name = name
        self._x = x
        self._y = y

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y


# Класс юнита (подразделения)
class Unit(GameObject, ABC):
    def __init__(self, id: int, name: str, x: int, y: int, hp: float):
        super().__init__(id, name, x, y)
        self._hp = hp

    def is_alive(self) -> bool:
        return self._hp > 0

    def get_hp(self) -> float:
        return self._hp

    def receive_damage(self, damage: float) -> None:
        # Здоровье не может уйти ниже нуля
        self._hp = max(0.0, self._hp - damage)


# Класс лучника
class Archer(Unit, Attacker, Moveable):
    def __init__(self, id: int, name: str, x: int, y: int, hp: float = 100.0, damage: float = 15.0,
                 move_range: int = 6):
        super().__init__(id, name, x, y, hp)
        self._damage = damage
        self._move_range = move_range

    @property
    def move_range(self) -> int:
        return self._move_range

    def attack(self, unit: Unit) -> None:
        if not self.is_alive():
            print(f"{self.get_name()} мертв и не может атаковать")
        elif not unit.is_alive():
            print(f"Цель {unit.get_name()} уже мертва")
        else:
            unit.receive_damage(self._damage)
            print(f"{self.get_name()} атакует {unit.get_name()} и наносит {self._damage} урона")
            print(f"  -> Здоровье {unit.get_name()} после атаки: {unit.get_hp()}")

    def move_to(self, x: int, y: int) -> None:
        if not self.is_alive():
            print(f"{self.get_name()} мертв и не может двигаться")
            return

        # Вычисляем расстояние (сумма разниц координат по модулю)
        distance = abs(x - self._x) + abs(y - self._y)

        if distance <= self._move_range:
            self._x = x
            self._y = y
            print(f"{self.get_name()} переместился на координаты ({self._x}, {self._y})")
        else:
            print(f"Точка слишком далеко для {self.get_name()} (расстояние {distance}, максимум {self._move_range})")


# Базовый класс для построек
class Building(GameObject, ABC):
    def __init__(self, id: int, name: str, x: int, y: int, built: bool = False):
        super().__init__(id, name, x, y)
        self._built = built

    def is_built(self) -> bool:
        return self._built

    def build(self) -> None:
        self._built = True


# Класс крепости
class Fort(Building, Attacker):
    def __init__(self, id: int, name: str, x: int, y: int, built: bool = False, damage: float = 30.0):
        super().__init__(id, name, x, y, built)
        self._damage = damage

    def attack(self, unit: Unit) -> None:
        if not self.is_built():
            print(f"Стрелять нельзя, {self.get_name()} не построена")
        elif not unit.is_alive():
            print(f"{self.get_name()}: цель уже мертва")
        else:
            unit.receive_damage(self._damage)
            print(f"{self.get_name()} стреляет по {unit.get_name()} и наносит {self._damage} урона")
            print(f"  -> Здоровье {unit.get_name()} после выстрела: {unit.get_hp()}")


# Класс дома на колесах
class MobileHouse(Building, Moveable):
    def __init__(self, id: int, name: str, x: int, y: int, built: bool = False, move_range: int = 20):
        super().__init__(id, name, x, y, built)
        self._move_range = move_range

    @property
    def move_range(self) -> int:
        return self._move_range

    def move_to(self, x: int, y: int) -> None:
        if not self.is_built():
            print(f"{self.get_name()} не построен, перемещение невозможно")
            return

        distance = abs(x - self._x) + abs(y - self._y)

        if distance <= self._move_range:
            self._x = x
            self._y = y
            print(f"{self.get_name()} переместился на ({self._x}, {self._y})")
        else:
            print(f"Точка слишком далеко для {self.get_name()} (расстояние {distance}, максимум {self._move_range})")


# Точка входа (демонстрация)
if __name__ == "__main__":
    # Создаем объекты
    archer = Archer(1, "Герой", 1, 1, hp=80.0, damage=20.0, move_range=5)
    enemy = Archer(2, "Враг", 5, 5, hp=50.0, damage=10.0, move_range=3)
    fort = Fort(3, "Главная крепость", 0, 0, built=False, damage=30.0)
    house = MobileHouse(4, "Дом на колесах", 10, 10, built=False, move_range=15)

    print("--- Начальное состояние ---")
    print(f"{archer.get_name()}: HP={archer.get_hp()}")
    print(f"{enemy.get_name()}: HP={enemy.get_hp()}")

    print("\n--- Проверка атаки ---")
    fort.attack(enemy)
    fort.build()
    fort.attack(enemy)
    archer.attack(enemy)

    print("\n--- Проверка движения ---")
    archer.move_to(10, 10)
    archer.move_to(2, 3)

    house.move_to(5, 5)

    print("\n--- Итоговое состояние ---")
    print(f"{archer.get_name()}: HP={archer.get_hp()}, Позиция=({archer.get_x()}, {archer.get_y()})")
    print(f"{enemy.get_name()}: HP={enemy.get_hp()}, Жив={enemy.is_alive()}")
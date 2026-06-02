from __future__ import annotations
from abc import ABC, abstractmethod


# ─── Products ────────────────────────────────────────────────────────────────

class Car:
    """A car with configurable parts."""
    def __init__(self):
        self.seats: int = 0
        self.engine: str = ""
        self.trip_computer: bool = False
        self.gps: bool = False

    def __str__(self):
        return (
            f"Car:\n"
            f"  Seats        : {self.seats}\n"
            f"  Engine       : {self.engine}\n"
            f"  Trip Computer: {self.trip_computer}\n"
            f"  GPS          : {self.gps}"
        )


class Manual:
    """A user manual that describes the car's configuration."""
    def __init__(self):
        self.sections: list[str] = []

    def add_section(self, text: str):
        self.sections.append(text)

    def __str__(self):
        return "Car Manual:\n" + "\n".join(f"  - {s}" for s in self.sections)


# ─── Builder Interface ────────────────────────────────────────────────────────

class Builder(ABC):
    """Specifies methods for creating the different parts of a product."""

    @abstractmethod
    def reset(self): ...

    @abstractmethod
    def set_seats(self, number: int): ...

    @abstractmethod
    def set_engine(self, engine: str): ...

    @abstractmethod
    def set_trip_computer(self, enabled: bool): ...

    @abstractmethod
    def set_gps(self, enabled: bool): ...


# ─── Concrete Builders ────────────────────────────────────────────────────────

class CarBuilder(Builder):
    """Builds an actual Car object."""

    def __init__(self):
        self.reset()

    def reset(self):
        self._car = Car()

    def set_seats(self, number: int):
        self._car.seats = number

    def set_engine(self, engine: str):
        self._car.engine = engine

    def set_trip_computer(self, enabled: bool):
        self._car.trip_computer = enabled

    def set_gps(self, enabled: bool):
        self._car.gps = enabled

    def get_product(self) -> Car:
        car = self._car
        self.reset()       # ready for next build
        return car


class CarManualBuilder(Builder):
    """Builds a Manual that documents the car's features."""

    def __init__(self):
        self.reset()

    def reset(self):
        self._manual = Manual()

    def set_seats(self, number: int):
        self._manual.add_section(f"Seats: {number}-seat configuration")

    def set_engine(self, engine: str):
        self._manual.add_section(f"Engine: {engine} — refer to Chapter 2 for operating instructions")

    def set_trip_computer(self, enabled: bool):
        if enabled:
            self._manual.add_section("Trip Computer: installed — see Chapter 4")

    def set_gps(self, enabled: bool):
        if enabled:
            self._manual.add_section("GPS: installed — see Chapter 5")

    def get_product(self) -> Manual:
        manual = self._manual
        self.reset()
        return manual


# ─── Director ────────────────────────────────────────────────────────────────

class Director:
    """
    Defines the order in which to call building steps.
    Works with any builder passed to it.
    """

    def __init__(self):
        self._builder: Builder | None = None

    def set_builder(self, builder: Builder):
        self._builder = builder

    def construct_sports_car(self):
        self._builder.reset()
        self._builder.set_seats(2)
        self._builder.set_engine("SportEngine V8")
        self._builder.set_trip_computer(True)
        self._builder.set_gps(True)

    def construct_suv(self):
        self._builder.reset()
        self._builder.set_seats(7)
        self._builder.set_engine("SUV Diesel V6")
        self._builder.set_trip_computer(True)
        self._builder.set_gps(True)


# ─── Client Code ─────────────────────────────────────────────────────────────

def main():
    director = Director()

    # ── Build a Sports Car ──
    car_builder = CarBuilder()
    director.set_builder(car_builder)
    director.construct_sports_car()
    sports_car = car_builder.get_product()
    print(sports_car)

    print()

    # ── Build its Manual ──
    manual_builder = CarManualBuilder()
    director.set_builder(manual_builder)
    director.construct_sports_car()
    sports_manual = manual_builder.get_product()
    print(sports_manual)

    print()

    # ── Build an SUV ──
    director.set_builder(car_builder)
    director.construct_suv()
    suv = car_builder.get_product()
    print(suv)

    print()

    # ── Custom build WITHOUT the director ──
    car_builder.reset()
    car_builder.set_seats(4)
    car_builder.set_engine("Hybrid Engine")
    # Trip computer and GPS omitted intentionally
    custom_car = car_builder.get_product()
    print("Custom Build (no director):")
    print(custom_car)


if __name__ == "__main__":
    main()
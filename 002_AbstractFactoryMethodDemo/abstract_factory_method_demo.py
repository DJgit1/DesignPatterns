"""
Abstract Factory Pattern Demo — GUI Factory (Dive Into Design Patterns)
User inputs OS name at runtime; matching UI elements are rendered.
"""

from abc import ABC, abstractmethod


# ──────────────────────────────────────────────
# Abstract Products
# ──────────────────────────────────────────────

class Button(ABC):
    @abstractmethod
    def paint(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def paint(self) -> str:
        pass


# ──────────────────────────────────────────────
# Concrete Products — Windows
# ──────────────────────────────────────────────

class WinButton(Button):
    def paint(self) -> str:
        return "[ Windows Button  ▣ ]"


class WinCheckbox(Checkbox):
    def paint(self) -> str:
        return "[✔] Windows Checkbox"


# ──────────────────────────────────────────────
# Concrete Products — macOS
# ──────────────────────────────────────────────

class MacButton(Button):
    def paint(self) -> str:
        return "(  macOS Button  ●  )"


class MacCheckbox(Checkbox):
    def paint(self) -> str:
        return "[◉] macOS  Checkbox"


# ──────────────────────────────────────────────
# Concrete Products — Linux
# ──────────────────────────────────────────────

class LinuxButton(Button):
    def paint(self) -> str:
        return "<  Linux Button  ◈  >"


class LinuxCheckbox(Checkbox):
    def paint(self) -> str:
        return "[■] Linux  Checkbox"


# ──────────────────────────────────────────────
# Abstract Factory
# ──────────────────────────────────────────────

class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


# ──────────────────────────────────────────────
# Concrete Factories
# ──────────────────────────────────────────────

class WinFactory(GUIFactory):
    def create_button(self) -> Button:
        return WinButton()

    def create_checkbox(self) -> Checkbox:
        return WinCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


class LinuxFactory(GUIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()


# ──────────────────────────────────────────────
# Client Code (Application)
# ──────────────────────────────────────────────

class Application:
    def __init__(self, factory: GUIFactory):
        self._factory = factory
        self._button: Button = None
        self._checkbox: Checkbox = None

    def create_ui(self):
        self._button = self._factory.create_button()
        self._checkbox = self._factory.create_checkbox()

    def paint(self):
        print("\n  Rendering UI elements:")
        print("  ┌─────────────────────────────┐")
        print(f"  │  Button  : {self._button.paint()}")
        print(f"  │  Checkbox: {self._checkbox.paint()}")
        print("  └─────────────────────────────┘")


# ──────────────────────────────────────────────
# Application Configurator / Entry Point
# ──────────────────────────────────────────────

FACTORIES = {
    "windows": WinFactory,
    "mac":     MacFactory,
    "linux":   LinuxFactory,
}


def get_factory(os_name: str) -> GUIFactory:
    key = os_name.strip().lower()
    if key not in FACTORIES:
        raise ValueError(
            f"  ✖  Unknown OS: '{os_name}'.\n"
            f"  Supported options: {', '.join(FACTORIES.keys())}"
        )
    return FACTORIES[key]()


def main():
    print("=" * 45)
    print("   Abstract Factory Pattern — GUI Demo")
    print("=" * 45)
    print(f"  Supported OS: {', '.join(FACTORIES.keys())}")
    print("-" * 45)

    os_input = input("  Enter OS name (Windows / Mac / Linux): ")

    try:
        factory = get_factory(os_input)
        app = Application(factory)
        app.create_ui()
        app.paint()
    except ValueError as e:
        print(f"\n{e}")

    print("=" * 45)


if __name__ == "__main__":
    main()
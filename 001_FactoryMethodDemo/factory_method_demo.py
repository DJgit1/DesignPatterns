from abc import ABC, abstractmethod


# Product interface
class Button(ABC):
    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def on_click(self, callback) -> None:
        pass


# Concrete products
class WindowsButton(Button):
    def render(self) -> None:
        print("Rendering a button in Windows style.")

    def on_click(self, callback) -> None:
        print("Binding a native Windows click event.")
        self.callback = callback

    def click(self) -> None:
        print("Windows button clicked.")
        self.callback()


class HTMLButton(Button):
    def render(self) -> None:
        print("Rendering a button as HTML.")

    def on_click(self, callback) -> None:
        print("Binding a browser click event.")
        self.callback = callback

    def click(self) -> None:
        print("HTML button clicked.")
        self.callback()


# Creator
class Dialog(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    def render(self) -> Button:
        button = self.create_button()
        button.on_click(self.close_dialog)
        button.render()
        return button

    def close_dialog(self) -> None:
        print("Closing dialog...")


# Concrete creators
class WindowsDialog(Dialog):
    def create_button(self) -> Button:
        return WindowsButton()


class WebDialog(Dialog):
    def create_button(self) -> Button:
        return HTMLButton()


# Client code
class Application:
    def __init__(self, os_type: str):
        self.os_type = os_type
        self.dialog = None

    def initialize(self) -> None:
        if self.os_type == "Windows":
            self.dialog = WindowsDialog()
        elif self.os_type == "Web":
            self.dialog = WebDialog()
        else:
            raise ValueError("Error! Unknown operating system.")

    def main(self) -> None:
        self.initialize()
        button = self.dialog.render()
        print()
        button.click()


if __name__ == "__main__":
    os_type = input("Enter OS type (Windows/Web): ").strip()
    app = Application(os_type)
    app.main()
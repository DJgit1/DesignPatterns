import copy
from abc import ABC, abstractmethod


# ── Abstract Base (Prototype) ──────────────────────────────────────────────────
class Shape(ABC):
    def __init__(self, source: "Shape | None" = None):
        if source is not None:
            # Prototype constructor: copy fields from source
            self.x = source.x
            self.y = source.y
            self.color = source.color
        else:
            # Default constructor
            self.x = 0
            self.y = 0
            self.color = "black"

    @abstractmethod
    def clone(self) -> "Shape":
        """Each subclass must implement its own cloning."""
        ...

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"x={self.x}, y={self.y}, color='{self.color}')"
        )


# ── Concrete Prototype: Rectangle ─────────────────────────────────────────────
class Rectangle(Shape):
    def __init__(self, source: "Rectangle | None" = None):
        super().__init__(source)               # copies x, y, color
        if source is not None:
            self.width = source.width
            self.height = source.height
        else:
            self.width = 0
            self.height = 0

    def clone(self) -> "Rectangle":
        return Rectangle(self)                 # passes self as source

    def __repr__(self):
        base = super().__repr__()[:-1]         # trim closing ')'
        return f"{base}, width={self.width}, height={self.height})"


# ── Concrete Prototype: Circle ─────────────────────────────────────────────────
class Circle(Shape):
    def __init__(self, source: "Circle | None" = None):
        super().__init__(source)               # copies x, y, color
        if source is not None:
            self.radius = source.radius
        else:
            self.radius = 0

    def clone(self) -> "Circle":
        return Circle(self)                    # passes self as source

    def __repr__(self):
        base = super().__repr__()[:-1]
        return f"{base}, radius={self.radius})"


# ── Client Code: Application ───────────────────────────────────────────────────
class Application:
    def __init__(self):
        self.shapes: list[Shape] = []

        # Create a circle and add it
        circle = Circle()
        circle.x = 10
        circle.y = 10
        circle.radius = 20
        circle.color = "red"
        self.shapes.append(circle)

        # Clone the circle — identical copy, independent object
        another_circle = circle.clone()
        self.shapes.append(another_circle)

        # Create a rectangle and add it
        rectangle = Rectangle()
        rectangle.width = 10
        rectangle.height = 20
        rectangle.color = "blue"
        self.shapes.append(rectangle)

    def business_logic(self):
        """Clone all shapes without knowing their concrete types."""
        shapes_copy: list[Shape] = []

        for shape in self.shapes:
            # Polymorphism: calls the correct clone() for each subclass
            shapes_copy.append(shape.clone())

        return shapes_copy


# ── Demo ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = Application()

    print("=== Original Shapes ===")
    for s in app.shapes:
        print(f"  {s}  |  id={id(s)}")

    clones = app.business_logic()

    print("\n=== Cloned Shapes ===")
    for s in clones:
        print(f"  {s}  |  id={id(s)}")

    print("\n=== Verify Independence (modifying a clone does not affect original) ===")
    clones[0].x = 999
    print(f"  Original circle: {app.shapes[0]}")
    print(f"  Cloned   circle: {clones[0]}")
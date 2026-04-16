from assets import assets


class CanvasButton:
    """
    A custom button class for Tkinter Canvas with hover and click states.
    """

    def __init__(self, canvas, x, y, text, callback):
        self.canvas = canvas
        self.x, self.y = x, y
        self.text = text
        self.callback = callback

        assets.load("button", "elements/button.png")
        assets.load("button-hover", "elements/button-hover.png")
        assets.load("button-click", "elements/button-click.png")

        # Assets
        self.img_normal = assets.get("button")
        self.img_hover = assets.get("button-hover")
        self.img_click = assets.get("button-click")

        # Unique tag for this specific button instance
        self.tag = f"btn_{id(self)}"

        self.draw()
        self.bind_events()

    def draw(self):
        """Initial rendering of the button components."""
        # The main image serves as the primary event target
        self.bg_id = self.canvas.create_image(
            self.x,
            self.y,
            image=self.img_normal,
            anchor="nw",
            tags=("dynamic", self.tag),
        )

        # Text shadow for the 3D effect
        self.shadow_id = self.canvas.create_text(
            self.x + 126,
            self.y + 38,
            text=self.text,
            font=("candice", 26, "bold"),
            fill="#a80e4f",
            anchor="center",
            tags=("dynamic", self.tag),
        )

        # Main text
        self.text_id = self.canvas.create_text(
            self.x + 124,
            self.y + 34,
            text=self.text,
            font=("candice", 26, "bold"),
            fill="#fefefe",
            anchor="center",
            tags=("dynamic", self.tag),
        )

    def bind_events(self):
        """Binds events to the shared tag to avoid double-triggering."""
        # Binding to the tag ensures that moving between text and image
        # doesn't trigger Enter/Leave repeatedly
        self.canvas.tag_bind(self.tag, "<Enter>", self.on_hover)
        self.canvas.tag_bind(self.tag, "<Leave>", self.on_leave)
        self.canvas.tag_bind(self.tag, "<Button-1>", self.on_press)
        self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.on_release)

    def on_hover(self, event):
        self.canvas.itemconfig(self.bg_id, image=self.img_hover)
        self.canvas.itemconfig(self.text_id, fill="#d9d9d9")

    def on_leave(self, event):
        self.canvas.itemconfig(self.bg_id, image=self.img_normal)
        self.canvas.itemconfig(self.text_id, fill="#fefefe")

    def on_press(self, event):
        """Simulates a 'pressed' look by swapping image and offsetting text."""
        self.canvas.itemconfig(self.bg_id, image=self.img_click)
        self.canvas.itemconfig(self.text_id, fill="#ffffff")

    def on_release(self, event):
        """Triggers the callback and restores original appearance."""
        self.canvas.itemconfig(self.bg_id, image=self.img_hover)
        self.canvas.itemconfig(self.text_id, fill="#d9d9d9")
        if self.callback:
            self.callback()


class SmallCanvasButton(CanvasButton):
    """
    A custom small button class for Tkinter Canvas with hover and click states.
    """

    def __init__(self, canvas, x, y, text, callback):
        self.canvas = canvas
        self.x, self.y = x, y
        self.text = text
        self.callback = callback

        assets.load("small-button", "elements/button.png", 140)
        assets.load("small-button-hover", "elements/button-hover.png", 140)
        assets.load("small-button-click", "elements/button-click.png", 140)

        # Assets
        self.img_normal = assets.get("small-button")
        self.img_hover = assets.get("small-button-hover")
        self.img_click = assets.get("small-button-click")

        # Unique tag for this specific button instance
        self.tag = f"btn_{id(self)}"

        self.draw()
        self.bind_events()

    def draw(self):
        """Initial rendering of the button components."""
        # The main image serves as the primary event target
        self.bg_id = self.canvas.create_image(
            self.x,
            self.y,
            image=self.img_normal,
            anchor="nw",
            tags=("dynamic", self.tag),
        )

        # Text shadow for the 3D effect
        self.shadow_id = self.canvas.create_text(
            self.x + 72,
            self.y + 22,
            text=self.text,
            font=("candice", 14),
            fill="#a80e4f",
            anchor="center",
            tags=("dynamic", self.tag),
        )

        # Main text
        self.text_id = self.canvas.create_text(
            self.x + 70,
            self.y + 20,
            text=self.text,
            font=("candice", 14),
            fill="#fefefe",
            anchor="center",
            tags=("dynamic", self.tag),
        )


class CanvasCircleHitBox:
    """
    A mathematical circle hitbox for the Canvas.
    Invisible by default, with a debug mode for placement.
    """

    def __init__(self, canvas, x, y, radius, callback, debug=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.callback = callback
        self.debug = debug

        self.debug_id = None

        # Listen for clicks on the entire canvas
        self.canvas.bind("<Button-1>", self.check_click, add="+")

        if self.debug:
            self.draw_debug()

    def draw_debug(self):
        """Draws a visual representation of the hitbox."""
        x1, y1 = self.x - self.radius, self.y - self.radius
        x2, y2 = self.x + self.radius, self.y + self.radius

        self.debug_id = self.canvas.create_oval(
            x1, y1, x2, y2, outline="red", width=2, dash=(4, 4), tags="debug_hitbox"
        )

    def check_click(self, event):
        """
        Mathematical check: Is the click inside the circle?
        Formula: (mouse_x - center_x)^2 + (mouse_y - center_y)^2 <= radius^2
        """
        distance_sq = (event.x - self.x) ** 2 + (event.y - self.y) ** 2
        if distance_sq <= self.radius**2:
            if self.callback:
                self.callback()

    def toggle_debug(self):
        """Switch debug view on or off."""
        self.debug = not self.debug
        if self.debug:
            self.draw_debug()
        elif self.debug_id:
            self.canvas.delete(self.debug_id)
            self.debug_id = None

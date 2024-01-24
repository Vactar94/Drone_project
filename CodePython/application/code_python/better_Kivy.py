from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Rectangle, Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


class Rectangle_hint(Widget):
    def __init__(self, color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(*color)
            self.rrect = RoundedRectangle(pos=self.calculate_initial_pos(), size=self.size)

        self.bind(pos=self.update_rrect_pos_size, size=self.update_rrect_pos_size)

    def calculate_initial_pos(self):
        # Calculer la position initiale du RoundedRectangle en utilisant pos_hint
        if self.parent:
            center_x = self.pos_hint.get('center_x', 0.5)
            center_y = self.pos_hint.get('center_y', 0.5)
            x = self.pos_hint.get('x', 0.0)
            y = self.pos_hint.get('y', 0.0)

            return (
                self.parent.x + self.parent.width * (center_x - 0.5) + self.parent.width * x,
                self.parent.y + self.parent.height * (center_y - 0.5) + self.parent.height * y
            )
        return self.pos

    def on_size(self, instance, value):
        # La méthode on_size est appelée lors du premier affichage
        self.rrect.pos = self.calculate_initial_pos()
        self.rrect.size = (
            self.parent.width * self.size_hint[0],
            self.parent.height * self.size_hint[1]
        )

    def update_rrect_pos_size(self, instance, value):
        self.rrect.pos = self.pos
        self.rrect.size = self.size


class RoundedRectangle_hint(Widget):
    def __init__(self, color=(1, 1, 1, 1), radius=[0, 0], **kwargs):
        super().__init__(**kwargs)

        # Créez le RoundedRectangle initial
        with self.canvas:
            Color(*color)
            self.rrect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)

        # Liez la mise à jour du RoundedRectangle aux changements de pos et size du widget parent
        self.bind(pos=self.update_rrect_pos_size, size=self.update_rrect_pos_size)

    def update_rrect_pos_size(self, instance, value):
        # Mettez à jour la position et la taille du RoundedRectangle en fonction du widget parent
        self.rrect.pos = self.pos
        self.rrect.size = self.size


class Better_Button(Button):
    _get_added_widget = []

    def __init__(self, angle=0, **kwargs):
        super().__init__(**kwargs)

        # Ajoutez une transformation pour changer la direction du txt
        if angle != 0:
            with self.canvas.before:
                PushMatrix()
                self.rot = Rotate(angle=angle, center=(self.size[0] * 0.5, self.size[1] * 0.5))

            with self.canvas.after:
                PopMatrix()

        self.bind(pos=self.update_rotation_origin, size=self.update_rotation_origin)

    def update_rotation_origin(self, instance, value):
        # Mettez à jour l'origine de la rotation lorsque la position ou la taille change
        try:
            self.rot.origin = self.center
        except:
            pass

    @property
    def get_added_widget(self) -> list:
        return self._get_added_widget

    def add_widget(self, widget, index=0, canvas=None):
        self.get_added_widget.append(widget)
        return super().add_widget(widget, index, canvas)


class Better_Label(Label):
    _get_added_widget = []

    def __init__(self, angle=0, **kwargs):
        super().__init__(**kwargs)

        # Ajoutez une transformation pour changer la direction du txt
        if angle != 0:
            with self.canvas.before:
                PushMatrix()
                self.rot = Rotate(angle=angle, center=(self.size[0] * 0.5, self.size[1] * 0.5))

            with self.canvas.after:
                PopMatrix()

        self.bind(pos=self.update_rotation_origin, size=self.update_rotation_origin)

    def update_rotation_origin(self, instance, value):
        # Mettez à jour l'origine de la rotation lorsque la position ou la taille change
        try:
            self.rot.origin = self.center
        except:
            pass

    @property
    def get_added_widget(self) -> list:
        return self._get_added_widget

    def add_widget(self, widget, index=0, canvas=None):
        self.get_added_widget.append(widget)
        return super().add_widget(widget, index, canvas)


class Better_Screen(Screen):
    _get_added_widget = []

    def __init__(self, notifications: dict = None, **kw):

        super().__init__(**kw)
        self.streamable = False

        if notifications != None and type(notifications) != dict:
            print("notification incorrecte il faut passer un dictonnaire enculer ")
            print(notifications.text)
            a = 1 + "g"
        else:
            self.notifications = notifications

    @property
    def get_added_widget(self) -> list:
        return self._get_added_widget

    def add_widget(self, widget, index=0, canvas=None):
        self.get_added_widget.append(widget)
        return super().add_widget(widget, index, canvas)

    def update_bg(self, element, value):
        """update les positions des bg de pleins de trucs"""
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size

    def on_pre_leave(self, *args):
        return super().on_pre_leave(*args)

    def __str__(self):
        return self.name


class RoundedImage(Widget):
    def __init__(self, image_source: str, radius: list[int, int], **kwargs):
        self.image = Image(source=image_source, allow_stretch=True, keep_ratio=False)
        super(RoundedImage, self).__init__(**kwargs)

        self.add_widget(self.image)

        self.radius = radius

    def on_size(self, instance, value):
        self.image.size = self.size
        self.image.pos = self.pos

    def on_pos(self, instance, value):
        self.image.pos = value

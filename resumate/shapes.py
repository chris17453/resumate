
class shape_rectangle:
    def __init__(self, id, left=0, top=0, width=0, height=0,background_color=None):
        self.id = id
        self._left = left
        self._top = top
        self._width = width
        self._height = height
        self._background_color = background_color
        self._type="rect"

    @property
    def type(self):
        return self._type

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
    @property
    def background_color(self):
        return self._background_color

class shape_circle:
    def __init__(self, id, left=0, top=0, diameter=0, background_color=None):
        self.id = id
        self._left = left
        self._top = top
        self._diameter = diameter
        self._background_color = background_color
        self._type="circle"

    @property
    def type(self):
        return self._type

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @property
    def diameter(self):
        return self._diameter

    @property
    def radius(self):
        return self._diameter/2

    @property
    def background_color(self):
        return self._background_color

class shape_picture:
    def __init__(self, id, left=0, top=0, max_width=0, max_height=0, mask=None,background_color=None):
        self.id = id
        self._left = left
        self._top = top
        self._width=None
        self._height=None
        self._max_width=max_width
        self._max_height=max_height
        self._background_color = background_color
        self._mask=mask
        self._type="picture"

    @property
    def type(self):
        return self._type

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @property
    def background_color(self):
        return self._background_color

    @property
    def image(self):
        return self._image
    
    @property
    def height(self):
        return self._height
    @property
    def width(self):
        return self._width

    @property
    def max_height(self):
        return self._max_height
    @property
    def max_width(self):
        return self._max_width
    @property
    def mask(self):
        return self._mask


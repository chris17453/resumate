from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus import Flowable
from reportlab.lib import colors

rendered_details = []

def capture_details(flowable,  x, y):
    global rendered_details
    # Store information about this flowable
    # Store details including the text, position, size, and style
    rendered_details.append({
        "x": x,
        "y": y,
        "flowable":flowable

    })


class ParagraphD(Paragraph):
    def __init__(self, text, style, **kwargs):
        super().__init__(text, style, **kwargs)  # Pass all keyword arguments to the superclass
        self.details = {}

    def drawOn(self, canvas, x, y, _sW=0):
        #width, height = self.wrap(canvas._doc.width, canvas._doc.height)
        super().drawOn(canvas, x, y, _sW)
        capture_details(self,  x, y)
        frame_height = self._frame._height  # Get the available height of the frame
        line_height = frame_height - self.height  # Calculate the position of the line relative to the bottom of the frame
        #print(y,line_height)

class LineDrawer(Flowable):
    def __init__(self, height=0, color=colors.black,frame=None):

        super().__init__()
        self.width = 1
        self.height = height
        self.color = color
        self._frame=frame
        

    def draw(self):
        self.canv.setStrokeColor(self.color)
        width=self._frame._width
    
        self.canv.line(0, self.height,width, self.height)
        frame_height = self._frame._height if self._frame else self.height
        frame_y_position = self._frame._y if self._frame else 0
        line_height = frame_y_position  - self.height  
       
        capture_details(self,  0, line_height)

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

class SpacerD(Flowable):
    def __init__(self,width=0, height=0, thing=0):
        super().__init__()
        self.width = width
        self.height = height
    
    def draw(self):
        frame_y_position = self._frame._y if self._frame else 0
        line_height = frame_y_position  - self.height  
        capture_details(self,  self._frame.width, line_height)

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

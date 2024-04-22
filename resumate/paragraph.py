import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import Flowable
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg,logger
from reportlab.graphics import renderPDF
from reportlab.pdfbase.pdfmetrics import stringWidth
from io import BytesIO
import logging

rendered_details = []
import warnings

def capture_details(flowable,  x, y):
    global rendered_details
    if hasattr(flowable,'parent'):
        return
    # Store information about this flowable
    # Store details including the text, position, size, and style
    rendered_details.append({
        "x": x,
        "y": y,
        "flowable":flowable

    })

# Step 1: Create a custom logging handler
class WarningCaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.warnings = []

    def emit(self, record):
        if record.levelno == logging.WARNING:
            raise Exception(f"Warning escalated to error: {record.getMessage()}")


# Step 2: Get the logger used by svg2rlg
logger = logging.getLogger('svglib')

# Step 3: Set the logger level to capture warnings
logger.setLevel(logging.WARNING)

# Step 4: Attach the custom handler to the logger
handler = WarningCaptureHandler()
logger.addHandler(handler)


def search_svg(technology):
    # Navigate to the icons directory
    icons_dir = "devicon/icons"
    tech_dir = os.path.join(icons_dir, technology)

    # Check if the technology directory exists
    if not os.path.exists(tech_dir):
        print("Technology not found.")
        return None

    # Get all SVG files in the technology directory
    svg_files = [f for f in os.listdir(tech_dir) if f.endswith(".svg")]

    # Sort files with "original" and without "wordmark" first, then others
    def custom_sort(item):
        if "original" in item:
            if "wordmark" in item:
                return 1  # "original wordmark" as second priority
            return 0  # "original" as top priority
        return 2  # all other items as lowest priority

    svg_files=sorted(svg_files,key= custom_sort)

    # Attempt to draw and render each SVG file and handle warnings as exceptions
    for svg_file in svg_files:
        svg_path = os.path.join(tech_dir, svg_file)
        try:
            drawing = svg2rlg(svg_path)
            # Create a buffer for PDF output
            buffer = BytesIO()
            # Render the drawing to the buffer
            renderPDF.drawToFile(drawing, buffer)
            buffer.close()
            return svg_path
        except Exception as e:
            print(f"Error loading or drawing SVG file {svg_path}: {e}")
            continue

    print("No suitable SVG files found for the technology.")
    return None

class ParagraphD(Paragraph):
    def __init__(self, text, style, **kwargs):
        super().__init__(text, style, **kwargs)  # Pass all keyword arguments to the superclass
        self.details = {}


    #def wrap(self,aW,aH):
    #    
    #    width = stringWidth(self.text, self.style['font_name'], self.style['font_size'])
    #    
    #    return super.wrapOn(aW,aH)
    #    #return self.width,self.height

    def wrapOn(self, canv,  availWidth, availHeight):
        text_width = stringWidth(self.text, self.style.fontName, self.style.fontSize)
        #print( text_width)
        # Constrain the width to the calculated text width or available width, whichever is smaller
        constrained_width = min(text_width, availWidth)
        # Use the constrained width to wrap the paragraph
        return super().wrap(constrained_width, availHeight)


    def drawOn(self, canvas, x, y, _sW=0):
        #width, height = self.wrap(canvas._doc.width, canvas._doc.height)
        super().drawOn(canvas, x, y, _sW)
        capture_details(self,  x, y)
        #print(y,line_height)

class SingleWordD(Flowable):
    def __init__(self, text, style):
        super().__init__()
        self.text = text
        self.style=style
        

    def wrap(self, availWidth, availHeight):
        # Use stringWidth to calculate the width of the word
        self.width = stringWidth(self.text, self.style.fontName, self.style.fontSize)
        self.height = self.style.fontSize * 1.2  # Approximate height based on font size
        return self.width, self.height

    def draw(self):
        # Set the font and draw the word
        self.canvas.setFont(self.style.fontName, self.style.fontSize)
        self.canvas.setFillColor(self.style.textColor)
        self.canvas.drawString(self.x,self.y, self.text)

    def drawOn(self, canvas, x, y, _sW=0):
        self.canvas=canvas
        #width, height = self.wrap(canvas._doc.width, canvas._doc.height)
        self.x=x
        self.y=y
        self.draw()

        capture_details(self,  x, y)


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
    
    #def draw(self):
    #    frame_y_position = self._frame._y if self._frame else 0
    #    line_height = frame_y_position  - self.height  
    #    capture_details(self,  self._frame.width, line_height)
    def drawOn(self, canvas, x, y, _sW=0):
        self.canvas=canvas
        #width, height = self.wrap(canvas._doc.width, canvas._doc.height)
        self.x=x
        self.y=y
        capture_details(self,  self.width+x, y)


    def wrap(self,aW,Ah):
        return self.width,self.height
    
class SVGFlowableD(Flowable):
    def __init__(self, svg_file, width=None, height=None):
        super().__init__()
        self.svg_file = search_svg(svg_file)
        self.target_width=width
        self.target_height=height
        self.drawing = svg2rlg(self.svg_file)
        if self.drawing==None:
            self.width=width
            self.height=height
        else:    
            # Calculate scaling factors based on desired width and height
            if self.target_width and self.target_height:
                scaling_x = self.target_width / self.drawing.minWidth()
                scaling_y = self.target_height / self.drawing.height
            elif self.width:
                scaling_x = scaling_y = self.target_width / self.drawing.width
            elif self.height:
                scaling_x = scaling_y = self.target_height / self.drawing.height
            else:
                print("Either width or height must be provided.")
                return
            self.drawing.width = self.drawing.minWidth() * scaling_x
            self.drawing.height = self.drawing.height * scaling_y
            self.width = self.drawing.width
            self.height = self.drawing.height
            self.drawing.scale(scaling_x,scaling_y)

    def wrapOn(self,canv, width, height):
        return self.width,self.height


    def drawOn(self, canv, x, y, _sW=0):
        self.canv = canv
        if self.drawing:
            renderPDF.draw(self.drawing, canv, x,y)
        capture_details(self,  x, y)




class SVGRRowD(Flowable):
    def __init__(self, contents=[], **kwargs):
        super().__init__(**kwargs)
        
        self.width=0
        self.height=0
        for item in contents:
            item.parent=self

        self.contents = contents

    def calc_dimentions(self,width,height):
        mx=0
        my=0
        height=0
        width=width

        for item in self.contents:
            w,h=item.wrap(width,height)
            if h>height: 
                height=h

            if mx+w>width:
                mx=0
                my+=height
                height=0
            mx+=w
        my+=height

        self.width=mx
        self.height=my    

    
    def wrapOn(self,canv, width, height):
        super().wrapOn(canv, width, height)
        self.calc_dimentions(width,height)
        return self.width, self.height


    def drawOn(self, canvas, x, y, _sW):
        #super().drawOn(canvas, x, y, _sW)
        mx=0
        my=0
        height=0
        width=self._frame.width
        for flowable in self.contents:
            w,h=flowable.wrap(self.width,self.height)
            if h>height: 
                height=h

            if mx+w>width:
                mx=0
                my-=height
                height=0
            #canvas.setStrokeColorRGB(0, 0, 0)  # Black color for the rectangle
            #canvas.rect(x+mx,y+my,flowable.width, flowable.height, stroke=1, fill=0)
            flowable.drawOn(canvas, x+mx, y+my)
            mx+=w
           
        my-=height
        capture_details(self,  x, y)



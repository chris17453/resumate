import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import Flowable
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg,logger,Svg2RlgAttributeConverter
from reportlab.graphics import renderPDF
from reportlab.pdfbase.pdfmetrics import stringWidth
from io import BytesIO
import logging

from .svg_flatener import flaten_svg

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

def insert_suffix_before_extension(filename, suffix):
    base_name, extension = os.path.splitext(filename)
    return f"{base_name}_{suffix}{extension}"

def search_svg(technology):
    svg_files=[technology]
    # if this is not a actual URL
    if not os.path.exists(technology):
        # Navigate to the icons directory
        icons_dir = "submodules/devicons/icons"
        tech_dir = os.path.join(icons_dir, technology)
        
        if os.path.exists(tech_dir):
            # Get all SVG files in the technology directory
            svg_files = [os.path.join(tech_dir, f) for f in os.listdir(tech_dir) if f.endswith(".svg")]
            


            # Sort files with "original" and without "wordmark" first, then others
            def custom_sort(item):
                if "original" in item:
                    if "wordmark" in item:
                        return 1  # "original wordmark" as second priority
                    return 0  # "original" as top priority
                return 2  # all other items as lowest priority

            svg_files=sorted(svg_files,key= custom_sort)

        else:
            print("Technology not in devicon")
            print(technology)
            icons_dir = os.path.join("submodules/logos/logos",technology.replace(' ','-')+".svg")
            print(icons_dir)
            if not os.path.exists(icons_dir):    
                print("Technology not in logos: "+icons_dir)
                return None
            svg_files=[icons_dir]


    # Attempt to draw and render each SVG file and handle warnings as exceptions
    for svg_file in svg_files:
        try:
            drawing = svg2rlg(svg_file)
            # Create a buffer for PDF output
            buffer = BytesIO()
            # Render the drawing to the buffer
            renderPDF.drawToFile(drawing, buffer)
            buffer.close()
            return svg_file
        except Exception as e:
            output=insert_suffix_before_extension(svg_file,"_flatten")
            print ("Flatening")
            print(output)
            flaten_svg(svg_file,output)
            print ("Flatening")
            print(output)
            return output
            #print(f"Error loading or drawing SVG file {svg_path}: {e}")
            #continue

    print("No suitable SVG files found for the technology.")
    return None

class ParagraphD(Paragraph):
    def __init__(self, text, style,debug=None, **kwargs):
        if  style.bold:
            text=f"<b>{text}</b>"
            #print("BOLD"+text)
                        
        super().__init__(text, style, **kwargs)  # Pass all keyword arguments to the superclass
        self.details = {}
        self.debug=debug


    def wrapOn(self, canv,  availWidth, availHeight):
        text_width = stringWidth(self.text, self.style.fontName, self.style.fontSize)
        #print( text_width)
        # Constrain the width to the calculated text width or available width, whichever is smaller
        constrained_width = min(text_width, availWidth)
        # Use the constrained width to wrap the paragrap
        return super().wrap(constrained_width, self.style.leading+self.style.spaceAfter+self.style.spaceBefore)


    def drawOn(self, canvas, x, y, _sW=0):
        #width, height = self.wrap(canvas._doc.width, canvas._doc.height)
        super().drawOn(canvas, x, y, _sW)
        if self.debug: 
            canvas.setStrokeColorRGB(0, 0, 0)  # Black color for the rectangle
            canvas.rect(x,y,self.width, self.height, stroke=1, fill=0)

         
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
    def __init__(self, svg_file, text=None, style=None, placement="bottom", size=0,padding=5,color=None,debug=None):
        super().__init__()
        mapping = (
            ("red", colors.red),
            ("#ff0000", colors.red),
            ("#ff000055", colors.Color(1, 0, 0, 1/3.0)),
            ("#f00", colors.red),
            ("#f00f", colors.red),
            ("rgb(100%,50%,10%)", colors.Color(1, 1.0/255 * 128, 1.0/255 * 26, 1)),
            ("rgb(255, 0, 0)", colors.red),
            ("rgba(255, 255, 128, .5)", colors.Color(1, 1, 1.0/255 * 128, .5)),
            ("fuchsia", colors.Color(1, 0, 1, 1)),
            ("slategrey", colors.HexColor(0x708090)),
            ("transparent", colors.Color(0, 0, 0, 0)),
            ("whatever", None),
        )
        args={}
        if color!=None:
            color_number = int(color[1:], 16)
            args['color_converter']= lambda x:colors.HexColor(color)


        self.svg_file = search_svg(svg_file)
        self.drawing = svg2rlg(self.svg_file,**args)
        self.text=text
        self.style=style
        self.svg_x=0
        self.svg_y=0
        self.svg_width=size
        self.svg_height=size
        self.text_x=0
        self.text_y=0
        self.text_width=0
        self.text_height=0
        self.padding=padding
        self.placement=placement
        self.debug=debug
        self.calculate_bounds()

    def calculate_bounds(self):
        if self.text:
            self.text_width = stringWidth(self.text, self.style.fontName, self.style.fontSize)
            self.text_height = self.style.leading #x+self.text_x,y+self.text_y
        if self.drawing:
            # Calculate scaling factors based on desired width and height
            if self.svg_width and self.svg_height:
                scaling_x = self.svg_width / self.drawing.minWidth()
                scaling_y = self.svg_height / self.drawing.height
            elif self.width:
                scaling_x = scaling_y = self.svg_width / self.drawing.width
            elif self.height:
                scaling_x = scaling_y = self.svg_height / self.drawing.height
            else:
                print("Either width or height must be provided.")
                return
            self.drawing.width = self.drawing.minWidth() * scaling_x
            self.drawing.height = self.drawing.height * scaling_y
            self.svg_width = self.drawing.width
            self.svg_height = self.drawing.height
            self.drawing.scale(scaling_x,scaling_y)

        if self.placement=="bottom":
            self.width=max(self.svg_width,self.text_width)+self.padding*2
            self.height=self.svg_height+self.text_height+self.padding*3

            self.text_x=(self.width-self.text_width)/2
            self.text_y=self.padding #self.height-self.text_height-self.padding
            self.svg_x=(self.width-self.svg_width)/2
            self.svg_y=self.padding*2+self.text_height

        elif self.placement=="top":
            self.width=max(self.svg_width,self.text_width)+self.padding*2
            self.height=self.svg_height+self.text_height+self.padding*3

            self.text_x=(self.width-self.text_width)/2
            self.text_y=self.padding*2+self.svg_height #self.height-self.text_height-self.padding
            self.svg_x=(self.width-self.svg_width)/2
            self.svg_y=self.padding

        elif self.placement=="left":
            self.width=self.svg_width+self.text_width+self.padding*2
            self.height=self.svg_height+self.padding*2

            self.text_x=self.padding
            self.text_y=(self.height-self.text_height)/2
            self.svg_x=self.padding*2+self.text_width
            self.svg_y=self.padding

        elif self.placement=="right":
            self.width=self.svg_width+self.text_width+self.padding*2
            self.height=self.svg_height+self.padding*2

            self.text_x=self.padding*2+self.svg_width
            self.text_y=(self.height-self.text_height)/2
            self.svg_x=self.padding
            self.svg_y=self.padding


    def wrapOn(self,canv, width, height):
        return self.width,self.height

    def drawOn(self, canvas, x, y, _sW=0):
        if self.drawing:
            renderPDF.draw(self.drawing, canvas, x+self.svg_x,y+self.svg_y)
            if self.debug: 
                canvas.setStrokeColorRGB(0, 0, 0)  # Black color for the rectangle
                canvas.rect(x+self.svg_x,y+self.svg_y,self.svg_width, self.svg_height, stroke=1, fill=0)

        canvas.setFont(self.style.fontName, self.style.fontSize)
        canvas.setFillColor(self.style.textColor)
        canvas.drawString(x+self.text_x,y+self.text_y, self.text)
        if self.debug: 
            canvas.setStrokeColorRGB(0, 0, 0)  # Black color for the rectangle
            canvas.rect(x+self.text_x,y+self.text_y,self.text_width, self.text_height, stroke=1, fill=0)

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
            
            if mx+w>width:
                mx=0
                my+=height
                height=0
                
            if h>height: 
                height=h

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
        for item in self.contents:
            w,h=item.wrap(width,height)
            
            if mx+w>width:
                mx=0
                my+=height
                height=0
                
            if h>height: 
                height=h

            item.drawOn(canvas, x+mx, y+my)
            mx+=w
        my+=height
            #canvas.setStrokeColorRGB(0, 0, 0)  # Black color for the rectangle
            #canvas.rect(x+mx,y+my,flowable.width, flowable.height, stroke=1, fill=0)
        capture_details(self,  x, y)



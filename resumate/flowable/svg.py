import os
from reportlab.platypus import Flowable
from reportlab.lib import colors
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfbase.pdfmetrics import stringWidth
from io import BytesIO
from .common import capture_details
from .svg_flatener import flaten_svg


def insert_suffix_before_extension(filename, suffix):
    base_name, extension = os.path.splitext(filename)
    return f"{base_name}_{suffix}{extension}"



def search_svg(technology):
    svg_files = [technology]
    
    # If this is an actual file path, use it directly
    if os.path.exists(technology):
        return technology
        
    # Navigate to the icons directory
    icons_dir = "submodules/devicons/icons"
    tech_dir = os.path.join(icons_dir, technology.lower())  # Convert to lowercase for matching

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

        svg_files = sorted(svg_files, key=custom_sort)
    else:
        # Try logos directory
        icons_dir = os.path.join("submodules/logos/logos", technology.replace(' ', '-').lower() + ".svg")
        if os.path.exists(icons_dir):
            svg_files = [icons_dir]
        else:
            # Try some common name variations
            variations = [
                technology.lower(),
                technology.upper(), 
                technology.capitalize(),
                technology.replace(' ', ''),
                technology.replace(' ', '-'),
                technology.replace(' ', '_')
            ]
            
            for variation in variations:
                # Check devicons with variation
                tech_dir = os.path.join("submodules/devicons/icons", variation)
                if os.path.exists(tech_dir):
                    svg_files = [os.path.join(tech_dir, f) for f in os.listdir(tech_dir) if f.endswith(".svg")]
                    break
                    
                # Check logos with variation
                logo_path = os.path.join("submodules/logos/logos", variation + ".svg")
                if os.path.exists(logo_path):
                    svg_files = [logo_path]
                    break
            else:
                # If no SVG found, return None instead of trying to process
                print(f"Warning: No SVG found for technology '{technology}'")
                return None

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
            # Try flattening the SVG
            try:
                output = insert_suffix_before_extension(svg_file, "_flatten")
                print(f"Flattening SVG: {svg_file} -> {output}")
                flaten_svg(svg_file, output)
                
                # Test the flattened version
                drawing = svg2rlg(output)
                buffer = BytesIO()
                renderPDF.drawToFile(drawing, buffer)
                buffer.close()
                return output
            except Exception as flatten_error:
                print(f"Error processing SVG file {svg_file}: {e}")
                print(f"Flattening also failed: {flatten_error}")
                continue

    print(f"No suitable SVG files found for the technology: {technology}")
    return None
          

def search_svg2(technology):
    """Search for SVG icons - simplified and fixed version."""
    import os
    
    # If it's already a valid path, return it
    if technology and os.path.exists(technology):
        return technology
    
    if not technology:
        print(f"Warning: Empty technology name provided")
        return None
    
    # Clean the technology name for searching
    clean_name = technology.lower().replace(' ', '').replace('/', '').replace('-', '').replace('#', 'sharp').replace('+', 'plus').replace('.', '')
    
    print(f"DEBUG: Searching for '{technology}' -> cleaned: '{clean_name}'")
    
    # Direct mappings for problem icons
    direct_mappings = {
        'vmwarevsphere': 'vmware',
        'mysqlmariadb': 'mysql',
        'bashell': 'bash',
        'cplusplus': 'cplusplus',
        'csharp': 'csharp',
    }
    
    search_name = direct_mappings.get(clean_name, clean_name)
    
    # List of paths to check
    base_paths = [
        f"submodules/devicons/icons/{search_name}",
        f"submodules/logos/logos/{search_name}.svg",
    ]
    
    # Check each path
    for path in base_paths:
        print(f"DEBUG: Checking path: {path}")
        
        # If it's a directory (devicons style)
        if os.path.isdir(path):
            print(f"DEBUG: Found directory: {path}")
            try:
                files = os.listdir(path)
                svg_files = [f for f in files if f.endswith('.svg')]
                print(f"DEBUG: SVG files in directory: {svg_files}")
                
                if svg_files:
                    # Priority order
                    for priority in ['original', 'plain']:
                        for svg_file in svg_files:
                            if priority in svg_file and 'wordmark' not in svg_file:
                                full_path = os.path.join(path, svg_file)
                                print(f"DEBUG: Selected priority file: {full_path}")
                                return full_path
                    
                    # Just return first SVG if no priority match
                    full_path = os.path.join(path, svg_files[0])
                    print(f"DEBUG: Selected first file: {full_path}")
                    return full_path
            except Exception as e:
                print(f"DEBUG: Error reading directory {path}: {e}")
        
        # If it's a direct file path
        elif os.path.exists(path):
            print(f"DEBUG: Found file: {path}")
            return path
    
    print(f"Warning: No SVG found for '{technology}'")
    return None

class SVGFlowableD(Flowable):
    def __init__(self, svg_file, text=None, style=None, placement="bottom", size=0,padding=5,color=None,debug=None):
        super().__init__()

        args={}
        if color!=None:
            if isinstance(color,str):
                color = int(color[1:], 16)
            args['color_converter']= lambda x:colors.HexColor(color)

        self.svg_file = search_svg(svg_file)
        
        # Handle missing SVG gracefully
        if self.svg_file is None:
            self.drawing = None
            print(f"Warning: Using text-only fallback for missing SVG: {svg_file}")
        else:
            try:
                self.drawing = svg2rlg(self.svg_file, **args)
            except Exception as e:
                print(f"Error loading SVG {self.svg_file}: {e}")
                self.drawing = None
                
        self.text = text
        self.style = style
        self.svg_x = 0
        self.svg_y = 0
        self.svg_width = size if self.drawing else 0
        self.svg_height = size if self.drawing else 0
        self.text_x = 0
        self.text_y = 0
        self.text_width = 0
        self.text_height = 0
        self.padding = padding
        self.placement = placement
        self.debug = debug
        self.calculate_bounds()

    def calculate_bounds(self):
        if self.text:
            self.text_width = stringWidth(self.text, self.style.fontName, self.style.fontSize)
            self.text_height = self.style.leading
            
        if self.drawing:
            # Calculate scaling factors based on desired width and height
            if self.svg_width and self.svg_height:
                scaling_x = self.svg_width / self.drawing.minWidth()
                scaling_y = self.svg_height / self.drawing.height
            elif self.svg_width:
                scaling_x = scaling_y = self.svg_width / self.drawing.width
            elif self.svg_height:
                scaling_x = scaling_y = self.svg_height / self.drawing.height
            else:
                print("Either width or height must be provided.")
                return
            self.drawing.width = self.drawing.minWidth() * scaling_x
            self.drawing.height = self.drawing.height * scaling_y
            self.svg_width = self.drawing.width
            self.svg_height = self.drawing.height
            self.drawing.scale(scaling_x, scaling_y)

        # Layout calculations - handle missing SVG case
        if self.placement == "bottom":
            self.width = max(self.svg_width, self.text_width) + self.padding * 2
            self.height = self.svg_height + self.text_height + self.padding * 3

            self.text_x = (self.width - self.text_width) / 2
            self.text_y = self.padding
            self.svg_x = (self.width - self.svg_width) / 2
            self.svg_y = self.padding * 2 + self.text_height

        elif self.placement == "top":
            self.width = max(self.svg_width, self.text_width) + self.padding * 2
            self.height = self.svg_height + self.text_height + self.padding * 3

            self.text_x = (self.width - self.text_width) / 2
            self.text_y = self.padding * 2 + self.svg_height
            self.svg_x = (self.width - self.svg_width) / 2
            self.svg_y = self.padding

        elif self.placement == "left":
            self.width = self.svg_width + self.text_width + self.padding * 2
            self.height = max(self.svg_height, self.text_height) + self.padding * 2

            self.text_x = self.padding
            self.text_y = (self.height - self.text_height) / 2
            self.svg_x = self.padding * 2 + self.text_width
            self.svg_y = self.padding

        elif self.placement == "right":
            self.width = self.svg_width + self.text_width + self.padding * 2
            self.height = max(self.svg_height, self.text_height) + self.padding * 2

            self.text_x = self.padding * 2 + self.svg_width
            self.text_y = (self.height - self.text_height) / 2
            self.svg_x = self.padding
            self.svg_y = self.padding

        # If no SVG, just use text dimensions
        if not self.drawing:
            self.width = self.text_width + self.padding * 2
            self.height = self.text_height + self.padding * 2
            self.text_x = self.padding
            self.text_y = self.padding

    def wrap(self, width, height):
        return self.width, self.height

    def wrapOn(self, canv, width, height):
        return self.width, self.height

    def drawOn(self, canvas, x, y, _sW=0):
        # Draw SVG if available
        if self.drawing:
            renderPDF.draw(self.drawing, canvas, x + self.svg_x, y + self.svg_y)
            if self.debug:
                canvas.setStrokeColorRGB(0, 0, 0)
                canvas.rect(x + self.svg_x, y + self.svg_y, self.svg_width, self.svg_height, stroke=1, fill=0)

        # Draw text
        if self.text:
            canvas.setFont(self.style.fontName, self.style.fontSize)
            canvas.setFillColor(self.style.textColor)
            canvas.drawString(x + self.text_x, y + self.text_y, self.text)
            if self.debug:
                canvas.setStrokeColorRGB(0, 0, 0)
                canvas.rect(x + self.text_x, y + self.text_y, self.text_width, self.text_height, stroke=1, fill=0)

        capture_details(self, x, y)



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

    def wrap(self, availWidth, availHeight):
        #super().wrap(availWidth,availHeight)
        self.calc_dimentions(availWidth,availHeight)
        return self.width, self.height

    
    def wrapOn(self,canv, width, height):
        #super().wrapOn(canv, width, height)
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
                my-=height
                height=0
                
            if h>height: 
                height=h

            item.drawOn(canvas, x+mx, y-my)
            mx+=w
        my-=height
            #canvas.setStrokeColorRGB(0, 0, 0)  # Black color for the rectangle
            #canvas.rect(x+mx,y+my,flowable.width, flowable.height, stroke=1, fill=0)
        capture_details(self,  x, y)



from reportlab.platypus import Paragraph,Frame,Image
from .shapes import shape_circle,shape_rectangle, shape_picture
from reportlab.lib.utils import ImageReader
from .flowable import LineDrawer, ParagraphD

from .section import add_items

def draw_shapes(metadata,canvas):
    shapes=metadata['objects']

    for shape in shapes:
        item=shapes[shape]
        if not isinstance( item,shape_rectangle) and not isinstance( item,shape_circle) :
            continue
        
        hex_color=item.background_color
        if hex_color==None:
            continue
        else :
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
        # Convert to normalized RGB
        r_normalized = r / 255
        g_normalized = g / 255
        b_normalized = b / 255        
        if item.type=='rect':
            canvas.setFillColorRGB(r_normalized,g_normalized, b_normalized)  
            canvas.rect(item.left,item.top, item.width, item.height, stroke=0, fill=1)

        if item.type=='circle':
            canvas.setFillColorRGB(r_normalized,g_normalized, b_normalized)  
            canvas.circle(item.left,item.top, item.diameter, stroke=0, fill=1)


def header_footer(canvas, doc, metadata, styles):
    add_header(canvas, doc, metadata,styles)
    add_footer(canvas, doc, metadata,styles)



def add_header(canvas, doc, metadata, styles):
    resume=metadata['resume']
  # Define the dimensions and position for the header frame
    header=metadata['header']

    # draw the background objects
    draw_shapes(metadata,canvas)

    header_frame = Frame(header.left, header.top,header.width,header.height)
    

    # List of paragraphs (Flowable objects) for the header
    story=add_items(metadata['template']['global'],metadata['template']['header'],metadata['resume'],styles)
    
    # Calculate available width and starting height within the frame
    available_width = header_frame.width
    current_y = header_frame._y2
    # Draw each paragraph in the header frame on the canvas
    for flowable in story:
        flowable_width, flowable_height = flowable.wrap(header.width, header.height)  # Wrap content to fit the frame
        #print(flowable_width, flowable_height)
        try:
            current_y -= flowable.style.leading+flowable.style.spaceAfter # Move up the start position for the next flowable
        except:
            current_y -= flowable_height # Move up the start position for the next flowable
        flowable.drawOn(canvas, header_frame._x1, current_y)

    profile_image(metadata['objects']['picture'],resume['header']['picture'],canvas)    

def profile_image(object,image_path,c):
    image = ImageReader(image_path)
    image_width, image_height = image.getSize()
    aspect_ratio = image_width / image_height
    new_width = object.max_width
    new_height = new_width / aspect_ratio

    # Determine the diameter of the circle to be the smaller of the new dimensions
    circle_diameter = min(new_width, new_height)

    # Position for the image
    xpos, ypos = object.left, object.top

    if object.mask=='circle':
        # Draw a circle mask
        c.saveState()
        path = c.beginPath()  # Start a new path for clipping
        # Position the circle to be centered over the image
        path.circle(xpos + new_width / 2, ypos + new_height / 2, circle_diameter / 2)
        c.clipPath(path, stroke=0, fill=0)  # Use the path for clipping
        c.drawImage(image, xpos, ypos, new_width, new_height, mask='auto')  # Draw the image within the clipped path
        c.restoreState()  # Restore the original state (removing the clipping path)
    else:
        c.drawImage(image, xpos, ypos, new_width, new_height, mask='auto')  # Draw the image within the clipped path
        



def add_footer(canvas,doc,metadata, styles):
    resume=metadata['resume']
    # Define the dimensions and position for the header frame
    footer=metadata['footer']
    frame = Frame(footer.left, footer.top,footer.width,footer.height)

    hex_color=footer.background_color
    if hex_color==None:
        r = 0
        g = 0
        b = 0
    else :
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
    # Convert to normalized RGB
    r_normalized = r / 255
    g_normalized = g / 255
    b_normalized = b / 255        
    #canvas.setFillColorRGB(r_normalized,g_normalized, b_normalized)  # Set color to green (RGB)
    #canvas.rect(footer.left,footer.top, footer.width, footer.height, stroke=1, fill=1)

    #print(metadata)

    # List of paragraphs (Flowable objects) for the header
    story = [
        LineDrawer(5,styles['footer_Heading1'].textColor,frame),
        Paragraph(f"Page {doc.page} of {metadata['pages']} ", styles['footer_Text']),

    ]
    #print(metadata['pages'])

    # Calculate available width and starting height within the frame
    current_y = frame._y2
    # Draw each paragraph in the header frame on the canvas
    for flowable in story:
        flowable_width, flowable_height = flowable.wrap(footer.width, footer.height)  # Wrap content to fit the frame
        #print(flowable_width, flowable_height)
        try:
            current_y -= flowable.style.leading+flowable.style.spaceAfter # Move up the start position for the next flowable
        except:
            current_y -= flowable_height # Move up the start position for the next flowable
        flowable.drawOn(canvas, frame._x1, current_y)



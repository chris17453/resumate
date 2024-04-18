from reportlab.platypus import Paragraph,Frame
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def header_footer(canvas, doc, metadata, styles):
    add_header(canvas, doc, metadata,styles)
    add_footer(canvas, doc, metadata,styles)

def add_header(canvas, doc, metadata, styles):
    resume=metadata['resume']
  # Define the dimensions and position for the header frame
    header=metadata['header']
    
    hex_color=header.background_color
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
    canvas.setFillColorRGB(r_normalized,g_normalized, b_normalized)  # Set color to green (RGB)
    canvas.rect(header.left,header.top, header.width, header.height, stroke=1, fill=1)


    header_frame = Frame(header.left, header.top,header.width,header.height)
    

    # List of paragraphs (Flowable objects) for the header
    story = [
        Paragraph(f"<b>Name:</b> {resume['main_data']['name']}", styles['Title']),
        Paragraph(f"<b>Address:</b> {resume['main_data']['address']}", styles['BodyText']),
        Paragraph(f"<b>Phone:</b> {resume['main_data']['phone']}", styles['BodyText']),
        Paragraph(f"<b>Email:</b> {resume['main_data']['email']}", styles['BodyText']),
    ]

    # Calculate available width and starting height within the frame
    available_width = header_frame.width
    current_y = header_frame._y2
    # Draw each paragraph in the header frame on the canvas
    for flowable in story:
        flowable_width, flowable_height = flowable.wrap(header.width, header.height)  # Wrap content to fit the frame
        print(flowable_width, flowable_height)
        current_y -= flowable.style.leading+flowable.style.spaceAfter # Move up the start position for the next flowable
        flowable.drawOn(canvas, header_frame._x1, current_y)
        
    canvas.setFillColorRGB(0, 1, 0)  # Set color to green (RGB)
    canvas.rect(header.left,header.top, header.width, header.height, stroke=1, fill=0)

    

    # Finish up

    ## Optional: Include an image if available
    #if 'picture' in resume['main_data'] and resume['main_data']['picture']:
    #    try:
    #        img_path = resume['main_data']['picture']
    #        img = Image(img_path, width=1 * inch, height=1 * inch)
    #        if current_height >= img.height:
    #            img.drawOn(canvas, header_frame._x2 - img.width, header_frame._y2 - img.height)
    #    except Exception as e:
    #        error_msg = Paragraph(f"Failed to load image: {e}", styles['BodyText'])
    #        error_msg_width, error_msg_height = error_msg.wrap(available_width, current_height)
    #        if error_msg_height <= current_height:
    #            error_msg.drawOn(canvas, header_frame._x1, header_frame._y2 - error_msg_height)





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
    canvas.setFillColorRGB(r_normalized,g_normalized, b_normalized)  # Set color to green (RGB)
    canvas.rect(footer.left,footer.top, footer.width, footer.height, stroke=1, fill=1)



    # List of paragraphs (Flowable objects) for the header
    story = [
        Paragraph(f"<b>Page: 1 of 1</b> ", styles['Heading2']),
    ]

    # Calculate available width and starting height within the frame
    current_y = frame._y2
    # Draw each paragraph in the header frame on the canvas
    for flowable in story:
        flowable_width, flowable_height = flowable.wrap(footer.width, footer.height)  # Wrap content to fit the frame
        print(flowable_width, flowable_height)
        current_y -= flowable.style.leading+flowable.style.spaceAfter # Move up the start position for the next flowable
        flowable.drawOn(canvas, frame._x1, current_y)



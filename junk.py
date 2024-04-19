

def paginate(frame_element,elements):
    pages=[]

    frame = Frame(frame_element.left+24, frame_element.top+14,frame_element.width-48,frame_element.height-12)

    current_y = frame._y2
    page=[]
    #print(frame_element.height)
    for flowable in elements:
        flowable_width,flowable_height=flowable.wrap(frame_element.width-48,frame_element.height-12)
        space_before=0
        space_after=0
        text="None"
        if hasattr(flowable, 'style'):
            space_before=flowable.style.spaceBefore
            space_after=flowable.style.spaceAfter
            text=flowable.text
        
        
        
        if hasattr(flowable, 'style'):
            current_y -= flowable_height+flowable.style.spaceAfter # Move up the start position for the next flowable
        else:
            current_y-=flowable_height
            
        #print(flowable_height,flowable_height+space_after,space_before,current_y,frame_element.width,frame_element.height,text)
        

        if current_y <=frame._y1:
            current_y=frame._y2
            pages.append(page)
            page=[]
            if hasattr(flowable, 'style'):
                new_style = ParagraphStyle('new_style', parent=flowable.style)  # Create a new style based on the existing one
                new_style.textColor = colors.red  # Change text color
                flowable.style = new_style  # Assign the new style to the flowable            else:
        page.append(flowable)

    if len(page)>0:
        pages.append(page)
    #print(len(pages))
    return pages

        

from reportlab.platypus import Paragraph, Spacer
from .paragraph import ParagraphD, LineDrawer

def add_passions(passions, styles):
    story=[]
    story.append(ParagraphD(f"<b>Pasisons</b>", styles['Body_Text']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for item in passions:
        story.append(ParagraphD(item, styles['Body_Text']))
    story.append(Spacer(1, 12)) 
    return story

from reportlab.platypus import Paragraph, Spacer
from .paragraph import ParagraphD, LineDrawer, SpacerD

def add_achievements(achievements, styles):
    story=[]
    story.append(ParagraphD(f"<b>Achievements</b>", styles['Body_Text']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for item in achievements:
        story.append(ParagraphD(item, styles['Body_Text']))
    story.append(SpacerD(1, 15)) 
    return story

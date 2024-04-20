from reportlab.platypus import KeepTogether
from .paragraph import ParagraphD, LineDrawer, SpacerD

def add_strengths(strengths, styles):
    heading="Strengths".upper()
    story = []
    story.append(ParagraphD(heading, styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for item in strengths:
        story.append(ParagraphD(item, styles['Body_Text']))
    story.append(SpacerD(1, 15)) 
    return [KeepTogether(story)]

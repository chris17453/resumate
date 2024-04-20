from reportlab.platypus import Paragraph, Spacer
from .paragraph import ParagraphD, LineDrawer, SpacerD
from reportlab.platypus import KeepTogether


def add_achievements(achievements, styles):
    heading="Achievements".upper()
    story = []
    story.append(ParagraphD(heading, styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for item in achievements:
        story.append(ParagraphD(item, styles['Body_Text']))
    story.append(SpacerD(1, 15)) 
    return [KeepTogether(story)]

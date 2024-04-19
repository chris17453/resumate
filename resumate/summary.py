from .paragraph import ParagraphD,LineDrawer,SpacerD
from reportlab.lib import colors


def add_summary(summary, styles):
    story=[]
    story.append(ParagraphD(f"SUMMARY", styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))
    story.append(ParagraphD(summary, styles['BodyText']))
    story.append(SpacerD(1,15))
    return story

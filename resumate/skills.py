from reportlab.platypus import Paragraph, Spacer
from .paragraph import ParagraphD, LineDrawer

def add_skills(skills, styles):
    story=[]
    story.append(ParagraphD(f"<b>Skills</b>", styles['BodyText']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for skill in skills:
        story.append(ParagraphD(f"<b>{skill['category']} Skills:</b> {', '.join(skill['skills'])}", styles['BodyText']))
        story.append(Spacer(1, 12)) 
    return story

from reportlab.platypus import KeepTogether
from .paragraph import ParagraphD, LineDrawer, SpacerD

def add_skills(skills, styles):
    story=[]
    story.append(ParagraphD(f"Skills", styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for skill in skills:
        story.append(ParagraphD(f"<b>{skill['category']} Skills:</b> {', '.join(skill['skills'])}", styles['Body_Text']))
    story.append(SpacerD(1, 15)) 
    return [KeepTogether(story)]

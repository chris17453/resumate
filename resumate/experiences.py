from reportlab.platypus import Paragraph, Spacer
from .paragraph import ParagraphD, LineDrawer, SpacerD






def add_experiences(experiences, styles):
    story=[]
    story.append(ParagraphD(f"EXPERIENCE", styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for experience in experiences:
        story.extend(add_experience(experience, styles))    
    return story

def add_experience(experience, styles):

    story=[]
    story.append(ParagraphD(f"{experience['role']}", styles['Heading2']))
    story.append(ParagraphD(f"{experience['start']} - {experience['finished']}", styles['Subtitle_Right']))
    story.append(ParagraphD(f"{experience['company']}", styles['Subtitle']))
    story.append(SpacerD(1, 5)  )
    story.append(ParagraphD(f"{experience['feature_comment']}", styles['Body_Text']))
    # Successes
    successes = ', '.join(experience['successes'])
    story.append(ParagraphD(f"Successes: {successes}", styles['Body_Text']))
    story.append(SpacerD(1, 10))
    return story
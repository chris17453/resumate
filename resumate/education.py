from reportlab.platypus import Paragraph, Spacer
from .paragraph import ParagraphD, LineDrawer

from .paragraph import ParagraphD

def add_education(education, styles):
    story = []
    story.append(ParagraphD("EDUCATION", styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))
    
    # Add school name
    story.append(ParagraphD(f"School: {education['school']}", styles['BodyText']))
    
    # Add course name
    story.append(ParagraphD(f"Course: {education['course']}", styles['BodyText']))
    
    # Add start date
    story.append(ParagraphD(f"From: {education['from']}", styles['BodyText']))
    
    # Add end date
    story.append(ParagraphD(f"To: {education['to']}", styles['BodyText']))
    
    story.append(Spacer(1, 12))
    
    return story
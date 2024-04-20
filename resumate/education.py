from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus import KeepTogether
from .paragraph import ParagraphD, LineDrawer

def add_education(education, styles):
    heading="Education".upper()
    story = []
    story.append(ParagraphD(heading, styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))
    
    # Add school name
    story.append(ParagraphD(f"School: {education['school']}", styles['Body_Text']))
    
    # Add course name
    story.append(ParagraphD(f"Course: {education['course']}", styles['Body_Text']))
    
    # Add start date
    story.append(ParagraphD(f"From: {education['from']}", styles['Body_Text']))
    
    # Add end date
    story.append(ParagraphD(f"To: {education['to']}", styles['Body_Text']))
    
    story.append(Spacer(1, 12))
    
    return [KeepTogether(story)]

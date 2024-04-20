from reportlab.platypus import Paragraph, Spacer
from .paragraph import ParagraphD, LineDrawer, SpacerD
from reportlab.platypus import KeepTogether

def add_certificates(certificates, styles):
    heading="Certificates".upper()
    story = []
    story.append(ParagraphD(heading, styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))


    for certificate in certificates:
        # Add each part of the certificate as a separate paragraph
        story.append(ParagraphD(f"School: {certificate['school']}", styles['Body_Text']))
        story.append(ParagraphD(f"Course: {certificate['course']}", styles['Body_Text']))
        story.append(ParagraphD(f"Date: {certificate['date']}", styles['Body_Text']))
        story.append(SpacerD(1, 12))  # Add space after each full certificate entry

    # Keep all certificate entries together on the same page if possible
    return [KeepTogether(story)]
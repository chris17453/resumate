from reportlab.platypus.flowables import HRFlowable, KeepTogether
from reportlab.platypus import KeepTogether
from .paragraph import ParagraphD, LineDrawer, SpacerD


# Function to add references to the document
def add_references(references, styles):
    story = []
    story.append(ParagraphD("REFERENCES", styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    for reference in references:
        # Add reference name
        story.append(ParagraphD(f"{reference['name']}, {reference['relationship']}", styles['Body_Text']))

        
        # Add email
        story.append(ParagraphD(f"Email: {reference['email']}", styles['Body_Text']))

        # Add phone
        story.append(ParagraphD(f"{reference['phone']}", styles['Body_Text']))

        # Add a spacer after each reference
        story.append(SpacerD(1, 12))
    
    return [KeepTogether(story)]


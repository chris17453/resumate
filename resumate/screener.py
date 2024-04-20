from reportlab.platypus import KeepTogether
from .paragraph import ParagraphD, LineDrawer, SpacerD

# Function to add screener data to the document
def add_screener(screener, styles):
    story = []
    story.append(ParagraphD("Screener Information", styles['Heading1']))
    story.append(LineDrawer(5,styles['Heading2'].textColor))

    # Adding each item from screener data
    story.append(ParagraphD(f"Veteran: {'Yes' if screener['veteran'] else 'No'}", styles['Body_Text']))
    story.append(ParagraphD(f"Disability: {'Yes' if screener['disability'] else 'No'}", styles['Body_Text']))
    story.append(ParagraphD(f"US Citizen: {'Yes' if screener['us citizen'] else 'No'}", styles['Body_Text']))
    story.append(ParagraphD(f"Over 18: {'Yes' if screener['over 18'] else 'No'}", styles['Body_Text']))
    story.append(ParagraphD(f"Willing to Travel: {'Yes' if screener['willing to travel'] else 'No'}", styles['Body_Text']))
    story.append(SpacerD(1, 12))  # Spacing after the last item

    return [KeepTogether(story)]

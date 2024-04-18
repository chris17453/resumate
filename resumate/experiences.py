from reportlab.platypus import Paragraph, Spacer

def add_experiences(experiences, styles):
    story=[]
    for experience in experiences:
        story.extend(add_experience(experience, styles))    
    return story

def add_experience(experience, styles):

    story=[]
    story.append(Paragraph(f"<b>Role:</b> {experience['role']}", styles['Heading2']))
    story.append(Paragraph(f"Company: {experience['company']}", styles['BodyText']))
    story.append(Paragraph(f"From {experience['start']} to {experience['finished']}, Currently working: {'Yes' if experience['currently_working'] else 'No'}", styles['BodyText']))
    story.append(Paragraph(f"Feature Comment: {experience['feature_comment']}", styles['BodyText']))
    # Successes
    successes = ', '.join(experience['successes'])
    story.append(Paragraph(f"Successes: {successes}", styles['Heading2']))
    story.append(Spacer(1, 12))
    return story
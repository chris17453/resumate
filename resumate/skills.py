from reportlab.platypus import Paragraph, Spacer


def add_skills(skills, styles):
    story=[]
    for skill in skills:
        story.append(Paragraph(f"<b>{skill['category']} Skills:</b> {', '.join(skill['skills'])}", styles['BodyText']))
        story.append(Spacer(1, 12)) 
    return story

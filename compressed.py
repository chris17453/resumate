|-- /
|   |-- footer.py
|   |-- generator.py
|   |-- styles.py
|   |-- experiences.py
|   |-- pdf_metadata.py
|   |-- pdf.py
|   |-- header.py
|   |-- io.py
|   |-- __init__.py
|   |-- cli.py
|   |-- skills.py

Path: resumeonator/footer.py
File: footer.py
-------
from reportlab.platypus import Paragraph

def add_footer(resume_data, styles, total_pages):
    page_number=1
    footer_text = f"Page {page_number} of {total_pages}"
    footer_paragraph = Paragraph(footer_text, styles['Heading2'])
    story=[]
    story.append(footer_paragraph)
    return story
Path: resumeonator/generator.py
File: generator.py
-------

import yaml
from faker import Faker
import random

fake = Faker()

def generate_skills(category):
    skills = {
        'Technical': ['Python', 'Java', 'C++', 'JavaScript', 'SQL', 'AWS', 'Docker', 'Kubernetes', 'Machine Learning'],
        'Management': ['Project Management', 'Leadership', 'Budgeting', 'Strategic Planning', 'Agile Methodologies'],
        'Communication': ['Public Speaking', 'Negotiation', 'Persuasion', 'Interpersonal Communication', 'Writing'],
        'Analytical': ['Data Analysis', 'Critical Thinking', 'Problem Solving', 'Research', 'Statistics']
    }
    return {
        'category': category,
        'skills': random.sample(skills[category], k=random.randint(2, 5))
    }

def generate_position():
    positions = ['Software Engineer', 'Data Analyst', 'Project Manager', 'Marketing Specialist', 'Financial Analyst']
    return random.choice(positions)

def generate_experience():
    return {
        'role': fake.job(),
        'company': fake.company(),
        'start': fake.date_between(start_date='-10y', end_date='-2y').isoformat(),
        'finished': fake.date_between(start_date='-2y', end_date='today').isoformat(),
        'currently_working': fake.boolean(chance_of_getting_true=25),
        'feature_comment': fake.paragraph(nb_sentences=2),
        'successes': [fake.sentence() for _ in range(random.randint(2, 5))],
        'skills_used': [generate_skills(random.choice(['Technical', 'Management', 'Communication', 'Analytical']))
                        for _ in range(random.randint(1, 4))]
    }


def generate_links():
    return [
        {
            'type': 'GitHub',
            'url': 'github.com/' + fake.user_name(),
            'name': 'github',
            'order': random.randint(1, 5)
        },
        {
            'type': 'LinkedIn',
            'url': 'linkedin.com/in/' + fake.user_name(),
            'name': 'linkedin',
            'order': random.randint(1, 5)
        }
    ]
def generate_resume_data(num_experiences):
    return {
        'main_data': {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'position':generate_position(),
            'links': generate_links(),
            'picture': 'Path_to_picture.jpg'
        },
        'experiences': [generate_experience() for _ in range(num_experiences)],
        'skills': [generate_skills(category) for category in ['Technical', 'Management', 'Communication', 'Analytical']],
        'cover_page': fake.boolean(),
        'theme': {
            'color_scheme': {
                'background': fake.hex_color(),
                'foreground': fake.hex_color()
            }
        }
    }

def generated_resume(filename, num_experiences):
    resume_data = generate_resume_data(num_experiences)
    with open(filename, 'w') as file:
        yaml.safe_dump(resume_data, file, default_flow_style=False)
    print(f"Generated resume data saved to '{filename}'.")

Path: resumeonator/styles.py
File: styles.py
-------
import yaml
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.colors import HexColor

# Mapping for text alignment to be used in style conversion
alignment_mapping = {
    'TA_LEFT': TA_LEFT,
    'TA_CENTER': TA_CENTER,
    'TA_RIGHT': TA_RIGHT,
    'TA_JUSTIFY': TA_JUSTIFY
}
def create_styles(style_data):
    default_styles = getSampleStyleSheet()  # This gets the default styles
    custom_styles = {}

    for style_name, style_attrs in style_data.items():
        # If there's a parent style specified, try to find it in custom styles first
        if 'parent' in style_attrs:
            parent_style_name = style_attrs.pop('parent')  # Remove the parent from attrs
            parent_style = custom_styles.get(parent_style_name)
            if parent_style is None:
                parent_style = default_styles.get(parent_style_name)
            if parent_style is None:
                raise ValueError(f"Parent style '{parent_style_name}' not found in stylesheet")
        else:
            parent_style = None

        # Convert alignment value to ReportLab enum
        if 'alignment' in style_attrs:
            alignment = style_attrs['alignment'].upper()
            if alignment in alignment_mapping:
                style_attrs['alignment'] = alignment_mapping[alignment]
            else:
                raise ValueError(f"Invalid alignment value '{alignment}'")

        # Create the custom style, ensuring that 'parent' is an actual ParagraphStyle object
        custom_styles[style_name] = ParagraphStyle(name=style_name, parent=parent_style, **style_attrs)

    return custom_stylesPath: resumeonator/experiences.py
File: experiences.py
-------
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
    return storyPath: resumeonator/pdf_metadata.py
File: pdf_metadata.py
-------
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Frame,PageTemplate
from reportlab.lib.units import inch

import yaml

class frame_def:
    def __init__(self, id, left, top, width, height):
        self.id = id
        self._left = left
        self._top = top
        self._width = width
        self._height = height

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


def load_resume_from_yaml(yaml_file):
    """
    Load resume data from a YAML file.
    """
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)
    
def load_page_template_metadata(metadata_file):
    """
    Load page template metadata from a YAML file.
    """
    with open(metadata_file, 'r') as file:
        metadata = yaml.safe_load(file)
    return metadata.get('page_template', {})



def create_page_template(metadata):
    frames = []
    frames_dict = {}

    for frame_data in metadata.get('frames', []):
        x1=_eval_with_units(frame_data.get('left', '0'), frames_dict)
        y1=_eval_with_units(frame_data.get('top', '0'), frames_dict)
        width=_eval_with_units(frame_data.get('width', '0'), frames_dict)
        height=_eval_with_units(frame_data.get('height', '0'), frames_dict)
        frame_id=frame_data.get('id', '')
        frames_dict[frame_id] =frame_def(frame_id,x1,y1,width,height)
        frame = Frame(
            x1,
            y1,
            width,
            height,
            id=frame_id
        )
        frames.append(frame)
        #print (f"{x1},{y1},{width},{height},{frame_id}")


         

    page_template = PageTemplate(id='default', frames=frames,pagesize=letter,)
    return page_template

def _eval_with_units(expression, frames):
    # Define units and dimensions
    page_width, page_height = letter

    # Create a local dictionary to include frames and global measurements
    frames['inch']= inch
    frames['page_width']= page_width
    frames['page_height']= page_height
    
    expression=expression.replace("inch","*inch")
    # Evaluate the expression using local and global scope
    result = eval(expression, {}, frames)
    #print (expression,":",result)
    return result

Path: resumeonator/pdf.py
File: pdf.py
-------
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate,FrameBreak

from .styles import create_styles
from .pdf_metadata import load_page_template_metadata, create_page_template
from .header import add_header
from .footer import  add_footer
from .experiences import add_experiences
from .skills import add_skills




def generate_pdf(resume_data, pdf_file, metadata_file):
    """
    Generate a PDF file from resume data using the specified page template metadata.
    """
    # Load page template metadata
    metadata = load_page_template_metadata(metadata_file)
    styles=create_styles(metadata['styles'])
    # Create page template
    page_template = create_page_template(metadata)

    margin=0
    # Create PDF document with page template
    doc = BaseDocTemplate(pdf_file, 
                          pagesize=letter,
                          rightMargin=margin, leftMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                        showBoundary=1,

                          )
    
    doc.addPageTemplates(page_template)  

    header=add_header(resume_data, styles) 
    exp=add_experiences(resume_data['experiences'],styles)
    skill=add_skills( resume_data['skills'], styles)
    footer=add_footer(resume_data, styles,total_pages=1)
    # Ensure header and footer stay with subsequent content
    header[-1].keepWithNext = True
    footer[-1].keepWithNext = True
    elements=header +[FrameBreak()]+footer+[FrameBreak()]+exp+[FrameBreak()]+skill
    
    doc.build(elements)
Path: resumeonator/header.py
File: header.py
-------
from reportlab.platypus import Paragraph

def add_header(resume_data, styles):
    story=[]
    story.append(Paragraph(f"<b>Name:</b> {resume_data['main_data']['name']}", styles['Title']))
    story.append(Paragraph(f"<b>Address:</b> {resume_data['main_data']['address']}", styles['BodyText']))
    story.append(Paragraph(f"<b>Phone:</b> {resume_data['main_data']['phone']}", styles['BodyText']))
    story.append(Paragraph(f"<b>Email:</b> {resume_data['main_data']['email']}", styles['BodyText']))
    #if 'picture' in resume_data['main_data'] and resume_data['main_data']['picture']:
    #    try:
    #        story.append(Image(resume_data['main_data']['picture'], width=100, height=100))
    #        story.append(Spacer(1, 12))
    #    except Exception as e:
    #        story.append(Paragraph(f"Failed to load image: {e}", styles['BodyText']))
    #       story.append(Spacer(1, 12))
    return story
Path: resumeonator/io.py
File: io.py
-------
import yaml

def create_resume_template(yaml_file):
    """
    Create a template YAML file for a resume with structured sections.

    :param yaml_file: Path to the YAML file where the template will be saved.
    """
    resume_template = {
        'main_data': {
            'name': 'Your Name',
            'address': 'Your Address',
            'phone': 'Your Phone Number',
            'email': 'Your Email',
            'position': 'The position you\'re applying for',
            'links': [
                {
                    'type': 'GitHub',
                    'url': 'github.com/stuff',
                    'name': 'github',
                    'order':  2
              },{
                        'type': 'LinkedIn',
                    'url': 'linkedin.com/u/user',
                    'name': 'github',
                    'order': 1 ,
              
              }

            ],

            'picture': 'Path to your picture'
        },


        'experiences': [
            {
                'role': 'Your Role',
                'company': 'Company Name',
                'start': 'Start Date',
                'finished': 'End Date',
                'currently_working': False,
                'feature_comment': 'Key Achievement or Comment',
                'successes': [
                    'Success 1',
                    'Success 2'
                ],
                'skills_used': [
                    {
                        'category': 'Technical',
                        'skills': ['Skill 1', 'Skill 2']
                    }
                ]
            }
        ],
        'skills': [
            {
                'category': 'Technical',
                'skills_list': ['Skill 1', 'Skill 2']
            },
            {
                'category': 'Management',
                'skills_list': ['Skill 1', 'Skill 2']
            }
        ],
        'cover_page': True,
        'theme': {
            'color_scheme': {
                'background': 'Color Code',
                'foreground': 'Color Code'
            }
        }
    }

    with open(yaml_file, 'w') as file:
        yaml.safe_dump(resume_template, file, default_flow_style=False)

def load_resume_from_yaml(yaml_file):
    """
    Load resume data from a YAML file.

    :param yaml_file: Path to the YAML file containing resume data.
    :return: A dictionary containing the loaded resume data.
    """
    with open(yaml_file, 'r') as file:
        resume_data = yaml.safe_load(file)
    return resume_data

def save_resume_to_yaml(resume_data, yaml_file):
    """
    Save resume data to a YAML file.

    :param resume_data: A dictionary containing the resume data.
    :param yaml_file: Path to the YAML file where the data will be saved.
    """
    with open(yaml_file, 'w') as file:
        yaml.safe_dump(resume_data, file, default_flow_style=False)

Path: resumeonator/__init__.py
File: __init__.py
-------
Path: resumeonator/cli.py
File: cli.py
-------
import os
import argparse
from .io import load_resume_from_yaml,save_resume_to_yaml,create_resume_template
from .pdf import generate_pdf
from .generator import generated_resume



def main():
    parser = argparse.ArgumentParser(description="Resume YAML File Management")
    parser.add_argument('action', choices=['template', 'load', 'save', 'generate_pdf', 'generate_fake','extract'], help="Action to perform: create a new template, load data, save data, generate PDF, or generate fake resume data, extract pdf data")
    parser.add_argument('file', help="Path to the YAML file")
    parser.add_argument('dir', nargs='?', default=None, help="Directory to store resume files")

    args = parser.parse_args()
    
    if args.dir==None:
        args.dir=os.path.dirname(args.file)
        
    if os.path.exists(args.dir):
        print("Error: Directory already exists.")

    else: 
        os.makedirs(args.dir)

    if args.action == 'template':
        create_resume_template(args.file)
        print(f"Created a new resume template at {args.file}")
    elif args.action == 'load':
        data = load_resume_from_yaml(args.file)
        print(f"Loaded resume data from {args.file}:\n{data}")
    elif args.action == 'save':
        data = load_resume_from_yaml(args.file)
        save_resume_to_yaml(data, args.file)
        print(f"Saved updated resume data to {args.file}")
    elif args.action == 'generate_fake':
        generated_resume(args.file, 5)  # Generate fake resume data with 5 experiences
        print(f"Generated fake resume data saved to {args.file}")
    elif args.action == 'generate_pdf':
        data = load_resume_from_yaml(args.file)
        pdf_file = args.file.replace('.yaml', '.pdf')  # Assuming the output PDF file will have the same name as the YAML file
        generate_pdf(data, pdf_file,"template/resume-1.yaml")
        print(f"PDF generated: {pdf_file}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
Path: resumeonator/skills.py
File: skills.py
-------
from reportlab.platypus import Paragraph, Spacer


def add_skills(skills, styles):
    story=[]
    for skill in skills:
        story.append(Paragraph(f"<b>{skill['category']} Skills:</b> {', '.join(skill['skills'])}", styles['BodyText']))
        story.append(Spacer(1, 12)) 
    return story

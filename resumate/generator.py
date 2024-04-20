
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
def generate_resume_data(num_experiences,num_achievements=5,num_strengths=1,num_passions=2):
    return {
        'main_data': {
            'name': fake.name(),
            'address': fake.address(),
            'location': fake.city()+", "+fake.state(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'position':generate_position(),
            'links': generate_links(),
            'picture': 'assets/avatar.png'
        },
        'summary': fake.paragraph(nb_sentences=5),
        'cover_page': fake.paragraph(nb_sentences=15),
        'education': {
           'school': fake.company() + " School",
           'course':  fake.catch_phrase() + " Course",
           'from':fake.date(),
           'to':fake.date(),
        },

        'certificates': {
           'school': fake.company() + " School",
           'course':  fake.catch_phrase() + " Course",
           'date':fake.date(),
        },
        'strengths':  [fake.paragraph(nb_sentences=3) for _ in range(num_strengths)],
        'passions': [fake.paragraph(nb_sentences=3) for _ in range(num_passions)],
        'experiences': [generate_experience() for _ in range(num_experiences)],
        'achievements': [fake.paragraph(nb_sentences=3) for _ in range(num_achievements)],
        'skills': [generate_skills(category) for category in ['Technical', 'Management', 'Communication', 'Analytical']],
          'cover_page': fake.boolean()
    }
     

def generated_resume(filename, num_experiences):
    resume_data = generate_resume_data(num_experiences)
    with open(filename, 'w') as file:
        yaml.safe_dump(resume_data, file, default_flow_style=False)
    print(f"Generated resume data saved to '{filename}'.")


import os
import argparse
from .io import load_resume_from_yaml,save_resume_to_yaml,create_resume_template
from .pdf import generate_pdf
from .generator import generated_resume
from .template import template



def main():
    parser = argparse.ArgumentParser(description="Resume YAML File Management")
    parser.add_argument('action', choices=['template', 'load', 'save', 'generate_pdf', 'generate_fake','extract','new_style'], help="Action to perform: create a new template, load data, save data, generate PDF, or generate fake resume data, extract pdf data, amke a new pdf template")
    parser.add_argument('file', help="Path to the YAML file")
    parser.add_argument('dir', nargs='?', default=None, help="Directory to store resume files")

    args = parser.parse_args()
    
    if args.dir==None:
        args.dir=os.path.dirname(args.file)
        
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    if args.action == 'new_style':
        t=template(args.file)
        t.build()
        t.save()
        print(f"Created a new template style at {args.file}")
    elif args.action == 'template':
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
        generated_resume(args.file, 10)  # Generate fake resume data with 5 experiences
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

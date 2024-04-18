from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate,FrameBreak,NextPageTemplate,KeepTogether

from .styles import create_styles
from .pdf_metadata import load_page_template_metadata, create_page_template
from .experiences import add_experiences
from .skills import add_skills


# Define a function to draw headers if needed
def on_page(canvas, doc):
    # Draw header by creating a temporary frame to contain the header content
    header_frame = Frame(doc.leftMargin, doc.height - inch, doc.width, 0.5 * inch)
    header_frame.add(header_content, canvas)
    canvas.restoreState()


def generate_pdf(resume_data, pdf_file, metadata_file):
    """
    Generate a PDF file from resume data using the specified page template metadata.
    """
    # Load page template metadata
    metadata = load_page_template_metadata(metadata_file)
    metadata['resume']=resume_data
    # Create page template
    frame_dict,page_template,styles = create_page_template(metadata)
    

    margin=0
    # Create PDF document with page template
    doc = BaseDocTemplate(pdf_file, 
                          pagesize=letter,
                          rightMargin=margin, leftMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                          showBoundary=1,
                          )
    
    doc.addPageTemplates(page_template)  

    
    #header=add_header(resume_data, styles) 
    #footer=add_footer(resume_data, styles,total_pages=1)
    exp=add_experiences(resume_data['experiences'],styles)
    skill=add_skills( resume_data['skills'], styles)
    
    flowables=[]
    flowables.append(NextPageTemplate('wide_column'))
    flowables.append(KeepTogether() )
    flowables.extend(exp)
    #flowables.append(FrameBreak())
    flowables.append(NextPageTemplate('small_column'))
    flowables.extend(skill)
    
    
#[NextPageTemplate('header')]+ header +[FrameBreak()]+ \
#             [NextPageTemplate('footer')]+ footer+[FrameBreak()]+\
             
    
    
    doc.build(flowables)

import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate,FrameBreak,PageBreak


from .styles import create_styles
from .pdf_metadata import load_page_template_metadata, create_page_template, create_combined_template, calculate_objects
from .experiences import add_experiences
from .skills import add_skills


from .paragraph import rendered_details
from .summary import add_summary
from .education import add_education
from .achievements import add_achievements
from .strengths import add_strengths
from .passions import add_passions
from .screener import add_screener
from .references import add_references

def generate_pdf(resume_data, pdf_file, metadata_file):
    """
    Generate a PDF file from resume data using the specified page template metadata.
    """
    global rendered_details
    # Load page template metadata
    metadata = load_page_template_metadata(metadata_file)
    metadata['resume']=resume_data
    # Create page template
    metadata['objects'] =calculate_objects(metadata)
    frame_dict,page_template,styles = create_page_template(metadata)
    buffer1 = io.BytesIO()
    buffer2 = io.BytesIO()


    margin=0
    # Create PDF document with page template
    doc1 = BaseDocTemplate(buffer1, 
                          pagesize=letter,
                          rightMargin=margin, leftMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                          showBoundary=False,
                          )
    ## Create PDF document with page template
    doc2 = BaseDocTemplate(buffer2, 
                          pagesize=letter,
                          rightMargin=margin, leftMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                          showBoundary=False,
                          )
    
#
    doc1.addPageTemplates(page_template[0])  
    doc2.addPageTemplates(page_template[1])  

    summary=add_summary(resume_data['summary'],styles)

    exp=add_experiences(resume_data['experiences'],styles)
    edu=add_education(resume_data['education'],styles)
    references=add_references(resume_data['references'],styles)

    flowables=summary+exp+edu+references


    doc1.build(flowables)


    pages=[]
    if len(rendered_details)>0:
        page={}
        column=[]
        previous_y=rendered_details[0]['y']
        for item in rendered_details:
            if item['y']>previous_y:
                page['wide']=column
                pages.append(page)
                column=[]
                page={}
            previous_y=item['y']
            column.append(item['flowable'])
        if len(column)>0:
            page['wide']=column
            pages.append(page)


    buffer1.close()
    # Next Column
    # dont reasign.. funky stuff
    rendered_details.clear()
    screener=add_screener(resume_data['screener'],styles)
    achievements=add_achievements( resume_data['achievements'], styles)
    skill=add_skills( resume_data['skills'], styles)
    passions=add_passions( resume_data['passions'], styles)
    strengths=add_strengths( resume_data['strengths'], styles)
    flowables=screener+strengths+achievements+skill+passions
    #print(skill)
    doc2.build(flowables)

    pages2=[]
    if len(rendered_details)>0:
        page={}
        column=[]
        previous_y=rendered_details[0]['y']
        
        for item in rendered_details:
            if item['y']>previous_y:
                page['small']=column
                pages2.append(page)
                column=[]
                page={}
            previous_y=item['y']
            column.append(item['flowable'])
        if len(column)>0:
            page['small']=column
            pages2.append(page)

    buffer2.close()
    
    merged_pages = []
    max_length = max(len(pages), len(pages2))

    for i in range(max_length):
        wide_content = pages[i]['wide'] if i < len(pages) else []
        small_content = pages2[i]['small'] if i < len(pages2) else []
        merged_pages.append({'wide': wide_content, 'small': small_content})

    # build the pdf
    metadata['pages']=len(merged_pages)
    pdf_build(pdf_file,margin,merged_pages,metadata)    

    
def pdf_build(pdf_file,margin,merged_pages,metadata):
        # Create PDF document with page template
    doc3 = BaseDocTemplate(pdf_file, 
                          pagesize=letter,
                          rightMargin=margin, leftMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                          showBoundary=False,
                          )


    elements=[]

    for page in merged_pages:
        for item in page['wide']:
            elements.append(item)

        elements.append(FrameBreak)
        for item in page['small']:
            elements.append(item)
        
        elements.append(PageBreak())
    
    page_template=create_combined_template(metadata)
    doc3.addPageTemplates(page_template)  

    doc3.build(elements)            

    

    





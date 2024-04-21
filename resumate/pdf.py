import yaml
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate,FrameBreak,PageBreak


from .pdf_metadata import load_page_template_metadata, create_page_template, create_combined_template, calculate_objects
# from .experiences import add_experiences
#from .old.skills import add_skills
from .paragraph import rendered_details
# from .summary import add_summary
# from .education import add_education
# from .achievements import add_achievements
# from .strengths import add_strengths
# from .passions import add_passions
# from .screener import add_screener
# from .references import add_references
# from .certificates import add_certificates
from .section import add_section

def generate_pdf_old(resume_data, pdf_file, metadata_file):
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
    certificates=add_certificates(resume_data['certificates'],styles)
    flowables=summary+exp+edu+certificates+references


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
    doc = BaseDocTemplate(pdf_file, 
                          pagesize=letter,
                          rightMargin=margin, leftMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                          showBoundary=False,
                          )
    elements=[]
    page_index=0
    page_length=len(merged_pages)
    for page in merged_pages:
        for column in page:
            for item in page[column]:
                elements.append(item)
            elements.append(FrameBreak)
        page_index+=1
        # WTF why did this change? used to need it .. now it doesnt?
        #if page_index<page_length: elements.append(PageBreak())
        
    page_template=create_combined_template(metadata)
    doc.addPageTemplates(page_template)  

    doc.build(elements)            

    

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

    # pre data inception wonder stuff
    
    margin=0
   
      
    column_index=0
    all_pages={}
    for column_name in sorted(metadata['template']['columns'], key=lambda x: metadata['template']['columns'][x]['order']):
        rendered_details.clear()
        all_pages[column_name] = []
        flowables = []
        # Create PDF document with page template
        # user memory so we dont waste disk IO
        buffer = io.BytesIO()
        doc = BaseDocTemplate(buffer, 
                        pagesize=letter,
                        rightMargin=margin, leftMargin=margin,
                        topMargin=margin, bottomMargin=margin,
                        showBoundary=False,
                        )
        doc.addPageTemplates(page_template[column_index])  
        column_index += 1

        base = metadata['template']['global']
        column = metadata['template']['columns'][column_name]
            
        for section_name in sorted(column['sections'], key=lambda x: column['sections'][x]['order']):
            section = column['sections'][section_name]
            section['name'] = section_name
            data = {section_name: metadata['resume'][section_name]}
            #print(data)
            flowables.extend(add_section(base, section, data, styles))


        # this builds what we just build dynamicaly.. 
        # but ONLY per column...
        #print(flowables)
        doc.build(flowables)
        buffer.close()
        
    
        ## everything in this column has been rendered.. 
        ## lets grab the elements and drop them into an array with pagination
        if len(rendered_details)>0:
            column=[]
            previous_y=rendered_details[0]['y']
            for item in rendered_details:
                if item['y']>previous_y:
                    all_pages[column_name].append(column)
                    column=[]
                previous_y=item['y']
                column.append(item['flowable'])

            if len(column)>0:
                all_pages[column_name].append(column)

    ## ok all columns have been rendered... lets merge the pages

    # Merge all pages
    merged_pages = []
    max_length = max(len(all_pages[columns]) for columns in all_pages)
 
    for i in range(max_length):
        page={}
        for column_name in all_pages:
            column=all_pages[column_name]
            page[column_name]=column[i] if i < len(column) else []
        merged_pages.append(page)
 
   
    # build the pdf
    metadata['pages']=len(merged_pages)
    pdf_build(pdf_file,margin,merged_pages,metadata)    


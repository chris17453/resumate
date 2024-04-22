
import yaml

import pprint

def load_template(template_file):
    """
    Load page template metadata from a YAML file.
    """
    with open(template_file, 'r') as file:
        metadata = yaml.safe_load(file)
    return metadata.get('page_template', {})

def save_template(template_file,metadata):
    with open(template_file, 'w') as file:
        yaml.dump({'page_template': metadata}, file)

class frame:
    def __init__(self, frame_id, left, top, width, height):
        self.id = frame_id
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class shape:
    def __init__(self, shape_id, shape_type, left, top, width, height, background_color):
        self.id = shape_id
        self.type = shape_type
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.background_color = background_color

class picture:
    def __init__(self, picture_id, left, top, max_width, max_height, mask, background_color):
        self.id = picture_id
        self.left = left
        self.top = top
        self.max_width = max_width
        self.max_height = max_height
        self.mask = mask
        self.background_color = background_color

class global_settings:
    def __init__(self, bold, upper):
        self.bold = bold
        self.upper = upper

class column:
    def __init__(self, name, keep_together, column_type):
        self.name = name
        self.keep_together = keep_together
        self.column_type = column_type
        self.data = []
        self.format = []

class template:
  def generate_template(self, template_file):
        header_frame = frame('header', '0.25 inch', 'page_height-1.5 inch-.25 inch', 'page_width - .5 inch', '1.5 inch')
        footer_frame = frame('footer', '.25 inch', '.25 inch', 'page_width - .5 inch', '.5 inch')
        wide_column_frame = frame('wide_column', '.25 inch', 'footer.height+footer.top+.25 inch', '(page_width - .75 inch) * 0.66', 'page_height-header.height-footer.height -1 inch')
        small_column_frame = frame('small_column', 'wide_column.left+wide_column.width +0.25 inch', 'footer.height+footer.top+.25 inch', 'page_width - wide_column.width -.75 inch', 'page_height-header.height-footer.height -1 inch')

        header_bg_rect = shape('header_bg_rect', 'rect', 0, 'page_height-2 inch', 'page_width', '2 inch', '#004455')
        edge_color_rect = shape('edge_color_rect', 'rect', 0, 0, '.125 inch', 'page_height', '#EE0000')
        header_bg_circle = shape('header_bg_circle', 'circle', 'page_width - 1.5 inch', 'page_height-1 inch', '.75 inch', '.75 inch', '#222222')

        picture = picture('picture', 'header.left+header.width-1.95 inch', 'header.top + .10 inch', '1.4 inch', '1.4 inch', 'circle', '#000000')

        global_settings = global_settings(True, True)

        self.metadata['frames'] = [header_frame, footer_frame, wide_column_frame, small_column_frame]
        self.metadata['shapes'] = [header_bg_rect, edge_color_rect, header_bg_circle]
        self.metadata['picture'] = picture
        self.metadata['global'] = global_settings

        # Remaining metadata and column def        



def generate_template(template_file):
    #metadata=load_template(template_file)
    metadata={}
    column_wide={}
    column_small={}
    metadata['frames']=[{'id': 'header', 'left': '0.25 inch', 'top': 'page_height-1.5 inch-.25 inch', 'width': 'page_width - .5 inch', 'height': '1.5 inch'}, 
            {'id': 'footer', 'left': '.25 inch', 'top': '.25 inch', 'width': 'page_width - .5 inch', 'height': '.5 inch'}, 
            {'id': 'wide_column', 'left': '.25 inch', 'top': 'footer.height+footer.top+.25 inch', 'width': '(page_width - .75 inch) * 0.66', 'height': 'page_height-header.height-footer.height -1 inch'}, 
            {'id': 'small_column', 'left': 'wide_column.left+wide_column.width +0.25 inch', 'top': 'footer.height+footer.top+.25 inch', 'width': 'page_width - wide_column.width -.75 inch', 'height': 'page_height-header.height-footer.height -1 inch'}]
    
    metadata['shapes']=[{'id': 'header_bg_rect', 'type': 'rect', 'left': 0, 'top': 'page_height-2 inch', 'width': 'page_width', 'height': '2 inch', 'background-color': '#004455'}, 
            {'id': 'edge_color_rect', 'type': 'rect', 'left': 0, 'top': 0, 'width': '.125 inch', 'height': 'page_height', 'background-color': '#EE0000'}, 
            {'id': 'header_bg_circle', 'type': 'circle', 'left': 'page_width - 1.5 inch', 'top': 'page_height-1 inch', 'diameter': '.75 inch', 'background-color': '#222222'}]
    metadata['picture']= {'id': 'picture', 'left': 'header.left+header.width-1.95 inch', 'top': 'header.top + .10 inch', 'max_width': '1.4 inch', 'max_height': '1.4 inch', 'mask': 'circle', 'background-color': '#000000'}
    
    column_wide['summary']={'order':1,'keep_together': True, 'type': 'text', 'data': 'text', 
                            'format': [
                                {'data': 'text', 'type': 'string', 'style': 'Heading2'},
                                {'data': ['cplusplus','csharp','python','ansible','terraform','aws'], 'type': 'svgrow', 'style': 'Heading2','svg_size':'.25 inch'},
                                ]}
    column_wide['experiences'] = {'order':2,'keep_together': False, 'type': 'array', 'data': ['role', 'company', 'start', 'end', 'curently_working', 'feature_comment', 'success', 'skills_used'], 
                                  'format': [{'data': 'role', 'type': 'string', 'style': 'Heading2'}, 
                                             {'data': '{start:%b %Y} - {end:%b %Y}', 'type': 'format', 'style': 'Heading2_Right'}, 
                                             {'data': 'company', 'type': 'string', 'style': 'Heading2'}, 
                                             {'data': 'feature_comment', 'type': 'string', 'style': 'Text'}, 
                                             {'data': 'success', 'type': 'list', 'style': 'List'}, 
                                             {'data': 'skills_used', 'type': 'table', 'style': 'Table'},
                                             {'data': 15, 'type': 'spacer', 'style': ''}
                                             
                                             ]}
    column_wide['education'] = {'order':3,'keep_together': True, 'type': 'array', 'data': [{'school': ['school', 'course', 'start', 'end']}], 
                                'format': [
                                    {'data': 'school', 'type': 'string', 'style': 'Heading2'}, 
                                    {'data': '{start:%b %Y} - {end:%b %Y}', 'type': 'format', 'style': 'Heading2_Right'},

                                    {'data': 'course', 'type': 'string', 'style': 'Heading2'}, 
                                    ]}
    

    column_wide['certificates'] = {'order':4,'keep_together': True, 'type': 'array', 'data': ['name', 'date'], 'format': [ {'data': '{date:%b %Y}', 'type': 'format', 'style': 'Heading2_Right'},{'data': 'name', 'type': 'string', 'style': 'Heading2'}]}
    column_wide['references']= {'order':5,'keep_together': True, 'type': 'array', 'data': [{'reference': ['name', 'phone', 'email', 'relationship']}], 'format': [{'data': '{name},{relationship}', 'type': 'format', 'style': 'Heading2'}, {'data': 'phone', 'type': 'string', 'style': 'Text'}, {'data': 'email', 'type': 'string', 'style': 'Text'}]}
    column_small['screener']= {'order':1,'keep_together': True, 'type': 'object', 'data': ['veteran', 'disability', 'us_citizen', 'over_18', 'willing_to_travel', 'remote', 'hybrid', 'office', 'start_date'], 'format': [{'data': 'Veteran: {veteran} ', 'type': 'format', 'style': 'Text'}, {'data': 'Disabled: {disability} ', 'type': 'format', 'style': 'Text'}, {'data': 'US Citizen: {us_citizen}', 'type': 'format', 'style': 'Text'}, {'data': 'Over 18: {over_18}', 'type': 'format', 'style': 'Text'}, {'data': 'Travel: {willing_to_travel}', 'type': 'format', 'style': 'Text'}, {'data': 'Remote: {remote}', 'type': 'format', 'style': 'Text'}, {'data': 'Hybrid: {hybrid}', 'type': 'format', 'style': 'Text'}, {'data': 'Office: {office}', 'type': 'format', 'style': 'Text'}, {'data': 'Start Date: {start_date}', 'type': 'format', 'style': 'Text'}]}
    column_small['strengths']= {'order':2,'keep_together': True, 'type': 'array', 'data': ['strengths'], 'format': [{'data': 'strengths', 'type': 'list', 'style': 'Text'}]}
    column_small['achievements']= {'order':3,'keep_together': True, 'type': 'array', 'data': ['achievements'], 'format': [{'data': 'achievements', 'type': 'list', 'style': 'Text'}]}
    column_small['skills'] ={'order':4,'keep_together': True, 'type': 'array', 'data': ['skills'], 'format': [{'data': 'skills', 'type': 'list', 'style': 'Text'}]}
    column_small['passions'] ={'order':5,'keep_together': True, 'type': 'array', 'data': ['passions'], 'format': [{'data': 'passions', 'type': 'list', 'style': 'Text'} ]}
    

    metadata['template']=   {
        'global':{'heading': {'bold': True, 'upper': True}, 'list': {'bullet_style': '-'}},
        'header':{'name': 'header', 'frame': 'header', 'type': 'text', 'data': ['name', 'address', 'location', 'phone', 'email', 'position', 'github', 'linkedin', 'picture'], 'format': [{'data': 'name', 'type': 'string', 'style': 'Heading1'}, {'data': 'position', 'type': 'string', 'style': 'Heading2'}, {'data': 'email', 'type': 'string', 'style': 'Text'}, {'data': 'phone', 'type': 'string', 'style': 'Text'},                                    {'data': 'location', 'type': 'string', 'style': 'Text'}, {'data': 'GitHub: {github}', 'type': 'format', 'style': 'Text'}, {'data': 'Linkedin: {linkedin}', 'type': 'format', 'style': 'Text'}]} ,
        'footer':{'name': 'footer', 'frame': 'footer', 'type': 'text', 'data': ['page', 'page_total'], 'format': [{'data': 'Page {page} of {page_total}', 'type': 'format', 'style': 'Text'}]},
        'columns':{  
                                'wide':{'sections':column_wide,'order':1},
                                'small':{'sections':column_small,'order':2}
                                } 
                            }
    metadata['styles']=generate_stylesheet(metadata)
    
    save_template(template_file,metadata)


def generate_stylesheet(data):
    theme={  
        'text_light':'#222222', 
        'text_dark':'#FFFFFF', 
        'bg_light':'#FFFFFF', 
        'bg_dark':'#222222'
        }
    footer_dark=False
    header_dark=True
    even_column_dark=False
    odd_column_dark=False
    
    style_sheet={}
    column_index=0
    for column in data['template']['columns']:
        dark = even_column_dark if column_index % 2 == 0 else odd_column_dark
        for section in data['template']['columns'][column]['sections']:
            style(section,"Heading1",style_sheet,theme,dark)
            section_obj=data['template']['columns'][column]['sections'][section]
            for item in section_obj['format']:
                style(section,item['style'],style_sheet,theme,dark)
    column_index+=1
    
    section='header'
    style(section,"Heading1",style_sheet,theme,header_dark)
    for item in data['template']['header']['format']:
        style(section,item['style'],style_sheet,theme,header_dark)

    section='footer'
    style(section,"Heading1",style_sheet,theme,footer_dark)
    for item in data['template']['footer']['format']:
        style(section,item['style'],style_sheet,theme,footer_dark)

    return style_sheet
    


def style(section, style_type, style_sheet, theme, dark=False):
    base_template = {
        'fontName': 'Helvetica',
        'fontSize': 12,
        'leading': 14 ,
        'textColor': theme['text_dark'] if dark else theme['text_light'],
        'alignment': 'TA_LEFT',
        'leftIndent': 0,
        'firstLineIndent': 0,
        'spaceAfter': 4,
        'bgColor': theme['bg_dark'] if dark else theme['bg_light']
    }

    heading_templates = {
        'Heading1': {'fontSize': 13,'leading': 13, 'spaceAfter': 5,'bold': True, 'upper': True},
        'Heading2': {'fontSize': 10,'leading': 10, 'spaceAfter': 3,'bold': True, 'upper': True},
        'Heading3': {'fontSize': 10,'leading': 10, 'spaceAfter': 3,'bold': False, 'upper': True},
        'Heading1_Right': {'fontSize': 13,'leading': 0, 'spaceAfter': 0,'bold': True , 'upper': True ,'alignment': 'TA_RIGHT'},
        'Heading2_Right': {'fontSize': 10,'leading': 0, 'spaceAfter': 0,'bold': True, 'upper': True,'alignment': 'TA_RIGHT'},
        'Heading3_Right': {'fontSize': 10,'leading': 0, 'spaceAfter': 0,'bold': False, 'upper': True,'alignment': 'TA_RIGHT'},
        'Text': {'fontSize': 10,'leading': 12,},
        'Left': {'alignment': 'TA_LEFT'},
        'Right': {'alignment': 'TA_RIGHT', 'spaceAfter': 0, 'leading': 0}
              
      
    }
    style_name = f"{section}_{style_type}"
    style_sheet[style_name] = {**base_template, **heading_templates.get(style_type, {})}






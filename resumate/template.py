
import yaml

from .shapes import shape_circle,shape_picture,shape_rectangle, frame
import pprint


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
    def __init__(self,template_file):
        self.template_file=template_file
        self.metadata={}
        self.styles={}
        self.template={}
        self.column_wide={}
        self.column_small={}
        self.footer_dark=False
        self.header_dark=True
        self.even_column_dark=False
        self.odd_column_dark=False
        
        self.theme={  
            'text_light':'#222222', 
            'text_dark':'#FFFFFF', 
            'bg_light':'#FFFFFF', 
            'bg_dark':'#222222'
            }

        self.base_template = {
            'fontName': 'Helvetica',
            'fontSize': 12,
            'leading': 14 ,
            'alignment': 'TA_LEFT',
            'leftIndent': 0,
            'firstLineIndent': 0,
            'spaceAfter': 4,
        }
        
        self.heading_templates = {
            'Title': {'fontSize': 20,'leading': 20, 'spaceAfter': 10,'bold': True, 'upper': True},
            'Heading1': {'fontSize': 13,'leading': 13, 'spaceAfter': 10,'bold': True, 'upper': True},
            'Heading2': {'fontSize': 10,'leading': 10, 'spaceAfter': 3,'bold': False, 'upper': True},
            'Heading3': {'fontSize': 10,'leading': 10, 'spaceAfter': 3,'bold': False, 'upper': True},
            'Heading1_Right': {'fontSize': 13,'leading': 0, 'spaceAfter': 0,'bold': True , 'upper': True ,'alignment': 'TA_RIGHT'},
            'Heading2_Right': {'fontSize': 10,'leading': 0, 'spaceAfter': 0,'bold': False, 'upper': True,'alignment': 'TA_RIGHT'},
            'Heading3_Right': {'fontSize': 10,'leading': 0, 'spaceAfter': 0,'bold': False, 'upper': True,'alignment': 'TA_RIGHT'},
            'Text': {'fontSize': 10,'leading': 10,},
            'Left': {'alignment': 'TA_LEFT'},
            'Right': {'alignment': 'TA_RIGHT', 'spaceAfter': 0, 'leading': 0}
                
        
        }        

    def generate_columns(self):
        self.column_wide['summary']={'order':1,'keep_together': True, 'type': 'text', 'data': 'text', 
                                'format': [
                                    {'data': 'text', 'type': 'string', 'style': 'Heading2'}
                                    ]}
        self.column_wide['experiences'] = {'order':2,'keep_together': False, 
                                    'type': 'array', 
                                    'data': ['role', 'company', 'start', 'end', 'curently_working', 'feature_comment', 'success', 'skills'], 
                                    'format': [{'data': 'role', 'type': 'string', 'style': 'Heading2'}, 
                                                {'data': '{start:%b %Y} - {end:%b %Y}', 'type': 'format', 'style': 'Heading2_Right'}, 
                                                {'data': 'company', 'type': 'string', 'style': 'Heading2'}, 
                                                {'data': 'feature_comment', 'type': 'string', 'style': 'Text'}, 
                                                {'data': 'success', 'type': 'list', 'style': 'List'}, 
                                                {'data': 'skills', 'type': 'table', 'style': 'Table'},
                                                {'data': 15, 'type': 'spacer', 'style': ''}
                                                
                                                ]}
        self.column_wide['education'] = {'order':3,'keep_together': True, 'type': 'array', 'data': [{'school': ['school', 'course', 'start', 'end']}], 
                                    'format': [
                                        {'data': 'school', 'type': 'string', 'style': 'Heading2'}, 
                                        {'data': '{start:%b %Y} - {end:%b %Y}', 'type': 'format', 'style': 'Heading2_Right'},

                                        {'data': 'course', 'type': 'string', 'style': 'Heading2'}, 
                                        ]}
        

        self.column_wide['certificates'] = {'order':4,'keep_together': True, 'type': 'array', 'data': ['name', 'date'], 'format': [ {'data': '{date:%b %Y}', 'type': 'format', 'style': 'Heading2_Right'},{'data': 'name', 'type': 'string', 'style': 'Heading2'}]}
        self.column_wide['references']= {'order':5,'keep_together': True, 'type': 'array', 'data': [{'reference': ['name', 'phone', 'email', 'relationship']}], 'format': [{'data': '{name},{relationship}', 'type': 'format', 'style': 'Heading2'}, {'data': 'phone', 'type': 'string', 'style': 'Text'}, {'data': 'email', 'type': 'string', 'style': 'Text'}]}
        self.column_small['screener']= {'order':1,'keep_together': True, 'type': 'object', 'data': ['veteran', 'disability', 'us_citizen', 'over_18', 'willing_to_travel', 'remote', 'hybrid', 'office', 'start_date'], 'format': [{'data': 'Veteran: {veteran} ', 'type': 'format', 'style': 'Text'}, {'data': 'Disabled: {disability} ', 'type': 'format', 'style': 'Text'}, {'data': 'US Citizen: {us_citizen}', 'type': 'format', 'style': 'Text'}, {'data': 'Over 18: {over_18}', 'type': 'format', 'style': 'Text'}, {'data': 'Travel: {willing_to_travel}', 'type': 'format', 'style': 'Text'}, {'data': 'Remote: {remote}', 'type': 'format', 'style': 'Text'}, {'data': 'Hybrid: {hybrid}', 'type': 'format', 'style': 'Text'}, {'data': 'Office: {office}', 'type': 'format', 'style': 'Text'}, {'data': 'Start Date: {start_date}', 'type': 'format', 'style': 'Text'}]}
        self.column_small['strengths']= {'order':2,'keep_together': True, 'type': 'array', 'data': ['strengths'], 'format': [{'data': 'strengths', 'type': 'list', 'style': 'Text'}]}
        self.column_small['achievements']= {'order':3,'keep_together': True, 'type': 'array', 'data': ['achievements'], 'format': [{'data': 'achievements', 'type': 'list', 'style': 'Text'}]}
        self.column_small['skills'] ={'order':4,'keep_together': True, 'type': 'array', 'data': ['skills'], 'format': [{'data': 'skills', 'type': 'list', 'style': 'Text'}]}
        self.column_small['passions'] ={'order':5,'keep_together': True, 'type': 'array', 'data': ['passions'], 'format': [{'data': 'passions', 'type': 'list', 'style': 'Text'} ]}
        
    def generate_template(self):
        self.template=   {
            'global':{'heading': {'bold': True, 'upper': True}, 'list': {'bullet_style': '-'}},
            'header':{'name': 'header', 'frame': 'header', 'type': 'text', 
                    'data': ['name', 'address', 'location', 'phone', 'email', 'position', 'github', 'linkedin', 'picture'], 
                    'format': [ {'data': 'name'     ,'type': 'string', 'style': 'Title'}, 
                                {'data': 'position' ,'svg':'submodules/fluentui-system-icons/assets/Trophy/SVG/ic_fluent_trophy_16_filled.svg'     ,'type': 'svg','color':'#FFFFFF', 'placement':'right','size':'.15 inch', 'style': 'Heading2'},
                                {'data': 'email'    ,'svg':'submodules/fluentui-system-icons/assets/Mail/SVG/ic_fluent_mail_16_filled.svg'         ,'type': 'svg','color':'#FFFFFF', 'placement':'right','size':'.15 inch', 'style': 'Text'}, 
                                {'data': 'phone'    ,'svg':'submodules/fluentui-system-icons/assets/Phone/SVG/ic_fluent_phone_16_filled.svg'       ,'type': 'svg','color':'#FFFFFF', 'placement':'right','size':'.15 inch', 'style': 'Text'},                                    
                                {'data': 'location', 'svg':'submodules/fluentui-system-icons/assets/Location/SVG/ic_fluent_location_16_filled.svg' ,'type': 'svg','color':'#FFFFFF', 'placement':'right','size':'.15 inch', 'style': 'Text'}, 
                                #{'data': 'GitHub: {github}', 'type': 'svg', 'placement':'right','size':'.15 inch','type': 'format', 'style': 'Text'}, 
                                #{'data': 'Linkedin: {linkedin}', 'type': 'format', 'style': 'Text'}
                                ]
                                } ,
            'footer':{'name': 'footer', 'frame': 'footer', 'type': 'text', 'data': ['page', 'page_total'], 'format': [{'data': 'Page {page} of {page_total}', 'type': 'format', 'style': 'Text'}]},
            'columns':{  
                                    'wide':{'sections':self.column_wide,'order':1},
                                    'small':{'sections':self.column_small,'order':2}
                                    } 
                                }

    def generate_stylesheet(self):

        
        column_index=0
        for column in self.template['columns']:
            dark = self.even_column_dark if column_index % 2 == 0 else self.odd_column_dark
            for section in self.template['columns'][column]['sections']:
                self.style(section,"Heading1",dark)
                section_obj=self.template['columns'][column]['sections'][section]
                for item in section_obj['format']:
                    self.style(section,item['style'],dark)
        column_index+=1
        
        section='header'
        self.style(section,"Heading1",self.header_dark)
        for item in self.template['header']['format']:
            self.style(section,item['style'],self.header_dark)

        section='footer'
        self.style(section,"Heading1",self.footer_dark)
        for item in self.template['footer']['format']:
            self.style(section,item['style'],self.footer_dark)

    def style(self,section, style_type,dark):
        template = {
            'textColor': self.theme['text_dark'] if dark else self.theme['text_light'],
            'bgColor': self.theme['bg_dark'] if dark else self.theme['bg_light']
        }
   
        style_name = f"{section}_{style_type}"
        self.styles[style_name] = {**self.base_template,**template, **self.heading_templates.get(style_type, {})}

    def build(self):
        self.header_frame = frame('header', '0.5 inch', 'page_height-1.5 inch-.5 inch', 'page_width - 1 inch', '1.5 inch')
        self.footer_frame = frame('footer', '.25 inch', '.25 inch', 'page_width - .5 inch', '.5 inch')
        self.wide_column_frame = frame('wide_column', '.25 inch', 'footer.height+footer.top+.25 inch', '(page_width - .75 inch) * 0.66', 'page_height-header.height-footer.height -1 inch')
        self.small_column_frame = frame('small_column', 'wide_column.left+wide_column.width +0.25 inch', 'footer.height+footer.top+.25 inch', 'page_width - wide_column.width -.75 inch', 'page_height-header.height-footer.height -1 inch')
        self.header_bg_rect = shape_rectangle('header_bg_rect', 0, 'page_height-2 inch', 'page_width', '2 inch', '#004455')
        self.edge_color_rect = shape_rectangle('edge_color_rect',  0, 0, '.125 inch', 'page_height', '#EE0000')
        self.header_bg_circle = shape_circle('header_bg_circle', 'page_width - 1.5 inch', 'page_height-1 inch', '.75 inch', '#222222',1)
        self.picture = shape_picture('picture', 'header.left+header.width-1.70 inch', 'header.top + .35 inch', '1.4 inch', '1.4 inch', 'circle', '#000000')
        self.global_settings = global_settings(True, True)
        self.metadata['frames'] = [self.header_frame, self.footer_frame, self.wide_column_frame, self.small_column_frame]
        self.metadata['shapes'] = [self.header_bg_rect, self.edge_color_rect, self.header_bg_circle]
        self.metadata['picture'] = self.picture
        self.metadata['global'] = self.global_settings
        self.generate_columns()
        self.generate_template()
        self.generate_stylesheet()
        self.metadata['template'] = self.template
        self.metadata['styles'] = self.styles
    
    def load(self):
        """
        Load page template metadata from a YAML file.
        """
        with open(self.template_file, 'r') as file:
            self.metadata = yaml.safe_load(file)
        return self.metadata.get('page_template', {})
    

    def save(self):
        with open(self.template_file, 'w') as file:
            yaml.emitter.Emitter.prepare_tag = lambda self, tag: ''
            yaml.dump({'page_template': self.metadata}, file)




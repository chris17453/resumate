from reportlab.lib.pagesizes import letter
from reportlab.platypus import Frame,PageTemplate
from reportlab.lib.units import inch
from functools import partial

import yaml
from .header import header_footer
from .styles import create_styles

class frame_def:
    def __init__(self, id, left, top, width, height,background_color=None):
        self.id = id
        self._left = left
        self._top = top
        self._width = width
        self._height = height
        self._background_color = background_color

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
    @property
    def background_color(self):
        return self._background_color


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
    styles=create_styles(metadata['styles'])
    
    frames = []
    frames_dict = {}
    page_templates=[]
    for frame_data in metadata['frames']:
        x1=_eval_with_units(frame_data.get('left', '0'), frames_dict)
        y1=_eval_with_units(frame_data.get('top', '0'), frames_dict)
        width=_eval_with_units(frame_data.get('width', '0'), frames_dict)
        height=_eval_with_units(frame_data.get('height', '0'), frames_dict)
        frame_id=frame_data.get('id', '')
        bg_color=frame_data.get('background-color', None)
        frames_dict[frame_id] =frame_def(frame_id,x1,y1,width,height,bg_color)
        if frame_id=='header' or frame_id=='footer':
            continue
        frame = Frame(
            x1,
            y1,
            width,
            height,
            id=frame_id,
        )
        frames.append(frame)
        page_templates.append( PageTemplate(id=frame_id, frames=frame,pagesize=letter))
        #print (f"{x1},{y1},{width},{height},{frame_id}")
    metadata['header']=frames_dict['header']
    metadata['footer']=frames_dict['footer']
    
    return [frames_dict,page_templates,styles]


def create_combined_template(metadata):
    styles=create_styles(metadata['styles'])
    
    frames = []
    frames_dict = {}
    for frame_data in metadata['frames']:
        x1=_eval_with_units(frame_data.get('left', '0'), frames_dict)
        y1=_eval_with_units(frame_data.get('top', '0'), frames_dict)
        width=_eval_with_units(frame_data.get('width', '0'), frames_dict)
        height=_eval_with_units(frame_data.get('height', '0'), frames_dict)
        frame_id=frame_data.get('id', '')
        bg_color=frame_data.get('background-color', None)
        frames_dict[frame_id] =frame_def(frame_id,x1,y1,width,height,bg_color)
        
        if frame_id=='header' or frame_id=='footer':
            continue
        frame = Frame(
            x1,
            y1,
            width,
            height,
            id=frame_id,
        )
        frames.append(frame)
    
    page_template=PageTemplate(id=frame_id, frames=frames,pagesize=letter,onPage=partial(header_footer, metadata=metadata,styles=styles))
    
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


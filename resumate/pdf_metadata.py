from reportlab.lib.pagesizes import letter
from reportlab.platypus import Frame,PageTemplate
from reportlab.lib.units import inch
from functools import partial

import yaml
from .header import header_footer
from .styles import create_styles
from .common import _eval_with_units


from .shapes import shape_circle,shape_rectangle, shape_picture

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


def calculate_objects(metadata):
    objects = {}
    for item in metadata['frames']:
        x1=_eval_with_units(item.get('left', '0'), objects)
        y1=_eval_with_units(item.get('top', '0'), objects)
        width=_eval_with_units(item.get('width', '0'), objects)
        height=_eval_with_units(item.get('height', '0'), objects)
        item_id=item.get('id', '')
        bg_color=item.get('background_color', None)
        objects[item_id] =shape_rectangle(item_id,x1,y1,width,height,bg_color)
    
    item=metadata['picture']
    x1=_eval_with_units(item.get('left', '0'), objects)
    y1=_eval_with_units(item.get('top', '0'), objects)
    max_width=_eval_with_units(item.get('max_width', '0'), objects)
    max_height=_eval_with_units(item.get('max_height', '0'), objects)
    mask=item.get('mask', 'circle')
    item_id=item.get('id', '')
    bg_color=item.get('background_color', None)
    depth=item.get('depth', 0)
    objects[item_id] =shape_picture(item_id,x1,y1,max_width,max_height,mask,bg_color,depth)

    
    for item in metadata['shapes']:
        item_id=item.get('id', '')
        item_type=item.get('type', '')
        if item_type=='rect':
            x1=_eval_with_units(item.get('left', '0'), objects)
            y1=_eval_with_units(item.get('top', '0'), objects)
            width=_eval_with_units(item.get('width', '0'), objects)
            height=_eval_with_units(item.get('height', '0'), objects)
            bg_color=item.get('background_color', None)
            depth=item.get('depth', 0)
            objects[item_id] =shape_rectangle(item_id,x1,y1,width,height,bg_color,depth)
        if item_type=='circle':
            x1=_eval_with_units(item.get('left', '0'), objects)
            y1=_eval_with_units(item.get('top', '0'), objects)
            diameter=_eval_with_units(item.get('diameter', '0'), objects)
            bg_color=item.get('background_color', None)
            depth=item.get('depth', 0)
            objects[item_id] =shape_circle(item_id,x1,y1,diameter,bg_color,depth)
    
    return objects




def create_page_template(metadata):
    styles=create_styles(metadata['styles'])
    
    frames = []
    frames_dict = metadata['objects']
    page_templates=[]

    for frame_data in metadata['frames']:
        frame_id=frame_data.get('id', '')
        shape=frames_dict[frame_id]
        if frame_id=='header' or frame_id=='footer':
            continue
        frame = Frame(shape.left,shape.top,shape.width,shape.height,id=shape.id,)
        frames.append(frame)
        page_templates.append( PageTemplate(id=frame_id, frames=frame,pagesize=letter))
        
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
        bg_color=frame_data.get('background_color', None)
        frames_dict[frame_id] =shape_rectangle(frame_id,x1,y1,width,height,bg_color)
        
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


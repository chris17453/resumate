from datetime import datetime
from .paragraph import ParagraphD,LineDrawer,SpacerD
from reportlab.platypus import KeepTogether, Paragraph, Spacer
import copy 

from .common import ucfirst, get_style

def add_section(base, section, data,styles):
    pdf_object=[]
    name=section['name']
    if base['heading']['upper']:
        heading=section['name'].upper()
    else:
        heading=ucfirst(section['name'])
    if base['heading']['bold']:
        heading=f"<b>{heading}</b>"
    
    style=get_style(name,'Heading1',styles)
    pdf_object.append(ParagraphD(heading,style))
    pdf_object.append(SpacerD(5,5))
    pdf_object.append(LineDrawer(5,style.textColor))

    
    pdf_object.extend(add_items(base,section,data,styles))

    # add the spacing gap at the end
    pdf_object.append(SpacerD(1,20))
    if 'keep_together' in section and section['keep_together']==True:
        return [KeepTogether(pdf_object)]
    else:
        return pdf_object


def add_items(base,section,data,styles):
    pdf_object=[]
    name=section['name']
    if section['type']=='text':
        pdf_object.extend(add_item(base,section,data[name],styles,name)  )

    elif section['type']=='array':
        for item in data[name]:
            #print (f"List: {section['name']}")
            pdf_object.extend(add_item(base,section,item,styles,name))

    elif section['type']=='object':
            #print (f"List: {section['name']}")
            pdf_object.extend(add_item(base,section,data[name],styles,name))
        
    return pdf_object


def convert_data(data):
    # Create a deep copy of the original data
    data_copy = copy.deepcopy(data)
    
    # Recursive function to traverse nested structures
    def _convert(item):
        if isinstance(item, dict):
            for key, value in item.items():
                item[key] = _convert(value)
            return item
        elif isinstance(item, list):
            for i, value in enumerate(item):
                item[i] = _convert(value)
            return item
        elif isinstance(item, str):
            try:
                datetime_obj = datetime.strptime(item, "%Y-%m-%d")
                return datetime_obj.date()
            except ValueError :
                return item
        else:
            return item
    
    # Call the recursive function on the copied data
    return _convert(data_copy)
def add_item(base,section,data,styles,name):
    pdf_object=[]
    #print(data)
    #print(section)
    object_type=ParagraphD
    if name=='header' or name=='footer':
         object_type=Paragraph



    data_copy=convert_data(data)
    for item in section['format']:
        #print(item)
        style=get_style(name,item['style'],styles)
        if item['type']=="spacer":
                pdf_object.append(SpacerD(5,item['data']))
        elif item['type']=="string":
                pdf_object.append(object_type(str(data_copy[item['data']]), style))
        elif item['type']=="format":
                #print(data)
                pdf_object.append(object_type(str(item['data'].format(**data_copy)), style))
        elif item['type']=="list":
            if isinstance(data_copy,str):
                pdf_object.append(object_type(data_copy, style,  bulletText=base['list']['bullet_style']))
            else:
                pdf_object.append(object_type(item['data'].format(**data_copy), style,  bulletText=base['list']['bullet_style']))

    return pdf_object


def add_item3(base, section, data, styles, name):
    pdf_object = []

    # Check if the data is a dictionary (nested object)
    if isinstance(data, dict):
        # Iterate over each key-value pair in the dictionary
        for key, value in data.items():
            # Recursively add each key-value pair as an item
            pdf_object.extend(add_item(base, section, {key: value}, styles, name))
    # Check if the data is a list (nested list)
    elif isinstance(data, list):
        # Iterate over each item in the list
        for item in data:
            # Recursively add each item in the list
            pdf_object.extend(add_item(base, section, item, styles, name))
    else:
        # If the data is a string or other primitive type, add it as a single item
        for item_format in section['format']:
            style = get_style(name, item_format['style'], styles)
            if item_format['type'] == "string":
                pdf_object.append(ParagraphD(str(data), style))
            elif item_format['type'] == "format":
                pdf_object.append(ParagraphD(str(item_format['data'].format(**{name: data})), style))
            elif item_format['type'] == "list":
                pdf_object.append(ParagraphD(str(item_format['data'].format(**{name: data})), style,
                                             bulletText=base['list']['bullet_style']))

    return pdf_object

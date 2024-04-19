import yaml
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.colors import HexColor

# Mapping for text alignment to be used in style conversion
alignment_mapping = {
    'TA_LEFT': TA_LEFT,
    'TA_CENTER': TA_CENTER,
    'TA_RIGHT': TA_RIGHT,
    'TA_JUSTIFY': TA_JUSTIFY
}
def create_styles(style_data):
    default_styles = getSampleStyleSheet()  # This gets the default styles
    custom_styles = {}

    for style_name, style_attrs in style_data.items():
        # If there's a parent style specified, try to find it in custom styles first
        if 'parent' in style_attrs:
            parent_style_name = style_attrs.pop('parent')  # Remove the parent from attrs
            parent_style = custom_styles.get(parent_style_name)
            if parent_style is None:
                parent_style = default_styles.get(parent_style_name)
            if parent_style is None:
                raise ValueError(f"Parent style '{parent_style_name}' not found in stylesheet")
        else:
            parent_style = None

        # Convert alignment value to ReportLab enum
        if 'alignment' in style_attrs:

            if isinstance(style_attrs['alignment'], str):
                alignment = style_attrs['alignment'].upper()
                if alignment in alignment_mapping:
                    style_attrs['alignment'] = alignment_mapping[alignment]
                else:
                    raise ValueError(f"Invalid alignment value '{alignment}'")
            else:
                alignment = style_attrs['alignment']


        # Create the custom style, ensuring that 'parent' is an actual ParagraphStyle object
        custom_styles[style_name] = ParagraphStyle(name=style_name, parent=parent_style, **style_attrs)

    return custom_styles
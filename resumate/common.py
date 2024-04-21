def ucfirst(string):
    return string[0].upper() + string[1:] if string else ''
    
def get_style(name,style,styles):
    style=f"{name}_{style}"

    return styles[style]
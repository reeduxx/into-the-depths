from blessed import Terminal

def get_background_brightness(term):
    try:
        bg = term.get_bgcolor(0.1)
        
        if isinstance(bg, tuple):
            return sum(bg) / 3
    except:
        pass
    
    return 255 # If color cannot be determined, assume white

def get_colors(term):
    brightness = get_background_brightness(term)
    # The game title is white/red on darker screens and white/green on lighter screens
    opaque_color = term.black if brightness > 128 else term.white
    translucent_color = term.green if brightness > 128 else term.red
    
    return opaque_color, translucent_color
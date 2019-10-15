def mid_preset(min_val, max_val, confidence):
    """
    Returns beta distribution parameters (symmetric)
    """
    loc = min_val
    scale = max_val - min_val
    a = b = max(min(confidence+1,3),0.1)**2
    return {'a': a, 'b': b, 'loc': loc, 'scale': scale}

def high_preset(min_val, max_val, confidence):
    """
    Returns beta distribution parameters (left skewed)
    """
    loc = min_val
    scale = max_val - min_val
    b = min(2.5,confidence+1.5)
    b = max(b,0.1)
    a = 6 - b 
    return {'a': a, 'b': b, 'loc': loc, 'scale': scale}

def low_preset(min_val, max_val, confidence):
    """
    Returns beta distribution parameters (right skewed)
    """
    loc = min_val
    scale = max_val - min_val
    a = min(confidence+1.5,2.5)
    a = max(a,0.1)
    b = 6 - a 
    return {'a': a, 'b': b, 'loc': loc, 'scale': scale}

def priamka(x1, y1, x2, y2, X=False, Y=False):
    """Aproximuje ako priamku hodnotu x alebo y podla dvoch bodov. MOZE BYT ZADANE IBA X ALEBO IBA Y !!!"""
    a = (y2 - y1) / (x2 - x1)
    b = a * x1 - y1
    if X:
        Y = a * X - b
        return Y
    elif Y:
        X = (b + Y) / a
        return X
    else:
        print("Error. Zadate hladanu hodnotu x alebo y")        
    pass
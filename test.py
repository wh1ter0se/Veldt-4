def flip_color_order(rgb,color_order):
    color_order = list(color_order)
    indexes = [color_order.index('R'), color_order.index('G'), color_order.index('B')]
    r,g,b = rgb
    print(indexes)
    if color_order == 'RGB': return r,g,b
    elif color_order == 'RBG': return r,b,g
    elif color_order == 'BRG': return b,r,g
    elif color_order == 'BGR': return b,g,r
    elif color_order == 'GBR': return g,b,r
    elif color_order == 'GRB': return g,r,b
    # r = rgb[indexes[0]]
    # g = rgb[indexes[1]]
    # b = rgb[indexes[2]]
    # return (r,g,b)

print(flip_color_order([255,0,0],'GBR'))
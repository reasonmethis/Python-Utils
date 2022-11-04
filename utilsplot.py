from io import BytesIO

def fig2bytes(fig):
    #https://stackoverflow.com/questions/43564943/saving-matplotlib-plot-to-memory-and-placing-on-tkinter-canvas
    buf = BytesIO()
    try:
        fig.savefig(buf, format='png')
        #buf.seek(0)
        img = buf.getvalue()
        #if need a png image in memory, use, instead of previous line:
        #from PIL import Image
        #img = Image.open(buf)
    finally:
        buf.close()
    return img

def fig2mem_alt(fig):
    #https://stackoverflow.com/questions/61662117/matplotlib-export-figure-to-png-in-memory-buffer
    import base64
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic
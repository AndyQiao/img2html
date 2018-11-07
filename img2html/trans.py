import jinja2
from PIL import Image
from collections import namedtuple

ImgHtml=list 
ImgHtmlRow=list
ImgHtmlItem=namedtuple('ImgHtmlItem', ['color', 'char'])
Point=namedtuple('Point', ['x', 'y'])
Pixel=namedtuple('Pixel',['r', 'g', 'b'])


TEMPLATE = '''
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <style type="text/css">
        body {
            margin: 0px; padding: 0px; line-height:100%; letter-spacing:0px; text-align: center;
            min-width: {{width}}px;
            width: auto !important;
            font-size: {{size}}px;
            background-color: #{{background}};
            font-family: {{font_family}};
        }
    </style>
</head>
<body>
<div>
{% for group in html_image %}
    {% for item in group %}<font color="#{{ item.color }}">{{ item.char }}</font>{% endfor %}
    <br>
{% endfor %}
</div>
</body>
</html>'''

class Trans():
    def __init__(self,font_size,background,title,font_family):
        self.font_size=font_size
        self.background=background
        self.title=title
        self.font_family=font_family

    def trans(self, source, char):
        image = Image.open(source)

        width, height = image.size
        rows, cols = round(height/self.font_size), round(width/self.font_size)

        imgHtml = ImgHtml()
        for row in range(rows):
            imgHtmlRow = ImgHtmlRow()
            for col in range(cols):
                pixels = []
                for x in range(self.font_size):
                    for y in range(self.font_size):
                        point = Point(col * self.font_size + x, row * self.font_size + y)
                        if(point.x >= width or point.y >= height):
                            continue 
                        pixel = Pixel(*image.getpixel(point)[:3])
                        pixels.append(pixel)
                pixel = self.average(pixels)
                imgHtmlItem = ImgHtmlItem(self.rgb2hex(pixel), char)
                imgHtmlRow.append(imgHtmlItem)
            imgHtml.append(imgHtmlRow)

        self.render('D:\\code\\trans_img2html\\after.html', imgHtml)
    
    def average(self, pixels):
        r,g,b=0,0,0
        for pixel in pixels:
            r += pixel.r;
            g += pixel.g;
            b += pixel.b;
        base = float(len(pixels))
        return Pixel(
            r = round(r/base),
            g = round(g/base),
            b = round(b/base)
        )

    def rgb2hex(self, pixel):
        return '{:02x}{:02x}{:02x}'.format(*pixel)


    def render(self, output_file, html_image):
        template = jinja2.Template(TEMPLATE)
        html_text = template.render(
            html_image=html_image,
            size=self.font_size,
            background=self.background,
            title=self.title,
            font_family=self.font_family,
            width=self.font_size * len(html_image[0]) * 2
        )
        with open(output_file, 'w', encoding='UTF-8') as f:
            f.write(html_text)

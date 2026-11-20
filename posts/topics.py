from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance, ImageFilter
im=ImageOps.exif_transpose(Image.open('inputs/photo.jpg')).convert('RGB')
# 4:5 crop keeping face + top dark area
W0,H0=im.size; ch=int(W0*5/4); y0=H0-ch-40; im=im.crop((0,y0,W0,y0+ch)).resize((1080,1350),Image.LANCZOS)
im=ImageEnhance.Contrast(im).enhance(1.08); im=ImageEnhance.Color(im).enhance(1.08)
W,H=im.size
# dark gradient on left for text
g=Image.new("L",(W,H)); gd=ImageDraw.Draw(g)
for y in range(H):
    a=int(225*max(0,(y-700)/650)**0.9); gd.line([(0,y),(W,y)],fill=a)
ov=Image.new("RGB",(W,H),(6,10,22)); im=Image.composite(ov,im,g)
d=ImageDraw.Draw(im)
B="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; SB="/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf"
import os
if not os.path.exists(SB): SB=B
f=lambda p,s: ImageFont.truetype(p,s)
RED=(232,57,43)
d.text((70,800),"What I'll be",font=f(B,58),fill="white")
d.text((70,872),"talking about",font=f(B,58),fill="white")
d.rectangle((70,962,190,969),fill=RED)
items=["A/B testing","Statistics, made simple","SQL for real jobs","Data visualization","Product & growth analytics","Careers in data"]
y=995
for it in items:
    d.ellipse((74,y+16,92,y+34),fill=RED)
    d.text((115,y+25),it,font=f(SB,34),fill="white",anchor="lm"); y+=52
d.text((W-70,H-70),"@heytheanalyst",anchor="rm",font=f(SB,34),fill=(220,224,232))
im.save("topics_post.jpg",quality=95)
im.resize((540,675)).save("prev.png")

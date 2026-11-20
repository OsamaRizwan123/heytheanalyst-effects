from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance
import subprocess
im=ImageOps.exif_transpose(Image.open('inputs/photo.jpg')).convert('RGB')
W0,H0=im.size; ch=int(W0*5/4); y0=H0-ch-40; im=im.crop((0,y0,W0,y0+ch)).resize((1080,1350),Image.LANCZOS)
im=ImageEnhance.Contrast(im).enhance(1.06); im=ImageEnhance.Color(im).enhance(0.9)
W,H=im.size; d=ImageDraw.Draw(im)
FONT=subprocess.check_output(["fc-match","-f","%{file}","Inter:bold"]).decode()
YEL=(250,236,160)
lines=["you’re not","“non-technical.”","you just haven’t","started yet."]
f=ImageFont.truetype(FONT,100)
y=815
for ln in lines:
    d.text((W/2,y),ln,font=f,fill=YEL,anchor="mm",stroke_width=0); y+=106
d.text((W-60,H-70),"follow @heytheanalyst",font=ImageFont.truetype(FONT,40),fill=YEL,anchor="rm")
im.save("quote_post.jpg",quality=95); im.resize((540,675)).save("prev.png")

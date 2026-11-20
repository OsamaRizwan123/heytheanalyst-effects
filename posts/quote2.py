from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance, ImageFilter
FONT="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; YEL=(250,236,160)
def make(path,out,lines,ycenter,crop_y,size=100,blurbox=None,shadow=False,dark=None):
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    if blurbox:
        bl=im.filter(ImageFilter.GaussianBlur(28)); m=Image.new("L",im.size,0)
        ImageDraw.Draw(m).ellipse(blurbox,fill=255); m=m.filter(ImageFilter.GaussianBlur(40)); im=Image.composite(bl,im,m)
    W0,H0=im.size; ch=int(W0*5/4); y0=int((H0-ch)*crop_y); im=im.crop((0,y0,W0,y0+ch)).resize((1080,1350),Image.LANCZOS)
    im=ImageEnhance.Color(im).enhance(0.92)
    if dark:
        g=Image.new("L",im.size,0); gd=ImageDraw.Draw(g); a,b,al=dark
        for y in range(a,b): gd.line([(0,y),(1080,y)],fill=int(al*(1-abs((y-(a+b)/2)/((b-a)/2)))**0.6))
        im=Image.composite(Image.new("RGB",im.size,(10,12,20)),im,g)
    d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,size); lh=int(size*1.06)
    y=ycenter-lh*(len(lines)-1)/2
    for ln in lines:
        if shadow: d.text((542,y+4),ln,font=f,fill=(20,20,20),anchor="mm")
        d.text((540,y),ln,font=f,fill=YEL,anchor="mm"); y+=lh
    if shadow: d.text((1022,1283),"follow @heytheanalyst",font=ImageFont.truetype(FONT,40),fill=(0,0,0),anchor="rm")
    d.text((1020,1280),"follow @heytheanalyst",font=ImageFont.truetype(FONT,40),fill=YEL,anchor="rm")
    im.save(out,quality=95); return im
a=make('inputs/photo.jpg',"sunset_post.jpg",
  ["coding isn’t dying.","copy-paste","coding is."],250,0.55,100,dark=(60,420,90))
b=make('inputs/photo.jpg',"mirror_post.jpg",
  ["your certificates","don’t get you hired.","your projects do."],930,0.75,90,blurbox=(1250,840,1540,1320),dark=(700,1350,170),shadow=True)
o=Image.new("RGB",(1090,675),"black"); o.paste(a.resize((540,675)),(0,0)); o.paste(b.resize((540,675)),(550,0)); o.save("prev2.png")

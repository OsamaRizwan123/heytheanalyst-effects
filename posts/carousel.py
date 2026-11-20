from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance, ImageFilter
FONT="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; YEL=(250,236,160)
f=lambda s: ImageFont.truetype(FONT,s)
# slide 1: text only
s1=Image.new("RGB",(1080,1350),(14,16,22)); d=ImageDraw.Draw(s1)
d.text((540,610),"is coding",font=f(150),fill=YEL,anchor="mm"); d.text((540,770),"dying?",font=f(150),fill=YEL,anchor="mm")
d.text((1020,1280),"swipe →".replace(" →",""),font=f(38),fill=(150,150,150),anchor="rm")
s1.save("slide1.jpg",quality=95)
U='inputs/'
def load(p,cy,blur=None):
    im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    if blur:
        bl=im.filter(ImageFilter.GaussianBlur(28)); m=Image.new("L",im.size,0); ImageDraw.Draw(m).ellipse(blur,fill=255); m=m.filter(ImageFilter.GaussianBlur(40)); im=Image.composite(bl,im,m)
    W0,H0=im.size; ch=int(W0*5/4); y0=int((H0-ch)*cy); im=im.crop((0,y0,W0,y0+ch)).resize((1080,1350),Image.LANCZOS)
    im=ImageEnhance.Brightness(im).enhance(0.78); return ImageEnhance.Color(im).enhance(0.9)
BGS={"OpenAI":(load(U+'8798886d-image.jpg',1.0),"bottom"),
     "Google":(load(U+'475084f9-image.jpg',0.55),"top"),
     "Meta":(load(U+'abe8d8ea-image.jpg',0.75,blur=(1250,840,1540,1320)),"bottom")}
cuts={"OpenAI":312,"Google":390,"Meta":380}
for n,k in enumerate(["OpenAI","Google","Meta"],start=2):
    im,pos=BGS[k]; im=im.copy()
    _r=Image.open(f'job_{k}.png'); raw=_r.crop((90,0,1150,min(cuts[k],_r.height)))
    card=Image.new("RGB",(raw.width,raw.height+200),"white"); card.paste(raw,(0,170))
    w=780; h=int(card.height*w/card.width); c=card.resize((w,h),Image.LANCZOS); x=50; y=110 if pos=='top' else 1350-h-130
    sh=Image.new("RGBA",(w+60,h+60),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((30,38,w+30,h+38),radius=28,fill=(0,0,0,130)); sh=sh.filter(ImageFilter.GaussianBlur(16))
    im.paste(sh,(x-30,y-30),sh); m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w,h),radius=28,fill=255); im.paste(c,(x,y),m)
    lg=Image.open(f"logo_{k.lower()}.png"); lh=78 if k!="Meta" else 62; lg=lg.resize((int(lg.width*lh/lg.height),lh),Image.LANCZOS)
    im.paste(lg,(x+34,y+int(125/2)-lh//2+8),lg)
    dd=ImageDraw.Draw(im); cyh=y+int(125/2)+8; lx=x+34+lg.width+26
    dd.line([(lx-13,cyh-24),(lx-13,cyh+24)],fill=(210,214,220),width=3)
    dd.text((lx+6,cyh),"Data Scientist",font=f(34),fill=(110,118,130),anchor="lm")
    d=ImageDraw.Draw(im); d.text((1020,1280),"follow @heytheanalyst",font=f(36),fill=YEL,anchor="rm")
    im.save(f"slide{n}_{k}.jpg",quality=95)
    # guide version showing logo spot
    g=im.copy(); gd=ImageDraw.Draw(g); gd.rounded_rectangle((x+40,y+30,x+340,y+30+int(130*w/1060)),radius=14,outline=(200,205,212),width=4); gd.text((x+170,y+30+int(65*w/1060)),"logo here",font=f(30),fill=(190,195,204),anchor="mm")
    g.resize((360,450)).save(f"g{n}.png")
o=Image.new("RGB",(360*4+30,450),"black"); o.paste(s1.resize((360,450)),(0,0))
for i in range(2,5): o.paste(Image.open(f"g{i}.png"),((i-1)*370,0))
o.save("crop.png")

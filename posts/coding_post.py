from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance, ImageFilter
FONT="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; YEL=(250,236,160); RED=(232,57,43)
f=lambda s: ImageFont.truetype(FONT,s)
im=ImageOps.exif_transpose(Image.open('inputs/photo.jpg')).convert('RGB')
W0,H0=im.size; ch=int(W0*5/4); y0=int((H0-ch)*0.55); im=im.crop((0,y0,W0,y0+ch)).resize((1080,1350),Image.LANCZOS)
im=ImageEnhance.Brightness(im).enhance(0.55); im=ImageEnhance.Color(im).enhance(0.85)
d=ImageDraw.Draw(im)
d.text((540,120),"is coding dying?",font=f(92),fill=YEL,anchor="mm")
d.text((540,205),"then why does every top company still ask for it?",font=f(34),fill="white",anchor="mm")
y=270
from PIL import Image as I
cuts={"OpenAI":(0,0,1150,226),"Google":(0,0,1150,312),"Meta":(0,0,1150,226)}
for k in ["OpenAI","Google","Meta"]:
    raw=I.open(f'job_{k}.png').crop(cuts[k]).crop((90,0,1150,cuts[k][3]))
    card=I.new("RGB",(raw.width,raw.height+95),"white"); card.paste(raw,(0,95))
    cd=ImageDraw.Draw(card); tw=cd.textlength(k,font=f(40))
    cd.rounded_rectangle((30,24,30+tw+44,84),radius=30,fill=RED); cd.text((52+tw/2,54),k,font=f(40),fill="white",anchor="mm")
    cd.text((60+tw+70,54),"from the job posting",font=f(30),fill=(150,155,165),anchor="lm")
    w=860; h=int(card.height*w/card.width); c=card.resize((w,h),I.LANCZOS); x=110
    sh=I.new("RGBA",(w+60,h+60),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((30,38,w+30,h+38),radius=24,fill=(0,0,0,120)); sh=sh.filter(ImageFilter.GaussianBlur(14))
    im.paste(sh,(x-30,y-30),sh); m=I.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w,h),radius=24,fill=255); im.paste(c,(x,y),m)
    y+=h+32
d=ImageDraw.Draw(im)
d.text((1020,1300),"follow @heytheanalyst",font=f(36),fill=YEL,anchor="rm")
im.save("coding_post.jpg",quality=95); im.resize((540,675)).save("prev.png"); print(y)

# Orbit effect: cards circle your head (behind at the top, in front at the bottom).
# Needs frames f_###.png (ffmpeg -ss START -t DUR -i video -vf fps=30 f_%03d.png)
# and person masks m_###.png (rembg, model u2net_human_seg). Writes o_###.png to overlay back onto the video.
import numpy as np, glob, math, sys
from PIL import Image, ImageDraw, ImageFilter
srcs=["assets/charts/1b_after.png","assets/charts/2b_after.png","assets/charts/5b_after.png","assets/charts/6b_after.png","assets/charts/7b_after.png","assets/charts/9b_after.png"]  # images that orbit your head
CW,CH=165,293
CX,CY,RX,RY=590,950,450,330
def mk(p):
    im=Image.open(p).convert("RGB"); w,h=im.size; t=CW/CH
    if w/h>t: nw=int(h*t); im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    else: nh=int(w/t); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
    im=im.resize((CW,CH),Image.LANCZOS).convert("RGBA")
    m=Image.new("L",(CW,CH),0); ImageDraw.Draw(m).rounded_rectangle([0,0,CW-1,CH-1],radius=16,fill=255); im.putalpha(m)
    pad=24; sh=Image.new("RGBA",(CW+2*pad,CH+2*pad),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([pad,pad+6,pad+CW,pad+CH+6],radius=16,fill=(0,0,0,120))
    sh=sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(im,(pad,pad))
    ImageDraw.Draw(sh).rounded_rectangle([pad,pad,pad+CW-1,pad+CH-1],radius=16,outline=(255,255,255,230),width=4); return sh
cards=[mk(p) for p in srcs]
def ease(x): x=max(0,min(1,x)); return x*x*(3-2*x)
fs=sorted(glob.glob("f_*.png"))
for i,f in enumerate(fs):
    t=i/30; fr=Image.open(f).convert("RGBA"); m=Image.open(f.replace("f_","m_")).convert("L")
    person=fr.copy(); person.putalpha(m)
    a=ease(t/0.45)*(1-ease((t-2.55)/0.45)); items=[]
    for k,c in enumerate(cards):
        th=2*math.pi*k/len(cards)+2*math.pi*t/2.8
        r=0.55+0.45*a; x=CX+RX*math.cos(th)*r; y=CY+RY*math.sin(th)*r; depth=math.sin(th)
        sc=(0.8+0.25*(depth+1)/2)*(0.4+0.6*a); items.append((depth,x,y,sc,c))
    out=fr.copy()
    for front in (False,True):
        for depth,x,y,sc,c in sorted(items,key=lambda z:z[0]):
            if (depth>0.15)!=front: continue
            cc=c.resize((int(c.width*sc),int(c.height*sc)),Image.BILINEAR)
            if a<0.999: cc.putalpha(cc.getchannel("A").point(lambda p:int(p*a)))
            out.alpha_composite(cc,(int(x-cc.width/2),int(y-cc.height/2)))
        if not front: out.alpha_composite(person)
    out.convert("RGB").save(f.replace("f_","o_"))

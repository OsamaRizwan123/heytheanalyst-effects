import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS,DUR=1080,960,30,10.5
B="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
NAVY,RED,YEL,GREYC,GOLD=(11,31,75),(232,57,43),(245,184,0),(140,150,160),(190,140,0)
def f(s): return ImageFont.truetype(B,s)
old=Image.open('inputs/photo.jpg').convert('RGB')
new=Image.open('inputs/photo.jpg').convert('RGB')
OB=old.crop((0,2226,1206,2381)); NB=new.crop((0,2226,1206,2381))
OT=old.crop((0,20,1206,150)); NT=new.crop((0,5,1206,135))
_av=NT.crop((48,0,178,130)).resize((112,112)); _m=Image.new("L",_av.size,0); ImageDraw.Draw(_m).ellipse((0,0,111,111),fill=255)
ImageDraw.Draw(OT).ellipse((60,6,182,128),fill="white"); OT.paste(_av,(55,13),_m)
xs=[120,360,602,843,1084]; BW=1000; SC=BW/1206; BH=int(OB.height*SC); TH=int(OT.height*SC)
def spr(img,cx): return img.crop((cx-120,0,cx+120,img.height))
O={n:spr(OB,xs[i]) for i,n in enumerate(["Home","Network","Post","Notif","Jobs"])}
N={n:spr(NB,xs[i]) for i,n in enumerate(["Home","Jobs","Network","Notif","More"])}
blank=Image.new("RGB",OB.size,"white")
BG=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(BG)
for x in range(0,W,70): d.line([(x,0),(x,H)],fill=(241,242,245),width=2)
for y in range(0,H,70): d.line([(0,y),(W,y)],fill=(241,242,245),width=2)
BX=(W-BW)//2; TY=345; BY=640
X=lambda i:BX+xs[i]*SC; YC=BY+BH/2
CX,CY=BX+978*SC,TY+65*SC   # compose spot in top bar
def ease(x): x=min(max(x,0),1); return 4*x**3 if x<.5 else 1-(-2*x+2)**3/2
def back(x): x=min(max(x,0),1); c1=1.70158; c3=c1+1; return 1+c3*(x-1)**3+c1*(x-1)**2
def card(im,img,x,y,w,h,alpha=1.0):
    r=img.resize((w,h)); m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w,h),radius=22,fill=int(255*alpha))
    sh=Image.new("RGBA",(w+60,h+60),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((30,38,w+30,h+38),radius=22,fill=(0,0,0,int(50*alpha)))
    sh=sh.filter(ImageFilter.GaussianBlur(16)); im.paste(sh,(x-30,y-30),sh); im.paste(r,(x,y),m)
def put(im,s,cx,cy,scale=1.0,alpha=1.0,outline=None):
    w,h=int(s.width*SC*scale),int(s.height*SC*scale); r=s.resize((max(w,1),max(h,1)))
    m=Image.new("L",r.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,w,h),radius=16,fill=int(255*alpha)); im.paste(r,(int(cx-w/2),int(cy-h/2)),m)
    if outline and alpha>0.5: ImageDraw.Draw(im).rounded_rectangle((cx-w/2,cy-h/2,cx+w/2,cy+h/2),radius=16,outline=outline,width=4)
def ring(d,cx,cy,r,col,p):
    if p>0: d.ellipse((cx-r*p,cy-r*p,cx+r*p,cy+r*p),outline=col,width=7)
def pill(d,cx,cy,txt,size,fill):
    ft=f(size); w=d.textlength(txt,font=ft); d.rounded_rectangle((cx-w/2-24,cy-size*0.8,cx+w/2+24,cy+size*0.8),radius=size,fill=fill); d.text((cx,cy),txt,font=ft,fill="white",anchor="mm")
def header(d,a,b):
    ft=f(46); w1=d.textlength(a+" ",font=ft); w2=d.textlength(b,font=ft); x=(W-w1-w2)/2
    d.text((x,262),a+" ",font=ft,fill=RED,anchor="lm"); d.text((x+w1,262),b,font=ft,fill=NAVY,anchor="lm")
def label(d,y,txt,col): d.text((BX,y),txt,font=f(26),fill=col,anchor="lm")
def frame(t):
    im=BG.copy(); d=ImageDraw.Draw(im)
    # ---------- phase titles
    if t<1.3: header(d,"LinkedIn:","what changed?"); tag=("OLD",GREYC)
    elif t<5.6: header(d,"Change 1:","the buttons moved"); tag=("1. MOVED",NAVY)
    elif t<8.2: header(d,"Change 2:","the icon style"); tag=("2. RESTYLED",NAVY)
    else: header(d,"LinkedIn:","what changed?"); tag=("NEW",RED)
    # ---------- top bar
    landed = t>=3.4
    card(im,NT if landed else OT,BX,TY,BW,TH); d=ImageDraw.Draw(im)
    label(d,TY-24,"TOP BAR",GREYC)
    if landed: ring(d,CX,CY,52,YEL,back((t-3.4)/0.3))
    # ---------- bottom bar
    card(im,OB if t<1.3 else (NB if t>=8.2 else blank),BX,BY,BW,BH); d=ImageDraw.Draw(im)
    label(d,BY-24,"BOTTOM NAVIGATION BAR",GREYC)
    if t<1.3:
        ring(d,X(4),YC,78,RED,back((t-0.5)/0.3)); ring(d,X(2),YC,78,YEL,back((t-0.8)/0.3))
    elif t<8.2:
        p=(t-1.3)/2.2   # movement 1.3 -> 3.5
        put(im,O["Home"],X(0),YC); put(im,O["Notif"],X(3),YC)
        # Post flies up to the top bar compose spot
        pp=ease(p)
        if pp<1:
            px=X(2)+(CX-X(2))*pp; py=YC+(CY-YC)*pp-math.sin(math.pi*pp)*60
            put(im,O["Post"],px,py,1-0.45*pp,1.0,outline=YEL)
            if 0.1<pp<0.9: d=ImageDraw.Draw(im); d.text((px-90,py),"Post",font=f(28),fill=GOLD,anchor="rm")
        jp=ease((p-0.15)/0.8)
        jx=X(4)+(X(1)-X(4))*jp; jy=YC-math.sin(math.pi*jp)*150
        nx=X(1)+(X(2)-X(1))*ease((p-0.3)/0.6)
        mo=min(1,max(0,(p-0.85)/0.15))
        # style crossfade 5.8 -> 8.0, left to right
        def sty(i): return min(1,max(0,(t-5.8-i*0.35)/0.5))
        slots=[(X(0),YC,"Home","Home"),(jx,jy,"Jobs","Jobs"),(nx,YC,"Network","Network"),(X(3),YC,"Notif","Notif")]
        for i,(x,y,on,nn) in enumerate(slots):
            a=sty(i); put(im,O[on],x,y,1.0+(0.2*math.sin(math.pi*jp) if on=="Jobs" else 0),1-a, outline=RED if on=="Jobs" and t<5.6 else None)
            if a>0: put(im,N[nn],x,y,1.0,a)
        if mo>0: put(im,N["More"],X(4),YC,1.0,mo)
        d=ImageDraw.Draw(im)
        if 3.8<t<5.6:
            d.text((W/2,505),"Jobs: far right  >  2nd spot",font=f(30),fill=RED,anchor="mm")
            d.text((W/2,553),"Post: bottom bar  >  top bar",font=f(30),fill=GOLD,anchor="mm")
        if 5.8<t<8.2:
            d.text((W/2,505),"Filled icons  >  outline icons",font=f(30),fill=NAVY,anchor="mm")
            d.text((W/2,553),"+ the Post slot is now More",font=f(28),fill=GREYC,anchor="mm")
    else:
        ring(d,X(1),YC,78,RED,back((t-8.3)/0.3))
        d.text((W/2,530),"Moved + restyled",font=f(32),fill=NAVY,anchor="mm")
    pill(d,W/2,BY+BH+75,*tag[:1],34,tag[1]) if False else pill(d,W/2,BY+BH+75,tag[0],34,tag[1])
    return im
if sys.argv[1:]==["still"]:
    for tt in (1.0,2.3,3.0,4.5,6.6,9.5): frame(tt).resize((540,480)).save(f"n2_{tt}.png")
    sys.exit()
p=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","li_navbar_v2.mp4"],stdin=subprocess.PIPE)
for i in range(int(DUR*FPS)): p.stdin.write(frame(i/FPS).tobytes())
p.stdin.close(); p.wait(); print("ok")

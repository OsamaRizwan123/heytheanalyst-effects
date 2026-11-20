import numpy as np, matplotlib.pyplot as plt, subprocess, sys
from PIL import Image
W,H=1080,1000; S=2; FPS=30; DUR=27.0
F="Poppins"; NAVY,RED,GREY,INK,MUT,BLUE="#0b3d91","#e8392b","#c9ced6","#1c2433","#7a8494","#4472c4"
months=["Jan","Feb","Mar","Apr","May","Jun"]
data={"Dubai":[120,122,125,124,128,130],"Abu Dhabi":[60,61,62,63,63,64],"Sharjah":[40,44,49,55,61,68],"Ajman":[15,15,16,15,16,16]}
DEF={"Dubai":"#4472c4","Abu Dhabi":"#ed7d31","Sharjah":"#a5a5a5","Ajman":"#ffc000"}
def cl(x): return float(np.clip(x,0,1))
def ease(x): x=cl(x); return x*x*(3-2*x)
def back(x):
    x=cl(x); c1=1.70158; c3=c1+1; return 1+c3*(x-1)**3+c1*(x-1)**2
def mix(a,b,t):
    a=np.array(plt.matplotlib.colors.to_rgb(a)); b=np.array(plt.matplotlib.colors.to_rgb(b)); return tuple(a+(b-a)*t)
STEPS=[(0,"The raw data",MUT),(2.4,"Normal person: insert chart",MUT),(6.5,"Consultant: ask the question first",RED),
       (9.5,"1. Remove the clutter",RED),(14.0,"2. Change the data: growth %",RED),(17.5,"3. Highlight the story",RED),
       (20.5,"4. Title = the answer",RED),(24.0,"Same data. Different answer.",NAVY)]
fig=plt.figure(figsize=(W/180,H/180),dpi=180*S,facecolor="white")
def fy(px): return 1-px/H
def draw(t):
    fig.clf()
    bg=fig.add_axes([0,0,1,1]); bg.set_xlim(0,W); bg.set_ylim(0,H); bg.axis("off")
    for x in range(0,W,70): bg.plot([x,x],[0,H],color="#f1f2f5",lw=0.8)
    for y in range(0,H,70): bg.plot([0,W],[y,y],color="#f1f2f5",lw=0.8)
    k=max(i for i,(st,_,_) in enumerate(STEPS) if t>=st); st,lab,col=STEPS[k]; sc=back((t-st)/0.35)
    if sc>0.05: fig.text(0.5,fy(290),lab,ha="center",va="center",fontsize=11*sc,color="white",fontweight="bold",family=F,bbox=dict(boxstyle="round,pad=0.5",fc=col,ec="none"))
    if t<2.6:   # raw table
        a=ease((t-0.1)/0.4)*(1-ease((t-2.3)/0.3))
        ax=fig.add_axes([0.1,0.1,0.8,0.48]); ax.axis("off")
        cols=["City"]+months; cw=1/7
        for j,c in enumerate(cols): ax.text(cw*j+cw/2,0.95,c,ha="center",va="center",fontsize=10,family=F,fontweight="bold",color="white",alpha=a,bbox=dict(boxstyle="square,pad=0.6",fc=NAVY,ec="none",alpha=a))
        for i,(c,v) in enumerate(data.items()):
            ra=a*ease((t-0.3-0.2*i)/0.3)
            ax.text(cw/2,0.75-i*0.18,c,ha="center",va="center",fontsize=10,family=F,color=INK,alpha=ra)
            for j,x in enumerate(v): ax.text(cw*(j+1)+cw/2,0.75-i*0.18,str(x),ha="center",va="center",fontsize=10,family=F,color=INK,alpha=ra)
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        fig.text(0.5,fy(360),"Food delivery orders (thousands), illustrative",ha="center",fontsize=9.5,family=F,color=MUT,alpha=a)
        return
    ax=fig.add_axes([0.1,0.13,0.72,0.35])
    bars=1-ease((t-14.2)/0.5); lines=ease((t-14.5)/1.2)
    grid=1-ease((t-10.0)/0.5); leg=1-ease((t-11.6)/0.5); ctit=1-ease((t-13.0)/0.5)
    grow=ease((t-2.6)/1.2)
    x=np.arange(6); w=0.2
    if bars>0:
        for i,(c,v) in enumerate(data.items()):
            ax.bar(x+(i-1.5)*w,np.array(v)*grow,w,color=DEF[c],alpha=bars,zorder=3)
        ax.set_ylim(0,145)
    if lines>0:
        ax2=fig.add_axes([0.1,0.13,0.72,0.35]); ax2.patch.set_alpha(0)
        hl=ease((t-17.7)/0.6)
        for c,v in data.items():
            idx=np.array(v)/v[0]*100; n=1+lines*5; xx=np.linspace(0,n,60); yy=np.interp(xx,x,idx)
            isS=c=="Sharjah"; colr=mix(DEF[c],RED if isS else GREY,hl)
            ax2.plot(xx,yy,color=colr,lw=2.2+1.4*hl*isS,zorder=4 if isS else 3)
            if lines>0.98:
                la=ease((t-16.0)/0.4)
                off={"Dubai":8,"Abu Dhabi":0,"Ajman":-8,"Sharjah":0}[c]
                ax2.text(5.15,idx[-1]+off,f"{c} +{idx[-1]-100:.0f}%",va="center",fontsize=(10 if isS else 8.5),family=F,fontweight="bold",color=colr,alpha=la,clip_on=False)
        ax2.set_xlim(-0.4,5.4); ax2.set_ylim(90,185); ax2.axis("off")
        ax2.axhline(100,xmin=0.03,xmax=0.97,color="#dde2e8",lw=1)
    ax.set_xticks(x); ax.set_xticklabels(months,family=F,fontsize=9,color=INK); ax.set_xlim(-0.6,5.6)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    yax=1-ease((t-14.2)/0.4)
    ax.spines["left"].set_color("#bfbfbf"); ax.spines["left"].set_alpha(yax); ax.spines["bottom"].set_color("#cfd5dd")
    ax.tick_params(length=0); ax.tick_params(axis="y",colors=mix("white","#595959",yax),labelsize=8.5)
    if grid>0: ax.grid(axis="y",color="#d9d9d9",lw=1,alpha=grid); ax.set_axisbelow(True)
    if leg>0:
        lx=0.2
        for c in data:
            fig.text(lx,fy(965),"■ "+c,fontsize=8.5,color=DEF[c],alpha=leg); lx+=0.17
    if ctit>0:
        fig.text(0.46,fy(390),"Chart Title",ha="center",va="center",fontsize=14,color="#595959",alpha=ctit)
        if 12.9<t<13.4: q=ease((t-12.9)/0.3); fig.add_artist(plt.Line2D([0.36,0.36+0.2*q],[fy(390),fy(390)],color=RED,lw=3))
    if 4.0<t<6.5:
        a=back((t-4.0)/0.35)
        if a>0.05: fig.text(0.5,fy(462),"\"Dubai is the biggest. Done!\"",ha="center",va="center",fontsize=13*a,family=F,fontweight="bold",color=MUT)
    if 6.7<t<9.5:
        q="Where is growth coming from?"; n=int(len(q)*cl((t-6.8)/1.4))
        fig.text(0.5,fy(462),q[:n],ha="center",va="center",fontsize=14,family=F,fontweight="bold",color=RED)
    if 14.4<t<20.6:
        fig.text(0.1,fy(462),"Growth since January (Jan = 100)",fontsize=10,family=F,color=MUT,alpha=ease((t-14.6)/0.4))
    if t>=20.7:
        L1,L2="Sharjah orders grew 70% in 6 months,","faster than every other city"
        n=int((len(L1)+len(L2))*cl((t-20.8)/2.4)); a1,a2=L1[:n],L2[:max(0,n-len(L1))]
        fig.text(0.1,fy(375),a1,fontsize=15,family=F,fontweight="bold",color=INK,va="center")
        if a2: fig.text(0.1,fy(415),a2,fontsize=15,family=F,fontweight="bold",color=RED,va="center")
        fig.text(0.1,fy(452),"Order growth since January (Jan = 100)",fontsize=9.5,family=F,color=MUT,alpha=ease((t-23.0)/0.4),va="center")
# zoom keyframes: (start,end, cx,cy (px), scale)
ZOOMS=[(9.6,11.2,430,740,1.7),(11.2,12.7,540,955,1.8),(12.7,14.0,500,390,1.8),(17.6,19.8,860,690,1.7),(20.6,23.6,420,400,1.5)]
def zoomparams(t):
    for a,b,cx,cy,s in ZOOMS:
        if a<=t<=b:
            r=min(ease((t-a)/0.45),ease((b-t)/0.45)); return cx,cy,1+(s-1)*r
    return W/2,H/2,1.0
def frame(t):
    draw(t); fig.canvas.draw()
    img=Image.frombuffer("RGBA",(W*S,H*S),bytes(fig.canvas.buffer_rgba())).convert("RGB")
    cx,cy,z=zoomparams(t)
    if z>1.001:
        w,h=W*S/z,H*S/z; x0=min(max(cx*S-w/2,0),W*S-w); y0=min(max(cy*S-h/2,0),H*S-h)
        img=img.crop((int(x0),int(y0),int(x0+w),int(y0+h)))
    return img.resize((W,H),Image.LANCZOS)
if sys.argv[1:]==["still"]:
    ts=[1.8,4.5,8,10.5,12,13.2,16.5,18.7,22,26]; ims=[frame(t).resize((270,250)) for t in ts]
    o=Image.new("RGB",(5*280,2*260),"black")
    for k,im in enumerate(ims): o.paste(im,((k%5)*280,(k//5)*260))
    o.save("vsheet.png"); sys.exit()
p=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","v.mp4"],stdin=subprocess.PIPE)
for i in range(int(DUR*FPS)): p.stdin.write(frame(i/FPS).tobytes())
p.stdin.close(); p.wait(); print("ok")

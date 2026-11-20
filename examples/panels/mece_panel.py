import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as P, subprocess, sys
from PIL import Image
W,H=1080,1000; S=2; FPS=30; DUR=40.0
F="Poppins"; NAVY,RED,INK,MUT,GREY="#0b3d91","#e8392b","#1c2433","#7a8494","#c9ced6"
def cl(x): return float(np.clip(x,0,1))
def ease(x): x=cl(x); return x*x*(3-2*x)
def back(x):
    x=cl(x); c1=1.70158; c3=c1+1; return 1+c3*(x-1)**3+c1*(x-1)**2
STEPS=[(0,"The problem",MUT),(3.2,"What most people do",MUT),(13.0,"What consultants do: MECE",RED),(19.0,"Break it down",RED),(25.5,"Check each box",RED),(31.0,"The answer",NAVY),(36.0,"No overlaps. No gaps.",NAVY)]
fig=plt.figure(figsize=(W/100,H/100),dpi=100*S,facecolor="white")
ax=fig.add_axes([0,0,1,1]); 
def T(x,y,s,**k): ax.text(x,y,s,family=F,**k)
def box(cx,cy,name,val,col,a,fill="white",lw=2):
    if a<=0.01: return
    sc=0.85+0.15*back(a)
    w,h=250*sc,112*sc
    ax.add_patch(P.FancyBboxPatch((cx-w/2,cy-h/2),w,h,boxstyle="round,pad=0,rounding_size=14",fc=fill,ec=col,lw=lw,alpha=a,zorder=5))
    T(cx,cy-18,name,ha="center",va="center",fontsize=15,color=INK,alpha=a,zorder=6)
    T(cx,cy+22,val,ha="center",va="center",fontsize=25,fontweight="bold",color=col if col!=GREY else MUT,alpha=a,zorder=6)
def link(x0,y0,x1,y1,col,p,lw=2.5):
    if p<=0: return
    xm=(x0+x1)/2; pts=np.array([[x0,y0],[xm,y0],[xm,y1],[x1,y1]])
    seg=np.linalg.norm(np.diff(pts,axis=0),axis=1); L=seg.sum()*p; out=[pts[0]]
    for i,sg in enumerate(seg):
        if L>=sg: out.append(pts[i+1]); L-=sg
        else: out.append(pts[i]+(pts[i+1]-pts[i])*L/sg); break
    o=np.array(out); ax.plot(o[:,0],o[:,1],color=col,lw=lw,solid_capstyle="round",zorder=3)
def typed(s,t0,dur,t): return s[:int(len(s)*cl((t-t0)/dur))]
notes=[("App is slow",210,480,-4),("Fewer iPhone\nusers",560,470,3),("Ramadan",880,500,-3),("Customers\norder less",260,680,2),("Fewer orders",620,660,-2),("Competitor\ndiscounts",880,720,4),("Bad weather",450,850,-3)]
def draw(t):
    ax.cla(); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    for x in range(0,W,60): ax.plot([x,x],[0,H],color="#f2f3f6",lw=0.9,zorder=0)
    for y in range(0,H,60): ax.plot([0,W],[y,y],color="#f2f3f6",lw=0.9,zorder=0)
    k=max(i for i,(st,_,_) in enumerate(STEPS) if t>=st); st,lab,col=STEPS[k]; sc=back((t-st)/0.35)
    if sc>0.05: T(W/2,300,lab,ha="center",va="center",fontsize=17*sc,fontweight="bold",color="white",bbox=dict(boxstyle="round,pad=0.55",fc=col,ec="none"),zorder=9)
    # question
    if t<13.2:
        a=1-ease((t-12.6)/0.5)
        q=typed("Revenue dropped 8%. Why?",0.4,1.6,t)
        T(W/2,365,q,ha="center",va="center",fontsize=26,fontweight="bold",color=INK,alpha=a)
    # sticky notes
    if 3.4<t<13.2:
        fa=1-ease((t-12.6)/0.5)
        for i,(s,x,y,r) in enumerate(notes):
            a=back((t-3.6-i*0.55)/0.35)*fa
            if a>0.05: T(x,y,s,ha="center",va="center",fontsize=17*min(a,1.05),color=INK,rotation=r,linespacing=1.1,alpha=min(fa,1),zorder=4,
                         bbox=dict(boxstyle="round,pad=0.7",fc="#fff4c2",ec="#f0dc8a",lw=1.2,alpha=min(fa,1)))
        # overlaps
        if t>8.0:
            p=ease((t-8.0)/0.6)*fa
            for (x0,y0,x1,y1) in [(260,680,620,660),(620,660,560,470)]:
                ax.plot([x0,x0+(x1-x0)*p],[y0,y0+(y1-y0)*p],color=RED,lw=3,ls=(0,(4,3)),zorder=3,alpha=fa)
            T(440,585,"Overlap",ha="center",fontsize=16,fontweight="bold",color=RED,alpha=ease((t-8.5)/0.4)*fa,zorder=6,bbox=dict(fc="white",ec="none",pad=3,alpha=ease((t-8.5)/0.4)*fa))
        if t>9.6:
            a=back((t-9.6)/0.35)*fa
            if a>0.05: T(880,860,"What's missing?",ha="center",fontsize=16*min(a,1.05),fontweight="bold",color=RED,alpha=min(fa,1),zorder=6)
        if t>10.8:
            a=ease((t-10.8)/0.4)*fa
            T(W/2,965,"Overlaps. Gaps. Going in circles.",ha="center",va="center",fontsize=19,fontweight="bold",color=MUT,alpha=a)
    # MECE definition
    if 13.3<t<19.3:
        fa=1-ease((t-18.8)/0.5)
        rows=[("M","utually"),("E","xclusive"),("C","ollectively"),("E","xhaustive")]
        for i,(L,rest) in enumerate(rows):
            a=back((t-13.6-i*0.3)/0.35)*fa; y=420+i*80
            if a>0.05:
                T(250,y,L,ha="right",va="center",fontsize=46*min(a,1.05),fontweight="bold",color=RED,alpha=min(fa,1))
                T(255,y,rest,ha="left",va="center",fontsize=40,fontweight="bold",color=INK,alpha=min(fa,1)*cl(a))
        a1=ease((t-15.6)/0.4)*fa; a2=ease((t-16.8)/0.4)*fa
        T(640,460,"No overlaps",ha="left",va="center",fontsize=22,color=MUT,alpha=a1); ax.plot([600,620],[460,460],color=GREY,lw=2,alpha=a1)
        T(640,620,"No gaps",ha="left",va="center",fontsize=22,color=MUT,alpha=a2); ax.plot([600,620],[620,620],color=GREY,lw=2,alpha=a2)
        if a1>0: ax.plot([600,600],[420,500],color=GREY,lw=2,alpha=a1)
        if a2>0: ax.plot([600,600],[580,660],color=GREY,lw=2,alpha=a2)
    # TREE
    if t>=19.2:
        R=(170,650); O=(540,520); A=(540,810); C=(900,430); Fq=(900,640)
        chk=lambda t0: ease((t-t0)/0.4)
        redp= t>=29.0
        box(*R,"Revenue","−8%",RED,ease((t-19.3)/0.4),fill="#fdecea" if redp else "white",lw=3 if redp else 2)
        link(R[0]+125,R[1],O[0]-125,O[1],RED if redp else GREY,ease((t-20.2)/0.6),4 if redp else 2.5)
        link(R[0]+125,R[1],A[0]-125,A[1],GREY,ease((t-20.2)/0.6))
        oval="−10%" if t>=26.0 else "?"; ocol=RED if t>=26.0 else GREY
        box(*O,"Orders",oval,ocol,ease((t-20.7)/0.4),fill="#fdecea" if redp else "white",lw=3 if redp else 2)
        aval="+2%" if t>=26.8 else "?"
        box(*A,"Avg order value",aval,GREY,ease((t-21.0)/0.4))
        if t>21.4: T(540,665,"×",ha="center",va="center",fontsize=30,color=MUT,alpha=ease((t-21.4)/0.3))
        link(O[0]+125,O[1],C[0]-125,C[1],GREY,ease((t-22.6)/0.6))
        link(O[0]+125,O[1],Fq[0]-125,Fq[1],RED if redp else GREY,ease((t-22.6)/0.6),4 if redp else 2.5)
        cval="−1%" if t>=27.6 else "?"
        box(*C,"Customers",cval,GREY,ease((t-23.1)/0.4))
        fval="−9%" if t>=28.4 else "?"; fcol=RED if t>=28.4 else GREY
        box(*Fq,"Orders per\ncustomer" if False else "How often they order",fval,fcol,ease((t-23.4)/0.4),fill="#fdecea" if redp else "white",lw=3 if redp else 2)
        if t>23.8: T(900,535,"×",ha="center",va="center",fontsize=30,color=MUT,alpha=ease((t-23.8)/0.3))
        if t>=19.5 and t<25.5:
            T(60,385,typed("Revenue = Orders × Avg order value",19.6,2.2,t),ha="left",fontsize=15,color=MUT)
            T(60,420,typed("Orders = Customers × How often they order",22.4,2.4,t),ha="left",fontsize=15,color=MUT)
        if t>=29.3:
            a=back((t-29.3)/0.35)
            if a>0.05: T(900,735,"The problem is here",ha="center",va="center",fontsize=17*min(a,1.05),fontweight="bold",color=RED,zorder=7)
        if t>=31.0:
            L1="Revenue fell because customers order less often,"; L2="not because we lost them"
            n=int((len(L1)+len(L2))*cl((t-31.1)/3.0))
            T(60,920,L1[:n],ha="left",va="center",fontsize=19,fontweight="bold",color=INK,zorder=8)
            if n>len(L1): T(60,962,L2[:n-len(L1)],ha="left",va="center",fontsize=19,fontweight="bold",color=RED,zorder=8)
def frame(t):
    draw(t); fig.canvas.draw()
    return Image.frombuffer("RGBA",(W*S,H*S),bytes(fig.canvas.buffer_rgba())).convert("RGB").resize((W,H),Image.LANCZOS)
if sys.argv[1:]==["still"]:
    ts=[2,7,10.5,12,16,18,22,24.5,28.5,30,34,38]; ims=[frame(t).resize((360,333)) for t in ts]
    o=Image.new("RGB",(4*365,3*338),"black")
    for k,im in enumerate(ims): o.paste(im,((k%4)*365,(k//4)*338))
    o.save("sheet.png"); sys.exit()
p=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","slow","-crf","14","-pix_fmt","yuv420p","v.mp4"],stdin=subprocess.PIPE)
for i in range(int(DUR*FPS)): p.stdin.write(frame(i/FPS).tobytes())
p.stdin.close(); p.wait(); print("ok")

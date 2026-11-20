import numpy as np, matplotlib.pyplot as plt, subprocess, sys
W,H=1080,1000; FPS=30; DUR=34.0
cats=["Cold\nfood","App\ncrash","Late\ndelivery","Other","Wrong\norder","Payment\nissue","Missing\nitems","Rude\nrider"]
vals=np.array([260,20,420,10,190,30,70,15]); order=np.argsort(-vals,kind="stable"); rank=np.empty(8,int); rank[order]=np.arange(8)
cum=np.cumsum(vals[order])/vals.sum()*100
BLUE,GREY,HL,INK,MUT,RED,GOLD="#4472c4","#c9ced6","#0b3d91","#1c2433","#7a8494","#e8392b","#f5b800"
F="Poppins"; S=4.6
def cl(x): return float(np.clip(x,0,1))
def ease(x): x=cl(x); return x*x*(3-2*x)
def back(x):
    x=cl(x); c1=1.70158; c3=c1+1; return 1+c3*(x-1)**3+c1*(x-1)**2
def mix(a,b,t):
    a=np.array(plt.matplotlib.colors.to_rgb(a)); b=np.array(plt.matplotlib.colors.to_rgb(b)); return tuple(a+(b-a)*t)
STEPS=[(0,"Before: the usual chart"),(7.3,"1. Remove the clutter"),(10.1,"2. Sort, biggest first"),(11.9,"3. Add the cumulative %"),
       (15.65,"4. Draw the 80% line"),(20.1,"5. Highlight the vital few"),(23.0,"6. Title = the answer"),(30.05,"It's a Pareto chart")]
L1,L2="3 issues cause 86% of complaints.","Fix late delivery first."
fig=plt.figure(figsize=(W/180,H/180),dpi=180,facecolor="white")
def fy(px): return 1-px/H
def frame(t):
    fig.clf()
    bg=fig.add_axes([0,0,1,1]); bg.set_xlim(0,W); bg.set_ylim(0,H); bg.axis("off")
    for x in range(0,W,70): bg.plot([x,x],[0,H],color="#f1f2f5",lw=0.8)
    for y in range(0,H,70): bg.plot([0,W],[y,y],color="#f1f2f5",lw=0.8)
    k=max(i for i,(st,_) in enumerate(STEPS) if t>=st); st,lab=STEPS[k]; sc=back((t-st)/0.35)
    if sc>0.05: fig.text(0.5,fy(305),lab,ha="center",va="center",fontsize=11*sc,color="white",fontweight="bold",family=F,
                        bbox=dict(boxstyle="round,pad=0.5",fc=MUT if k==0 else (HL if k==7 else RED),ec="none"))
    ax=fig.add_axes([0.1,0.115,0.84,0.38])
    grow=ease((t-0.2)/1.2); grid=1-ease((t-7.7)/0.4); leg=1-ease((t-8.5)/0.4); ctit=1-ease((t-9.3)/0.4)
    sp=ease((t-10.7)/1.0); yax=1-ease((t-20.2)/0.4)
    xs=[(1-sp)*i+sp*rank[i] for i in range(8)]
    for i in range(8):
        hp=ease((t-20.3-0.12*rank[i])/0.3); col=mix(BLUE, HL if rank[i]<3 else GREY, hp)
        a=1.0
        if rank[i]>=3 and 21.7<t<23.0: a=1-0.6*np.sin((t-21.7)/1.3*np.pi)
        ax.bar(xs[i],vals[i]*grow,0.66*(1-0.45*np.sin(np.pi*sp)),color=col,zorder=3,alpha=a)
        lb=back((t-20.3-0.1*rank[i])/0.3)
        if lb>0.05:
            if rank[i]<3: ax.text(xs[i],18,f"{vals[i]}",ha="center",va="bottom",fontsize=10.5*lb,family=F,fontweight="bold",color="white",zorder=8)
            else: ax.text(xs[i],vals[i]+8,f"{vals[i]}",ha="center",va="bottom",fontsize=9.5*lb,family=F,fontweight="bold",color=MUT,zorder=8)
    ax.set_xticks(xs); ax.set_xticklabels(cats,family=F,fontsize=8.5,color=INK,alpha=1-np.sin(np.pi*sp)*0.9)
    ax.set_xlim(-0.6,7.6); ax.set_ylim(0,500)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#bfbfbf"); ax.spines["left"].set_alpha(yax); ax.spines["bottom"].set_color("#cfd5dd")
    ax.tick_params(length=0,axis="x"); ax.tick_params(axis="y",colors=mix("white","#595959",yax),labelsize=9,length=0)
    if yax<=0: ax.set_yticks([])
    # cumulative line: first 3 points by 14.9, rest by 15.5
    n = 2*ease((t-12.1)/2.8) + 5*ease((t-14.9)/0.6)
    if n>0:
        xx=np.linspace(0,n,80); yy=np.interp(xx,np.arange(8),cum*S)
        ax.plot(xx,yy,color=RED,lw=2.4,zorder=5)
        tj=[12.1,13.5,14.9,0,0,0,0,15.5]
        for j in range(8):
            if j<=n+1e-6:
                ax.scatter([j],[cum[j]*S],s=34,color=RED,edgecolor="white",linewidth=1.5,zorder=6)
                if j in (0,1,2,7):
                    a=back((t-tj[j])/0.3)
                    if a>0.05: ax.text(j-0.12 if j else j+0.12,cum[j]*S+24,f"{cum[j]:.0f}%",ha="right" if j else "left",fontsize=(12 if j==2 else 10)*a,family=F,fontweight="bold",color=RED,zorder=7,bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="none",alpha=0.95))
    p80=ease((t-15.8)/0.8)
    if p80>0:
        ax.plot([-0.5,-0.5+8.0*p80],[80*S,80*S],color=GOLD,lw=2,ls=(0,(4,3)),zorder=4)
        if p80>0.9: ax.text(7.55,80*S+8,"80%",ha="right",fontsize=10,family=F,fontweight="bold",color="#c99600")
    bp=ease((t-21.0)/0.5)
    if bp>0:
        y=478; xe=-0.33+2.66*bp
        ax.plot([-0.33,-0.33,xe]+([xe] if bp>0.99 else []),[y-15,y,y]+([y-15] if bp>0.99 else []),color=HL,lw=2,clip_on=False)
        if bp>0.99: ax.text(1,y+8,"the vital few: 3 of 8 issues",ha="center",fontsize=10,family=F,fontweight="bold",color=HL,clip_on=False)
    if grid>0: ax.grid(True,axis="y",color="#d9d9d9",lw=1,alpha=grid); ax.set_axisbelow(True)
    if leg>0: fig.text(0.52,fy(985)-(1-leg)*0.03,"■ Series1",ha="center",fontsize=9,color=BLUE,alpha=leg)
    if ctit>0:
        fig.text(0.52,fy(378)+(1-ctit)*0.03,"Chart Title",ha="center",va="center",fontsize=15,color="#595959",alpha=ctit)
        if 9.3<t<9.8: q=ease((t-9.3)/0.25); fig.add_artist(plt.Line2D([0.4,0.4+0.24*q],[fy(378),fy(378)],color=RED,lw=3,alpha=ctit))
    ot=ease((t-9.7)/0.4)*(1-ease((t-23.3)/0.3))
    if ot>0: fig.text(0.1,fy(378),"Customer complaints by reason",va="center",fontsize=15,family=F,fontweight="bold",color=INK,alpha=ot)
    def typed(txt,a,b):
        if t<a: return ""
        return txt[:int(len(txt)*cl((t-a)/(b-a)))]
    s1=typed(L1,25.85,28.4); s2=typed(L2,28.66,29.9)
    cur="|" if int(t*3)%2==0 and t<29.9 and t>25.85 else ""
    if s1: fig.text(0.1,fy(372),s1+(cur if not s2 else ""),fontsize=16,family=F,fontweight="bold",color=INK,va="center")
    if s2: fig.text(0.1,fy(416),s2+cur,fontsize=16,family=F,fontweight="bold",color=HL,va="center")
    s3=ease((t-30.2)/0.5)
    if s3>0:
        fig.text(0.1,fy(456)-0.02*(1-s3),"Number of complaints by reason, with cumulative %",fontsize=9.5,family=F,color=MUT,alpha=s3,va="center")
        fig.text(0.1,fy(985)-0.02*(1-s3),"Source: illustrative data  |  @heytheanalyst",fontsize=8.5,family=F,color=MUT,alpha=s3)
    fig.canvas.draw(); return bytes(fig.canvas.buffer_rgba())
if sys.argv[1:]==["still"]:
    from PIL import Image
    ims=[]
    for t in [3,8.8,11.5,15.2,18,22,27.5,32]:
        frame(t); ims.append(Image.frombuffer("RGBA",(W,H),bytes(fig.canvas.buffer_rgba())).convert("RGB").resize((270,250)))
    o=Image.new("RGB",(4*280,2*260),"black")
    for k,im in enumerate(ims): o.paste(im,((k%4)*280,(k//4)*260))
    o.save("sheet.png"); sys.exit()
p=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
   "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","panel.mp4"],stdin=subprocess.PIPE)
for f in range(int(DUR*FPS)): p.stdin.write(frame(f/FPS))
p.stdin.close(); p.wait(); print("panel ok")

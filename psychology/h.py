import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as P
F="Poppins"; RED="#e8392b"; INK="#1c2433"; MUT="#7a8494"; NAVY="#0b3d91"; GREY="#b4bbc6"
def fig(title,sub,foot=None):
    f=plt.figure(figsize=(6,7.5),dpi=300,facecolor="white")
    f.text(0.07,0.93,title,fontsize=19,family=F,fontweight="bold",color=INK,va="top")
    f.text(0.07,0.865,sub,fontsize=10.5,family=F,color=MUT,va="top",linespacing=1.4)
    if foot: f.text(0.07,0.06,foot,fontsize=10,family=F,color=MUT,linespacing=1.4)
    return f
def lab(ax,t,c=MUT,b=False): ax.set_title(t,family=F,fontsize=11,fontweight="bold" if b else "normal",color=c,pad=10)
def clean(ax):
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#cfd5dd"); ax.spines["bottom"].set_color("#cfd5dd"); ax.tick_params(colors=MUT,labelsize=8,length=0)
# 1 proportional ink
f=fig("Proportional ink","Same two numbers: 100 vs 105.\nCut the axis, and a 5% gap looks like double.","Bars must start at 0. Ink should match the value.")
for k,(lo,t,c) in enumerate([(95,"Axis starts at 95",RED),(0,"Axis starts at 0",NAVY)]):
    ax=f.add_axes([0.1+k*0.46,0.17,0.36,0.55]); ax.bar(["A","B"],[100,105],color=[GREY,c],width=0.6); ax.set_ylim(lo,107); clean(ax)
    for tl in ax.get_xticklabels(): tl.set_family(F)
    lab(ax,t,c,True)
f.savefig("h1_proportional_ink.png",facecolor="white"); plt.close(f)
# 2 lie factor
f=fig("Lie factor","How much bigger the change looks ÷ how big it really is.\nAnything far from 1 is a distortion.")
ax=f.add_axes([0.07,0.12,0.86,0.66]); ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis("off")
ax.add_patch(P.Rectangle((1.2,1),1.4,2.5,fc=GREY)); ax.add_patch(P.Rectangle((3.2,1),1.4,5,fc=RED))
ax.text(2.9,0.4,"Bar B looks 2× taller",ha="center",family=F,fontsize=10,color=INK)
ax.text(7.3,6.2,"Visual change: +100%",ha="center",family=F,fontsize=12,color=INK)
ax.text(7.3,5.3,"Real change: +5%",ha="center",family=F,fontsize=12,color=INK)
ax.plot([5.6,9.0],[4.7,4.7],color=INK,lw=1.2)
ax.text(7.3,3.6,"Lie factor = 20",ha="center",family=F,fontsize=20,fontweight="bold",color=RED)
ax.text(7.3,2.6,"(Edward Tufte)",ha="center",family=F,fontsize=9.5,color=MUT)
f.savefig("h2_lie_factor.png",facecolor="white"); plt.close(f)
# 3 3D pie
f=fig("3D distortion","All four slices are exactly 25%.\nThe front one looks the biggest, only because it's closer.","Flatten it. 2D shows the true sizes.")
cols=[RED,"#4472c4","#a5a5a5","#ffc000"]; dark=["#a3261c","#2f5597","#7a7a7a","#bf9000"]
ax=f.add_axes([0.05,0.4,0.9,0.42]); ax.set_xlim(-1.3,1.3); ax.set_ylim(-0.9,0.7); ax.axis("off"); ax.set_aspect("equal")
sy=0.42; depth=0.22; ang=[225,315,45,135]   # front slice centred at 270
for d in np.linspace(depth,0,14):
    for k,a0 in enumerate(ang):
        th=np.radians(np.linspace(a0,a0+90,40)); xs=np.concatenate([[0],np.cos(th),[0]]); ys=np.concatenate([[0],np.sin(th)*sy,[0]])-d
        ax.fill(xs*1.0,ys,color=dark[k],lw=0)
for k,a0 in enumerate(ang):
    th=np.radians(np.linspace(a0,a0+90,40)); xs=np.concatenate([[0],np.cos(th),[0]]); ys=np.concatenate([[0],np.sin(th)*sy,[0]])
    ax.fill(xs,ys,color=cols[k],ec="white",lw=1)
ax2=f.add_axes([0.3,0.1,0.4,0.28]); ax2.pie([25]*4,colors=[RED,"#4472c4","#a5a5a5","#ffc000"],startangle=225,counterclock=False,wedgeprops=dict(ec="white",lw=1.5)); ax2.set_aspect("equal")
f.text(0.5,0.415,"Same data in 2D: four equal slices",ha="center",family=F,fontsize=10,color=INK)
f.savefig("h3_3d_distortion.png",facecolor="white"); plt.close(f)
# 4 dual axis
f=fig("Dual-axis illusion","Same two lines, same data. Only the right axis changed.\nLeft: ad spend grows slowly. Right: it 'overtakes' sales.","Two scales let you make any two lines look related.")
m=np.arange(12); sales=100+m*3; ads=20+m*1.5
for k,(lo,hi,t) in enumerate([(0,60,"Right axis 0–60"),(18,40,"Right axis 18–40")]):
    ax=f.add_axes([0.1+k*0.47,0.18,0.33,0.52]); ax.plot(m,sales,color=NAVY,lw=2.5); ax.set_ylim(80,150); clean(ax); ax.set_xticks([])
    a2=ax.twinx(); a2.plot(m,ads,color=RED,lw=2.5); a2.set_ylim(lo,hi); a2.tick_params(colors=RED,labelsize=8,length=0)
    for s in ["top","left","bottom"]: a2.spines[s].set_visible(False)
    a2.spines["right"].set_color(RED); lab(ax,t,INK,True)
f.text(0.1,0.13,"— Sales (left)",color=NAVY,family=F,fontsize=10); f.text(0.4,0.13,"— Ad spend (right)",color=RED,family=F,fontsize=10)
f.savefig("h4_dual_axis.png",facecolor="white"); plt.close(f)
# 5 aspect ratio
f=fig("Aspect ratio","Same line, same numbers.\nSquash it and growth looks flat. Stretch it and it looks explosive.","Pick a shape where the slope is around 45°.")
y=100+np.cumsum(np.r_[0,np.full(11,2.0)])+np.array([0,1,-1,2,0,1,3,2,4,3,5,6])
for (rect,t) in [([0.1,0.6,0.8,0.1],"Squashed: 'flat'"),([0.1,0.15,0.3,0.36],"Stretched: 'booming'"),([0.55,0.22,0.36,0.24],"About 45°: honest")]:
    ax=f.add_axes(rect); ax.plot(y,color=RED if "boom" in t else (MUT if "flat" in t else NAVY),lw=2.5); ax.set_xticks([]); ax.set_yticks([]); clean(ax)
    ax.set_title(t,family=F,fontsize=10.5,fontweight="bold",color=INK,pad=6,loc="left")
f.savefig("h5_aspect_ratio.png",facecolor="white"); plt.close(f)

import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as P
F="Poppins"; RED="#e8392b"; INK="#1c2433"; MUT="#7a8494"; NAVY="#0b3d91"; GREY="#c9ced6"
def fig(title,sub):
    f=plt.figure(figsize=(6,7.5),dpi=300,facecolor="white")
    f.text(0.07,0.93,title,fontsize=19,family=F,fontweight="bold",color=INK,va="top")
    f.text(0.07,0.865,sub,fontsize=10.5,family=F,color=MUT,va="top",linespacing=1.4)
    return f
# 1 preattentive
rng=np.random.default_rng(7); digits=rng.integers(0,10,(10,10)); digits[digits==3]=8
for (r,c) in [(1,2),(2,7),(4,4),(6,1),(7,8),(8,5),(3,9)]: digits[r,c]=3
f=fig("Pre-attentive attributes","How many 3s? Left: you have to search.\nRight: colour finds them before you think.")
for k,hl in enumerate([False,True]):
    ax=f.add_axes([0.05+k*0.47,0.17,0.43,0.6]); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    for r in range(10):
        for c in range(10):
            d=digits[r,c]; red=hl and d==3
            ax.text(c+0.5,9.5-r,str(d),ha="center",va="center",family=F,fontsize=11,fontweight="bold" if red else "normal",color=RED if red else "#555b66")
    ax.text(5,-0.6,"Search: slow" if not hl else "Pop-out: instant",ha="center",family=F,fontsize=11,fontweight="bold",color=MUT if not hl else RED)
f.savefig("1_preattentive.png",facecolor="white"); plt.close(f)
# 2 accuracy ranking
vals=[30,22]
f=fig("Accuracy ranking","Same two values (30 vs 22) in five encodings.\nTop is easiest to compare, bottom is hardest.")
names=["Position","Length","Angle","Area","Colour"]
for i,n in enumerate(names):
    y0=0.68-i*0.13; f.text(0.07,y0+0.045,f"{i+1}. {n}",family=F,fontsize=12,fontweight="bold",color=RED if i<2 else INK)
    ax=f.add_axes([0.42,y0,0.5,0.1]); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,1)
    if n=="Position":
        ax.plot([1,9],[0.1,0.1],color=GREY,lw=1); 
        for x,v in zip([3,7],vals): ax.scatter(x,0.1+v/35,s=60,color=NAVY,zorder=3); ax.plot([x,x],[0.1,0.1+v/35],color="#e6e9ee",lw=1)
    if n=="Length":
        for x,v in zip([3,7],vals): ax.add_patch(P.Rectangle((x-0.6,0.05),1.2,v/35,fc=NAVY))
    if n=="Angle":
        for x,v in zip([3,7],vals):
            ax.add_patch(P.Wedge((x,0.45),0.42,90,90+v*6,fc=NAVY,transform=ax.transData)); ax.add_patch(P.Wedge((x,0.45),0.42,90+v*6,450,fc="#e6e9ee"))
        ax.set_aspect("equal",adjustable="datalim")
    if n=="Area":
        for x,v in zip([3,7],vals): ax.add_patch(P.Circle((x,0.45),np.sqrt(v)/12,fc=NAVY))
        ax.set_aspect("equal",adjustable="datalim")
    if n=="Colour":
        cm=plt.matplotlib.colors.LinearSegmentedColormap.from_list("n",["#eef2f8",NAVY])
        for x,v in zip([3,7],vals): ax.add_patch(P.Rectangle((x-0.6,0.15),1.2,0.7,fc=cm(v/35)))
f.text(0.07,0.06,"Based on Cleveland & McGill (1984). That's why bars beat pies.",family=F,fontsize=9,color=MUT)
f.savefig("2_accuracy_ranking.png",facecolor="white"); plt.close(f)
# 3 stevens
f=fig("We underestimate area","The right circle has exactly 2× the area.\nMost people guess it's only about 1.5× bigger.")
ax=f.add_axes([0.08,0.2,0.84,0.55]); ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis("off"); ax.set_aspect("equal")
r1=1.6; r2=r1*np.sqrt(2)
ax.add_patch(P.Circle((3,3.5),r1,fc=NAVY)); ax.add_patch(P.Circle((7,3.5),r2,fc=RED))
ax.text(3,3.5-r2-0.6,"100",ha="center",family=F,fontsize=14,fontweight="bold",color=INK); ax.text(7,3.5-r2-0.6,"200",ha="center",family=F,fontsize=14,fontweight="bold",color=RED)
f.text(0.07,0.1,"Stevens' power law: area feels smaller than it is,\nso bubble charts understate big differences.",family=F,fontsize=10,color=MUT,linespacing=1.4)
f.savefig("3_area_underestimate.png",facecolor="white"); plt.close(f)
# 4 weber
f=fig("Weber's law","The same 2-unit difference.\nEasy to see when values are small, invisible when they're big.")
for k,(a,b,lab) in enumerate([(2,4,"2 vs 4"),(98,100,"98 vs 100")]):
    ax=f.add_axes([0.1+k*0.45,0.17,0.35,0.58]); ax.bar([0,1],[a,b],color=[NAVY,RED],width=0.6)
    ax.set_ylim(0,max(a,b)*1.12); ax.axis("off"); ax.set_xlim(-0.6,1.6)
    ax.text(0.5,-max(a,b)*0.08,lab,ha="center",family=F,fontsize=13,fontweight="bold",color=INK)
f.text(0.07,0.07,"Fix: show the change itself, not just the two totals.",family=F,fontsize=10,color=MUT)
f.savefig("4_webers_law.png",facecolor="white"); plt.close(f)
# 5 simultaneous contrast
f=fig("Simultaneous contrast","Both small squares are the exact same grey.\nThe background changes what your eye sees.")
ax=f.add_axes([0.07,0.17,0.86,0.58]); ax.set_xlim(0,10); ax.set_ylim(0,6.7); ax.axis("off")
ax.add_patch(P.Rectangle((0,0.6),4.8,5.5,fc="#1c2433")); ax.add_patch(P.Rectangle((5.2,0.6),4.8,5.5,fc="#eef0f3"))
for x in [2.4,7.6]: ax.add_patch(P.Rectangle((x-0.9,2.45),1.8,1.8,fc="#8a8f98"))
ax.text(5,0,"Same colour: #8A8F98",ha="center",family=F,fontsize=11,fontweight="bold",color=RED)
f.text(0.07,0.07,"In charts, the same colour can look different depending on what's around it.",family=F,fontsize=9.5,color=MUT)
f.savefig("5_simultaneous_contrast.png",facecolor="white"); plt.close(f)

# --- v2 of the accuracy-ranking image (bigger shapes, used in the final set) ---
f=plt.figure(figsize=(6,7.5),dpi=300,facecolor="white")
f.text(0.07,0.93,"Accuracy ranking",fontsize=19,family=F,fontweight="bold",color=INK,va="top")
f.text(0.07,0.865,"Same two values (30 vs 22) in five encodings.\nTop is easiest to compare, bottom is hardest.",fontsize=10.5,family=F,color=MUT,va="top",linespacing=1.4)
ax=f.add_axes([0.05,0.1,0.9,0.7]); ax.set_xlim(0,10); ax.set_ylim(0,10.5); ax.axis("off"); ax.set_aspect("equal")
vals=[30,22]; xs=[6.0,8.3]; cm=plt.matplotlib.colors.LinearSegmentedColormap.from_list("n",["#eef2f8",NAVY])
for i,n in enumerate(["Position","Length","Angle","Area","Colour"]):
    yc=9.2-i*2.1; ax.text(0.2,yc,f"{i+1}. {n}",family=F,fontsize=13,fontweight="bold",color=RED if i<2 else INK,va="center")
    for x,v in zip(xs,vals):
        if n=="Position": ax.plot([5,9.3],[yc-0.7]*2,color="#cfd5dd",lw=1); ax.scatter(x,yc-0.7+v/30*1.3,s=70,color=NAVY,zorder=3)
        elif n=="Length": ax.add_patch(P.Rectangle((x-0.35,yc-0.75),0.7,v/30*1.5,fc=NAVY))
        elif n=="Angle": ax.add_patch(P.Wedge((x,yc),0.75,90,450,fc="#e6e9ee")); ax.add_patch(P.Wedge((x,yc),0.75,90,90+v*360/80,fc=NAVY))
        elif n=="Area": ax.add_patch(P.Circle((x,yc),np.sqrt(v/30)*0.8,fc=NAVY))
        else: ax.add_patch(P.Rectangle((x-0.6,yc-0.6),1.2,1.2,fc=cm(0.35+v/30*0.65)))
f.text(0.07,0.06,"Based on Cleveland & McGill (1984). That's why bars beat pies.",family=F,fontsize=9,color=MUT)
f.savefig("2_accuracy_ranking.png",facecolor="white")

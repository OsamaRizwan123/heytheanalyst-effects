import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as P
F="Poppins"; RED="#e8392b"; INK="#1c2433"; MUT="#7a8494"; NAVY="#0b3d91"; GREY="#b4bbc6"
def fig(title,sub,foot=None):
    f=plt.figure(figsize=(6,7.5),dpi=300,facecolor="white")
    f.text(0.07,0.93,title,fontsize=19,family=F,fontweight="bold",color=INK,va="top")
    f.text(0.07,0.865,sub,fontsize=10.5,family=F,color=MUT,va="top",linespacing=1.4)
    if foot: f.text(0.07,0.06,foot,fontsize=10,family=F,color=MUT,linespacing=1.4)
    ax=f.add_axes([0.07,0.15,0.86,0.62]); ax.set_xlim(0,10); ax.set_ylim(0,7.2); ax.axis("off"); ax.set_aspect("equal")
    return f,ax
# circles: question + reveal
for k,rev in enumerate([False,True]):
    f=plt.figure(figsize=(6,7.5),dpi=300,facecolor="white")
    f.text(0.07,0.93,"How much bigger is the red one?" if not rev else "It's 4× bigger",fontsize=19,family=F,fontweight="bold",color=INK if not rev else RED,va="top")
    f.text(0.07,0.865,"Take a guess before you swipe." if not rev else "Most people guess about 2×. The red circle has exactly 4× the area.\nOur brain underestimates area, so bubble charts mislead.",fontsize=10.5,family=F,color=MUT,va="top",linespacing=1.4)
    ax=f.add_axes([0.07,0.15,0.86,0.62]); ax.set_xlim(0,10); ax.set_ylim(0,7.2); ax.axis("off"); ax.set_aspect("equal")
    r1=1.25; r2=2.5; ax.add_patch(P.Circle((2.4,3.6),r1,fc=NAVY)); ax.add_patch(P.Circle((6.9,3.6),r2,fc=RED))
    if rev:
        ax.text(2.4,3.6-r2-0.6,"1×",ha="center",family=F,fontsize=16,fontweight="bold",color=INK); ax.text(6.9,3.6-r2-0.6,"4×",ha="center",family=F,fontsize=16,fontweight="bold",color=RED)
    else:
        ax.text(2.4,3.6-r2-0.6,"1×",ha="center",family=F,fontsize=16,fontweight="bold",color=INK); ax.text(6.9,3.6-r2-0.6,"?",ha="center",family=F,fontsize=16,fontweight="bold",color=RED)
    f.savefig(f"3{'b_reveal' if rev else 'a_question'}_area.png",facecolor="white"); plt.close(f)
# proximity
f,ax=fig("Proximity","Same 18 dots. Spacing alone makes you see 3 groups.","In charts: put labels right next to the data,\nnot in a legend.")
for i in range(3):
    for j in range(6): ax.scatter(1.4+j*1.45,5.0+i*0.75,s=110,color=NAVY)
for g in range(3):
    for i in range(3):
        for j in range(2): ax.scatter(0.9+g*3.3+j*0.75,1.1+i*0.75,s=110,color=NAVY)
ax.text(5,4.3,"Even spacing: one block",ha="center",family=F,fontsize=10,color=MUT); ax.text(5,0.25,"Gaps: 3 groups",ha="center",family=F,fontsize=10,fontweight="bold",color=RED)
f.savefig("g1_proximity.png",facecolor="white"); plt.close(f)
# similarity
f,ax=fig("Similarity","Same grid. Colour alone makes you see rows instead of columns.","In charts: same colour = same category. Use it on purpose.")
for i in range(6):
    for j in range(6): ax.scatter(0.8+j*1.5,0.9+i*1.05,s=150,color=RED if i%2 else GREY)
f.savefig("g2_similarity.png",facecolor="white"); plt.close(f)
# enclosure
f,ax=fig("Enclosure","A shaded box instantly groups whatever is inside it.","In charts: shade the 'vital few',\nor the period you're talking about.")
rng=np.random.default_rng(4); pts=rng.uniform([0.5,0.6],[9.5,6.6],(22,2))
ax.add_patch(P.FancyBboxPatch((5.6,2.0),3.6,3.2,boxstyle="round,pad=0,rounding_size=0.4",fc="#fdecea",ec="none",zorder=0))
for x,y in pts: ax.scatter(x,y,s=110,color=NAVY,zorder=3)
f.savefig("g3_enclosure.png",facecolor="white"); plt.close(f)
# connection
f,ax=fig("Connection","A line beats colour. You see pairs,\neven though the colours don't match.","In charts: connected points read as one series,\nso only connect what belongs together.")
cols=[NAVY,RED]
for i in range(4):
    for j in range(3):
        x1,y=1.2+j*3.0,1.2+i*1.5; x2=x1+1.4
        ax.plot([x1,x2],[y,y],color=INK,lw=2,zorder=1)
        ax.scatter(x1,y,s=150,color=cols[(i+j)%2],zorder=3); ax.scatter(x2,y,s=150,color=cols[(i+j+1)%2],zorder=3)
f.savefig("g4_connection.png",facecolor="white"); plt.close(f)
# continuity
f,ax=fig("Continuity","You see two smooth lines crossing, not two V shapes touching.\nThe eye follows the smoothest path.","In charts: crossing lines confuse people.\nLabel them at the end, or split the chart.")
x=np.linspace(0.5,9.5,200); y1=1+5.5*(x-0.5)/9; y2=6.5-5.5*(x-0.5)/9
ax.plot(x,y1,color=NAVY,lw=4); ax.plot(x,y2,color=NAVY,lw=4)
f.savefig("g5_continuity.png",facecolor="white"); plt.close(f)
# figure-ground
f,ax=fig("Figure and ground","Grey falls into the background.\nThe one coloured line becomes 'the story'.","In charts: grey for context, one colour for the point you're making.")
rng=np.random.default_rng(2); xx=np.arange(12)
for k in range(7):
    y=3+np.cumsum(rng.normal(0,0.35,12)); ax.plot(0.5+xx*0.8,y,color=GREY,lw=1.8)
ax.plot(0.5+xx*0.8,1.2+xx*0.45,color=RED,lw=4)
f.savefig("g6_figure_ground.png",facecolor="white"); plt.close(f)

import numpy as np, matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
FONT="Patrick Hand"; RED="#c62828"; INK="#111111"; PINK="#f4c5c4"
fig=plt.figure(figsize=(6,10.6667),dpi=180,facecolor="white")
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,100); ax.set_ylim(0,177.8); ax.axis("off")
t1=ax.text(50,118,"Make charts like a ",fontsize=30,family=FONT,color=INK,ha="right",va="center")
fig.canvas.draw(); r=fig.canvas.get_renderer()
w1=t1.get_window_extent(r).width/1080*100; t1.remove()
w2=ax.text(0,0,"consultant",fontsize=30,family=FONT).get_window_extent(r).width/1080*100; ax.texts[-1].remove()
x0=50-(w1+w2)/2
ax.text(x0,118,"Make charts like a ",fontsize=30,family=FONT,color=INK,va="center")
ax.text(x0+w1,118,"consultant",fontsize=30,family=FONT,color=RED,va="center")
# chart area
L,R,B,T=15,88,58,102
ax.add_patch(plt.matplotlib.patches.FancyBboxPatch((L+1.2,B+0.3),3*8.6-1.2,T-B-0.8,boxstyle="round,pad=0,rounding_size=2",fc=PINK,ec="none",zorder=1))
vals=np.array([420,260,190,70,30,20,15,10]); bw=6.0; gap=8.6
H=(T-B-4)/470
for i,v in enumerate(vals):
    x=L+2.2+i*gap
    ax.add_patch(plt.Rectangle((x,B),bw,v*H,fc="white",ec=INK,lw=3,zorder=3))
cum=np.cumsum(vals)/vals.sum()
xs=np.array([L+2.2+i*gap+bw/2 for i in range(8)]); ys=B+cum*(T-B-2)
xx=np.linspace(xs[0],xs[-1],200); yy=make_interp_spline(xs,ys,k=2)(xx)
ax.plot(xx,yy,color=INK,lw=4,solid_capstyle="round",zorder=4)
ax.plot([L,R],[B+0.8*(T-B-2)]*2,color=RED,lw=2.5,ls=(0,(4,3)),zorder=2)
ax.text(R+0.5,B+0.8*(T-B-2),"80%",fontsize=15,family=FONT,color=RED,va="center")
ax.plot([L,L],[B,T+2],color="#444",lw=3.5,zorder=5); ax.plot([L,R+2],[B,B],color="#444",lw=3.5,zorder=5)
ax.text(50,24,"@heytheanalyst",fontsize=17,family=FONT,color=INK,ha="center")
fig.savefig("pareto_cover.jpg",facecolor="white",pil_kwargs={"quality":95})

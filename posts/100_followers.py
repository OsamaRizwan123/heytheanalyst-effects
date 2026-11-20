import numpy as np, matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
FONT="Patrick Hand"; RED="#c62828"; INK="#111"; PINK="#f4c5c4"
fig=plt.figure(figsize=(6,7.5),dpi=180,facecolor="white")
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,100); ax.set_ylim(0,125); ax.axis("off")
ax.text(50,108,"We just hit",fontsize=30,family=FONT,color=INK,ha="center",va="center")
ax.text(50,95,"100 followers",fontsize=40,family=FONT,color=RED,ha="center",va="center")
L,R,B,T=14,86,28,80
x=np.array([0,1,2,3,4,5,6]); y=np.array([2,8,15,35,55,78,100])
xs=L+3+x/6*(R-L-8); ys=B+y/100*(T-B-4)
xx=np.linspace(xs[0],xs[-1],200); yy=make_interp_spline(xs,ys,k=2)(xx)
ax.plot(xx,yy,color=INK,lw=4,solid_capstyle="round",zorder=4)
ty=B+(T-B-4)
ax.plot([L,R],[ty,ty],color=RED,lw=2.5,ls=(0,(4,3)),zorder=2)
ax.add_patch(plt.Circle((xs[-1],ty),1.8,fc=RED,ec="white",lw=2,zorder=7))
ax.text(xs[-1]-11,ty+3,"100 🎉".replace(" 🎉",""),fontsize=20,family=FONT,color=RED,ha="center")
ax.plot([L,L],[B,T+2],color="#444",lw=3.5); ax.plot([L,R+2],[B,B],color="#444",lw=3.5)
ax.text(50,17,"Thank you for following along.",fontsize=19,family=FONT,color=INK,ha="center")
ax.text(50,10,"So much more is coming.",fontsize=19,family=FONT,color=INK,ha="center")
ax.text(50,3.5,"@heytheanalyst",fontsize=15,family=FONT,color="#666",ha="center")
rng=np.random.default_rng(7)
def burst(cx,cy,r,col,n=12):
    for k in range(n):
        a=2*np.pi*k/n+rng.uniform(-0.1,0.1); r0=r*0.35; r1=r*rng.uniform(0.85,1.1)
        ax.plot([cx+r0*np.cos(a),cx+r1*np.cos(a)],[cy+r0*np.sin(a)*1.0,cy+r1*np.sin(a)*1.0],color=col,lw=2.6,solid_capstyle="round",zorder=6)
        ax.add_patch(plt.Circle((cx+(r1+1.2)*np.cos(a),cy+(r1+1.2)*np.sin(a)),0.45,color=col,zorder=6))
for cx,cy,r,c in [(xs[-1],ty,7,RED),(14,112,5,"#0b3d91"),(88,113,5.5,RED),(78,88,3.5,"#f5b800"),(22,92,3,"#f5b800")]:
    burst(cx,cy,r,c)
fig.savefig("100_followers.jpg",facecolor="white",pil_kwargs={"quality":95})

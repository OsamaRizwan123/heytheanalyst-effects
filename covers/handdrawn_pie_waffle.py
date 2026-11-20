import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as P
FONT="Patrick Hand"; RED="#c62828"; INK="#111111"; PINK="#f4c5c4"; GRN="#2e7d32"
fig=plt.figure(figsize=(6,10.6667),dpi=180,facecolor="white")
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,100); ax.set_ylim(0,177.8); ax.axis("off")
def two(y,a,b,fs):
    t=ax.text(0,0,a,fontsize=fs,family=FONT); fig.canvas.draw(); r=fig.canvas.get_renderer()
    w1=t.get_window_extent(r).width/1080*100; t.remove()
    t=ax.text(0,0,b,fontsize=fs,family=FONT); w2=t.get_window_extent(r).width/1080*100; t.remove()
    x0=50-(w1+w2)/2; ax.text(x0,y,a,fontsize=fs,family=FONT,color=INK,va="center"); ax.text(x0+w1,y,b,fontsize=fs,family=FONT,color=RED,va="center")
two(112,"Make charts like a ","consultant",30)
# left: pie sketch
cx,cy,r=27,84,15
ang=np.cumsum([0,60,50,70,45,55,80])
XL=["#4472c4","#ed7d31","#a5a5a5","#ffc000","#5b9bd5","#70ad47"]
for k in range(6): ax.add_patch(P.Wedge((cx,cy),r,90+ang[k],90+ang[k+1],fc=XL[k],ec="white",lw=1.5,zorder=3))
ax.add_patch(P.Circle((cx,cy),r,fc="none",ec=INK,lw=1.6,zorder=4))
ax.plot([cx-17,cx+17],[cy-17,cy+17],color=RED,lw=3.5,solid_capstyle="round",zorder=5); ax.plot([cx-17,cx+17],[cy+17,cy-17],color=RED,lw=3.5,solid_capstyle="round",zorder=5)
ax.text(cx,cy-25,"not this",fontsize=20,family=FONT,color=RED,ha="center")
# right: waffle sketch
x0,y0,s=60,70,4.4
for k in range(36):
    rr,cc=divmod(k,6); f=k<9
    ax.add_patch(P.FancyBboxPatch((x0+cc*s+0.4,y0+(5-rr)*s+0.4),s-0.8,s-0.8,boxstyle="round,pad=0,rounding_size=0.5",fc=RED if f else "white",ec=INK,lw=1.2,zorder=3))
ax.plot([x0+3,x0+9,x0+24],[y0-6,y0-11,y0-1],color=GRN,lw=0,zorder=5)
ax.text(x0+13.2,cy-25,"but this",fontsize=20,family=FONT,color=GRN,ha="center")
ax.annotate("",xy=(56,84),xytext=(45,84),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.8,mutation_scale=20))
ax.text(50,40,"6 charts. 20 seconds.",fontsize=19,family=FONT,color=INK,ha="center")
ax.text(50,24,"@heytheanalyst",fontsize=17,family=FONT,color=INK,ha="center")
fig.savefig("handdrawn_pie_waffle.jpg",facecolor="white",pil_kwargs={"quality":95})

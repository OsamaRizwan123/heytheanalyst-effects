exec(open('five.py').read().split("# 2 PIE")[0])
import matplotlib.patches as P
# PIE -> WAFFLE (before reused)
fig=new(); head(fig,False); title(fig,"Biryani is 1 in every 4 orders,","more than burgers and pizza","Share of food orders by cuisine, every square = 1%")
ax=fig.add_axes([0.12,0.12,0.76,0.6]); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off"); ax.set_aspect("equal")
for k in range(100):
    r,c=divmod(k,10); col=RED if k<26 else ("#9aa3b0" if k<43 else GREY)
    ax.add_patch(P.FancyBboxPatch((c+0.08,9-r+0.08),0.84,0.84,boxstyle="round,pad=0,rounding_size=0.12",fc=col,ec="none"))
for xx,lab,cc,bold in [(0.12,"Biryani 26%",RED,1),(0.42,"Burgers 17%","#9aa3b0",0),(0.70,"Others",GREY,0)]:
    fig.patches.append(P.FancyBboxPatch((xx,0.072),0.022,0.0176,boxstyle="round,pad=0,rounding_size=0.004",fc=cc,ec="none",transform=fig.transFigure,figure=fig))
    fig.text(xx+0.032,0.08,lab,va="center",fontsize=11 if bold else 10,family=F,fontweight="bold" if bold else "normal",color=RED if bold else MUT)
save(fig,"pie_a.png"); pair("pie")
# BAR -> DOT PLOT
areas=["Marina","Deira","JLT","Al Barsha","Downtown","Bur Dubai","JVC","Karama"]; t=np.array([29,33,27,31,30,34,41,32])
fig=new(); head(fig,False); title(fig,"JVC deliveries take the longest,","9 minutes slower than average","Average delivery time by area, minutes")
o=np.argsort(t); ax=fig.add_axes([0.22,0.1,0.58,0.64]); avg=t.mean()
ax.axvline(avg,color=INK,lw=1,ls=(0,(3,3)),zorder=1); ax.text(avg,8.15,f"City average {avg:.0f}",ha="center",family=F,fontsize=8.5,color=INK,bbox=dict(fc="white",ec="none",pad=2))
for k,i in enumerate(o):
    isJ=areas[i]=="JVC"; ax.plot([25,44],[k,k],color="#eef0f3",lw=1,zorder=0)
    ax.scatter(t[i],k,s=170 if isJ else 110,color=RED if isJ else "#9aa3b0",zorder=3,ec="white",lw=1.5)
    fig.text(0.9,0.1+0.64*(k+0.5)/8.6,f"{t[i]} min",va="center",family=F,fontsize=10,fontweight="bold" if isJ else "normal",color=RED if isJ else MUT) if False else ax.text(44.6,k,f"{t[i]} min",va="center",family=F,fontsize=10,fontweight="bold" if isJ else "normal",color=RED if isJ else MUT,clip_on=False)
ax.set_yticks(range(8)); ax.set_yticklabels([areas[i] for i in o],family=F,fontsize=10,color=INK)
ax.set_xlim(25,44); ax.set_ylim(-0.6,8.6); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ax.spines]; ax.tick_params(length=0)
save(fig,"bar_a.png"); pair("bar")
# TABLE -> HEATMAP
days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]; hrs=["12p","1p","2p","3p","4p","5p","6p","7p","8p","9p","10p","11p"]
h=np.arange(12); base=np.exp(-((h-1)/1.3)**2)*0.6+np.exp(-((h-8.6)/1.6)**2)
dm=np.array([0.75,0.72,0.78,0.95,1.25,1.1,0.85]); rng=np.random.default_rng(1)
Z=np.round((np.outer(dm,base)*400+80+rng.normal(0,12,(7,12)))).astype(int); Z[4,9]=Z.max()+35
fig=new(); head(fig,True); ax=fig.add_axes([0.1,0.2,0.86,0.6]); ax.axis("off")
tb=ax.table(cellText=Z.astype(str),rowLabels=days,colLabels=hrs,loc="center",cellLoc="center")
tb.auto_set_font_size(False); tb.set_fontsize(8); tb.scale(1,2.1)
for (r,c),cell in tb.get_celld().items(): cell.set_edgecolor("#bfbfbf"); cell.set_linewidth(0.6)
fig.text(0.5,0.84,"Orders by day and hour",ha="center",fontsize=13,color="#595959")
save(fig,"heat_b.png")
fig=new(); head(fig,False); title(fig,"Friday 9pm is the busiest hour,","plan riders around it","Orders by day and hour, darker = more orders")
ax=fig.add_axes([0.12,0.18,0.68,0.52]); cm=plt.matplotlib.colors.LinearSegmentedColormap.from_list("n",["#eef2f8","#0b3d91"])
for r in range(7):
    for c in range(12):
        ax.add_patch(P.Rectangle((c+0.04,6-r+0.04),0.92,0.92,fc=cm((Z[r,c]-Z.min())/(Z.max()-Z.min())),ec="none"))
ax.add_patch(P.Rectangle((9+0.02,2+0.02),0.96,0.96,fc="none",ec=RED,lw=3))
ax.annotate(f"{Z[4,9]} orders",xy=(10.0,2.5),xytext=(12.3,2.5),ha="left",va="center",family=F,fontsize=10,fontweight="bold",color=RED,arrowprops=dict(arrowstyle="-",color=RED,lw=1.5,shrinkA=2,shrinkB=0),annotation_clip=False)
ax.set_xlim(0,12); ax.set_ylim(-0.2,7.5); ax.axis("off")
for r,d in enumerate(days): ax.text(-0.2,6-r+0.5,d,ha="right",va="center",family=F,fontsize=9.5,color=RED if d=="Fri" else INK,fontweight="bold" if d=="Fri" else "normal")
for c,hh in enumerate(hrs):
    if c%3==0 or c==9: ax.text(c+0.5,7.15,hh,ha="center",family=F,fontsize=9,color=RED if c==9 else MUT,fontweight="bold" if c==9 else "normal")
save(fig,"heat_a.png"); pair("heat")

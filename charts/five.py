import numpy as np, matplotlib.pyplot as plt
from PIL import Image
F="Poppins"; RED="#e8392b"; INK="#1c2433"; MUT="#7a8494"; GREY="#c9ced6"; NAVY="#0b3d91"
XL=["#4472c4","#ed7d31","#a5a5a5","#ffc000","#5b9bd5","#70ad47","#264478","#9e480e"]
def head(fig,before):
    fig.text(0.5,0.96,"BEFORE" if before else "AFTER",ha="center",fontsize=16,family=F,fontweight="bold",color=MUT if before else RED)
def title(fig,l1,l2,sub):
    fig.text(0.07,0.885,l1,fontsize=14,family=F,fontweight="bold",color=INK)
    fig.text(0.07,0.845,l2,fontsize=14,family=F,fontweight="bold",color=RED)
    fig.text(0.07,0.81,sub,fontsize=8.5,family=F,color=MUT)
def clean(ax):
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#cfd5dd"); ax.tick_params(length=0)
def new(): return plt.figure(figsize=(7.5,6),dpi=400,facecolor="white")
def save(fig,n): fig.savefig(n,facecolor="white"); plt.close(fig)
def pair(n):
    a,b=Image.open(f"{n}_b.png"),Image.open(f"{n}_a.png"); o=Image.new("RGB",(a.width*2+40,a.height),"white")
    o.paste(a,(0,0)); o.paste(b,(a.width+40,0)); o.save(f"{n}.png")

# 2 PIE
cats=["Burgers","Pizza","Biryani","Shawarma","Chinese","Desserts","Healthy","Other"]
v=np.array([17,14,26,12,9,8,6,8])
fig=new(); head(fig,True); ax=fig.add_axes([0.1,0.2,0.8,0.6])
ax.pie(v,colors=XL,startangle=90,wedgeprops=dict(ec="white",lw=1))
ax.set_title("Chart Title",fontsize=14,color="#595959")
fig.legend([plt.Rectangle((0,0),1,1,fc=c) for c in XL],cats,ncol=4,loc="lower center",frameon=False,fontsize=8,bbox_to_anchor=(0.5,0.08))
save(fig,"pie_b.png")
fig=new(); head(fig,False); title(fig,"Biryani is 1 in every 4 orders,","more than burgers and pizza","Share of food orders by cuisine, %")
o=np.argsort(v); ax=fig.add_axes([0.25,0.1,0.65,0.66])
cs=[RED if cats[i]=="Biryani" else GREY for i in o]
ax.barh(range(8),v[o],color=cs,height=0.65)
ax.set_yticks(range(8)); ax.set_yticklabels([cats[i] for i in o],family=F,fontsize=10,color=INK)
for k,i in enumerate(o): ax.text(v[i]+0.5,k,f"{v[i]}%",va="center",family=F,fontsize=10,fontweight="bold" if cats[i]=="Biryani" else "normal",color=RED if cats[i]=="Biryani" else MUT)
ax.set_xticks([]); clean(ax); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(True); ax.spines["left"].set_color("#cfd5dd")
save(fig,"pie_a.png"); pair("pie")

# 3 MESSY BAR
areas=["Marina","Deira","JLT","Al Barsha","Downtown","Bur Dubai","JVC","Karama"]
t=np.array([29,33,27,31,30,34,41,32])
fig=new(); head(fig,True); ax=fig.add_axes([0.12,0.2,0.82,0.6])
ax.bar(range(8),t,color=XL); ax.set_xticks(range(8)); ax.set_xticklabels(areas,rotation=45,ha="right",fontsize=8)
ax.grid(axis="y",color="#d9d9d9"); ax.set_axisbelow(True); ax.set_title("Chart Title",fontsize=14,color="#595959")
for s in ["top","right"]: ax.spines[s].set_visible(False)
save(fig,"bar_b.png")
fig=new(); head(fig,False); title(fig,"JVC deliveries take the longest,","7 minutes slower than average","Average delivery time by area, minutes (city average: 32)")
o=np.argsort(t); ax=fig.add_axes([0.25,0.1,0.65,0.66])
cs=[RED if areas[i]=="JVC" else GREY for i in o]; ax.barh(range(8),t[o],color=cs,height=0.65)
ax.set_yticks(range(8)); ax.set_yticklabels([areas[i] for i in o],family=F,fontsize=10,color=INK)
for k,i in enumerate(o): ax.text(t[i]+0.4,k,f"{t[i]}",va="center",family=F,fontsize=10,fontweight="bold" if areas[i]=="JVC" else "normal",color=RED if areas[i]=="JVC" else MUT)
ax.set_xticks([]); clean(ax); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(True); ax.spines["left"].set_color("#cfd5dd")
save(fig,"bar_a.png"); pair("bar")

# 4 DUAL AXIS
m=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]; x=np.arange(12)
rev=np.array([80,84,90,95,101,108,116,121,128,134,141,150]); cr=np.array([3.2,3.3,3.3,3.4,3.4,3.5,3.1,2.9,2.7,2.6,2.4,2.3])
fig=new(); head(fig,True); ax=fig.add_axes([0.13,0.2,0.74,0.6])
ax.bar(x,rev,color=XL[0]); ax2=ax.twinx(); ax2.plot(x,cr,color=XL[1],lw=2.2,marker="o",ms=4)
ax.set_ylim(0,160); ax2.set_ylim(2,3.6); ax.set_xticks(x); ax.set_xticklabels(m,fontsize=8); ax.grid(axis="y",color="#d9d9d9"); ax.set_axisbelow(True)
ax.set_title("Chart Title",fontsize=14,color="#595959")
fig.legend([plt.Rectangle((0,0),1,1,fc=XL[0]),plt.Line2D([],[],color=XL[1],lw=2)],["Revenue (AED k)","Conversion rate (%)"],ncol=2,loc="lower center",frameon=False,fontsize=8,bbox_to_anchor=(0.5,0.08))
save(fig,"dual_b.png")
fig=new(); head(fig,False); title(fig,"Revenue kept growing,","but conversion has dropped since July","Monthly revenue (AED k) and conversion rate (%)")
a1=fig.add_axes([0.08,0.47,0.84,0.27]); a2=fig.add_axes([0.08,0.11,0.84,0.27])
a1.bar(x,rev,color=GREY,width=0.7); a1.text(11,rev[-1]+4,"150k",ha="center",family=F,fontsize=9,color=INK); a1.text(0,rev[0]+4,"80k",ha="center",family=F,fontsize=9,color=MUT)
a1.text(-0.4,175,"Revenue",family=F,fontsize=10,fontweight="bold",color=INK)
a2.plot(x[:7],cr[:7],color=GREY,lw=2.5); a2.plot(x[6:],cr[6:],color=RED,lw=3.2); a2.scatter([5,11],[cr[5],cr[11]],color=[GREY,RED],s=30,zorder=5)
a2.text(5,cr[5]+0.12,"3.5%",ha="center",family=F,fontsize=9,color=MUT); a2.text(11,cr[11]+0.14,"2.3%",ha="center",family=F,fontsize=10,fontweight="bold",color=RED)
a2.text(-0.4,3.95,"Conversion rate",family=F,fontsize=10,fontweight="bold",color=INK); a2.set_ylim(1.8,3.8); a1.set_ylim(0,170)
for a in (a1,a2): a.set_yticks([]); clean(a); a.set_xticks(x); a.set_xticklabels([mm if i%3==0 or i==11 else "" for i,mm in enumerate(m)],family=F,fontsize=8.5,color=INK); a.set_xlim(-0.6,11.6)
save(fig,"dual_a.png"); pair("dual")

# 5 3D
q=["Q1","Q2","Q3","Q4"]; s=np.array([1.8,2.0,1.9,2.4])
fig=new(); head(fig,True); ax=fig.add_axes([0.02,0.12,0.96,0.72],projection="3d")
ax.bar3d(np.arange(4),np.zeros(4),np.zeros(4),0.6,0.6,s,color=XL[:4],shade=True)
ax.set_xticks(np.arange(4)+0.3); ax.set_xticklabels(q); ax.set_yticks([]); ax.view_init(22,-58); ax.set_zlim(0,2.6)
ax.set_title("Chart Title",fontsize=14,color="#595959",y=0.95)
save(fig,"3d_b.png")
fig=new(); head(fig,False); title(fig,"Q4 was the best quarter,","sales up 26% on Q3","Quarterly sales, AED millions")
ax=fig.add_axes([0.08,0.1,0.84,0.62]); cs=[GREY,GREY,GREY,RED]; ax.bar(range(4),s,color=cs,width=0.6)
for i in range(4): ax.text(i,s[i]+0.05,f"{s[i]:.1f}M",ha="center",family=F,fontsize=11,fontweight="bold" if i==3 else "normal",color=RED if i==3 else MUT)
ax.set_xticks(range(4)); ax.set_xticklabels(q,family=F,fontsize=11,color=INK); ax.set_yticks([]); clean(ax); ax.set_ylim(0,2.7)
save(fig,"3d_a.png"); pair("3d")

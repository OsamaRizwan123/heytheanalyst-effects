import numpy as np, matplotlib.pyplot as plt
F="Poppins"; RED="#e8392b"; INK="#1c2433"; MUT="#7a8494"; GREY="#c9ced6"
m=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
rng=np.random.default_rng(3)
base={"Organic":40,"Paid":36,"Direct":33,"Email":29,"Referral":26,"Display":22,"Affiliate":19,"Social":14}
d={}
for k,v in base.items():
    r=np.cumsum(rng.normal(0,3.4,12)); r-=np.linspace(r[0],r[-1],12); d[k]=v+r+rng.normal(0,1.2)*np.linspace(0,1,12)
d["Social"]=np.array([14,15,17,20,22,26,29,33,36,39,42,45])
x=np.arange(12)
# BEFORE
fig,ax=plt.subplots(figsize=(7.5,6),dpi=400)
cols=["#4472c4","#ed7d31","#a5a5a5","#ffc000","#5b9bd5","#70ad47","#264478","#9e480e"]
for (k,v),c in zip(d.items(),cols): ax.plot(x,v,color=c,lw=1.8,marker="o",ms=3,label=k)
ax.set_xticks(x); ax.set_xticklabels(m,fontsize=8); ax.grid(color="#d9d9d9"); ax.set_ylim(0,60)
ax.set_title("Chart Title",fontsize=14,color="#595959",pad=12)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.legend(ncol=4,loc="upper center",bbox_to_anchor=(0.5,-0.08),frameon=False,fontsize=8)
fig.text(0.5,0.96,"BEFORE",ha="center",fontsize=16,family=F,fontweight="bold",color=MUT)
fig.subplots_adjust(top=0.84,bottom=0.17,left=0.1,right=0.95); fig.savefig("before.png",facecolor="white"); plt.close()
# AFTER
fig,ax=plt.subplots(figsize=(7.5,6),dpi=400)
for k,v in d.items():
    if k!="Social": ax.plot(x,v,color=GREY,lw=1.6,zorder=2)
ax.plot(x,d["Social"],color=RED,lw=3.2,zorder=5)
ax.scatter([11],[45],color=RED,s=40,zorder=6)
ax.text(11.3,45,"Social\n45k (×3)",va="center",fontsize=11,family=F,fontweight="bold",color=RED,linespacing=1.1)
ax.text(11.3,np.mean([d[k][-1] for k in d if k!="Social"]),"Other 7\nchannels",va="center",fontsize=8.5,family=F,color=MUT,linespacing=1.1)
ax.text(-0.25,14,"14k",va="center",fontsize=9,family=F,color=RED,ha="right")
ax.set_xticks(x); ax.set_xticklabels([mm if i in(0,3,6,9,11) else "" for i,mm in enumerate(m)],fontsize=8.5,family=F,color=INK)
ax.set_yticks([]); [ax.spines[s].set_visible(False) for s in ["top","right","left"]]; ax.spines["bottom"].set_color("#cfd5dd")
ax.tick_params(length=0); ax.set_ylim(5,58); ax.set_xlim(-1,13.6)
fig.text(0.5,0.96,"AFTER",ha="center",fontsize=16,family=F,fontweight="bold",color=RED)
fig.text(0.07,0.885,"Social traffic tripled this year,",fontsize=14,family=F,fontweight="bold",color=INK)
fig.text(0.07,0.845,"every other channel stayed flat",fontsize=14,family=F,fontweight="bold",color=RED)
fig.text(0.07,0.81,"Monthly website visits by channel (thousands)",fontsize=8.5,family=F,color=MUT)
fig.subplots_adjust(top=0.77,bottom=0.1,left=0.07,right=0.95); fig.savefig("after.png",facecolor="white"); plt.close()

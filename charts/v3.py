exec(open('five.py').read().split("# 2 PIE")[0])
import matplotlib.patches as P
from matplotlib.path import Path
GREEN="#2e9e5b"
items=[("Revenue",10.0),("Food cost",-3.2),("Salaries",-2.4),("Rent",-1.5),("Delivery\napps",-1.2),("Marketing",-0.5),("Profit",1.2)]
# WATERFALL BEFORE
fig=new(); head(fig,True); ax=fig.add_axes([0.12,0.22,0.82,0.58])
names=[n.replace("\n"," ") for n,_ in items]; vals=[abs(v) for _,v in items]
ax.bar(range(7),vals,color=XL[:7]); ax.set_xticks(range(7)); ax.set_xticklabels(names,rotation=45,ha="right",fontsize=8)
ax.grid(axis="y",color="#d9d9d9"); ax.set_axisbelow(True); ax.set_title("Chart Title",fontsize=14,color="#595959")
for s in ["top","right"]: ax.spines[s].set_visible(False)
save(fig,"wf_b.png")
# WATERFALL AFTER
fig=new(); head(fig,False); title(fig,"Delivery apps take AED 1.2M,","the same as the profit we keep","Restaurant P&L for the year, AED millions")
ax=fig.add_axes([0.07,0.13,0.88,0.6]); run=0
for i,(n,v) in enumerate(items):
    if i==0: b,h,c=0,v,NAVY; run=v
    elif i==6: b,h,c=0,run,GREEN
    else: b,h=run+v,-v; c=RED if "apps" in n else GREY; run+=v
    ax.bar(i,h,bottom=b,color=c,width=0.62)
    if 0<i<6: ax.plot([i-1+0.31,i-0.31],[b+h,b+h],color="#aab2bd",lw=1)
    if i==6: ax.plot([5+0.31,6-0.31],[run,run],color="#aab2bd",lw=1)
    lab=f"{v:+.1f}" if 0<i<6 else f"{abs(v):.1f}"
    hl=c in (RED,GREEN,NAVY)
    ax.text(i,b+h+0.15,lab,ha="center",family=F,fontsize=10,fontweight="bold" if hl else "normal",color=c if hl else MUT)
ax.set_xticks(range(7)); ax.set_xticklabels([n for n,_ in items],family=F,fontsize=8.5,color=INK)
ax.get_xticklabels()[4].set_color(RED); ax.get_xticklabels()[4].set_fontweight("bold")
ax.set_yticks([]); clean(ax); ax.set_ylim(0,11)
save(fig,"wf_b2.png")
import shutil; shutil.move("wf_b2.png","wf_a.png"); pair("wf")
# SANKEY BEFORE: table
rows=[("Dine-in","4.5"),("Delivery","4.0"),("Catering","1.5"),("Total revenue","10.0"),("Food cost","(3.2)"),("Gross profit","6.8"),("Salaries","(2.4)"),("Rent","(1.5)"),("Delivery app commission","(1.2)"),("Marketing","(0.5)"),("Operating profit","1.2")]
fig=new(); head(fig,True); ax=fig.add_axes([0.12,0.12,0.76,0.66]); ax.axis("off")
tb=ax.table(cellText=[[a,b] for a,b in rows],colLabels=["Line item","AED m"],loc="center",cellLoc="left",colWidths=[0.7,0.3])
tb.auto_set_font_size(False); tb.set_fontsize(9.5); tb.scale(1,2.2)
for (r,c),cell in tb.get_celld().items():
    cell.set_edgecolor("#bfbfbf"); cell.set_linewidth(0.6)
    if r==0: cell.set_facecolor("#d9e1f2"); cell.get_text().set_fontweight("bold")
    if r in (4,6,11): cell.get_text().set_fontweight("bold")
fig.text(0.5,0.84,"Income statement",ha="center",fontsize=13,color="#595959")
save(fig,"sk_b.png")
# SANKEY AFTER
fig=new(); head(fig,False); title(fig,"Out of every AED 10 we earn,","we keep AED 1.2","Restaurant P&L for the year, AED millions")
ax=fig.add_axes([0.02,0.06,0.96,0.7]); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
k=0.62; NW=0.22
def node(x,y,v,c): ax.add_patch(P.Rectangle((x,y-v*k),NW,v*k,fc=c,ec="none"))
def flow(x0,y0,x1,y1,v,c,a=0.35):
    h=v*k; xa,xb=x0+NW,x1; xm=(xa+xb)/2
    verts=[(xa,y0),(xm,y0),(xm,y1),(xb,y1),(xb,y1-h),(xm,y1-h),(xm,y0-h),(xa,y0-h),(xa,y0)]
    codes=[Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.LINETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.CLOSEPOLY]
    ax.add_patch(P.PathPatch(Path(verts,codes),fc=c,ec="none",alpha=a))
def lab(x,y,t,v,c,ha="left",bold=False):
    ax.text(x,y,t,ha=ha,va="bottom",family=F,fontsize=8.5,color=c,fontweight="bold" if bold else "normal",linespacing=1.0)
    ax.text(x,y,f"{v:.1f}",ha=ha,va="top",family=F,fontsize=9.5,color=c,fontweight="bold")
X=[0.9,3.3,5.7,8.0]
# col0 sources
src=[("Dine-in",4.5),("Delivery",4.0),("Catering",1.5)]; y=9.6; ry=8.4
for n,v in src:
    node(X[0],y,v,NAVY); flow(X[0],y,X[1],ry,v,NAVY,0.18); lab(X[0]-0.08,y-v*k/2,n,v,INK,"right"); y-=v*k+0.35; ry-=v*k
node(X[1],8.4,10,NAVY); ax.text(X[1]+NW/2,8.55,"Revenue 10.0",ha="center",va="bottom",family=F,fontsize=10,fontweight="bold",color=NAVY)
# col2
gp_top=9.0; fc_top=gp_top-6.8*k-0.5
node(X[2],gp_top,6.8,GREEN); flow(X[1],8.4,X[2],gp_top,6.8,GREEN)
node(X[2],fc_top,3.2,RED); flow(X[1],8.4-6.8*k,X[2],fc_top,3.2,RED)
ax.text(X[2]+NW/2,gp_top+0.15,"Gross profit 6.8",ha="center",va="bottom",family=F,fontsize=9.5,fontweight="bold",color=GREEN)
ax.text(X[2]+NW/2,fc_top-3.2*k-0.15,"Food cost 3.2",ha="center",va="top",family=F,fontsize=9.5,fontweight="bold",color=RED)
# col3
outs=[("Profit",1.2,GREEN),("Salaries",2.4,GREY),("Rent",1.5,GREY),("Delivery apps",1.2,RED),("Marketing",0.5,GREY)]
y=9.9; sy=gp_top
for n,v,c in outs:
    node(X[3],y,v,c if c!=GREY else "#9aa3b0"); flow(X[2],sy,X[3],y,v,c,0.35 if c!=GREY else 0.5)
    lab(X[3]+NW+0.1,y-v*k/2,n,v,c if c!=GREY else MUT,bold=c!=GREY); y-=v*k+0.42; sy-=v*k
save(fig,"sk_a.png"); pair("sk")

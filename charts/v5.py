exec(open('five.py').read().split("# 2 PIE")[0])
import matplotlib.patches as P
from PIL import ImageDraw, ImageFont
GREEN="#2e9e5b"; DG="#9aa3b0"
# 9 MEKKO
seg=["Burgers","Asian","Arabic","Healthy","Desserts"]; size=np.array([30,25,20,15,10])
pl=["Us","Competitor A","Competitor B","Others"]
sh=np.array([[45,25,20,10],[8,47,30,15],[30,30,25,15],[25,20,35,20],[20,30,20,30]])
fig=new(); head(fig,True); ax=fig.add_axes([0.12,0.22,0.82,0.58]); x=np.arange(5); w=0.2
for j in range(4): ax.bar(x+(j-1.5)*w,size*sh[:,j]/100,w,color=XL[j],label=pl[j])
ax.set_xticks(x); ax.set_xticklabels(seg,fontsize=9); ax.grid(axis="y",color="#d9d9d9"); ax.set_axisbelow(True)
ax.set_title("Chart Title",fontsize=14,color="#595959"); [ax.spines[s].set_visible(False) for s in ["top","right"]]
ax.legend(ncol=4,loc="upper center",bbox_to_anchor=(0.5,-0.08),frameon=False,fontsize=8)
save(fig,"mk_b.png")
fig=new(); head(fig,False); title(fig,"We lead in burgers, but we're almost","absent in Asian, the 2nd biggest market","Bar width = segment's share of the market. Height = share by player")
ax=fig.add_axes([0.07,0.1,0.86,0.62]); ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
cols=[RED,"#5c6b80","#9aa3b0","#d5d9e0"]; x0=0
for i,s in enumerate(size):
    y=0
    for j in range(4):
        h=sh[i,j]; ax.add_patch(P.Rectangle((x0+0.4,y+0.4),s-0.8,h-0.8,fc=cols[j],ec="none"))
        if h>=12 and s>=10: ax.text(x0+s/2,y+h/2,f"{h}%",ha="center",va="center",family=F,fontsize=9 if j else 10,fontweight="bold" if j==0 else "normal",color="white" if j<2 else INK)
        elif j==0: ax.text(x0+s/2,y+h/2,f"{h}%",ha="center",va="center",family=F,fontsize=8.5,fontweight="bold",color="white")
        y+=h
    ax.text(x0+s/2,-3,seg[i],ha="center",va="top",family=F,fontsize=9,color=RED if seg[i]=="Asian" else INK,fontweight="bold" if seg[i]=="Asian" else "normal")
    ax.text(x0+s/2,-8.5,f"{s}%",ha="center",va="top",family=F,fontsize=7.5,color=MUT); x0+=s
for k,(n,c) in enumerate(zip(pl,cols)):
    ax.add_patch(P.Rectangle((k*25,104),3,3,fc=c,ec="none",clip_on=False)); ax.text(k*25+4.5,105.5,n,va="center",family=F,fontsize=8.5,color=RED if k==0 else INK,fontweight="bold" if k==0 else "normal")
save(fig,"mk_a.png")
# 10 2x2
ini=["Free delivery\nweekends","Loyalty points","New app design","Combo meals","Kitchen in JVC","Corporate plans","Late-night menu","AI recommendations"]
imp=np.array([8.3,6.6,6,7.4,8.5,4.4,5.7,3.4]); eff=np.array([2.6,3.4,8.5,1.4,8,6,2.4,7.5])
fig=new(); head(fig,True); ax=fig.add_axes([0.12,0.3,0.82,0.5]); x=np.arange(8)
ax.bar(x-0.2,imp,0.4,color=XL[0],label="Impact"); ax.bar(x+0.2,eff,0.4,color=XL[1],label="Effort")
ax.set_xticks(x); ax.set_xticklabels([i.replace("\n"," ") for i in ini],rotation=45,ha="right",fontsize=8); ax.grid(axis="y",color="#d9d9d9"); ax.set_axisbelow(True)
ax.set_title("Chart Title",fontsize=14,color="#595959"); [ax.spines[s].set_visible(False) for s in ["top","right"]]
ax.legend(ncol=2,loc="upper center",bbox_to_anchor=(0.5,-0.42),frameon=False,fontsize=8); save(fig,"mx_b.png")
fig=new(); head(fig,False); title(fig,"Start with 4 quick wins:","high impact, low effort","8 initiatives scored on impact and effort (1–10)")
ax=fig.add_axes([0.1,0.1,0.82,0.62]); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.add_patch(P.Rectangle((0,5),5,5,fc="#fdecea",ec="none"))
ax.axvline(5,color="#cfd5dd",lw=1); ax.axhline(5,color="#cfd5dd",lw=1)
for (t,xx,yy,c) in [("QUICK WINS",0.3,9.6,RED),("BIG BETS",5.3,9.6,MUT),("FILL-INS",0.3,0.4,MUT),("AVOID",5.3,0.4,MUT)]:
    ax.text(xx,yy,t,family=F,fontsize=9,fontweight="bold",color=c,va="top" if yy>5 else "bottom")
for n,i_,e_ in zip(ini,imp,eff):
    q=i_>5 and e_<5; ax.scatter(e_,i_,s=150 if q else 90,color=RED if q else DG,zorder=3,ec="white",lw=1.5)
    ha="left"; dx=0.3
    if e_>7.6: ha="right"; dx=-0.3
    ax.text(e_+dx,i_,n,va="center",ha=ha,family=F,fontsize=8.5,color=INK if q else MUT,fontweight="bold" if q else "normal",linespacing=1.05)
ax.set_xticks([]); ax.set_yticks([]); [ax.spines[s].set_visible(False) for s in ax.spines]
ax.text(5,-0.5,"Effort (low to high)",ha="center",va="top",family=F,fontsize=9.5,color=INK); ax.text(-0.4,5,"Impact (low to high)",ha="right",va="center",rotation=90,family=F,fontsize=9.5,color=INK)
save(fig,"mx_a.png")
# 11 DRIVER TREE
fig=new(); head(fig,True); ax=fig.add_axes([0.1,0.2,0.8,0.6]); ax.axis("off")
rows=[["Metric","Last month","This month"],["Revenue (AED k)","1,250","1,150"],["Orders","50,000","45,000"],["Avg order value","25.0","25.6"],["Active customers","20,000","19,800"],["Orders per customer","2.50","2.27"]]
tb=ax.table(cellText=rows[1:],colLabels=rows[0],loc="center",cellLoc="center",colWidths=[0.46,0.27,0.27]); tb.auto_set_font_size(False); tb.set_fontsize(10); tb.scale(1,2.6)
for (r,c),cell in tb.get_celld().items():
    cell.set_edgecolor("#bfbfbf"); cell.set_linewidth(0.6)
    if r==0: cell.set_facecolor("#d9e1f2"); cell.get_text().set_fontweight("bold")
fig.text(0.5,0.84,"Monthly KPIs",ha="center",fontsize=13,color="#595959"); save(fig,"dt_b.png")
fig=new(); head(fig,False); title(fig,"Revenue fell because customers","order less often, not because we lost them","Change vs last month")
ax=fig.add_axes([0.03,0.08,0.94,0.66]); ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
def box(x,y,name,val,c,bold=False):
    ax.add_patch(P.FancyBboxPatch((x-14,y-7),28,14,boxstyle="round,pad=0,rounding_size=2",fc="white" if c!=RED else "#fdecea",ec=c,lw=2.4 if c==RED else 1.4))
    ax.text(x,y+2.4,name,ha="center",va="center",family=F,fontsize=8.5,color=INK)
    ax.text(x,y-2.8,val,ha="center",va="center",family=F,fontsize=12,fontweight="bold",color=c if c!=DG else MUT)
def link(x0,y0,x1,y1,c): ax.plot([x0+14,(x0+x1)/2,(x0+x1)/2,x1-14],[y0,y0,y1,y1],color=c,lw=2.2 if c==RED else 1.2,solid_capstyle="round")
box(15,55,"Revenue","−8%",RED); box(50,75,"Orders","−10%",RED); box(50,30,"Avg order value","+2%",DG)
box(85,90,"Active customers","−1%",DG); box(85,60,"Orders per customer","−9%",RED)
link(15,55,50,75,RED); link(15,55,50,30,"#c9ced6"); link(50,75,85,90,"#c9ced6"); link(50,75,85,60,RED)
for (xx,yy,s) in [(32.5,52,"="),(67.5,75,"=")]: pass
ax.text(50,52.5,"×",ha="center",va="center",family=F,fontsize=16,color=MUT); ax.text(85,75,"×",ha="center",va="center",family=F,fontsize=16,color=MUT)
ax.text(85,45,"The problem is here",ha="center",va="center",family=F,fontsize=9.5,fontweight="bold",color=RED)
save(fig,"dt_a.png")
# 12 TORNADO
var=["Commission rate","Food cost","Order volume","Avg order value","Rent","Marketing spend"]
lo=np.array([0.4,0.7,0.8,0.85,1.05,1.1]); hi=np.array([2.0,1.7,1.6,1.55,1.35,1.3]); base=1.2
fig=new(); head(fig,True); ax=fig.add_axes([0.12,0.3,0.82,0.5]); x=np.arange(6); o=[4,2,0,5,1,3]
ax.bar(x-0.2,lo[o],0.4,color=XL[0],label="Low case"); ax.bar(x+0.2,hi[o],0.4,color=XL[1],label="High case")
ax.set_xticks(x); ax.set_xticklabels([var[i] for i in o],rotation=45,ha="right",fontsize=8.5); ax.grid(axis="y",color="#d9d9d9"); ax.set_axisbelow(True)
ax.set_title("Chart Title",fontsize=14,color="#595959"); [ax.spines[s].set_visible(False) for s in ["top","right"]]
ax.legend(ncol=2,loc="upper center",bbox_to_anchor=(0.5,-0.42),frameon=False,fontsize=8); save(fig,"tn_b.png")
fig=new(); head(fig,False); title(fig,"Delivery commission moves profit","more than anything else","Profit (AED m) if each assumption moves ±20%, base = 1.2")
ax=fig.add_axes([0.3,0.1,0.62,0.6]); y=np.arange(6)[::-1]
for i,(v,l,h) in enumerate(zip(var,lo,hi)):
    c=RED if i==0 else DG; ax.barh(y[i],l-base,left=base,color=c,height=0.6,alpha=0.55 if i==0 else 0.6); ax.barh(y[i],h-base,left=base,color=c,height=0.6)
    ax.text(l-0.04,y[i],f"{l:.1f}",ha="right",va="center",family=F,fontsize=9,color=c if i==0 else MUT,fontweight="bold" if i==0 else "normal")
    ax.text(h+0.04,y[i],f"{h:.1f}",ha="left",va="center",family=F,fontsize=9,color=c if i==0 else MUT,fontweight="bold" if i==0 else "normal")
ax.axvline(base,color=INK,lw=1.2); ax.text(base,6.0,"Base 1.2",ha="center",family=F,fontsize=9,color=INK,bbox=dict(fc="white",ec="none",pad=2))
ax.set_yticks(y); ax.set_yticklabels(var,family=F,fontsize=10,color=INK); ax.get_yticklabels()[0].set_color(RED); ax.get_yticklabels()[0].set_fontweight("bold")
ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ax.spines]; ax.tick_params(length=0); ax.set_xlim(0.1,2.3); ax.set_ylim(-0.6,6.4)
save(fig,"tn_a.png")
# headers + trim
fb=ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",88)
spec=[(9,"mk","Grouped bar chart","Marimekko chart"),(10,"mx","Grouped bar chart","2×2 matrix"),(11,"dt","KPI table","Driver tree"),(12,"tn","Grouped bar chart","Tornado chart")]
for n,k,b,a in spec:
    for suf,word,nm,col in [("_b","BEFORE",b,"#7a8494"),("_a","AFTER",a,"#e8392b")]:
        im=Image.open(k+suf+".png").convert("RGB"); W,H=im.size
        A=np.asarray(im.crop((0,215,W,H))).astype(int); ink=(np.abs(A-255).max(axis=2)>12)
        ys=np.where(ink.any(1))[0]; xs=np.where(ink.any(0))[0]; A=A[ys[0]:ys[-1]+1,xs[0]:xs[-1]+1]; rows_=ink.any(1)[ys[0]:ys[-1]+1]
        keep=[]; run=0
        for i,r in enumerate(rows_):
            run=0 if r else run+1
            if run<=130: keep.append(i)
        body=Image.fromarray(A[keep].astype(np.uint8)); bw,bh=body.size; M=100; top=260; bx,by=W-2*M,H-top-M
        s=min(bx/bw,by/bh); body=body.resize((int(bw*s),int(bh*s)),Image.LANCZOS)
        out=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(out)
        parts=[(word,col),("  ·  ","#c9ced6"),(nm,"#1c2433")]; xx=(W-sum(d.textlength(t,font=fb) for t,_ in parts))/2
        for t,c in parts: d.text((xx,50),t,font=fb,fill=c); xx+=d.textlength(t,font=fb)
        out.paste(body,((W-body.width)//2,top+(by-body.height)//2))
        out.save(f"final/{n}{'a_before' if suf=='_b' else 'b_after'}.png")

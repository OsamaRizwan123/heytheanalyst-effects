exec(open('five.py').read().split("# 2 PIE")[0])
from PIL import ImageDraw, ImageFont
coh=["Jan","Feb","Mar","Apr","May","Jun"]; size=[2400,2650,2500,2800,3100,3000]
ret={"Jan":[100,34,26,22,20,18,17],"Feb":[100,35,27,22,20,19],"Mar":[100,33,25,21,19],
     "Apr":[100,52,44,40],"May":[100,55,46],"Jun":[100,54]}
# BEFORE: raw cohort table
fig=new(); head(fig,True); ax=fig.add_axes([0.04,0.2,0.92,0.6]); ax.axis("off")
cells=[]
for c,s in zip(coh,size):
    r=ret[c]; cells.append([c,f"{s:,}"]+[f"{round(s*p/100):,}" for p in r[1:]]+[""]*(7-len(r)))
tb=ax.table(cellText=cells,colLabels=["Cohort","Users","M1","M2","M3","M4","M5","M6"],loc="center",cellLoc="center")
tb.auto_set_font_size(False); tb.set_fontsize(8.5); tb.scale(1,2.4)
for (r,c),cell in tb.get_celld().items():
    cell.set_edgecolor("#bfbfbf"); cell.set_linewidth(0.6)
    if r==0: cell.set_facecolor("#d9e1f2"); cell.get_text().set_fontweight("bold")
fig.text(0.5,0.84,"Active customers by signup month",ha="center",fontsize=13,color="#595959")
save(fig,"rc_b.png")
# AFTER: retention curves
fig=new(); head(fig,False); title(fig,"Customers who joined after the loyalty","launch stay twice as long","% of customers still ordering, by month since signup")
ax=fig.add_axes([0.1,0.1,0.72,0.62])
for c in coh:
    r=ret[c]; new_=c in("Apr","May","Jun")
    ax.plot(range(len(r)),r,color=RED if new_ else "#b4bbc6",lw=2.8 if new_ else 1.8,zorder=4 if new_ else 2,solid_capstyle="round")
ax.text(3.15,40,"Joined after\nloyalty launch\n40% at M3",family=F,fontsize=10,fontweight="bold",color=RED,va="center",linespacing=1.15)
ax.text(3.0,11,"Joined before: 21% at M3",family=F,fontsize=10,color=MUT,va="center",ha="center")
ax.scatter([3],[40],color=RED,s=40,zorder=6); ax.scatter([3],[21.7],color="#9aa3b0",s=40,zorder=6)
ax.set_xticks(range(7)); ax.set_xticklabels(["Signup","M1","M2","M3","M4","M5","M6"],family=F,fontsize=9,color=INK)
ax.set_yticks([0,25,50,75,100]); ax.set_yticklabels(["0%","25%","50%","75%","100%"],family=F,fontsize=8.5,color=MUT)
ax.grid(axis="y",color="#eef0f3"); ax.set_axisbelow(True); clean(ax); ax.set_ylim(0,105); ax.set_xlim(-0.2,6.1)
save(fig,"rc_a.png")
fb=ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",88)
for src,dst,word,nm,col in [("rc_b","8a_before","BEFORE","Cohort table","#7a8494"),("rc_a","8b_after","AFTER","Retention curves","#e8392b")]:
    im=Image.open(src+".png").convert("RGB"); d=ImageDraw.Draw(im); W=im.width; d.rectangle([0,0,W,215],fill="white")
    parts=[(word,col),("  ·  ","#c9ced6"),(nm,"#1c2433")]; x=(W-sum(d.textlength(t,font=fb) for t,_ in parts))/2
    for t,c in parts: d.text((x,50),t,font=fb,fill=c); x+=d.textlength(t,font=fb)
    im.save(f"named/{dst}.png")

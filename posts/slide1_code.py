from PIL import Image, ImageDraw, ImageFont, ImageFilter
import re
f=lambda s: ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf",s)
mono=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",30)
code='''import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# load experiment data
df = pd.read_csv("experiment_results.csv")
df = df.dropna(subset=["user_id", "group"])

# click-through rate by group
summary = (df.groupby("group")
             .agg(users=("user_id", "nunique"),
                  clicks=("clicked", "sum")))
summary["ctr"] = summary["clicks"] / summary["users"]
print(summary)

# two-proportion z-test
z, p_value = proportions_ztest(summary["clicks"],
                               summary["users"])

if p_value < 0.05:
    print("Significant: ship variant B")
else:
    print("Not significant: keep testing")

def retention(df, days=7):
    first = df.groupby("user_id")["date"].min()
    df = df.join(first, on="user_id", rsuffix="_first")
    df["day"] = (df["date"] - df["date_first"]).dt.days
    return df[df.day <= days]["user_id"].nunique()

weekly = df.resample("W", on="date")["revenue"].sum()
weekly.plot(title="Weekly revenue")
'''.split("\n")
KW={"import","from","as","def","return","if","else","print","for","in"}
bg=Image.new("RGB",(1080,1350),(14,16,22)); d=ImageDraw.Draw(bg)
y=40
for ln in code*2:
    x=50
    for tok in re.findall(r'"[^"]*"|#.*|\w+|\s+|[^\w\s]',ln):
        if tok.startswith("#"): c=(90,110,95)
        elif tok.startswith('"'): c=(150,120,80)
        elif tok in KW: c=(150,95,140)
        elif re.fullmatch(r"\d+(\.\d+)?",tok): c=(120,140,170)
        else: c=(110,120,140)
        d.text((x,y),tok,font=mono,fill=tuple(int(14+(v-14)*0.5) for v in c)); x+=d.textlength(tok,font=mono)
    y+=42
    if y>1350: break
bg=bg.filter(ImageFilter.GaussianBlur(1.2))
ov=Image.new("L",bg.size,0); od=ImageDraw.Draw(ov); od.rounded_rectangle((80,470,1000,910),radius=60,fill=180); ov=ov.filter(ImageFilter.GaussianBlur(70))
bg=Image.composite(Image.new("RGB",bg.size,(14,16,22)),bg,ov)
d=ImageDraw.Draw(bg); Y=(255,212,0)
d.text((540,610),"is coding",font=f(150),fill=Y,anchor="mm"); d.text((540,770),"dead?",font=f(150),fill=Y,anchor="mm")
d.text((1020,1280),"swipe",font=f(38),fill=(170,170,170),anchor="rm")
bg.save("slide1.jpg",quality=95)

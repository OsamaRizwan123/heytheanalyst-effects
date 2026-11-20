import re
segs=[(0.15,2.38,["Here's how to make a chart","like a consultant."]),
(2.52,4.11,["Zyadatar log yeh chart banate hain."]),
(4.28,6.13,["Everything's there,","lekin samajh kuch nahi aata."]),
(6.52,7.18,["So let's..."]),(7.29,9.84,["first, gridlines,","legend aur title hata do."]),
(10.14,11.76,["Then bars ko sort karo,","biggest first."]),
(11.90,13.58,["Ab cumulative percentage","ki line add karo."]),
(13.85,15.54,["Pehle teen issues?","86%."]),
(15.67,19.98,["80% pe ek line draw karo.","Because most problems","sirf kuch wajahon se aati hain."]),
(20.15,21.52,["Un teen ko highlight karo."]),
(21.59,24.85,["Baaki sab is just noise.","And finally,","title mein topic nahi,"]),
(24.92,25.55,["answer likho:"]),
(25.85,28.40,["“3 issues cause","86% of complaints."]),
(28.66,29.90,["Fix late delivery first.”"]),
(30.07,31.50,["And this is called","a Pareto chart."]),
(31.64,33.55,["Save kar lo,","next presentation mein kaam aayega."])]
KW=["consultant","sort","biggest first","cumulative","86%","80%","highlight","noise","answer","Fix late delivery first","Pareto chart","Save","gridlines","legend","title"]
def ts(x): return f"0:{int(x//60):02d}:{x%60:05.2f}"
lines=[]
for a,b,ch in segs:
    tot=sum(len(c)+4 for c in ch); t=a
    for c in ch: d=(b-a)*(len(c)+4)/tot; lines.append((t,t+d,c)); t+=d
out=[(a,min(lines[i+1][0] if i+1<len(lines) else 34,b+0.5),c) for i,(a,b,c) in enumerate(lines)]
def hi(c):
    for k in sorted(KW,key=len,reverse=True):
        c=re.sub(r"(?<![\w{])("+re.escape(k)+r")(?![\w])",r"{\\c&H2B39E8&}\1{\\c&HFFFFFF&}",c,flags=re.I)
    return c
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3,4,2,60,60,175,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open("captions.ass","w") as f:
    f.write(hdr)
    for a,b,c in out: f.write(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{hi(c)}\n")

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
FD="/usr/share/fonts/truetype/google-fonts/"
pdfmetrics.registerFont(TTFont("P",FD+"Poppins-Regular.ttf")); pdfmetrics.registerFont(TTFont("PB",FD+"Poppins-Bold.ttf"))
NAVY,RED,INK,MUT,LINE=HexColor("#0b3d91"),HexColor("#e8392b"),HexColor("#1c2433"),HexColor("#7a8494"),HexColor("#e6e9ee")
W,H=1200,800
WH=["1 time dimension, 1 measure, many categories","1 dimension, 1 measure, parts of a whole","1 dimension, 1 measure, compared to a benchmark","1 time dimension, 2 measures on different scales","2 dimensions, 1 measure","1 measure that adds and subtracts to a total","1 measure flowing through 2+ levels","2 dimensions (cohort × month), 1 measure","2 dimensions, 1 measure, segment size matters","1 dimension, 2 measures","1 measure built from other measures","1 outcome, many inputs that can move"]
C=[("Spaghetti line chart","Highlighted line chart","Too many lines and nobody knows where to look.","Grey out everything except the line that tells the story. Label it directly, no legend."),
("Pie chart","Waffle chart","Eight slices, eight colours. Nobody can compare the angles.","Show the one share that matters. 100 squares make '1 in 4' impossible to miss."),
("Bar chart","Dot plot","Random order, rainbow colours, no benchmark.","Sort it, put everyone against the average, and colour only the outlier."),
("Dual-axis chart","Small multiples","Two scales on one chart. You can make any line look like anything.","Split into two charts that share the same timeline. One message each."),
("Data table","Heatmap","84 numbers. The pattern is in there, but nobody will find it.","Let colour do the reading. The peak jumps out, then call it out in the title."),
("Bar chart","Waterfall chart","Revenue, costs and profit as bars of the same kind. No flow.","Walk from revenue to profit step by step. Highlight the step you want discussed."),
("Income statement","Sankey chart","A P&L table only finance people read.","Show where every dirham goes. Green is what you keep, red is what leaves."),
("Cohort table","Retention curves","Raw counts. Every cohort started at a different size.","Convert to % of signups, so every cohort starts at 100. Then highlight the change."),
("Grouped bar chart","Marimekko chart","Shares by segment, but you can't tell which segment is big.","Width = market size, height = share. Where you win and where you're missing, in one picture."),
("Grouped bar chart","2×2 matrix","Impact and effort as side-by-side bars for 8 ideas.","Plot impact vs effort. Start with the top-left corner: the quick wins."),
("KPI table","Driver tree","Revenue is down. The table can't tell you why.","Break the metric into its drivers. Follow the red path to the root cause."),
("Grouped bar chart","Tornado chart","Low and high cases for every assumption, in random order.","Move each assumption the same amount, sort by impact. The longest bar is what you protect first.")]
c=canvas.Canvas("Charts_Like_a_Consultant.pdf",pagesize=(W,H)); c.setTitle("12 Charts Like a Consultant"); c.setAuthor("@heytheanalyst")
def grid():
    c.setStrokeColor(HexColor("#f3f4f7")); c.setLineWidth(0.6)
    for x in range(0,W,40): c.line(x,0,x,H)
    for y in range(0,H,40): c.line(0,y,W,y)
def foot(n):
    c.setFont("P",11); c.setFillColor(MUT); c.drawString(60,30,"@heytheanalyst"); c.drawRightString(W-60,30,f"{n} / 14")
# cover
grid(); c.setFillColor(RED); c.roundRect(80,560,250,44,22,fill=1,stroke=0); c.setFillColor(HexColor("#ffffff")); c.setFont("PB",18); c.drawCentredString(205,574,"FREE GUIDE")
c.setFillColor(INK); c.setFont("PB",72); c.drawString(80,440,"12 charts"); c.setFillColor(RED); c.drawString(80,355,"like a consultant")
c.setFillColor(MUT); c.setFont("P",24); c.drawString(84,295,"Same data. Before vs after. One rule for each.")
c.drawImage(ImageReader("final/9b_after.png"),780,90,width=360,height=450,mask="auto")
c.setFillColor(INK); c.setFont("PB",18); c.drawString(84,120,"@heytheanalyst"); c.showPage()
for i,(b,a,prob,rule) in enumerate(C,1):
    c.setFillColor(HexColor("#ffffff")); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(RED); c.circle(92,722,24,fill=1,stroke=0); c.setFillColor(HexColor("#ffffff")); c.setFont("PB",22); c.drawCentredString(92,714,str(i))
    c.setFillColor(INK); c.setFont("PB",30); c.drawString(132,711,b); w=pdfmetrics.stringWidth(b,"PB",30)
    c.setFillColor(MUT); c.drawString(132+w+14,711,"→" if False else "to"); w2=pdfmetrics.stringWidth("to","PB",30)
    c.setFillColor(RED); c.drawString(132+w+28+w2,711,a)
    for k,(img,x) in enumerate([(f"final/{i}a_before.png",60),(f"final/{i}b_after.png",420)]):
        c.setStrokeColor(LINE); c.setLineWidth(1.2); c.roundRect(x-4,96,348,436,10,fill=0,stroke=1)
        c.drawImage(ImageReader(img),x,100,width=340,height=425,mask="auto")
    tx=800; c.setFillColor(NAVY); c.setFont("PB",13); c.drawString(tx,640,"WHEN YOU HAVE")
    def wrap(txt,y,font,size,col,width=340,lead=1.45):
        c.setFont(font,size); c.setFillColor(col); line=""
        for wd in txt.split():
            t=(line+" "+wd).strip()
            if pdfmetrics.stringWidth(t,font,size)>width: c.drawString(tx,y,line); y-=size*lead; line=wd
            else: line=t
        c.drawString(tx,y,line); return y-size*lead
    y=wrap(WH[i-1],610,"PB",19,NAVY); y-=26
    c.setFillColor(MUT); c.setFont("PB",13); c.drawString(tx,y,"THE PROBLEM"); y=wrap(prob,y-30,"P",19,INK); y-=26
    c.setFillColor(RED); c.setFont("PB",13); c.drawString(tx,y,"THE CONSULTANT FIX"); y=wrap(rule,y-30,"PB",19,INK)
    c.setStrokeColor(LINE); c.line(tx,150,W-60,150); c.setFillColor(MUT); c.setFont("P",12); c.drawString(tx,125,"Illustrative data")
    foot(i+1); c.showPage()
grid(); c.setFillColor(INK); c.setFont("PB",48); c.drawString(80,640,"The 5 rules behind every chart")
R=["Ask the question before you open Excel.","Remove everything that isn't data: gridlines, legends, 'Chart Title'.","Use colour for one thing only: the story.","Label directly, next to the data.","Make the title the answer, not the topic."]
for k,r in enumerate(R):
    y=540-k*80; c.setFillColor(RED); c.circle(102,y+10,20,fill=1,stroke=0); c.setFillColor(HexColor("#ffffff")); c.setFont("PB",20); c.drawCentredString(102,y+3,str(k+1))
    c.setFillColor(INK); c.setFont("P",26); c.drawString(140,y,r)
c.setFillColor(RED); c.setFont("PB",28); c.drawString(80,100,"Follow @heytheanalyst for more charts like a consultant")
c.showPage(); c.save()

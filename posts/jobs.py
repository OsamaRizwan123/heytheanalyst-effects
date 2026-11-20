from PIL import Image, ImageDraw, ImageChops
U='inputs/'
spec={"OpenAI":(U+'f3e59265-image.jpg',(40,470,1190,775),[(155,480,742,545)]),
      "Google":(U+'147b02bb-image.jpg',(40,700,1190,1085),[(1018,860,1168,928),(155,935,582,1005)]),
      "Meta":(U+'b33c51f6-image.jpg',(40,250,1190,625),[(712,330,808,395),(512,405,672,470)])}
for k,(p,box,hl) in spec.items():
    im=Image.open(p).convert('RGB'); m=Image.new('RGB',im.size,'white'); d=ImageDraw.Draw(m)
    for b in hl: d.rounded_rectangle(b,radius=10,fill=(255,233,120))
    im=ImageChops.multiply(im,m); im.crop(box).save(f'job_{k}.png')

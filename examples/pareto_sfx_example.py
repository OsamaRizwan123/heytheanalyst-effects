import numpy as np, wave
SR=48000; DUR=34.1; out=np.zeros(int(SR*DUR)); rng=np.random.default_rng(3)
def pop(f0=900,f1=500,d=0.09,amp=0.45):
    tt=np.arange(int(SR*d))/SR; ph=2*np.pi*np.cumsum(np.linspace(f0,f1,len(tt)))/SR; return amp*np.sin(ph)*np.exp(-tt*38)
def whoosh(d=0.6,amp=0.3):
    n=int(SR*d); x=np.convolve(rng.normal(0,1,n),np.ones(14)/14,"same"); return amp*x*np.sin(np.linspace(0,np.pi,n))**2
def ding(amp=0.35,d=0.9):
    tt=np.arange(int(SR*d))/SR; return amp*(np.sin(2*np.pi*1320*tt)+0.5*np.sin(2*np.pi*2640*tt))*np.exp(-tt*5)/1.5
def click(): return pop(2400,2000,0.025,0.15)
def add(t,s): i=int(t*SR); out[i:i+len(s)]+=s[:len(out)-i]
for i in range(8): add(0.2+i*0.13,pop(500+i*50,350,0.07,0.22))
for st in [7.3,10.1,11.9,15.65,20.1,23.0,30.05]: add(st,pop(800,500))
add(7.7,whoosh(0.3,0.18)); add(8.5,whoosh(0.3,0.18)); add(9.3,whoosh(0.35,0.2))
add(10.7,whoosh(0.9,0.3)); add(12.1,whoosh(2.8,0.12))
for t in [12.1,13.5,14.9]: add(t,pop(1100,800,0.06,0.3))
add(15.8,whoosh(0.7,0.2))
for r in range(8): add(20.3+0.12*r,click())
add(21.0,pop(1200,900,0.08,0.3))
for c in range(33): add(25.85+c*(2.55/33),click()*0.7)
for c in range(24): add(28.66+c*(1.24/24),click()*0.7)
add(30.2,whoosh(0.4,0.2)); add(30.6,ding())
with wave.open("sfx.wav","w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out,-1,1)*32767).astype(np.int16).tobytes())

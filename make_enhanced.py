from PIL import Image, ImageDraw, ImageFont
import os
W, H = 2400, 1500
img = Image.new("RGB", (W,H), (255,255,255))
d = ImageDraw.Draw(img)
def F(s,b=False):
    p = "C:\\Windows\\Fonts\\arialbd.ttf" if b else "C:\\Windows\\Fonts\\arial.ttf"
    return ImageFont.truetype(p, s)
navy=(18,52,86); blue=(42,110,180); grey=(90,90,90)
# header
d.ellipse([60,30,300,110], outline=(90,60,140), width=3)
d.text((180,50), "Abhivyakti-1", font=F(30,True), fill=(20,20,20), anchor="ma")
d.text((1200,30), "PROPOSED SOLUTION", font=F(42,True), fill=(0,0,0), anchor="ma")
d.text((1200,80), "DIGITAL LAND BOUNDARY RECONSTRUCTION & VERIFICATION", font=F(34,True), fill=(0,0,0), anchor="ma")
d.text((2180,45), "SMART INDIA", font=F(36,True), fill=(40,40,40), anchor="ma")
d.text((2180,85), "HACKATHON 2026", font=F(36,True), fill=(40,40,40), anchor="ma")
# flow
steps=[("Historical","Records",(220,235,245)),("RTK GNSS","Survey",(220,245,225)),("Digital","Boundary",(255,240,210)),("Stakeholder","Verification",(235,225,245)),("Authority","Approval",(220,235,245))]
x0=90; cw=360; gap=90; y0=170; ch=150
for i,(a,b,col) in enumerate(steps):
    x=x0+i*(cw+gap)
    d.rounded_rectangle([x,y0,x+cw,y0+ch], radius=22, fill=col, outline=(170,190,210), width=2)
    d.text((x+cw//2,y0+38), a, font=F(34,True), fill=navy, anchor="ma")
    d.text((x+cw//2,y0+82), b, font=F(34,False), fill=(0,0,0), anchor="ma")
    if i<4:
        ax=x+cw+12
        ay=y0+ch//2
        d.polygon([(ax,ay-22),(ax+45,ay),(ax,ay+22)], fill=blue)
# three cards
cards=[
 ("How the Solution Works",(235,243,250), navy, [
  "Extract measurements, landmarks & ownership from Khasra / maps.",
  "Reconstruct historical vertices via distance-intersection anchoring.",
  "Capture cm-level (±2 cm) coords with RTK GNSS + CORS; build GIS polygon.",
  "Auto-compare old vs surveyed boundaries; flag area & displacement.",
  "Farmer + co-owner + neighbor verification via offline-first mobile app.",
  "Evidence-linked objection, re-survey, authority approval & audit trail.",
 ]),
 ("How It Addresses the Problem",(235,248,238), (20,80,50), [
  "Digitizes old / manual records into geo-referenced measurable boundaries.",
  "Reduces disputes via 4-level timestamped multi-stakeholder verification.",
  "Replaces verbal claims with coords, photos & survey evidence.",
  "Detects area & boundary mismatch early — before final approval.",
  "Creates transparent, updateable, legally traceable digital record.",
  "Aligned to DILRMP, SVAMITVA, NAKSHA & CORS standards.",
 ]),
 ("Innovation & Uniqueness",(255,246,225), (120,70,10), [
  "Historical-to-digital reconstruction from colonial chain / tape records.",
  "RTK GNSS + GIS / PostGIS + drone-ready integration for precise mapping.",
  "4-level verification: owner, co-owner, neighbor, authority.",
  "Objection tied to photo + GPS + survey data; re-survey workflow.",
  "Offline-first multilingual app; full audit: who, when, what changed.",
  "Scalable GovTech SaaS with API licensing & dashboard analytics.",
 ]),
]
cy=380; ch2=870; cx0=70; cgap=45; cw2=(W-140-2*cgap)//3
for i,(title,col,tcol,bullets) in enumerate(cards):
    x=cx0+i*(cw2+cgap)
    d.rounded_rectangle([x,cy,x+cw2,cy+ch2], radius=55, fill=col, outline=(200,200,200), width=2)
    d.text((x+cw2//2,cy+30), title, font=F(33,True), fill=tcol, anchor="ma")
    by=cy+95
    for b in bullets:
        # wrap at ~52 chars
        words=b.split(); lines=[]; cur=""
        for w in words:
            if len(cur+" "+w)<52: cur=(cur+" "+w).strip()
            else: lines.append(cur); cur=w
        if cur: lines.append(cur)
        d.text((x+35,by), "•", font=F(28,True), fill=(0,0,0))
        for j,ln in enumerate(lines):
            d.text((x+60,by+j*36), ln, font=F(27,False), fill=(20,20,20))
        by+=len(lines)*36+14
# footer bar
fy=cy+ch2+35; fh=130
d.rounded_rectangle([40,fy,W-40,fy+fh], radius=22, fill=navy)
d.text((90,fy+fh//2), "FINAL OUTPUT", font=F(32,True), fill=(130,190,235), anchor="lm")
d.text((420,fy+fh//2), "Verified Digital Land Record  •  Accurate Boundary ±2 cm  •  Evidence-Based Verification  •  Full Audit Trail", font=F(32,True), fill=(255,255,255), anchor="lm")
img.save("proposal_enhanced.png", dpi=(300,300))
print("saved", img.size)

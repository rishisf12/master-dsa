from PIL import Image, ImageDraw, ImageFont
import os
W, H = 2400, 5200
bg = (255,255,255)
ink = (20,20,20)
navy = (15,42,68)
light_border = (190,190,190)
phase_bg = (15,42,68)
img = Image.new("RGB", (W, H), bg)
d = ImageDraw.Draw(img)
def load_font(size, bold=False):
    cands = ["C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"]
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()
f_title_main = load_font(52, True)
f_phase = load_font(32, True)
f_card_title = load_font(29, True)
f_body = load_font(25, False)
f_num = load_font(34, True)
f_small = load_font(26, False)
d.text((60,30), "Digital Land Boundary Reconstruction & Verification — 19-Step Workflow", font=f_title_main, fill=navy)
d.text((60,95), "Clean print-friendly version  •  Survey No. 124/3 example  •  High-contrast, no photos", font=f_small, fill=(80,80,80))
d.line([(60,140),(W-60,140)], fill=light_border, width=2)
steps = [
 (1, "Collect Govt Records", ["Survey / Khasra number","Recorded area","Boundary measurements","Reference landmarks","Ownership details"]),
 (2, "Identify Reference Landmarks", ["Roads, canals, bridges","Buildings, trees, structures","Verify on ground"]),
 (3, "Extract Historical Measurements", ["Chain / tape distances","Bearings / directions","Relation with landmarks","A-B baseline, V1-V3"]),
 (4, "Plan Field Survey", ["Generate survey plan","Mark expected vertices","Assign survey team"]),
 (5, "Locate Physical Landmarks", ["Visit & identify landmarks","Survey using RTK GNSS","Record coords + photos","Verify with records"]),
 (6, "Reconstruct Historical Vertices", ["Use historical measurements","Intersect distances / directions","Compute A-B-V1 triangle"]),
 (7, "Modern Field Survey", ["Use RTK GNSS rover","Physically verify each vertex"]),
 (8, "Capture Precise Coordinates", ["Lat 23.456789, Lon 78.987654","Elev 412.3 m, Acc +/-0.02 m","Store time, accuracy, surveyor ID"]),
 (9, "Generate Digital Parcel Boundary", ["Connect surveyed vertices","Calculate area, perimeter","Create digital polygon"]),
 (10, "Compare Old vs New Records", ["Check area difference","Detect boundary displacement","Flag inconsistencies"]),
 (11, "Preliminary Digital Record", ["Old 1.65 ha / New 1.72 ha","Vertices V1-V5","Status: Pending Verification","Store coords, photos"]),
 (12, "Farmer Mobile Verification", ["View parcel on map","Phone GPS locate","Inspect boundary","Approve / Raise objection","Upload photos"]),
 (13, "Co-owner Verification", ["Owner A: Verified","Owner B: Verified","Owner C: Pending","Owner D: Not verified","Track request status"]),
 (14, "Neighbor Verification", ["Adjacent holders verify","Shared boundary check","Parcel A vs B / C","Confirm or object"]),
 (15, "Objections", ["Mark disputed vertex","Provide reason","Upload photo evidence","Request re-survey"]),
 (16, "Resolve Objections", ["Review records","Check measurements","Field re-verification","Correct / confirm boundary"]),
 (17, "Authority Review & Approval", ["Review records + evidence","Check all verifications","See objections / resurvey","Approve or modify"]),
 (18, "Final Digital Land Record", ["Final area 1.72 ha","Vertices V1-V5","Status: Verified & Approved","Link to land records"]),
 (19, "Audit Trail & Transparency", ["History, user / surveyor ID","GPS, date-time, measurements","Photos, verifications","Objections, final approval"]),
]
phases = [
 ("PHASE A — HISTORICAL RECORDS & FIELD PLANNING", [0,1,2,3,4], 5),
 ("PHASE B — RTK SURVEY & DIGITAL BOUNDARY", [5,6,7,8,9,10], 3),
 ("PHASE C — MULTI-STAKEHOLDER VERIFICATION", [11,12,13,14,15], 3),
 ("PHASE D — APPROVAL & FINAL RECORD", [16,17,18], 3),
]
def bullet_lines(b):
    bl=[]; cw=""
    for w_ in b.split():
        if len(cw+" "+w_)<30: cw=(cw+" "+w_).strip()
        else: bl.append(cw); cw=w_
    if cw: bl.append(cw)
    return bl
y = 170
gap = 20
for phase_title, idxs, cols in phases:
    d.rectangle([40, y, W-40, y+66], fill=phase_bg)
    d.text((60, y+12), phase_title, font=f_phase, fill=(255,255,255))
    y += 80
    rows = (len(idxs)+cols-1)//cols
    for r in range(rows):
        row_idxs = idxs[r*cols:(r+1)*cols]
        # compute needed height
        max_b = 0
        for si in row_idxs:
            _,_,bullets = steps[si]
            h_need = 110
            for b in bullets:
                h_need += len(bullet_lines(b))*31 + 9
            max_b = max(max_b, h_need)
        card_h = max_b + 25
        n = len(row_idxs)
        card_w = (W-80-gap*(cols-1))//cols
        for k, si in enumerate(row_idxs):
            num,title,bullets = steps[si]
            x0 = 40 + k*(card_w+gap)
            d.rounded_rectangle([x0, y, x0+card_w, y+card_h], radius=16, outline=light_border, width=3, fill=(255,255,255))
            cx,cy,rad = x0+42, y+42, 27
            d.ellipse([cx-rad,cy-rad,cx+rad,cy+rad], fill=navy)
            d.text((cx-13 if num<10 else cx-21, cy-23), str(num), font=f_num, fill=(255,255,255))
            # title wrap
            words=title.split(); lines=[]; cur=""
            for w_ in words:
                if len(cur+" "+w_)<22: cur=(cur+" "+w_).strip()
                else: lines.append(cur); cur=w_
            if cur: lines.append(cur)
            tx=x0+80; ty=y+10
            for li,ln in enumerate(lines[:2]):
                d.text((tx, ty+li*33), ln, font=f_card_title, fill=navy)
            d.line([(x0+18,y+92),(x0+card_w-18,y+92)], fill=light_border, width=2)
            by=y+105
            for b in bullets:
                d.text((x0+26, by), "•", font=f_body, fill=(0,0,0))
                for j,bl in enumerate(bullet_lines(b)):
                    d.text((x0+50, by+j*31), bl, font=f_body, fill=ink)
                by += len(bullet_lines(b))*31+9
            if k < n-1:
                ay=y+card_h//2; ax0=x0+card_w+2
                d.polygon([(ax0,ay-9),(ax0+15,ay),(ax0,ay+9)], fill=(60,120,200))
        y += card_h + gap
    y += 14
d.text((60, y+5), "Flow: 1-5 Records & Planning  >  6-11 RTK Survey & Digital Boundary  >  12-16 Verification & Objections  >  17-19 Approval & Audit", font=load_font(25, True), fill=navy)
img2 = img.crop((0,0,W, y+60))
img2.save("workflow_clean.png", dpi=(300,300))
print("saved", img2.size)

#!/usr/bin/env python3
"""Generate SVSGK project detail pages.

Edit PROJECTS below, then run:  python3 tools/build.py
Writes  <slug>/index.html  for each project (static HTML, no build deps).
Data was transcribed from the brochures in /brochures.
"""
import html, json, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE = "9849630690"
WA = f"https://wa.me/91{PHONE}"
SITE = "https://svsgkrealty.com"

# ---------------------------------------------------------------- icons
I = {
 "pin":   '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "grid":  '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 "road":  '<path d="M8 3 4 21M16 3l4 18M12 4v3M12 11v3M12 18v2"/>',
 "shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "bank":  '<path d="M3 10l9-6 9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 21h18"/>',
 "compass":'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
 "tree":  '<path d="M12 22v-6M7 16h10l-3-4h2l-4-6-4 6h2z"/>',
 "drop":  '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
 "tank":  '<rect x="6" y="3" width="12" height="9" rx="2"/><path d="M8 12l-2 9M16 12l2 9M7 17h10"/>',
 "bolt":  '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "walk":  '<circle cx="13" cy="4" r="2"/><path d="M10 22l2-7 3 3v4M8 12l3-4 4 3 3 1M12 15l-2-4"/>',
 "gym":   '<path d="M6 7v10M18 7v10M3 10v4M21 10v4M6 12h12"/>',
 "kids":  '<circle cx="12" cy="5" r="2.2"/><path d="M5 10h14M12 10v5M9 22l3-7 3 7"/>',
 "flower":'<circle cx="12" cy="9" r="2.5"/><path d="M12 6.5V3M14.5 9H18M12 11.5V14M9.5 9H6M12 14v8M12 18c-2.5 0-4-1.5-4-3.5M12 18c2.5 0 4-1.5 4-3.5"/>',
 "pipe":  '<path d="M3 8h8a3 3 0 0 1 3 3v10M3 12h6a1 1 0 0 1 1 1v8M14 3v4M18 21V11"/>',
 "gate":  '<path d="M3 21V9a9 9 0 0 1 18 0v12M7 21v-9M12 21v-9M17 21v-9"/>',
 "cam":   '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><circle cx="12" cy="11" r="2.5"/>',
 "path":  '<path d="M4 21c4-4 2-8 6-10s6-4 6-8M10 21c3-3 2-6 6-8s4-3 4-6"/>',
 "rain":  '<path d="M7 15a4 4 0 0 1 .5-8 5 5 0 0 1 9.5 1.5A3.5 3.5 0 0 1 17 15z"/><path d="M8 18l-1 3M12 18l-1 3M16 18l-1 3"/>',
 "trash": '<path d="M4 7h16M10 7V4h4v3M6 7l1 14h10l1-14"/>',
 "villa": '<path d="M3 11l9-7 9 7M5 9.5V21h14V9.5M10 21v-6h4v6"/>',
 "apt":   '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
 "light": '<path d="M12 3v2M5 12H3M21 12h-2M6.3 6.3 4.9 4.9M17.7 6.3l1.4-1.4"/><path d="M9 17a5 5 0 1 1 6 0v2H9z"/><path d="M10 22h4"/>',
 "land":  '<path d="M3 20l5-9 4 6 3-4 6 7z"/><circle cx="17" cy="6" r="2"/>',
 "sun":   '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5 19 19M5 19l1.5-1.5M17.5 6.5 19 5"/>',
 "home":  '<path d="M3 11l9-7 9 7v10H3z"/><path d="M9 21v-6h6v6"/>',
 "doc":   '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 13h6M9 17h6"/>',
}
def ico(k): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{I[k]}</svg>'

# ---------------------------------------------------------------- data
PROJECTS = [
 {
  "slug": "svs-gk-homes",
  "name": "SVS GK Homes",
  "tag": "Invest in land, invest in the future. A three-phase gated plotted layout inside Greater Warangal Municipal Corporation limits.",
  "loc": "Madikonda, Kazipet, Hanumakonda",
  "map_q": "Madikonda, Kazipet, Hanamkonda, Telangana",
  "hero": "svs-gk-homes/hero.webp",
  "ov_img": "svs-gk-homes/hero.webp", "ov_cap": "Entrance arch and avenue roads, artist's impression",
  "card": "svs-gk-homes/hero.webp",
  "summary": "Three-phase gated layout near Kazipet with roads up to 150 ft wide.",
  "intro": "SVS GK Homes is a KUDA-approved, TS RERA-registered plotted community in Madikonda village, Kazipet Mandal, under the Greater Warangal Municipal Corporation. Spread across three phases with 30 ft to 150 ft CC roads, it sits next to NH-163 and Kapil Homes, a short drive from Kazipet Railway Station, NIT Warangal and Madikonda IT Hub.",
  "approvals": [("Approval","KUDA Approved"),("TS RERA No.","P00300007874"),("Authority","GWMC Limits"),("Bank Loan","Available")],
  "facts": [
    ("pin","Location","Madikonda Village, Kazipet Mandal, Hanumakonda District"),
    ("grid","Plot sizes","33x60, 40x60, 45x60 and 30x60"),
    ("road","Internal roads","150 ft, 100 ft, 60 ft, 40 ft and 30 ft CC roads"),
    ("shield","Approvals","KUDA approved, TS RERA P00300007874"),
    ("bank","Finance","Bank loan available"),
  ],
  "stats": [("3","Phases"),("480+","Plots"),("150 FT","Main Road"),("100%","Vaastu")],
  "location": {
    "Connectivity": ["Just 4 km from Kazipet Railway Station","Adjacent to National Highway 163","Proposed 150 ft & 100 ft roads as per Master Plan 2041","6 km from Warangal Urban Collector Office"],
    "Education": ["Very near to Sainik School & Hyderabad Public School","Just 5 km to NIT Warangal","Near Talla Padmavathi Engineering College","Just 7 km to Kakatiya University","Walkable distance to schools & engineering colleges"],
    "Work & Living": ["Near Madikonda IT Hub","Near by IT companies","Adjacent to Kapil Homes","Under Greater Warangal Municipal Corporation","Suitable for immediate house construction"],
  },
  "amenities": [
    ("road","150', 100', 60', 40' & 30' CC roads"),("compass","100% Vaastu plots"),("tree","Avenue plantation with drip system"),
    ("tank","4 lakh litre overhead water tank"),("light","Central lighting & full electricity"),("walk","Walking track"),
    ("gym","Gym centre"),("kids","Children's gaming zone"),("flower","Parks, lawns & flower plantation"),
    ("pipe","Underground drainage & water pipelines"),("gate","Elevated main gate with arch"),("cam","24 hrs security & solar fencing"),
    ("path","Footpaths with curb stones"),("rain","Water harvesting pits"),("trash","Separate garbage area"),
  ],
  "layout": "svs-gk-homes/layout.webp",
  "lps": [("Phase I","LP No. 0276/LO/3006/2022","File No. 012210/LO/DTCP/3006/0421/2024"),
          ("Phase II","LP No. 0027/LO/3006/2024","File No. 000534/LO/DTCP/3006/0020/2024"),
          ("Phase III","LP No. 0114/LO/3006/2024","File No. 003012/LO/DTCP/3006/0103/2024")],
  "survey": "Sy. Nos. 398/A, 398/A1, 398/B/1/1, 398/B/1/4, 398/C/2, 398/D, 410/A, 411/C/3, 412/C/1 and others, Madikonda Village, Kazipet Mandal, Hanumakonda District.",
  "gallery": [("svs-gk-homes/hero.webp","Layout entrance, artist's impression"),("svs-gk-homes/g1.webp","Kakatiya University, 7 km"),
              ("svs-gk-homes/g2.webp","Nearby landmark"),("svs-gk-homes/g3.webp","Madikonda IT Hub"),("svs-gk-homes/g4.webp","Model villa elevation")],
  "brochure": "svs-gk-homes.pdf",
  "developer": "SVS GK Developers & Constructions",
 },
 {
  "slug": "deva-deva-dream-homes",
  "name": "Deva Deva Dream Homes",
  "tag": "A 10-acre KUDA-approved layout facing the Madikonda to Dharmasagar 100 ft road.",
  "loc": "Madikonda, Kazipet, Hanumakonda",
  "map_q": "Madikonda, Kazipet, Hanamkonda, Telangana",
  "hero": "deva-deva-dream-homes/hero.webp",
  "ov_img": "deva-deva-dream-homes/hero.webp", "ov_cap": "Deva Deva Dream Homes main gate, artist's impression",
  "card": "deva-deva-dream-homes/hero.webp",
  "summary": "10 acres on the Madikonda to Dharmasagar 100 ft road, beside Kapil Homes.",
  "intro": "Deva Deva Dream Homes is a 10-acre gated plotted layout approved by the Kakatiya Urban Development Authority. It faces the main Madikonda to Dharmasagar 100 ft road, right beside Kapil Homes, inside Greater Warangal Municipal Corporation limits. Every internal road is a 40 ft M-30 grade CC road and all plots are 100% Vaastu.",
  "approvals": [("Approval","KUDA Approved"),("LP No.","0064/LO/3006/2025"),("Land","10 Acres"),("Bank Loan","Available")],
  "facts": [
    ("pin","Location","Madikonda (V), Kazipet (M), Hanumakonda District"),
    ("grid","Plot sizes","36x60, 45x60 and 40x60"),
    ("road","Internal roads","All 40 ft M-30 grade CC roads"),
    ("shield","Approvals","KUDA approved, LP No. 0064/LO/3006/2025"),
    ("bank","Finance","Bank loan available"),
  ],
  "stats": [("10","Acres"),("110","Plots"),("40 FT","CC Roads"),("100%","Vaastu")],
  "location": {
    "Connectivity": ["Facing the Madikonda to Dharmasagar 100 ft road","Just 4 km from Kazipet Railway Station","Adjacent to National Highway 163 (KUDA Outer Ring Road)","6 km from Warangal Urban Collector Office"],
    "Education": ["Very near to Sainik School & Hyderabad Public School","Close to Delhi Public School, Karunapuram","Just 5 km to NIT Warangal","Just 7 km to Kakatiya University","Walkable distance to schools & engineering colleges"],
    "Work & Living": ["Beside Kapil Homes on Dharmasagar Road","Near Madikonda IT Hub","Within Greater Warangal Municipal Corporation limits","Suitable for immediate house construction"],
  },
  "amenities": [
    ("road","40 ft M-30 grade CC roads"),("compass","100% Vaastu plots"),("tree","Avenue plantation with drip system"),
    ("tank","2 lakh litre overhead water tank"),("bolt","Full electricity"),("walk","Walking track"),
    ("kids","Children's gaming zone"),("flower","Parks, lawns & flower plantation"),("pipe","Underground drainage & water pipelines"),
    ("gate","Elevated main gate with arch"),("cam","24 hrs security & solar fencing"),("path","Footpaths with curb stones"),
    ("rain","Water harvesting pits"),("trash","Separate garbage area"),
  ],
  "layout": "deva-deva-dream-homes/layout.webp",
  "lps": [("Layout","LP No. 0064/LO/3006/2025","Kakatiya Urban Development Authority")],
  "survey": "Sy. Nos. 262/A, 262/A1, 263/A, 263/A1, 270/A, 270/A1, 271/A, 271/B, 271/C1, 271/C2, 272/A, 272/B, 272/C1, 272/C2, 273/A, 273/B, 273/C/1, 273/C/2, Madikonda Village, Kazipet Mandal, Hanumakonda District.",
  "map_img": "deva-deva-dream-homes/map.webp",
  "gallery": [("deva-deva-dream-homes/hero.webp","Main gate, artist's impression"),("deva-deva-dream-homes/g1.webp","Planned row villas"),
              ("deva-deva-dream-homes/g2.webp","Model house elevation"),("deva-deva-dream-homes/map.webp","Location map")],
  "brochure": "deva-deva-dream-homes.pdf",
  "developer": "Deva Deva Developers",
 },
 {
  "slug": "svs-gk-county",
  "name": "SVS GK County",
  "tag": "Find your dream fulfilled in this ideal environment. 140 Vaastu plots, 2 km from the Outer Ring Road.",
  "loc": "Madikonda, Kazipet, Hanamkonda",
  "map_q": "Madikonda, Kazipet, Hanamkonda, Telangana",
  "hero": "../hero.webp",
  "ov_img": "svs-gk-county/g3.webp", "ov_cap": "Upcoming planned villa houses, artist's impression",
  "card": "svs-gk-county/g3.webp",
  "summary": "140 Vaastu plots, 2 km from Kazipet Railway Station and the ORR.",
  "intro": "SVS GK County is a KUDA-approved gated community in Madikonda village, within Greater Warangal Municipal Corporation limits. With 33 ft and 40 ft M-20 grade CC roads, Mission Bhagiratha pipelines and planned villas and apartments, it is 2 km from both Kazipet Railway Station and the Outer Ring Road.",
  "approvals": [("Approval","KUDA Approved"),("LP No.","0017/GWMC/SWDL/2025"),("Member","CREDAI"),("Bank Loan","Available")],
  "facts": [
    ("pin","Location","Madikonda (V), Kazipet (M), Hanamkonda District"),
    ("grid","Plot sizes","30x55, 30x60 and 40x60"),
    ("road","Internal roads","All 33 ft & 40 ft CC (M-20 grade) roads"),
    ("shield","Approvals","KUDA approved, LP No. 0017/GWMC/SWDL/2025"),
    ("bank","Finance","Bank loan available, CREDAI member"),
  ],
  "stats": [("140+","Plots"),("2 KM","To ORR"),("40 FT","CC Roads"),("100%","Vaastu")],
  "location": {
    "Connectivity": ["Just 2 km from Kazipet Railway Station","Just 2 km to Outer Ring Road (ORR)","Existing 60 ft road, to be widened as per Master Plan 2041","4 km from Warangal Urban Collector Office"],
    "Education": ["4 km to Hyderabad Public School","Just 3 km to NIT Warangal","Just 6 km to Kakatiya University","Near Delhi Public School & Raman School","Walkable distance to schools & engineering colleges"],
    "Work & Living": ["Near Madikonda IT Hub","Under Kakatiya Urban Development Authority","Within Greater Warangal Municipal Corporation limits","Suitable for immediate house construction"],
  },
  "amenities": [
    ("road","33' & 40' CC (M-20) roads"),("compass","100% Vaastu plots"),("tree","Avenue plantation with drip system"),
    ("land","Full landscaping"),("tank","2 lakh litre OHT & sump"),("bolt","Electricity lines in the venture"),
    ("flower","Parks, lawns & flower plantation"),("pipe","Underground drainage & water pipelines"),("drop","Mission Bhagiratha pipelines"),
    ("gate","Elevated main gate with arch"),("cam","24 hrs security & solar fencing"),("path","Footpaths with curb stones"),
    ("villa","Upcoming planned villas"),("apt","Upcoming planned apartments"),("rain","Water harvesting pits"),("trash","Separate garbage area"),
  ],
  "layout": "svs-gk-county/layout.webp",
  "lps": [("Layout","LP No. 0017/GWMC/SWDL/2025","Application No. 005764/GWMC/00125/SWDL/2025")],
  "survey": "Sy. Nos. 141/B1, 134/B1, 142/B1, 132/A, 132/B, 133/B, 133/A, 134/A, 141/A, 142/A, 134/B, 141/B/1, 141/B/2, 142/B2, Madikonda Village, Kazipet Mandal, Hanamakonda District.",
  "map_img": "svs-gk-county/map.webp",
  "gallery": [("svs-gk-county/g1.webp","Planned villa, elevation 1"),("svs-gk-county/g2.webp","Planned villa, elevation 2"),
              ("svs-gk-county/g3.webp","Planned villa, elevation 3"),("svs-gk-county/map.webp","Location map")],
  "brochure": "svs-gk-county.pdf",
  "developer": "SVS GK Developers",
 },
 {
  "slug": "kakatiya-vantage",
  "name": "Kakatiya Vantage",
  "tag": "A right choice for your big dreams. A highway-facing layout on the 200 ft Hyderabad to Warangal road.",
  "loc": "Chinnapendyala, Ghanpur, Jangaon",
  "map_q": "Chinnapendyala, Ghanpur, Telangana",
  "hero": "kakatiya-vantage/hero.webp",
  "ov_img": "kakatiya-vantage/hero.webp", "ov_cap": "Kakatiya Vantage entrance, artist's impression",
  "card": "kakatiya-vantage/hero.webp",
  "summary": "Highway-facing layout with 484 plots near Ghanpur Railway Station.",
  "intro": "Kakatiya Vantage is a large highway-facing plotted layout at Chinnapendyala, Ghanpur, along the proposed 200 ft Hyderabad to Warangal road as per Master Plan 2041. Approved by the Kakatiya Urban Development Authority, it offers 33x55 Vaastu plots with 30 ft to 100 ft CC roads, UPVC drainage and Mission Bhagiratha lines.",
  "approvals": [("Approval","KUDA Approved"),("LTP No.","265852/LP/GP/213547/0003/2023"),("Member","CREDAI"),("Bank Loan","Available")],
  "facts": [
    ("pin","Location","Chinnapendyala, Ghanpur, Jangaon District"),
    ("grid","Plot size","33x55"),
    ("road","Internal roads","30', 40', 50', 60' & 100' CC roads"),
    ("shield","Approvals","KUDA approved, LTP No. 265852/LP/GP/213547/0003/2023"),
    ("bank","Finance","Bank loan available, CREDAI member"),
  ],
  "stats": [("484","Plots"),("200 FT","Highway"),("100 FT","Main Road"),("100%","Vaastu")],
  "location": {
    "Connectivity": ["Highway-facing layout on the Hyderabad to Warangal road","Just 2 km from Ghanpur Railway Station","Just 5 km to Outer Ring Road","Just 15 km to Kazipet Railway Station"],
    "Education": ["Near by Delhi Public School","Just 6 km to NIT Warangal","Walkable distance to schools & engineering colleges","Near Little Flower High School"],
    "Work & Living": ["Near Sub Registrar Office, Ghanpur","Near Madikonda IT Hub","1 km to Chinnapendyala village","Under Kakatiya Urban Development Authority","Suitable for immediate house construction"],
  },
  "amenities": [
    ("road","30' to 100' CC roads"),("compass","100% Vaastu plots"),("tree","Avenue plantation with drip system"),
    ("land","Full landscaping"),("bolt","Overhead electricity cable system"),("flower","Parks, lawns & flower plantation"),
    ("pipe","UGD & UPVC water pipelines"),("drop","Mission Bhagiratha UPVC lines"),("gate","Elevated main gate with arch"),
    ("cam","24 hrs security & solar fencing"),("path","Footpaths with curb stones"),("villa","Upcoming planned villas"),
    ("apt","Upcoming planned apartments"),("rain","Water harvesting pits"),("trash","Separate garbage area"),
  ],
  "layout": "kakatiya-vantage/layout.webp",
  "lps": [("Layout","LTP No. 265852/LP/GP/213547/0003/2023","Kakatiya Urban Development Authority")],
  "survey": "Sy. Nos. 286/B, 287/B, 288/A1, 288/A/2, 288/C/1 and others of Ghanpur (V&M); 252/C/2, 257/2/1/1 and others of Chinnapendyala Village; 231/B, 232/C/2/1 and others of Rajavaram Village, Chilpur Mandal, Jangaon District.",
  "map_img": "kakatiya-vantage/map.webp",
  "gallery": [("kakatiya-vantage/hero.webp","Entrance plaza, artist's impression"),("kakatiya-vantage/g1.webp","Model villa elevation"),
              ("kakatiya-vantage/g2.webp","Hyderabad to Warangal highway"),("kakatiya-vantage/g3.webp","Nearby landmark"),
              ("kakatiya-vantage/g4.webp","Ghanpur Railway Station")],
  "brochure": "kakatiya-vantage.pdf",
  "developer": "Akshitha Developers",
 },
]

# ---------------------------------------------------------------- build
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import render, card

def main():
    for p in PROJECTS:
        others = [o for o in PROJECTS if o is not p]
        d = os.path.join(ROOT, p["slug"]); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as f: f.write(render(p, others, I))
        print("wrote", p["slug"])
    lp = os.path.join(ROOT, "index.html"); t = open(lp).read()
    a = t.index("<!-- cards:start -->") + len("<!-- cards:start -->"); b = t.index("<!-- cards:end -->")
    t = t[:a] + "\n" + "\n".join(card(p, "") for p in PROJECTS) + "\n" + t[b:]
    open(lp, "w").write(t); print("wrote listing cards")

if __name__ == "__main__":
    main()

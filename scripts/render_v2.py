"""Enhanced SVG renderer: dark theme and CJK-aware text wrapping."""
import html, json, sys, unicodedata
from pathlib import Path
from validate import validate

def units(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)

def wrap(s, limit=28):
    result=[]; line=""
    for paragraph in str(s).split("\n"):
        for word in paragraph.split(" "):
            candidate=(line+" "+word).strip()
            if line and units(candidate)>limit:
                result.append(line); line=""
            for char in word:
                if line and units(line+char)>limit:
                    result.append(line); line=""
                line+=char
            if units(line)<limit: line+=" "
        result.append(line.strip()); line=""
    return result

def render(d, theme="light"):
    errors=validate(d)
    if errors: raise ValueError("; ".join(errors))
    if theme not in ("light","dark"): raise ValueError("Unknown theme")
    dark=theme=="dark"
    bg,card,accent,ink,muted,stroke=("#101722","#1B2635","#203754","#F0F5FC","#A9B9CB","#34445A") if dark else ("#F7F9FC","#FFFFFF","#EDF4FF","#142338","#526276","#DDE5EF")
    direction=d.get("direction","TB"); layers=d["layers"]; nodes={n["id"]:n for n in d["nodes"]}
    w,h,g,lg,m,header=260,110,24,92,52,122; count=max(map(len,layers))
    W=max(760,count*w+(count-1)*g+2*m) if direction=="TB" else 2*m+len(layers)*w+(len(layers)-1)*lg
    H=header+len(layers)*h+(len(layers)-1)*lg+m if direction=="TB" else header+count*h+(count-1)*g+m
    pos={}
    for i,layer in enumerate(layers):
        for j,key in enumerate(layer):
            if direction=="TB":
                span=len(layer)*w+(len(layer)-1)*g; x=(W-span)/2+j*(w+g); y=header+i*(h+lg)
            else:
                span=len(layer)*h+(len(layer)-1)*g; x=m+i*(w+lg); y=header+(count*h+(count-1)*g-span)/2+j*(h+g)
            pos[key]=(x,y)
    e=lambda s:html.escape(str(s),quote=True)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(d["title"])}">',
         f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{muted}"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<text x="{m}" y="48" font-family="Noto Sans, sans-serif" font-size="24" font-weight="700" fill="{ink}">{e(d["title"])}</text>',
         f'<text x="{m}" y="74" font-family="Noto Sans, sans-serif" font-size="12" fill="{muted}">{e(d.get("subtitle",""))}</text>']
    for edge in d.get("edges",[]):
        a,b=pos[edge["from"]],pos[edge["to"]]
        if direction=="TB":
            x1,y1,x2,y2=a[0]+w/2,a[1]+h,b[0]+w/2,b[1]; mid=(y1+y2)/2
            path=f'M{x1:.1f},{y1:.1f} V{mid:.1f} H{x2:.1f} V{y2-7:.1f}'
        else:
            x1,y1,x2,y2=a[0]+w,a[1]+h/2,b[0],b[1]+h/2; mid=(x1+x2)/2
            path=f'M{x1:.1f},{y1:.1f} H{mid:.1f} V{y2:.1f} H{x2-7:.1f}'
        out.append(f'<path d="{path}" fill="none" stroke="{muted}" stroke-width="1.6" marker-end="url(#arrow)"/>')
    for key,(x,y) in pos.items():
        n=nodes[key]; active=n.get("accent",False); fill=accent if active else card
        out.append(f'<g id="node-{e(key)}"><rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="13" fill="{fill}" stroke="{stroke}"/>')
        out.append(f'<rect x="{x+16:.1f}" y="{y+20:.1f}" width="4" height="46" rx="2" fill="#72A9F4"/>')
        labels=wrap(n["label"],27)[:2]
        for i,t in enumerate(labels):
            out.append(f'<text x="{x+33:.1f}" y="{y+33+i*18:.1f}" font-family="Noto Sans, sans-serif" font-size="15" font-weight="600" fill="{ink}">{e(t)}</text>')
        for i,t in enumerate(wrap(n.get("subtitle",""),36)[:2]):
            out.append(f'<text x="{x+33:.1f}" y="{y+35+len(labels)*18+i*15:.1f}" font-family="Noto Sans, sans-serif" font-size="11" fill="{muted}">{e(t)}</text>')
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("output"); p.add_argument("--theme",choices=["light","dark"],default="light")
    a=p.parse_args(); dest=Path(a.output); dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(render(json.loads(Path(a.input).read_text(encoding="utf-8")),a.theme),encoding="utf-8")
    print("Rendered",dest)

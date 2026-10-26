# Re-rig Tripo's "tommy model 2.glb" for the game:
#  - its template skeleton faces +x; turn it to face +z like the mesh: (x,y,z) -> (-z, y, x)
#  - bones get pure translations (identity rest rotations) and matching inverse bind matrices
#  - names lose the "mixamorig:" prefix (Hips, Spine, LeftArm...)
#  - skin weights are recomputed: nearest bone segments, 1/d^4 falloff, best 4
import json,struct,sys,math
src,dst=sys.argv[1],sys.argv[2]
d=open(src,'rb').read()
L=struct.unpack('<I',d[12:16])[0]; j=json.loads(d[20:20+L]); h=20+L; BL=struct.unpack('<I',d[h:h+4])[0]
B=bytearray(d[h+8:h+8+BL])
nodes=j['nodes']; s=j['skins'][0]
def view(i):
  a=j['accessors'][i]; bv=j['bufferViews'][a['bufferView']]; o=bv.get('byteOffset',0)+a.get('byteOffset',0)
  ct={5126:'f',5121:'B',5123:'H'}[a['componentType']]; n={'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]; sz=struct.calcsize(ct)*n
  return o,bv.get('byteStride',sz),ct,n,sz,a['count']
def read(i):
  o,st,ct,n,sz,c=view(i); return [struct.unpack('<'+ct*n,B[o+k*st:o+k*st+sz]) for k in range(c)]
def write(i,rows):
  o,st,ct,n,sz,c=view(i)
  for k,r in enumerate(rows): B[o+k*st:o+k*st+sz]=struct.pack('<'+ct*n,*r)
parent={c:i for i,n in enumerate(nodes) for c in n.get('children',[])}
ibm=read(s['inverseBindMatrices'])
world={}
for k,jn in enumerate(s['joints']):
  m=ibm[k]; R=[[m[0],m[4],m[8]],[m[1],m[5],m[9]],[m[2],m[6],m[10]]]; t=[m[12],m[13],m[14]]
  x,y,z=[-sum(R[q][i]*t[q] for q in range(3)) for i in range(3)]
  world[jn]=[-z,y,x]
def wpos(i):
  if i in world: return world[i]
  p=parent.get(i); return wpos(p) if p is not None else [0,0,0]
idx={n['name'].replace('mixamorig:',''):i for i,n in enumerate(nodes)}
# end bones that carry no bind matrix: put them where the mesh ends
P=read(j['meshes'][0]['primitives'][0]['attributes']['POSITION'])
top=max(v[1] for v in P); handTip=max(v[0] for v in P)
world[idx['HeadTop_End']]=[wpos(idx['Head'])[0], top, wpos(idx['Head'])[2]]
for sd,sg in (('Left',1),('Right',-1)):
  hw=wpos(idx[sd+'Hand']); world.setdefault(idx[sd+'HandMiddle4'],[sg*handTip,hw[1],hw[2]])
# the template skeleton isn't fitted to this body: centre each joint in the limb or torso slice around it
def centroid(f):
  q=[v for v in P if f(v)]
  return [sum(v[i] for v in q)/len(q) for i in range(3)] if q else None
def fit(nm, axes, f):
  i=idx[nm]; w=wpos(i); c=centroid(lambda v: f(v,w))
  if c:
    for a in axes: w[a]=c[a]
  world[i]=w
for nm in ('Hips','Spine','Spine1','Spine2','Neck','Head'):
  fit(nm,(0,2),lambda v,w: abs(v[1]-w[1])<.012 and abs(v[0])<.12)
for sd,sg in (('Left',1),('Right',-1)):
  side=lambda v,sg=sg: v[0]*sg>.005 and abs(v[0])<.2
  fit(sd+'UpLeg',(0,2),lambda v,w,side=side: side(v) and abs(v[1]-(w[1]-.03))<.012)
  fit(sd+'Leg',(0,2),lambda v,w,side=side: side(v) and abs(v[1]-w[1])<.012)
  old=list(wpos(idx[sd+'Foot']))
  fit(sd+'Foot',(0,2),lambda v,w,side=side: side(v) and w[1]+.01<v[1]<w[1]+.03)
  nw=wpos(idx[sd+'Foot'])
  for t in ('ToeBase','Toe_End'):
    p=wpos(idx[sd+t]); world[idx[sd+t]]=[p[0]+nw[0]-old[0],p[1],p[2]+nw[2]-old[2]]
  for nm in (sd+'Arm',sd+'ForeArm',sd+'Hand'):
    fit(nm,(1,2),lambda v,w: abs(v[0]-w[0])<.01 and v[1]>.6)
  hw=wpos(idx[sd+'Hand']); world[idx[sd+'HandMiddle4']]=[sg*handTip,hw[1],hw[2]]
for nm in ('Hips','LeftUpLeg','LeftLeg','LeftFoot','LeftArm','LeftForeArm','LeftHand','Spine2'): print(nm,[round(x,3) for x in wpos(idx[nm])])
isBone={i for i,n in enumerate(nodes) if n['name'].startswith('mixamorig:')}
for i,n in enumerate(nodes):
  if i not in isBone: continue
  p=parent.get(i); pw=wpos(p) if p in isBone else [0,0,0]
  w=wpos(i); n['translation']=[w[q]-pw[q] for q in range(3)]
  n['name']=n['name'].replace('mixamorig:','')
jid={nodes[jn]['name']:k for k,jn in enumerate(s['joints'])}
write(s['inverseBindMatrices'],[[1,0,0,0,0,1,0,0,0,0,1,0,-world[jn][0],-world[jn][1],-world[jn][2],1] for jn in s['joints']])
W=lambda nm: wpos(idx[nm])
segs=[('Hips','Hips','Spine'),('Spine','Spine','Spine1'),('Spine1','Spine1','Spine2'),('Spine2','Spine2','Neck'),('Neck','Neck','Head'),('Head','Head','HeadTop_End')]
for sd in ('Left','Right'):
  segs+= [(sd+'Shoulder',sd+'Shoulder',sd+'Arm'),(sd+'Arm',sd+'Arm',sd+'ForeArm'),(sd+'ForeArm',sd+'ForeArm',sd+'Hand'),(sd+'Hand',sd+'Hand',sd+'HandMiddle4'),
          (sd+'UpLeg',sd+'UpLeg',sd+'Leg'),(sd+'Leg',sd+'Leg',sd+'Foot'),(sd+'Foot',sd+'Foot',sd+'ToeBase'),(sd+'ToeBase',sd+'ToeBase',sd+'Toe_End')]
segs=[(jid[b],W(a),W(c)) for b,a,c in segs]
hipY=W('Hips')[1]
def dist(v,a,b):
  ab=[b[i]-a[i] for i in range(3)]; av=[v[i]-a[i] for i in range(3)]; L2=sum(x*x for x in ab) or 1e-9
  t=max(0,min(1,sum(ab[i]*av[i] for i in range(3))/L2)); return math.sqrt(sum((av[i]-t*ab[i])**2 for i in range(3)))
J=[];Wt=[]
for v in P:
  cand=[]
  for k,a,b in segs:
    dd=dist(v,a,b)
    nm=nodes[s['joints'][k]]['name']
    # keep the legs apart: a vertex never takes the other side's leg; below the hips nothing goes to the arms
    if 'Leg' in nm or 'Foot' in nm or 'Toe' in nm:
      if (nm.startswith('Left') and v[0] < -.01) or (nm.startswith('Right') and v[0] > .01): continue
    if v[1] < hipY-.02 and ('Arm' in nm or 'Hand' in nm or 'Shoulder' in nm): continue
    cand.append((dd,k))
  cand.sort(); best=cand[:4]; d0=max(best[0][0],.004)
  ws=[(d0/max(dd,.004))**4 for dd,_ in best]; ws=[w if w>.02 else 0 for w in ws]; t=sum(ws)
  J.append([k for _,k in best]); Wt.append([w/t for w in ws])
att=j['meshes'][0]['primitives'][0]['attributes']
write(att['JOINTS_0'],J); write(att['WEIGHTS_0'],Wt)
js=json.dumps(j,separators=(',',':')).encode(); js+=b' '*((4-len(js)%4)%4); B+=b'\0'*((4-len(B)%4)%4)
out=struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(B))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(B),0x004E4942)+bytes(B)
open(dst,'wb').write(out); print('wrote',len(out),'joints fmt',j['accessors'][att['JOINTS_0']]['componentType'])

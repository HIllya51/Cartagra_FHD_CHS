with open('../uitext.txt','r',encoding='utf8') as ff:
    lines=ff.read().split('\n') 
with open('./names.txt','r',encoding='utf8') as ff:
    names=ff.read().split('\n') 
nametouitext={}
for i in range(len(names)-1):
    if i%3!=0:continue
    nametouitext[names[i][3:]]=names[i+1][3:]
cnt=0
for i in range(len(lines)-1):
    if i%3!=0:continue
    if lines[i][-1]=='-':
        #print(lines[i][7:-1] )
        if lines[i][7:-1] in nametouitext:
            #print(nametouitext[lines[i][7:-1]])
            lines[i+1]=lines[i+1][:7]+nametouitext[lines[i][7:-1]]
        if 'その他\\'+lines[i][7:-1] in nametouitext:
            #print(nametouitext['その他\\'+lines[i][7:-1]][3:])
            lines[i+1]=lines[i+1][:7]+nametouitext['その他\\'+lines[i][7:-1]][3:]
with open('../uitext.txt','w',encoding='utf8') as ff:
    ff.write('\n'.join(lines))

with open(r'C:\InnocentGrey\カルタグラ FHD\files\PARAM\_voice_param','rb') as ff:
    bs=ff.read()
import json
with open('../font/remap_charset2.txt','r',encoding='utf8') as ff:
    remap_charset2=json.load(ff) 
import ctypes 
voicenum=ctypes.c_uint.from_buffer_copy(bs[0:4]).value
print(voicenum)
idx=4 
#pf=open('names.txt','w',encoding='utf8')

for i in range((voicenum)):
    for j in range(1000):
        if bs[idx+j]==0:
            name=bs[idx:idx+j]
            idx+=j+1
            break
    print(i,name.decode('utf8'))
    #print('%02x|%s'%(i,name.decode('utf8')),file=pf)
    #print('%02x|%s'%(i,name.decode('utf8')),file=pf)
    #print('',file=pf)
appendix=bs[idx:]
newbs=b''
newbs+=bs[0:4]
for i in range(voicenum):
    text=list(names[i*3+1][3:]) 
        
    for ii in range(len(text)): 
        text[ii]=remap_charset2.get(text[ii],text[ii])
    trans2=''.join(text) 
    newbs+=trans2.encode('utf8')
    newbs+=b'\x00'
newbs+=appendix
with open(r'C:\InnocentGrey\カルタグラ FHD\files\PARAM_NEW\_voice_param','wb') as ff:
    ff.write(newbs)
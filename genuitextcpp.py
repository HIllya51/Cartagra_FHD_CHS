import json
with open('uitext.txt','r',encoding='utf8') as ff:
    lines=ff.read().split('\n') 
with open('font/remap_charset2.txt','r',encoding='utf8') as ff:
    remap_charset2=json.load(ff) 
pf=open('patch/uitext.cpp','w',encoding='utf-8-sig')
print('''
#include<vector> 
std::vector<std::pair<int,const char*>>uitexts={
''',file=pf)
 
for i in range(len(lines)):
    if i%3!=1:continue
    addr=lines[i][:6]
    _addr=int(addr,16)
    trans=lines[i][7:]
    origin=lines[i-1][7:]
    # if _addr>=0x3FF150 and _addr<=0x3FF390:
    #     #print(origin)
    #     continue
    if _addr==0:continue
    if  origin!=trans:
        trans=trans.replace('＄','\\n')
        text=list(trans) 
         
        for ii in range(len(text)): 
            text[ii]=remap_charset2.get(text[ii],text[ii])
        trans2=''.join(text) 
        #print(addr,origin,trans)
         
        print('{0x'+addr+',u8"'+trans2+'"},',file=pf)
print('};',file=pf) 
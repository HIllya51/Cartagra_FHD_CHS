import json
with open('uitext.txt','r',encoding='utf8') as ff:
    lines=ff.read().split('\n') 
with open('font/remap_charset2.txt','r',encoding='utf8') as ff:
    remap_charset2=json.load(ff) 
with open('font/remap_charset4.txt','r',encoding='utf8') as ff:
    remap_charset4=json.load(ff) 
pf=open('patch/uitext.cpp','w',encoding='utf-8-sig')
pf2=open('patch/erroruitext.cpp','w',encoding='utf-8-sig')
print('''
#include<vector> 
std::vector<std::pair<int,const char*>>uitexts={
''',file=pf)
print('''
#include<unordered_map> 
#include<string> 
std::unordered_map<std::wstring,std::wstring>erroruitext={
''',file=pf2)
for i in range(len(lines)):
    if i%3!=1:continue
    addr=lines[i][:6]
    _addr=int(addr,16)
    trans=lines[i][7:]
    origin=lines[i-1][7:]
    if _addr>=0x3FF150 and _addr<=0x3FF390:
        #print(origin)
        continue
    if _addr in []:
        _map=remap_charset2
    else:
        _map=remap_charset4
    if  origin!=trans:
        trans=trans.replace('＄','\\n')
        text=list(trans) 
        for ii in range(len(text)): 
            text[ii]=remap_charset4.get(text[ii],text[ii])
        trans1=''.join(text) 
        text=list(trans) 
        for ii in range(len(text)): 
            text[ii]=remap_charset2.get(text[ii],text[ii])
        trans2=''.join(text) 
        #print(addr,origin,trans)
        if '【' not in  trans and (not (_addr<=0x401220 and _addr>=0x400900)):
            print(hex(_addr),trans)
            print('{L"'+trans1.replace('\n','\\n')+'",L"'+trans2.replace('\n','\\n')+'"},',file=pf2)
        print('{0x'+addr+',u8"'+trans1+'"},',file=pf)
print('};',file=pf)
print('};',file=pf2)
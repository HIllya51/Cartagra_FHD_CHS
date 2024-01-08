import os ,ctypes,json
mymap={}
with open('font/remap_charset2.txt','r',encoding='utf8') as ff:
    remap_charset2=json.load(ff) 
pf=open('patch/tolongtexts.cpp','w',encoding='utf-8-sig')
print('''
#include<unordered_map> 
#include<string> 
std::unordered_map<std::wstring,std::wstring>trans={
''',file=pf)
cnt=0
for f in os.listdir('SCRIPT_FHD/text'):
    #if f!='0206-05-03':continue
    #if f!='0000-op0_HD':continue
    #print(f)
    with open('SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
        lines=ff.read().split('\n')
    with open('SCRIPT_FHD/SCRIPT_FHD/'+f,'rb') as ff:
        cankao=ff.read()
    for i in range(len(lines)-1):
        if len(lines[i])==0:continue
        #i=len(lines)-1-_i
        if i%3!=1:continue
        idx=int(lines[i][:4],16)
        originlength=ctypes.c_ushort.from_buffer_copy(cankao[idx:idx+2]).value
        text=lines[i][5:].replace('＄','\n').replace('―','—')
        origin=lines[i-1][5:].replace('＄','\n')
        #print(text)
        
        # if len(text)>originlength:
        #     print(text)
        
        #
        #print(text)
        text_save=text
        text=list(text)
        for ii in range(len(text)):
            text[ii]=remap_charset2.get(text[ii],text[ii])
        text=''.join(text) 
        length=len(text)  
        #text=text[:originlength]
        if originlength!=length and (('$d' in text_save ) or (f=='0206-10-00' and  text_save[-1]=='\n')):
            #print(text)
            length+=999
            if text_save[-1]=='\n' :
                text=text[:-1]+' \n'
        
        if originlength>=length:
            while length<originlength:
                if text[-1]=='\n':
                    text=text[:-1]+' '+'\n'
                else:
                    text+=' '
                length+=1
            
            saveend=cankao[idx+2+originlength*2+2:]  
            #print(bytes(saveend)[:30].hex())
            cankao=cankao[:idx]
            cankao+=(length.to_bytes(2,'little'))
            cankao+=(text.encode('utf-16-le')+b'\x00\x00') 
            cankao+=saveend 
        else:
            _1=origin.split("$d")
            _2=text.split("$d")
            if len(_1)!=len(_2):
                raise Exception(f,origin,text)
            for i in range(len(_1)):
                if _1[i] in mymap:
                    if mymap[_1[i]]==_2[i]:
                        continue
                
                mymap[_1[i]]=_2[i]
                cnt+=1
                print('{L"'+_1[i].replace('\n','\\n')+'",L"'+_2[i].replace('\\','\\\\').replace('\n','\\n')+'"},',file=pf)
    with open('SCRIPT_FHD/SCRIPT_FHD_transed/'+f,'wb') as ff:
        ff.write(bytes(cankao))
# with open(r'C:\InnocentGrey\カルタグラ FHD\trans.json','w',encoding='utf8') as ff:
#     ff.write(json.dumps(mymap,ensure_ascii=False,indent=4))

print('};',file=pf)
print(cnt,len(mymap))

with open('SCRIPT_FHD/text/_varstr','r',encoding='utf8') as ff:
    lines=ff.read().split('\n')
with open('SCRIPT_FHD/SCRIPT_FHD/_varstr','rb') as ff:
    bs=ff.read()
import ctypes 
idx=0
target=b''
textidx=0
while idx<len(bs):
    blocklength=ctypes.c_short.from_buffer_copy(bs[idx:idx+2]).value
    #print(hex(blocklength))
    idx+=2
    mid=bs[idx:idx+6]
    #print(bs[idx:idx+6].hex())
    idx+=6
    length=ctypes.c_ushort.from_buffer_copy(bs[idx:idx+2]).value
    #print(hex(length))
    idx+=2
    if length:
        text=bs[idx:idx+length*2]
       # print(1,text.decode('utf-16-le'),1)
        
        idx+=length*2+2
        
        text=lines[textidx*3+1][5:]
        text=list(text)
        for ii in range(len(text)):
            text[ii]=remap_charset2.get(text[ii],text[ii])
        text=''.join(text) 
        blocklength=2+6+2+2+len(text)*2
        target=target+blocklength.to_bytes(2,'little')+mid+len(text).to_bytes(2,'little')+text.encode('utf-16-le')+b'\x00\x00' 
        textidx+=1
    else:
        target=target+blocklength.to_bytes(2,'little')+mid+b'\x00\x00\x00\x00' 
    if textidx==2:
        target=target+bs[idx:]
        break
with open('SCRIPT_FHD/SCRIPT_FHD_transed/_varstr','wb') as ff:
    ff.write(target)
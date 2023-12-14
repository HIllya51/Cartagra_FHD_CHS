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
    
    with open('SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
        lines=ff.read().split('\n')
    with open('SCRIPT_FHD/SCRIPT_FHD/'+f,'rb') as ff:
        cankao=ff.read()
    for _i in range(len(lines)-1):
        i=len(lines)-1-_i
        if i%3!=1:continue
        idx=int(lines[i][:4],16)
        originlength=ctypes.c_ushort.from_buffer_copy(cankao[idx:idx+2]).value
        text=lines[i][5:].replace('＄','\n')
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
            for i in range(len(_1)):
                if _1[i] in mymap:
                    if mymap[_1[i]]==_2[i]:
                        continue
                 
                mymap[_1[i]]=_2[i]
                cnt+=1
                print('{L"'+_1[i].replace('\n','\\n')+'",L"'+_2[i].replace('\n','\\n')+'"},',file=pf)
    with open('SCRIPT_FHD/SCRIPT_FHD_transed/'+f,'wb') as ff:
        ff.write(bytes(cankao))
# with open(r'C:\InnocentGrey\カルタグラ FHD\trans.json','w',encoding='utf8') as ff:
#     ff.write(json.dumps(mymap,ensure_ascii=False,indent=4))

print('};',file=pf)
print(cnt,len(mymap))
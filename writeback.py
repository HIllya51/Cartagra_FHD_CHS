import os ,ctypes,json
mymap={}
with open('font/remap_charset2.txt','r',encoding='utf8') as ff:
    remap_charset2=json.load(ff) 
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
        #print(text)
        length=len(text)  
        # if len(text)>originlength:
        #     print(text)
        
        #
        #print(text)
        text=list(text)
        for ii in range(len(text)):
            text[ii]=remap_charset2.get(text[ii],text[ii])
        text=''.join(text) 
        
        #text=text[:originlength]
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
            _1=lines[i-1][5:].replace('＄','\n').split("$d")
            _2=text.split("$d")
            for i in range(len(_1)):
                mymap[_1[i]]=_2[i]
    with open('SCRIPT_FHD/SCRIPT_FHD_transed/'+f,'wb') as ff:
        ff.write(bytes(cankao))
with open('trans.json','w',encoding='utf8') as ff:
    ff.write(json.dumps(mymap,ensure_ascii=False,indent=4))
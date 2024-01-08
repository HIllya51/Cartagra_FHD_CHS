from ctypes import c_ushort,c_ubyte
import os
num=0 
for f in os.listdir('SCRIPT_FHD'):
    #if f.startswith('00')==False:continue
    #if f.startswith('a')==False:continue
    #if f!='0000-op0_HD':continue
    #if f!='a1-3-1':continue
    #if f!='0206-01-00':continue
    if f.startswith('_') and f!='_varstr':continue
    fw=open('text2/'+f,'w',encoding='utf8')
    with open('SCRIPT_FHD/'+f,'rb') as ff:
        bs=ff.read()
    idx=0
    textnum=0
    while idx<len(bs):
        blocklength=c_ushort.from_buffer_copy(bs[idx:idx+2]).value
        #if blocklength==0:break
       # print(hex(idx),hex(blocklength))
       # print(bs[idx+2:idx+4].hex())
        
        if bs[idx+2]==0x24:
            textoff=10
        elif bs[idx+2]==0x28:
            textoff=14
        elif bs[idx+2]==0x2b:
            textoff=11
        elif bs[idx+2]==0x1d:
            textoff=8
        else: 
            textoff=0
        if textoff:
            textidx=idx+textoff
            textleng=c_ushort.from_buffer_copy(bs[textidx:textidx+2]).value
            
            if textleng and textleng*2<blocklength:
                text=bs[textidx+2:textidx+2+textleng*2].decode('utf-16-le').replace('\n','＄')
                textnum+=1
                #print(textnum,bs[idx+2:idx+4].hex(),hex(textleng),text)
                print('%04x'%textidx+"|"+text,file=fw)
                print('%04x'%textidx+"|"+text,file=fw)
                print('',file=fw)
        idx+=blocklength
        if idx<len(bs):
            if blocklength%2!=0:
                idx+=1
 
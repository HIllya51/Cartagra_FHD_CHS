from ctypes import c_ushort,c_ubyte
import os
num=0
for f in os.listdir('SCRIPT_FHD'):
    #if f.startswith('00')==False:continue
    #if f.startswith('a')==False:continue
    #if f!='0000-op0_HD':continue
    #if f!='0206-01-00':continue
    print(f)
    fw=open('text/'+f,'w',encoding='utf8')
    with open('SCRIPT_FHD/'+f,'rb') as ff:
        bs=ff.read()
    idx=10
    num_=0
    while idx<len(bs):
        try:
            length=c_ushort.from_buffer_copy(bs[idx:idx+2]).value*2
            #print(hex(idx),hex(length))
            if length<=1 or length>300:
                idx+=1
                continue
            
            checkzero= c_ushort.from_buffer_copy(bs[idx+2+length:idx+2+length+2]).value
             
            string=bs[idx+2:idx+2+length]   
            ok=False
            if  bs[idx-8:idx-6]==b'\x61\x6d':#判断
                ok=True
            if bs[idx-10:idx-7]==b'\x00\x2b\x03':
                ok=True
            if bs[idx-9:idx-6]==b'\x00\x24\x03':
                ok=True
            if ok and checkzero==0:#stringidx==0:
                 
                num_+=1
                num+=1
                text=string.decode('utf-16-le')
                text=text.replace('\n','＄')
                print('%04x'%idx+"|"+text,file=fw)
                print('%04x'%idx+"|"+text,file=fw)
                print('',file=fw)
                idx+=(2+length+2)
        except ValueError:
            pass
        idx+=1
    #break 
    print(num_,num)
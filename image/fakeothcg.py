import os
for _dir in ['OTHCG']:
    
    path=rf'C:\InnocentGrey\カルタグラ FHD\files\image\{_dir}.PAK'
    packPAKpath=rf'C:\InnocentGrey\カルタグラ FHD\files\image\{_dir}_NEW'
    packPAKpathdefault=rf'C:\InnocentGrey\カルタグラ FHD\files\image\{_dir}'
    newPAKpath=rf'C:\InnocentGrey\カルタグラ FHD\CHSPAK\{_dir}.PAK'
     

    with open(path,'rb') as ff:
        bs=ff.read() 
    
    from ctypes import c_uint,c_byte 
    count=(c_uint.from_buffer_copy(bs[4:4+4]).value)
    #print(count)
    data_offset =(c_uint.from_buffer_copy(bs[0:0+4]).value)
    #print(data_offset)  
    block_size =(c_uint.from_buffer_copy(bs[0xC:0xC+4]).value) 
    print(block_size)
    first_offset = data_offset // block_size;
    #print(first_offset)
    flags = (c_byte.from_buffer_copy(bs[0x21:0x21+1]).value) 
    #print(flags)
    index_offset = 0x24
    while (index_offset < data_offset):
        if c_uint.from_buffer_copy(bs[index_offset:index_offset+4]).value == first_offset:
            break;
        index_offset += 4;
    #print(index_offset)
    names=[]
    if flags&2!=0:
        names_offset = c_uint.from_buffer_copy(bs[index_offset - 4:index_offset]).value;
        for i in range(count):
            b=bs[names_offset:names_offset+50].split(b'\x00')[0]
            #print(hex(i),hex(names_offset),b.hex())
            names_offset+=len(b)+1 
            names.append(b.decode('utf8')) 
    bslist=list(bs)[:first_offset*block_size]

    for i in range(count):
        Offset=c_uint.from_buffer_copy(bs[index_offset:index_offset+4]).value* block_size;
        Size=c_uint.from_buffer_copy(bs[index_offset+4:index_offset+8]).value
        
        print(i,names[i],hex(Offset),hex(Offset+Size),Offset%block_size, Size%block_size ) 
        #size%4不为0时，填充0
        # with open('unpack/'+names[i],'wb') as ff:
        #     ff.write(bs[Offset:Offset+Size]) 
        fnames=[
            packPAKpath+'/'+names[i],
            packPAKpath+'/'+names[i]+'.cz',
            packPAKpathdefault+'/'+names[i],
            packPAKpathdefault+'/'+names[i]+'.cz'
        ]
        for _fn in fnames:
            if os.path.exists(_fn):
                with open(_fn,'rb') as ff:
                    fbs=ff.read() 
                break
        
        save_size=_size=len(fbs)
        if (_size%block_size)!=0:
            _add=block_size-_size%block_size
            _size+=_add
            fbs+=_add*b'\x00'
        #bs[index_offset+4:index_offset+8]= 
        #print(hex(index_offset))
        for j in range(4):
            bslist[index_offset+4+j]=save_size.to_bytes(4,'little')[j]
    
        for j in range(4):
            bslist[index_offset+0+j]=first_offset.to_bytes(4,'little')[j]
        first_offset+=_size//block_size
        bslist+=list(fbs)
        index_offset+=8  
    
    memnewothcgbs=bytes(bslist) 
with open(r'C:\InnocentGrey\カルタグラ FHD\CHSPAK\OTHCG.DAT','wb') as ff:
    ff.write(memnewothcgbs[:0x3800])  
pf=open('../patch/othcg.cpp','w',encoding='utf-8-sig')
print('''
#include<unordered_map> 
#include<string> 
''',file=pf) 

import os

def getdatas(bs):
    
    from ctypes import c_uint,c_byte 
    count=(c_uint.from_buffer_copy(bs[4:4+4]).value)  
    data_offset =(c_uint.from_buffer_copy(bs[0:0+4]).value) 
    block_size =(c_uint.from_buffer_copy(bs[0xC:0xC+4]).value)  
    first_offset = data_offset // block_size; 
    flags = (c_byte.from_buffer_copy(bs[0x21:0x21+1]).value)  
    index_offset = 0x24
    while (index_offset < data_offset):
        if c_uint.from_buffer_copy(bs[index_offset:index_offset+4]).value == first_offset:
            break;
        index_offset += 4; 
    names=[]
    newcz={}
    newczdata=b''
    if flags&2!=0:
        names_offset = c_uint.from_buffer_copy(bs[index_offset - 4:index_offset]).value;
        for i in range(count):
            b=bs[names_offset:names_offset+50].split(b'\x00')[0]
            names_offset+=len(b)+1 
            #print(hex(i),hex(names_offset),b.hex())
            names.append(b.decode()) 
    bslist=list(bs)
    newOffset=None
    offsets=[]
    offset2size={}
    for i in range(count):
        Offset=c_uint.from_buffer_copy(bs[index_offset:index_offset+4]).value* block_size;
        Size=c_uint.from_buffer_copy(bs[index_offset+4:index_offset+8]).value
        index_offset+=8  
        print(i,names[i],hex(Offset),hex(Size) ) 
        offsets.append(hex(Offset));
        if (Size%block_size)!=0:
            _add=block_size-Size%block_size
            Size+=_add
        offset2size[hex(Offset)]=hex(Size)
        if os.path.exists(r'C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG_NEW\\'+names[i]):
            
            with open(r'C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG_NEW\\'+names[i],'rb') as ff:
                _data=ff.read()
            newcz[hex(Offset)]=[hex(len(newczdata)),hex(len(_data))]
            newczdata+=_data
    return offsets,offset2size,newcz,newczdata
with open(r'C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG.PAK','rb') as ff:
    othcgbs=ff.read()  
oldfileoffset,oldfilesize,_,_=getdatas(othcgbs)        
newfileoffset,newfilesize,newcz,newczdata=getdatas(memnewothcgbs)  
with open(r'C:\InnocentGrey\カルタグラ FHD\CHSPAK\OTHCG.IMG','wb')  as ff:
    ff.write(newczdata)
pakoffsetnew2old={}
for i in range(len(newfileoffset)):
    pakoffsetnew2old[newfileoffset[i]]=oldfileoffset[i]
print('std::unordered_map<int,std::pair<int,int>>newcz={',file=pf)
for k in newcz:
    print('{',k,',{'+newcz[k][0]+','+newcz[k][1]+'} },',file=pf)
print('};',file=pf)

print('std::unordered_map<int,int>pakoffsetnew2old={',file=pf)
for k in pakoffsetnew2old:
    print('{',k,',',pakoffsetnew2old[k],'},',file=pf)
print('};',file=pf)

print('std::unordered_map<int,int>oldfilesize={',file=pf)
for k in oldfilesize:
    print('{',k,',',oldfilesize[k],'},',file=pf)
print('};',file=pf)
print('std::unordered_map<int,int>newfilesize={',file=pf)
for k in newfilesize:
    print('{',k,',',newfilesize[k],'},',file=pf)
print('};',file=pf)
 
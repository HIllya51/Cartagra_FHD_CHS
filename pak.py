#__type=3
for __type in [1,2,3,4]:
    if __type==1:
        path=r'C:\InnocentGrey\カルタグラ FHD\files\SCRIPT.PAK'
        packPAKpath=r'C:\Users\wcy\Documents\GitHub\Cartagra_FHD_CHS\SCRIPT_FHD/SCRIPT_FHD_transed'
        newPAKpath=r'C:\InnocentGrey\カルタグラ FHD\CHSPAK\SCRIPT.PAK'
    elif __type==2:
        path=r'C:\InnocentGrey\カルタグラ FHD\files\FONT.PAK'
        packPAKpath=r'C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW'
        newPAKpath=r'C:\InnocentGrey\カルタグラ FHD\CHSPAK\FONT.PAK'
    elif __type==4:
        path=r'C:\InnocentGrey\カルタグラ FHD\files\FONT_V.PAK'
        packPAKpath=r'C:\InnocentGrey\カルタグラ FHD\files\FONT_V_NEW'
        newPAKpath=r'C:\InnocentGrey\カルタグラ FHD\CHSPAK\FONT_V.PAK'
    elif __type==3:
        path=r'C:\InnocentGrey\カルタグラ FHD\files\SYSFONT.PAK'
        packPAKpath=r'C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW'
        newPAKpath=r'C:\InnocentGrey\カルタグラ FHD\CHSPAK\SYSFONT.PAK'

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
        
        print(i,names[i],hex(Offset),hex(Size),hex(Offset+Size),Offset%block_size, Size%block_size ) 
        #size%4不为0时，填充0
        # with open('unpack/'+names[i],'wb') as ff:
        #     ff.write(bs[Offset:Offset+Size]) 

        with open(packPAKpath+'/'+names[i],'rb') as ff:
            fbs=ff.read()
        
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
    with open(newPAKpath,'wb') as ff:
        ff.write(bytes(bslist))

if 0:#check
    with open(newPAKpath,'rb') as ff:
        bs=ff.read() 
    
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
    print(index_offset)
    names=[]
    if flags&2!=0:
        names_offset = c_uint.from_buffer_copy(bs[index_offset - 4:index_offset]).value;
        for i in range(count):
            b=bs[names_offset:names_offset+50].split(b'\x00')[0]
            names_offset+=len(b)+1 
            #print(hex(i),hex(names_offset),b.hex())
            names.append(b.decode()) 
    bslist=list(bs)
    newOffset=None
    for i in range(count):
        Offset=c_uint.from_buffer_copy(bs[index_offset:index_offset+4]).value* block_size;
        Size=c_uint.from_buffer_copy(bs[index_offset+4:index_offset+8]).value
        index_offset+=8  
        print(i,names[i],hex(Offset),hex(Offset+Size),Offset%block_size, Size%block_size) 
        
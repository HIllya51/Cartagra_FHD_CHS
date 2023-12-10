 
names={}
transmap={}  
everymap={}
transmap1={}   
naketransmap={}
nakeeverymap={}
xxxmap={}
from tqdm import tqdm
import os,re,json,sys,random,requests,urllib,hashlib
half=' …()[]1234567890!@#$%^&*_+-=,./?;:\'"`~qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
QUAN='―「　」〜（）［］１２３４５６７８９０！＠＃＄％＾＆＊＿＋－＝，．／？；：＇＂｀～ｑｗｅｒｔｙｕｉｏｐａｓｄｆｇｈｊｋｌｚｘｃｖｂｎｍＱＷＥＲＴＹＵＩＯＰＡＳＤＦＧＨＪＫＬＺＸＣＶＢＮＭ'
fuhaos=half+QUAN+'。，、；’：“”‘！？【】『』'
naketrans=str.maketrans(fuhaos,len(fuhaos)*'［')
castkata2hira=str.maketrans('ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ','ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ')
class TS( ):  
     
    def translate(self,query):  
         
        appid = '20151211000007653'
        secretKey = 'IFJB6jBORFuMmVGDRude'
        myurl = '/api/trans/vip/translate'

        fromLang = 'jp'
        toLang = 'zh'
        salt = random.randint(32768, 65536)
        q= query
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
        
        res=requests.get('https://api.fanyi.baidu.com'+myurl)
        try:
            _='\n'.join([_['dst'] for _ in res.json()['trans_result']])  
             
            return _
        except:
            raise Exception(res.text)
ts=TS()
import fugashi
tagger = fugashi.Tagger("-Owakati") 
def parse_2(string:str):
    nodes=tagger.parseToNodeList(string)
    _=[]
    for node in nodes:
        if set(node.surface)-set(fuhaos)==set():
            _.append(node.surface)
        else:
            if node.feature.kana:
                _.append(node.feature.kana)
            else:
                _.append(node.surface)
   
    return ''.join(_)
    
def parsetokana(string:str):
    strings=string.split(' ')
    _=[]
    for string in strings:
        _.append(parse_2(string))
    return (' '.join(_)).translate(castkata2hira)
def unspace(text):

    if len(text) and  text[0]=='＄':
        text=text[1:]
    if len(text) and text[-1]=='＄':
        text=text[:-1]
    return text
def naked(text):
    text=text.translate(naketrans).replace('［','')
    return text
def parrubyold(text):
    return re.sub('<(.*?)<(.*?)>','\\1',text)
def parrubynew(text):
    _= re.sub('\\$\\[(.*?)\\$/(.*?)\\$\\]','\\1',text) 
    return _
for f in (os.listdir('script/script_pair')):
    with open('script/script_pair/'+f,'r',encoding='utf8') as ff:
        oldtexts=ff.read().split('\n')
    f=f[:-6]
    everymap[f]={}
    nakeeverymap[f]={}
    lasttrans=lastorigin=None
    for i in (range(len(oldtexts))):
        if i%3==0:
            origin=parrubyold(oldtexts[i])
        if i%3==1:
            trans=oldtexts[i]
            origin=unspace(origin)
            nakeorigin=naked(origin)
            if lastorigin:
                transmap1[naked(lastorigin+origin)]=[lasttrans,trans]
            
            if origin[:2]=='♯【' and origin[-1]=='】':
                origin=origin[2:-1]
                if origin not in names:
                    names[origin]=[]
                names[origin].append(trans[2:-1])
            else:
                lastorigin=origin
                lasttrans=trans
                if origin not in everymap[f]:
                    everymap[f][origin]=[]
                
                everymap[f][origin].append(trans)
                # if len(set(everymap[f][origin]))>1:
                #     print(origin,everymap[f][origin])
                    #经检查，虽然有多种翻译，但其实没必要区分。
                if origin not in transmap:
                    transmap[origin]=[] 
                transmap[origin].append(trans)
                if nakeorigin not in naketransmap:
                    naketransmap[nakeorigin]=[] 
                naketransmap[nakeorigin].append(trans)
                if nakeorigin not in nakeeverymap[f]:
                    nakeeverymap[f][nakeorigin]=[] 
                nakeeverymap[f][nakeorigin].append(trans)

                xxxmap[parsetokana(nakeorigin)]=trans
from collections import Counter
for name in names:
    #print(name,Counter(names[name]),sorted(list(Counter(names[name]).keys()),key=lambda x: -Counter(names[name])[x])[0])
    names[name]=sorted(list(Counter(names[name]).keys()),key=lambda x: -Counter(names[name])[x])[0]
try:
    with open('leven.json','r',encoding='utf8') as ff:
        leven=json.load(ff)
except:
    leven={}
try:
    with open('jifan.json','r',encoding='utf8') as ff:
        jifan=json.load(ff)
except:
    jifan={}
#unknownpf=open('unknown.txt','w',encoding='utf8')
#unknownpfold=open('unknownold.txt','w',encoding='utf8')
 
def trygetfrommap_(text,mpbig,mpsmall, file):
    if file in mpsmall and text in mpsmall[file]:
        return mpsmall[file][text]
    if text in mpbig:
        return mpbig[text]
    if text in leven:
        return leven[text]
    text=parsetokana(text) 
    #print(text,file=unknownpf)
    if text in leven:
        return leven[text]
    return xxxmap.get(text,None)
# with open('xxxmap.json','w',encoding='utf8') as ff:
#     print(xxxmap,file=ff)
# with open('naketransmap.json','w',encoding='utf8') as ff:
#     print(naketransmap,file=ff)
# with open('nakeeverymap.json','w',encoding='utf8') as ff:
#     print(nakeeverymap,file=ff)
def trygetfrommap(text,file):
    trans=trygetfrommap_(text,transmap,everymap,file)
    if type(trans)==list:
        trans=trans[0]
    if trans:
        return trans
    else:
        text=naked(text)
        trans= trygetfrommap_(text,naketransmap,nakeeverymap,file)
        if type(trans)==list:
            trans=trans[0]
        if trans:
            return trans
        else: 
            lian= transmap1.get(text,None)
            if lian:
                #print(lian)
                if lian[0][-1]=='」':lian[0]=lian[0][:-1]
                if lian[1][0]=='「':lian[1]=lian[1][1:]
                return lian[0]+'。'+lian[1]
            else:
                return None
unknown=[]
unknownf=[]
unknownxx=[]
def addspace(origin,trans):
    if len(origin) and origin[0]=='＄' and trans[0]!='＄':
        trans='＄'+trans
    if len(origin) and origin[-1]=='＄' and trans[-1]!='＄':
        trans=trans+'＄'
    return trans
for f in tqdm(os.listdir('SCRIPT_FHD/text')):
    global isnew
    with open('SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
        newtexts=ff.read().split('\n') 
    #if f!='0206-03-00':continue
    #print(everymap[f])
    print(f)
    if f+'.s.txt' in os.listdir('./script/script_pair'):
        isnew=False
    else:
        isnew=True
    for i in (range(len(newtexts)-1)):
        if i%3!=0:continue 
        #print(newtexts[i])
        text=newtexts[i][5:] 
        idxhex=newtexts[i][:5]
        text=parrubynew(text)
        if text[0]=='@':
            _idx=text.find('@',1)
            namepredix=text[1:_idx]
            if namepredix not in names:
                names[namepredix]=namepredix
            namepredix='@'+names[namepredix]+'@'
            text=text[_idx+1:]
        else:
            namepredix=''
        origintext=text
        text=unspace(text)
        trans=trygetfrommap(text,f) 
        if trans:
            newtexts[i+1]=idxhex+namepredix+addspace(origintext, trans)
            #print(newtexts[i+1])
        else: 
            #newtexts[i+1]=idxhex+namepredix+'UNKNOWN'
            #print(f,text)
            _text=text.split('$d')
            _ts=[]
            #print(_text)
            for __t in _text:
                if __t=='':
                    _ts.append('')
                    continue
                if __t not in jifan:
                    trans=ts.translate(__t)
                    jifan[__t]=trans
                    with open('jifan.json','w',encoding='utf8') as ff:
                        ff.write(json.dumps(jifan,ensure_ascii=False,indent=4))
                else:
                    trans=jifan[__t]
                _ts.append(trans)
            trans='$d'.join(_ts)
            #newtexts[i+1]=idxhex+namepredix+'JF:'+addspace(origintext, trans)
            
            unknown.append(text)
            unknownf.append(f)
            #print(f,text,file=unknownpf)
            # if isnew ==False:
                
            #     print(f,text,file=unknownpfold)
            #print(newtexts[i])
        #print((newtexts[i+1])) 
    with open('SCRIPT_FHD/text/'+f,'w',encoding='utf8') as ff:
        ff.write('\n'.join(newtexts))
print(len(set(unknown))) 
from collections import Counter
#print(Counter(unknownf))
sys.exit(0)
import Levenshtein

for origin in tqdm(unknown):
    use=None
    mdis=999
    origin=naked(origin)
    for key in naketransmap:
        dis= Levenshtein.distance(origin,key)
        if dis<len(origin)//5 and dis<mdis:
            print(origin,key)
            use=key
            mdis=dis
    if use:
        leven[origin]=naketransmap[use]
        with open('leven.json','w',encoding='utf8')as ff:
            ff.write(json.dumps(leven,ensure_ascii=False))
        continue
    origin=parsetokana(origin) 
    for key in xxxmap:
        dis= Levenshtein.distance(origin,key)
        if dis<len(origin)//5 and dis<mdis:
            print(origin,key)
            use=key
            mdis=dis
    if use:
        leven[origin]=xxxmap[use]
        with open('leven.json','w',encoding='utf8')as ff:
            ff.write(json.dumps(leven,ensure_ascii=False))
        continue
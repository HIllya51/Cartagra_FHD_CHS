import quopri ,os
maps={}
for f in os.listdir(r'..\SCRIPT_FHD\text'):
    #if f!='0206-05-03':continue
    #if f!='0000-op0_HD':continue
    #print(f)
     
    with open(r'..\SCRIPT_FHD\text/'+f,'r',encoding='utf8') as ff:
        lines=ff.read().split('\n')
    for i in range(len(lines)):
        if i%3==1:
            ori=lines[i-1][5:]
            ts=lines[i][5:]
            if '$d' in ori:
                #print(ori)
                oris=ori.split('$d')
                tss=ts.split('$d')
                for j in range(len(oris)):
                    maps[oris[j].replace('…','').replace('、','').replace('─','―').replace('？','')]=tss[j]
#print(maps)
maps.update({
    '答えれない':maps.get('答えられない')
})

maps.update({
    '誠也の部屋【カルタグラ 〜ツキ狂イノ病〜 ＜REBIRTH FHD SIZE EDITION＞ 攻略】 ':'恋狱～月狂病～ ＜REBIRTH FHD SIZE EDITION＞ 攻略',
    'カルタグラ 〜ツキ狂イノ病〜 ＜REBIRTH FHD SIZE EDITION＞★':'恋狱～月狂病～ ＜REBIRTH FHD SIZE EDITION＞★',
    '最終更新日':'最后更新日期',
    'ディスクレス':'无盘运行',
    'セーブ可能数':'可存档数量',
    '修正パッチ':'修正补丁',
    'メーカーリンク':'发行商',
    '可':'支持',
    '無':'无',
    'フルコンプセーブ':'全CG存档下载',
    '│パッケージ版はDL版コード付き。':'│包装版附带DL版激活码。',
    'とりあえず完了。再検証済み。セーブ番号の整理をしたので途中まで攻略を使っていた人は注意。':'已重新验证。由于整理了存档编号，所以攻略到一半的人请注意顺序。',
    '「カルタグラ 〜ツキ狂イノ病〜」のフルHDリメイク作品です。':'此攻略为《恋狱月狂病》FHD（全高清重制版）攻略。',
    '''
              和み匣の「サクラメント 〜月ノ視ル夢〜」シナリオ等が統合されていて各所で新規の追加シナリオやENDがあります。''':'此版整合了和之匣中的由良后日谈等剧情，并且也有其他新增的剧情和结局。',
    'の選択肢はCG差分の回収の為に見ておくこと。回想シーンでも一応回収できるかと。':'中的选项是为了收集CG差分（大部分为H），在回想scene中应该也能收集。',
    '''
              ☆の選択肢はEND11を見た後に出現する追加選択肢なので出現しない場合は無視してください。''':'☆的选项是在END11（即和菜END1）之后出现的附加选项，没有出现可暂时忽略。',
    '''
              ★の選択肢はFHD版で追加された選択肢です。結構あります。''':'★的选项是在FHD中新增的选项。数量相当多。',
    'ルート分岐条件の大元は旧カルタグラから殆ど変わっていませんが':'攻略路线和分支与旧版《恋狱月狂病》相比基本上没有变化。',
    '''
              一部のシナリオが★の追加選択肢で必須の選択をしていないと発生しないようになっています。(凛、冬史、和菜、由良)''':'但是如果没有选择★新增的攻略角色必须项，会无法进入部分角色线。（凛、冬史、和菜、由良）',
    '''
              追加ルートにも入るには★の追加選択肢で必須の選択肢を選んでいる必要があるみたいです。''':'进入附加路线似乎也需要选择★新增的必选项。',
    'END番号はエンディングリストの順番で記載しています。':'结局END的编号是按照EXTRA中结局列表的顺序记录。',
    '途中まで攻略を使っていた人はEND12以降(和菜シナリオ)に入るためには':'使用本攻略打到一半的玩家，如果要进END12（和菜剧情），',
    '''
              序盤の選択肢から影響があるので最初からやり直すこと。''':'因为早期选项也会影响后续剧情，所以需要重新开始。',
    'マウスジェスチャー機能をONにするとフリック操作で既読ジャンプが使えるのでチャート5以降は活用するといいかと。':'开启鼠标手势功能后，可以使用轻扫操作进行已读跳转，从列表5开始使用可节约观看重复剧情的时间。',
    '一部のキャラが同じ世界観の「殻ノ少女シリーズ」に継続出演してます。':'本作部分角色在同一世界观的《壳之少女》中也有继续登场。',
    '''
              シリーズを続けてプレイする場合は最低でもEND15までクリアしておくこと。''':'所以如果计划从这部开始攻略IG系列游戏，至少要阅读完END15（TRUE END真结局）剧情。',
    '「和み匣」収録の凛のシナリオが収録されてないのでキャラが気に入った人は「':'《和之匣》中凛的部分剧情在本作中没有收录，如果你喜欢这个角色，推荐购买「',
    '」を買っておくといいかも':'」多作捆绑包。',
    '和菜必須':'和菜必选',
    '\u3000※冬史必須':'\u3000※冬史必选',
    '(外に出す)':'(外射)',
    '冬史出現':'冬史出现',
    'シスターBAD+1':'修女BE +1',
    'シスターBAD+3でルート分岐':'修女BE +3会达成分支路线',
    'END1【聖奴隷】':'END1【圣奴隶】',
    'H発生':'H事件',
    'END4【凛の幸せ】凛END':'END4【凛的幸福】凛END',
    'タコ焼き+1':'章鱼烧+1',
    '七七+2でルート分岐':'七七+2会达成分支路线',
    '双子+2でルート分岐':'双子+2会达成分支路线',
    'END5【襲撃者】(小雪＆芹)':'END5【袭击者】(小雪＆芹)',
    'Hシーン回収後終了':'回收Hscene后结束',
    '(凛の顔にかける)':'(射在凛的脸上)',
    '凛Hシーン差分回収後終了':'回收凛的差分Hscene后结束',
    '初音+1でルート分岐':'初音+1会达成分支路线',
    'END6【初音の幸せ】初音END':'END6【初音的幸福】初音END',
    '差分Hシーン回収後終了':'回收差分Hscene后结束',
    '楼子+1でルート分岐':'楼子+1会达成分支路线',
    'タコ焼き＋2の時のみCG回収＆選択肢':'仅限章鱼烧+2时可以回收此CG和选择项',
    'END7【無力】':'END7【无力】',
    'END8【楼子の幸せ】楼子END':'END8【楼子的幸福】楼子END',
    'タコ焼き＋2の時のみCG回収':'仅限章鱼烧+2时回收此CG',
    'END9【暗闇の光】(楼子回収)':'END9【暗处的光】(楼子线回收)',
    'END10【冬史の愛】冬史END':'END10【冬史的爱】冬史END',
    'END11【エピローグ】和菜END1':'END11【epilogue】和菜END1',
    '雨雀差分Hシーン回収後終了':'回收雨雀的差分Hscene后结束',
    '楼子差分Hシーン回収後終了':'回收楼子的差分Hscene后结束',
    '冬史差分Hシーン回収後終了':'回收冬史的差分Hscene后结束',
    'END11後に':'END11完成后',
    '由良分岐必須':'由良分支必选',
    'END12【グランドエピローグ】':'END12【grand epilogue】',
    '以下継続':'从以下继续',
    '●サクラメント：雪椿シナリオ':'●Sacrament：雪椿线',
    'END13【惨劇】':'END13【惨剧】',
    'END14【旅立ち】':'END14【远行】',
    'END15【トゥルーエンド】和菜END2':'END15【TRUE END】和菜END2',
    '''
              ●サクラメント：白詰草シナリオ''':'Sacrament：白诘草线',
    'END17【海の影】由良BAD':'END17【海之影】由良BE',
    'END16【逃避行】':'END16【私奔】',
    'END18【海の光】由良END':'END18【海之光】由良END',
    'から':'开始'
})
for i in range(50):
    maps['セーブ%02d'%i]='save%02d'%i
for i in range(10):
    maps['チャート%d'%i]='列表%d'%i
with open('誠也の部屋【カルタグラ ～ツキ狂イノ病～ ＜REBIRTH FHD SIZE EDITION＞ 攻略】.mhtml','r',encoding='utf8') as ff:
    texts=ff.read()
texts1=texts
sig='>'
idx=0 
savepos=[]



_bf='<table'.join(texts.split('<table')[:3])
_af='<table'.join(texts.split('<table')[3:]) 
_af='</table>'.join(_af.split('</table>')[1:])
texts=_bf+_af
 
_bf='<tr>'.join(texts.split('<tr>')[:16])
_af='<tr>'.join(texts.split('<tr>')[16:]) 
_af='</tr>'.join(_af.split('</tr>')[1:])
texts=_bf+_af

_bf='<tr>'.join(texts.split('<tr>')[:20])
_af='<tr>'.join(texts.split('<tr>')[20:]) 
_af='</tr>'.join(_af.split('</tr>')[1:])
texts=_bf+_af

for i in range(4):
        
    _bf='<a'.join(texts.split('<a')[:4])
    _af='<a'.join(texts.split('<a')[4:]) 
    _af='</a>'.join(_af.split('</a>')[1:])
    texts=_bf+_af
while 1:
    idx=texts.find(sig, idx+1)
    if idx==-1:break
    idx+=len(sig)
    end=texts.find('<',idx)
    
    #print(text)
    # text=text.replace('★','')
    if len(texts[idx:end].strip()) and '=' in texts[idx:end] :
        if '/' in texts[idx:end]:continue
        
        text=(quopri.decodestring(texts[idx:end].encode('utf-8')).decode('EUC-JP'))
       # print(text) 
         
        if text==texts[idx:end]:continue
        savepos.append((idx,(end)))
for pos in reversed(savepos):
    #print(texts[pos[0]:pos[1]])
    text=quopri.decodestring(texts[pos[0]:pos[1]].encode('utf-8')).decode('EUC-JP')
    if len(text)==0:continue
    #print(text)

    if text[0] in '★☆※◆':
        star=text[0]
        text=text[1:]
    else:star='' 
    for sp in '　│':
        textss=text.split(sp)
        text=textss[0]
        text1=maps.get(text,None)
        if text1 is None :
            text1=maps.get(text.replace('…','').replace('、','').replace('─','―').replace('？',''),None)

        if text1 is None:
            #print(text,list(text))
            text1=text 
        
        textss[0]=text1
        text=sp.join(textss)
    text=star+text
    text=quopri.encodestring(text.encode('utf8',errors='ignore')).decode('utf-8')
    texts=texts[:pos[0]]+text+texts[pos[1]:]
texts=texts.replace('EUC-JP','utf8').replace('euc-jp','utf8')


texts=texts.replace('\n              =EF=BC=8F =EF=BC=8F','')
with open('攻略.mhtml','w',encoding='utf8') as ff:
    ff.write(texts)

 
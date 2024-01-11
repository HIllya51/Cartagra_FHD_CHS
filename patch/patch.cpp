#include <Windows.h>
#include<vector>
#include<string>
#include<fstream> 
#include<unordered_map>
#include<Shlwapi.h>
#include<regex>
#include"lib/minhook/include/MinHook.h"
#include<filesystem>
#include<thread>
#include"lib/Detours-4.0.1/include/detours.h"
#include"lyric/lyric.h"
extern std::unordered_map<std::wstring,std::wstring>trans;
extern std::vector<std::pair<int,const char*>>uitexts;
extern std::unordered_map<int,std::pair<int,int>>newcz;
extern std::unordered_map<int,int>pakoffsetnew2old;
extern std::unordered_map<int,int>oldfilesize;
extern std::unordered_map<int,int>newfilesize;
std::string newczhead;
std::string newcz_data;
bool once=true;
HWND g_hwnd;
HLRC g_lrc=0;
HLRC g_lrc_movie_1=0;
HLRC g_lrc_movie_2=0;
void createmovielrc(){
    auto t = std::thread([] {
        g_lrc_movie_1 = CreateLyric(3);
        g_lrc_movie_2 = CreateLyric(4);
        SetWindowLong(getlyrichwnd(g_lrc_movie_1),GWL_EXSTYLE, GetWindowLong(getlyrichwnd(g_lrc_movie_1),GWL_EXSTYLE) | WS_EX_TRANSPARENT);
        SetLyricParent(g_lrc_movie_1, g_hwnd);
        SetWindowLong(getlyrichwnd(g_lrc_movie_2),GWL_EXSTYLE, GetWindowLong(getlyrichwnd(g_lrc_movie_2),GWL_EXSTYLE) | WS_EX_TRANSPARENT);
        SetLyricParent(g_lrc_movie_2, g_hwnd);
        
        MSG msg;
        while (GetMessage(&msg, nullptr, 0, 0))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        });

    t.detach();
}

auto CreateWindowExW_s=CreateWindowExW;
HWND CreateWindowExWh(
    _In_ DWORD dwExStyle,
    _In_opt_ LPCWSTR lpClassName,
    _In_opt_ LPCWSTR lpWindowName,
    _In_ DWORD dwStyle,
    _In_ int X,
    _In_ int Y,
    _In_ int nWidth,
    _In_ int nHeight,
    _In_opt_ HWND hWndParent,
    _In_opt_ HMENU hMenu,
    _In_opt_ HINSTANCE hInstance,
    _In_opt_ LPVOID lpParam){
        if(once){
            once=false;
            g_hwnd=CreateWindowExW_s(dwExStyle,lpClassName,lpWindowName,dwStyle,X,Y,nWidth,nHeight,hWndParent,hMenu,hInstance,lpParam);
            SetWindowTextW(g_hwnd,L"恋狱～月狂病～《REBIRTH FHD SIZE EDITION》");
            createmovielrc();
            return g_hwnd;
        }
        else{
            return CreateWindowExW_s(dwExStyle,lpClassName,lpWindowName,dwStyle,X,Y,nWidth,nHeight,hWndParent,hMenu,hInstance,lpParam);
        }
       
    }
__declspec(dllexport) void dumy() {}
bool endWith(const std::wstring& s,const std::wstring& s2) {
    if ((s.size() > s2.size()) && (s.substr(s.size() - s2.size(), s2.size()) == s2)) {
        return true;
    }
    return false;
} 
bool pendWith(const std::wstring& s,const std::wstring& s2) {
    if ((s.size() > s2.size()) && (s.substr(s.size() - s2.size(), s2.size()) == s2)) {
        if(s[s.size()-s2.size()-1]==L'\\'||s[s.size()-s2.size()-1]==L'/')
            return true;
        else
            return false;

    }
    return false;
} 
void AppendLog(const std::wstring& logFilePath, const std::string& logMessage) {
    std::ofstream logFile(logFilePath, std::ios::app);
    if (logFile.is_open()) {
        logFile << logMessage << std::endl;
        logFile.close(); 
    } else { 
    }
}

std::wstring StringToWideString(const std::string& text, UINT encoding)
    {
        std::vector<wchar_t> buffer(text.size() + 1);
        int length = MultiByteToWideChar(encoding, 0, text.c_str(), text.size() + 1, buffer.data(), buffer.size());
        return std::wstring(buffer.data(), length - 1);
      
    }

    std::string WideStringToString(const std::wstring& text, UINT encoding=CP_UTF8)
    {
        std::vector<char> buffer((text.size() + 1) * 4);
        WideCharToMultiByte(encoding, 0, text.c_str(), -1, buffer.data(), buffer.size(), nullptr, nullptr);
        return buffer.data();
    }
    std::vector<std::wstring> strSplit(const std::wstring& s, const std::wstring  delim)
{
    std::wstring item;
    std::vector<std::wstring> tokens;

    // Copy the input string so that we can modify it
    std::wstring str = s;

    size_t pos = 0;
    while ((pos = str.find(delim)) != std::wstring::npos) {
        item = str.substr(0, pos);
        tokens.push_back(item);
        str.erase(0, pos + delim.length());
    }
    tokens.push_back(str);

    return tokens;
}
bool all_ascii(const wchar_t *s, int maxsize )
{
  if (s)
    for (int i = 0; i < maxsize && *s; i++, s++)
      if (*s > 127) // unsigned char
        return false;
  return true;
} 
auto CreateFile_save = CreateFileW;
HANDLE  WINAPI   CreateFileWh(
        __in     LPCWSTR lpFileName,
        __in     DWORD dwDesiredAccess,
        __in     DWORD dwShareMode,
        __in_opt LPSECURITY_ATTRIBUTES lpSecurityAttributes,
        __in     DWORD dwCreationDisposition,
        __in     DWORD dwFlagsAndAttributes,
        __in_opt HANDLE hTemplateFile
    ) {  
        wchar_t current[MAX_PATH*2]={0};
        GetCurrentDirectoryW(MAX_PATH,current);
        auto redirects={
            //L"OTHCG.PAK",
            //L"PARAM.PAK",
            L"PARTS.PAK",L"SYSCG.PAK",
            L"FONT.PAK",L"FONT_V.PAK",L"SYSFONT.PAK",L"SCRIPT.PAK" 
        }; 
        for(auto _:redirects){
            if(pendWith(lpFileName,_)){
                wcscat(current,L"\\CHSPAK\\");
                wcscat(current,_);
                 
                lpFileName=current; 
                break;
            }
        }   
        return CreateFile_save(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
    }

typedef __int64 (__fastcall *sub_1401012C0_t)(__int64 a1, __int64 a2, int a3);
auto sub_1401012C0_s=(sub_1401012C0_t)(0x1012C0+(uint64_t)GetModuleHandle(0));
__int64 __fastcall sub_1401012C0(__int64 a1, __int64 a2, int a3){
    // if(((LPCWSTR)a2)[0]==L'@')
    //     MessageBoxW(0,(LPCWSTR)a2,L"",0);
    if(all_ascii((LPCWSTR)a2,wcslen((LPCWSTR)a2)))
        return sub_1401012C0_s(a1,a2,a3);
    std::wstring _=std::wstring((LPCWSTR)a2);
     
    for(auto spliter:{L"$d",L"$n"}){
        auto sps=strSplit(_,spliter);
        for(auto &s:sps){
            
            if(trans.find(s)!=trans.end()){
                s=trans[s];
            }
            else{
                auto _s=std::regex_replace(s, std::wregex(L"@【(.+?)】@"), L"@$1@");
                
                if(trans.find(_s)!=trans.end()){
                    s=trans[_s];
                } 
            }
        }
        std::wstring __;
        for(int i=0;i<sps.size();i++){
            if(i)
                __+=spliter;
            __+=sps[i];
        } 
        _=__;
    }
    return sub_1401012C0_s(a1,(__int64)_.c_str(),a3);
} 
std::wstring currentplayingmovie;
bool started=false;
auto addr_movie_stop=0x263232+(uint64_t)GetModuleHandle(0);
void hidehide(HLRC lrc){
    SetLyricTextW(lrc,L""); 
    LyricUpdate(lrc,0);
    LyricHide(lrc);
}
void notifymovie_stop(){
    //MessageBoxW(0,currentplayingmovie.c_str(),L"stop",0);
    started=false; 
    hidehide(g_lrc_movie_1);
    hidehide(g_lrc_movie_2);
} 
std::vector<char> readfile(const wchar_t* fname) {
    FILE* f;
    _wfopen_s(&f, fname, L"rb");
    if (f == 0)return {};
    fseek(f, 0, SEEK_END);
    auto len = ftell(f);
    fseek(f, 0, SEEK_SET);
    auto buff = std::vector<char>(len);
    fread(buff.data(), 1, len, f);
    fclose(f);
    return buff;
} 
void slowshowhidelyric(HLRC lrc,const wchar_t* text,float duration){
   
        int msd=duration*1000.0;
        auto start=GetTickCount64();
        LyricShow(lrc);
        SetLyricTextW(lrc,text);  
        bool alpha255=false;
        while(started){
            auto current=GetTickCount64()-start;
            if(current<=512){
                LyricUpdate(lrc,current/2);
                
            }
            else if(msd-current<=512){
                LyricUpdate(lrc,(msd-current)/2);
            }
            else if(alpha255==false){
                alpha255=true;
                LyricUpdate(lrc,255);
            }
            else if(current>msd)break;
            Sleep(8);
        } 
        hidehide(lrc);
     
}
struct _struct{
        float t1,t2;
        std::wstring s;
};
ULONGLONG timems;
void showlrc(std::vector<_struct>& data,HLRC lrc){
    std::thread([data,lrc](){
        auto iter=data.begin();
        while (started && iter<data.end())
        {
            auto runedtime=GetTickCount64()-timems;
            auto runeds=runedtime/1000.0;
            if(runeds>= iter->t1 && runeds<=iter->t2){ 
                auto duration= iter->t2- runeds ;
                // char xx[1000];
                // sprintf(xx,"%I64d %f %f",runedtime,runeds,iter->t2);
                // AppendLog(LR"(C:\InnocentGrey\カルタグラ FHD\1.txt)",xx);
                slowshowhidelyric(lrc,(iter->s).c_str(),duration); 
                iter++;
            }
            Sleep(100);
        }
        
    }).detach();
}
void startshowlrc(){
    timems=GetTickCount64();
    started=true; 
    
    auto fn=L".\\CHSPAK\\LRC\\"+currentplayingmovie+L".txt";
    if(std::filesystem::exists(fn)==false)return; 
     
    
    std::vector<_struct>data1,data2;
    auto fdata=readfile(fn.c_str());
    fdata.push_back(0);
    for(auto && line:strSplit(StringToWideString(fdata.data(),65001),L"\n")){
         
        auto && ss=strSplit(line,L"|");
        if(ss.size()!=2)break;
        float t1,t2;wchar_t s1[1000];
        if(swscanf(ss[0].c_str(),L"[%f-%f]%s",&t1,&t2,s1)!=3)break;
        auto s11=wcschr(ss[0].c_str(),L']')+1;
        data1.push_back({t1,t2,s11});
        data2.push_back({t1,t2,ss[1]});
    }
    RECT rect;
    GetClientRect(g_hwnd,&rect);
    float scale=rect.bottom/1080.0; 
    
    SetLyricPosition(g_lrc_movie_1,-50.0*scale, rect.bottom-150.0*scale, rect.right,100.0*scale);

    SetLyricFontW(g_lrc_movie_1, L"宋体", 40.0*scale);
    SetLyricColorStyle(g_lrc_movie_1, 4);
       
    SetLyricPosition(g_lrc_movie_2,50.0*scale, 0.0*scale, rect.right,100.0*scale);

    SetLyricFontW(g_lrc_movie_2, L"Yu Mincho", 40.0*scale);
    SetLyricColorStyle(g_lrc_movie_2, 4);
    
    showlrc(data1,g_lrc_movie_1);
    showlrc(data2,g_lrc_movie_2);
    
}
bool hookaddress(uintptr_t address,uintptr_t newfunction){
    BYTE common_hook[] = {
		0x9c, // push rflags
		0x50, // push rax
		0x53, // push rbx
		0x51, // push rcx
		0x52, // push rdx
		0x54, // push rsp
		0x55, // push rbp
		0x56, // push rsi
		0x57, // push rdi
		0x41, 0x50, // push r8
		0x41, 0x51, // push r9
		0x41, 0x52, // push r10
		0x41, 0x53, // push r11
		0x41, 0x54, // push r12
		0x41, 0x55, // push r13
		0x41, 0x56, // push r14
		0x41, 0x57, // push r15
		// https://docs.microsoft.com/en-us/cpp/build/x64-calling-convention
		// https://stackoverflow.com/questions/43358429/save-value-of-xmm-registers
		0x48, 0x83, 0xec, 0x20, // sub rsp,0x20
		0xf3, 0x0f, 0x7f, 0x24, 0x24, // movdqu [rsp],xmm4
		0xf3, 0x0f, 0x7f, 0x6c, 0x24, 0x10, // movdqu [rsp+0x10],xmm5
		0x48, 0x8d, 0x94, 0x24, 0xa8, 0x00, 0x00, 0x00, // lea rdx,[rsp+0xa8] 
		0x48, 0xb8, 0,0,0,0,0,0,0,0, // mov rax,@TextHook::Send
		0x48, 0x89, 0xe3, // mov rbx,rsp
		0x48, 0x83, 0xe4, 0xf0, // and rsp,0xfffffffffffffff0 ; align stack
		0xff, 0xd0, // call rax
		0x48, 0x89, 0xdc, // mov rsp,rbx
		0xf3, 0x0f, 0x6f, 0x6c, 0x24, 0x10, // movdqu xmm5,XMMWORD PTR[rsp + 0x10]
		0xf3, 0x0f, 0x6f, 0x24, 0x24, // movdqu xmm4,XMMWORD PTR[rsp]
		0x48, 0x83, 0xc4, 0x20, // add rsp,0x20
		0x41, 0x5f, // pop r15
		0x41, 0x5e, // pop r14
		0x41, 0x5d, // pop r13
		0x41, 0x5c, // pop r12
		0x41, 0x5b, // pop r11
		0x41, 0x5a, // pop r10
		0x41, 0x59, // pop r9
		0x41, 0x58, // pop r8
		0x5f, // pop rdi
		0x5e, // pop rsi
		0x5d, // pop rbp
		0x5c, // pop rsp
		0x5a, // pop rdx
		0x59, // pop rcx
		0x5b, // pop rbx
		0x58, // pop rax
		0x9d, // pop rflags
		0xff, 0x25, 0x00, 0x00, 0x00, 0x00, // jmp qword ptr [rip]
		0,0,0,0,0,0,0,0 // @original
	};
	int send_offset = 50, original_offset = 116;

    auto trampoline=new char[sizeof(common_hook)];
    DWORD DUMMY;
    //VirtualProtect((LPVOID)address, 10, PAGE_EXECUTE_READWRITE, &DUMMY);
    VirtualProtect((LPVOID)trampoline, sizeof(common_hook), PAGE_EXECUTE_READWRITE, &DUMMY);
	void* original;
	MH_STATUS error;
    if((error = MH_CreateHook((LPVOID)address, trampoline, &original)) != MH_OK) { 
        //MessageBoxW(0,StringToWideString(MH_StatusToString(error),65001).c_str(),L"1",0);
		 return false;
    }
	*(uintptr_t*)(common_hook + send_offset) =newfunction;
	*(void**)(common_hook + original_offset) = original;
	memcpy(trampoline, common_hook, sizeof(common_hook));
	if((error=MH_EnableHook((LPVOID)address)) != MH_OK){
        //MessageBoxW(0,StringToWideString(MH_StatusToString(error),65001).c_str(),L"2",0);
        return false;
    }
    
    return true;
}
auto modulebase=(uint64_t)GetModuleHandle(0); 
void patchstring(){
    
    // auto addr=0x3FCE28+modulebase;
    // strcpy((char*)addr, "SYSFONT_CHS.PAK");
    // addr=0x3F2288+modulebase;
    // strcpy((char*)addr, "FONT_CHS.PAK");
    // addr=0x3F2298+modulebase;
    // strcpy((char*)addr, "FONT_V_CHS.PAK");
    // addr=0x3D4408+modulebase; 
    // strcpy((char*)addr, "SCRIPT_CHS.PAK");  
    // addr=0x3FD830+modulebase;
    // strcpy((char*)addr,  u8"恋狱～月狂病～《REBIRTH FHD SIZE EDITION》");

    for(auto _pair:uitexts){
        auto addr=_pair.first+modulebase; 
            strcpy((char*)addr, _pair.second);
        
    }
 
    auto addr=0x1AB66+modulebase;  //なし
    DWORD old,_;
    VirtualProtect( (LPVOID) addr, 7, PAGE_EXECUTE_READWRITE, &old);
    *(int*)(addr+3)=*(int*)(addr+3)+4;
    addr=0x2A2770+modulebase;
    VirtualProtect( (LPVOID) addr, 7, PAGE_EXECUTE_READWRITE, &old);
    *(int*)(addr+3)=*(int*)(addr+3)+4;

    
    addr=0x29EA13+modulebase;   //下部
    VirtualProtect( (LPVOID) addr, 7, PAGE_EXECUTE_READWRITE, &old);
    *(int*)(addr+3)=*(int*)(addr+3)+0x3FF4D4-0x3FF4C8;

    addr=0x2A0B92+modulebase;   //既読の色表示
    VirtualProtect( (LPVOID) addr, 7, PAGE_EXECUTE_READWRITE, &old);
    *(int*)(addr+3)=*(int*)(addr+3)+0x3FFEC8-0x3FFEB0;

    addr=0x29E82F+modulebase;   //既読のみ
    VirtualProtect( (LPVOID) addr, 7, PAGE_EXECUTE_READWRITE, &old);
    *(int*)(addr+3)=*(int*)(addr+3)+0x3FF490-0x3FF470;
    
    addr=0x2A1261+modulebase;   //既読色
    VirtualProtect( (LPVOID) addr, 7, PAGE_EXECUTE_READWRITE, &old);
    *(int*)(addr+3)=*(int*)(addr+3)+0x400030-0x3FFF20;

    addr=0x3370A+modulebase;   //最新へ
    VirtualProtect( (LPVOID) addr, 7, PAGE_EXECUTE_READWRITE, &old);
    *(int*)(addr+3)=*(int*)(addr+3)+0x3D5C90-0x3D5C78;
}


bool SetFilePointerToPosition(HANDLE hFile, int64_t offset, DWORD moveMethod) {
    LARGE_INTEGER liOffset;
    liOffset.QuadPart = offset;
    return SetFilePointerEx(hFile, liOffset, NULL, moveMethod);
}
int64_t GetFilePointer(HANDLE hFile) {
    LARGE_INTEGER position;
    if (SetFilePointerEx(hFile, {0}, &position, FILE_CURRENT)) {
        return position.QuadPart;
    }
    return -1;
}
HMODULE g_hm;
std::string LoadResImage(LPCWSTR pszResID) 
{ 
	HMODULE hModule=g_hm;
	HRSRC hRsrc = ::FindResource (hModule, pszResID,L"DATA"); // type   
	if (!hRsrc)  
		return 0;  
	// load resource into memory   
	DWORD len = SizeofResource(hModule, hRsrc);  
	BYTE* lpRsrc = (BYTE*)LoadResource(hModule, hRsrc);  
	if (!lpRsrc)  
		return 0;  
	// Allocate global memory on which to create stream   
	HGLOBAL m_hMem = GlobalAlloc(GMEM_FIXED, len);  
	BYTE* pmem = (BYTE*)GlobalLock(m_hMem);  
	memcpy(pmem,lpRsrc,len);  
	 
	GlobalUnlock(m_hMem);  
	 
	FreeResource(lpRsrc); 
	return std::string((char*)pmem,len);
} 
void preloadnewcz(){ 
    
    newczhead=std::move(LoadResImage(L"OTHCGDAT"));
    newcz_data=std::move(LoadResImage(L"OTHCGIMG"));
     
}
 
auto ReadFiles=ReadFile;
BOOL ReadFileH(
    _In_ HANDLE hFile,
    LPVOID lpBuffer,
    _In_ DWORD nNumberOfBytesToRead,
    _Out_opt_ LPDWORD lpNumberOfBytesRead,
    _Inout_opt_ LPOVERLAPPED lpOverlapped
    ){
        wchar_t output[10000];
        wchar_t filepath[MAX_PATH];
        GetFinalPathNameByHandleW(hFile,filepath,MAX_PATH,0);
        auto cur=GetFilePointer(hFile);

        if(endWith(filepath,L".webm")&&cur==0&&nNumberOfBytesToRead==2048){
            currentplayingmovie=std::wstring(filepath);
            currentplayingmovie=currentplayingmovie.substr(currentplayingmovie.size()+1-sizeof("cartagra_movie_06.webm"));
            startshowlrc();
        }

        if(pendWith(filepath,L"OTHCG.PAK")){ 
            //wsprintf(output,L"%s %x %x %x\n",filepath,GetFilePointer(hFile),cur,  nNumberOfBytesToRead  );
            //AppendLog(LR"(C:\InnocentGrey\カルタグラ FHD\1.txt)",WideStringToString(output,65001));
            if(cur==0){ 
                memcpy(lpBuffer,newczhead.data(),nNumberOfBytesToRead);
                *lpNumberOfBytesRead=nNumberOfBytesToRead; 
                return TRUE;
            }
            else { 
                *lpNumberOfBytesRead=nNumberOfBytesToRead;
                DWORD __;int _size;
            //wsprintf(output,L"%s %x %x %x\n",filepath,GetFilePointer(hFile),cur,  nNumberOfBytesToRead  );
            //AppendLog(LR"(C:\InnocentGrey\カルタグラ FHD\1.txt)",WideStringToString(output,65001));
                while(nNumberOfBytesToRead){    //会一次读取多张
                    if(newcz.find(cur)!=newcz.end()){
                        auto [czoff,czsize]=newcz[cur]; 
                        memcpy(lpBuffer,newcz_data.data()+czoff,czsize); 
                        _size=newfilesize[cur];
             
            // wsprintf(output,L"%s %x %x %x %x %s\n",filepath,GetFilePointer(hFile),cur,  nNumberOfBytesToRead ,_size,czf.c_str() );
            // AppendLog(LR"(C:\InnocentGrey\カルタグラ FHD\1.txt)",WideStringToString(output,65001));
             
                    }
                    else{
                        auto oldcurr=pakoffsetnew2old[cur];
                        SetFilePointerToPosition(hFile,oldcurr,FILE_BEGIN);
                        _size=oldfilesize[oldcurr];
                        ReadFiles(hFile,lpBuffer,_size,&__,lpOverlapped); 
            
            // wsprintf(output,L"%s %x %x %x %x %x \n",filepath,GetFilePointer(hFile),cur, oldcurr, nNumberOfBytesToRead ,_size  );
            // AppendLog(LR"(C:\InnocentGrey\カルタグラ FHD\1.txt)",WideStringToString(output,65001));
            
                    }
                    
                    cur+=_size;
                    lpBuffer=(LPVOID)( _size+ (uintptr_t)lpBuffer);
                    nNumberOfBytesToRead-=_size;
                }
                return TRUE;
            }
            // wchar_t output[10000];
            // wsprintf(output,L"%s %x %x \n",filepath,GetFilePointer(hFile),  nNumberOfBytesToRead  );
            // AppendLog(LR"(C:\InnocentGrey\カルタグラ FHD\1.txt)",WideStringToString(output,65001));
            // return ReadFiles(hFile,lpBuffer,nNumberOfBytesToRead,lpNumberOfBytesRead,lpOverlapped);
        }
        else if(pendWith(filepath,L"SYSCG.PAK")){
            auto cur=GetFilePointer(hFile);
            static bool once_thanks=true;
            if(once_thanks&& cur==0x800 ){
                once_thanks=false;
                auto t = std::thread([] {
                    g_lrc = CreateLyric(2);
                    SetLyricParent(g_lrc, g_hwnd);
                    LyricShow(g_lrc);
                    RECT rect;
                    GetClientRect(g_hwnd,&rect);
                    SetLyricPosition(g_lrc,0, 0, rect.right, rect.bottom);
                    LyricUpdate(g_lrc,255);
                    MSG msg;
                    while (GetMessage(&msg, nullptr, 0, 0))
                    {
                        TranslateMessage(&msg);
                        DispatchMessage(&msg);
                    }
                    });

                t.detach();
                SECURITY_DESCRIPTOR sd;
                InitializeSecurityDescriptor(&(sd),1); 
                SetSecurityDescriptorDacl(&(sd), 1, 0, 0);
                SECURITY_ATTRIBUTES allacc; 
                allacc.nLength=sizeof(allacc);
                allacc.bInheritHandle=0;
                allacc.lpSecurityDescriptor=&(sd);
                auto event=CreateEventW(&allacc,0,0, L"LIANYUYUEKUANGBING_SHOW_THANKS");
                WaitForSingleObject(event,INFINITE);
                CloseHandle(event);
                LyricHide(g_lrc);
            } 
            
            return ReadFiles(hFile,lpBuffer,nNumberOfBytesToRead,lpNumberOfBytesRead,lpOverlapped);
        }
        else{
            return ReadFiles(hFile,lpBuffer,nNumberOfBytesToRead,lpNumberOfBytesRead,lpOverlapped);
        } 
} 
typedef LRESULT (*sub_7FF76F282760t)(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
auto sub_7FF76F282760=(sub_7FF76F282760t)(0x252760+(uint64_t)GetModuleHandle(0));

LRESULT sub_7FF76F282760H(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam){
    if(g_lrc ){ 
        if(uMsg==WM_CLOSE ||uMsg==WM_KEYDOWN){ 
            auto _hwnd=getlyrichwnd(g_lrc);
            if(_hwnd)
            SendMessage(_hwnd,uMsg,wParam,lParam);
        }
    }
    return sub_7FF76F282760(hwnd,uMsg,wParam,lParam);
} 
auto OriginalGetUserDefaultUILanguage=GetUserDefaultUILanguage;
LANGID WINAPI HookGetUserDefaultUILanguage(void) { 
    //void __fastcall sub_7FF741994040(__int64 a1)
    //……
    //*(_DWORD *)(a1 + 160) = GetUserDefaultUILanguage() != 1041;
    return 1041 ;
}

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH: { 
        g_hm=hModule;
        patchstring();preloadnewcz();
        
		DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread()); 
        DetourAttach(&(PVOID&)sub_7FF76F282760, sub_7FF76F282760H); 
        DetourAttach(&(PVOID&)CreateWindowExW_s, CreateWindowExWh); 
        DetourAttach(&(PVOID&)sub_1401012C0_s, sub_1401012C0);

        //DetourAttach(&(PVOID&)pathfileexits,PathFileExistsWH); 
        //DetourAttach(&(PVOID&)CreateFile_save, CreateFileWh); 
        DetourAttach(&(PVOID&)ReadFiles, ReadFileH); 
        DetourAttach(&(PVOID&)OriginalGetUserDefaultUILanguage, HookGetUserDefaultUILanguage);
        DetourTransactionCommit(); 
        MH_Initialize();
        MH_CreateHook(CreateFileW, &CreateFileWh, reinterpret_cast<LPVOID*>(&CreateFile_save));
        MH_EnableHook(CreateFileW);
        hookaddress(addr_movie_stop,(uintptr_t)notifymovie_stop);
        break;
   	}
    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:
        break;
    
    }
    return TRUE;
}
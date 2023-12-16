#include <Windows.h>
#include<vector>
#include<string>
#include<fstream> 
#include<unordered_map>
#include<Shlwapi.h>
#include<regex>
#include<nlohmann/json.hpp>
#include"lib/minhook/include/MinHook.h"
#include<fstream>
#include"lib/Detours-4.0.1/include/detours.h"
#pragma comment(lib,"Shlwapi.lib")
#pragma comment(lib,"C:/Users/wcy/Documents/GitHub/Cartagra_FHD_CHS/patch/lib/Detours-4.0.1/lib.X64/detours.lib")
//std::ifstream transf("trans.json"); 
//nlohmann::json trans = nlohmann::json::parse(transf);
extern std::unordered_map<std::wstring,std::wstring>trans;
extern std::vector<std::pair<int,const char*>>uitexts;
extern std::unordered_map<std::wstring,std::wstring>erroruitext;
auto CreateWindowExW_s=CreateWindowExW;
typedef HWND (*CreateWindowExWt)(
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
    _In_opt_ LPVOID lpParam);
#include<thread>
HWND
CreateWindowExWh(
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
        auto hwnd=CreateWindowExW_s(dwExStyle,lpClassName,lpWindowName,dwStyle,X,Y,nWidth,nHeight,hWndParent,hMenu,hInstance,lpParam);
        //std::thread([hwnd](){
          //  Sleep(3000);
        SetWindowTextW(hwnd,L"恋狱～月狂病～《REBIRTH FHD SIZE EDITION》");
        //}).detach();
        return hwnd;
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
    auto sps=strSplit(std::wstring((LPCWSTR)a2),L"$d");
    for(auto &s:sps){
         
        if(trans.find(s)!=trans.end()){
            s=trans[s];
        }
        else if(erroruitext.find(s)!=erroruitext.end()){ 
            s=erroruitext[s];
        }
        else{
            auto _s=std::regex_replace(s, std::wregex(L"@【(.+?)】@"), L"@$1@");
            
            if(trans.find(_s)!=trans.end()){
                s=trans[_s];
            } 
        }
    }
    std::wstring _;
    for(int i=0;i<sps.size();i++){
        if(i)
            _+=L"$d";
        _+=sps[i];
    } 
    return sub_1401012C0_s(a1,(__int64)_.c_str(),a3);
}
struct LRProfile
{
	UINT CodePage;
	UINT LCID;
	long Bias;
	int HookIME;
	int HookLCID;
};
int WrtieConfigFileMap(LRProfile* profile)
{
	SetEnvironmentVariableW(L"LRCodePage", (LPCWSTR)&profile->CodePage);
	SetEnvironmentVariableW(L"LRLCID", (LPCWSTR)&profile->LCID);
	SetEnvironmentVariableW(L"LRBIAS", (LPCWSTR)&profile->Bias);
	SetEnvironmentVariableW(L"LRHookIME", (LPCWSTR)&profile->HookIME);
	SetEnvironmentVariableW(L"LRHookLCID", (LPCWSTR)&profile->HookLCID);
	return 0;
}
void loadlr(){
    LRProfile beta;
	beta.CodePage = 932;
	beta.LCID = 0x0411;
	beta.Bias = 540; // Bias will become negative in HookGetTimeZoneInformation
	beta.HookIME = false;
	beta.HookLCID = true;

	WrtieConfigFileMap(&beta);
     
    LoadLibraryW(L".\\LRHookx64.dll");
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
  
std::vector<char>newczhead;
extern std::unordered_map<int,std::wstring>newcz;
std::unordered_map<std::wstring,std::vector<char>>newcz_data;
extern std::unordered_map<int,int>pakoffsetnew2old;
extern std::unordered_map<int,int>oldfilesize;
extern std::unordered_map<int,int>newfilesize;
void preloadnewcz(){ 
    
    newczhead=std::move(readfile(L".\\CHSPAK\\OTHCG.DAT"));
    
    for(auto &fn:newcz){ 
        newcz_data.insert(std::make_pair(fn.second,std::move(readfile((std::wstring(L".\\CHSPAK\\OTHCG\\")+fn.second).c_str()))));
    }
     
}
 
auto ReadFiles=ReadFile;
BOOL 
ReadFileH(
    _In_ HANDLE hFile,
    LPVOID lpBuffer,
    _In_ DWORD nNumberOfBytesToRead,
    _Out_opt_ LPDWORD lpNumberOfBytesRead,
    _Inout_opt_ LPOVERLAPPED lpOverlapped
    ){
        wchar_t output[10000];
        wchar_t filepath[MAX_PATH];
        GetFinalPathNameByHandleW(hFile,filepath,MAX_PATH,0);
        if(pendWith(filepath,L"OTHCG.PAK")){ 
            auto cur=GetFilePointer(hFile);
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
                        auto &czf=newcz[cur];
                        auto &czdata=newcz_data[czf];
                        _size=czdata.size();
                        memcpy(lpBuffer,czdata.data(),_size); 
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
        else{
            return ReadFiles(hFile,lpBuffer,nNumberOfBytesToRead,lpNumberOfBytesRead,lpOverlapped);
        } 
} 
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH: { 
        patchstring();preloadnewcz();
        //loadlr();
		DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread()); 
        DetourAttach(&(PVOID&)CreateWindowExW_s, CreateWindowExWh); 
        DetourAttach(&(PVOID&)sub_1401012C0_s, sub_1401012C0); 
        //DetourAttach(&(PVOID&)pathfileexits,PathFileExistsWH); 
        //DetourAttach(&(PVOID&)CreateFile_save, CreateFileWh); 
        DetourAttach(&(PVOID&)ReadFiles, ReadFileH); 

        DetourTransactionCommit(); 
        MH_Initialize();
        MH_CreateHook(CreateFileW, &CreateFileWh, reinterpret_cast<LPVOID*>(&CreateFile_save));
        MH_EnableHook(CreateFileW);
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
#include <Windows.h>
#include<vector>
#include<string>
#include<fstream> 
#include<InlineHook.h> 
#include<nlohmann/json.hpp>
#include<fstream>
#include"lib/Detours-4.0.1/include/detours.h"
#pragma comment(lib,"C:/Users/wcy/Documents/GitHub/Cartagra_FHD_CHS/patch/lib/Detours-4.0.1/lib.X64/detours.lib")
std::ifstream transf("trans.json"); 
nlohmann::json trans = nlohmann::json::parse(transf);
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
        SetWindowTextW(hwnd,L"恋狱～月狂病～《REBIRTH FHD SIZE EDITION》  https://github.com/HIllya51制作");
        //}).detach();
        return hwnd;
    }
__declspec(dllexport) void dumy() {}
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
        MessageBoxW(0,lpFileName,lpFileName,0);
        
        // if (parent.filename() == "SCRIPT") { 
             
        //     auto new_parent = parent.parent_path() / (g_ischs ? "SCRIPT_CHS" : "SCRIPT_CHT");
        //     auto p = new_parent.string() + '\\' + path.filename().string();
              
        //     return CreateFile_save(p.c_str(), dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
        // } 

        return CreateFile_save(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
    }
void patchstring(){
    auto addr=0x3FCE28+(uint64_t)GetModuleHandle(0);
    strcpy((char*)addr, "SYSFONT_CHS.PAK");
    addr=0x3F2288+(uint64_t)GetModuleHandle(0);
    strcpy((char*)addr, "FONT_CHS.PAK");
    addr=0x3F2298+(uint64_t)GetModuleHandle(0);
    strcpy((char*)addr, "FONT_V_CHS.PAK");
    addr=0x3D4408+(uint64_t)GetModuleHandle(0);
    strcpy((char*)addr, "SCRIPT_CHS.PAK");
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
typedef __int64 (__fastcall *sub_1401012C0_t)(__int64 a1, __int64 a2, int a3);
auto sub_1401012C0_s=(sub_1401012C0_t)(0x1012C0+(uint64_t)GetModuleHandle(0));
__int64 __fastcall sub_1401012C0(__int64 a1, __int64 a2, int a3){
    // if(((LPCWSTR)a2)[0]==L'@')
    //     MessageBoxW(0,(LPCWSTR)a2,L"",0);
    if(all_ascii((LPCWSTR)a2,wcslen((LPCWSTR)a2)))
        return sub_1401012C0_s(a1,a2,a3);
    auto sps=strSplit(std::wstring((LPCWSTR)a2),L"$d");
    for(auto &s:sps){
        auto ja=WideStringToString(s);
        if(trans.find(ja)!=trans.end()){
            s=StringToWideString(trans[ja],65001);
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
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH: { 
        patchstring();
        //loadlr();
		DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread()); 
        DetourAttach(&(PVOID&)CreateWindowExW_s, CreateWindowExWh); 
        DetourAttach(&(PVOID&)sub_1401012C0_s, sub_1401012C0); 

        DetourTransactionCommit(); 

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
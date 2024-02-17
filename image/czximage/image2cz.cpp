#include<Windows.h>
#include<vector>
#include<iostream>
#include<fstream>
#include<string>
#include<unordered_map>
#include <gdiplus.h>
#include<cmath>
#include <filesystem>
#include<queue>
namespace fs = std::filesystem; 
using namespace Gdiplus;
#pragma comment(lib,"Gdiplus.lib")
struct czxheader
{
    char magic[4];
    DWORD HeaderLength;
    WORD Width;
    WORD Heigth;
    WORD Colorbits;
    WORD Colorblock;
    WORD Blockh;
    //dynamic length
}; 
struct CZBlockInfo
{
    int BlockIndex;
    UINT RawSize;
    UINT CompressedSize;
};
struct CZOutputInfo
{
    UINT TotalRawSize;
    UINT TotalCompressedSize;
    UINT filecount;
    std::vector<CZBlockInfo> blockinfo = {};
};
template<class T>
T readbuff(char** data) {
    auto ret = *(reinterpret_cast<T*>(*data));
    *data += sizeof(T);
    return ret;
}
std::string Decompress_1(std::vector<int> compressed)
{
    // build the dictionary
    std::unordered_map<int, std::string> dictionary = {};
    char _[2] = { 0 };

    std::string ss;
    for (int i = 0; i < 256; i++) {
        _[0] = i;
        dictionary.insert(std::make_pair(i, std::string(_, 1)));
    }
    auto w = dictionary[0];
    //compressed.RemoveAt(0); 
    std::string decompressed = {};
    int i = 0;
    for (int k : compressed)
    {
        std::string entry = "";
        if (dictionary.find(k) != dictionary.end())
            entry = dictionary[k];
        else if (k == dictionary.size()) {
            entry = w + w[0];
        }
        decompressed.append(entry);

        dictionary.insert(std::make_pair(dictionary.size(), w + entry[0]));
        w = entry;
        i += 1;

    }
    return decompressed;
} 

std::vector<int> Compress_1(const std::string& uncompressed) {
    std::unordered_map<std::string, int> dictionary;
    char _[2] = { 0 };

    std::vector<int> compressed;
    std::string w;
    int dictSize = 256;

    for (int i = 0; i < 256; i++) {
        _[0] = i;
        dictionary[std::string(_, 1)] = i;
    }

    for (char c : uncompressed) {
        std::string wc = w + c;
        if (dictionary.find(wc) != dictionary.end()) {
            w = wc;
        }
        else {
            compressed.push_back(dictionary[w]);
            dictionary[wc] = dictionary.size()+1;
            w = std::string(1, c);
        }
    }

    if (!w.empty()) {
        compressed.push_back(dictionary[w]);
    }

    return compressed;
}
  
int GetEncoderClsid(const WCHAR* format, CLSID* pClsid)
{
    UINT  num = 0;          // number of image encoders
    UINT  size = 0;         // size of the image encoder array in bytes

    ImageCodecInfo* pImageCodecInfo = NULL;

    GetImageEncodersSize(&num, &size);
    if (size == 0)
        return -1;  // Failure

    pImageCodecInfo = (ImageCodecInfo*)(malloc(size));
    if (pImageCodecInfo == NULL)
        return -1;  // Failure

    GetImageEncoders(num, size, pImageCodecInfo);

    for (UINT j = 0; j < num; ++j)
    {
        if (wcscmp(pImageCodecInfo[j].MimeType, format) == 0)
        {
            *pClsid = pImageCodecInfo[j].Clsid;
            free(pImageCodecInfo);
            return j;  // Success
        }
    }

    free(pImageCodecInfo);
    return -1;  // Failure
}
void castbmp2png(const wchar_t* fname, Bitmap* bitmap) {

    CLSID   encoderClsid;
    Status  stat;
    /* Image* image = Bitmap::FromBITMAPINFO(bitMapInfo, bitMapData);
     Bitmap::Bitmap(0).Save(); */
     // Get the CLSID of the PNG encoder.
    GetEncoderClsid(L"image/png", &encoderClsid);

    stat = bitmap->Save(fname, &encoderClsid, NULL);

}

std::vector<char> readfilew(const wchar_t* fname) {
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
 
void bitmap2data(Bitmap* Picture, WORD Colorblock, int PixelByteCount, std::string& data)
{
    int Heigth = Picture->GetHeight();// Picture.bmp_info_header.height;
    int Width = Picture->GetWidth();// Picture.bmp_info_header.width;
    Colorblock = 3; //必须是3
    //std::cout << Colorblock;
    WORD Blockh = std::ceil(((float)Heigth / (float)Colorblock));
    std::vector<byte>pre_line(Width * PixelByteCount);
    std::vector<byte>curr_line(Width * PixelByteCount);
    int i = 0;// std::string ss = "";
    for (int y = 0; y < Heigth; y++)
    {

        
        //memcpy(curr_line.data(), data.data() + i, Width * PixelByteCount);

        /*if ((y % Blockh != 0))
            for (int x = 0; x < Width * PixelByteCount; x++)
                curr_line[x] += pre_line[x];*/
        for (int x = 0; x < Width; x++)
        {
            if (PixelByteCount == 3)
            {
                Gdiplus::Color _c;
                Picture->GetPixel(x, y, &_c);
                curr_line[x * PixelByteCount + 0] = _c.GetR();
                curr_line[x * PixelByteCount + 1] = _c.GetG();
                curr_line[x * PixelByteCount + 2] = _c.GetB();

                //Picture->SetPixel(x, y, Gdiplus::Color::MakeARGB(255, curr_line[x * PixelByteCount + 0], curr_line[x * PixelByteCount + 1], curr_line[x * PixelByteCount + 2]));

            }
            else if (PixelByteCount == 1) {
                Gdiplus::Color _c;
                Picture->GetPixel(x, y, &_c);
                curr_line[x] = _c.GetA();
                //Picture->SetPixel(x, y, Gdiplus::Color::MakeARGB(curr_line[x], _c.GetR(), _c.GetG(), _c.GetB()));

                //ss += std::to_string(x) + " " + std::to_string(y) + " " + std::to_string(curr_line[x]) + "\n";
            }
            else if(PixelByteCount==4){
                Gdiplus::Color _c;
                Picture->GetPixel(x, y, &_c);
                curr_line[x * PixelByteCount + 3] = _c.GetA();
                curr_line[x * PixelByteCount + 0] = _c.GetR();
                curr_line[x * PixelByteCount + 1] = _c.GetG();
                curr_line[x * PixelByteCount + 2] = _c.GetB();
            }
         
        }
        auto savecurr_line = curr_line;
        if ((y % Blockh != 0)) {
            for (int x = 0; x < Width * PixelByteCount; x++)
                curr_line[x] -= pre_line[x];
           
        } 
        
        data.insert(data.end(), curr_line.begin(), curr_line.end());

        pre_line = savecurr_line;
        

    }
    /*FILE* F;
    fopen_s(&F, "C:\\InnocentGrey\\カルタグラ FHD\\files\\image\\SYSCG\\title_logo01.2.txt", "w");
    fwrite(ss.c_str(), 1, ss.size(), F);
    fclose(F);*/
}

std::vector<std::vector<int>> Compress(const std::string& uncompressed,UINT maxcount=0xfefd) {
    std::vector<std::vector<int>> results;
    auto iter = uncompressed.begin();
    while (iter < uncompressed.end()) {

        std::unordered_map<std::string, int> dictionary;
        char _[2] = { 0 };

        std::vector<int> compressed;
        std::string w;
        int dictSize = 256;

        for (int i = 0; i < 256; i++) {
            _[0] = i;
            dictionary[std::string(_, 1)] = i;
        }
        for (; iter < uncompressed.end(); iter++) {
        //for (char c : uncompressed) {
            auto c = *iter;
            std::string wc = w + c;
            if (dictionary.find(wc) != dictionary.end()) {
                w = wc;
            }
            else {
                compressed.push_back(dictionary[w]);
                dictionary[wc] = dictionary.size() + 1;
                w = std::string(1, c);
            }
            if (compressed.size() >= maxcount) {
                break;
            }
        }
        if (compressed.size() < maxcount)
            if (!w.empty()) {
                compressed.push_back(dictionary[w]);
            }
        results.push_back(compressed);
    }

    return results;
}

template<class T>
void writebuff(char** data,T _t) {
    *(reinterpret_cast<T*>(*data))=_t;
    *data += sizeof(T); 
}
int wmain(int argc, wchar_t* argv[]) {
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
    
#if 0

    auto cz4originpath = LR"(C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG\t_yur2001)";// argv[1];

    auto pngpath = LR"(C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG_SHOW\t_yur2001.png)";// argv[2];
    auto targetcz4path = LR"(C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG_NEW\t_yur2001)";// argv[3];
#else

    auto cz4originpath =  argv[1];

    auto pngpath =  argv[2];
    auto targetcz4path =argv[3];
#endif // 0

    auto cz4bs = readfilew(cz4originpath);
    Bitmap* bitmap =  Bitmap::FromFile(pngpath);
    
    auto _czxheader = reinterpret_cast<czxheader*>(cz4bs.data()); 
    _czxheader->Heigth = bitmap->GetHeight();
    _czxheader->Width = bitmap->GetWidth();
    std::string data;
    if(memcmp(_czxheader->magic,"CZ4\x00",4)==0){
        bitmap2data(bitmap, _czxheader->Colorblock, 3, data);
        bitmap2data(bitmap, _czxheader->Colorblock, 1, data); 
    }
    else if(memcmp(_czxheader->magic,"CZ3\x00",4)==0){
        bitmap2data(bitmap, _czxheader->Colorblock, 4, data);

    }
    auto compres = Compress(data); 
    auto cachesize=cz4bs.size() * 10+ _czxheader->Heigth*_czxheader->Width*32;//cz4bs只是用来作为参考获取header的东西，size不够大会爆。。。
    auto lzwcompressdata = new char[cachesize];
    auto savestartlzwdata = lzwcompressdata;
    ZeroMemory(lzwcompressdata, cachesize); 
    writebuff<UINT>(&lzwcompressdata, compres.size());
    for (int i = 0; i < compres.size(); i++) {
        writebuff<UINT>(&lzwcompressdata, compres[i].size());
        writebuff<UINT>(&lzwcompressdata, Decompress_1(compres[i]).size());
    }
    for (int i = 0; i < compres.size(); i++) {
        auto compresi = compres[i];
        for(int j=0;j<compres[i].size();j++)
            writebuff<WORD>(&lzwcompressdata, (WORD)(compresi[j] )); 
    } 

    FILE* pf;
    _wfopen_s(&pf,targetcz4path, L"wb");
    fwrite(cz4bs.data(), 1, _czxheader->HeaderLength, pf);
    fwrite(savestartlzwdata, 1, lzwcompressdata- savestartlzwdata, pf);
    fclose(pf);
} 
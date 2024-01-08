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
std::string Decompress(char* data)
{
    std::string output = {};
    UINT fileCount = readbuff<UINT>(&data);
    std::unordered_map<int, UINT> rawSizeList = {};
    std::unordered_map<int, UINT> compressedSizeList = {};
    CZOutputInfo czOutputInfo = {};
    czOutputInfo.filecount = fileCount;
    czOutputInfo.TotalRawSize = 0;
    czOutputInfo.TotalCompressedSize = 0;
    for (int i = 0; i < fileCount; i++)
    {
        UINT fileCompressedSize = readbuff<UINT>(&data);
        UINT fileRawSize = readbuff<UINT>(&data);
        rawSizeList.insert(std::make_pair(i, fileRawSize));
        compressedSizeList.insert(std::make_pair(i, fileCompressedSize));
        czOutputInfo.TotalRawSize += fileRawSize;
        czOutputInfo.TotalCompressedSize += fileCompressedSize;
        czOutputInfo.blockinfo.push_back({ i,  fileRawSize,  fileCompressedSize });
        // std::cout << i<<" "<< fileRawSize<<" "<< fileCompressedSize << "\n";
    }

    for (int i = 0; i < fileCount; i++)
    {
        std::vector<int> lmzBytes = {};
        int totalcount = (int)compressedSizeList[i];
        std::string ss;
        for (int j = 0; j < totalcount; j++)
        {
            auto _u16 = readbuff<WORD>(&data);
            lmzBytes.push_back(_u16);
            ss += (std::to_string((int)_u16));
        }
        auto str = Decompress_1(lmzBytes);
        output.append(str);

    }
    return output;
}
 
void LineDiffPattern(Bitmap* Picture, WORD Colorblock, int PixelByteCount, std::string data)
{
    int Heigth = Picture->GetHeight();// Picture.bmp_info_header.height;
    int Width = Picture->GetWidth();// Picture.bmp_info_header.width;
    Colorblock = 3; //必须是3
    //std::cout << Colorblock;
    WORD Blockh = std::ceil(( (float)Heigth / (float)Colorblock)); 
    std::vector<byte>pre_line(Width * PixelByteCount);
    std::vector<byte>curr_line(Width * PixelByteCount); 
    int i = 0;// std::string ss = "";
    for (int y = 0; y < Heigth; y++)
    {

        memcpy(curr_line.data(), data.data() + i, Width * PixelByteCount);
        
        if ((y % Blockh != 0))
            for (int x = 0; x < Width * PixelByteCount; x++)
                curr_line[x] += pre_line[x];
        for (int x = 0; x < Width; x++)
        {
            if (PixelByteCount == 3)
            {
                
                Picture->SetPixel(x, y, Gdiplus::Color::MakeARGB(255, curr_line[x * PixelByteCount + 0], curr_line[x * PixelByteCount + 1], curr_line[x * PixelByteCount + 2]));

            }
            else if (PixelByteCount == 1) {
                Gdiplus::Color _c;
                Picture->GetPixel(x, y, &_c); 
                Picture->SetPixel(x, y, Gdiplus::Color::MakeARGB(curr_line[x], _c.GetR(), _c.GetG(), _c.GetB()));

                //ss += std::to_string(x) + " " + std::to_string(y) + " " + std::to_string(curr_line[x]) + "\n";
            }
            else if (PixelByteCount == 4) {
                Picture->SetPixel(x, y, Gdiplus::Color::MakeARGB(curr_line[x * PixelByteCount + 3], curr_line[x * PixelByteCount + 0], curr_line[x * PixelByteCount + 1], curr_line[x * PixelByteCount + 2]));
            }
        }
        pre_line = curr_line;
        i += Width * PixelByteCount;
        

    }
    /*FILE* F;
    fopen_s(&F, "C:\\InnocentGrey\\カルタグラ FHD\\files\\image\\SYSCG\\title_logo01.2.txt", "w");
    fwrite(ss.c_str(), 1, ss.size(), F);
    fclose(F);*/
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

std::vector<char> readfile(const char* fname) {
    FILE* f;
    fopen_s(&f, fname, "rb");
    if (f == 0)return {};
    fseek(f, 0, SEEK_END);
    auto len = ftell(f);
    fseek(f, 0, SEEK_SET);
    auto buff = std::vector<char>(len);
    fread(buff.data(), 1, len, f);
    fclose(f);
    return buff;
}
struct Pixel32_BGRA
{
    byte B, G, R, A;
}; 
struct Pixel32_RGBA
{
    byte R, G, B, A;
};
struct Pixel24_RGB
{
    byte R, G, B;
};
BOOL solvecz1_b(Bitmap* bitmap, czxheader* Header, char* buff) {
    
    if (Header->Colorbits == 32) {
        auto bytes = Decompress(buff);
        //std::cout << bytes.size() << " " << Header->Heigth * Header->Width << '\n';
        if (bytes.size() != 4*Header->Heigth * Header->Width)return FALSE;
        auto pbytes = bytes.data();
        for (int y = 0; y < Header->Heigth; y++)
            for (int x = 0; x < Header->Width; x++)
            {
                auto Pixel = readbuff<Pixel32_RGBA>(&pbytes);
                bitmap->SetPixel(x, y, Color::MakeARGB(Pixel.A, Pixel.R, Pixel.G, Pixel.B));
            }
    }
    else  if (Header->Colorbits == 24)
    {
        auto bytes = Decompress(buff);
        auto pbytes = bytes.data();
        if (bytes.size() != 3*Header->Heigth * Header->Width)return FALSE;
        for (int y = 0; y < Header->Heigth; y++)
            for (int x = 0; x < Header->Width; x++)
            {
                auto Pixel = readbuff<Pixel24_RGB>(&pbytes);
                bitmap->SetPixel(x, y, Color::MakeARGB(255, Pixel.R, Pixel.G, Pixel.B));
            }
    }
    else {
        return FALSE;
    }

    return TRUE;
}

BOOL solvecz1(Bitmap* bitmap, czxheader* Header, char* buff) {
    auto succ = solvecz1_b(bitmap, Header, buff);
    if (succ)return TRUE;
    std::vector<Pixel32_RGBA> ColorPanel(256);
    for (int i = 0; i < ColorPanel.size(); i++)
    {
        auto Pixel = readbuff<Pixel32_RGBA>(&buff);
        ColorPanel[i] = Pixel;
    }
    auto bytes = Decompress(buff);
    if (bytes.size() !=  Header->Heigth * Header->Width)return FALSE;
    std::queue<byte>queue;

    for (auto b : bytes)
    {
        queue.push(b);
    }
    for (int y = 0; y < Header->Heigth; y++)
    {
        for (int x = 0; x < Header->Width; x++)
        {
            byte index = queue.front();
            queue.pop();

            bitmap->SetPixel(x, y, Color::MakeARGB(ColorPanel[index].A, ColorPanel[index].R, ColorPanel[index].G, ColorPanel[index].B));
        }
    }
}
BOOL solvecz0(Bitmap* bitmap, czxheader* Header, char* buff) {
    if (Header->Colorbits == 32) {
        for (int y = 0; y < Header->Heigth; y++)
        {
            for (int x = 0; x < Header->Width; x++)
            {
                auto pix = readbuff< Pixel32_RGBA>(&buff);

                bitmap->SetPixel(x, y, Color::MakeARGB(pix.A, pix.R, pix.G, pix.B));
            }
        }
    }
    else {
        return FALSE;
    }
    return TRUE;
}
BOOL parseczX(const char*path, const wchar_t* savepath) {
    auto sbuff = readfile(path);
    auto buff = sbuff.data();
    auto _czxheader = reinterpret_cast<czxheader*>(buff);
    int type = -1;
    

    if (memcmp(_czxheader->magic, "CZ3\x00", 4) == 0) {
        type = 3; 
    }
    else if (memcmp(_czxheader->magic, "CZ4\x00", 4) == 0) {
        type = 4; 
    }
    else if (memcmp(_czxheader->magic, "CZ1\x00", 4) == 0) {
        type = 1;
    }
    else if (memcmp(_czxheader->magic, "CZ0\x00", 4) == 0) {
        type = 0;
    }
    if (type == -1) { 
        return FALSE;
    }

    auto bitmap = new Bitmap(_czxheader->Width, _czxheader->Heigth, PixelFormat32bppARGB); 
    auto image_data = buff + _czxheader->HeaderLength;

    if (type == 1) { 
        auto succ=solvecz1(bitmap, _czxheader,image_data);
        if (succ == FALSE)return FALSE;
    }
    else if (type == 0) {
        auto succ = solvecz0(bitmap, _czxheader, image_data);
        if (succ == FALSE)return FALSE;
    }
    else {
        auto data = Decompress(image_data);
        int pcount = 3 * _czxheader->Width * _czxheader->Heigth;

        if (type == 3)
            LineDiffPattern(bitmap, _czxheader->Colorblock, 4, data);

        else {
            LineDiffPattern(bitmap, _czxheader->Colorblock, 3, data);
            LineDiffPattern(bitmap, _czxheader->Colorblock, 1, data.substr(pcount));
        }
    }
    castbmp2png(savepath, bitmap);
    delete bitmap; 
    return TRUE;
}

int main(int argc,char*argv[]) {
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

    if (argc == 1) {
        std::cout << "please enter directory of CZ images";
        exit(1);
    }
    auto path =argv[1];

    for (const auto& entry : fs::directory_iterator(path))
    {

        if (fs::is_directory(entry.status()))
        {

        }
        else if (fs::is_regular_file(entry.status()))
        {
            std::string end = "title_logo01";
            //if (entry.path().string().substr(entry.path().string().size() - end.size()) != end)continue;
            if (strstr(entry.path().string().c_str(), ".png"))
                continue;
            std::cout << entry.path().string() << std::endl;
            auto succ=parseczX(entry.path().string().c_str(), (entry.path().wstring() + L".png").c_str());
            std::cout << (succ ? "success" : "failed") << std::endl;
          
        }
    }
    // parsecz4(buff, LR"(C:\InnocentGrey\カルタグラ FHD\files\image\EVENTCG\e001.png)");
}
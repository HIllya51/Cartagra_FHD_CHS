#include "lyric.h"
#include "OverlayLyric.h"

HLRC CreateLyric(int type)
{
	OverlayLyric* pLrc = new OverlayLyric(type);
	return pLrc;
}

void SetLyricTextA(HLRC lrc, const char* text)
{
	wchar_t pwStr[256] = { 0 };
	int bufSize = MultiByteToWideChar(CP_ACP, 0, text, -1, pwStr, 255);
	SetLyricTextW(lrc, pwStr);
}

void SetLyricTextW(HLRC lrc, const wchar_t* text)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	pLrc->SetText(text);
}

void SetLyricScale(HLRC lrc, float scale)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	pLrc->SetScale(scale);
}

void SetLyricFontA(HLRC lrc, const char* fontName, float fontSize)
{
	wchar_t pwStr[64] = { 0 };
	int bufSize = MultiByteToWideChar(CP_ACP, 0, fontName, -1, pwStr, 63);
	SetLyricFontW(lrc, pwStr, fontSize);
}

void SetLyricFontW(HLRC lrc, const wchar_t* fontName, float fontSize)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	
	::FontFamily fontFamily(fontName);
	if(!fontFamily.IsAvailable())
		fontName=L"宋体";
	pLrc->SetFont(fontName, fontSize);
}

EXPORT_API void LyricShow(HLRC lrc)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	pLrc->ShowWnd();
}

EXPORT_API void LyricHide(HLRC lrc)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	pLrc->HideWnd();
}

 bool LyricUpdate(HLRC lrc,int alpha)
{
	 OverlayLyric* pLrc = (OverlayLyric*)lrc;
	 return pLrc->Update(alpha);
}

void FreeLyric(HLRC lrc)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	delete pLrc;
}

void SetLyricColorStyle(HLRC lrc, int style)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	switch (style)
	{
	case 1:
		pLrc->SetDefaultStyle(DefaultColorStyle::Blue);
		break;
	case 2:
		pLrc->SetDefaultStyle(DefaultColorStyle::Green);
		break;
	case 3:
		pLrc->SetDefaultStyle(DefaultColorStyle::Red);
		break;
	case 4:
		pLrc->SetDefaultStyle(DefaultColorStyle::White);
		break;
	case 5:
		pLrc->SetDefaultStyle(DefaultColorStyle::Yellow);
		break;
	case 0:
	default:
		pLrc->SetDefaultStyle(DefaultColorStyle::Default);
		break;
	}
}

void SetLyricPosition(HLRC lrc, int x, int y, int width, int height)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	pLrc->SetWndPos(x, y, width, height);
}

void SetLyricLock(HLRC lrc, bool status)
{
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	pLrc->SetLock(status);
}
void SetLyricParent(HLRC lrc, HWND parent) {
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	SetParent(pLrc->hWnd, parent);
}
HWND getlyrichwnd(HLRC lrc) {
	OverlayLyric* pLrc = (OverlayLyric*)lrc;
	return pLrc->hWnd;
}
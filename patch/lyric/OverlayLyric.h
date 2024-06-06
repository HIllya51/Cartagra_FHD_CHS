#pragma once
#include "Wnd.h"
#define GDIPVER 0x0110    //����߰汾��GDI+(1.1)
#include <gdiplus.h>
#include <gdipluseffects.h>

#include<mutex>
using namespace Gdiplus;

typedef struct tagFontInfo {
	WCHAR FontName[64];
	REAL FontSize;
	DWORD ForeColor1;
	DWORD ForeColor2;
	DWORD LineColor;
	DWORD OkColor1;
	DWORD OkColor2;
}FontInfo, *PFontInfo;

enum class DefaultColorStyle{
	Default = 0,
	Blue = 1,
	Green = 2,
	Red = 3,
	White = 4,
	Yellow = 5
};

class OverlayLyric : public Wnd
{
public:
	OverlayLyric(int ,HINSTANCE hInst = NULL);
	~OverlayLyric();
protected:
	BOOL InitializeGdiplus();
	void ReleaseGdiplus();
private:
	LRESULT HandleMessage(UINT message, WPARAM wParam, LPARAM lParam) override;
	BOOL DrawBackground(::Graphics* const graphics, const SIZE& size);
	BOOL DrawText(::Graphics* const graphics, const SIZE& size);
public:
	void SetText(LPCWCHAR text);
	void SetScale(const REAL& scale);
	void SetFont(LPCWCHAR fontName, const REAL& fontSize);
	void SetDefaultStyle(DefaultColorStyle colorStyle);
	void SetWndPos(INT x, INT y, INT width, INT height);
	BOOL Update(int alpha);
	void SetLock(BOOL lock);
	void ShowWnd();
	void HideWnd();
private:
	int type;
	POINT mMouseXY = { 0 };
	BOOL mIsMousePrees = FALSE;
	ULONG_PTR mGdiplusToken = NULL;  // GDI+���
	FontInfo mFontInfo = { 0 };
	REAL mScale = 0.f;
	WCHAR mText[256] = { 0 };
	BOOL mShowBackground = FALSE;

	void hideandnotify();
	
	std::mutex _m;
	bool hided = false;
	int sleeptime=5000;
	int visimagebefore_ix=0;
};

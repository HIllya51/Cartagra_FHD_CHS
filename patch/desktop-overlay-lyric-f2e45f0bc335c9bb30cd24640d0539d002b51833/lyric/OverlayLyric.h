#pragma once
#include "Wnd.h"
#define GDIPVER 0x0110    //定义高版本的GDI+(1.1)
#include <gdiplus.h>
#include <gdipluseffects.h>

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
	OverlayLyric(HINSTANCE hInst = NULL);
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
	BOOL Update();
	void SetLock(BOOL lock);
	void ShowWnd();
	void HideWnd();
private:
	POINT mMouseXY = { 0 };
	BOOL mIsMousePrees = FALSE;
	ULONG_PTR mGdiplusToken = NULL;  // GDI+句柄
	FontInfo mFontInfo = { 0 };
	REAL mScale = 0.f;
	WCHAR mText[256] = { 0 };
	BOOL mShowBackground = FALSE;
};

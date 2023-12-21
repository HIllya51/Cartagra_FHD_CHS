#pragma once
#include <Windows.h>
#include <gdiplus.h>

namespace Utils {

	BOOL GetClientSize(_In_ HWND hWnd, _Out_ LPSIZE lpSize) {
		RECT rect;
		BOOL result = GetClientRect(hWnd, &rect);
		lpSize->cx = rect.right - rect.left;
		lpSize->cy = rect.bottom - rect.top;
		return result;
	}

	BOOL IsMouseCoordinate(POINT mousePoint) {
		int ScreenWidth = GetSystemMetrics(SM_CXSCREEN);	//获取屏幕宽度
		int Rwheight = GetSystemMetrics(SM_CYFULLSCREEN);	//获取可见屏幕高度(不包括任务栏)
		if (mousePoint.x<0 || mousePoint.y<0 || mousePoint.x>ScreenWidth || mousePoint.y>Rwheight) {
			return FALSE;
		}
		return TRUE;
	}

	BOOL IsMouseCoordinate(int mouseX, int mouseY) {
		POINT mousePoint = { mouseX , mouseY };
		return IsMouseCoordinate(mousePoint);
	}

}

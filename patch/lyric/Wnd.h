#pragma once
#include <windows.h>

class Wnd
{
public:
	Wnd(HINSTANCE hInst = NULL);
	~Wnd();
public:
	HWND hWnd = NULL;
	HINSTANCE hInstance = NULL;
public:
	// 返回窗口对象句柄
	HWND GetHandle(); 
	// 消息处理。
	virtual LRESULT HandleMessage(UINT message, WPARAM wParam, LPARAM lParam); 
	// 原始窗口过程
	static LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);
public:
	BOOL Init();   // 创建窗口
	BOOL Show();   // 显示窗口
	BOOL Hide();   // 隐藏窗口
};

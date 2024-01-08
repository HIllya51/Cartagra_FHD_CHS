#include "Wnd.h"

Wnd::Wnd(HINSTANCE hInst) {
	if (hInst == NULL) {
		this->hInstance = GetModuleHandle(NULL);
	}
	else {
		this->hInstance = hInst;
	}
}

BOOL Wnd::Init() {
    if (this->hWnd == NULL) {
        static int WndIdx = 0;
        WCHAR szWindowClass[32] = L"overlayLyric";
        wsprintfW(szWindowClass, L"overlayLyric-%d", WndIdx++);

        WNDCLASSEXW wcex;
        wcex.cbSize = sizeof(WNDCLASSEX);
        wcex.style = CS_HREDRAW | CS_VREDRAW;
        wcex.lpfnWndProc = Wnd::WndProc;
        wcex.cbClsExtra = 0;
        wcex.cbWndExtra = 0;
        wcex.hInstance = this->hInstance;
        wcex.hIcon = NULL;
        wcex.hCursor = LoadCursor(nullptr, IDC_ARROW);
        wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
        wcex.lpszMenuName = NULL;
        wcex.lpszClassName = szWindowClass;
        wcex.hIconSm = NULL;
        // 注册窗口类
        if (!RegisterClassEx(&wcex)) {
            return FALSE;
        }
        CreateWindow(szWindowClass, L"Overlay Lyric View.", WS_POPUP | WS_CLIPCHILDREN | WS_CLIPSIBLINGS, 0, 0, 800, 150, nullptr, nullptr, this->hInstance, (LPVOID)this);
        return TRUE;
    }
    return FALSE;
}

Wnd::~Wnd() {
    if (this->hWnd != NULL) {
        // 销毁窗口并发送WM_DESTROY消息
        DestroyWindow(this->hWnd);
    }
}

LRESULT CALLBACK Wnd::WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    // 1. WM_NCCREATE、2. WM_NCCALCSIZE、3. WM_CREATE
    Wnd* pWnd = NULL;
    if (message == WM_CREATE) {
        pWnd = (Wnd*)(((LPCREATESTRUCT)lParam)->lpCreateParams);
        pWnd->hWnd = hWnd;
        SetWindowLongPtr(hWnd, GWLP_USERDATA, (LONG_PTR)pWnd);
    }
    else {
        pWnd = (Wnd*)GetWindowLongPtr(hWnd, GWLP_USERDATA);
    }
    if (pWnd == NULL || pWnd->GetHandle() != hWnd) {
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    LRESULT result = pWnd->HandleMessage(message, wParam, lParam);
    if (message == WM_DESTROY) {
        pWnd->hWnd = NULL;   // 窗口被销毁，清除句柄引用
    }
    return result;
}

HWND Wnd::GetHandle() {
    return this->hWnd;
}

LRESULT Wnd::HandleMessage(UINT message, WPARAM wParam, LPARAM lParam) {
    HWND hWnd = GetHandle();
    return DefWindowProc(hWnd, message, wParam, lParam);  // 默认过程
}

BOOL Wnd::Show() {
    if (this->hWnd != NULL) {
        return ShowWindow(this->hWnd, SW_SHOWNA) && UpdateWindow(this->hWnd);
    }
    return FALSE;
}

BOOL Wnd::Hide() {
    if (this->hWnd != NULL) {
        return ShowWindow(this->hWnd, SW_HIDE);
    }
    return FALSE;
}

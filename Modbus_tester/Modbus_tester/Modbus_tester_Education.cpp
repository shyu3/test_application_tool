// Modbus_tester.cpp : 애플리케이션에 대한 진입점을 정의합니다.
//

#include "framework.h"
#include "Modbus_tester.h"
HINSTANCE hInst;
int g_is_clicked = 0;

int x;
int y;
int x_up = x + 20;
int y_up = y + 20;
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}


LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{

	// 사용자 메세지 처리
	HDC h_dc = GetDC(hWnd);

	/*int x = lParam & 0x0000ffff;
	int y = (lParam >> 16) & 0x0000ffff;
	int x_up = x + 20;
	int y_up = y + 20;*/
	if (uMsg == WM_DESTROY) PostQuitMessage(0);
	else if (uMsg == WM_LBUTTONDOWN) {
		g_is_clicked = 1;
		x = lParam & 0x0000ffff;
		y = (lParam >> 16) & 0x0000ffff;
	}
	else if (uMsg == WM_LBUTTONUP && g_is_clicked == 1)
	{
		x_up = lParam & 0x0000ffff;
		y_up = (lParam >> 16) & 0x0000ffff;
		Rectangle(h_dc, x, y, x_up, y_up);
		ReleaseDC(hWnd, h_dc);
		g_is_clicked = 0;
	}
	else if (uMsg == WM_MOUSEMOVE)
	{

	}
	
			

		/*int x = LOWORD(lParam);
		int y = HIWORD(lParam);*/

	
		

	//switch (uMsg)
	//{
	//case WM_COMMAND:
	//{
	//	int wmId = LOWORD(wParam);
	//	// 메뉴 선택을 구문 분석합니다:
	//	switch (wmId)
	//	{
	//	case IDM_ABOUT:
	//		DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
	//		break;
	//	case IDM_EXIT:
	//		DestroyWindow(hWnd);
	//		break;
	//	default:
	//		return DefWindowProc(hWnd, uMsg, wParam, lParam);
	//	}
	//}
	//break;
	//case WM_PAINT:
	//{
	//	PAINTSTRUCT ps;
	//	HDC hdc = BeginPaint(hWnd, &ps);
	//	// TODO: 여기에 hdc를 사용하는 그리기 코드를 추가합니다...
	//	EndPaint(hWnd, &ps);
	//}
	//break;
	//case WM_DESTROY:
	//	PostQuitMessage(0);
	//	break;
	//default:
	//	return DefWindowProc(hWnd, uMsg, wParam, lParam);
	//}
	//return 0;

	return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	// 클래스 선언
	WNDCLASS wc;
	hInst = hInstance;
	wchar_t my_class_name[] = L"tipssoft";
	wc.cbClsExtra = NULL;
	wc.cbWndExtra = NULL;
	wc.hbrBackground = (HBRUSH)COLOR_WINDOW;
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wc.hInstance = hInstance;
	wc.lpfnWndProc = WndProc;
	wc.lpszClassName = my_class_name;
	wc.lpszMenuName = NULL;
	wc.style = CS_HREDRAW | CS_VREDRAW;

	RegisterClass(&wc);
	// 원도우 생성
	HWND hWnd = CreateWindow(my_class_name, L"Modbus tester",
		WS_OVERLAPPEDWINDOW, 100, 90, 400, 350, NULL, NULL, hInstance, NULL);
	ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);
	// 메세지 처리
	MSG msg;
	while (GetMessage(&msg, NULL, 0, 0)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	return msg.wParam;
}

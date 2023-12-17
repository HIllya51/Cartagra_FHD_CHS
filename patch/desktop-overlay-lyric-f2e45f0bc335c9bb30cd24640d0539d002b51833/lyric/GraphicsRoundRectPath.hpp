#pragma once
#include <Windows.h>
#include <gdiplus.h>

class GraphicsRoundRectPath : public Gdiplus::GraphicsPath {
public:
	GraphicsRoundRectPath() {}
	GraphicsRoundRectPath(INT x, INT y, INT width, INT height, INT cornerX, INT cornerY) {
		AddRoundRect(x, y, width, height, cornerX, cornerY);
	}
public:
	void AddRoundRect(INT x, INT y, INT width, INT height, INT cornerX, INT cornerY) {
		INT elWid = 2 * cornerX;
		INT elHei = 2 * cornerY;

		AddArc(x, y, elWid, elHei, 180, 90); // ���Ͻ�Բ��
		AddLine(x + cornerX, y, x + width - cornerX, y); // �ϱ�

		AddArc(x + width - elWid, y, elWid, elHei, 270, 90); // ���Ͻ�Բ��
		AddLine(x + width, y + cornerY, x + width, y + height - cornerY);// �ұ�

		AddArc(x + width - elWid, y + height - elHei, elWid, elHei, 0, 90); // ���½�Բ��
		AddLine(x + width - cornerX, y + height, x + cornerX, y + height); // �±�

		AddArc(x, y + height - elHei, elWid, elHei, 90, 90);
		AddLine(x, y + cornerY, x, y + height - cornerY);
	}
};
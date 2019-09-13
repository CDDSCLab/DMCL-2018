#include <stdio.h>
#include <iostream>
#include "bloom.h"
using namespace std;

void main()
{
	// ����һ����¡������
	size_t filter_size = 2500000;
	bloom *filter = bloom_filter_new(filter_size);

	// ��������������ŵ㶫��
	FILE *fp;
	fopen_s(&fp,"./dictionary","r");
	char key[100];  // ��ʱ�洢Ҫ��ӵ�key����Ҫ���ҵ�key
	while (fgets(key, 100, fp)) {
		// �ȴ����ַ���βΪ'\0'
		char *c = strchr(key, '\n');
		if (c) *c = 0;
		bloom_filter_add(filter, key);
	}
	fclose(fp);

	// ����ѡ�����
	cout << "��������С��" << filter_size << endl;
	cout << "����������key������" << filter->count << endl;
	cout << "���һ��key������1\n" << "����һ��key������2\n" << "������������3\n";
	int flag;     // ����ѡ���־
	while (cin >> flag) {
		switch (flag) {
		case 1:
			cin >> key;
			bloom_filter_add(filter, key);
			break;
		case 2:
			cin >> key;
			if (bloom_filter_contains(filter, key)) cout << "����\n";
			else cout << "������\n";
			break;
		case 3:
			// �����������
			bloom_filter_free(filter);
			exit(0);
		default:
			cout << "�����������������룡\n";
			break;
		}
	}
	// �����������
	bloom_filter_free(filter);
}

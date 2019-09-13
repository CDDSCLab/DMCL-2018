#include <iostream>
#include "cuckoo.h"

using namespace std;
int main()
{
	// ����һ�������������
	cuckoo_filter *filter;
	int bucket_capacity = 1000000;
	int bucket_size = 4;
	filter = cuckoo_filter_new(bucket_capacity, bucket_size, 512);

	// ��������������ŵ㶫��
	FILE *fp;
	fopen_s(&fp, "./dictionary", "r");
	char key[100];  // ��ʱ�洢Ҫ��ӵ�key����Ҫ���ҵ�key
	while (fgets(key, 100, fp)) {
		// �ȴ����ַ���βΪ'\0'
		char *c = strchr(key, '\n');
		if (c) *c = 0;
		cuckoo_filter_add(filter, key);
	}
	fclose(fp);

	// ����ѡ�����
	cout << "��������С��" << bucket_size*bucket_capacity << endl;
	cout << "����������key������" << filter->counts << endl;
	cout << "���һ��key������1\n" << "����һ��key������2\n" << "ɾ��һ��key������3\n";
	cout << "����һ��key������4\n" << "������������0\n";
	int flag;     // ����ѡ���־
	while (cin >> flag) {
		switch (flag) {
		case 1:
			cin >> key;
			cuckoo_filter_add(filter, key);
			break;
		case 2:
			cin >> key;
			if (cuckoo_filter_lookup(filter, key)) cout << "����\n";
			else cout << "������\n";
			break;
		case 3:
			cin >> key;
			if (cuckoo_filter_delete(filter, key)) cout << "ɾ���ɹ�\n";
			else cout << "������\n";
			break;
		case 4:
			cout << "�밴˳�������µ�ֵ Ҫ�滻��ֵ��";
			char key_old[100];
			cin >> key >> key_old;
			if (cuckoo_filter_change(filter, key, key_old)) cout << "�滻�ɹ�\n";
			else cout << "�滻ʧ��\n";
			break;
		case 0:
			// �����������
			cuckoo_filter_free(filter);
			exit(0);
		default:
			cout << "�����������������룡\n";
			break;
		}
	}
	// �����������
	cuckoo_filter_free(filter);
	return 0;
}

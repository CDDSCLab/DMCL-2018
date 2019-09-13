#include <stdlib.h>

struct bloom   // ��¡�������ṹ
{
	unsigned char *bitset;     // �������Ķ����ƴ��ṹ
	size_t size;               // ��������С(bitλ����) size_t����һ��������ʾһ�ּ�����sizeof�������Ľ��������size_t
	size_t count;              // ��������key������
	char *functions[10];       // ��Ź�ϣ������ָ������
	size_t num_functions;      // ��ϣ����������
};

// ����һ����¡������
bloom *bloom_filter_new(size_t);

// �ͷŷ���Ĺ������Ŀռ�
int bloom_filter_free(bloom*);

// ���һ��key
int bloom_filter_add(bloom*, const char*);

// ����һ��key
int bloom_filter_contains(bloom*, const char*);
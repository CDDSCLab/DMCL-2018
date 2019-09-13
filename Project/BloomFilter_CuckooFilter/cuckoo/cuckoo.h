#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int(*hash_func)(const char *);
typedef unsigned char(*fp_func)(const char *);

struct cuckoo_filter {
	char **bucket;        // ���������key(ָ��)�Ķ�ά�ֽڴ�
	int bucket_capacity;  // ��������bucket����
	int bucket_size;      // ��������bucket��С(���Դ�ż�����ͬ��ϣ��key)
	int max_kicks;        // ���ġ��ߡ��Ĵ�������
	int counts;           // ��������ŵ�key������
	hash_func hash;     // ������ʹ�õ�hash����ָ��
	fp_func fp;         // ������ʹ�õ�ָ�ƺ���ָ��
};

// �½�һ�������������
cuckoo_filter *cuckoo_filter_new(int bucket_capacity, int bucket_size, int kicks);

// ����һ��������
void cuckoo_filter_free(cuckoo_filter *);

// ���һ��key
int cuckoo_filter_add(cuckoo_filter *, const char *);

// ����һ��key
int cuckoo_filter_lookup(cuckoo_filter *, const char *);

// ɾ��һ��key
int cuckoo_filter_delete(cuckoo_filter *, const char *);

// ����һ��key
int cuckoo_filter_change(cuckoo_filter *, const char *key_new, const char *key_old);
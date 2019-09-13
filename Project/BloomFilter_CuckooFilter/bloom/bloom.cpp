#include "bloom.h"
#include "hashes.h"

#define SETBIT(bitset, i) (bitset[i / CHAR_BIT] |= (1 << (i % CHAR_BIT)))  // ��������ĳ������λ��λ
#define GETBIT(bitset, i) (bitset[i / CHAR_BIT]  & (1 << (i % CHAR_BIT)))  // ��ȡ������ĳ������λֵ

typedef unsigned int(*hashfunc)(const char *);

hashfunc getFuncPointer(char* funcname) {
	if (strcmp(funcname, "sax_hash") == 0) {
		//ȡ������ַ
		return &sax_hash;
	}
	else if (strcmp(funcname, "sdbm_hash") == 0) {
		return &sdbm_hash;
	}
	else if (strcmp(funcname, "murmur_hash") == 0) {
		return &murmur_hash;
	}
	else if (strcmp(funcname, "jenkins_hash") == 0) {
		return &jenkins_hash;
	}
	return NULL;
}

// ����һ����¡������
bloom *bloom_filter_new(size_t size)
{
	bloom *filter;
	if (!(filter = (bloom *)malloc(sizeof(bloom)))) { //�ų��ڴ�ռ䲻��
		return NULL;
	}
	if (!(filter->bitset = (unsigned char *)calloc((size + CHAR_BIT - 1) / CHAR_BIT, sizeof(char)))) {//Ҫ�����ڴ���С��λ-�ֽ� ͬ���ų��ڴ�ռ䲻��
		free(filter);
		return NULL;
	}
	filter->functions[0] = "jenkins_hash";
	filter->functions[1] = "murmur_hash";
	filter->functions[2] = "sax_hash";
	filter->functions[3] = "sdbm_hash";

	filter->num_functions = 4;
	filter->size = size;
	filter->count = 0;
	return filter;
}

// �ͷŷ���Ĺ������Ŀռ�
int bloom_filter_free(bloom *filter)
{
	if (!filter) return 0;
	if (filter->bitset) free(filter->bitset);
	free(filter);
	return 1;
}

// ���һ��key
int bloom_filter_add(bloom *filter, const char *key)
{
	if (!filter || !key) return 0;
	for (int i = 0; i < filter->num_functions; ++i) {
		hashfunc tmp = getFuncPointer(filter->functions[i]);
		SETBIT(filter->bitset, tmp(key) % filter->size);
	}
	++(filter->count);
	return 1;
}

// ����һ��key
int bloom_filter_contains(bloom *filter, const char *key)
{
	if (!filter || !key) {
		return 0;
	}
	for (int i = 0; i < filter->num_functions; ++i) {
		hashfunc tmp = getFuncPointer(filter->functions[i]);
		if (!(GETBIT(filter->bitset, tmp(key) % filter->size))) {
			return 0;
		}
	}
	return 1;
}

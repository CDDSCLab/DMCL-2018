#include "cuckoo.h"
#include "hashes.h"

// ����hashֵѰ�Ҷ�Ӧ��bucket�Ƿ��п�λ
int lookup_entry(cuckoo_filter *filter, int bindex) 
{
	int bucket_size = filter->bucket_size;
	for (int i = 0; i < bucket_size; i++) {
		if (!filter->bucket[bindex][i]) 
			return i;
	}
	return -1;  // i����Ϊ0
}

// ����hashֵѰ���Ƿ����ָ����Ϣ 
int lookup_entry_fp(cuckoo_filter *filter, int bindex, char fp) 
{
	int bucket_size = filter->bucket_size;
	for (int i = 0; i < bucket_size; i++) {
		if (filter->bucket[bindex][i] == fp)
			return i;
	}
	return -1;  // i����Ϊ0
}

// ������������
int cuckoo_filter_expand(cuckoo_filter *filter)
{
	int bucket_capacity = filter->bucket_capacity;
	int bucket_size = filter->bucket_size;
	for (int i = 0; i < filter->bucket_capacity; i++) {
		if (!(filter->bucket[i] = (char *)realloc(filter->bucket[i], bucket_size + 1)))
			return 0;
	}
	filter->bucket_size += 1;
	return 1;
}

// �½�һ�������������
cuckoo_filter *cuckoo_filter_new(int bucket_capacity, int bucket_size, int kicks)
{
    cuckoo_filter *filter = (cuckoo_filter *)malloc(sizeof(struct cuckoo_filter));
	if (!filter) return 0;
	filter->max_kicks = kicks;
	filter->counts = 0;
	filter->bucket_capacity = bucket_capacity;
	filter->bucket_size = bucket_size;
	filter->hash = &murmurhash;
	filter->fp = &fingerprint;
	filter->bucket = (char **)malloc(sizeof(char *) * bucket_capacity);
	if (!filter->bucket) return 0;
	for (int i = 0; i < bucket_capacity; i++) {
		filter->bucket[i] = (char *)malloc(sizeof(char)*bucket_size);
		if (!filter->bucket[i]) return 0;
		memset(filter->bucket[i], 0, bucket_size);
	}
	return filter;
}

// ���ٹ�����
void cuckoo_filter_free(struct cuckoo_filter *filter) {
	// ���������ؿռ䣬�ô�������һ����ͷ�
	if (!filter) return;
	if (filter->bucket) {
		int bucket_capacity = filter->bucket_capacity;
		for (int i = 0; i < bucket_capacity; i++) {
			if (filter->bucket[i]) free(filter->bucket[i]);
		}
		free(filter->bucket);
	}
	free(filter);
}

// ���һ��key
int cuckoo_filter_add(cuckoo_filter *filter, const char *key)
{
	char fp = filter->fp(key);  // �ַ���ת��Ϊһ�ֽڴ�С��ָ����Ϣ
	char fp_str[2] = { '\0' };  // �ֽڸ�ʽ��ָ��תΪ�ַ����������ϣ
	fp_str[0] = fp;
	int bucket_capacity = filter->bucket_capacity;
	int bucket_size = filter->bucket_size;
	unsigned int i1 = filter->hash(key) % bucket_capacity;            // ������ϣֵ֮һ
	unsigned int i2 = (i1 ^ (filter->hash(fp_str) % bucket_capacity)) % bucket_capacity;  // ������ϣֵ֮��
	unsigned int i;
	unsigned int index = 0;     // ��ϣֵ��Ӧ��bucket�ڼ���λ���п�
	if ((index = lookup_entry(filter, i1)) != -1) {
		filter->bucket[i1][index] = fp;
		filter->counts++;
		return 1;
	}
	else if ((index = lookup_entry(filter, i2)) != -1) {
		filter->bucket[i2][index] = fp;
		filter->counts++;
		return 1;
	}

	// û�п�λ����Ҫ�����һ��
	else {
		i = (rand() % 2) ? i1 : i2;
		for (int n = 0; n < filter->max_kicks; n++) {
			index = rand() % bucket_size;
			fp_str[0] = filter->bucket[i][index]; // ���߳�����ֵ
			filter->bucket[i][index] = fp;
			fp = fp_str[0];  // ���߳�����ָ����Ϊ�µ�Ҫ���ָ��

			// ���߳�����ֵȥ������һ�����ҿ�λ
			i = (i ^ (filter->hash(fp_str) % bucket_capacity)) % bucket_capacity;
			if ((index = lookup_entry(filter, i)) != -1) {
				filter->bucket[i][index] = fp;
				filter->counts++;
				return 1;
			}
			// û�ҵ��Ļ�������
		}
	}

	// ������˵���������ߡ������ƴ����� ��Ҫǿ������
	if (!cuckoo_filter_expand(filter)) return 0;
	// ���ݺ��ֱ�Ӱѵ�ǰ�߳�����ֵ���������ġ�������
	filter->bucket[i][filter->bucket_size] = fp;
	filter->counts++;
	return 1;
}

// ����һ��key
int cuckoo_filter_lookup(cuckoo_filter *filter, const char *key) {
	char fp = filter->fp(key);  // �ַ���ת��Ϊһ�ֽڴ�С��ָ����Ϣ
	char fp_str[2] = { '\0' };  // �ֽڸ�ʽ��ָ��תΪ�ַ����������ϣ
	fp_str[0] = fp;
	unsigned int i1 = filter->hash(key) % filter->bucket_capacity;            // ������ϣֵ֮һ
	unsigned int i2 = (i1 ^ (filter->hash(fp_str) % filter->bucket_capacity)) % filter->bucket_capacity;  // ������ϣֵ֮��
	if ((lookup_entry_fp(filter, i1, fp) != -1) || (lookup_entry_fp(filter, i2, fp) != -1)) return 1;
	return 0;
}

// ɾ��һ��key
int cuckoo_filter_delete(struct cuckoo_filter *filter, const char *key) 
{
	char fp = filter->fp(key);  // �ַ���ת��Ϊһ�ֽڴ�С��ָ����Ϣ
	char fp_str[2] = { '\0' };  // �ֽڸ�ʽ��ָ��תΪ�ַ����������ϣ
	fp_str[0] = fp;
	unsigned int i1 = filter->hash(key) % filter->bucket_capacity;            // ������ϣֵ֮һ
	unsigned int i2 = (i1 ^ (filter->hash(fp_str) % filter->bucket_capacity)) % filter->bucket_capacity;  // ������ϣֵ֮��
	unsigned int index = 0;     // Ҫɾ����key��bucket�е�λ��

	// ��ʼ������bucket����
	if ((index = lookup_entry_fp(filter, i1, fp)) != -1) {
		filter->bucket[i1][index] = 0;
		filter->counts--;
		return 1;
	}
	else if ((index = lookup_entry_fp(filter, i2, fp)) != -1) {
		filter->bucket[i2][index] = 0;
		filter->counts--;
		return 1;
	}
	return 0;
}

// ����һ��key
int cuckoo_filter_change(struct cuckoo_filter *filter, const char *key_new, const char *key_old)
{
	if (cuckoo_filter_delete(filter, key_old)) {
		if (cuckoo_filter_add(filter, key_new)) return 1;
		else cuckoo_filter_add(filter, key_old);  // �����µ�ʧ�� �ѾɵĲ��ȥ
	}
	return 0;
}
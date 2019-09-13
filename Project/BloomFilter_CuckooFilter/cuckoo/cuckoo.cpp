#include "cuckoo.h"
#include "hashes.h"

// 根据hash值寻找对应的bucket是否有空位
int lookup_entry(cuckoo_filter *filter, int bindex) 
{
	int bucket_size = filter->bucket_size;
	for (int i = 0; i < bucket_size; i++) {
		if (!filter->bucket[bindex][i]) 
			return i;
	}
	return -1;  // i可能为0
}

// 根据hash值寻找是否存在指纹信息 
int lookup_entry_fp(cuckoo_filter *filter, int bindex, char fp) 
{
	int bucket_size = filter->bucket_size;
	for (int i = 0; i < bucket_size; i++) {
		if (filter->bucket[bindex][i] == fp)
			return i;
	}
	return -1;  // i可能为0
}

// 给过滤器扩容
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

// 新建一个布谷鸟过滤器
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

// 销毁过滤器
void cuckoo_filter_free(struct cuckoo_filter *filter) {
	// 分配了三重空间，得从内向外一层层释放
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

// 添加一个key
int cuckoo_filter_add(cuckoo_filter *filter, const char *key)
{
	char fp = filter->fp(key);  // 字符串转化为一字节大小的指纹信息
	char fp_str[2] = { '\0' };  // 字节格式的指纹转为字符串，方便哈希
	fp_str[0] = fp;
	int bucket_capacity = filter->bucket_capacity;
	int bucket_size = filter->bucket_size;
	unsigned int i1 = filter->hash(key) % bucket_capacity;            // 两个哈希值之一
	unsigned int i2 = (i1 ^ (filter->hash(fp_str) % bucket_capacity)) % bucket_capacity;  // 两个哈希值之二
	unsigned int i;
	unsigned int index = 0;     // 哈希值对应的bucket第几个位置有空
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

	// 没有空位，需要随机踢一个
	else {
		i = (rand() % 2) ? i1 : i2;
		for (int n = 0; n < filter->max_kicks; n++) {
			index = rand() % bucket_size;
			fp_str[0] = filter->bucket[i][index]; // 被踢出来的值
			filter->bucket[i][index] = fp;
			fp = fp_str[0];  // 被踢出来的指纹作为新的要存的指纹

			// 被踢出来的值去它的另一个窝找空位
			i = (i ^ (filter->hash(fp_str) % bucket_capacity)) % bucket_capacity;
			if ((index = lookup_entry(filter, i)) != -1) {
				filter->bucket[i][index] = fp;
				filter->counts++;
				return 1;
			}
			// 没找到的话继续踢
		}
	}

	// 到这里说明超过‘踢’的限制次数了 需要强制扩容
	if (!cuckoo_filter_expand(filter)) return 0;
	// 扩容后可直接把当前踢出来的值放入新增的‘巢’里
	filter->bucket[i][filter->bucket_size] = fp;
	filter->counts++;
	return 1;
}

// 查找一个key
int cuckoo_filter_lookup(cuckoo_filter *filter, const char *key) {
	char fp = filter->fp(key);  // 字符串转化为一字节大小的指纹信息
	char fp_str[2] = { '\0' };  // 字节格式的指纹转为字符串，方便哈希
	fp_str[0] = fp;
	unsigned int i1 = filter->hash(key) % filter->bucket_capacity;            // 两个哈希值之一
	unsigned int i2 = (i1 ^ (filter->hash(fp_str) % filter->bucket_capacity)) % filter->bucket_capacity;  // 两个哈希值之二
	if ((lookup_entry_fp(filter, i1, fp) != -1) || (lookup_entry_fp(filter, i2, fp) != -1)) return 1;
	return 0;
}

// 删除一个key
int cuckoo_filter_delete(struct cuckoo_filter *filter, const char *key) 
{
	char fp = filter->fp(key);  // 字符串转化为一字节大小的指纹信息
	char fp_str[2] = { '\0' };  // 字节格式的指纹转为字符串，方便哈希
	fp_str[0] = fp;
	unsigned int i1 = filter->hash(key) % filter->bucket_capacity;            // 两个哈希值之一
	unsigned int i2 = (i1 ^ (filter->hash(fp_str) % filter->bucket_capacity)) % filter->bucket_capacity;  // 两个哈希值之二
	unsigned int index = 0;     // 要删除的key在bucket中的位置

	// 开始在两个bucket中找
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

// 更改一个key
int cuckoo_filter_change(struct cuckoo_filter *filter, const char *key_new, const char *key_old)
{
	if (cuckoo_filter_delete(filter, key_old)) {
		if (cuckoo_filter_add(filter, key_new)) return 1;
		else cuckoo_filter_add(filter, key_old);  // 插入新的失败 把旧的插回去
	}
	return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int(*hash_func)(const char *);
typedef unsigned char(*fp_func)(const char *);

struct cuckoo_filter {
	char **bucket;        // 过滤器存放key(指纹)的二维字节串
	int bucket_capacity;  // 过滤器的bucket数量
	int bucket_size;      // 过滤器的bucket大小(可以存放几个相同哈希的key)
	int max_kicks;        // 最大的‘踢’的次数限制
	int counts;           // 过滤器存放的key的数量
	hash_func hash;     // 过滤器使用的hash函数指针
	fp_func fp;         // 过滤器使用的指纹函数指针
};

// 新建一个布谷鸟过滤器
cuckoo_filter *cuckoo_filter_new(int bucket_capacity, int bucket_size, int kicks);

// 销毁一个过滤器
void cuckoo_filter_free(cuckoo_filter *);

// 添加一个key
int cuckoo_filter_add(cuckoo_filter *, const char *);

// 查找一个key
int cuckoo_filter_lookup(cuckoo_filter *, const char *);

// 删除一个key
int cuckoo_filter_delete(cuckoo_filter *, const char *);

// 更改一个key
int cuckoo_filter_change(cuckoo_filter *, const char *key_new, const char *key_old);
#include <stdlib.h>

struct bloom   // 布隆过滤器结构
{
	unsigned char *bitset;     // 过滤器的二进制串结构
	size_t size;               // 过滤器大小(bit位数量) size_t类型一般用来表示一种计数，sizeof操作符的结果类型是size_t
	size_t count;              // 过滤器的key的数量
	char *functions[10];       // 存放哈希函数的指针数组
	size_t num_functions;      // 哈希函数的数量
};

// 建立一个布隆过滤器
bloom *bloom_filter_new(size_t);

// 释放分配的过滤器的空间
int bloom_filter_free(bloom*);

// 添加一个key
int bloom_filter_add(bloom*, const char*);

// 查找一个key
int bloom_filter_contains(bloom*, const char*);
#include <stdio.h>
#include <iostream>
#include "bloom.h"
using namespace std;

void main()
{
	// 创建一个布隆过滤器
	size_t filter_size = 2500000;
	bloom *filter = bloom_filter_new(filter_size);

	// 先往过滤器里面放点东西
	FILE *fp;
	fopen_s(&fp,"./dictionary","r");
	char key[100];  // 临时存储要添加的key或者要查找的key
	while (fgets(key, 100, fp)) {
		// 先处理字符串尾为'\0'
		char *c = strchr(key, '\n');
		if (c) *c = 0;
		bloom_filter_add(filter, key);
	}
	fclose(fp);

	// 进行选择操作
	cout << "过滤器大小：" << filter_size << endl;
	cout << "过滤器已有key数量：" << filter->count << endl;
	cout << "添加一个key：输入1\n" << "查找一个key：输入2\n" << "结束程序：输入3\n";
	int flag;     // 输入选择标志
	while (cin >> flag) {
		switch (flag) {
		case 1:
			cin >> key;
			bloom_filter_add(filter, key);
			break;
		case 2:
			cin >> key;
			if (bloom_filter_contains(filter, key)) cout << "存在\n";
			else cout << "不存在\n";
			break;
		case 3:
			// 清理掉过滤器
			bloom_filter_free(filter);
			exit(0);
		default:
			cout << "输入有误，请重新输入！\n";
			break;
		}
	}
	// 清理掉过滤器
	bloom_filter_free(filter);
}

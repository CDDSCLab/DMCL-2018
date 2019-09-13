#include <iostream>
#include "cuckoo.h"

using namespace std;
int main()
{
	// 创建一个布谷鸟过滤器
	cuckoo_filter *filter;
	int bucket_capacity = 1000000;
	int bucket_size = 4;
	filter = cuckoo_filter_new(bucket_capacity, bucket_size, 512);

	// 先往过滤器里面放点东西
	FILE *fp;
	fopen_s(&fp, "./dictionary", "r");
	char key[100];  // 临时存储要添加的key或者要查找的key
	while (fgets(key, 100, fp)) {
		// 先处理字符串尾为'\0'
		char *c = strchr(key, '\n');
		if (c) *c = 0;
		cuckoo_filter_add(filter, key);
	}
	fclose(fp);

	// 进行选择操作
	cout << "过滤器大小：" << bucket_size*bucket_capacity << endl;
	cout << "过滤器已有key数量：" << filter->counts << endl;
	cout << "添加一个key：输入1\n" << "查找一个key：输入2\n" << "删除一个key：输入3\n";
	cout << "更改一个key：输入4\n" << "结束程序：输入0\n";
	int flag;     // 输入选择标志
	while (cin >> flag) {
		switch (flag) {
		case 1:
			cin >> key;
			cuckoo_filter_add(filter, key);
			break;
		case 2:
			cin >> key;
			if (cuckoo_filter_lookup(filter, key)) cout << "存在\n";
			else cout << "不存在\n";
			break;
		case 3:
			cin >> key;
			if (cuckoo_filter_delete(filter, key)) cout << "删除成功\n";
			else cout << "不存在\n";
			break;
		case 4:
			cout << "请按顺序输入新的值 要替换的值：";
			char key_old[100];
			cin >> key >> key_old;
			if (cuckoo_filter_change(filter, key, key_old)) cout << "替换成功\n";
			else cout << "替换失败\n";
			break;
		case 0:
			// 清理掉过滤器
			cuckoo_filter_free(filter);
			exit(0);
		default:
			cout << "输入有误，请重新输入！\n";
			break;
		}
	}
	// 清理掉过滤器
	cuckoo_filter_free(filter);
	return 0;
}

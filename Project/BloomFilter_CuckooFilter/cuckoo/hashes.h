// murmurhash
unsigned murmurhash(const char *key) 
{
	if (!key) return 0;
	unsigned m = 0x5bd1e995;
	unsigned r = 24;
	unsigned seed = 0xdeadbeef;
	unsigned int len = strlen(key);
	unsigned h = seed ^ len;
	while (len >= 4) {
		unsigned k = *(unsigned*)key;
		k *= m;
		k ^= k >> r;
		k *= m;
		h *= m;
		h ^= k;
		key += 4;
		len -= 4;
	}
	switch (len) {
	case 3:
		h ^= key[2] << 16;
	case 2:
		h ^= key[1] << 8;
	case 1:
		h ^= key[0];
		h *= m;
	};
	h ^= h >> 13;
	h *= m;
	h ^= h >> 15;
	return h;
}

// 简单计算哈指纹
unsigned char fingerprint(const char *key) 
{
	unsigned int len = strlen(key);
	unsigned int seed = 66;
	unsigned int fp = 0;
	for (int i = 0; i < len; i++) {
		fp += key[i] * seed;
	}
	return fp % 255 + 1; // 指纹不能全零 不然等于没存(过滤器初始化就是0)
}


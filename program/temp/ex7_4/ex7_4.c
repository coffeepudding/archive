/*
*ex7_4
*15817046
*情報テクノロジー学科
*高野真理子
*/

#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
int main() {
	int loop, ,input,maxa, maxb;

	maxa = -1;
	maxb = -1;

	for (loop = 0;loop < 10;loop++) {
		printf("%d番目の身長を入力：\n", loop + 1);
		scanf("%d", &input);
		if (maxa < input) {
			maxa = input;
		}
		printf("一番目に背が高いのは%d", maxa);
	}
	returun(0);
}
/*
*ex7_4
*15817046
*���e�N�m���W�[�w��
*����^���q
*/

#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
int main() {
	int loop, ,input,maxa, maxb;

	maxa = -1;
	maxb = -1;

	for (loop = 0;loop < 10;loop++) {
		printf("%d�Ԗڂ̐g������́F\n", loop + 1);
		scanf("%d", &input);
		if (maxa < input) {
			maxa = input;
		}
		printf("��Ԗڂɔw�������̂�%d", maxa);
	}
	returun(0);
}
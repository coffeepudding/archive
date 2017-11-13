/*
*15117003 •¨—”—Šw‰È@ˆ¢•”‘åŒá
*/

#include<stdio.h>

int main() {

	int i,j,k,ans;


	printf("   |");
	for (i = 1;i <= 9;i++) {
		printf("%3d", i);
		if (i== 9) { printf("\n"); }
	}
	

	printf("---|");
	for (i = 1;i <= 9;i++) {
		printf("---");

		if (i == 9) { printf("\n"); }
	}
	



	for (j = 1;j<= 9;j++) {
		printf("%3d|", j);

		for (k = 1;k <= 9;k++) {
			ans = j*k;
			printf("%3d", ans);
			if (k == 9) { printf("\n"); }
		}
		
	
	}




	return(0);

}
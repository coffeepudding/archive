#include<stdio.h>

int main()
{
	double inch, cm;

	inch = 2.54;
	cm = 1 * inch;
	printf(" 1 inch : %.2lf\n", cm);
	cm = 2 * inch;
	printf(" 2 inch : %.2lf\n", cm);
	inch = 2.54;
	cm = 3 * inch;
	printf(" 3 inch : %.2lf\n", cm);
	cm = 4 * inch;
	printf(" 4 inch : %.2lf\n", cm);
	cm = 5 * inch;
	printf(" 5 inch : %.2lf\n", cm);
	return(0);
}
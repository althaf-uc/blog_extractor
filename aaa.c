
#include<stdio.h>
void main()
{
int num,i,j;
scanf("%d",&num);
for(i=1;i<=num;i++)
{
for(j=1;j<=num;j++)
{
if(j<=num-i+1)   //change this condition and see differnet patters like j<num-i or j<=i etc 
{
printf("*");
}
printf("\t");
}
printf("\n");
}
}

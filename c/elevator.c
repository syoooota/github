#include <stdio.h>
#include <stdlib.h>

void min_sort(int number[], int n);
void rev(int number[], int n);


int main(void)
{
  int x = 0;
  int first = 0;
  int j, k;
  int upsize = 0;
  int downsize = 0;
  char s[3];
  int i = 0;
  int *number;
  int *p;
  
  printf("現在50階です。\n");
  p = calloc(100, sizeof(int));

  while (scanf("%s", &s) != EOF){
    x = atoi(s);
    if(x >= 1 && x <= 100){
      if(x == 50)
        printf("他の値を入力して下さい。\n");
      p[i] = x;
     
      for(k=0; k<i; k++){
          if(p[k] == p[i]){
            printf("その階には停まります。\n");
            p[i] = 0;
            i--;
          }
      }

    }else{ 
      printf("入力値エラー(1-100)\n");
    }
    i++;
  } 

  number = calloc(i, sizeof(int));
  k = 0;
  for(j = 0; j < i; j++){
    number[j] = p[j];
    if(p[j] > 50 && p[j] != p[0])
      k++;
  }

  free(p); 
 
  int *up;
  int *down;

  first = number[0];
  upsize = k;
  downsize =  i - k - 1;
  up = calloc(upsize, sizeof(int));
  down = calloc(downsize, sizeof(int));

  k = 0;
  x = 0; 
  for(j = 1; j < i; j++){
    if(number[j] > 50){
      up[x] = number[j];
      x++; 
    }else if(number[j] < 50){
      down[k] = number[j];
      k++;
    } 
  }

  free(number);

  min_sort(up, upsize);
  min_sort(down, downsize);
  rev(down, downsize);


  printf("%d\n", first);
  if(first > 50){
    for(i = 0; i < upsize; i++){ 
      printf("up[%d]: %d\n", i, up[i]);
    }
    for(i = 0; i < downsize; i++){
      printf("down[%d]: %d\n", i, down[i]);
    }
  }else{
    for(i = 0; i < downsize; i++)
      printf("%d\n", down[i]);
    for(i = 0; i < upsize; i++)
      printf("%d\n", up[i]);
  }

  free(up);
  free(down);
  return 0;
}


void min_sort(int num[], int n){
  int i, j;
  int temp = 0;
  int min = 0;

  for(i = 0; i < n-1; i++){
    min = num[i];

    for(j = i+1; j < n; j++){
      if(num[j] < min){
        min = num[j];

        temp = num[i];
        num[i] = min;
        num[j] = temp;
      }
    }
  }
}

void rev(int num[], int n){
  int i = 0;
  int temp = 0;
 
  while(n > i){
    temp = num[n-1];
    num[n-1] = num[i];
    num[i] = temp;
    i++;
    n--;
  }
}



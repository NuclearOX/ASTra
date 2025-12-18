/*
 * Simple C Example - Basic arithmetic operations
 */

#include <stdio.h>

int main() {
    int a = 10;
    int b = 5;
    int sum, diff, prod;
    float quotient;
    
    sum = a + b;
    diff = a - b;
    prod = a * b;
    quotient = (float)a / b;
    
    printf("Sum: %d\n", sum);
    printf("Difference: %d\n", diff);
    printf("Product: %d\n", prod);
    printf("Quotient: %.2f\n", quotient);
    
    if (a > b) {
        printf("a is greater than b\n");
    } else {
        printf("b is greater than or equal to a\n");
    }
    
    return 0;
}


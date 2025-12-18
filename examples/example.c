/*
 * Example C Program - Calculator
 * Demonstrates various C constructs for Halstead Metrics analysis
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_SIZE 100

// Function to calculate factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Function to check if a number is prime
int is_prime(int num) {
    if (num < 2) {
        return 0;
    }
    
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            return 0;
        }
    }
    return 1;
}

// Function to perform arithmetic operations
double calculate(double a, double b, char op) {
    switch (op) {
        case '+':
            return a + b;
        case '-':
            return a - b;
        case '*':
            return a * b;
        case '/':
            if (b != 0) {
                return a / b;
            } else {
                printf("Error: Division by zero!\n");
                return 0;
            }
        case '^':
            return pow(a, b);
        default:
            printf("Error: Invalid operator!\n");
            return 0;
    }
}

// Main function
int main() {
    int choice, num1, num2, result;
    double d1, d2, dresult;
    char operator;
    
    printf("=== Calculator Program ===\n");
    printf("1. Factorial\n");
    printf("2. Prime Check\n");
    printf("3. Arithmetic Operations\n");
    printf("Enter your choice: ");
    scanf("%d", &choice);
    
    switch (choice) {
        case 1:
            printf("Enter a number: ");
            scanf("%d", &num1);
            if (num1 < 0) {
                printf("Error: Factorial of negative number is undefined.\n");
            } else {
                result = factorial(num1);
                printf("Factorial of %d is %d\n", num1, result);
            }
            break;
            
        case 2:
            printf("Enter a number: ");
            scanf("%d", &num1);
            if (is_prime(num1)) {
                printf("%d is a prime number.\n", num1);
            } else {
                printf("%d is not a prime number.\n", num1);
            }
            break;
            
        case 3:
            printf("Enter first number: ");
            scanf("%lf", &d1);
            printf("Enter operator (+, -, *, /, ^): ");
            scanf(" %c", &operator);
            printf("Enter second number: ");
            scanf("%lf", &d2);
            
            dresult = calculate(d1, d2, operator);
            printf("Result: %.2f %c %.2f = %.2f\n", d1, operator, d2, dresult);
            break;
            
        default:
            printf("Invalid choice!\n");
    }
    
    return 0;
}


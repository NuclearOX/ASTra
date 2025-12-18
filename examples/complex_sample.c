#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define MAX_SIZE 50
#define THRESHOLD 10.5

// Definizione di una struttura dati complessa
typedef struct {
    int id;
    double values[MAX_SIZE];
    double average;
    double variance;
} DataSet;

// Funzione per calcolare la media
double calculate_mean(double arr[], int n) {
    double sum = 0.0;
    int i;
    for (i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum / n;
}

// Funzione per calcolare la varianza
double calculate_variance(double arr[], int n, double mean) {
    double sum_sq_diff = 0.0;
    int j;
    for (j = 0; j < n; j++) {
        double diff = arr[j] - mean;
        sum_sq_diff += pow(diff, 2);
    }
    return sum_sq_diff / (n - 1);
}

// Funzione principale di elaborazione
void process_data(DataSet *data, int count) {
    if (count <= 1) {
        printf("Errore: Dati insufficienti per l'analisi statistica.\n");
        return;
    }

    data->average = calculate_mean(data->values, count);
    data->variance = calculate_variance(data->values, count, data->average);

    printf("Analisi ID: %d\n", data->id);
    printf("Media Calcolata: %.4f\n", data->average);
    printf("Varianza: %.4f\n", data->variance);

    // Selezione basata sulla soglia
    if (data->variance > THRESHOLD) {
        printf("Stato: Alta variabilita' rilevata.\n");
    } else {
        printf("Stato: Variabilita' nella norma.\n");
    }
}

int main() {
    // Inizializzazione dati
    DataSet myData;
    myData.id = 101;
    int sample_count = 5;
    
    // Assegnazione manuale per generare operandi
    myData.values[0] = 12.5;
    myData.values[1] = 15.2;
    myData.values[2] = 9.8;
    myData.values[3] = 11.0;
    myData.values[4] = 14.5;

    // Elaborazione
    process_data(&myData, sample_count);

    // Ciclo fittizio per aumentare la complessità degli operatori
    int k = 0;
    while(k < 3) {
        switch(k) {
            case 0:
                printf("Step di inizializzazione completato.\n");
                break;
            case 1:
                printf("Verifica integrita' memoria...\n");
                break;
            default:
                printf("Processo terminato con successo.\n");
        }
        k++;
    }

    return 0;
}
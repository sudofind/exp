/*
    MPI realization of calculating sum over multiple vectors.

    Each process (except of #0) initialized its own vector, sums its elements
    and send resulting local sum to process #0, which calculates sum over all
    received sums.
    Also, this program measures the time of calculations.
*/


#include <stdio.h>
#include "mpi.h"

int main(int argc, char **argv) {

    int rank, size;
    int N_local = 1024;
    double local_sum;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (!rank) {
        double start = MPI_Wtime();
        double global_sum = 0;
        for (int i = 1; i < size; i++) {
            MPI_Recv(&local_sum, 1, MPI_DOUBLE, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, &status);
            global_sum += local_sum;
        }
        printf("I am %d process, global sum equals %f\nTime passed: %f\n",
               rank, global_sum, MPI_Wtime() - start);

    } else {
        local_sum = 0;
        double a[N_local];

        // Array initialization
        for (int i = 0; i < N_local; i++) a[i] = N_local * rank + i;

        // Calculate local sum
        for (int i = 0; i < N_local; i++) local_sum += a[i];

        // Send local sum to process #0
        MPI_Send(&local_sum, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}

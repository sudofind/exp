/*
    MPI realization of summing over the circle.

    Suppose, that each process #i can only do one operation ---
    to sum its number to variable. This program propagates values
    through the circle of processes and each circle node adds its
    number to this variable. Then, each node prints resulting sum.

    This program is hard to write with using MPI_Send and MPI_Recv
    functions only. It is caused by the fact, that deadlock may appear.
    So, this program uses the MPI_Isend and MPI_Irecv functions.
*/


#include <stdio.h>
#include "mpi.h"


int main(int argc, char **argv) {

    int rank, size;
    int receive_value;
    int current_sum;
    MPI_Status status;
    MPI_Request request;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    current_sum = 0;
    for (int i = 0; i < size; i++) {

        MPI_Isend(&current_sum, 1, MPI_INT, (rank + 1) % size, 1337, MPI_COMM_WORLD, &request);
        MPI_Irecv(&receive_value, 1, MPI_INT, (size + rank - 1) % size, 1337, MPI_COMM_WORLD, &request);
        MPI_Wait(&request, &status);

        current_sum = receive_value + rank;
    }


    for (int j = 0; j < size; j++) {
        // int tmp = j;
        // int tmp2 = j+1;
        // MPI_Bcast(&tmp, 1, MPI_INT, 0, MPI_COMM_WORLD); // does not synchronize processes
        // MPI_Reduce(&tmp, &tmp2, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD); // does not synchronize processes
        printf("  %d  ", j);
        // int k = MPI_Barrier(MPI_COMM_WORLD); // does not synchronize processes
        // printf("k is %d     ", k); // Error code is 0 for all the processes
        if (j == rank)
            printf("I am %d, my sum is %d\n", rank, current_sum);
    }

    MPI_Finalize();
    return 0;
}

/*
    MPI realization of sending and receiving messages across processes.

    In the following code, process #0 sends integer variable to process #1.
    Both of then print information about sending/receiving.
*/


#include <stdio.h>
#include "mpi.h"

int main(int argc, char **argv) {

    int rank, size, x = 5;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (!rank) {
        x = 7;
        MPI_Send(&x, 1, MPI_INT, 1, 1337, MPI_COMM_WORLD);
        printf("I am %d, sent %d to %d\n", rank, x, 1);
    } else if (rank == 1) {
        MPI_Recv(&x, 1, MPI_INT, 0, 1337, MPI_COMM_WORLD, &status);
        printf("I am %d, received %d from %d\n", rank, x, 0);
    }
    MPI_Finalize();

    return 0;
}

/*
    MPI realization of sending messages across many processes.

    Each process #i with even number sends message to the process #(i+1).
    All of the processes print information about sending/receiving.
    Also, this program handles incorrect running --- if you try to run it
    with odd number of processes, the program aborts.
*/


#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv) {

    int rank, size, x = -5;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size % 2) {
        printf("Got %d processes! Number of processes must be even!\n", size);
        // fflush(stdout);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    if (rank % 2) {
        MPI_Recv(&x, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        printf("I am %d, received %d from %d\n", rank, x, status.MPI_SOURCE);
    } else {
        x = 10 * rank;
        MPI_Send(&x, 1, MPI_INT, rank + 1, rank + 1, MPI_COMM_WORLD);
        printf("I am %d, sent %d to %d\n", rank, x, rank + 1);
    }

    MPI_Finalize();
    return 0;
}

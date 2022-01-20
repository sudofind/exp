/*
    MPI realization of sending messages across many processes.

    Process #0 sends messages to all the other processes.
    All of the processes from #1 to #(N-1) print information about receiving.
*/


#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
    int rank, size, x = 3;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (!rank) {
        x = 11;
        for (int i = 1; i < size; i++) {
            MPI_Send(&x, 1, MPI_INT, i, i+1337, MPI_COMM_WORLD);
            x += 1;
        }
    } else {
        MPI_Recv(&x, 1, MPI_INT, 0, rank+1337, MPI_COMM_WORLD, &status);
        printf("I am %d, received %d from 0\n", rank, x);
    }

    MPI_Finalize();
    return 0;
}

/*
    MPI realization of broadcast sending and ordering the output of the program.

    In this program I will use the ability of MPI to make broadcast sending
    (with the use of MPI_Bcast function). Process #0 sends the same data to
    all the other processes. Processes from #1 to #(N-1) receive this data
    and print it synchronically (with the use of MPI_Barrier function).
    Also, processes will print their numbers in ordered way.

    But MPI_Barrier does not work as it is supposed to :(
*/


#include <stdio.h>
#include "mpi.h"

int main(int argc, char **argv) {

    int rank, size;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int broadcasted_value;

    for (int i = 0; i < 5; i++) {
        MPI_Barrier(MPI_COMM_WORLD);
        broadcasted_value = rank + i;
        MPI_Bcast(&broadcasted_value, 1, MPI_INT, 0, MPI_COMM_WORLD);
        for (int j = 0; j < size; j++) {
            MPI_Barrier(MPI_COMM_WORLD);
            if (rank == j)
                printf("I am %d, got the value %d\n", rank, broadcasted_value, j);
        }
    }

    MPI_Finalize();
    return 0;
}

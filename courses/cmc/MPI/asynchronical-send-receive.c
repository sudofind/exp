/*
    MPI realization of program with asynchronical MPI functions.

    In this program 2 processes will send to each other some information,
    and then receive it from each other. In case of using basic MPI_Send
    and MPI_Recv functions the deadlock occurs. But I will use MPI_Isend
    and MPI_Irecv. Also I will need a MPI_Wait function.
*/


#include <stdio.h>
#include "mpi.h"


int main(int argc, char **argv) {

    int rank, size;
    MPI_Status status;
    MPI_Request request;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != 2) {
        printf("Please set number of processes to 2. Thank you!\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int shared_value = rank;

    MPI_Isend(&shared_value, 1, MPI_INT, !rank, 1337, MPI_COMM_WORLD, &request);
    MPI_Irecv(&shared_value, 1, MPI_INT, !rank, 1337, MPI_COMM_WORLD, &request);
    MPI_Wait(&request, &status);

    printf("I am %d, I got value %d\n", rank, shared_value);

    MPI_Finalize();
    return 0;
}

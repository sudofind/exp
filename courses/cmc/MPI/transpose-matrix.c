/*
    MPI realization of matrix transposing.

    Each process #i stores i-th row of matrix. I need to
    transpose this matrix so that process #i stores i-th column
    of matrix. I will use MPI_Alltoall.

    Then I will calculate resulting matrix columns sum. I will use
    MPI_Allreduce. Then each process must print out sum of each column.

*/


#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {

    int rank, size;

    // Getting command line arguments

    /*
    char input_key[] = "-i";

    int input_idx = 0;
    for (int i = 0; i < argc; i++) {
        printf("%s\n", argv[i]);
        if (!strcmp(argv[i], input_key)) {
            input_idx = i;
            break;
        }
    }

    int input_data = atoi(argv[input_idx + 1]);
    printf("Input data is %d\n", input_data);
    */

    int input_data = 0;
    // MPI initialization
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Memory allocation
    int data[1000];
    int received_data[1000];

    // Data initialization
    for (int i = 0; i < size; i++)
        data[i] = (rank + 1) * 100 + (input_data * 10) + (i + 1);

    printf("I am %d my values are: ", rank);
    for (int i = 0; i < size; i++)
        printf(" %d ", data[i]);
    printf("\n");

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Alltoall(data,          1, MPI_INT,
                 received_data, 1, MPI_INT,
                 MPI_COMM_WORLD);

    printf("I am %d my values are: ", rank);
    for (int i = 0; i < size; i++)
        printf(" %d ", received_data[i]);
    printf("\n");


    MPI_Finalize();
    return 0;

}

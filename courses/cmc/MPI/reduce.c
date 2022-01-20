/*
    MPI realization of data reduction.

    Consider each process to compute some vectors. Then we need to reduce
    all this data (calculate the element-wise sum) to one root process and
    print it out.
*/


#include <stdio.h>
#include "mpi.h"


int main(int argc, char **argv) {

    int rank, size;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int N_data = 100;
    int somehow_computed_data[N_data];
    int reduced_data[N_data];
    for (int i = 0; i < N_data; i++)
        somehow_computed_data[i] = (1337 * i * rank + 42) % 1000;


    MPI_Reduce(somehow_computed_data, reduced_data, N_data, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (!rank) {
        for (int i = 0; i < 10; i++) {
            printf("%d ", reduced_data[i]);
        }
        printf("\n");
    }

    MPI_Finalize();
    return 0;
}

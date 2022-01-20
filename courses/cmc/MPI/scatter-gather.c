/*
    MPI realization of partical vector normalization.

    This program tends to get experience in using MPI_Scatter and
    MPI_Gather functions. The task is the following:
      1. Send parts of vector to every process
      2. Normalize each part separately within each process
      3. Collect all processed data to root process and print it out.
*/


#include <stdio.h>
#include "mpi.h"


int main(int argc, char **argv) {

    int rank, size;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int N_input = 10;

    if (N_input % size) {
        printf("Please use number of processes, multiple of %d", N_input);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int send_buf[N_input];
    int receive_buf[N_input];

    // Random initialization of send_buf for process #0
    if (!rank) {
        for (int i = 0; i < N_input; i++)
            send_buf[i] = (1337 * i + 42) % 1000;
    }

    if (!rank) {
        for (int i = 0; i < N_input; i++)
            printf("%d ", send_buf[i]);
        printf("\n");
    }

    // Scattering

    MPI_Scatter(send_buf, N_input / size, MPI_INT,
                receive_buf, N_input / size, MPI_INT,
                0, MPI_COMM_WORLD);

    // Integer normalization
    int local_sum = 0;
    for (int i = 0; i < N_input / size; i++)
        local_sum += receive_buf[i];
    int local_mean = local_sum / (N_input / size);

    for (int i = 0; i < N_input / size; i++)
        receive_buf[i] -= local_mean;

    // Gathering
    MPI_Gather(receive_buf, N_input / size, MPI_INT,
               send_buf, N_input / size, MPI_INT,
               0, MPI_COMM_WORLD);

    if (!rank) {
        for (int i = 0; i < N_input; i++)
            printf("%d ", send_buf[i]);
        printf("\n");
    }

    MPI_Finalize();
    return 0;

}

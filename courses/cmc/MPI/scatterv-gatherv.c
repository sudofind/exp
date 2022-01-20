/*
    MPI realization of partical vector normalization.

    This program tends to get experience in using MPI_Scatterv and
    MPI_Gatherv functions. The task is the following:
      1. Send parts of vector to every process
      2. Normalize each part separately within each process
      3. Collect all processed data to root process and print it out.

    Difference with scatter-gather.c is that at this program
    there is no assumption that processes number must be a multiple
    of vector size.
*/


#include <stdio.h>
#include <mpi.h>


int main(int argc, char **argv) {

    int rank, size;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size > 10) {
        printf("Maximum processes number is 10\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    // Data initialization
    int N_data = 10;
    int data[N_data];
    int recv_data[N_data];

    if (!rank) {
        for (int i = 0; i < N_data; i++) {
            data[i] = (1337 * i + 42 ) % 1000;
        }

        printf("Initial values are:    ");
        for (int i = 0; i < N_data; i ++)
            printf(" %d ", data[i]);
        printf("\n");
    }

    // MPI_Scatterv input parameters initialization
    int send_sizes[N_data];
    int displs[N_data];

    int part_size = N_data / size;
    int n_remains = N_data % size;
    int k = 0;
    for (int i = 0; i < size; i++) {
        if (i < n_remains) {
            send_sizes[i] = part_size + 1;
        } else {
            send_sizes[i] = part_size;
        }
        displs[i] = k;
        k += send_sizes[i];
    }

    MPI_Scatterv(data, send_sizes, displs, MPI_INT,
                 recv_data, send_sizes[rank], MPI_INT,
                 0, MPI_COMM_WORLD);


    // Data processing
    int mean = 0;
    for (int i = 0; i < send_sizes[rank]; i++)
        mean += recv_data[i];
    mean /= send_sizes[rank];

    for (int i = 0; i < send_sizes[rank]; i++)
        recv_data[i] -= mean;

    // MPI_Gatherv usage

    MPI_Gatherv(recv_data, send_sizes[rank], MPI_INT,
                data, send_sizes, displs, MPI_INT,
                0, MPI_COMM_WORLD);

    // Result output
    if (!rank) {
        printf("Normalized values are: ");
        for (int i = 0; i < N_data; i ++)
            printf(" %d ", data[i]);
        printf("\n");
    }



    MPI_Finalize();
    return 0;
}

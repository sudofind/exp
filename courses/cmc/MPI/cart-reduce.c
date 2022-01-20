/*
    MPI realization of reduction through a cart.

    Cart dimensions calculates from processes number.
    Each process stores its coordinates in terms of cart space.
    Then each row reduces its data. The reduction values are stored
    in each process of a row (MPI_Allreduce). Then each columns reduces
    its data. The reduction values are also stored in each process
    of a column.
*/


#include <stdio.h>
#include <mpi.h>


int main(int argc, char **argv) {

    int rank, size;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Create cart
    int n_dims = 2;
    int periods[] = {0, 0};
    int reorder = 0;
    MPI_Comm cart_comm;
    int dims[] = {0, 0};

    MPI_Dims_create(size, n_dims, dims);


    MPI_Cart_create(MPI_COMM_WORLD, n_dims, dims, periods, reorder, &cart_comm);

    // Initialize processes vectors
    int cart_coords[2];
    MPI_Cart_coords(cart_comm, rank, n_dims, cart_coords);

    int data[] = { 10 * cart_coords[0], 10 * cart_coords[1] };
    int reduced_data[n_dims];

    //printf("I am %d (%d, %d), data equals (%d, %d)\n",
    //       rank, cart_coords[0], cart_coords[1], data[0], data[1]);

    MPI_Barrier(cart_comm);

    // Perform reducing
    for (int i = 0; i < dims[1]; i++) {
        if (cart_coords[1] == i) {
            // Create subcart
            int remain_dims[] = {0, 1};
            MPI_Comm subcart_comm;
            MPI_Cart_sub(cart_comm, remain_dims, &subcart_comm);

            // Reduce over subcart
            MPI_Allreduce(data, reduced_data, 2, MPI_INT, MPI_SUM, subcart_comm);
        }
    }

    printf("I am %d (%d, %d), reduced data equals (%d, %d)\n",
           rank, cart_coords[0], cart_coords[1], reduced_data[0], reduced_data[1]);

    MPI_Finalize();
    return 0;
}

/*
    MPI realization of calculating PI value through integral.

    Each process from #1 to #(N-1) calculate integral on particular
    interval. After that they send their local sums to process #0,
    which sums them and calculates value of the integral
    on the full interval [0, 1].
*/

#include <stdio.h>
#include <mpi.h>


void calculate_pi_without_MPI(long num_steps) {
    /*
        Calculating PI without using MPI.

        This function is needed to validate MPI realization.
    */
    double step, pi;
    double x, sum = 0.;

    step = 1.0 / (double) num_steps;
    for (long i = 0; i < num_steps; i++) {
        x = (i + 0.5) * step;
        sum = sum + 4. / (1. + x * x);
    }
    pi = step * sum;
    printf("PI without MPI: %.10f\n", pi);
}


void calculate_pi_with_MPI(long num_steps, int *argc, char ***argv) {
    /*
        Calculating PI with using MPI.
    */

    double step, pi, x;
    double global_sum, local_sum;
    int rank, size;
    MPI_Status status;

    step = 1.0 / (double) num_steps;

    MPI_Init(argc, argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size <= 1) {
        printf("Too few number of processes: %d. The program needs at least 2 processes!\n", size);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    if (!rank) {
        global_sum = 0;
        for (int i = 1; i < size; i++) {
            MPI_Recv(&local_sum, 1, MPI_DOUBLE, MPI_ANY_SOURCE, 1337, MPI_COMM_WORLD, &status);
            global_sum += local_sum;
        }
        pi = step * global_sum;
        printf("PI with MPI:    %.10f\n", pi);
        calculate_pi_without_MPI(num_steps);
    } else {
        local_sum = 0;
        for (long i = rank - 1; i < num_steps; i += size - 1) {
            x = (i + 0.5) * step;
            local_sum += 4. / (1. + x * x);
        }
        MPI_Send(&local_sum, 1, MPI_DOUBLE, 0, 1337, MPI_COMM_WORLD);
    }

    MPI_Finalize();
}


int main(int argc, char **argv) {
    long num_steps = 100000;
    calculate_pi_with_MPI(num_steps, &argc, &argv);
}

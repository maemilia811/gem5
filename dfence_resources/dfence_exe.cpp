#include <dirent.h>
#include <m5_mmap.h>
#include <sys/wait.h>
#include <unistd.h>

#include <cstring>
#include <iostream>
#include <string>
#include <vector>

#include <gem5/m5ops.h>

int main() {

    // Use the m5op_addr to input the "magic" address
    m5op_addr = 0XFFFF0000;

    // Use the map_m5_mem to map the "magic" address range to /dev/mem
    map_m5_mem();

    printf("Terminó de mapearse la memoria\n");
    // Use the gem5 m5ops to annotate the start of the ROI
    m5_work_begin_addr(0, 0);
    //ROI
    printf("Begin ROI\n");

    int result = system("/home/gem5/dfence_bin");

    if (result != 0) {
        printf("Error al ejecutar dfence_bin. Codigo: %d\n", result);
    }

    //end ROI
    // Use the gem5 m5ops to annotate the end of the ROI
    m5_work_end_addr(0, 0);
    printf(" End ROI\n");


    // struct dirent *d;
    // DIR *dr;
    // dr = opendir(".");
    // if (dr!=NULL) {
    //     std::cout<<"List of Files & Folders:\n";
    //     for (d=readdir(dr); d!=NULL; d=readdir(dr)) {
    //         std::cout<<d->d_name<< ", ";
    //     }
    //     closedir(dr);
    // }
    // else {
    //     std::cout<<"\nError Occurred!";
    // }
    // std::cout<<std::endl;

    // Use unmap_m5_mem to unmap the "magic" address range
    unmap_m5_mem();
    printf("Terminó de mapeo de memoria \n");

    // Terminar simulación
    m5_exit(0);
    printf("Despues del exit\n");
    return 0;
}

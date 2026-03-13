#include "../dfence_sec.h"

int main(void){

    uint32_t m5op_addr = 0XFFFF0000;

    map_m5_mem();

    printf("Finished memory mapping\n");

    m5_work_begin_addr(0, 0);

    printf("Begin ROI\n");
    #ifdef MFENCEV1
        int result = system("/home/gem5/spectrev1_mfence");
    #elif LFENCEV1
        int result = system("/home/gem5/spectrev1_lfence");
    #elif DFENCEV1
        int result = system("/home/gem5/spectrev1_dfence");
    #elif LFENCEV4
        int result = system("/home/gem5/spectrev4_lfence");
    #elif DFENCEV4
        int result = system("/home/gem5/spectrev4_dfence");
    #elif V1
        int result = system("/home/gem5/spectrev1");
    #elif V4
        int result = system("/home/gem5/spectrev4");
    #elif BENCHMARK
        int result = system("/home/gem5/benchmark");
    #elif BENCHMARK_dfence
        int result = system("/home/gem5/benchmark_dfence");
    #elif BENCHMARK_lfence
        int result = system("/home/gem5/benchmark_lfence");
    #endif

    m5_work_end_addr(0, 0);

    printf(" End ROI\n");

    return 0;
}

#include "../dfence_sec.h"

extern "C" {
    #include <gem5/m5ops.h> // Or whatever your specific m5 include path is
}

int main(void){
    // 1. You no longer need map_m5_mem() or m5op_addr for RISC-V

    printf("Begin ROI\n");

    // 2. Use the standard pseudo-instruction call
    m5_work_begin(0, 0);

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
    #elif RISCV_SPECV1
        int result = system("/home/gem5/spectrev1_riscv_wp");
    #endif

    // 3. Use standard work_end
    m5_work_end(0, 0);

    printf(" End ROI\n");

    return 0;
}

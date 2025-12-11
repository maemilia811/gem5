#include "../dfence_exe.h"

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
    #elif MFENCEV4
        int result = system("/home/gem5/spectrev4_mfence");
    #elif LFENCEV4
        int result = system("/home/gem5/spectrev4_lfence");
    #elif DFENCEV4
        int result = system("/home/gem5/spectrev4_dfence");
    #elif V1
        int result = system("/home/gem5/spectrev1");
    #elif V4
        int result = system("/home/gem5/spectrev4");
    #elif MFENCEV1_v2
        int result = system("/home/gem5/spectrev1_mfence_v2");
    #elif LFENCEV1_v2
        int result = system("/home/gem5/spectrev1_lfence_v2");
    #elif DFENCEV1_v2
        int result = system("/home/gem5/spectrev1_dfence_v2");
    #elif MFENCEV4_v2
        int result = system("/home/gem5/spectrev4_mfence_v2");
    #elif LFENCEV4_v2
        int result = system("/home/gem5/spectrev4_lfence_v2");
    #elif DFENCEV4_v2
        int result = system("/home/gem5/spectrev4_dfence_v2");
    #elif V1_v2
        int result = system("/home/gem5/spectrev1_v2");
    #elif V4_v2
        int result = system("/home/gem5/spectrev4_v2");
    #endif

    m5_work_end_addr(0, 0);

    printf(" End ROI\n");

    return 0;
}

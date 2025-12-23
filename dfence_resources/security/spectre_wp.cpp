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
    #elif LFENCEV4
        int result = system("/home/gem5/spectrev4_lfence");
    #elif DFENCEV4
        int result = system("/home/gem5/spectrev4_dfence");
    #elif V1
        int result = system("/home/gem5/spectrev1");
    #elif V4
        int result = system("/home/gem5/spectrev4");
    #elif LFENCEV1_ext
        int result = system("/home/gem5/spectrev1_lfence_ext");
    #elif DFENCEV1_ext
        int result = system("/home/gem5/spectrev1_dfence_ext");
    #elif LFENCEV4_ext
        int result = system("/home/gem5/spectrev4_lfence_ext");
    #elif DFENCEV4_ext
        int result = system("/home/gem5/spectrev4_dfence_ext");
    #elif V1_ext
        int result = system("/home/gem5/spectrev1_ext");
    #elif V4_ext
        int result = system("/home/gem5/spectrev4_ext");
    #endif

    m5_work_end_addr(0, 0);

    printf(" End ROI\n");

    return 0;
}

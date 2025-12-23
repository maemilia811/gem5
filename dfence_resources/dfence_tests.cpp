#include "dfence_exe.h"

int main(void){

    uint32_t m5op_addr = 0XFFFF0000;

    map_m5_mem();

    printf("Finished memory mapping\n");

    m5_work_begin_addr(0, 0);

    printf("Begin ROI\nExecuting tests with dfence..\n");
    // int result = system("/home/gem5/df_add");
    // result = system("/home/gem5/df_st");
    // result = system("/home/gem5/df_st2");
    // result = system("/home/gem5/df_st3");
    // result = system("/home/gem5/df_ld");
    // result = system("/home/gem5/df_ld2");
    // result = system("/home/gem5/df_test");
    // result = system("/home/gem5/df_test2");
    int result = system("/home/gem5/df_ssb");

    if (result != 0) {
        printf("dfence_bin: Error, code: %d\n", result);
        return result;
    }

    m5_work_end_addr(0, 0);

    printf(" End ROI\n");

    return 0;
}

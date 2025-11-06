#include "dfence_exe.h"

int main(void){

    uint32_t m5op_addr = 0XFFFF0000;

    map_m5_mem();

    printf("Finished memory mapping\n");

    m5_work_begin_addr(0, 0);

    printf("Begin ROI\n");

    int result = system("/home/gem5/dfence_bin");

    if (result != 0) {
        printf("dfence_bin: Error, code: %d\n", result);
        return result;
    }

    m5_work_end_addr(0, 0);

    printf(" End ROI\n");

    return 0;
}

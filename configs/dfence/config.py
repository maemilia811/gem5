import gem5.components.processors.simple_switchable_processor as Proc
import gem5.simulate.simulator as Sim
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import (
    DiskImageResource,
    obtain_resource,
)


def workbegin_handler():
    print("Done booting Linux!")

    # Cambiar de KVM a O3 antes de ejecutar el ROI
    print("Switching from KVM to O3 CPU...")
    processor.switch()

    # Ejecutar el binario dentro del guest (O3 CPU)
    print("Running dfence_bin in guest...")

    # La simulación terminará automáticamente si tu binario llama m5_exit()
    yield False


def exit_event_handler():

    print("Third exit: Finished `after_boot.sh` script")
    # The after_boot.sh script will run a script if it is passed via
    # m5 readfile. This is the last exit event before the simulation exits.
    yield True


cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16KiB",
    l1d_assoc=8,
    l1i_size="16KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)
memory = SingleChannelDDR4_2400(size="3GiB")
processor = Proc.SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=CPUTypes.O3,
    num_cores=1,
    isa=ISA.X86,
)

for proc in processor.start:
    proc.core.usePerf = False

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

kernel = obtain_resource(
    "x86-linux-kernel-6.8.0-52-generic",
    resource_version="1.0.0",
    clients=["gem5-resources"],
)

disk = obtain_resource(
    "test-disk-dfence",
    resource_version="4.0.0",
    clients=["GEM5_RESOURCE_JSON_APPEND"],
)

board.set_kernel_disk_workload(
    kernel=kernel,
    kernel_args=[
        "earlyprintk=ttyS0",
        "console=ttyS0",
        "lpj=7999923",
        "root=/dev/sda2",
    ],
    disk_image=disk,
    readfile_contents="""#!/bin/bash
                        /home/gem5/dfence
                        exit 0
                        """,
)


sim = Sim.Simulator(
    board=board,
    full_system=True,
    on_exit_event={
        Sim.ExitEvent.WORKBEGIN: workbegin_handler(),
        Sim.ExitEvent.EXIT: exit_event_handler(),
    },
)
sim.run()

import gem5.components.processors.simple_processor as ProcSimple
import gem5.components.processors.simple_switchable_processor as Proc
import gem5.simulate.simulator as Sim
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import (
    obtain_resource,
)

# ---------- Define the system ----------
cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="16KiB",
    l1i_size="16KiB",
    l2_size="256KiB",
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


# ---------- Resources ---------

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
        "iomem=relaxed",
        # "mitigations=off",
        # "nospectre_v1",
        # "hardened_usercopy=off",
    ],
    disk_image=disk,
    readfile_contents="""#!/bin/bash
    /home/gem5/spectrev1_dfence_wp
    exit 0
    """,
)

# ---------- Define Event Handlers---------


def exit_event_handler():
    yield False


def workbegin_handler():
    processor.switch()
    yield False


def workend_handler():
    yield False


# ---------- Run simulator ----------

sim = Sim.Simulator(
    board=board,
    full_system=True,
    on_exit_event={
        Sim.ExitEvent.EXIT: exit_event_handler(),
        Sim.ExitEvent.WORKBEGIN: workbegin_handler(),
        Sim.ExitEvent.WORKEND: workend_handler(),
    },
)

sim.show_exit_event_messages()

sim.run()

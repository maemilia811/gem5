# multisim_x86_two_readfiles.py

import gem5.components.processors.simple_switchable_processor as Proc
import gem5.simulate.simulator as Sim
import gem5.utils.multisim as multisim
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource

# --- tell MultiSim how many parallel worker processes to use ---
multisim.set_num_processes(4)

# ---------- Resources (shared) ----------
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

# ---------- Readfile variants ----------
readfile_variants = [
    """#!/bin/bash
/home/gem5/spectrev1_lfence_wp
exit 0
""",
    """#!/bin/bash
/home/gem5/spectrev1_dfence_wp
exit 0
""",
    """#!/bin/bash
/home/gem5/spectrev1_mfence_wp
exit 0
""",
    """#!/bin/bash
/home/gem5/spectrev1_wp
exit 0
""",
]


# ---------- Event handler factories ----------
def make_exit_event_handler():
    yield False


def make_workbegin_handler(sim):
    sim.switch_processor()
    yield False


def make_workend_handler():
    yield False


# ---------- Build one simulator per readfile variant ----------
for i, readfile_contents in enumerate(readfile_variants):

    cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
        l1d_size="16KiB",
        l1i_size="16KiB",
        l2_size="256KiB",
    )

    memory = SingleChannelDDR4_2400(size="3GiB")

    processor = Proc.SimpleSwitchableProcessor(
        starting_core_type=CPUTypes.O3,
        switch_core_type=CPUTypes.O3,
        num_cores=1,
        isa=ISA.X86,
    )

    board = X86Board(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

    board.set_kernel_disk_workload(
        kernel=kernel,
        kernel_args=[
            "earlyprintk=ttyS0",
            "console=ttyS0",
            "lpj=7999923",
            "root=/dev/sda2",
            "iomem=relaxed",
        ],
        disk_image=disk,
        readfile_contents=readfile_contents,
    )

    # --- Simulator ---
    sim = Sim.Simulator(
        board=board,
        full_system=True,
        id=f"sim_readfile_variant_{i}",
    )

    sim.on_exit_event = {
        Sim.ExitEvent.EXIT: make_exit_event_handler(),
        Sim.ExitEvent.WORKBEGIN: make_workbegin_handler(sim),
        Sim.ExitEvent.WORKEND: make_workend_handler(),
    }

    multisim.add_simulator(sim)

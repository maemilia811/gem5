import argparse
from pathlib import Path

from O3_RISCV import *

from m5.objects import *

import gem5.simulate.simulator as Sim
from gem5.components.boards.riscv_board import RiscvBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource

parser = argparse.ArgumentParser(
    description="Run a gem5 RISC-V simulation with a custom binary."
)
parser.add_init_argument = parser.add_argument(
    "binary_path", type=str, help="Path to the RISC-V binary to execute"
)
args = parser.parse_args()

cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="32KiB",
    l1i_size="32KiB",
    l2_size="512KiB",
)

memory = SingleChannelDDR4_2400(size="3GiB")

custom_cpu_instance = O3_RISCV_CPU()

wrapped_core = BaseCPUCore(core=custom_cpu_instance, isa=ISA.RISCV)
processor = BaseCPUProcessor(cores=[wrapped_core])

for simple_core in processor.cores:
    for i in range(len(simple_core.core.isa)):
        simple_core.core.isa[i].riscv_type = "RV32"
        simple_core.core.isa[i].enable_rvv = False


board = RiscvBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(BinaryResource(local_path=args.binary_path))

sim = Sim.Simulator(board=board)
sim.run()

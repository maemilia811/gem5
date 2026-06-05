import argparse
from pathlib import Path

from O3_X86 import *

from m5.objects import *

import gem5.simulate.simulator as Sim
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
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

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB",
    l1i_size="32KiB",
    l2_size="512KiB",
)

memory = SingleChannelDDR4_2400(size="3GiB")

custom_cpu_instance = O3_x86_CPU()
wrapped_core = BaseCPUCore(core=custom_cpu_instance, isa=ISA.X86)
processor = BaseCPUProcessor(cores=[wrapped_core])

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(BinaryResource(local_path=args.binary_path))

sim = Sim.Simulator(board=board)
sim.run()

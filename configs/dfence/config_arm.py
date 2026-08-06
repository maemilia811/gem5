import argparse
from pathlib import Path

import gem5.components.processors.simple_processor as ProcSimple
import gem5.components.processors.simple_processor as Proc
import gem5.simulate.simulator as Sim
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import (
    BinaryResource,
    obtain_resource,
)

parser = argparse.ArgumentParser(
    description="Run a gem5 RISC-V simulation with a custom binary."
)
parser.add_init_argument = parser.add_argument(
    "binary_path", type=str, help="Path to the ARM binary to execute"
)
args = parser.parse_args()


# ---------- Define the system ----------
cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="16KiB",
    l1i_size="16KiB",
    l2_size="256KiB",
)

memory = SingleChannelDDR4_2400(size="3GiB")

processor = Proc.SimpleProcessor(
    cpu_type=CPUTypes.O3,
    num_cores=1,
    isa=ISA.ARM,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)


board.set_se_binary_workload(
    binary=BinaryResource(local_path=args.binary_path)
)

sim = Sim.Simulator(
    board=board,
)

sim.show_exit_event_messages()

sim.run()

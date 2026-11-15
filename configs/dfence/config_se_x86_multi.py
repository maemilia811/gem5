from pathlib import Path

from O3_X86 import *

from m5.objects import *

import gem5.utils.multisim as multisim
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

BENCH_ROOT = Path("../benchmarks")
BENCH = "spectrev4"

# variant name -> binary path. The variant name is also the simulator id,
# so each run's output lands in <outdir>/<variant>/.
VARIANTS = {
    "baseline": BENCH_ROOT / "baseline/x86" / BENCH / "bin/spectrev4_x86",
    "naive_dfence": BENCH_ROOT
    / "naive/x86"
    / BENCH
    / "bin/spectrev4_x86_dfence",
    "naive_lfence": BENCH_ROOT
    / "naive/x86"
    / BENCH
    / "bin/spectrev4_x86_fence",
    "smart_dfence": BENCH_ROOT
    / "smart/x86"
    / BENCH
    / "bin/spectrev4_x86_dfence",
}


def build_simulator(variant: str, binary_path: Path) -> Simulator:
    cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size="32KiB",
        l1i_size="32KiB",
        l2_size="512KiB",
    )
    memory = SingleChannelDDR4_2400(size="3GiB")

    cpu = O3_x86_CPU()
    core = BaseCPUCore(core=cpu, isa=ISA.X86)
    processor = BaseCPUProcessor(cores=[core])

    board = X86Board(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )
    board.set_se_binary_workload(BinaryResource(local_path=str(binary_path)))

    return Simulator(board=board, id=variant)


for variant, path in VARIANTS.items():
    if not path.exists():
        print(f"[multisim] skipping {variant}: {path} not found")
        continue
    multisim.add_simulator(build_simulator(variant, path))

# Optional: limit concurrency
multisim.set_num_processes(4)

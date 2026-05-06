# Copyright (c) 2012 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.objects import *


# Simple ALU Instructions have a latency of 1
class Simple_Int(FUDesc):
    opList = [OpDesc(opClass="IntAlu", opLat=1)]
    count = 2


# Complex ALU instructions have a variable latencies
class Complex_Int(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu", opLat=1),
        OpDesc(opClass="IntMult", opLat=2, pipelined=True),
        OpDesc(opClass="IntDiv", opLat=12, pipelined=False),
        OpDesc(opClass="IprAccess", opLat=3, pipelined=True),
    ]
    count = 2


class FP_ASIMD_0(FUDesc):
    # ASIMD ALU
    opList = [
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=3),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=4),
        # ASIMD MISCV
        OpDesc(opClass="SimdMisc", opLat=2),
        # ASIMD INTEGER MULTIPLY
        OpDesc(opClass="SimdMult", opLat=4),
        OpDesc(opClass="SimdMultAcc", opLat=4),
        OpDesc(opClass="SimdMatMultAcc", opLat=4),
        # FP CONVERT
        OpDesc(opClass="SimdFloatCvt", opLat=4),
        OpDesc(opClass="FloatCvt", opLat=2),
        # FP MISC
        OpDesc(opClass="SimdFloatMisc", opLat=4),
        OpDesc(opClass="FloatMisc", opLat=3),
        # FP ADD
        OpDesc(opClass="FloatAdd", opLat=2),
        # FP MULTIPLY
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="SimdFloatMatMultAcc", opLat=5),
        # FP DIVIDE
        OpDesc(opClass="FloatDiv", opLat=9, pipelined=False),
        OpDesc(opClass="SimdFloatDiv", opLat=8),
        # FP SQRT
        OpDesc(opClass="SimdSqrt", opLat=9),
        OpDesc(opClass="FloatSqrt", opLat=9, pipelined=False),
        OpDesc(opClass="SimdFloatAlu", opLat=5),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="FloatCmp", opLat=3),
        # CRYPTO MOPS
        # VECTOR STORE DATA
    ]
    count = 1


class FP_ASIMD_1(FUDesc):
    opList = [
        # ASIMD ALU
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=3),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=4),
        # ASIMD MISCV
        OpDesc(opClass="SimdMisc", opLat=2),
        # FP MISC
        OpDesc(opClass="SimdFloatMisc", opLat=4),
        OpDesc(opClass="FloatMisc", opLat=3),
        # FP ADD
        OpDesc(opClass="FloatAdd", opLat=2),
        # FP MULTIPLY
        OpDesc(opClass="FloatMult", opLat=3),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="SimdFloatMatMultAcc", opLat=5),
        # ASIMD SHIFT
        OpDesc(opClass="SimdShift", opLat=3),
        OpDesc(opClass="SimdShiftAcc", opLat=3),
        OpDesc(opClass="SimdFloatAlu", opLat=5),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="FloatCmp", opLat=3),
        # CRYPTO MOPS
        # VECTOR STORE DATA
    ]
    count = 1


class Load_Store(FUDesc):
    opList = [
        OpDesc(opClass="MemRead", opLat=4),
        OpDesc(opClass="FloatMemRead", opLat=5),
        OpDesc(opClass="MemWrite", opLat=2),
    ]
    count = 2


# Load/Store Units
class Load(FUDesc):
    opList = [
        OpDesc(opClass="MemRead", opLat=4),
        OpDesc(opClass="FloatMemRead", opLat=5),
    ]
    count = 1


class Int_Store(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite", opLat=2),
    ]
    count = 2


# Functional Units for this CPU
class O3_ARM_v8a_FUP(FUPool):
    FUList = [
        Simple_Int(),
        Complex_Int(),
        FP_ASIMD_0(),
        FP_ASIMD_1(),
        Load_Store(),
        Load(),
        Int_Store(),
    ]


class O3_ARM_8a_BTB(SimpleBTB):
    numEntries = 2048
    tagBits = 18
    associativity = 1
    instShiftAmt = 2
    btbReplPolicy = LRURP()
    btbIndexingPolicy = BTBSetAssociative(
        num_entries=Parent.numEntries,
        set_shift=Parent.instShiftAmt,
        assoc=Parent.associativity,
        tag_bits=Parent.tagBits,
    )


# Bi-Mode Branch Predictor
class O3_ARM_8a_BP(BiModeBP):
    btb = O3_ARM_8a_BTB()
    ras = ReturnAddrStack(numEntries=16)
    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    instShiftAmt = 2


class O3_ARM_8a_3(ArmO3CPU):
    LQEntries = 16
    SQEntries = 16
    LSQDepCheckShift = 0
    LFSTSize = 1024
    SSITSize = "1024"
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 3
    fetchBufferSize = 16
    fetchToDecodeDelay = 3
    decodeWidth = 3
    decodeToRenameDelay = 2
    renameWidth = 3
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 6
    issueWidth = 8
    wbWidth = 8
    fuPool = O3_ARM_v8a_FUP()
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 8
    squashWidth = 8
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5
    numPhysIntRegs = 128
    numPhysFloatRegs = 192
    numPhysVecRegs = 48
    numIQEntries = 32
    numROBEntries = 160  # out of order window size

    switched_out = False
    branchPred = O3_ARM_8a_BP()


# Instruction Cache
class L1_ICache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 2
    tgts_per_mshr = 8
    size = "32KiB"
    assoc = 4
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True


# Data Cache
class L1_DCache(Cache):
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 6
    tgts_per_mshr = 8
    size = "32KiB"
    assoc = 4
    write_buffers = 16
    # Consider the L2 a victim cache also for clean lines
    writeback_clean = True


# L2 Cache
class O3_ARM_8aL2(Cache):
    tag_latency = 12
    data_latency = 12
    response_latency = 12
    mshrs = 16
    tgts_per_mshr = 8
    size = "512KiB"
    assoc = 8
    write_buffers = 8
    clusivity = "mostly_excl"
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=8, latency=1, prefetch_on_access=True)
    tags = BaseSetAssoc()
    replacement_policy = RandomRP()

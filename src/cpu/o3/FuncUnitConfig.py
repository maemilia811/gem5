# Copyright (c) 2010, 2017, 2020, 2024 Arm Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Copyright (c) 2006-2007 The Regents of The University of Michigan
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

from m5.defines import buildEnv
from m5.objects.FuncUnit import *
from m5.params import *
from m5.SimObject import SimObject


class IntALU(FUDesc):
    opList = [OpDesc(opClass="IntAlu")]
    count = 6


class IntMultDiv(FUDesc):
    opList = [
        OpDesc(opClass="IntMult", opLat=3),
        OpDesc(opClass="IntDiv", opLat=20, pipelined=False),
    ]

    count = 2


class FP_ALU(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=2),
        OpDesc(opClass="FloatCmp", opLat=2),
        OpDesc(opClass="FloatCvt", opLat=2),
    ]
    count = 4


class FP_MultDiv(FUDesc):
    opList = [
        OpDesc(opClass="FloatMult", opLat=4),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),
        OpDesc(opClass="FloatDiv", opLat=12, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=24, pipelined=False),
    ]
    count = 2


class SIMD_Unit(FUDesc):
    opList = [
        OpDesc(opClass="SimdAdd"),
        OpDesc(opClass="SimdAddAcc"),
        OpDesc(opClass="SimdAlu"),
        OpDesc(opClass="SimdCmp"),
        OpDesc(opClass="SimdCvt"),
        OpDesc(opClass="SimdMisc"),
        OpDesc(opClass="SimdMult"),
        OpDesc(opClass="SimdMultAcc"),
        OpDesc(opClass="SimdMatMultAcc"),
        OpDesc(opClass="SimdShift"),
        OpDesc(opClass="SimdShiftAcc"),
        OpDesc(opClass="SimdDiv"),
        OpDesc(opClass="SimdSqrt"),
        OpDesc(opClass="SimdFloatAdd"),
        OpDesc(opClass="SimdFloatAlu"),
        OpDesc(opClass="SimdFloatCmp"),
        OpDesc(opClass="SimdFloatCvt"),
        OpDesc(opClass="SimdFloatDiv"),
        OpDesc(opClass="SimdFloatMisc"),
        OpDesc(opClass="SimdFloatMult"),
        OpDesc(opClass="SimdFloatMultAcc"),
        OpDesc(opClass="SimdFloatMatMultAcc"),
        OpDesc(opClass="SimdFloatSqrt"),
        OpDesc(opClass="SimdReduceAdd"),
        OpDesc(opClass="SimdReduceAlu"),
        OpDesc(opClass="SimdReduceCmp"),
        OpDesc(opClass="SimdFloatReduceAdd"),
        OpDesc(opClass="SimdFloatReduceCmp"),
        OpDesc(opClass="SimdExt"),
        OpDesc(opClass="SimdFloatExt"),
        OpDesc(opClass="SimdConfig"),
        OpDesc(opClass="SimdAes"),
        OpDesc(opClass="SimdAesMix"),
        OpDesc(opClass="SimdSha1Hash"),
        OpDesc(opClass="SimdSha1Hash2"),
        OpDesc(opClass="SimdSha256Hash"),
        OpDesc(opClass="SimdSha256Hash2"),
        OpDesc(opClass="SimdShaSigma2"),
        OpDesc(opClass="SimdShaSigma3"),
    ]
    count = 4


class Matrix_Unit(FUDesc):
    opList = [
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
    ]
    count = 1


class PredALU(FUDesc):
    opList = [OpDesc(opClass="SimdPredAlu")]
    count = 1


class ReadPort(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="SimdUnitStrideLoad"),
        OpDesc(opClass="SimdUnitStrideMaskLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad"),
        OpDesc(opClass="SimdStridedLoad"),
        OpDesc(opClass="SimdIndexedLoad"),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdWholeRegisterLoad"),
        OpDesc(opClass="SimdStrideSegmentedLoad"),
    ]
    count = 0


class WritePort(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="SimdUnitStrideStore"),
        OpDesc(opClass="SimdUnitStrideMaskStore"),
        OpDesc(opClass="SimdUnitStrideSegmentedStore"),
        OpDesc(opClass="SimdStridedStore"),
        OpDesc(opClass="SimdIndexedStore"),
        OpDesc(opClass="SimdWholeRegisterStore"),
        OpDesc(opClass="SimdStrideSegmentedStore"),
    ]
    count = 0


class RdWrPort(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="SimdUnitStrideLoad"),
        OpDesc(opClass="SimdUnitStrideStore"),
        OpDesc(opClass="SimdUnitStrideMaskLoad"),
        OpDesc(opClass="SimdUnitStrideMaskStore"),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedStore"),
        OpDesc(opClass="SimdStridedLoad"),
        OpDesc(opClass="SimdStridedStore"),
        OpDesc(opClass="SimdIndexedLoad"),
        OpDesc(opClass="SimdIndexedStore"),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdWholeRegisterLoad"),
        OpDesc(opClass="SimdWholeRegisterStore"),
        OpDesc(opClass="SimdStrideSegmentedLoad"),
        OpDesc(opClass="SimdStrideSegmentedStore"),
    ]
    count = 4


class IprPort(FUDesc):
    opList = [OpDesc(opClass="IprAccess", opLat=3, pipelined=False)]
    count = 1


""""
Version icelake adaptada de https://github.com/darchr/gem5-skylake-config/blob/master/gem5-configs/system/core.py
"""

from m5.objects import *


class port0(FUDesc):
    # Port 0: ALU, LEA, Shift, JMP, FMA, Vector ALU/Shift, Vector Div/Sqrt, AES
    opList = [
        # Int ALU, LEA, Int shift, jump1
        OpDesc(opClass="IntAlu", opLat=1),
        # VEC ALU
        OpDesc(opClass="FloatAdd", opLat=4),
        OpDesc(opClass="FloatCmp", opLat=4),
        OpDesc(opClass="FloatCvt", opLat=4),
        OpDesc(opClass="FloatMult", opLat=4),
        OpDesc(opClass="FloatMultAcc", opLat=4),
        # VEC ALU, Shift, FMA
        OpDesc(opClass="SimdAdd", opLat=1),
        OpDesc(opClass="SimdAlu", opLat=1),
        OpDesc(opClass="SimdCmp", opLat=1),
        OpDesc(opClass="SimdShift", opLat=1),
        OpDesc(opClass="SimdFloatAdd", opLat=4),
        OpDesc(opClass="SimdFloatAlu", opLat=4),
        OpDesc(opClass="SimdFloatCmp", opLat=4),
        OpDesc(opClass="SimdFloatMisc", opLat=4),
        OpDesc(opClass="SimdFloatDiv", opLat=14, pipelined=False),
        OpDesc(opClass="SimdFloatSqrt", opLat=14, pipelined=False),
        # FP div
        OpDesc(opClass="FloatDiv", opLat=14, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=14, pipelined=False),
        # Cryptography
        OpDesc(opClass="SimdAes", opLat=3),
        OpDesc(opClass="SimdAesMix", opLat=3),
        # System & Config (Required by gem5)
        OpDesc(opClass="IprAccess", opLat=3, pipelined=False),
        OpDesc(opClass="SimdConfig", opLat=1),
    ]
    count = 1


class port1(FUDesc):
    # Port 1: ALU, LEA, MUL, IDIV, FMA, Vector ALU/Shift/Mul, Shuffle
    opList = [
        OpDesc(opClass="IntAlu", opLat=1),
        OpDesc(opClass="IntMult", opLat=3),
        OpDesc(opClass="IntDiv", opLat=15, pipelined=False),
        OpDesc(opClass="FloatAdd", opLat=4),
        OpDesc(opClass="FloatMult", opLat=4),
        OpDesc(opClass="FloatMultAcc", opLat=4),
        OpDesc(opClass="FloatMisc", opLat=4),
        OpDesc(opClass="SimdMult", opLat=4),
        OpDesc(opClass="SimdMultAcc", opLat=4),
        OpDesc(opClass="SimdFloatMult", opLat=4),
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        OpDesc(opClass="SimdShift", opLat=1),
        OpDesc(opClass="SimdMisc", opLat=1),  # Shuffles
        OpDesc(opClass="SimdCvt", opLat=4),
    ]
    count = 1


class port5(FUDesc):
    # Port 5: ALU, LEA, MULHi, Vector ALU, Shuffle, SHA, Matrix
    opList = [
        # Int ALU, LEA
        OpDesc(opClass="IntAlu", opLat=1),
        OpDesc(opClass="IntMult", opLat=3),
        # VEC ALU
        OpDesc(opClass="FloatAdd", opLat=4),
        OpDesc(opClass="FloatCmp", opLat=4),
        OpDesc(opClass="FloatCvt", opLat=4),
        OpDesc(opClass="FloatMult", opLat=4),
        OpDesc(opClass="FloatMultAcc", opLat=4),
        OpDesc(opClass="SimdAdd", opLat=1),
        OpDesc(opClass="SimdAlu", opLat=1),
        OpDesc(opClass="SimdCmp", opLat=1),
        OpDesc(opClass="SimdMisc", opLat=1),
        OpDesc(opClass="SimdExt", opLat=1),
        OpDesc(opClass="SimdFloatExt", opLat=1),
        OpDesc(opClass="SimdReduceAdd", opLat=1),
        OpDesc(opClass="SimdReduceAlu", opLat=1),
        OpDesc(opClass="SimdReduceCmp", opLat=1),
        # Cryptography (Icelake executes SHA on Port 5)
        OpDesc(opClass="SimdSha1Hash", opLat=3),
        OpDesc(opClass="SimdSha1Hash2", opLat=3),
        OpDesc(opClass="SimdSha256Hash", opLat=3),
        OpDesc(opClass="SimdSha256Hash2", opLat=3),
        OpDesc(opClass="SimdShaSigma2", opLat=3),
        OpDesc(opClass="SimdShaSigma3", opLat=3),
        # Matrix operations
        OpDesc(opClass="Matrix", opLat=4),
        OpDesc(opClass="MatrixMov", opLat=1),
        OpDesc(opClass="MatrixOP", opLat=4),
    ]
    count = 1


class port6(FUDesc):
    # Port 6: ALU, LEA, Shift, JMP, Predication
    opList = [
        OpDesc(opClass="IntAlu", opLat=1),
        OpDesc(opClass="SimdPredAlu", opLat=1),
    ]
    count = 1


class port2_3(FUDesc):
    # Ports 2 & 3: Dedicated Load Units
    opList = [
        OpDesc(opClass="MemRead", opLat=1),
        OpDesc(opClass="FloatMemRead", opLat=1),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=1),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=1),
        OpDesc(opClass="SimdStridedLoad", opLat=1),
        OpDesc(opClass="SimdIndexedLoad", opLat=1),
    ]
    count = 2


class port4_9(FUDesc):
    # Ports 4 & 9: Dedicated Store Data Units
    opList = [
        OpDesc(opClass="MemWrite", opLat=1),
        OpDesc(opClass="FloatMemWrite", opLat=1),
        OpDesc(opClass="SimdUnitStrideStore", opLat=1),
        OpDesc(opClass="SimdWholeRegisterStore", opLat=1),
        OpDesc(opClass="SimdStridedStore", opLat=1),
        OpDesc(opClass="SimdIndexedStore", opLat=1),
    ]
    count = 2


class port7_8(FUDesc):
    # Ports 7 & 8: Store Address Generation (STA)
    opList = [OpDesc(opClass="MemWrite", opLat=1)]
    count = 2

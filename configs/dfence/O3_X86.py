""" "
Version icelake adaptada de https://github.com/darchr/gem5-skylake-config/blob/master/gem5-configs/system/core.py
"""

from m5.defines import buildEnv
from m5.objects import *
from m5.objects.FuncUnit import *
from m5.params import *
from m5.SimObject import SimObject


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


class IcelakeFUPool(FUPool):
    FUList = [
        port0(),
        port1(),
        port5(),
        port6(),
        port2_3(),
        port4_9(),
        port7_8(),
    ]


class O3_x86_CPU(X86O3CPU):
    numPhysIntRegs = 280
    numROBEntries = 352
    fetchBufferSize = Param.Unsigned(16, "Fetch buffer size in bytes")
    fuPool = IcelakeFUPool()

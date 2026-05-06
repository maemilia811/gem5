from m5.objects import *


# ALU
class ALU(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu", opLat=1),
        OpDesc(opClass="IprAccess", opLat=3, pipelined=True),
    ]
    count = 8


# MUL/DIV
class MUL_DIV(FUDesc):
    opList = [
        OpDesc(opClass="IntMult", opLat=2, pipelined=True),
        OpDesc(opClass="IntDiv", opLat=12, pipelined=False),
    ]
    count = 2


# LOAD
class LOAD(FUDesc):
    opList = [
        OpDesc(opClass="MemRead", opLat=4),
        OpDesc(opClass="FloatMemRead", opLat=5),
    ]
    count = 3


# extras
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


class Int_Store(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite", opLat=2),
    ]
    count = 1


class O3_RISCV_FUP(FUPool):
    FUList = [
        ALU(),
        MUL_DIV(),
        LOAD(),
        Int_Store(),
        FP_ASIMD_0(),
        FP_ASIMD_1(),
    ]


class O3_RISCV_CPU(RiscvO3CPU):
    numROBEntries = 32
    fuPool = O3_RISCV_FUP()

GEM5_PATH = /home/maria/Documentos/FAMAF/Tesis/tesis
ISA = x86
GXX = g++
all: spectrev1 spectrev1_dfence spectrev1_lfence spectrev1_mfence \
	spectrev4 spectrev4_dfence spectrev4_lfence spectrev4_mfence \
	spectrev1_v2 spectrev1_dfence_v2 spectrev1_lfence_v2 spectrev1_mfence_v2 \
	spectrev4_v2 spectrev4_dfence_v2 spectrev4_lfence_v2 spectrev4_mfence_v2 \
	spectrev1_v3 spectrev1_dfence_v3 spectrev1_lfence_v3 spectrev1_mfence_v3 \
	spectrev4_v3 spectrev4_dfence_v3 spectrev4_lfence_v3 spectrev4_mfence_v3 \
	dfence_tests

spectrev1: spectre_wp.cpp
	$(GXX) -DV1 -o spectrev1_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_dfence: spectre_wp.cpp
	$(GXX) -DDFENCEV1 -o spectrev1_dfence_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_lfence: spectre_wp.cpp
	$(GXX) -DLFENCEV1 -o spectrev1_lfence_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_mfence: spectre_wp.cpp
	$(GXX) -DMFENCEV1 -o  spectrev1_mfence_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4: spectre_wp.cpp
	$(GXX) -DV4 -o spectrev4_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_dfence: spectre_wp.cpp
	$(GXX) -DDFENCEV4 -o spectrev4_dfence_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_lfence: spectre_wp.cpp
	$(GXX) -DLFENCEV4  -o spectrev4_lfence_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_mfence: spectre_wp.cpp
	$(GXX) -DLFENCEV4  -o spectrev4_mfence_wp spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_v2: spectre_wp.cpp
	$(GXX) -DV1_v2 -o spectrev1_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_dfence_v2: spectre_wp.cpp
	$(GXX) -DDFENCEV1_v2 -o spectrev1_dfence_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_lfence_v2: spectre_wp.cpp
	$(GXX) -DLFENCEV1_v2 -o spectrev1_lfence_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_mfence_v2: spectre_wp.cpp
	$(GXX) -DMFENCEV1_v2 -o  spectrev1_mfence_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_v2: spectre_wp.cpp
	$(GXX) -DV4_v2 -o spectrev4_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_dfence_v2: spectre_wp.cpp
	$(GXX) -DDFENCEV4_v2 -o spectrev4_dfence_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_lfence_v2: spectre_wp.cpp
	$(GXX) -DLFENCEV4_v2  -o spectrev4_lfence_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_mfence_v2: spectre_wp.cpp
	$(GXX) -DLFENCEV4_v2  -o spectrev4_mfence_wp_v2 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_v3: spectre_wp.cpp
	$(GXX) -DV1_v3 -o spectrev1_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_dfence_v3: spectre_wp.cpp
	$(GXX) -DDFENCEV1_v3 -o spectrev1_dfence_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_lfence_v3: spectre_wp.cpp
	$(GXX) -DLFENCEV1_v3 -o spectrev1_lfence_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev1_mfence_v3: spectre_wp.cpp
	$(GXX) -DMFENCEV1_v3 -o  spectrev1_mfence_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_v3: spectre_wp.cpp
	$(GXX) -DV4_v3 -o spectrev4_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_dfence_v3: spectre_wp.cpp
	$(GXX) -DDFENCEV4_v3 -o spectrev4_dfence_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_lfence_v3: spectre_wp.cpp
	$(GXX) -DLFENCEV4_v3  -o spectrev4_lfence_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

spectrev4_mfence_v3: spectre_wp.cpp
	$(GXX) -DLFENCEV4_v3  -o spectrev4_mfence_wp_v3 spectre_wp.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

dfence_tests: dfence_tests.cpp
	$(GXX) -o df_tests dfence_tests.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

clean:
	rm -f bin/spectrev1_wp bin/spectrev1_dfence_wp bin/spectrev1_lfence_wp bin/spectrev1_mfence_wp bin/spectrev4_wp bin/spectrev4_dfence_wp bin/spectrev4_lfence_wp bin/spectrev4_mfence_wp bin/df_tests

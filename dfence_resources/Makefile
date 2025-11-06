GEM5_PATH = /home/maria/Documentos/FAMAF/Tesis/tesis
ISA = x86
GXX = g++

all: dfence

dfence: dfence_exe.cpp
	$(GXX) -o dfence dfence_exe.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

test: test
	$(GXX) -o test test.cpp -no-pie -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

clean:
	rm -f dfence

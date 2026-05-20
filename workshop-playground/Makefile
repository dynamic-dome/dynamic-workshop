# Workshop Playground - OSDP Frame Decoder (C)

CC      := gcc
CFLAGS  := -Wall -Wextra -O0 -g
LDFLAGS :=

TARGET  := osdp_frame_decoder
SRCS    := osdp_frame_decoder.c

.PHONY: all clean static-check scan-build cortex-m

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

# Static analysis with clang (uses default checker)
static-check:
	clang --analyze $(SRCS) -Xclang -analyzer-output=text

# Optional: scan-build for deeper analysis
scan-build:
	scan-build -o ./scan-results $(CC) $(CFLAGS) -o $(TARGET) $(SRCS)

clean:
	rm -f $(TARGET) $(TARGET).exe
	rm -rf scan-results

# Cross-compile for ARM Cortex-M (illustration only - requires arm-none-eabi-gcc)
cortex-m:
	@command -v arm-none-eabi-gcc >/dev/null 2>&1 || { echo "arm-none-eabi-gcc not installed - skip cross-compile"; exit 0; }
	arm-none-eabi-gcc $(CFLAGS) -mcpu=cortex-m4 -mthumb -o $(TARGET).elf $(SRCS)

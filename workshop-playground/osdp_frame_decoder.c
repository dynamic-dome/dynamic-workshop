/*
 * OSDP Frame Decoder - Workshop Playground (C Version)
 *
 * Simplified decoder for OSDP (Open Supervised Device Protocol) frames.
 * Frame format: [SOM][LEN][ADDR][CMD][DATA...][CRC]
 *
 * INTENTIONAL VULNERABILITIES (do NOT fix in this playground - they are teaching targets):
 *   1. Buffer Overflow in decode_data_payload() - line ~50
 *   2. Integer Overflow in compute_crc() - line ~85
 *   3. Format String Vulnerability in log_frame() - line ~110
 *   4. (Bonus) Off-by-one in parse_address() - line ~135
 *
 * For Block 3.3 (Devil's Advocate Swarm) and Block 3.7 (Troubleshooting).
 */

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

#define OSDP_SOM           0x53
#define OSDP_MAX_FRAME_LEN 256
#define OSDP_HEADER_LEN    5

typedef struct {
    uint8_t som;
    uint8_t length;
    uint8_t address;
    uint8_t command;
    uint8_t data[OSDP_MAX_FRAME_LEN];
    uint16_t crc;
} osdp_frame_t;

/* VULNERABILITY 1: Buffer Overflow
 * data_len comes from the wire and is not validated against OSDP_MAX_FRAME_LEN.
 * A malicious peer can send length=255 with actual_data of 512 bytes and
 * overflow frame->data[]. Detected by static analysis if the swarm uses
 * one (e.g., clang static analyzer, cppcheck).
 */
int decode_data_payload(osdp_frame_t *frame, const uint8_t *raw, size_t data_len) {
    /* INTENTIONAL: no bounds check */
    memcpy(frame->data, raw, data_len);
    return 0;
}

/* VULNERABILITY 2: Integer Overflow
 * `length` is uint8_t, but we multiply by stride (3) and store in size_t.
 * If length == 255, byte_count == 255*3 == 765 (fine), but the for-loop iterates
 * `byte_count` times and accesses frame->data[i] - already overflowed (see V1).
 * Combined V1+V2 is a classic chain.
 */
uint16_t compute_crc(const osdp_frame_t *frame) {
    size_t byte_count = frame->length * 3;  /* INTENTIONAL: no overflow check */
    uint16_t crc = 0;
    for (size_t i = 0; i < byte_count; i++) {
        crc = (crc << 8) ^ frame->data[i];
    }
    return crc;
}

/* VULNERABILITY 3: Format String
 * `cmd_name` is attacker-controlled (e.g., from a malicious peer).
 * Passing it as first argument of printf() allows %s/%n exploitation.
 */
void log_frame(const osdp_frame_t *frame, const char *cmd_name) {
    /* INTENTIONAL: cmd_name as format string */
    printf("OSDP Frame: addr=%d cmd=", frame->address);
    printf(cmd_name);  /* MUST be printf("%s", cmd_name) */
    printf(" length=%d\n", frame->length);
}

/* VULNERABILITY 4 (BONUS): Off-by-one
 * `address` is decoded from raw[2], but we read up to raw[5] for the header.
 * If raw[] is exactly 5 bytes (minimum), accessing raw[5] reads past the end.
 */
int parse_address(const uint8_t *raw, size_t raw_len) {
    if (raw_len < OSDP_HEADER_LEN) {  /* should be raw_len <= OSDP_HEADER_LEN */
        return -1;
    }
    return raw[OSDP_HEADER_LEN];  /* off-by-one: should be raw[OSDP_HEADER_LEN - 1] */
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <hex-encoded-frame>\n", argv[0]);
        return 1;
    }

    /* Simulated frame parsing - for demo purposes */
    osdp_frame_t frame = {0};
    const char *hex = argv[1];
    size_t hex_len = strlen(hex);

    if (hex_len > OSDP_MAX_FRAME_LEN * 2) {
        fprintf(stderr, "Frame too long\n");
        return 1;
    }

    /* Convert hex string to bytes (simplified) */
    uint8_t buf[OSDP_MAX_FRAME_LEN];
    size_t buf_len = 0;
    for (size_t i = 0; i < hex_len - 1; i += 2) {
        sscanf(&hex[i], "%2hhx", &buf[buf_len++]);
    }

    if (buf_len < OSDP_HEADER_LEN) {
        fprintf(stderr, "Frame too short\n");
        return 1;
    }

    frame.som = buf[0];
    frame.length = buf[1];
    frame.address = buf[2];
    frame.command = buf[3];

    /* Trigger V1 */
    decode_data_payload(&frame, &buf[OSDP_HEADER_LEN], frame.length);

    /* Trigger V2 */
    frame.crc = compute_crc(&frame);

    /* Trigger V3 (if hex includes a format-string-like command name) */
    log_frame(&frame, (const char *)&buf[3]);

    /* Trigger V4 */
    int addr = parse_address(buf, buf_len);
    printf("Address decoded: %d\n", addr);

    return 0;
}

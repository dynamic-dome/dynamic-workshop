/*
 * OSDP Frame Decoder - Workshop Playground (C Version)
 *
 * Simplified TEACHING decoder for OSDP (Open Supervised Device Protocol) frames.
 *
 * NOTE ON FRAME FORMAT: A real OSDP frame (SIA OSDP v2.2 / IEC 60839-11-5) is
 *   [SOM=0x53][ADDR][LEN_LSB][LEN_MSB][CTRL][DATA...][CRC-16/CCITT]
 *   -- i.e. ADDR comes BEFORE a 16-bit little-endian LEN, and the trailer is a
 *   CRC-16/CCITT. The struct below uses a SIMPLIFIED single-byte layout for
 *   teaching only; it is intentionally NOT wire-accurate. Do not use as a
 *   reference implementation.
 *
 * INTENTIONAL VULNERABILITIES (do NOT fix in this playground - they are teaching targets;
 * referenced by function name so the targets survive future edits):
 *   1. Buffer Overflow   in decode_data_payload()
 *   2. Integer Overflow  in compute_crc()      (uint8_t arithmetic wraps around)
 *   3. Format String     in log_frame()
 *   4. (Bonus) Off-by-one in read_frame_crc()  (reads the CRC one byte past frame end)
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

/* Simplified teaching layout -- real OSDP puts ADDR before a 16-bit LEN (see header note). */
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
 * `byte_count` is computed in uint8_t. For length values above ~251 the
 * addition wraps around (e.g. 255 + 4 == 259, which is 3 in a uint8_t), so the
 * CRC loop runs over a far smaller range than the real frame. The CRC is then
 * computed over the wrong bounds -- a genuine integrity bug driven purely by the
 * wrap-around (real OSDP integrity uses CRC-16/CCITT over the full frame).
 */
uint16_t compute_crc(const osdp_frame_t *frame) {
    /* INTENTIONAL: uint8_t arithmetic wraps for large length (no widening) */
    uint8_t byte_count = (uint8_t)(frame->length + 4);  /* +4 for header+CRC bytes */
    uint16_t crc = 0;
    for (uint8_t i = 0; i < byte_count; i++) {
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

/* VULNERABILITY 4 (BONUS): Off-by-one at the frame tail
 * The CRC trailer sits at the END of an OSDP frame. For a frame of `frame_len`
 * bytes the valid indices are raw[0 .. frame_len-1], so the last (CRC) byte is
 * raw[frame_len - 1]. This reads raw[frame_len] -- one byte past the end, a
 * classic off-by-one when locating the CRC. The guard still lets frame_len equal
 * the buffer length through, so a minimum-size frame triggers the OOB read.
 */
int read_frame_crc(const uint8_t *raw, size_t frame_len) {
    if (frame_len < OSDP_HEADER_LEN) {
        return -1;
    }
    return raw[frame_len];  /* off-by-one: last valid byte is raw[frame_len - 1] */
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

    /* Validate hex input: must be non-empty and even-length.
     * Hardened against a size_t underflow on empty input (hex_len - 1 wrapping to
     * SIZE_MAX) and a silently dropped final nibble on odd input. This is an
     * unplanned robustness fix in main(), NOT one of the four teaching vulns. */
    if (hex_len == 0 || hex_len % 2 != 0) {
        fprintf(stderr, "Invalid hex length (must be non-empty and even)\n");
        return 1;
    }

    /* Convert hex string to bytes (simplified) */
    uint8_t buf[OSDP_MAX_FRAME_LEN];
    size_t buf_len = 0;
    for (size_t i = 0; i < hex_len; i += 2) {
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
    int crc_tail = read_frame_crc(buf, buf_len);
    printf("CRC tail byte: %d\n", crc_tail);

    return 0;
}

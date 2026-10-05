/*
 * OSDP Frame Decoder - Workshop Playground (C Version)
 *
 * Simplified TEACHING decoder for OSDP (Open Supervised Device Protocol) frames.
 *
 * NOTE ON FRAME FORMAT: A real OSDP frame (SIA OSDP v2.2 / IEC 60839-11-5) is
 *   [SOM=0x53][ADDR][LEN_LSB][LEN_MSB][CTRL][DATA...][CRC-16/CCITT]
 *   -- i.e. ADDR comes BEFORE a 16-bit little-endian LEN, and the trailer is a
 *   CRC-16/CCITT. The struct below uses a SIMPLIFIED single-byte layout for
 *   teaching only; it is NOT wire-accurate, on purpose. Do not use as a
 *   reference implementation.
 *
 * Practice material of the Claude Code Praxisbibliothek.
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

/* Copy the payload of a frame into the frame struct. */
int decode_data_payload(osdp_frame_t *frame, const uint8_t *raw, size_t data_len) {
    memcpy(frame->data, raw, data_len);
    return 0;
}

/* Checksum over the frame (simplified; real OSDP uses CRC-16/CCITT). */
uint16_t compute_crc(const osdp_frame_t *frame) {
    uint8_t byte_count = (uint8_t)(frame->length + 4);  /* +4 for header+CRC bytes */
    uint16_t crc = 0;
    for (uint8_t i = 0; i < byte_count; i++) {
        crc = (crc << 8) ^ frame->data[i];
    }
    return crc;
}

/* Print one line per frame; cmd_name is the command name sent by the peer. */
void log_frame(const osdp_frame_t *frame, const char *cmd_name) {
    printf("OSDP Frame: addr=%d cmd=", frame->address);
    printf(cmd_name);
    printf(" length=%d\n", frame->length);
}

/* Return the CRC byte from the tail of a frame of frame_len bytes. */
int read_frame_crc(const uint8_t *raw, size_t frame_len) {
    if (frame_len < OSDP_HEADER_LEN) {
        return -1;
    }
    return raw[frame_len];
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

    /* Validate hex input: must be non-empty and even-length (an empty string would make
     * hex_len - 1 wrap to SIZE_MAX, an odd one would silently drop its last nibble). */
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

    /* payload */
    decode_data_payload(&frame, &buf[OSDP_HEADER_LEN], frame.length);

    /* checksum */
    frame.crc = compute_crc(&frame);

    /* log line */
    log_frame(&frame, (const char *)&buf[3]);

    /* CRC byte at the tail */
    int crc_tail = read_frame_crc(buf, buf_len);
    printf("CRC tail byte: %d\n", crc_tail);

    return 0;
}

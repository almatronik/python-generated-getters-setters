#include "buffer.h"
#include <climits>

void buffer_insert(uint8_t *buf, uint8_t start, uint8_t length, uint32_t value)
{
    uint8_t pos = start % CHAR_BIT;
    uint8_t index = start / CHAR_BIT;

    for (uint8_t i = 0; i < length; i++)
    {
        uint8_t bit = (uint8_t)((value >> i) & 1U);

        if (bit == 0)
        {
            buf[index] &= ~(1U << pos);
        }
        else
        {
            buf[index] |= (1U << pos);
        }

        pos++;
        if (pos == CHAR_BIT)
        {
            pos = 0;
            index++;
        }
    }
}

uint32_t buffer_extract(uint8_t *buf, uint8_t start, uint8_t length)
{
    uint32_t value = 0;
    uint8_t pos = start % CHAR_BIT;
    uint8_t index = start / CHAR_BIT;

    for (uint8_t i = 0; i < length; i++)
    {
        uint8_t bit = (buf[index] >> pos) & 1U;

        if (bit == 1U)
        {
            value |= (((uint32_t)1) << i);
        }

        pos++;
        if (pos == CHAR_BIT)
        {
            pos = 0;
            index++;
        }
    }

    return value;
}
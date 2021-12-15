#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>


int random_byte()
{
    return random() >> 24;
}


int get_file_size(FILE *fp)
{
    int size;
    if (fp) {
        fseek(fp, 0L, SEEK_END);
        size = ftell(fp);
        rewind(fp);
    }
    return size;
}


int get_append_length(int num_iterations)
{
    int times_to_append = num_iterations / 500;
    int append_length = times_to_append * 10;
    return append_length;
}


char* allocate_buffer(int file_length, int append_length)
{
    int length = file_length + append_length;
    char *buffer = malloc((length + 1) * sizeof(char));
    memset(buffer + file_length, '\0', append_length);
    return buffer;
}


bool get_input(FILE *fp, char *buffer, int length)
{
    char *temp = malloc((length + 1) * sizeof(char));
    bool success = false;
    if (fp) {
        fread(temp, sizeof(char), length, fp);
        fclose(fp);
        strncpy(buffer, temp, length);
        success = true;
    }
    return success;
}


void generate_random_input(char *buffer, int offset, int length)
{
    for (int i = offset; i < offset + length; ++i) {
        buffer[i] = random_byte();
    }
}


int main(int argc, char *argv[])
{
    uint32_t prng_seed = atoi(argv[1]);
    uint32_t num_iterations = atoi(argv[2]);
    char *initial_seed = argv[3];

    // Set random seed.
    srandom(prng_seed);

    FILE *fp = NULL;
    int file_size, append_length;
    char *input;

    
    if (initial_seed == NULL) {
        if (access("seed", F_OK) == 0) {
            // Use default seed in current directory if not specified.
            fp = fopen("seed", "r");
            file_size = get_file_size(fp);
        } else {
            /* Initial file size is a function of the prng seed in case the 
             * specific length of the file matters.
             */ 
            file_size = (prng_seed % 10) + 1;
        }
    } else {
        // Initial file specified.
        fp = fopen(initial_seed, "r");
        file_size = get_file_size(fp);
    }

    // Allocate large enough array in memory.
    append_length = get_append_length(num_iterations);
    input = allocate_buffer(file_size, append_length);

    if (!get_input(fp, input, file_size)) {
        generate_random_input(input, 0, file_size);
    }

    for (int i = 0; i < num_iterations; ++i) {
        for (int j = 0; j < file_size; ++j) {
            // 13% chance of updating each byte.
            if (random() % 100 < 13) {
                input[j] = random_byte();
            }
        }

        // Add 10 random characters every 500 iterations.
        if (i > 0 && i % 500 == 0) {
            generate_random_input(input, file_size, 10);
            file_size += 10;
        }
    }
    
    printf("%s", input);
    
}

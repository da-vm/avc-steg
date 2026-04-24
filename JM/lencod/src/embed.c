#include "embed.h"

int embed( VideoParameters *p_Vid, short int mv ) {
    if( p_Vid->secret.finished )
        return mv;

    if( p_Vid->secret.secret_bits[p_Vid->secret.current_position] == '\0' ) {
        p_Vid->secret.finished = 1;
        return mv;
    }

    int secret_bit = p_Vid->secret.secret_bits[p_Vid->secret.current_position] - '0';
    p_Vid->secret.current_position++;
    mv = ( mv & ~1 ) | secret_bit;
    return mv;
}
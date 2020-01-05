#ifndef FIFTEEN_PUZZLE_SOLVER_UTILS_H
#define FIFTEEN_PUZZLE_SOLVER_UTILS_H


#include <string>

/**
 * Prints a message with a timestamp.
 * @param msg message
 */
void infoMessage(const std::string &msg);

/**
 * Gets the current timestamp.
 * @param milliseconds
 * @return
 */
std::string currentTimeStr(bool milliseconds=true);

#endif //FIFTEEN_PUZZLE_SOLVER_UTILS_H

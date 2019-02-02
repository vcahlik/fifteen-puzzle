#include <iostream>
#include <ctime>
#include <chrono>
#include <sys/time.h>
#include <iomanip>
#include "Utils.h"

void infoMessage(const std::string &msg) {
    timeval curTime;
    gettimeofday(&curTime, nullptr);
    int milli = static_cast<int>(curTime.tv_usec / 1000);
    char buffer[80];
    strftime(buffer, 80, "%Y-%m-%d %H:%M:%S", localtime(&curTime.tv_sec));

    std::cout << "[" << buffer << "." << std::setw(3) << std::setfill('0') << milli << "] " << msg << std::endl;
}
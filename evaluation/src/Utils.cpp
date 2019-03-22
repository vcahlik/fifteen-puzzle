#include "Utils.h"
#include <iostream>
#include <ctime>
#include <chrono>
#include <sys/time.h>
#include <iomanip>

void infoMessage(const std::string &msg) {
    std::cout << "[" << currentTimeStr() << "] " << msg << std::endl;
}

std::string currentTimeStr(bool milliseconds) {
    timeval curTime;
    gettimeofday(&curTime, nullptr);
    char buffer[80];
    strftime(buffer, 80, "%Y-%m-%dT%H:%M:%S", localtime(&curTime.tv_sec));
    std::ostringstream oss;

    if (milliseconds) {
        int milli = static_cast<int>(curTime.tv_usec / 1000);
        oss << buffer << "." << std::setw(3) << std::setfill('0') << milli;
    } else {
        oss << buffer;
    }
    return oss.str();
}

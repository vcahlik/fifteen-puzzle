add_subdirectory(Algorithms)
add_subdirectory(Heuristics)

set(SOURCES
        ${SOURCES}
        ${CMAKE_CURRENT_SOURCE_DIR}/Node.cpp
        PARENT_SCOPE
        )

set(HEADERS
        ${HEADERS}
        ${CMAKE_CURRENT_SOURCE_DIR}/Node.h
        PARENT_SCOPE
        )
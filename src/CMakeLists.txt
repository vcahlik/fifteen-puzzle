add_subdirectory(StateSpaceSearch)

set(SOURCES
        ${SOURCES}
        ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/Board.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/Utils.cpp
        PARENT_SCOPE
        )

set(HEADERS
        ${HEADERS}
        ${CMAKE_CURRENT_SOURCE_DIR}/Board.h
        ${CMAKE_CURRENT_SOURCE_DIR}/Utils.h
        PARENT_SCOPE
        )
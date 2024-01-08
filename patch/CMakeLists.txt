cmake_minimum_required(VERSION 3.16)

set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
set(CMAKE_FINAL_OUTPUT_DIRECTORY "C:/InnocentGrey/カルタグラ FHD")
 
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY $<1:${CMAKE_FINAL_OUTPUT_DIRECTORY}>) 
add_compile_options(
  /std:c++17
  /MP
  /wd4018 
  /wd4819 
  /wd4244
  /wd4267
  /DVERSION="${VERSION}"
  /DUNICODE 
  /D_UNICODE
)
project(patch)


add_subdirectory(lib/minhook)

add_library(lyric lyric/lyric.cpp lyric/OverlayLyric.cpp lyric/Wnd.cpp)

add_library(CHSpatch MODULE patch.cpp uitext.cpp tolongtexts.cpp othcg.cpp patch.rc)  

target_link_libraries(CHSpatch Gdiplus Shlwapi minhook lyric ${CMAKE_CURRENT_SOURCE_DIR}/lib/Detours-4.0.1/lib.X64/detours.lib)

 
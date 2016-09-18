include_directories(.)
include_directories(../POSIX)
include_directories(../Utility)

add_lldb_library(lldbPluginProcessCygwin
  ProcFileReader.cpp
  )

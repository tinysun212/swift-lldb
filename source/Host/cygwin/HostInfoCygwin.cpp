//===-- HostInfoCygwin.cpp -------------------------------------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#include "lldb/Host/cygwin/HostInfoCygwin.h"

#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <sys/types.h>
#include <sys/utsname.h>

using namespace lldb_private;

uint32_t HostInfoCygwin::GetMaxThreadNameLength() { return 16; }

bool HostInfoCygwin::GetOSVersion(uint32_t &major, uint32_t &minor,
                                   uint32_t &update) {
  struct utsname un;

  ::memset(&un, 0, sizeof(utsname));
  if (uname(&un) < 0)
    return false;

  int status = sscanf(un.release, "%u.%u", &major, &minor);
  return status == 2;
}

bool HostInfoCygwin::GetOSBuildString(std::string &s) {
  struct utsname un;
  ::memset(&un, 0, sizeof(utsname));
  s.clear();

  if (uname(&un) < 0)
    return false;

  s.assign(un.release);
  return true;
}

bool HostInfoCygwin::GetOSKernelDescription(std::string &s) {
  struct utsname un;

  ::memset(&un, 0, sizeof(utsname));
  s.clear();

  if (uname(&un) < 0)
    return false;

  s.assign(un.version);

  return true;
}

FileSpec HostInfoCygwin::GetProgramFileSpec() {
  static FileSpec g_program_filespec;

  if (!g_program_filespec) {
    char exe_path[PATH_MAX];
    ssize_t len = readlink("/proc/self/exe", exe_path, sizeof(exe_path) - 1);
    if (len > 0) {
      exe_path[len] = 0;
      g_program_filespec.SetFile(exe_path, false);
    }
  }

  return g_program_filespec;
}

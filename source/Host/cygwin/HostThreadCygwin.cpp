//===-- HostThreadCygwin.cpp -----------------------------------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

// lldb Includes
#include "lldb/Host/cygwin/HostThreadCygwin.h"
#include "lldb/Host/Host.h"

// C includes
#include <errno.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>

// C++ includes
#include <string>

using namespace lldb_private;

HostThreadCygwin::HostThreadCygwin() {}

HostThreadCygwin::HostThreadCygwin(lldb::thread_t thread)
    : HostThreadPosix(thread) {}

void HostThreadCygwin::SetName(lldb::thread_t thread, llvm::StringRef &name) {
  ::pthread_setname_np(thread, name.data());  
}

void HostThreadCygwin::GetName(lldb::thread_t thread,
                               llvm::SmallVectorImpl<char> &name) {
  char buf[256];
  ::pthread_getname_np(thread, buf, sizeof(buf));

  name.clear();
  name.append(buf, buf + strlen(buf));
}

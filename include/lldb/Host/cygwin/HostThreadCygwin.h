//===-- HostThreadCygwin.h --------------------------------------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#ifndef lldb_Host_cygwin_HostThreadCygwin_h_
#define lldb_Host_cygwin_HostThreadCygwin_h_

#include "lldb/Host/posix/HostThreadPosix.h"

#include "llvm/ADT/SmallString.h"
#include "llvm/ADT/StringRef.h"

namespace lldb_private {

class HostThreadCygwin : public HostThreadPosix {
public:
  HostThreadCygwin();
  HostThreadCygwin(lldb::thread_t thread);

  static void SetName(lldb::thread_t tid, llvm::StringRef &name);
  static void GetName(lldb::thread_t tid, llvm::SmallVectorImpl<char> &name);  
};
}

#endif

"""
Test lldb-mi can interpret CLI commands directly.
"""

from __future__ import print_function


import lldbmi_testcase
from lldbsuite.test.decorators import *
from lldbsuite.test.lldbtest import *
from lldbsuite.test import lldbutil


class MiCliSupportTestCase(lldbmi_testcase.MiTestCaseBase):

    mydir = TestBase.compute_mydir(__file__)

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    def test_lldbmi_target_create(self):
        """Test that 'lldb-mi --interpreter' can create target by 'target create' command."""

        self.spawnLldbMi(args=None)

        # Test that "target create" loads executable
        self.runCmd("target create \"%s\"" % self.myexe)
        self.expect("\^done")

        # Test that executable was loaded properly
        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\"")
        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    @skipIfLinux  # llvm.org/pr22841: lldb-mi tests fail on all Linux buildbots
    def test_lldbmi_breakpoint_set(self):
        """Test that 'lldb-mi --interpreter' can set breakpoint by 'breakpoint set' command."""

        self.spawnLldbMi(args=None)

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Test that "breakpoint set" sets a breakpoint
        self.runCmd("breakpoint set --name main")
        self.expect("\^done")
        self.expect("=breakpoint-created,bkpt={number=\"1\"")

        # Test that breakpoint was set properly
        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("=breakpoint-modified,bkpt={number=\"1\"")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    @skipIfLinux  # llvm.org/pr22841: lldb-mi tests fail on all Linux buildbots
    def test_lldbmi_settings_set_target_run_args_before(self):
        """Test that 'lldb-mi --interpreter' can set target arguments by 'setting set target.run-args' command before than target was created."""

        self.spawnLldbMi(args=None)

        # Test that "settings set target.run-args" passes arguments to executable
        # FIXME: --arg1 causes an error
        self.runCmd(
            "setting set target.run-args arg1 \"2nd arg\" third_arg fourth=\"4th arg\"")
        self.expect("\^done")

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Run
        self.runCmd("-exec-run")
        self.expect("\^running")

        # Test that arguments were passed properly
        self.expect("@\"argc=5\\\\r\\\\n\"")

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    @skipIfLinux  # llvm.org/pr22841: lldb-mi tests fail on all Linux buildbots
    def test_lldbmi_settings_set_target_run_args_after(self):
        """Test that 'lldb-mi --interpreter' can set target arguments by 'setting set target.run-args' command after than target was created."""

        self.spawnLldbMi(args=None)

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Test that "settings set target.run-args" passes arguments to executable
        # FIXME: --arg1 causes an error
        self.runCmd(
            "setting set target.run-args arg1 \"2nd arg\" third_arg fourth=\"4th arg\"")
        self.expect("\^done")

        # Run
        self.runCmd("-exec-run")
        self.expect("\^running")

        # Test that arguments were passed properly
        self.expect("@\"argc=5\\\\r\\\\n\"")

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    @skipIfLinux  # llvm.org/pr22841: lldb-mi tests fail on all Linux buildbots
    def test_lldbmi_process_launch(self):
        """Test that 'lldb-mi --interpreter' can launch process by "process launch" command."""

        self.spawnLldbMi(args=None)

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Set breakpoint
        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\"")

        # Test that "process launch" launches executable
        self.runCmd("process launch")
        self.expect("\^done")

        # Test that breakpoint hit
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    @skipIfLinux  # llvm.org/pr22841: lldb-mi tests fail on all Linux buildbots
    def test_lldbmi_thread_step_in(self):
        """Test that 'lldb-mi --interpreter' can step in by "thread step-in" command."""

        self.spawnLldbMi(args=None)

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Run to main
        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\"")
        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

        # Test that "thread step-in" steps into (or not) printf depending on debug info
        # Note that message is different in Darwin and Linux:
        # Darwin: "*stopped,reason=\"end-stepping-range\",frame={addr=\"0x[0-9a-f]+\",func=\"main\",args=[{name=\"argc\",value=\"1\"},{name=\"argv\",value="0x[0-9a-f]+\"}],file=\"main.cpp\",fullname=\".+main.cpp\",line=\"\d\"},thread-id=\"1\",stopped-threads=\"all\"
        # Linux:
        # "*stopped,reason=\"end-stepping-range\",frame={addr="0x[0-9a-f]+\",func=\"__printf\",args=[{name=\"format\",value=\"0x[0-9a-f]+\"}],file=\"printf.c\",fullname=\".+printf.c\",line="\d+"},thread-id=\"1\",stopped-threads=\"all\"
        self.runCmd("thread step-in")
        self.expect("\^done")
        it = self.expect(["@\"argc=1\\\\r\\\\n\"",
                          "\*stopped,reason=\"end-stepping-range\".+?func=\"(?!main).+?\""])
        if it == 0:
            self.expect(
                "\*stopped,reason=\"end-stepping-range\".+?func=\"main\"")

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    @skipIfLinux  # llvm.org/pr22841: lldb-mi tests fail on all Linux buildbots
    def test_lldbmi_thread_step_over(self):
        """Test that 'lldb-mi --interpreter' can step over by "thread step-over" command."""

        self.spawnLldbMi(args=None)

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Run to main
        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\"")
        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

        # Test that "thread step-over" steps over
        self.runCmd("thread step-over")
        self.expect("\^done")
        self.expect("@\"argc=1\\\\r\\\\n\"")
        self.expect("\*stopped,reason=\"end-stepping-range\"")

    @skipIfWindows  # llvm.org/pr24452: Get lldb-mi tests working on Windows
    @skipIfFreeBSD  # llvm.org/pr22411: Failure presumably due to known thread races
    @skipIfLinux  # llvm.org/pr22841: lldb-mi tests fail on all Linux buildbots
    def test_lldbmi_thread_continue(self):
        """Test that 'lldb-mi --interpreter' can continue execution by "thread continue" command."""

        self.spawnLldbMi(args=None)

        # Load executable
        self.runCmd("-file-exec-and-symbols %s" % self.myexe)
        self.expect("\^done")

        # Run to main
        self.runCmd("-break-insert -f main")
        self.expect("\^done,bkpt={number=\"1\"")
        self.runCmd("-exec-run")
        self.expect("\^running")
        self.expect("\*stopped,reason=\"breakpoint-hit\"")

        # Test that "thread continue" continues execution
        self.runCmd("thread continue")
        self.expect("\^done")
        self.expect("@\"argc=1\\\\r\\\\n")
        self.expect("\*stopped,reason=\"exited-normally\"")

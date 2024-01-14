import getpass
import os
import re
import shlex
import subprocess

import pexpect
import threading
import time


class OpenVPNManager:
    def __init__(self, config_path, password):
        self.config_path = config_path
        self.password = password
        self.process = None
        self.thread = None

    def start(self):
        if self.process or (self.thread and self.thread.is_alive()):
            print("OpenVPN is already running.")
        else:
            self.thread = threading.Thread(target=self._start_openvpn_thread)
            self.thread.start()
            print("OpenVPN started in a separate thread.")
        time.sleep(1)

    def _start_openvpn_thread(self):
        openvpn_command = f"sudo openvpn {self.config_path}"
        self.process = self._sudo(openvpn_command)
        if self.process:
            try:
                pass
                # Simulate waiting for user input (replace with actual tasks)
                #
                time.sleep(700)
            finally:
                pass
            #     # Stop the OpenVPN process gracefully
            #     self._stop_openvpn()

    def _sudo(self, command):
        child = pexpect.spawn(command)
        try:
            # Expecting the password prompt
            child.expect(['password', pexpect.EOF], timeout=6)
            # Sending the password
            child.sendline(self.password)
            # Wait for the command to finish
            child.expect(pexpect.EOF)

            if "pgrep" in command:
                result_output = child.before.decode("utf-8")
                return result_output

        except pexpect.ExceptionPexpect as e:
            pass
        finally:
            if "pgrep" or "kill" in command:
                pass
            elif child:
                return child

    def _stop_openvpn(self):
        try:
            if self.process:
                # Stop the OpenVPN process gracefully
                self.process.sendintr()  # Send an interrupt signal
                self.process.expect(pexpect.EOF)  # Wait for the process to finish
        except pexpect.ExceptionPexpect as e:
            print(f"Error stopping OpenVPN: {e}")

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.kill_openvpn_processes()
            print("thread is stopped")
        if self.process:
            self._stop_openvpn()
            print("process is stopped")
        time.sleep(1)

    def kill_openvpn_processes(self):
        try:
            # Run pgrep to get the PID of openvpn
            pgrep_command = "/usr/bin/sudo pgrep openvpn"
            pgrep_output = self._sudo(pgrep_command)
            # pgrep_output = str(pgrep_output).split("-")
            pgrep_output = re.findall(r'\b\d+\b', pgrep_output)

            if pgrep_output:
                for pid in pgrep_output:
                    # print(f"Killing openvpn process with PID: {pid}")
                    # Run sudo kill command
                    kill_command = f"sudo kill {pid}"
                    self._sudo(kill_command)

        except Exception as e:
            print(f"An error occurred: {e}")


#
# if __name__ == "__main__":
#     openvpn_manager = OpenVPNManager(config_path="/home/mb/Downloads/nikto13-il1.vpnjantit-udp-2500.ovpn")
#     openvpn_manager.start()
#     #
#     # print("3")
#     # time.sleep(100)
#     openvpn_manager.stop()
#     # finally:
#     #     # Stop the OpenVPN command and thread when needed
#     #     openvpn_manager.stop()

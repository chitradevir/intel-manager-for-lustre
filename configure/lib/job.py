
from configure.models import Job

from logging import getLogger, FileHandler, StreamHandler, DEBUG, INFO
job_log = getLogger('job')
job_log.setLevel(DEBUG)
job_log.addHandler(FileHandler("job.log"))
import settings
if settings.DEBUG:
    job_log.setLevel(DEBUG)
    #job_log.addHandler(StreamHandler())
else:
    job_log.setLevel(INFO)

class StepPaused(Exception):
    """A step did not execute because the job is paused."""
    pass

class StepAborted(Exception):
    """A step did not execute because the job has errored."""
    pass

class StepFailed(Exception):
    """A step executed and returned an exception.  The job has been marked as errored."""
    def __init__(self, step_exception):
        self.step_exception = step_exception
    pass

class StepCleanError(Exception):
    """A step encountered an error which prevented it making any changes,
       such the step may be retried at will.  For example, an attempt to
       mkfs over ssh failed to establish a connection: there is no risk that
       mkfs command started running"""
    pass

class StepDirtyError(Exception):
    """A step encountered an error which may have left the system in 
       an inconsistent state.  For example, connectivity was lost partway
       through a mkfs operation: we don't know if the filesystem is formatted
       or not"""
    pass


STEP_PAUSE_DELAY = 10

class Step(object):
    def __init__(self, job, args):
        self.args = args
        self.job_id = job.id

        # This step is the final one in the job
        self.final = False

    def mark_final(self):
        self.final = True

    def is_idempotent(self):
        """Indicate whether the step is idempotent.  For example, mounting 
           a target.  Step subclasses which are idempotent should override this and
           return True."""
        return False

    def run(self):
        raise NotImplementedError

    def retry(self):
        steps = self.get_steps()
        # Which one failed?

class StateChangeJob(object):
    """Subclasses must define a class attribute 'stateful_object'
       identifying another attribute which returns a StatefulObject"""
    def get_stateful_object(self):
        stateful_object = getattr(self, self.stateful_object)
        assert(isinstance(stateful_object, StatefulObject))
        return stateful_object

from logging import getLogger, FileHandler, DEBUG
getLogger('ssh').setLevel(DEBUG)
getLogger('ssh').addHandler(FileHandler("ssh.log"))
def debug_ssh(host, command):
    ssh_monitor = host.monitor.downcast()

    import paramiko
    import socket
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    from settings import AUDIT_PERIOD
    # How long it may take to establish a TCP connection
    SOCKET_TIMEOUT = 3600
    # How long it may take to get the output of our agent
    # (including tunefs'ing N devices)
    SSH_READ_TIMEOUT = 3600

    args = {"hostname": ssh_monitor.host.address,
            "username": ssh_monitor.get_username(),
            "timeout": SOCKET_TIMEOUT}
    if ssh_monitor.port:
        args["port"] = ssh_monitor.port
    # Note: paramiko has a hardcoded 15 second timeout on SSH handshake after
    # successful TCP connection (Transport.banner_timeout).
    ssh.connect(**args)
    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.settimeout(SSH_READ_TIMEOUT)
    channel.exec_command(command)
    result_stdout = channel.makefile('rb').read()
    result_stderr = channel.makefile_stderr('rb').read()
    result_code = channel.recv_exit_status()
    ssh.close()

    getLogger('ssh').debug("%s: %s" % (host, command))

    job_log.debug("debug_ssh:%s:%s:%s" % (host, result_code, command))
    if result_code != 0:
        job_log.error(result_stdout)
        job_log.error(result_stderr)
    return result_code, result_stdout, result_stderr

from monitor.models import *
from configure.models import *

class MkfsStep(Step):
    def _mkfs_command(self, target):
        args = []
        primary_mount = target.targetmount_set.get(primary = True)

        args.append({
            ManagedMgs: "--mgs",
            ManagedMdt: "--mdt",
            ManagedOst: "--ost"
            }[target.__class__])

        if isinstance(target, FilesystemMember):
            args.append("--fsname=%s" % target.filesystem.name)
            args.extend(target.filesystem.mgsnode_spec())

        args.append("--reformat")

        for secondary_mount in target.targetmount_set.filter(primary = False):
            host = secondary_mount.host
            nids = ",".join([n.nid_string for n in host.nid_set.all()])
            assert nids != "", RuntimeError("No NIDs known for host %s" % host)
            args.append("--failover=%s" % nids)

        args.append(primary_mount.block_device.path)

        return "/usr/sbin/mkfs.lustre %s" % " ".join(args)

    def run(self, kwargs):
        target_id = kwargs['target_id']
        target = Target.objects.get(id = target_id).downcast()

        assert(isinstance(target, ManagedTarget))
        host = target.targetmount_set.get(primary = True).host
        command = self._mkfs_command(target)

        code, out, err = debug_ssh(host, command)
        # Assume nonzero returns from mkfs mean it didn't touch anything
        if code != 0:
            from configure.lib.job import StepDirtyError
            raise StepDirtyError()

class NullStep(Step):
    def run(self, kwargs):
        pass

class MountStep(Step):
    def _mount_command(self, target_mount):
        assert(target_mount.block_device.path != None)
        return "mount -t lustre %s %s" % (target_mount.block_device.path, target_mount.mount_point)

    def is_idempotent(self):
        return True

    def run(self, kwargs):
        target_mount_id = kwargs['target_mount_id']
        target_mount = TargetMount.objects.get(id = target_mount_id)

        code, out, err = debug_ssh(target_mount.host, self._mount_command(target_mount))
        if code != 0 and code != 17 and code != 114:
            from configure.lib.job import StepCleanError
            print code, out, err
            print StepCleanError
            raise StepCleanError()

class MkdirStep(Step):
    def _mkdir_command(self, target_mount):
        return "/bin/mkdir -p %s" % (target_mount.mount_point)

    def is_idempotent(self):
        return True

    def run(self, kwargs):
        target_mount_id = kwargs['target_mount_id']
        target_mount = TargetMount.objects.get(id = target_mount_id)

        code, out, err = debug_ssh(target_mount.host, self._mkdir_command(target_mount))
        if code != 0:
            from configure.lib.job import StepCleanError
            print code, out, err
            print StepCleanError
            raise StepCleanError()

class StartLNetStep(Step):
    def is_idempotent(self):
        return True

    def run(self, kwargs):
        host = Host.objects.get(id = kwargs['host_id'])

        code, out, err = debug_ssh(host, "/usr/sbin/lctl network up")
        if code != 0:
            from configure.lib.job import StepCleanError
            print code, out, err
            print StepCleanError
            raise StepCleanError()

class StopLNetStep(Step):
    def is_idempotent(self):
        return True

    def run(self, kwargs):
        host = Host.objects.get(id = kwargs['host_id'])

        code, out, err = debug_ssh(host, "/root/hydra-rmmod.py ptlrpc; /usr/sbin/lctl network down")
        if code != 0:
            from configure.lib.job import StepCleanError
            print code, out, err
            print StepCleanError
            raise StepCleanError()


class LoadLNetStep(Step):
    def is_idempotent(self):
        return True

    def run(self, kwargs):
        host = Host.objects.get(id = kwargs['host_id'])

        code, out, err = debug_ssh(host, "/sbin/modprobe lnet")
        if code != 0:
            from configure.lib.job import StepCleanError
            print code, out, err
            print StepCleanError
            raise StepCleanError()

class UnloadLNetStep(Step):
    def is_idempotent(self):
        return True

    def run(self, kwargs):
        host = Host.objects.get(id = kwargs['host_id'])

        code, out, err = debug_ssh(host, "/root/hydra-rmmod.py lnet")
        if code != 0:
            from configure.lib.job import StepCleanError
            print code, out, err
            print StepCleanError
            raise StepCleanError()

class UnmountStep(Step):
    def _unmount_command(self, target_mount):
        return "umount -t lustre %s" % (target_mount.mount_point)

    def is_idempotent(self):
        return True

    def run(self, kwargs):
        target_mount_id = kwargs['target_mount_id']
        target_mount = TargetMount.objects.get(id = target_mount_id)

        code, out, err = debug_ssh(target_mount.host, self._unmount_command(target_mount))
        # FIXME: assuming code=1 is an 'already unmounted' therefore ok
        if (code != 0) and (code != 1):
            from configure.lib.job import StepCleanError
            print code, out, err
            print StepCleanError
            raise StepCleanError()

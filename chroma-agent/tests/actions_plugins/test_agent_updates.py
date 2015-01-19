import mock
import os
from tempfile import NamedTemporaryFile

from mock import patch

from chroma_agent.action_plugins import agent_updates
from chroma_agent.device_plugins import lustre
from chroma_agent import config
from tests.command_capture_testcase import CommandCaptureTestCase, CommandCaptureCommand


class TestManageUpdates(CommandCaptureTestCase):
    def setUp(self):
        super(TestManageUpdates, self).setUp()
        self.tmpRepo = NamedTemporaryFile(delete=False)

        self.old_scan_packages = lustre.scan_packages
        lustre.scan_packages = mock.Mock(return_value={})

    def tearDown(self):
        if os.path.exists(self.tmpRepo.name):
            os.remove(self.tmpRepo.name)

        lustre.scan_packages = self.old_scan_packages

    def test_configure_repo(self):
        import chroma_agent
        expected_content = """
[Intel Lustre Manager]
name=Intel Lustre Manager updates
baseurl=http://www.test.com/test.repo
enabled=1
gpgcheck=0
sslverify = 1
sslcacert = /var/lib/chroma/authority.crt
sslclientkey = /var/lib/chroma/private.pem
sslclientcert = /var/lib/chroma/self.crt
"""
        with patch('__builtin__.open', spec=file, create=True) as mock_open:
            with patch.object(chroma_agent.config, 'path', "/var/lib/chroma/", create=True):
                agent_updates.configure_repo('http://www.test.com/test.repo')
                mock_open.return_value.write.assert_called_once_with(expected_content)

    def test_unconfigure_repo(self):
        agent_updates.unconfigure_repo(self.tmpRepo.name)
        self.assertFalse(os.path.exists(self.tmpRepo.name))

    def test_update_packages(self):
        self.add_commands(CommandCaptureCommand(('yum', 'clean', 'all', '--enablerepo=*')),
                          CommandCaptureCommand(('repoquery', '--disablerepo=*', '--enablerepo=myrepo', '--pkgnarrow=updates', '-a'), stdout="""chroma-agent-99.01-3061.noarch
chroma-agent-management-99.01-3061.noarch
"""),
                          CommandCaptureCommand(('repoquery', '--requires', 'mypackage')),
                          CommandCaptureCommand(('yum', 'update', '-y', '--enablerepo=myrepo', 'chroma-agent-99.01-3061.noarch', 'chroma-agent-management-99.01-3061.noarch')))
        agent_updates.update_packages(['myrepo'], ['mypackage'])

        self.assertRanAllCommandsInOrder()

    def test_install_packages(self):
        self.add_commands(CommandCaptureCommand(('yum', 'clean', 'all', '--enablerepo=*')),
                          CommandCaptureCommand(('yum', 'install', '-y', '--enablerepo=myrepo', 'foo', 'bar')),
                          CommandCaptureCommand(('yum', 'check-update', '-q', '--disablerepo=*', '--enablerepo=myrepo'), stdout="""
jasper-libs.x86_64                                                                             1.900.1-16.el6_6.3                                                                             myrepo
"""),
                          CommandCaptureCommand(('yum', 'update', '-y', '--enablerepo=myrepo', 'jasper-libs.x86_64')))

        agent_updates.install_packages(['myrepo'], ['foo', 'bar'])

        self.assertRanAllCommandsInOrder()

    def test_kernel_status(self):
        def try_run(args):
            if args == ["rpm", "-qR", "lustre-modules"]:
                return """/bin/sh
/bin/sh
/bin/sh
kernel = 2.6.32-358.18.1.el6
rpmlib(CompressedFileNames) <= 3.0.4-1
rpmlib(FileDigests) <= 4.6.0-1
rpmlib(PayloadFilesHavePrefix) <= 4.0-1
rpmlib(PayloadIsXz) <= 5.2-1
"""
            elif args == ["uname", "-r"]:
                return "2.6.32-358.2.1.el6.x86_64\n"
            elif args == ["rpm", "-q", "kernel"]:
                return """kernel-2.6.32-358.2.1.el6.x86_64
kernel-2.6.32-358.18.1.el6.x86_64
"""

        with patch('chroma_agent.chroma_common.lib.shell.try_run', side_effect=try_run):
            result = agent_updates.kernel_status()
            self.assertDictEqual(result, {
                'required': 'kernel-2.6.32-358.18.1.el6.x86_64',
                'running': 'kernel-2.6.32-358.2.1.el6.x86_64',
                'available': [
                    "kernel-2.6.32-358.2.1.el6.x86_64",
                    "kernel-2.6.32-358.18.1.el6.x86_64"
                ]
            })

    def test_install_packages_force(self):
        self.add_commands(CommandCaptureCommand(('yum', 'clean', 'all', '--enablerepo=*')),
                          CommandCaptureCommand(('repoquery', '--requires', '--enablerepo=myrepo', 'foo'), stdout="""/usr/bin/python
python >= 2.4
python(abi) = 2.6
yum >= 3.2.29
/bin/sh
kernel = 2.6.32-279.14.1.el6_lustre
lustre-backend-fs

        """),
                          CommandCaptureCommand(('yum', 'install', '-y', '--enablerepo=myrepo', 'kernel-2.6.32-279.14.1.el6_lustre')),
                          CommandCaptureCommand(('yum', 'install', '-y', '--enablerepo=myrepo', 'foo')),
                          CommandCaptureCommand(('yum', 'check-update', '-q', '--disablerepo=*', '--enablerepo=myrepo'), stdout="""
jasper-libs.x86_64                                                                             1.900.1-16.el6_6.3                                                                             myrepo
"""),
                          CommandCaptureCommand(('yum', 'update', '-y', '--enablerepo=myrepo', 'jasper-libs.x86_64')))

        agent_updates.install_packages(['myrepo'], ['foo'], force_dependencies=True)

        self.assertRanAllCommandsInOrder()

    def test_set_profile_success(self):
        self.mock_read_uri_result = None

        def mock_ReadServerURI(args):
            return self.mock_read_uri_result

        with patch('chroma_agent.utils.ReadServerURI', side_effect=mock_ReadServerURI):
            config.update('settings', 'profile', {'managed': False})

            # Go from managed = False to managed = True
            self.add_command(('yum', 'install', '-y', '--enablerepo=iml-agent', 'chroma-agent-management'))
            self.mock_read_uri_result = {'objects': [{'managed': True}]}
            self.assertEqual(agent_updates.set_profile('test_profile'), None)
            self.assertRanAllCommandsInOrder()

            # Go from managed = True to managed = False
            self.reset_command_capture()
            self.add_command(('yum', 'remove', '-y', '--enablerepo=iml-agent', 'chroma-agent-management'))
            self.mock_read_uri_result = {'objects': [{'managed': False}]}
            self.assertEqual(agent_updates.set_profile('test_profile'), None)
            self.assertRanAllCommandsInOrder()

            # Go from managed = False to managed = False
            self.reset_command_capture()
            self.assertEqual(agent_updates.set_profile('test_profile'), None)
            self.assertRanAllCommandsInOrder()

    def test_set_profile_fail(self):
        self.mock_read_uri_result = None

        # Three times because yum will try three times.
        self.add_commands(CommandCaptureCommand(('yum', 'install', '-y', '--enablerepo=iml-agent', 'chroma-agent-management'), rc=1, stdout="Bad command stdout", stderr="Bad command stderr"),
                          CommandCaptureCommand(('yum', 'install', '-y', '--enablerepo=iml-agent', 'chroma-agent-management'), rc=1, stdout="Bad command stdout", stderr="Bad command stderr"),
                          CommandCaptureCommand(('yum', 'install', '-y', '--enablerepo=iml-agent', 'chroma-agent-management'), rc=1, stdout="Bad command stdout", stderr="Bad command stderr"))

        def mock_ReadServerURI(args):
            return self.mock_read_uri_result

        with patch('chroma_agent.utils.ReadServerURI', side_effect=mock_ReadServerURI):
            config.update('settings', 'profile', {'managed': False})

            # Go from managed = False to managed = True, but it will fail.
            self.mock_read_uri_result = {'objects': [{'managed': True}]}
            self.assertEqual(agent_updates.set_profile('test_profile'), 'Unable to set profile because yum returned Bad command stdout')
            self.assertRanAllCommandsInOrder()


from testconfig import config
from tests.integration.core.chroma_integration_testcase import ChromaIntegrationTestCase
from tests.integration.core.remote_operations import SimulatorRemoteOperations, RealRemoteOperations


class TestCreateFilesystem(ChromaIntegrationTestCase):
    TEST_SERVERS = config['lustre_servers'][0:4]
    fs_name = "testfs"

    def _exercise_simple(self, fs_id):
        filesystem = self.get_filesystem(fs_id)
        client = config['lustre_clients'][0]['address']
        self.remote_operations.mount_filesystem(client, filesystem)
        try:
            self.remote_operations.exercise_filesystem(client, filesystem)
        finally:
            self.remote_operations.unmount_filesystem(client, filesystem)

    def test_create(self):
        """ Test that a filesystem can be created"""

        self.assertGreaterEqual(len(config['lustre_servers']), 4)

        self.hosts = self.add_hosts([
            config['lustre_servers'][0]['address'],
            config['lustre_servers'][1]['address'],
            config['lustre_servers'][2]['address'],
            config['lustre_servers'][3]['address']
        ])

        volumes = self.get_shared_volumes(required_hosts = 4)
        self.assertGreaterEqual(len(volumes), 4)

        mgt_volume = volumes[0]
        mdt_volume = volumes[1]
        ost1_volume = volumes[2]
        ost2_volume = volumes[3]
        self.set_volume_mounts(mgt_volume, self.hosts[0]['id'], self.hosts[1]['id'])
        self.set_volume_mounts(mdt_volume, self.hosts[1]['id'], self.hosts[0]['id'])
        self.set_volume_mounts(ost1_volume, self.hosts[2]['id'], self.hosts[3]['id'])
        self.set_volume_mounts(ost2_volume, self.hosts[3]['id'], self.hosts[2]['id'])

        self.filesystem_id = self.create_filesystem({
            'name': self.fs_name,
            'mgt': {'volume_id': mgt_volume['id']},
            'mdt': {
                'volume_id': mdt_volume['id'],
                'conf_params': {}

            },
            'osts': [{
                'volume_id': ost1_volume['id'],
                'conf_params': {}
            }, {
                'volume_id': ost2_volume['id'],
                'conf_params': {}
            }],
            'conf_params': {}
        })

        self._exercise_simple(self.filesystem_id)

        self.assertTrue(self.get_filesystem_by_name(self.fs_name)['name'] == self.fs_name)


class TestExistsFilesystem(TestCreateFilesystem):
    def setUp(self):
        # connect the remote operations but otherwise...
        if config.get('simulator', False):
            self.remote_operations = SimulatorRemoteOperations(self, self.simulator)
        else:
            self.remote_operations = RealRemoteOperations(self)

        # Enable agent debugging
        self.remote_operations.enable_agent_debug(self.TEST_SERVERS)

        self.wait_until_true(self.supervisor_controlled_processes_running)
        self.initial_supervisor_controlled_process_start_times = self.get_supervisor_controlled_process_start_times()

    def test_exists(self):
        self.assertTrue(self.get_filesystem_by_name(self.fs_name)['name'] == self.fs_name)
        self._exercise_simple(self.get_filesystem_by_name(self.fs_name)['id'])
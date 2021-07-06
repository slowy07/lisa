# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from pathlib import Path

from assertpy import assert_that

from lisa import Node, TestCaseMetadata, TestSuite, TestSuiteMetadata
from lisa.features import Sriov
from lisa.testsuite import simple_requirement
from lisa.operating_system import Ubuntu, Redhat, CentOs, Oracle
from lisa.tools import Git


@TestSuiteMetadata(
    area="dpdk",
    category="functional",
    description="""
    This test suite check DPDK functionality
    """,
)
class dpdk(TestSuite):
    _ubuntu_packages = [
        "librdmacm-dev",
        "librdmacm1",
        "build-essential",
        "libnuma-dev",
        "libmnl-dev",
        "libelf-dev",
        "meson",
        "rdma-core",
        "librdmacm-dev",
        "librdmacm1",
        "build-essential",
        "libnuma-dev",
        "libmnl-dev",
        "libelf-dev",
        "dpkg-dev",
        "pkg-config",
        "python3-pip",
        "python3-pyelftools",
        "python-pyelftools",
    ]

    _dpdk_github = "https://github.com/DPDK/dpdk.git"

    def _install_dpdk_dependencies(self, node: Node) -> None:
        if isinstance(node.os, Ubuntu):
            node.os.install_packages(self._ubuntu_packages)
            self.log.info("Packages installed for Ubunutu")
        elif isinstance(node.os, Redhat) or isinstance(node.os, CentOs):
            node.os.install_packages(
                ["groupinstall", "'Infiniband Support'"], signed=False
            )  # todo gross hack to support groupinstall
            result = node.execute(
                "dracut --add-drivers 'mlx4_en mlx4_ib mlx5_ib' -f"
            )  # add mellanox drivers
            self.log.debug("\n".join([result.stdout, result.stderr]))

    def _install_dpdk(self, node: Node) -> None:
        git_tool = node.tools[Git]
        git_tool.clone(self._dpdk_github, cwd=node.working_path)
        self.log.info(node.execute("ls -la", cwd=node.working_path).stdout)

    @TestCaseMetadata(
        description="""
            This test case checks DPDK can be built and installed correctly.
        """,
        requirement=simple_requirement(
            supported_features=[Sriov],
        ),
        priority=1,
    )
    def check_dpdk_build(self, case_name: str, node: Node) -> None:
        sriov_feature = node.features[Sriov]
        sriov_is_enabled = sriov_feature.enabled()
        self.log.info(f"Verify SRIOV is enabled: {sriov_is_enabled}")
        assert_that(sriov_is_enabled).described_as(
            "SRIOV was not enabled for this test node."
        )
        self._install_dpdk_dependencies(node)
        self._install_dpdk(node)

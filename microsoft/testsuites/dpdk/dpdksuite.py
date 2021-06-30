# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from pathlib import Path

from assertpy import assert_that

from lisa import Node, TestCaseMetadata, TestSuite, TestSuiteMetadata
from lisa.features import Sriov
from lisa.testsuite import simple_requirement


@TestSuiteMetadata(
    area="dpdk",
    category="functional",
    description="""
    This test suite check DPDK functionality
    """,
)
class dpdk(TestSuite):
    def _install_dpdk(self, node: Node, case_path: Path) -> None:
        pass

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
        pass

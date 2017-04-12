.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Wenjing Chu (Huawei) and others

=============================================
Background and the Purpose of This Worksheet
=============================================

The Dovetail test suite for OPNFV Compliance Verification Program (CVP) [1]
consists of a set of test areas that are developed the community. A test area
is a convenient grouping of test cases focused on one area, typically
corresponding to test cases developed by a project or projects. It can also be
incorporated from upstream open source communities.

In order for new test areas or new test cases in existing test areas be accepted into
Dovetail compliance test suite for CVP, they must be in scope as defined by CVP governance
document [1], and meet requirements
(including quality requirements) documented in the Dovetail wiki page [2].
 
In addition, the features being tested by the proposed test
cases must be in the referenced OPNFV release (the corresponding release). 
E.g. the current Dovetail plan is for Danube release, and in this release, Dovetail also excludes 
hardware-only testing due to the lack of test framework aimed at
hardware testing at the Danube time frame.

When a proposal is made to add a new test area, or new test cases to an
existing test area to the Dovetail test suite, such proposal should be
accompanied by clear information that the proposed test area or test cases are
in the high level scope, as described above, and meet the requirements outlined in [2]. Information about the test
cases is also required in more detail to be included in the Dovetail test plan documentation
ir order to help tesers (the end users in the case of Dovetail) to have better
understanding of the test cases.

This worksheet is intended as a general guide to the project contributors of the
test cases in their researching and documenting such
information in a questionarie format. Normally, the PTLs and committers of the
originating OPNFV feature projects, on behalf of these projects, and in
cooperation with the testing projects that may have helped in 
developing the test cases, should be responsible for the completion of
this worksheet to ensure the information's accuracy. The Dovetail project will
work with the submitters to review the submitted worksheet in its weekly calls to ensure that the
information contained in the worksheet is complete, the proposed test area
falls in scope and in general meets test case requirement criteria in [2].
Dovetail project may also suggest remediation steps to help ensure quality. 
Once completed, the worksheet will then be
announced in the tech-discussion mailing list as a submission to be
incorporated into the compliance test suite and open for community inputs. The
remaining process is similar to a new project proposal, with two weeks of
community review and a meeting review in the Technical Discussion community
conference call to reach consensus in the inclusion of the proposed test area.

The compliance test suite will then be recommended to the TSC and approved by
voting in the TSC prior to launching the CVP in each release cycle that
contains updates.

The completed worksheet can be in wiki format. An example can be found in [3]
for your reference.

=============================
General Test Case Information
=============================

- Provide a high level description of the test area, main features being
  tested, and answer why it is in scope for Dovetail Danube. If there is a
  subset that is in scope, describe the subset.

- Describe how the features are tested, and justify why it is appropriate
  methodology for compliance testing. If modification or enhancement are
  needed, please describe the work needed in Dovetail.

- Describe how the automated test cases are implemented, and why it is
  appropriate for compliance testing. If modification or enhancement are
  needed, please describe the work needed in Dovetail

- Describe test results, pass/fail criteria

- Describe the conditions that the SUT must be in for the test cases to run.
  Are the test cases executable in a limited subset of OPNFV Scenarios only? If
  so, which subset have the pre-conditions met to pass?

- Provide a link of pass test run results /  examples.

- Any other important information or comments

========================================= 
Specific Test Case Requirement / Criteria
=========================================


All test cases must meet these criteria.

- If there is an industry standard, the test cases should follow the standard.
  Please provide references of the standards.

- If the existing standards are not followed, please provide justifications. An
  exception is required.

- If a compliance test suite exists for the upstream component being tested,
  the upstream test suite should be used as a baseline. Please describe the
  baseline upstream suite.
	- If this is not followed, or a subset is excluded or modified from the
	  upstream, please provide justifications. An exception is required.

- Test cases must be able to pass one or more OPNFV reference deployment or
  deployments, as deployed according to one or more scenarios that are in scope
  of the corresponding OPNFV release. Please describe the scenarios that the test cases can pass (assuming
  the scenarios are correctly deployed - i.e. if it is due to errors of the SUT
  software, we don't disqualify a test case for that.)

- The features being tested must not rely on unmerged patches in the upstream
  projects. In other words, unmerged patches are considered not mature enough
  for Dovetail suite. Please list the upstream projects and affirm this is the
  case to the relevant upstream projects.

- The features being tested must be in scope of CVP during the corresponding release cycle.
  Please affirm that this is the case for the proposed set of test cases.

- Any other important information or comments.

============= 
JIRA Tickets
=============

If additional work is required to meet the requirements, please list the
associated JIRA tickets. The tickets should clearly state the work to be done,
assigned resources, and completion time.

==========
References
==========
[1] CVP governance document:
https://wiki.opnfv.org/display/dovetail/CVP+document

[2] Dovetail test case requirements:
https://wiki.opnfv.org/display/dovetail/Dovetail+Test+Case+Requirements

[3] SDNVPN compliance test cases for Dovetail:
https://wiki.opnfv.org/display/sdnvpn/SDNVPN+Testing#SDNVPNTesting-TestcompliancetemplateforDovetail



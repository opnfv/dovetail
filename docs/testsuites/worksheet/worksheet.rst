.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Wenjing Chu (Huawei) and others

==============================
Purpose of This Worksheet
==============================

In order for new test areas or test cases in the test areas be accepted into Dovetail test suite for 
CVP, they must be in scope as defined by CVP governance document approved by the Board of Directors 
CVP document, and meet requirements (including quality requirements) documented in the wiki page: 
Dovetail Test Case Requirements. In addition, the features being tested by the proposed test cases 
must be in the scope of Danube release.Current Dovetail plan for Danube also excludes hardware-only 
testing due to lack of test framework aimed at hardware testing at the Danube time frame.
When a proposal is made to add a new test area, or new test cases to an existing test area to the 
Dovetail test suite, such proposal should be accompanied by clear information that the proposed test 
area or test cases are in scope and meet the requirements outlined in the above wiki page. This 
worksheet is intended as a general guide in researching and documenting such information in a 
questionarie format. The completed worksheet will then be reviewed in Dovetail project meetings to 
reach consensus determination or suggest remediation steps.

=============================
General Test Case Information
=============================

- Provide a high level description of the test area, main features being tested, and answer why it is in scope for Dovetail Danube. If there is a subset that is in scope, describe the subset.

- Describe how the features are tested, and justify why it is appropriate methodology for compliance testing. If modification or enhancement are needed, please describe the work needed in Dovetail.

- Describe how the automated test cases are implemented, and why it is appropriate for compliance testing. If modification or enhancement are needed, please describe the work needed in Dovetail

- Describe test results, pass/fail criteria

- Describe the conditions that the SUT must be in for the test cases to run. Are the test cases executable in a limited subset of OPNFV Scenarios only? If so, which subset have the pre-conditions met to pass?

- Provide a link of pass test run results /  examples, if any.

- Any other important information or comments

========================================= 
Specific Test Case Requirement / Criteria
=========================================


All test cases must meet these criteria.

- If there is an industry standard, the test cases should follow the standard. Please provide references of the standards.

- If the existing standards are not followed, please provide justifications. An exception is required.

- If a compliance test suite exists for the upstream component being tested, the upstream test suite should be used as a baseline. Please describe the baseline upstream suite.
	- If this is not followed, or a subset is excluded or modified from the upstream, please provide justifications. An exception is required.

- Test cases must be able to pass at least some OPNFV reference deployment or deployments, as deployed according to one or more scenarios.that are in scope of Danub. Please describe the scenarios that the test cases can pass (assuming the scenarios are correctly deployed - i.e. if it is due to errors of the SUT software, we don't disqualify a test case for that.)

- The features being tested must not rely on unmerged patches in the upstream projects. In other words, unmerged patches are considered not mature enough for Dovetail suite. Please list the upstream projects and affirm this is the case to the relevant upstream projects.

- The features being tested must be in scope of CVP during the Danube cycle. Please affirm that this is the case for the proposed set of test cases.

- Any other important information or comments.

============= 
JIRA Tickets
=============

If additional work is required to meet the requirements, please list the associated JIRA tickets. The tickets should clearly state the work to be done, assigned resources, and completion time.


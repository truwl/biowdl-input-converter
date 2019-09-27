# Copyright (c) 2019 Leiden University Medical Center
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path

from biowdl_input_converter.input_conversions import biowdl_yaml_to_samplegroup
from biowdl_input_converter.output_conversions import \
    samplegroup_to_biowdl_old_yaml
from biowdl_input_converter.samplestructure import Library, ReadGroup, \
    Sample, SampleGroup

import yaml

FILESDIR = Path(__file__).parent / Path("files")

COMPLETE_WITH_CONTROL_SAMPLEGROUP = SampleGroup([
    Sample(id="s1", libraries=[
        Library(id="lib1", readgroups=[
            ReadGroup(
                id="rg1",
                R1="r1.fq",
                R1_md5="hello",
                R2="r2.fq",
                R2_md5="hey"
            )])]),
    Sample(id="s2", additional_properties=dict(control="s1"), libraries=[
        Library(id="lib1", readgroups=[
            ReadGroup(
                id="rg1",
                R1="r1.fq",
                R1_md5="aa",
                R2="r2.fq",
                R2_md5="bb"
            )])])])


def test_import_biowdl_old_yaml():
    samplegroup = biowdl_yaml_to_samplegroup(
        FILESDIR / Path("complete_with_control.yml"))
    assert COMPLETE_WITH_CONTROL_SAMPLEGROUP == samplegroup


def test_export_biowdl_old_yaml():
    with (FILESDIR / Path("complete_with_control.yml")).open("r") as yaml_h:
        yaml_contents = yaml_h.read()
    yaml_exported = samplegroup_to_biowdl_old_yaml(
        COMPLETE_WITH_CONTROL_SAMPLEGROUP)
    # Load the yamls to assure they are functionally equivalent regardless of
    # order
    assert yaml.safe_load(yaml_exported) == yaml.safe_load(yaml_contents)
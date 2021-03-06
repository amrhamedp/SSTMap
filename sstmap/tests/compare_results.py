"""
Test scripts
General purpose: Take in two files as input and run the tests
Should be able to import the module and run for hsa and gist calculations run
as part of installation.

Place it insdie the test suite, at the end of test scripts import and run tests
Use numpy testing module.

Test quantities: divide into three groups
"""


import sys
import numpy as np
import numpy.testing as npt


class TestGistOutput():
    
    def __init__(self, test_data, ref_data):
        self.test_data = test_data
        self.ref_data = ref_data

    def test_grid(self):
        
        passed = True
        try:
            #npt.assert_equal(self.test_data.shape, self.ref_data.shape)
            npt.assert_almost_equal(self.test_data[:, 1:4], self.ref_data[:, 1:4], decimal=3)
        except Exception as e:
            print e
            passed = False

        return passed

    def test_voxel_number(self):

        passed = True
        try:
            npt.assert_equal(self.test_data.shape, self.ref_data.shape)
        except Exception as e:
            print e
            passed = False

        return passed

    def test_quantity(self, quantity_index):

        passed = True
        try:
            npt.assert_array_almost_equal(self.test_data[:, quantity_index], self.ref_data[:, quantity_index], decimal=2)
        except Exception as e:
            print e
            passed = False

        return passed


def read_gist_sstmap(sstmap_gist_summary):
    columns_to_read = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18]
    sstmap_data = np.loadtxt(sstmap_gist_summary, skiprows=1, usecols=columns_to_read)
    #sstmap_data = sstmap_data[np.where(sstmap_data[:, 4] != 1.0)]
    return np.round(sstmap_data, 3)

def read_gist_cpptraj(cpptraj_gist_summary):
    columns_to_read = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20]
    cpptraj_data = np.loadtxt(cpptraj_gist_summary, skiprows=2, usecols=columns_to_read)
    if cpptraj_data.shape[1] == 24:
        columns_to_read = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 13, 14, 15, 16, 21, 22]
        cpptraj_data = np.loadtxt(cpptraj_gist_summary, skiprows=2, usecols=columns_to_read)
    
    #cpptraj_data = cpptraj_data[np.where(cpptraj_data[:, 4] != 1.0)]
    return cpptraj_data

if __name__ == '__main__':
    
    # Prepare data for testing
    test_result = {1: "Passed", 0: "Failed"}
    test_data, ref_data = read_gist_sstmap(sys.argv[1]), read_gist_cpptraj(sys.argv[2])
    diff_nwat = []
    for row in xrange(test_data.shape[0]):
        if test_data[row, 4] <= 1:
            test_data[row, 6:14] *= 0.0
        # record voxels with different water number but exclude them for tests
        else:
            if abs(int(test_data[row, 4]) - int(ref_data[row, 4])) >= 1:
                diff_nwat.append([test_data[row, :], ref_data[row, :]])
                test_data[row, 4:] *= 0.0
                ref_data[row, 4:] *= 0.0
    # Run tests
    print "Checking grid and voxel placement ...",
    testcase = TestGistOutput(test_data, ref_data)
    result = testcase.test_voxel_number()
    print test_result[bool(result)]
    result = testcase.test_grid()
    print test_result[bool(result)]
    print "Coverage for remaining tests.", 100*float(test_data.shape[0] - len(diff_nwat))/test_data.shape[0]
    print "Checking quantities ..."
    test_num = 0
    for quantity_index in xrange(4, test_data.shape[1]):
        result = testcase.test_quantity(quantity_index)
        print "Test %d ... %s" % (test_num, test_result[bool(result)])
        test_num += 1


        
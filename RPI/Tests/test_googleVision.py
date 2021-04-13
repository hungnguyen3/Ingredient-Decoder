from unittest import TestCase
import googleVision as dut


class GetMatchingArrTest(TestCase):

    def test_get_matching_arr0(self):
        list1 = ["apple", "banana", "orange", "grape"]
        list2 = ["red", "orange", "yellow", "green"]
        result = sorted(dut.getMatchingArr(list1, list2))
        assert result == ["orange"]

    def test_get_matching_arr1(self):
        list1 = ["a", "b", "c", "d", "d", "c", "b"]
        list2 = ["a", "b", "c", "d", "e", "f", "F", "E", "D", "E", "D", "C", "B", "A"]
        result = sorted(dut.getMatchingArr(list1, list2))
        expected = ["a", "b", "c", "d"]

        assert result == expected

    def test_get_matching_arr2(self):
        list1 = ["a", "b", "c", "d"]
        list2 = ["F", "E", "D", "E", "D", "C", "B", "A"]
        result = sorted(dut.getMatchingArr(list1, list2))
        expected = ["a", "b", "c", "d"]

        assert result == expected

    def test_get_matching_arr3(self):
        list1 = ["a", "b", "c", "d"]
        list2 = ["F", "E", "G", "E"]
        result = sorted(dut.getMatchingArr(list1, list2))
        expected = []

        assert result == expected

    def test_get_matching_arr4(self):
        list1 = ["a", "b", "c", "d"]
        list2 = []
        result = sorted(dut.getMatchingArr(list1, list2))
        expected = []

        assert result == expected

    def test_get_matching_arr5(self):
        list1 = "notOCR"
        list2 = ["F", "E", "D", "E", "D", "C", "B", "A"]
        result = dut.getMatchingArr(list1, list2)
        expected = "notOCR"
        print(result)
        assert result == expected

    def test_get_matching_arr6(self):
        list1 = "notRecognition"
        list2 = ["F", "E", "D", "E", "D", "C", "B", "A"]
        result = dut.getMatchingArr(list1, list2)
        expected = "notRecognition"

        assert result == expected
#
# class RequestOCRTest(TestCase):
#
#
#     def requestOCR(img_path):
#         img_data = prepareRequest(img_path, 'TEXT_DETECTION', 1)
#         response = requests.post(url,
#                                  data=img_data,
#                                  params={'key': key},
#                                  headers={'Content-Type': 'application/json'})
#         try:
#             response = response.json()["responses"][0]["textAnnotations"][0]["description"].lower()
#             return response
#         except KeyError:
#             return "notOCR"
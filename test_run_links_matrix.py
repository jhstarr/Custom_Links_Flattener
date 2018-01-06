import unittest
import json
import csv
from links_matrix_function import process_links_matrix

class MatrixTestCase(unittest.TestCase):
    """Tests for links_matrix_function.py"""

    def test_first_input(self):
        """Do the first test input and history matrices return 
        correct results."""
        
        links_input_filename = 'test_files/link_matrix_input1.csv' 
        links_output_filename = 'test_files/output_records1.csv'
        history_input_filename = 'test_files/links_history0.csv'
        history_output_filename = 'test_files/links_history1.csv'

        results1 = process_links_matrix(
            links_input_filename,
            history_input_filename)

        filename1 = 'test_files/output_matrix1.json'
        with open(filename1) as f_obj:
            om1_right_answer = json.load(f_obj)

        filename2 = 'test_files/history_matrix1.json'
        with open(filename2) as f_obj:
            hm1_right_answer = json.load(f_obj)
        
        self.assertEqual(results1, (om1_right_answer,hm1_right_answer))


    def test_second_input(self):
        """Do the second input and history matrices return 
        correct results."""
        
        links_input_filename = 'test_files/link_matrix_input2.csv' 
        links_output_filename = 'test_files/output_records2.csv'
        history_input_filename = 'test_files/links_history1.csv'
        history_output_filename = 'test_files/links_history2.csv'

        results2 = process_links_matrix(
            links_input_filename, 
            history_input_filename)
       
        filename1 = 'test_files/output_matrix2.json'
        with open(filename1) as f_obj:
            om2_right_answer = json.load(f_obj)

        filename2 = 'test_files/history_matrix2.json'
        with open(filename2) as f_obj:
            hm2_right_answer = json.load(f_obj)

        self.assertEqual(results2, (om2_right_answer,hm2_right_answer))

unittest.main()


import unittest

from get_video_info import youtube_search, get_video_id_from_url
from app import get_mongo_search_query, append_to_query


class Test_Fitness_Vid(unittest.TestCase):
    
    def test_get_video_id_from_url(self):
        """
        Tests various youtube video formats to see if the right video_id is properly extracted
        """
        self.assertEqual(get_video_id_from_url('https://www.youtube.com/embed/DqGwxR_0d1M'), 'DqGwxR_0d1M')
        self.assertEqual(get_video_id_from_url('https://youtu.be/DqGwxR_0d1M'), 'DqGwxR_0d1M')
        self.assertEqual(get_video_id_from_url('https://www.youtube.com/watch?v=DqGwxR_0d1M&feature=youtu.be'), 'DqGwxR_0d1M')
        self.assertEqual(get_video_id_from_url('https://www.youtube.com/watch?v=DqGwxR_0d1M'), 'DqGwxR_0d1M')
        
    def test_get_mongo_search_query(self):
        self.assertEqual(get_mongo_search_query('category_name', ["yoga"]), {'category_name': 'yoga'})
        self.assertEqual(get_mongo_search_query('category_name', ["yoga", "cardio"]), {'$or': [{'category_name':'yoga'}, {'category_name':'cardio'}]})
        self.assertEqual(get_mongo_search_query('category_name', ["yoga", "cardio", 'strenght']), {'$or': [{'category_name':'yoga'}, {'category_name':'cardio'}, {'category_name':'strenght'}]})
    
if __name__ == '__main__':
    unittest.main()
    
    
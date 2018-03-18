import unittest

from get_video_info import youtube_search, get_video_id_from_url


class Test_Fitness_Vid(unittest.TestCase):
    
    def test_get_video_id_from_url(self):
        """
        Tests various youtube video formats to see if the right video_id is properly extracted
        """
        self.assertEqual(get_video_id_from_url('https://www.youtube.com/embed/DqGwxR_0d1M'), 'DqGwxR_0d1M')
        self.assertEqual(get_video_id_from_url('https://youtu.be/DqGwxR_0d1M'), 'DqGwxR_0d1M')
        self.assertEqual(get_video_id_from_url('https://www.youtube.com/watch?v=DqGwxR_0d1M&feature=youtu.be'), 'DqGwxR_0d1M')
        self.assertEqual(get_video_id_from_url('https://www.youtube.com/watch?v=DqGwxR_0d1M'), 'DqGwxR_0d1M')
        
if __name__ == '__main__':
    unittest.main()
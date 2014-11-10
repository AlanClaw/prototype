# -*- coding: utf8 -*-
'''
#-*- coding:big5 -*- 
# -*- coding: utf8 -*-
'''
import logging
_logger = logging.getLogger(__name__)

import urllib2
from bs4 import BeautifulSoup

import ComUtils

class ApalPlayerRecord(object):

    PERCENTAGE_INDEX = [6,9,12]
    CALCULABLE_DATA_INDEX = range(4,22)
    
    DATA_KEY_LIST_MAPPING =   [  "Number"   ,
                                 "Name"     ,
                                 "Position" ,
                                 "Starter"  ,
                                 "3FGA"     ,
                                 "3FGM"     ,
                                 "3FG"      ,
                                 "FGA"      ,
                                 "FGM"      ,
                                 "FG"       ,
                                 "FTA"      ,
                                 "FTM"      ,
                                 "FT"       ,
                                 "OREB"     ,
                                 "DREB"     ,
                                 "REB"      ,
                                 "AST"      ,
                                 "STL"      ,
                                 "BLK"      ,
                                 "TOV"      ,
                                 "PF"       ,
                                 "PT"       ,
                                 "EFF"      ,
                                 "Comment"  
                              ]
    
    def __init__(self):
        self.DNP = True
        self.data = {"Number"     : "-1" ,
                     "Name"       : ""   ,
                     "Position"   : ""   ,
                     "Starter"    : False,
                     "3FGA"       : "0"  ,
                     "3FGM"       : "0"  ,
                     "3FG"        : "0"  ,
                     "FGA"        : "0"  ,
                     "FGM"        : "0"  ,
                     "FG"         : "0"  ,
                     "FTA"        : "0"  ,
                     "FTM"        : "0"  ,
                     "FT"         : "0"  ,
                     "OREB"       : "0"  ,
                     "DREB"       : "0"  ,
                     "REB"        : "0"  ,
                     "AST"        : "0"  ,
                     "STL"        : "0"  ,
                     "BLK"        : "0"  ,
                     "TOV"        : "0"  ,
                     "PF"         : "0"  ,
                     "PT"         : "0"  ,
                     "EFF"        : "0"  ,
                     "Comment"    : ""   
                    }


    def calculcate_percentage_data(self):
        """
        """
        
        for index in self.PERCENTAGE_INDEX:
            
            record_name      = self.DATA_KEY_LIST_MAPPING[index]
            denominator_key  = self.DATA_KEY_LIST_MAPPING[index-2]
            numerator_key    = self.DATA_KEY_LIST_MAPPING[index-1]
            
            try:
                self.data[record_name] = \
                    float(self.data[numerator_key]) / self.data[denominator_key]
            except ArithmeticError:
                self.data[record_name] = 0
            self.data[record_name] = round(self.data[record_name], 2)

    def calculcate_EFF_value(self):
        """
        """
        self.data['EFF'] = (float(self.data.get("PT")) + float(self.data.get("REB")) + \
                           float(self.data.get("AST")) + float(self.data.get("STL")) + \
                           float(self.data.get("BLK"))) - \
                           (( float(self.data.get("3FGA")) + float(self.data.get("FGA"))) - \
                            ( float(self.data.get("3FGM")) + float(self.data.get("FGM")))) - \
                            (float(self.data.get("FTA"))-float(self.data.get("FTM"))) - \
                            float(self.data.get("TOV"))
                

class ApalPlayerAvgRecord(ApalPlayerRecord):
    
    
    def __init__(self, player_name, player_num):
        '''
        '''
        super(ApalPlayerAvgRecord, self).__init__()
        
        self.GP = 0
        self.data["Name"] = player_name
        self.data["Number"] = player_num

    def calculate_average_record(self):
        """
        """
        index_list = list(set(self.CALCULABLE_DATA_INDEX).difference(set(self.PERCENTAGE_INDEX)))
        
        for index in index_list:
            
            record_name = self.DATA_KEY_LIST_MAPPING[index]
            try:
                self.data[record_name] = float(self.data.get(record_name)) / self.GP
            except ArithmeticError:
                self.data[record_name] = 0

class TeamRecord(object):
    
    team_name = None
    quarter_scores = None
    players = None
    
    def __init__(self):
        
        self.team_name = ""
        self.quarter_scores = []
        self.players = []

class GameInfo(object):
    
    temaA_name = None
    teamB_name = None
    game_sched_info = None
    game_result = None
    game_location = None
    game_date = None
    game_time = None
    
    def __init__(self):
        self.temaA_name = None
        self.teamB_name = None
        self.game_sched_info = None
        self.game_location = None
        self.game_result = None
        self.game_date = None
        self.game_time = None        
        
class ApalBoxScoreSpider(object):
    
    _box_url = None
    
    teamA = None
    teamB = None
    game_info = None
    
    def __init__(self, url):
        
        self._box_url = url
        
        self.teamA = TeamRecord()
        self.teamB = TeamRecord()
        self.game_info = GameInfo()
        
    def extract_target_data(self):
        
        page = urllib2.urlopen(self._box_url)
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), 'html5lib')
        
        # get team name
        self.extract_team_name(soup)

        # get player records respectively
        all_theads = soup.find_all('thead')
        self.extract_players_record(self.teamA, all_theads[-2])
        self.extract_players_record(self.teamB, all_theads[-1])

        # get this game information
        self.extract_game_info(soup)
        
        # get all quarter score
        game_score_section = soup.find_all("tr", align = "center")
        team1_section = game_score_section[0]
        team2_section = game_score_section[1]
        self.extract_game_score(self.teamA, team1_section)
        self.extract_game_score(self.teamB, team2_section)

    def extract_team_name(self, soup):
        
        all_tables = soup.find_all('td', style="vertical-align:middle;")
        
        team1 = ComUtils.get_utf8_value(all_tables[-3].contents)
        team2 = ComUtils.get_utf8_value(all_tables[-1].contents)
        
        _logger.debug(u'teamA = {0}'.format(team1.decode('utf-8')))
        self.teamA.team_name = team1
        _logger.debug(u'teamB = {0}'.format(team2.decode('utf-8')))
        self.teamB.team_name = team2
        
    def extract_players_record(self, team, parse_target):
        
        record_trs =  parse_target.find_all('tr')[2:-2]
        _logger.debug("total player_tmp: {0}".format(str(len(record_trs))))
        
        team.players = []
        for player_row in record_trs:
            cells = player_row.find_all('td')
            player_tmp = ApalPlayerRecord()                        
            for cell_index in range(23): # by APAL web site
#                 tmp = (player_tmp.data[cell_index][0], ComUtils.get_utf8_value(cells[cell_index]))
                key_name = ApalPlayerRecord().DATA_KEY_LIST_MAPPING[cell_index]
                player_tmp.data[key_name] = ComUtils.get_utf8_value(cells[cell_index])
                
            team.players.append(player_tmp)

#         for player in team.players:
#             for index in range(23):
#                 print "{0} = {1}".format(player.data[index][0], player.data[index][1])
        ''' deal with DNP player '''
        record_index = [4,5,7,8,10,11,13,14,16,17,18,19,20,21]
        for player in team.players:
            for cell_index in record_index:
                key_name = ApalPlayerRecord().DATA_KEY_LIST_MAPPING[cell_index]
                if player.data.get(key_name) != u'0'.encode('utf-8'):
                    player.DNP = False
                    break
            
#             print "{0} = {1}, index={2}, DNP={3}".format(player.data[1][0],
#                                                 player.data[1][1],
#                                                 cell_index,
#                                                 player.DNP
#                                                 )
            
    def extract_game_info(self, soup):
        """
        """
        all_tables = soup.find_all('td', style="vertical-align:middle;")
#         print all_tables
        game_sched_info = ComUtils.get_utf8_value(all_tables[0].contents)
#         _logger.debbug(game_sched_info)
        
        game_result = ComUtils.get_utf8_value(u"(") + ComUtils.get_utf8_value(all_tables[1].contents) + \
                      ComUtils.get_utf8_value(u") ")
        game_result += ComUtils.get_utf8_value(all_tables[2].contents)
        game_result += ComUtils.get_utf8_value(u"(") + ComUtils.get_utf8_value(all_tables[3].contents) + \
                      ComUtils.get_utf8_value(u") ")
#         _logger.debug("game_result = {0}".format(game_result))
        _logger.debug( soup.find_all('div', 't3')[0].contents[0].split("/")[0].encode('utf-8'))
        game_loc_time = ComUtils.get_utf8_value(soup.find_all('div', 't3')[0].contents).split("/")
        
        
        self.game_info.game_sched_info = game_sched_info.split("/")[0].strip()
        self.game_info.game_result = game_result
        self.game_info.game_location = game_loc_time[0].strip()
        self.game_info.game_date = game_loc_time[1].strip()
        self.game_info.game_time = game_loc_time[2].strip()
        self.game_info.temaA_name = self.teamA.team_name
        self.game_info.teamB_name = self.teamB.team_name
        
        
    def extract_game_score(self, team, soup):
        """
        """
        game_score = soup.find_all('td')
#         print score_team1
        assert team.team_name == ComUtils.get_utf8_value(game_score[0].contents)
        quarter_scores = []
        for cell in game_score[1:]:
            score = ComUtils.get_utf8_value(cell.contents)
            quarter_scores.append(score)
        team.quarter_scores = quarter_scores
#         print team.quarter_scores
    
    def generate_csv(self):
        pass
    

if __name__ == "__main__":
    """
    """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
    
    inst = ApalBoxScoreSpider(r"http://apal.linchen.com.tw/files/902-1000-3438-10000.php")
    inst.extract_target_data()
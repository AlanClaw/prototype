# -*- coding: UTF-8 -*-
'''# -*- coding: CP1252 -*-'''
import sys
if sys.version_info.major < 3:
    reload(sys)
sys.getdefaultencoding()

import logging
_logger = logging.getLogger(__name__)

import urllib2, os
from bs4 import BeautifulSoup

import xlwt

from ApalBoxScoreSpider import ApalBoxScoreSpider as ApalBoxScoreSpider
from ApalBoxScoreSpider import ApalPlayerAvgRecord as ApalPlayerAvgRecord 
from ApalBoxscoreWriter import ApalBoxscoreWriter as ApalBoxscoreWriter

class ApalBoxscoreManager(object):
    
    def __init__(self, apal_url):
        '''
        '''
        self.apal_url = apal_url
        self.workbooks = {}
        self.teams_avg_record = {}

    def run_flow(self):
        '''
        '''
        all_links = self.get_all_boxscore_link()
        
        # get all data write to workbook
        for link in all_links:
            print link
            boxscore_spider = ApalBoxScoreSpider(link)
            boxscore_spider.extract_target_data()
            
            boxscore_writer = ApalBoxscoreWriter()
            teamA_wb = self.get_write_book(boxscore_spider.teamA)
            teamB_wb = self.get_write_book(boxscore_spider.teamB)
            
            boxscore_writer.write_game_boxscore_to_sheet(teamA_wb,
                                                   boxscore_spider.teamA, 
                                                   boxscore_spider.teamB, 
                                                   boxscore_spider.game_info)
            
            boxscore_writer.write_game_boxscore_to_sheet(teamB_wb,
                                                   boxscore_spider.teamB, 
                                                   boxscore_spider.teamA,
                                                   boxscore_spider.game_info)

            teamA_avg_obj = self.get_team_avg_record_obj(boxscore_spider.teamA)
            teamB_avg_obj = self.get_team_avg_record_obj(boxscore_spider.teamB)
            self.add_player_data_to_avg_obj(teamA_avg_obj, boxscore_spider.teamA)
            self.add_player_data_to_avg_obj(teamB_avg_obj, boxscore_spider.teamB)

        # calculate avg PERCENTAGE_INDEX, write avg data to wb
        for team_name in self.teams_avg_record.keys():
            
            team_avg_obj = self.teams_avg_record.get(team_name)
            self.calculcate_player_avg_record(team_avg_obj)
            
            
            wb_file_name = team_name + u'.xls'.encode('utf-8')
            wb = self.workbooks.get(wb_file_name)
        
            boxscore_writer = ApalBoxscoreWriter()
            boxscore_writer.write_avg_data_to_sheet(wb, team_avg_obj)
        
        # write to xlxs file
        for file_name in self.workbooks.keys():

            wb = self.workbooks.get(file_name)
            
            record_fldr = "Records"
            if not os.path.exists(record_fldr):
                os.makedirs(record_fldr)
            
            cur_path = os.getcwd()
            file_path_base = os.path.join(cur_path, record_fldr)
            file_path = os.path.join(file_path_base, file_name)
            
            print file_path
            wb.save(file_path.decode('utf-8'))

    def get_file_name(self, team):
        '''
        '''
        return team.team_name + u'.xls'.encode('utf-8')
    
    
    def get_write_book(self, team):
        '''
        '''
        
        file_name = self.get_file_name(team)
    
        if not self.workbooks.has_key(file_name):
            wb = xlwt.Workbook(encoding="utf-8")
            self.workbooks[file_name] = wb
            
        return self.workbooks.get(file_name)
    
    def add_player_data_to_avg_obj(self, team_avg_obj, team_record):
        """
        @param team_avg_obj: player dict, {%player name%: ApalPlayerAvgRecord()...}
        @param team: TeamRecord()
        """
            
        for player in team_record.players:
            
            _logger.debug(player.data.get("Name"))
            _logger.debug(player.data.get("Number"))
            
            player_name = player.data.get("Name")
            player_num = player.data.get("Number")
            
            if not team_avg_obj.has_key(player_num):
                _logger.debug("Add player name %s" %player_name)
                team_avg_obj[player_num] = ApalPlayerAvgRecord(player_name, 
                                                                player_num)
                # initialize calculable value
                for index in ApalPlayerAvgRecord.CALCULABLE_DATA_INDEX:
                    record_name = ApalPlayerAvgRecord.DATA_KEY_LIST_MAPPING[index]
                    team_avg_obj.get(player_num).data[record_name] = \
                        int(team_avg_obj.get(player_num).data.get(record_name))
            
            if not player.DNP:
                # calculate player data
                team_avg_obj.get(player_num).GP += 1
                
                for index in ApalPlayerAvgRecord.CALCULABLE_DATA_INDEX:

                    record_name = ApalPlayerAvgRecord.DATA_KEY_LIST_MAPPING[index]

                    if index not in ApalPlayerAvgRecord.PERCENTAGE_INDEX:
                        _logger.debug(team_avg_obj.get(player_num).data.get(record_name))
                        _logger.debug(type(team_avg_obj.get(player_num).data.get(record_name)))
                        
                        team_avg_obj.get(player_num).data[record_name] += \
                            int(player.data.get(record_name).decode('utf-8'))
    
    def calculcate_player_avg_record(self, team_avg_obj):
        """
        """
        for player_avg_obj in team_avg_obj.values():
            player_avg_obj.calculate_average_record()
            player_avg_obj.calculcate_percentage_data()
            
    def get_team_avg_record_obj(self, team):
        '''
        '''
        
        team_name = team.team_name
        
        if not self.teams_avg_record.has_key(team_name):
            self.teams_avg_record[team_name] = {}
            
            for player in team.players:
                player_name = player.data.get("Name")
                player_num = player.data.get("Number")
                
                # set player's data
                self.teams_avg_record.get(team_name)[player_num] = ApalPlayerAvgRecord(player_name, 
                                                                                        player_num)
                
                player_avg_obj = self.teams_avg_record.get(team_name).get(player_num)
                
                # initialize calculable value
                for index in ApalPlayerAvgRecord.CALCULABLE_DATA_INDEX:
                    item = ApalPlayerAvgRecord.DATA_KEY_LIST_MAPPING[index]
                    player_avg_obj.data[item] = int(player_avg_obj.data.get(item))
                
        
        return self.teams_avg_record.get(team_name)
    
    def get_all_boxscore_link(self):
        '''
        '''
        all_links = []
        
        page = urllib2.urlopen(self.apal_url)
        
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), 'html5lib')
        
        game_table = soup.find_all('table', id='StageMatchListTable')[0]
        links = game_table.find_all('a')
        
        for link in links:
            all_links.append(link['href'])
            
        return all_links
    
if __name__ == "__main__":
    
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
    
    boxscore_generator = ApalBoxscoreManager(r'http://apal.linchen.com.tw/files/600-1000-177.php')
    boxscore_generator.run_flow()
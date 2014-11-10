# -*- coding: utf8 -*-
'''# -*- coding: CP1252 -*-'''
import logging
_logger = logging.getLogger(__name__)

import sys, traceback

import xlwt

from ApalBoxScoreSpider import ApalBoxScoreSpider as ApalBoxScoreSpider
from ApalBoxScoreSpider import ApalPlayerRecord as ApalPlayerRecord
from ApalBoxScoreSpider import ApalPlayerAvgRecord as ApalPlayerAvgRecord

class ApalBoxscoreWriter(object):
    
    def __init__(self):
        pass
        
        self.style_default = xlwt.easyxf('align: horiz center;')

    def write_game_info(self, w_sheet, x, y, game_info, team1, team2):
        # game info
        w_sheet.write(y, x, "Game Date", self.style_default)
        w_sheet.write(y, x + 1, unicode(game_info.game_date.decode('utf-8')), self.style_default)
        w_sheet.write(y + 1, x, "Game Location", self.style_default)
        w_sheet.write(y + 1, x + 1, unicode(game_info.game_location.decode('utf-8')), self.style_default)
        w_sheet.write(y + 2, x, "Opponents", self.style_default)
        w_sheet.write(y + 2, x + 1, unicode(game_info.teamB_name.decode('utf-8')), self.style_default)
        w_sheet.write(y + 5, x, team1.team_name.decode('utf-8'), self.style_default)
        w_sheet.write(y + 6, x, team2.team_name.decode('utf-8'), self.style_default)


    def write_game_result(self, w_sheet, x, y, team1, team2):
        # game and quarter result
        style_item = xlwt.easyxf('pattern: pattern solid, fore_colour light_orange;'
                                 'align: horiz center;')
        col_index_base = x + 1
        for index in range(len(team1.quarter_scores)):
            if index == (len(team1.quarter_scores) - 1): # TOTAL
                w_sheet.write(y, col_index_base + index, "TOTAL", style_item)
            elif index > 3: # OT
                w_sheet.write(y, col_index_base + index, "OT{0}".format(str(index - 3)), style_item)
            else:
                w_sheet.write(y, col_index_base + index, "Q{0}".format(str(index + 1)), style_item) # regular game time
            w_sheet.write(y+1, col_index_base + index, int(team1.quarter_scores[index].decode('utf-8')), self.style_default)
            w_sheet.write(y+2, col_index_base + index, int(team2.quarter_scores[index].decode('utf-8')), self.style_default)

    def write_player_record(self, w_sheet, team, x, y):
        
        # team name
        # 8887EB
        style_team = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                                 'align: horiz center;')
        w_sheet.write(y, x, team.team_name, style_team)
        
        assert team.players is not None
        
        # write item name
        # light_orange 
        style_item = xlwt.easyxf('pattern: pattern solid, fore_colour light_orange;'
                                 'align: horiz center;')
        x_tmp = x
        for record_name in ApalPlayerRecord.DATA_KEY_LIST_MAPPING:
            w_sheet.write(y+1, x_tmp, record_name, style_item)
            x_tmp += 1
        
        #initial percentage_style
        style_percentage = xlwt.easyxf('align: horiz center;', 
                                       num_format_str = "0.0%")
        
        # initial total record
        total_record = ApalPlayerRecord()
        for index in ApalPlayerRecord.CALCULABLE_DATA_INDEX:
            record_name = ApalPlayerRecord.DATA_KEY_LIST_MAPPING[index]
            total_record.data[record_name] = int(total_record.data.get(record_name))
        
        # write player data
        y_tmp = y+2
        for player in team.players:
            x_tmp = x
#             for record_name in ApalPlayerRecord().DATA_KEY_LIST_MAPPING:
            for index in range(len(ApalPlayerRecord.DATA_KEY_LIST_MAPPING)):
#                 print player.data.get(record_name)
                record_name = ApalPlayerRecord.DATA_KEY_LIST_MAPPING[index]
                
                if index == 2 and player.DNP:
                    w_sheet.write(y_tmp, x_tmp, "DNP", self.style_default)
                        
                elif index in ApalPlayerRecord.CALCULABLE_DATA_INDEX:
                    total_record.data[record_name] += int(player.data.get(record_name).decode('utf-8'))
                    
                    # deal with percentage display
                    if index in ApalPlayerRecord.PERCENTAGE_INDEX:
                        w_sheet.write(y_tmp, x_tmp, 
                                      float(player.data.get(record_name).decode('utf-8'))/100,
                                      style_percentage)
                    else:
                        w_sheet.write(y_tmp, x_tmp, 
                                      int(player.data.get(record_name).decode('utf-8')),
                                      self.style_default)
                elif index == 22:
                    # calculate EFF
#                     player.data["EFF"] = self._get_EFF_value(player)
                    player.calculcate_EFF_value()
                    w_sheet.write(y_tmp, x_tmp, int(player.data.get("EFF")), self.style_default)
                    
                else:
                    w_sheet.write(y_tmp, x_tmp, player.data.get(record_name).decode('utf-8'),
                                  self.style_default)
                    
                x_tmp += 1
            y_tmp += 1
        
        # deal with total percentage number
        total_record.calculcate_percentage_data()
            
        # write team total
        style_total = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;'
                                 'align: horiz center;')
        style_total_percentage = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;'
                                             'align: horiz center;', 
                                             num_format_str = "0.0%")
        
        w_sheet.write(y_tmp, x, u"Total".decode('utf-8'), style_total)
        x_tmp = x
        
        for index in range(len(ApalPlayerRecord.DATA_KEY_LIST_MAPPING)):
            record_name = ApalPlayerRecord.DATA_KEY_LIST_MAPPING[index]
            
            _logger.debug("total = {0}".format(total_record.data.get(record_name)))
            
            if index in ApalPlayerRecord.PERCENTAGE_INDEX:
                w_sheet.write(y_tmp, x_tmp+index, 
                              total_record.data.get(record_name),
                              style_total_percentage)
            
            elif index in ApalPlayerRecord.CALCULABLE_DATA_INDEX:
                w_sheet.write(y_tmp, x_tmp+index, total_record.data.get(record_name), style_total)
    
    def write_game_boxscore_to_sheet(self, write_book, team1, team2, game_info):
        '''
        '''        
        sheet_name = u"{0} vs {1}".format(team1.team_name.decode('utf-8'),
                                          team2.team_name.decode('utf-8'))
        
        try:
            write_sheet = write_book.add_sheet(sheet_name, cell_overwrite_ok = True)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            write_sheet = None
        
        if write_sheet is not None:
            # write all the game data to the specific w_sheet
            x = 1
            y = 1
    
            # Need 2*3 rectangle        
            self.write_game_info(write_sheet, x, y, game_info, team1, team2)
            
            # Need 3*(5+n) rectangle
            self.write_game_result(write_sheet, x, y+4, team1, team2)
    
            # 
            self.write_player_record(write_sheet, team1, x, y+9)
            shift = len(team1.players) + 5
            self.write_player_record(write_sheet, team2, x, y+9+shift)

    
    def write_avg_data_to_sheet(self, write_book, team_avg_obj):
        """
        @param team_avg_obj: ApalPlayerAvgRecord()
        @param write_book: xlwt.Workbook(encoding="utf-8")
        """
        sheet_name = u"Average Record"
    
        try:
            write_sheet = write_book.add_sheet(sheet_name, cell_overwrite_ok = True)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            write_sheet = None
    
        if write_sheet is not None:
            x = 1
            y = 1
            
            self._write_player_avg_data(write_sheet, team_avg_obj, x, y)
            
    def _write_player_avg_data(self, w_sheet, team_avg_obj, x, y):
        """
        @param team_avg_obj: ApalPlayerAvgRecord()
        @param w_sheet: xlwt.Workbook(encoding="utf-8")
        """
        # light_orange 
        style_item = xlwt.easyxf('pattern: pattern solid, fore_colour light_orange;'
                                 'align: horiz center;')
        
        #initial percentage_style
        style_avg = xlwt.easyxf('align: horiz center;', 
                                num_format_str = "0.0")
        
        style_percentage = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;'
                                             'align: horiz center;', 
                                             num_format_str = "0.0%")
        
        # write item name
        x_tmp = x
        for record_name in ApalPlayerRecord().DATA_KEY_LIST_MAPPING:
            if not cmp(record_name, "Starter"):
                w_sheet.write(y+1, x_tmp, "GP", style_item)
            else:
                w_sheet.write(y+1, x_tmp, record_name, style_item)
            x_tmp += 1

        y_tmp = y+2
        
        for player_avg_obj in team_avg_obj.values():
            
            x_tmp = x
#             for record_name in ApalPlayerRecord().DATA_KEY_LIST_MAPPING:
            for index in range(len(ApalPlayerAvgRecord.DATA_KEY_LIST_MAPPING)):
                
                record_name = ApalPlayerRecord.DATA_KEY_LIST_MAPPING[index]
                if not cmp(record_name, "Starter"):
                    w_sheet.write(y_tmp, x_tmp, 
                              player_avg_obj.GP,
                              self.style_default)
                    
                elif index in ApalPlayerAvgRecord.PERCENTAGE_INDEX:
                    w_sheet.write(y_tmp, x_tmp, 
                                  player_avg_obj.data.get(record_name),
                                  style_percentage)
                else:
                    w_sheet.write(y_tmp, x_tmp, 
                                  player_avg_obj.data.get(record_name),
                                  style_avg)
                
                x_tmp += 1
            
            player_avg_obj.calculcate_EFF_value()
            index_of_EFF = 22
            w_sheet.write(y_tmp, x+index_of_EFF, 
                          player_avg_obj.data.get('EFF'),
                          style_avg)
            
            y_tmp += 1
    
    def _get_EFF_value(self, player):
        '''
        '''
        '''
        (PTS + TRB + AST + STL + BLK) -(FGA-FGM)-(FTA-FTM)-TO
        '''
        
        EFF = (int(player.data.get("PT")) + int(player.data.get("REB")) + \
               int(player.data.get("AST")) + int(player.data.get("STL")) + \
               int(player.data.get("BLK"))) - \
               (( int(player.data.get("3FGA")) + int(player.data.get("FGA"))) - \
                ( int(player.data.get("3FGM")) + int(player.data.get("FGM")))) - \
                (int(player.data.get("FTA"))-int(player.data.get("FTM"))) - \
                int(player.data.get("TOV"))
        
        return EFF
    
    def get_sheet_index_by_name(self, read_workbook, sheet_name):
        '''
        @return: return index of the sheet name, or return -1 if no one match
        '''
        index = -1
        
        for sheet in read_workbook.sheets():
            index += 1
#             _logger.debug(sheet_name.encode('utf-8'))
            if unicode(sheet.name).encode('utf-8') == unicode(sheet_name).encode('utf-8'):
                _logger.debug('sheet: {0}, index: {1}'.format(unicode(sheet_name).encode('utf-8'), 
                                                              str(index)))
                return index
        return -1
    
    def is_sheet_exist(self, read_workbook, sheet_name):
        '''
        '''
        for sheet in read_workbook.sheets():
            if sheet.name == sheet_name:
                _logger.debug('sheet exist')
                _logger.debug(sheet.name)
                return True
        return False

if __name__ == '__main__':
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )

    apal_spider = ApalBoxScoreSpider(r"http://apal.linchen.com.tw/files/902-1000-3438-10000.php")
    apal_spider.extract_target_data()
    
#     print apal_spider.teamA.team_name, apal_spider.teamB.team_name, apal_spider.game_info
#     
#     print apal_spider.game_info.game_sched_info
#     print apal_spider.game_info.game_location
#     print apal_spider.game_info.game_date
#     print apal_spider.game_info.game_time
#     print apal_spider.game_info.game_date + ' ' + \
#           apal_spider.teamA.team_name + " vs. " + apal_spider.teamB.team_name
    
    apal_data_writer = ApalBoxscoreWriter()
    apal_data_writer.write_game_info_to_xls(apal_spider.teamA, apal_spider.teamB, 
                                            apal_spider.game_info)
    apal_data_writer.write_game_info_to_xls(apal_spider.teamB, apal_spider.teamA, 
                                            apal_spider.game_info)
    
    apal_spider2 = ApalBoxScoreSpider(r"http://apal.linchen.com.tw/files/902-1000-3440-10000.php")
    apal_spider2.extract_target_data()
    apal_data_writer2 = ApalBoxscoreWriter()
    apal_data_writer2.write_game_info_to_xls(apal_spider2.teamA, apal_spider2.teamB, 
                                            apal_spider2.game_info)
    apal_data_writer2.write_game_info_to_xls(apal_spider2.teamB, apal_spider2.teamA, 
                                            apal_spider2.game_info)
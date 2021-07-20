"""Copyright since 2020, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""
import pandas as pd

from datetime import datetime, timedelta
from typing import Union, List, NamedTuple, Optional, Any, Callable, Dict, Iterable
from io import BytesIO
from functools import reduce
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.format import Format

from osci.datalake import DataLake
from osci.datalake.schemas.public import OSCIChangeRankingExcelSchema, OSCIChangeRankingSchema

Row = int
Column = int
Rule = Dict[str, Any]

STAR_STAR_SUPERSCRIPT = '*'
NUMBER_SUPERSCRIPT: Callable[[int], str] = lambda num: str(num)


def reduce_rules(rules: Iterable[Rule]) -> Rule:
    def _merge_rules(left: Rule, right: Rule) -> Rule:
        return {**left, **right}

    if rules:
        return reduce(_merge_rules, rules)
    return {}


class Position(NamedTuple):
    row: Row
    col: Column


class TableColumn(NamedTuple):
    name: str
    superscript_suffix: Optional[str]
    df_key: str
    format_rule: Rule
    cell_scale: Optional[Union[int, float]]


class OSCIChangeExcelWriter:
    schema = OSCIChangeRankingExcelSchema

    plus_minus_format_rule: Rule = {'num_format': '+0;-0;—'}
    numbers_format_rule: Rule = {'num_format': '0'}
    superscript_format_rule: Rule = {'font_script': 1}
    bold_format_rule: Rule = {'bold': True}
    blue_font_color_rule: Rule = {'font_color': '#2E75B5'}
    align_center_rule: Rule = {'align': 'center'}

    @staticmethod
    def border_rule_fabric(border_size: int) -> Dict[str, int]:
        return {'border': border_size}

    border_rule_1: Rule = {'border': 1}

    position_change_format_rule: Rule = reduce_rules((border_rule_1,
                                                      bold_format_rule,
                                                      blue_font_color_rule,
                                                      plus_minus_format_rule,
                                                      align_center_rule))

    change_format_rule: Rule = reduce_rules((border_rule_1,
                                             blue_font_color_rule,
                                             plus_minus_format_rule))

    number_cell_format_rule: Rule = reduce_rules((border_rule_1, numbers_format_rule))

    table_columns: List[TableColumn] = [
        TableColumn(schema.position, None,
                    schema.position, reduce_rules((border_rule_1, bold_format_rule, align_center_rule)),
                    cell_scale=5),
        TableColumn(schema.position_change, STAR_STAR_SUPERSCRIPT,
                    OSCIChangeRankingSchema.position_change, position_change_format_rule,
                    cell_scale=1.2),
        TableColumn(schema.company, None,
                    OSCIChangeRankingSchema.company, border_rule_1,
                    cell_scale=4),
        TableColumn(schema.active, NUMBER_SUPERSCRIPT(1),
                    OSCIChangeRankingSchema.active, number_cell_format_rule,
                    cell_scale=1.2),
        TableColumn(schema.change_suffix, STAR_STAR_SUPERSCRIPT,
                    OSCIChangeRankingSchema.active_change, change_format_rule,
                    cell_scale=1.2),
        TableColumn(schema.total, NUMBER_SUPERSCRIPT(2),
                    OSCIChangeRankingSchema.total, number_cell_format_rule,
                    cell_scale=1.2),
        TableColumn(schema.change_suffix, STAR_STAR_SUPERSCRIPT,
                    OSCIChangeRankingSchema.total_change, change_format_rule,
                    cell_scale=1.2)
    ]

    def __init__(self, sheet_name: str, from_date: datetime, to_date: datetime, top_size: int):
        self.writer, self.buffer = DataLake().public.get_excel_writer()
        self.workbook: Workbook = self.writer.book
        self.worksheet: Worksheet = self.workbook.add_worksheet(sheet_name)
        self.from_date = from_date
        self.to_date = to_date
        self.top_size = top_size

        self.superscript_format = self.get_format(self.superscript_format_rule)

    def get_format(self, *rules: Rule) -> Format:
        return self.workbook.add_format(reduce_rules(rules))

    def write(self, df):
        header_position = Position(0, 1)
        table_header_position = Position(header_position.row + 2, header_position.col)
        comments_position = Position(table_header_position.row + 1,
                                     table_header_position.col + len(self.table_columns) + 1)

        table_position = Position(table_header_position.row + 1, table_header_position.col)
        self._write_header(position=header_position)
        self._write_table_header(start_from=table_header_position)
        self._write_comments(start_from=comments_position)
        self._write_table(df, start_from=table_position)

    def _write_header(self, position: Position = Position(0, 1)):
        self.worksheet.write(*position,
                             f'{self.from_date:%Y} (differences from {self.from_date:%B, %d} to {self.to_date:%B, %d})')

    def _write_comments(self, start_from: Position = Position(3, 9)):
        row = start_from.row
        self.worksheet.write_rich_string(row, start_from.col,
                                         self.superscript_format, NUMBER_SUPERSCRIPT(1),
                                         ' Active Contributors are those who authored 10 '
                                         'or more pushes in the time period')
        row += 1
        self.worksheet.write_rich_string(row, start_from.col,
                                         self.superscript_format, NUMBER_SUPERSCRIPT(2),
                                         ' Total Community counts those who authored 1 '
                                         'or more pushes in the time period')
        row += 1
        self.worksheet.write_rich_string(row, start_from.col,
                                         self.superscript_format, STAR_STAR_SUPERSCRIPT,
                                         ' Changes are relative to the metrics at the end of the previous month')
        row += 2
        self.worksheet.write(row, start_from.col,
                             f'The top {self.top_size} is calculated using the Active Contributors metric')
        row += 1
        self.worksheet.write(row, start_from.col,
                             'If two companies have equal Active Contributors, '
                             'their relative positions are determined by Total Community')

    def _write_table_header(self, start_from: Position):
        row, col = start_from
        header_format = self.get_format(self.border_rule_1, self.bold_format_rule)
        superscript_format = self.get_format(self.bold_format_rule, self.superscript_format_rule)
        border_format = self.get_format(self.border_rule_1)
        center_header_format = self.get_format(self.border_rule_1, self.bold_format_rule, self.align_center_rule)

        for table_column in self.table_columns:
            if table_column.superscript_suffix:
                self.worksheet.write_rich_string(row, col, header_format, table_column.name,
                                                 superscript_format, table_column.superscript_suffix, border_format)
            else:
                self.worksheet.write(row, col, table_column.name,
                                     center_header_format
                                     if table_column.name in {self.schema.position, self.schema.position_change}
                                     else header_format)
            col_width = len(table_column.name) * table_column.cell_scale
            self.worksheet.set_column(col, col, width=col_width)
            col += 1

    def _write_table(self, df: pd.DataFrame, start_from: Position):
        row, start_col = start_from
        for record in df.head(self.top_size).to_dict('records'):
            col = start_col
            for table_column in self.table_columns:
                self.worksheet.write(row, col, record[table_column.df_key], self.get_format(table_column.format_rule))
                col += 1
            row += 1

    def save(self) -> BytesIO:
        self.writer.save()
        return self.buffer


class OSCIChangeRankingExcel:
    schema = OSCIChangeRankingExcelSchema
    base_name = 'OSCI_Ranking'
    dir_name = 'SolutionsHub_OSCI_change_ranking'

    def __init__(self, to_date: datetime, from_date: Optional[datetime] = None, rows_limit: int = 100):
        self.from_date = from_date if from_date else self.get_previous_date(date=to_date)
        self.to_date = to_date
        self.rows_limit = rows_limit

    @staticmethod
    def get_previous_date(date: datetime):
        if date.month == 1:
            return datetime(year=date.year, month=date.month, day=1)
        return datetime(year=date.year, month=date.month, day=1) - timedelta(days=1)

    @property
    def name(self) -> str:
        return DataLake().public.get_osci_change_excel_report_name(base_report_name=self.base_name,
                                                                   date=self.to_date)

    @property
    def url(self) -> str:
        return DataLake().public.get_osci_change_excel_report_url(base_report_name=self.base_name,
                                                                  report_dir_name=self.dir_name,
                                                                  date=self.to_date)

    @property
    def path(self) -> str:
        return DataLake().public.get_osci_change_excel_report_path(base_report_name=self.base_name,
                                                                   report_dir_name=self.dir_name,
                                                                   date=self.to_date)

    def save(self, df: pd.DataFrame):
        DataLake().public.write_bytes_to_file(path=self.path,
                                              buffer=self._write(df))

    def _write(self, change_ranking_df: pd.DataFrame) -> BytesIO:
        writer = OSCIChangeExcelWriter(sheet_name=self.base_name,
                                       from_date=self.from_date,
                                       to_date=self.to_date,
                                       top_size=self.rows_limit)

        df = change_ranking_df.reset_index().rename(columns={OSCIChangeRankingSchema.position: self.schema.position})
        df[self.schema.position] += 1
        df[self.schema.position_change] *= -1
        df = df.fillna(0)

        writer.write(df)
        return writer.save()

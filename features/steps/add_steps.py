from behave import *

use_step_matcher("re")


def data_from_table(context):
    return [
        {head: row[head] for head in context.table.headings if row[head]}
        for row in context.table.rows
        ]
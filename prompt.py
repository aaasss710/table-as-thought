import pandas as pd
import json
import matplotlib.pyplot as plt
import ast
import math
def serialize_dataframe(df, use_brackets=False, use_row_labels=True):
    # Serialize column names
    df.columns = [str(col) for col in df.columns]
    columns_str = ', '.join(df.columns)
    
    # Serialize each row
    if use_brackets:
        row_format = '[' + ', '.join(['{}'] * len(df.columns)) + ']'
    else:
        row_format = ', '.join(['{}'] * len(df.columns))
    
    rows = [row_format.format(*map(str, row)) for _, row in df.iterrows()]
    
    if use_row_labels:
        row_labels = ['[ROW{}]'.format(i+1) for i in range(len(df))]
        rows_str = ', '.join(['{}, {}'.format(label, row) for label, row in zip(row_labels, rows)])
    else:
        rows_str = ', '.join(rows)
    
    # Combine the serialized column names and rows
    serialized_str = columns_str + ', ' + rows_str
    
    return serialized_str


def serialize_dataframe_to_json(df, mode='column_centric'):
    if mode == 'column_centric':
        data_dict = df.to_dict(orient='list')
        return json.dumps(data_dict)
    
    elif mode == 'row_centric':
        row_dicts = [{"row": idx, **row.to_dict()} for idx, row in df.iterrows()]
        return json.dumps(row_dicts, indent=4)
    
    else:
        raise ValueError("Invalid mode. Choose either 'column_centric' or 'row_centric'.")
    
def serialize_dataframe_to_bracket(df):
    # First list is the column names
    serialized = [list(df.columns)]
    
    # Then add each row as a list
    for _, row in df.iterrows():
        serialized.append(list(row))
    
    return serialized


# def visualize_table_dark(data, col_labels, highlighted_cells=None, highlight_row=False, highlight_column=False)->plt.Figure:
#     """
#     Visualizes a table with a darker and clearer color scheme.
    
#     Parameters:
#     - data: List of lists containing table data.
#     - col_labels: List containing column labels.
#     - highlighted_cells: List of cell indices to be highlighted.
#     - highlight_row: Boolean, if True, colors each row uniformly with distinct colors.
#     - highlight_column: Boolean, if True, colors each column uniformly with distinct colors.
    
#     Returns:
#     - A matplotlib plot with the visualized table.
#     """
#     # Set up the figure and axes
#     fig, ax = plt.subplots(figsize=(12, 8))
    
#     # Hide axes
#     ax.axis('off')
#     ax.axis('tight')

#     # Table from data
#     table = ax.table(cellText=data, colLabels=col_labels, cellLoc='center', loc='center')
    
#     # Generate a list of colors
#     num_rows, num_cols = len(data), len(data[0])
#     colors = plt.cm.Dark2.colors

#     for i, key in enumerate(table.get_celld().keys()):
#         cell = table[key]
#         cell.set_fontsize(12)
#         if key[0] == 0:
#             cell.set_fontsize(14)
#             cell.set_text_props(weight='bold')
#             cell.set_facecolor("#333333")
#             cell.set_text_props(color="white")
#         else:
#             cell.set_facecolor("#555555")
#             cell.set_text_props(color="black")
            
#             # Row-wise coloring
#             if highlight_row:
#                 cell.set_facecolor(colors[key[0] % len(colors)])
            
#             # Column-wise coloring
#             if highlight_column:
#                 cell.set_facecolor(colors[key[1] % len(colors)])
#             if not highlight_row and not highlight_column:
#                 cell.set_facecolor("#ffffff")
#         # Specific cell highlighting (overrides row/column coloring)
#         if highlighted_cells and list(key) in highlighted_cells:
#             cell.set_facecolor("#ffff00")
        
#         cell.set_edgecolor('black')

#     # Adjust table proportions
#     table.auto_set_font_size(False)
#     table.auto_set_column_width(col=list(range(len(col_labels))))
#     table.scale(1.2, 1.2)

#     return fig


def get_real_row(row, list_num_rows):
    real_row = 0
    
    while row>=0:
        try:
            row -= list_num_rows[real_row]
        except IndexError:
            print(row, list_num_rows)
        if row>=0:
            real_row += 1
    return real_row

def is_in_cell(row, list_num_rows):
    for num_rows in list_num_rows:
        if row==0:
            return False
        row-=num_rows
    return True


def visualize_table_dark(full_data, picture_save_path,   highlighted_cells=None, highlight_row=False, highlight_column=False)->plt.Figure:
    """
    Visualizes a table with a darker and clearer color scheme.
    
    Parameters:
    - full_data: List of lists containing table data and column labels.
    - highlighted_cells: List of cell indices to be highlighted.
    - highlight_row: Boolean, if True, colors each row uniformly with distinct colors.
    - highlight_column: Boolean, if True, colors each column uniformly with distinct colors.
    
    Returns:
    - A matplotlib plot with the visualized table.
    """
    max_char_per_line = 200//len(full_data[0])
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Hide axes
    ax.axis('off')
    ax.axis('tight')
    list_num_rows = []
    all_split_rows = []
    for row in full_data:
        if any (len(str(cell)) > max_char_per_line for cell in row):
            num_rows_split =  max(math.ceil(len(str(cell)) / max_char_per_line) for cell in row)
            list_num_rows.append(num_rows_split) 
            rows_split = [[] for _ in range(num_rows_split)]
            for cell in row:
                cell = str(cell)
                num_cells_split = math.ceil(len(cell) / max_char_per_line)
                for i in range(num_cells_split):
                    rows_split[i].append(cell[i*max_char_per_line:min((i+1)*max_char_per_line, len(cell))])
                for i in range(num_cells_split, num_rows_split):
                    rows_split[i].append(' ')
            all_split_rows.extend(rows_split)
        else:
            list_num_rows.append(1)
            all_split_rows.append(row)       
                
    num_column = max(len(row) for row in all_split_rows)
    for i, row in enumerate(all_split_rows):
        if len(row) < num_column:
            row.extend([' ']*(num_column-len(row)))
            all_split_rows[i] = row
    
    table = ax.table(cellText=all_split_rows,  cellLoc='center', loc='center')
    # table = ax.table(cellText=wrapped_data, colLabels=wrapped_col_labels, cellLoc='center', loc='center')

    
    # Generate a list of colors
    num_rows, num_cols = len(full_data), len(full_data[0])
    colors = plt.cm.Dark2.colors
    last_real_row = None
    face_color = "white"
    for i, key in enumerate(table.get_celld().keys()):
        # print(key)
        cell = table[key]
        cell.set_fontsize(12)
        real_row = get_real_row(key[0], list_num_rows)
        
        if real_row == 0:
            cell.set_fontsize(14)
            cell.set_text_props(weight='bold')
            cell.set_facecolor("white")
            cell.set_text_props(color="black")
        else:
            cell.set_facecolor("#555555")
            cell.set_text_props(color="black")
            
            # Row-wise coloring
            if highlight_row:
                face_color = colors[(real_row ) % len(colors)]
                cell.set_facecolor(face_color)
            
            # Column-wise coloring
            if highlight_column:
                face_color = colors[key[1] % len(colors)]
                cell.set_facecolor(face_color)
            if not highlight_row and not highlight_column:
                cell.set_facecolor("#ffffff")
        # Specific cell highlighting (overrides row/column coloring)
        # if highlighted_cells and list((real_row, key[1])) in highlighted_cells:
        #     face_color = "#ffff00"
        #     cell.set_facecolor(face_color)
        
        
        if not highlighted_cells and not highlight_row and not highlight_column:
            cell.set_edgecolor('black')
            
            if key[0] == sum(list_num_rows) - 1 :
                if  is_in_cell(key[0], list_num_rows):
                    cell.visible_edges = 'LRB'
            elif  is_in_cell(key[0], list_num_rows):
                cell.visible_edges = 'vertical'
            else:
                cell.visible_edges = 'LRT'
        else:
            
            cell.set_edgecolor(face_color)
        if highlighted_cells:
            if list((real_row, key[1])) in highlighted_cells: 
                face_color = "#ffff00"
                cell.set_facecolor(face_color)
                cell.set_edgecolor(face_color)    
            else: 
                cell.set_edgecolor('black')
            
                if key[0] == sum(list_num_rows) - 1:
                    cell.visible_edges = 'LRB'
                elif  is_in_cell(key[0], list_num_rows):
                    cell.visible_edges = 'vertical'
                else:
                    cell.visible_edges = 'LRT'
            #     cell.set_linewidth([1.0, 1.0, 1.0, 1.0])
        # if real_row == 0 and key[1] > 0:
        #     cell.visible_edges = 'LR'
            
            # # cell._tc['top'].set_color('none')
            # cell.set_linewidth([1.0, 1.0, 0.0, 1.0])
            
        # else:
        #     # cell.visible_edges = 'open'
        #     cell.visible_edges = 'T'
        #     last_real_row = real_row
    # Adjust table proportions
    table.auto_set_font_size(False)
    table.auto_set_column_width(col=list(range(len(full_data[0]))))
    table.scale(1.2, 1.2)

    plt.savefig(picture_save_path, bbox_inches='tight')

def string_to_table(input_string):
    # Splitting the string into key-value pairs based on ', '
    pairs = input_string.split(', ')

    # Splitting each pair into key and value based on '[' and removing the closing ']'
    data = [pair.split('[') for pair in pairs]
    data = [(key, value.rstrip(']')) for key, value in data]

    # Creating a table-like structure (a dictionary in this case)
    table = {key: value for key, value in data}

    return table


def make_highted_cells_prompt(table_array, highlighted_cells):
    """
    Make a prompt for highlighted cells.
    table_array: a 2D array
    highlighted_cells: a list of tuples, each tuple is a cell index (row, column), note that the index of row starts from 1, which
    is the same as the index in the array where the first row represents the column names."""
    
    array_str_highlighted_cells = [' (row ' + str(cell[0] - 1) + ', column ' + str(cell[1])+ ', '+ str(table_array[cell[0]][cell[1]]) + '),' for cell in highlighted_cells]
    str_highlighted_cells = ''.join(array_str_highlighted_cells)
    prompt_higlight_cells = ' Please pay attention to the highlighted cells: ' + str_highlighted_cells + ' \n'    
    return prompt_higlight_cells
    
def make_prompt(prompt, table_df, basicprompt, prompt_CoT = None, prompt_higlight_cells = None, prompt_expert= None):
    prompt['Linearized_no_row_sign'] = basicprompt + serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
    prompt['Linearized_with_row_sign'] = basicprompt + serialize_dataframe(table_df, use_brackets=False, use_row_labels=True)
    prompt['json_column_centric'] = basicprompt + serialize_dataframe_to_json(table_df, mode='column_centric')
    prompt['json_row_centric'] = basicprompt + serialize_dataframe_to_json(table_df, mode='row_centric')
    prompt['bracket_format'] = basicprompt + str(serialize_dataframe_to_bracket(table_df))
    if prompt_CoT:
        prompt['CoT_Linearized_no_row_sign'] = basicprompt + prompt_CoT + serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
        prompt['CoT_Linearized_with_row_sign'] = basicprompt + prompt_CoT + serialize_dataframe(table_df, use_brackets=False, use_row_labels=True)
        prompt['CoT_json_column_centric'] = basicprompt + prompt_CoT + serialize_dataframe_to_json(table_df, mode='column_centric')
        prompt['CoT_json_row_centric'] = basicprompt + prompt_CoT + serialize_dataframe_to_json(table_df, mode='row_centric')
        prompt['CoT_bracket_format'] = basicprompt + prompt_CoT + str(serialize_dataframe_to_bracket(table_df))
    if prompt_higlight_cells:
        prompt['highlighted_cells_Linearized_no_row_sign'] = basicprompt + prompt_higlight_cells + serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
        prompt['highlighted_cells_Linearized_with_row_sign'] = basicprompt + prompt_higlight_cells + serialize_dataframe(table_df, use_brackets=False, use_row_labels=True)
        prompt['highlighted_cells_json_column_centric'] = basicprompt + prompt_higlight_cells + serialize_dataframe_to_json(table_df, mode='column_centric')
        prompt['highlighted_cells_json_row_centric'] = basicprompt + prompt_higlight_cells + serialize_dataframe_to_json(table_df, mode='row_centric')
        prompt['highlighted_cells_bracket_format'] = basicprompt + prompt_higlight_cells + str(serialize_dataframe_to_bracket(table_df))
    if prompt_expert:
        prompt['expert_Linearized_no_row_sign'] = prompt_expert + basicprompt +  serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
        prompt['expert_Linearized_with_row_sign'] = prompt_expert + basicprompt +  serialize_dataframe(table_df, use_brackets=False, use_row_labels=True)
        prompt['expert_json_column_centric'] = prompt_expert + basicprompt +  serialize_dataframe_to_json(table_df, mode='column_centric')
        prompt['expert_json_row_centric'] = prompt_expert + basicprompt +  serialize_dataframe_to_json(table_df, mode='row_centric')
        prompt['expert_bracket_format'] = prompt_expert + basicprompt +  str(serialize_dataframe_to_bracket(table_df))
    return prompt

def make_tuple_prompt(prompt, table_df, basicprompt, prompt_CoT = None, prompt_higlight_cells = None, prompt_expert= None):
    prompt['Linearized_no_row_sign'] = basicprompt + serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
    prompt['json_column_centric'] = basicprompt + serialize_dataframe_to_json(table_df, mode='column_centric')
    prompt['json_row_centric'] = basicprompt + serialize_dataframe_to_json(table_df, mode='row_centric')
    prompt['bracket_format'] = basicprompt + str(serialize_dataframe_to_bracket(table_df))
    if prompt_CoT:
        prompt['CoT_Linearized_no_row_sign'] = basicprompt + prompt_CoT + serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
        prompt['CoT_json_column_centric'] = basicprompt + prompt_CoT + serialize_dataframe_to_json(table_df, mode='column_centric')
        prompt['CoT_json_row_centric'] = basicprompt + prompt_CoT + serialize_dataframe_to_json(table_df, mode='row_centric')
        prompt['CoT_bracket_format'] = basicprompt + prompt_CoT + str(serialize_dataframe_to_bracket(table_df))
    if prompt_higlight_cells:
        prompt['highlighted_cells_Linearized_no_row_sign'] = basicprompt + prompt_higlight_cells + serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
        prompt['highlighted_cells_json_column_centric'] = basicprompt + prompt_higlight_cells + serialize_dataframe_to_json(table_df, mode='column_centric')
        prompt['highlighted_cells_json_row_centric'] = basicprompt + prompt_higlight_cells + serialize_dataframe_to_json(table_df, mode='row_centric')
        prompt['highlighted_cells_bracket_format'] = basicprompt + prompt_higlight_cells + str(serialize_dataframe_to_bracket(table_df))
    if prompt_expert:
        prompt['expert_Linearized_no_row_sign'] = prompt_expert + basicprompt +  serialize_dataframe(table_df, use_brackets=False, use_row_labels=False)
        prompt['expert_json_column_centric'] = prompt_expert + basicprompt +  serialize_dataframe_to_json(table_df, mode='column_centric')
        prompt['expert_json_row_centric'] = prompt_expert + basicprompt +  serialize_dataframe_to_json(table_df, mode='row_centric')
        prompt['expert_bracket_format'] = prompt_expert + basicprompt +  str(serialize_dataframe_to_bracket(table_df))
    return prompt
import re

def parse_list_of_lists(input_str):
    # Remove surrounding brackets and split by '], ['
    lists = re.split(r'\], \[', input_str.strip('[]'))
    
    result = []
    for lst in lists:
        # Split by comma, accounting for commas inside quotes
        elements = re.split(r', (?=(?:[^\'"]|\'[^\']*\'|"[^"]*")*$)', lst)
        
        parsed_elements = []
        for el in elements:
            el = el.strip('\'"')  # Remove surrounding quotes if present
            
            # Convert '[[]]' to an actual empty list
            if el == '[[]]':
                parsed_elements.append([])
            elif el.replace('.', '', 1).isdigit():
                parsed_elements.append(float(el) if '.' in el else int(el))
            elif el == 'nan':
                parsed_elements.append(None)
            else:
                parsed_elements.append(el)
        
        result.append(parsed_elements)
    
    return result


def extract_nested_brackets_as_list(input_string)->(list, str):
    """
    Extracts and converts the content within the first nested set of square brackets in the input string into a Python list.

    Parameters:
    input_string (str): The string from which to extract and convert the content.

    Returns:
    list: The extracted content within the first nested brackets as a Python list.
    str: The input string with the extracted content removed.

    """
    # Finding the first occurrence of '[[' and the corresponding closing ']]'
    opening_bracket = input_string.find('[[')
    if opening_bracket != -1:
        # Start searching for closing bracket after the opening bracket
        closing_bracket = input_string.rfind(']]', opening_bracket)
        if closing_bracket != -1:
            # Extracting the content
            content = input_string[opening_bracket:closing_bracket + 2]
            
            # print(content)
            # print(input_string.replace(content, ''))
            return parse_list_of_lists(content), input_string.replace(content, '')
            # try:
            #     # Converting the string representation of the list into a Python list
            #     # also return the prompt without content 
            #     return ast.literal_eval(content), input_string.replace(content, '')
            # except:
            #     print(content)
            #     assert False,  "Invalid format for conversion to a list." 
    assert False,  "No nested brackets found."


def generate_unique_name(picture_folder):
    """
    Save the picture with a unique name in the picture_folder
    """
    import uuid
    import os
    unique_filename = str(uuid.uuid4())
    try_count = 0
    while os.path.exists(os.path.join(picture_folder, unique_filename + '.png')):
        unique_filename = str(uuid.uuid4())
        try_count += 1
        assert  try_count < 100, "cannot find a unique name for the picture"
    picture_path = os.path.join(picture_folder, unique_filename + '.png')
    # picture.savefig(picture_path)
    return picture_path


def make_vision_prompt(prompt, picture_folder):
    
    table_df = None
    if 'bracket_format' in prompt:
        string_with_brackets = prompt['bracket_format']
        table_array, prompt_without_table = extract_nested_brackets_as_list(string_with_brackets)
        try:
            table_df = pd.DataFrame(table_array[1:], columns=table_array[0])
        except ValueError:
            print('The table cannot be converted to a DataFrame. It may be of inconsistent length.')
            print('The table_array is: {}'.format(table_array))
            print('The prompt is: {}'.format(string_with_brackets))  
    assert table_df is not None, "cannot find the table, please provide the prompt that contain the bracket of format table or the table_df"
    black_white_fig_path = generate_unique_name(picture_folder)
    high_light_column_fig_path = generate_unique_name(picture_folder)
    high_light_row_fig_path = generate_unique_name(picture_folder)
    black_white_fig = visualize_table_dark(table_array, black_white_fig_path)
    high_light_column_fig = visualize_table_dark(table_array,high_light_column_fig_path,  highlight_column=True)
    high_light_row_fig = visualize_table_dark(table_array,high_light_row_fig_path,  highlight_row=True)
    
    if 'highlighted_cells' in prompt:
        highlighted_cells = prompt['highlighted_cells']
        high_light_cell_fig_path = generate_unique_name(picture_folder)
        high_light_cell_fig = visualize_table_dark(table_array, high_light_cell_fig_path,  highlighted_cells=highlighted_cells)
        
    # find all of the keys that contain 'bracket_format', then remove the 'bracket_format' from the key and 'vision' to the key
    bracket_format_keys = [key for key in prompt.keys() if 'bracket_format' in key and 'result' not in key]
    for key in bracket_format_keys:
        bracket_prompt = prompt[key]
        # print(bracket_prompt)
        pure_key = key.replace('bracket_format', '')
        table_array, prompt_without_table = extract_nested_brackets_as_list(bracket_prompt)
        # replace everything between the first '[[]' and the last ']]' with the vision prompt
        prompt['vision_black_white' + pure_key] = {}
        prompt['vision_black_white' + pure_key]['prompt'] = prompt_without_table + ' Please look at table in the picture below. '
        prompt['vision_black_white' + pure_key]['figure_path'] = black_white_fig_path
        prompt['vision_high_light_column' + pure_key] = {}
        prompt['vision_high_light_column' + pure_key]['prompt'] = prompt_without_table + ' Please look at table in the picture below. '
        prompt['vision_high_light_column' + pure_key]['figure_path'] = high_light_column_fig_path
        prompt['vision_high_light_row' + pure_key] = {}
        prompt['vision_high_light_row' + pure_key]['prompt'] = prompt_without_table + ' Please look at table in the picture below. '
        prompt['vision_high_light_row' + pure_key]['figure_path'] = high_light_row_fig_path
        if 'highlighted_cells' in prompt:
            prompt['vision_high_light_cell' + pure_key] = {}
            prompt['vision_high_light_cell' + pure_key]['prompt'] = prompt_without_table + ' Please look at table in the picture below. '
            prompt['vision_high_light_cell' + pure_key]['figure_path'] = high_light_cell_fig_path
    return prompt
            
    
    
    
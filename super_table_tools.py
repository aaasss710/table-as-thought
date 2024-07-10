import ast

def process_dict_string(dict_string):
    # Convert string to dictionary
    try:
        dictionary = ast.literal_eval(dict_string)
    except (ValueError, SyntaxError) as e:
        return f"Error parsing string: {e}"
    
    return dictionary

def numeric_tool(super_table, column_name, operation_name):
    value_list = []
    system_message = ""
    for row in super_table:
        if column_name in row:
            try:
                value_list.append(row[column_name])
            except TypeError as e:
                system_message += "Type Error: " + str(e) + "\n"
                break
            
            if not isinstance(row[column_name], (int, float)):
                system_message += f"{row[column_name]} is not a numeric value in row {row["row_id"]}, please consider using update_row to fix it\n"
    if not value_list:
        return "No numeric values found in the column."
    if system_message:
        return system_message
    if operation_name == "mean":
        return sum(value_list) / len(value_list)
    elif operation_name == "sum":
        return sum(value_list)
    elif operation_name == "max":
        return max(value_list)
    elif operation_name == "min":
        return min(value_list)
    else:
        return f"Operation '{operation_name}' not supported."
    
def bool_tool(super_table, column_name, operation_name):
    value_list = []
    system_message = ""
    for row in super_table:
        if column_name in row:
            try:
                value_list.append(row[column_name])
            except TypeError as e:
                system_message += "Type Error: " + str(e) + "\n"
                break
            
            if not isinstance(row[column_name], bool):
                system_message += f"{row[column_name]} is not a boolean value in row {row["row_id"]}, please consider using update_row to fix it\n"
    if not value_list:
        return "No boolean values found in the column."
    if system_message:
        return system_message
    if operation_name == "count_true":
        return value_list.count(True)
    elif operation_name == "count_false":
        return value_list.count(False)
    elif operation_name == "all":
        return all(value_list)
    elif operation_name == "any":
        return any(value_list)
    else:
        return f"Operation '{operation_name}' not supported."

def is_time(value):
    if isinstance(value, dict):
        if any (key in value for key in ["year", "month", "day", "hour", "minute", "second"]):
            return True
    return False

def is_after(reference_time, time):
    """Check if the time is after the reference time."""
    if time["year"] >= reference_time["year"]:
        return True
    elif time["year"] == reference_time["year"]:
        if time["month"] >= reference_time["month"]:
            return True
        elif time["month"] == reference_time["month"]:
            if time["day"] >= reference_time["day"]:
                return True
            elif time["day"] == reference_time["day"]:
                if time["hour"] >= reference_time["hour"]:
                    return True
                elif time["hour"] == reference_time["hour"]:
                    if time["minute"] >= reference_time["minute"]:
                        return True
                    elif time["minute"] == reference_time["minute"]:
                        if time["second"] >= reference_time["second"]:
                            return True
    return False

def is_before(reference_time, time):
    """Check if the time is before the reference time."""
    if time["year"] <= reference_time["year"]:
        return True
    elif time["year"] == reference_time["year"]:
        if time["month"] <= reference_time["month"]:
            return True
        elif time["month"] == reference_time["month"]:
            if time["day"] <= reference_time["day"]:
                return True
            elif time["day"] == reference_time["day"]:
                if time["hour"] <= reference_time["hour"]:
                    return True
                elif time["hour"] == reference_time["hour"]:
                    if time["minute"] <= reference_time["minute"]:
                        return True
                    elif time["minute"] == reference_time["minute"]:
                        if time["second"] <= reference_time["second"]:
                            return True
    return False
def time_tool(super_table, column_name):
    value_list = []
    system_message = ""
    for row in super_table:
        if column_name in row:
            try:
                value_list.append(row[column_name])
            except TypeError as e:
                system_message += "Type Error: " + str(e) + "\n"
                break
            
            if not is_time(row[column_name]):
                system_message += f"{row[column_name]} is not a datetime value in row {row["row_id"]}, please consider using update_row to fix it\n"

    if system_message:
        return system_message
    
    return value_list


def auto_check(super_table, constrains):
    system_message = ""
    for constraint in constrains:
        if constraint["operation_name"] in ["mean", "sum", "max", "min"]:
            result = numeric_tool(super_table, constraint["key"], constraint["operation_name"])
            if isinstance(result, str):
                system_message += result
            else:
                for relational_operator_name, value_to_compare in constraint["relational_operator"].items():
                    if relational_operator_name == "greater_than":
                        if result <= value_to_compare:
                            system_message += f"{constraint['operation_name']} of {constraint['key']} is not greater than {value_to_compare}\n"
                    elif relational_operator_name == "less_than":
                        if result >= value_to_compare:
                            system_message += f"{constraint['operation_name']} of {constraint['key']} is not less than {value_to_compare}\n"
                    elif relational_operator_name == "equal_to":
                        if result != value_to_compare:
                            system_message += f"{constraint['operation_name']} of {constraint['key']} is not equal to {value_to_compare}\n"
                    elif relational_operator_name == "not_equal_to":
                        if result == value_to_compare:
                            system_message += f"{constraint['operation_name']} of {constraint['key']} is equal to {value_to_compare}\n"
                    elif relational_operator_name == "greater_than_or_equal_to":
                        if result < value_to_compare:
                            system_message += f"{constraint['operation_name']} of {constraint['key']} is not greater than or equal to {value_to_compare}\n"
                    elif relational_operator_name == "less_than_or_equal_to":
                        if result > value_to_compare:
                            system_message += f"{constraint['operation_name']} of {constraint['key']} is not less than or equal to {value_to_compare}\n"
                    else:
                        assert False,  f"Relational operator '{relational_operator_name}' not supported.\n"
        elif constraint["operation_name"] in ["all", "any"]:
            result = bool_tool(super_table, constraint["key"], constraint["operation_name"])
            if isinstance(result, str):
                system_message += result
            else:
                for relational_operator_name, value_to_compare in constraint["relational_operator"].items():
                    # if relational_operator_name == "greater_than":
                    #     if result <= value_to_compare:
                    #         system_message += f"{constraint['operation_name']} of {constraint['key']} is not greater than {value_to_compare}\n"
                    # elif relational_operator_name == "less_than":
                    #     if result >= value_to_compare:
                    #         system_message += f"{constraint['operation_name']} of {constraint['key']} is not less than {value_to_compare}\n"
                    # elif relational_operator_name == "equal_to":
                    #     if result != value_to_compare:
                    #         if constraint["operation_name"] in  ["count_true", "count_false"]:
                    #             system_message += f"{constraint['operation_name']} of {constraint['key']} is not equal to {value_to_compare}\n"
                    #         elif constraint["operation_name"]  == "all":
                    #             system_message += f"{constraint['operation_name']} of {constraint['key']} is not all {value_to_compare}\n"
                                
                    #         system_message += f"{constraint['operation_name']} of {constraint['key']} is not equal to {value_to_compare}\n"
                    # elif relational_operator_name == "not_equal_to":
                    #     if result == value_to_compare:
                    #         system_message += f"{constraint['operation_name']} of {constraint['key']} is equal to {value_to_compare}\n"
                    # elif relational_operator_name == "greater_than_or_equal_to":
                    #     if result < value_to_compare:
                    #         system_message += f"{constraint['operation_name']} of {constraint['key']} is not greater than or equal to {value_to_compare}\n"
                    # elif relational_operator_name == "less_than_or_equal_to":
                    #     if result > value_to_compare:
                    #         system_message += f"{constraint['operation_name']} of {constraint['key']} is not less than or equal to {value_to_compare}\n"
                    if relational_operator_name == "equal_to":
                        if result != value_to_compare:
                            if constraint["operation_name"] == "all":
                                if value_to_compare:
                                    system_message += f"Some of value in {constraint['key']} is False\n"
                                else:
                                    system_message += f"{constraint['key']} is all True\n"
                            elif constraint["operation_name"] == "any":
                                if value_to_compare:
                                    system_message += f"{constraint['key']} is all False\n"
                                else:
                                    system_message += f"Some of value in {constraint['key']} is True\n"
                    else:
                        assert False,  f"Relational operator '{relational_operator_name}' not supported.\n"
        elif constraint["operation_name"] == "check_time":
            result = time_tool(super_table, constraint["key"])
            if isinstance(result, str):
                system_message += result
            else:
                for relational_operator_name, value_to_compare in constraint["relational_operator"].items():
                    if relational_operator_name == "after":
                        for time in result:
                            if not is_after(value_to_compare, time):
                                system_message += f"{time} is not after {value_to_compare}\n"
                    elif relational_operator_name == "before":
                        for time in result:
                            if not is_before(value_to_compare, time):
                                system_message += f"{time} is not before {value_to_compare}\n"
                    elif relational_operator_name == "in":
                        start_time = value_to_compare["start"]
                        end_time = value_to_compare["end"]
                        for time in result:
                            if not is_after(start_time, time) or not is_before(end_time, time):
                                system_message += f"{time} is not in the time interval from {start_time} to {end_time}\n"
                    elif relational_operator_name == "not_in":
                        start_time = value_to_compare["start"]
                        end_time = value_to_compare["end"]
                        for time in result:
                            if is_after(start_time, time) and is_before(end_time, time):
                                system_message += f"{time} is in the time interval from {start_time} to {end_time}\n"
                    else:
                        assert False,  f"Relational operator '{relational_operator_name}' not supported.\n"
                    
        else:
            assert False,  f"Operation '{constraint['operation_name']}' not supported.\n"
    return system_message

def add_self_constrains(self_check, new_self_check):
    if "constrain_id" in new_self_check:
        if "constrain" in new_self_check:
            self_check[new_self_check["constrain_id"]] = new_self_check["constrain"]
            
        else:
            return "Constrain is missing. Please make sure to include the constrain key in the new_self_check dict.\n"
    else:
        return "Constrain ID is missing. Please make sure to include the constrain_id key in the new_self_check dict.\n"
       
def remove_self_constrains(self_check, constrain_id):
    if constrain_id in self_check:
        self_check.pop(constrain_id)
    else:
        return f"Constrain ID {constrain_id} does not exist.\n"
    return self_check

def add_auto_constrains(auto_check, new_auto_check):
    if "constrain_id" in new_auto_check:
        if "constrain" in new_auto_check:
            if "operation_name" in new_auto_check["constrain"]:
                new_constraint_id = new_auto_check.pop("constrain_id")
                auto_check[new_constraint_id] = new_auto_check
                return auto_check
            else:
                return "Operation name is missing. Please make sure to include the operation_name key in the constrain dict.\n"
        else:
            return "Constrain is missing. Please make sure to include the constrain key in the new_auto_check dict.\n"
    else:
        return "Constrain ID is missing. Please make sure to include the constrain_id key in the new_auto_check dict.\n"    

def remove_auto_constrains(auto_check, constrain_id):
    if constrain_id in auto_check:
        auto_check.pop(constrain_id)
    else:
        return f"Constrain ID {constrain_id} does not exist.\n"
    return auto_check  

def add_force_key(force_keys, new_force_key):
    if "force_key_id" in new_force_key:
        if "key" in new_force_key:
            force_key_id = new_force_key.pop("force_key_id")
            force_keys[force_key_id] = new_force_key
            return force_keys
        else:
            return "Key is missing. Please make sure to include the key key in the new_force_key dict.\n"
    else:
        return "Force Key ID is missing. Please make sure to include the force_key_id key in the new_force_key dict.\n"

def remove_force_key(force_keys, force_key_id):
    if force_key_id in force_keys:
        force_keys.pop(force_key_id)
    else:
        return f"Force Key ID {force_key_id} does not exist.\n"
    return force_keys

def add_row(super_table, constrains, row):
    system_message = auto_check(super_table, constrains)
    if system_message:
        return system_message
    else:
        if "row_id" in row:
            if row["row_id"] not in super_table:
                row_id = row.pop("row_id")
                super_table[row_id] = row
            else:
                return f"Row ID {row['row_id']} already exists. To update the existed row, please use update_row. To add a new row, please use a different row_id. \n"
        else:
            return "Row ID is missing. Please make sure to include the row_id key in the row dict.\n"
    
    return super_table

def remove_row(super_table, row_id):

    if row_id in super_table:
        super_table.pop(row_id)
    else:
        return f"Row ID {row_id} does not exist.\n"
    return super_table

def update_row(super_table, row):

    if "row_id" in row:
        if row["row_id"] in super_table:
            for key, value in row.items():
                if key != "row_id":
                    super_table[row["row_id"]][key] = value
        else:
            return f"Row ID {row['row_id']} does not exist. To add a new row, please use add_row.\n"
    else:
        return "Row ID is missing. Please make sure to include the row_id key in the row dict.\n"

    return super_table
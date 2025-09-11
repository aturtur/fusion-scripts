import json

def parse_json_from_metadata(tool, search):
    current_time = comp.CurrentTime
    metadata = active_tool.Output[current_time].Metadata
    for key, value in metadata.items():
        try:
            if key == search:
                json_data = json.loads(value)
                return json_data
        except:
            pass
    return None

active_tool = comp.ActiveTool()
data = parse_json_from_metadata(active_tool, "Note")

# Example usage
print(data['artist'])
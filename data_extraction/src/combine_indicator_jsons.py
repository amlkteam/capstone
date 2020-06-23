import json
import os

def replace_json_source(json, source_id):
    """returns an article json with the "source" value replaced with a
    dictionary:
    {"id": "<source_id>", "name": "<source_id> News"
    
    input:
        json: article json
        source_id: news source string
    
    use to modify article_json that has a string as the "source" value
    
    """
    
    modified_json = json
    id_string = source_id
    name_string = source_id + " News"
    
    modified_json["source"] = {"id": id_string, "name": name_string}
    
    return modified_json

def combine_article_jsons(json_folder_path, output_filename):
    """writes a combined json file based on all files in the json_folder_path
    
    input:
        json_folder_path: relative folder path containing indicator jsons
        output_filename: name of output file
        
    for each json, the source field is also updated to have a dictionary returned
    by replace_json_source()
    
    """
    
    output_path = json_folder_path + output_filename
    all_article_jsons = []
    
    if not os.path.exists(output_path):
        for json_path in os.listdir(json_folder_path):
            curr_path = json_folder_path + json_path
            if curr_path.endswith(".json"):

                with open(curr_path) as file:
                    indicator_data = json.load(file)
                    for article_json in indicator_data:
                        if article_json["title"]:
                            updated_json = replace_json_source(article_json, "CBC")
                            all_article_jsons.append(updated_json)
        print("TOTAL ARTICLE JSONS: ", len(all_article_jsons))

        with open(output_path, "w") as outfile:
            json.dump(all_article_jsons, outfile)
        print("FILE WRITTEN: ", output_path)
        
    else:
        print("FILE ALREADY EXISTS: ", output_path)

if __name__ == '__main__':
    json_path = "../data/unannotated_data/cbc/"
    output_file = "combined_CBC_articles.json"
    combine_article_jsons(json_path, output_file)
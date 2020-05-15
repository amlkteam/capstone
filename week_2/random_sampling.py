def random_sampling(indicator_name,entries,target_number=25):
    '''takes in an economic indicator's name, and the list containing json-format info of articles related to the indicator.
    return a random sample of target size and save as csv file for annotation use.'''
    
    sample = []
    added_url = set()
    
    while len(sample) < target_number:
        entry = random.choice(entries)
        if entry['url'] not in added_url:
            sample.append(entry)
            added_url.add(entry['url'])
    # reached desired sample size, save to file for annotation
    # change output_folder below. assuming same folder for all samples of different indicators
    output_folder = r'C:\Users\gen80\OneDrive\Documents\MDSlectures\capstone_sentiment_analysis\testout\annotations_small'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(os.path.join(output_folder,indicator_name+"_"+str(target_number)+'_annotations.csv'), 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source','author','title','description','url','urlToImage','publishedAt','content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in sample:
            writer.writerow(item)
        
    return sample
    
#use case
GDP_sample = random_sampling('GDP',GDP_entries,25)
employment_sample = random_sampling('employment',employment_entries,25)
housing_sample = random_sampling('housing',housing_entries,25)
interest_rate_sample = random_sampling('interest_rate',interest_rate_entries,25)
mortgage_rate_sample = random_sampling('mortgage_rate',mortgage_rate_entries,25)
TSX_sample = random_sampling('TSX',TSX_entries,25)
from youtube_search import YoutubeSearch

results = YoutubeSearch('marshmello alone', max_results=10).to_dict()

print(results)
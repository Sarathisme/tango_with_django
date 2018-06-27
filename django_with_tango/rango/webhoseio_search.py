import webhoseio

def config():
    webhoseio.config(token='570cccf0-2b47-4e79-a295-75e93b47349a')

def get_results(query):
    config()
    final_output = []
    output = webhoseio.query("filterWebContent", {"q":query})
    for post in output['posts']:
        final_output.append({'title': post['title'], 'text': post['text'][0:200], 'url': post['url']})
    return final_output

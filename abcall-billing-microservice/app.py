from chalice import Chalice

app = Chalice(app_name='abcall-billing-microservice')


@app.route('/billing')
def index():
    raise Exception
    return {'hello': 'world'}

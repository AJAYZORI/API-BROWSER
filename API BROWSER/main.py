from flask import Flask, request, render_template, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

    url = ""
    method = "GET"
    headers = ""
    body = ""
    token_url = ""
    client_id = ""
    client_secret = ""
    access_token = ""
    result = None

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'api_request':
            url = request.form['url']
            method = request.form['method']
            headers = request.form.get('headers', '')
            body = request.form.get('body', '')

            try:
                parsed_headers = eval(headers) if headers else {}
                response = requests.request(
                    method=method,
                    url=url,
                    headers=parsed_headers,
                    data=body,
                    verify=False
                )
                result = {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'body': response.text
                }
                session['history'].append({
                    'url': url,
                    'method': method,
                    'status': response.status_code
                })
                session.modified = True
            except Exception as e:
                result = {'error': str(e)}

        elif form_type == 'token_request':
            token_url = request.form['token_url']
            client_id = request.form['client_id']
            client_secret = request.form['client_secret']

            try:
                payload = {
                    'grant_type': 'client_credentials',
                    'client_id': client_id,
                    'client_secret': client_secret
                }
                response = requests.post(token_url, data=payload, verify=False)
                access_token = response.json().get('access_token', 'Token not found')
            except Exception as e:
                access_token = f"Error: {str(e)}"

    return render_template(
        'index.html',
        result=result,
        history=session['history'],
        url=url,
        method=method,
        headers=headers,
        body=body,
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token
    )

if __name__ == '__main__':
    app.run(debug=True)

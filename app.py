from flask import Flask, request, render_template
import controller

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    url = request.form['url']
    print(url)
    result = controller.main(url)
    output = result
    # output['status'] = 'Your input was ' + result['url']
    # output['input'] = 'Your input was ' + result['url']
    # output['msg'] = 'Your input was ' + result['url']

    return render_template('index.html', output=output)



if __name__ == '__main__':
    app.run(debug=True)
import datetime
import yahoo_finance as yf
from flask import Flask, render_template, request, redirect
import bokeh.plotting as bp

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
	return render_template('index.html', y = str(datetime.date.today().year),
	m = str(datetime.date.today().month), d = str(datetime.date.today().day))

@app.route('/submit', methods=['POST'])
def submit():
    ticker = request.form['ticker']
    ticker = ticker.upper()
    stock = yf.Share(ticker)
    begin_year = int(request.form['begin_year'])
    begin_month = int(request.form['begin_month'])
    begin_day = int(request.form['begin_day'])
    end_year = int(request.form['end_year'])    
    end_month = int(request.form['end_month'])
    end_day = int(request.form['end_day'])
    begin = datetime.date(begin_year, begin_month, begin_day)
    end = datetime.date(end_year, end_month, end_day)
    hist = stock.get_historical(str(begin), str(end))
    years = [int(x['Date'].split("-")[0]) for x in hist]
    months = [int(x['Date'].split("-")[1]) for x in hist]
    days = [int(x['Date'].split("-")[2]) for x in hist]
    x = [datetime.date(y, m, d) for y, m, d in zip(years, months, days)]
    price = request.form['features']
    if price == 'Open':
       y = [y['Open'] for y in hist]
    if price == 'High':
       y = [y['High'] for y in hist]
    if price == 'Close':
       y = [y['Close'] for y in hist]
    if price == 'Adj. Close':
       y = [y['Adj_Close'] for y in hist]
    bp.output_file("templates/results.html", title = "Stock Results")
    p = bp.figure(tools="pan,box_zoom,reset,save", title = ticker + ' (' + price + ")",
	x_axis_label='date', x_axis_type = "datetime", y_axis_label='price ($)')
    p.line(x, y, line_width = 2)
    bp.save(p)
    return render_template('results.html')

if __name__ == '__main__':
  app.run(port=33507)

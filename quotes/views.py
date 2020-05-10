from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.
def home(request):
	import requests
	import json
	
	if request.method == 'POST':
		ticker = request.POST['ticker_symbol']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_2be0c25c873f445e95766973b213f85f")
	
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {"api" : api})

	else:
		return render(request, 'home.html', {"ticker" : "Enter a ticker symbol above"})


def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added"))
			return redirect("add_stock")

	else:
		ticker_symbol = Stock.objects.all()
		output = []

		for ticker_item in ticker_symbol:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_2be0c25c873f445e95766973b213f85f")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {"ticker": ticker_symbol, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Delete successful"))
	return redirect(delete_stock)


def delete_stock(request):
	ticker_symbol = Stock.objects.all()
	return render(request, 'delete_stock.html', {"ticker": ticker_symbol})


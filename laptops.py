from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import time

filename = f'laptops.csv'
f = open(filename, 'a')
headers = 'name, description, old price, price, discount, monthly\n' 
f.write(headers)


print('This is for Educational Purposes Only')
print('Press ctrl + C to exit.')
start = int(input("From page: "))
end = int(input("To page: "))
time.sleep(3)
print('Fetching Data.... Please wait!')

for page_num in range(start, end + 1): 
	url = f'https://www.abenson.com/computers-gadget/laptops-computers/page/{page_num}.html'

	request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
	webpage = urlopen(request_site)
	webpage_html = webpage.read()
	webpage.close()

	page_soup = soup(webpage_html, "html.parser")

	#item container
	products = page_soup.findAll("li", {"class":"product-item"})


	for product in products:
		#product name
		product_name = product.findAll('a', {'class':'product-item-link'})
		product_name = product_name[0].text.strip()
		product_name = product_name.replace(',' , '')

		#product desciption
		product_desc = product.findAll('div', {'class':'description'}) 
		product_desc = product_desc[0].text.strip()
		product_desc = product_desc.replace(',' , ' |')

		#old price before sale
		old_price = product.findAll('span', {'class':'old-price'})
		if not old_price:
			old_price = ''
		else:
			old_price = old_price[0].text.strip()
			old_price = old_price.replace("₱" , "")
			old_price = old_price.replace("," , "")


		new_price = product.findAll('span', {'class':'special-price'})
		if not new_price:
			new_price = product.findAll('span', {'class':'price'})
			new_price = new_price[0].text.strip()
			new_price = new_price.replace("₱" , "")
			new_price = new_price.replace("," , "")
		else:
			new_price = new_price[0].text.strip()
			new_price = new_price.replace("₱" , "")
			new_price = new_price.replace("," , "")


		discount = product.findAll('span', {'class':'price-box-discount'})
		if not discount:
			discount = 'No discount'
		else:	
			discount = discount[0].text.strip()

		monthly = product.findAll('span', {'class':'abenson-monthly_price'})
		monthly = monthly[0].text
		monthly = monthly.replace("," , "")
		monthly = monthly.replace("₱" , "")
		monthly = monthly.replace("/mo" , "")

		# print(f'Product name: {product_name}')
		# print(f'Product description: {product_desc}')
		# print(f'Old Price: {old_price}')
		# print(f'New Price: {new_price}')
		# print(f'discount: {discount}')
		# print(f'Monthly: {monthly}')
		# print('\r')

		f.write(f'{product_name}, {product_desc}, {old_price}, {new_price}, {discount}, {monthly}\n')

	if page_num == end:
		print('Program Finished.. Thank You..')
	else:
		print('Fetching Data.... Please wait!')
	


f.close()
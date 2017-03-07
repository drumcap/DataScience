# IT news crawler & web api with Flask

##  Introduction
*  Crawled from It news web page and external API.
*  All data stored in MySQL and recent news stored in Redis too.
*  Some function like searching keyword can be used by web API.

##  Link
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/test

##  Database & Server
*  MySQL, Redis
*  AWS - EC2(ubuntu)

##  Data
*  The number of news article : 479
*  The number of comments : 2,927

##	API key issuance
*  Ex. user_id = alexmoon
*  save to Redis http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/auth?user_id=alexmoon

##	User Authentication & keyword search
*  Ex. keyword = 포켓몬
*  id: moonkwoo
*  api: 0e368fcb-2816-43ae-b866-4585bbd62186
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/news/search/포켓몬?user_id=moonkwoo&apikey=0e368fcb-2816-43ae-b866-4585bbd62186

##  recent news
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/news/recent

##  TOP5 news
*  Standard : recent
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/news/top5?sort=new
*  Standard : the number of comment
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/news/top5?sort=comment

##  keyword search in comment & show a page per page_size
*  Ex. keyword = 포켓몬
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/comment/search/포켓몬?page=2&pagesize=2

## Delete news
*  This function is available only when using HTTP mehod [DELETE]
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/news/<newslink>

## Find similar news
*  used Konlpy which is Korean morphological analyzer.
*  This function is available only on the local computer.
*  http://ec2-54-213-221-13.us-west-2.compute.amazonaws.com:5000/similar_news/<news_id>

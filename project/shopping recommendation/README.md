# Personalized item recommendation system in online fashion store



##	Introduction
*  The numerous online fashion stores in Korea recommend ‘some items purchased by other members who purchased this item’ or ‘the most popular items’ to their members. However the accuracy of recommendation is poor.

*  To improve the performance of recommendation, I use collaborative filtering with member's ratings of each item.

##	Language, Tool, Database
*	Python
*	Request, Beautifulsoup (web crawling)
*	Sqlalchemy, pymongo(connect to Database)
*	MySQL(save shopping mall data), MongoDB(save vector, similarity)

##	Data
*	The data is crawled from the popular Korean fashion online shopping mall for women.
*	The number of items :1,030
*	The number of writers : 32,569
*	The number of ratings : 153,803 (0.45% is filled)
*	The ratings of each item are used for collaborative filtering.

##	Collaborative filtering
* Model
	*	User based CF
		*	Using user vector and Similarity between users.
		*	There are more than 500 million similarities between users because the number of writer is 32,569.
		*	More than 300 million data are suitable for MongoDB.
	*	Item based CF
		*	Using item vector and Similarity between items.
		*	The Similarity between items are very low because there is much more writers than products.
	*	Popularity based CF
		*	Do not use any similarities.
		*	It is similar to recommend the popular or best items.
*	Similarity
	*	Cosine
	*	Jaccard
	*	Pearson Correlation
		*	The most of Pearson Correlation is negative, so Pearson Correlation is not suitable for this system.

##	Code stream (in ‘code’ directory)
*	connection.py : (This file is not in directory.) Connection information to database.
*	model.py : Database(MySQL) structure
1. product_crawler.py : Crawl the item's information and each link
	* productdb.py : Save and get the item's information and each link
2. comment_crawler.py : Crawl the writer's rating and ID from each link of items
	* commentdb.py : Save and get the writer's rating and ID
	* sortcommentdb.py : Count the number of rating per user and per item.
3. set_model.py : Compose train, test set and create vector.
	*	traintestdb.py : Divide items and users by train set and test set.
	*	gradedb.py : Create user vector and item vector from train set.
4. batch_similarity.py : Calculate Cosine, Jaccard, Pearson Correlation similarity.
	* similaritydb.py : Save and get the similarity between users and items
5. predict_score.py : Calculate MAE(mean absolute error), Recall, Precision from each model and similarity with threshold.



##	Summary
* with Cosine similarity, threshold is 0.3

Train/Test(95%/5%) | Ppopularity based CF | user bsed CF | item bsed CF
------------------ | -------------------- |--------------| ------------
Recall             | 1.0 				  | calculating  |0.6552
Precision          | 0.0749 			  | calculating  |0.3654


*	The popularity based CF recommends almost new items to users, so recall is 1 and precision is 0.0749. The accuracy of recommendation is poor.
*	The recall of item based CF with cosine similarity (threshold=0.3) is 0.5862 and the precision is 0.3864. The accuracy of recommendation is increase.
*	There is so much blank in data and CF considers blank as 0. This situation brings about degradation of accuracy of recommendation.
*	If real actual purchase history is used as input data, the accuracy of this recommendation system will be increase.

## Link
* Slideshare : http://www.slideshare.net/alexMoon18/ss-70094135
* Linkedin : http://www.linkedin.com/in/alex-moon-99b077132

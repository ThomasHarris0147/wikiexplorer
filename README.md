# Wrote a wiki explorer using python (beautiful soup) and d3.js
Have you ever played the wikipedia game? It goes something like this:
- Given a wiki article, you have to reach another wiki article in as few clicks or in faster time than your opponent.
- For example starting at Albert Einsteins article can you reach the Diary of a Wimpy Kid's article.




Although, it is believed (not sure if its proven) that every article can reach another article eventually, through whatever obscure paths. I wanted to visualize these paths altogether through a long complicated graph. It is not optimized, if you click on a link, it simply backtracks and does not find the fastest path back to root. However, you can get crazy funny results and links that you never thought would exist and also find interesting hotspot articles that seem to be a focal point for many other articles.
![image](https://github.com/user-attachments/assets/ae2fa962-db17-413d-981b-97dec3567262)
As you can see, given a wiki link, it will create a graph showing all links between each wiki article.

Although, there are some ui parameters you can fill in (for optimization purposes)
1. refresh rate - how fast each link is created, if you have strong internet, the graph can grow very fast, can lag your computer alot.
2. number of nodes per branch - some wiki articles can have 2,000 + links in them, this shortens it, for the sake of your computer and the graph.
3. total number of nodes - how many nodes you want to see total
4. reset tree - clears tree, so you can input a new link.
5. a search bar, to find certain links
6. if you click on a node it will highlight orange and the corresponding pink dots are the path back to root. Also the list of nodes on the left will update to show what those links are.
7. you can do step 6. also by clicking on a link in the search bar.


LEFT TODO: optimize it further, maybe apply Barnes-Hut Optimization, because each node is placed and has default d3.js physics applied (you can see at 2000+ nodes, how slow this can be, calculating physics for every node etc.)

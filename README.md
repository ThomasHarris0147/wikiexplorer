# Wrote a wiki explorer using python (beautiful soup) and d3.js
![image](https://github.com/user-attachments/assets/ae2fa962-db17-413d-981b-97dec3567262)
As you can see, given a wiki link, it will create a graph showing all links between each wiki article.

Although, there are some ui parameters you can fill in (for optimization purposes)
1. refresh rate - how fast each link is created, if you have strong internet, the graph can grow very fast, can lag your computer alot.
2. number of nodes per branch - some wiki articles can have 2,000 + links in them, this shortens it, for the sake of your computer and the graph.
3. total number of nodes - how many nodes you want to see total
4. reset tree - clears tree, so you can input a new link. glhf!


LEFT TODO: optimize it further, maybe apply Barnes-Hut Optimization, because each node is placed and has default d3.js physics applied (you can see at 2000+ nodes, how slow this can be, calculating physics for every node etc.)

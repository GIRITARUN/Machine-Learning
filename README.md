
This is an algorithm that implements FP-Growth algorithm(Frequent Pattern).
Indepth explanation can be found here :http://slidewiki.org/deck/1506_fpgrowth-a-frequent-pattern-growth-approach#tree-1506-slide-22049-1-view
Outline: First the frequent items are found and then a table in a very specific format is generated.
The table is then used to create a "Tree", which we traverse and find frequent patterns-This we do recursively at each level
After mining frequent patterns, we check what type of frequent pattern are they(Max pattern, Closed pattern)
Note:Lot of formatting had to be done to get the data in the usable format and also to convert the results into required format in the course


This is an algorithm that implements FP-Growth algorithm(Frequent Pattern). Indepth explanation can be found here :http://slidewiki.org/deck/1506_fpgrowth-a-frequent-pattern-growth-approach#tree-1506-slide-22049-1-view Outline: First the frequent items are found and then a table in a very specific format is generated. The table is then used to create a "Tree", which we traverse and find frequent patterns-This we do recursively at each level After mining frequent patterns, we check what type of frequent pattern are they(Max pattern, Closed pattern) Note:Lot of formatting had to be done to get the data in the usable format and also to convert the results into required format in the course

This readme file provides you a brief description of the contents of this directory.

--Data:

topic-i.txt, i=0,..,4 Input file for frequent pattern mining algorithms format: term1_index term2_index term3_index ... Columns are separated by blank.

vocab.txt
Dictionary that maps term index to term format: term_index term Columns are separated by Tab

pattern0: All the frequent patterns for topic0

Max 0: All the max patterns of topic 0

Closed patterns:
All the closed patterns of topic 0

Additional files:
These files are for your understanding of how we generate topic-i.txt files. paper_raw.txt: raw data of paper titles paper.txt : paper titles after removing stop words, changing to lower case and lemmatization

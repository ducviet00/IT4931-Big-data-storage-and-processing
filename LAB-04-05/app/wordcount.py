from pyspark import SparkContext
sc = SparkContext(appName="WordCount Empyrean")
lines = sc.textFile("hdfs://hadoop-master:9000/user/root/input/10-0.txt")
counts = lines.flatMap(lambda x: x.split(' ')) \
    .map(lambda x: (x, 1)) \
    .reduceByKey(lambda x, y: x+y)
# output = counts.collect()
# for (word, count) in output:
#     print("%s: %i" % (word, count))
counts.saveAsTextFile("hdfs://hadoop-master:9000/user/root/output/output.txt")
sc.stop()
